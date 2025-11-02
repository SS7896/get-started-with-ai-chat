"""Lightweight runner for local tarot demo that avoids Azure-dependent lifespan.

This creates a FastAPI app that includes the existing routes but does not run
the Azure-connected lifespan code found in `src.api.main`.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# Import the routes module from the package
from src.api import routes

app = FastAPI()
app.mount("/static", StaticFiles(directory="api/static"), name="static")

# Redirect root to the demo UI to avoid 500s when visiting '/'
@app.get("/")
def root_redirect():
	return RedirectResponse(url="/tarot")

# Include the existing routes after the redirect so the redirect takes precedence
app.include_router(routes.router)
