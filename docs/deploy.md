# 部署说明（本地 Docker 演示 & Azure 部署指引）

本说明包含两部分：在本地用 Docker 运行演示容器，以及如何将服务部署到 Azure（简要步骤）。

本地 Docker 演示

1. 构建镜像：

```bash
docker build -t tarot-demo -f Dockerfile.demo .
```

2. 运行（或使用 docker-compose）：

```bash
# Run with explicit port mapping (default PORT=50505)
docker run -p 50505:50505 -e PORT=50505 --rm tarot-demo
# 或 使用 docker-compose
docker-compose up --build
```

3. 打开浏览器：

```
http://localhost:50505/tarot
```

说明：该镜像使用 `scripts.run_tarot_demo:app` 启动一个不依赖 Azure 的 FastAPI 应用，适合本地演示、CI 测试或快速验收。

部署到 Azure App Service（简要）

1. 登录 Azure CLI 并选择订阅：

```bash
az login
az account set -s <SUBSCRIPTION_ID>
```

2. 创建资源组与容器注册表（如果尚未创建）。

3. 使用 Azure CLI 将容器镜像推送到 ACR 或 Docker Hub：

```bash
# 登录 ACR
az acr login --name <ACR_NAME>
docker tag tarot-demo <ACR_NAME>.azurecr.io/tarot-demo:latest
docker push <ACR_NAME>.azurecr.io/tarot-demo:latest
```

4. 在 Azure App Service 中创建 Web App for Containers，选择刚推送的镜像并启动。

5. 配置环境变量（如果要使用真实 `create_app()` 并启用 Azure-lifespan），在 App Service 的 Application Settings 中配置:

- AZURE_EXISTING_AIPROJECT_ENDPOINT
- AZURE_AI_CHAT_DEPLOYMENT_NAME
- 以及其它在 `src/api/main.py` 中使用的 Azure 环境变量

建议
- 对于快速演示使用 `Dockerfile.demo`（无需 Azure 凭证）。
- 若要生产化部署并使用 Azure AI 服务，请使用原始 `src/Dockerfile` 并确保环境变量与托管权限配置正确。
