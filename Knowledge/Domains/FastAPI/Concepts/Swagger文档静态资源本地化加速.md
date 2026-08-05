---
name: Swagger文档静态资源本地化加速
type: procedure
status: core
source: "[[接口文档打开慢的问题_原文]]"
domain: FastAPI
---

# Swagger文档静态资源本地化加速

## 类型判定
procedure — 三步根治：下载三个静态文件到本地 → 修改 `openapi/docs.py` 里的 CDN 地址 → 用 `app.mount()` 挂载静态目录。

## 类比 ★
### 一句话比喻
Swagger 文档打开慢就像**每次点菜都要等服务员去美国总部拿菜单**——一个 JS 文件、一个 CSS 文件、一个图标，全要去国外的服务器下载，等半天下不来。解决方案就是把这三样东西复印一份放在收银台抽屉里（本地 static 目录），顾客一点餐直接从抽屉拿，秒开。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| CDN 静态文件（JS/CSS/PNG） | 美国总部存档的菜单模板——跨国快递，慢 |
| 本地 static 目录 | 收银台抽屉里的菜单复印件——伸手就拿，秒到 |
| 修改 `docs.py` 源码 | 把点餐系统里"去美国拿菜单"的指令改成"从抽屉拿" |
| `app.mount("/static", ...)` | 告诉收银员："抽屉就在这儿，以后菜单从这儿拿" |
| swagger-ui-bundle.js | 点餐机的操作系统——没它界面显示不出来 |
| swagger-ui.css | 菜单的排版样式——没它排版乱糟糟 |
| favicon-32x32.png | 浏览器标签上的小图标——可有可无，有更好 |

## 是什么
FastAPI 的 Swagger 交互式文档（`/docs`）默认从国外 CDN 加载 swagger-ui 的 JS、CSS 和图标文件，导致国内访问极慢甚至打不开。解决方法是将这三个文件下载到本地 `static/` 目录，修改 FastAPI 源码中的引用地址指向本地，然后通过 `app.mount()` 将静态目录挂载为可访问路径。

## 输入-输出空间
- **输入**：下载的 3 个静态文件（swagger-ui-bundle.js、swagger-ui.css、favicon-32x32.png）
- **输出**：`/docs` 页面秒开，不再依赖国外 CDN
- **前置条件**：能访问到这三个文件的原始 CDN 地址（或从别人那里拷贝）

## 核心代码

### 第一步：下载三个静态文件
三个文件的 CDN 地址（来自 FastAPI 源码）：
1. `swagger-ui-bundle.js` — Swagger UI 的核心 JS
2. `swagger-ui.css` — Swagger UI 的样式
3. `favicon-32x32.png` — 图标

将这三个文件下载到项目根目录的 `static/` 文件夹中：
```
project/
├── main.py
└── static/
    ├── swagger-ui-bundle.js
    ├── swagger-ui.css
    └── favicon-32x32.png
```

### 第二步：修改 FastAPI 源码
找到 `site-packages/fastapi/openapi/docs.py`，定位以下三行并修改：

```python
# 原始（从 CDN 加载）—— 注释掉
# swagger_js_url = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"
# swagger_css_url = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css"
# swagger_favicon_url = "https://fastapi.tiangolo.com/img/favicon.png"

# 改为本地路径
swagger_js_url = "/static/swagger-ui-bundle.js"
swagger_css_url = "/static/swagger-ui.css"
swagger_favicon_url = "/static/favicon-32x32.png"
```

### 第三步：挂载静态目录
```python
# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 将 static 目录挂载到 /static 路径
app.mount("/static", StaticFiles(directory="static"), name="static")

# 之后正常定义路由...
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

> 注意：`app.mount()` 必须在所有路由定义**之前**调用，否则可能被路由拦截。

## 正例（≥2 个）
1. **国内开发环境**：没有翻墙工具的开发者，执行这三步后 `/docs` 秒开，开发体验从"等一分钟"变成"瞬间加载"。
2. **企业内网部署**：服务器完全不能访问外网时，将静态文件预先部署到服务器上，内网也能正常使用 Swagger 文档。
3. **生产环境优化**：即使是能访问外网的服务器，本地化静态文件也消除了对三方 CDN 的依赖风险（CDN 挂了不影响你）。

## 反例/边界（≥1 个）
1. **只改源码不改挂载**：把 `docs.py` 里的地址改成了 `/static/...`，但 `main.py` 没有 `app.mount()` → 访问 `/docs` 时 JS/CSS 文件 404，页面白屏。
2. **pip 升级后源码被覆盖**：每次 `pip install --upgrade fastapi` 都会覆盖 `docs.py`，需要重新修改。建议把修改后的 `docs.py` 备份一份。
3. **挂载顺序错误**：`app.mount()` 写在路由之后 → `/static` 路径可能被某个路由匹配劫持，静态文件访问不到。

## 详细解释
`app.mount()` 的第一个参数是**访问路径**（URL 前缀），第二个 `StaticFiles(directory="static")` 中的 `directory` 是**物理目录名**。两者可以不同，但通常保持一致以免混淆。

**ReDoc 文档**（`/redoc`）也会受同样的问题影响，解决方式相同——它需要加载的 JS 文件也来自 CDN。

**一劳永逸**：配置完成后本地所有 FastAPI 项目都受益，因为修改的是全局 site-packages 中的源码。

## 关系
### → 指向
- [[FastAPI项目环境搭建与第一个应用]] (docs 文档在第一个项目中首次遇到)
- [[FastAPI路由]] (/docs 中展示的就是路由信息)

### ← 被指向
- [[FastAPI导学]] (/docs 是 FastAPI 开发的核心工具，必须能用)
