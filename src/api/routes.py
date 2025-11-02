# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.
# See LICENSE file in the project root for full license information.
import json
import logging
import os
from typing import Dict

import fastapi
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from jinja2.exceptions import TemplateNotFound
from fastapi.templating import Jinja2Templates
from azure.ai.inference.prompts import PromptTemplate
from azure.ai.inference.aio import ChatCompletionsClient

from .util import get_logger, ChatRequest
from .search_index_manager import SearchIndexManager
from azure.core.exceptions import HttpResponseError


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
import secrets
# Import tarot module (sibling package under src)
try:
    from ..tarot import tarot as tarot_module
except Exception:
    # If package import fails in some environments, we fall back to None.
    tarot_module = None

security = HTTPBasic()


username = os.getenv("WEB_APP_USERNAME")
password = os.getenv("WEB_APP_PASSWORD")
basic_auth = username and password

def authenticate(credentials: Optional[HTTPBasicCredentials] = Depends(security)) -> None:

    if not basic_auth:
        logger.info("Skipping authentication: WEB_APP_USERNAME or WEB_APP_PASSWORD not set.")
        return
    
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return

auth_dependency = Depends(authenticate) if basic_auth else None

logger = get_logger(
    name="azureaiapp_routes",
    log_level=logging.INFO,
    log_file_name=os.getenv("APP_LOG_FILE"),
    log_to_console=True
)

router = fastapi.APIRouter()
templates = Jinja2Templates(directory="api/templates")


# Accessors to get app state
def get_chat_client(request: Request) -> ChatCompletionsClient:
    return request.app.state.chat


def get_chat_model(request: Request) -> str:
    return request.app.state.chat_model


def get_search_index_namager(request: Request) -> SearchIndexManager:
    return request.app.state.search_index_manager

def serialize_sse_event(data: Dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


@router.get("/", response_class=HTMLResponse)
async def index_name(request: Request, _ = auth_dependency):
    try:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
            },
        )
    except TemplateNotFound:
        # If the original index.html isn't present in this demo environment,
        # redirect to the lightweight tarot demo page which we provide.
        return RedirectResponse(url="/tarot")

@router.post("/chat")
async def chat_stream_handler(
    chat_request: ChatRequest,
    chat_client: ChatCompletionsClient = Depends(get_chat_client),
    model_deployment_name: str = Depends(get_chat_model),
    search_index_manager: SearchIndexManager = Depends(get_search_index_namager),
    _ = auth_dependency
) -> fastapi.responses.StreamingResponse:
    
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "text/event-stream"
    }    
    if chat_client is None:
        raise Exception("Chat client not initialized")

    async def response_stream():
        messages = [{"role": message.role, "content": message.content} for message in chat_request.messages]

        prompt_messages = PromptTemplate.from_string('You are a helpful assistant').create_messages()
        # Use RAG model, only if we were provided index and we have found a context there.
        if search_index_manager is not None:
            context = await search_index_manager.search(chat_request)
            if context:
                prompt_messages = PromptTemplate.from_string(
                    'You are a helpful assistant that answers some questions '
                    'with the help of some context data.\n\nHere is '
                    'the context data:\n\n{{context}}').create_messages(data=dict(context=context))
                logger.info(f"{prompt_messages=}")
            else:
                logger.info("Unable to find the relevant information in the index for the request.")
        try:
            accumulated_message = ""
            chat_coroutine = await chat_client.complete(
                model=model_deployment_name, messages=prompt_messages + messages, stream=True
            )
            async for event in chat_coroutine:
                if event.choices:
                    first_choice = event.choices[0]
                    if first_choice.delta.content:
                        message = first_choice.delta.content
                        accumulated_message += message
                        yield serialize_sse_event({
                                        "content": message,
                                        "type": "message",
                                    }
                                )

            yield serialize_sse_event({
                "content": accumulated_message,
                "type": "completed_message",
            })                        
        except BaseException as e:
            error_processed = False
            response = "There is an error!"
            try:
                if '(content_filter)' in e.args[0]:
                    rai_dict = e.response.json()['error']['innererror']['content_filter_result']
                    errors = []
                    for k, v in rai_dict.items():
                        if v['filtered']:
                            if 'severity' in v:
                                errors.append(f"{k}, severity: {v['severity']}")
                            else:
                                errors.append(k)
                    error_text = f"We have found the next safety issues in the response: {', '.join(errors)}"
                    logger.error(error_text)
                    response = error_text
                    error_processed = True
            except BaseException:
                pass
            if not error_processed:
                error_text = str(e)
                logger.error(error_text)
                response = error_text
            yield serialize_sse_event({
                            "content": response,
                            "type": "completed_message",
                        })
        yield serialize_sse_event({
            "type": "stream_end"
            })

    return StreamingResponse(response_stream(), headers=headers)


@router.get("/tarot/draw")
async def tarot_draw(count: int = 1, spread: str = "single"):
    """Endpoint to draw tarot cards. Supports `spread` parameter:

    - single: draw `count` cards (default)
    - three: past/present/future (ignores `count`)
    - cross: Celtic Cross (10 cards)

    Example: GET /tarot/draw?spread=three
    """
    if tarot_module is None:
        raise HTTPException(status_code=500, detail="Tarot module not available")
    try:
        if spread in ("single", ""):
            cards = tarot_module.draw(count)
            # normalize to objects and include a 1-based position for single draws
            cards = [{"position": str(i + 1), **c} for i, c in enumerate(cards)]
        else:
            cards = tarot_module.draw_spread(spread)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"spread": spread, "count": len(cards), "cards": cards}


@router.get("/tarot", response_class=HTMLResponse)
async def tarot_page(request: Request, _ = auth_dependency):
    """Render small tarot UI page."""
    return templates.TemplateResponse("tarot.html", {"request": request})
