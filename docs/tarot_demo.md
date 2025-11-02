# 塔罗模板演示 — 如何运行

本页说明如何在本地启动项目并访问演示模板页面（`/tarot`）。模板是最小交互示例，会调用后端 `/tarot/draw` API 并显示抽到的牌与中文释义。

先决条件
- 已安装 Python 3.8+。
- 在项目根目录。

快速运行（开发模式）

1. 在仓库根目录执行（可选创建虚拟环境）：

```bash
# 设置 PYTHONPATH，使 `src` 包可被导入
PYTHONPATH=src uvicorn "src.api.main:create_app" --factory --reload
```

2. 打开浏览器访问：

```
http://localhost:50505/tarot
```

交互说明
- 在页面选择牌阵（单牌 / 三牌 / 十字），填写张数（单牌时生效），点击“抽牌”按钮。
- 页面将调用 `/tarot/draw` 并把返回结果渲染为卡片。每个卡片对象包含 `position`, `card`, `meaning` 字段。

调试/测试
- 如果想只运行后端抽牌逻辑的单元测试：

```bash
PYTHONPATH=src pytest tests/test_tarot.py
```

如果你希望我把这个模板迁移到前端代码（`frontend`）或做更漂亮的 UI，我可以继续实现。
