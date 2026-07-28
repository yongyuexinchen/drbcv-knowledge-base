---
name: FastAPI项目环境搭建与第一个应用
type: procedure
status: core
source: "[[FastAPI的第一个程序_原文]]"
domain: FastAPI
---

# FastAPI项目环境搭建与第一个应用

## 类型判定
procedure — 四步从零启动：创建虚拟环境 → 安装 FastAPI → 写第一个路由 → 启动并访问 `/docs`。

## 类比 ★
### 一句话比喻
搭建 FastAPI 项目就像**开一家奶茶店**——先租个独立厨房（创建虚拟环境，隔离食材不串味），然后进货全套设备（`pip install fastapi[all]` 一次性买齐），接着挂上第一张菜单（写 `@app.get("/")` 路由），最后打开店门（启动 uvicorn），顾客就能在自助点餐机（`/docs`）上看到你的菜单并试吃了。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 虚拟环境（venv） | 独立后厨——每个项目有自己的调料架，红烧的酱油不影响清蒸的 |
| `pip install fastapi[all]` | 一次性进货——把能用到的食材、工具全买了，省得缺这缺那 |
| `app = FastAPI()` | 办营业执照——创建一个合法经营的店铺实例 |
| `@app.get("/")` | 挂上第一张菜单——"首页：Hello World 套餐" |
| `uvicorn main:app --reload` | 开店门——`--reload` 等于"菜单改了自动换"，不用关门重开 |
| `/docs` Swagger 文档 | 自助点餐机——顾客自己点点屏幕就能试菜，不用喊服务员 |
| `/redoc` 文档 | 一本精美的纸质菜单——只能看不能点，但排版更好 |

## 是什么
FastAPI 项目从零搭建的标准流程：用 `virtualenv` 创建隔离的 Python 环境，用 `pip install fastapi[all]` 安装框架及所有可选依赖，创建 `FastAPI()` 实例并定义第一个路由，通过 `uvicorn` 启动服务后即可在浏览器访问接口和自动生成的 Swagger 交互式文档。

## 核心代码

### 第一步：创建虚拟环境
```bash
# 安装虚拟环境管理工具（只需一次）
pip install virtualenv

# 在指定目录创建虚拟环境
cd D:\my_env
virtualenv fastapi_env

# 激活虚拟环境（Windows）
fastapi_env\Scripts\activate
# 激活后命令行前出现 (fastapi_env) 标识
```

### 第二步：安装 FastAPI
```bash
# 一次性安装 FastAPI + 所有可选依赖（推荐）
pip install fastapi[all]
# 包含：uvicorn、pydantic、starlette、jinja2 等
```

### 第三步：第一个 FastAPI 应用
```python
# main.py
from fastapi import FastAPI

app = FastAPI()                    # 创建应用实例

@app.get("/")                      # 根路径路由
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")          # 路径参数路由
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
```

### 第四步：启动并访问
```bash
uvicorn main:app --reload
# 访问: http://127.0.0.1:8000          → {"message": "Hello World"}
# 访问: http://127.0.0.1:8000/hello/张三 → {"message": "Hello 张三"}
# 文档: http://127.0.0.1:8000/docs      → Swagger 交互式文档
# 文档: http://127.0.0.1:8000/redoc     → ReDoc 只读文档
```

## 正例（≥2 个）
1. **学习每个新技术前建独立环境**：学 FastAPI 建 `fastapi_env`，学 Django 建 `django_env`，各环境的包互不干扰，告别版本冲突噩梦。
2. **项目部署时复现环境**：`pip freeze > requirements.txt` 导出依赖列表，部署服务器上 `pip install -r requirements.txt` 一键恢复完全相同的环境。
3. **多项目并行开发**：同时维护 3 个项目，每个项目独立虚拟环境，不会因为 A 项目升级了某个包导致 B 项目崩溃。

## 反例/边界（≥1 个）
1. **全局环境直接装包**：不建虚拟环境，直接在系统 Python 里 `pip install fastapi` → 做 5 个项目后系统 Python 的 site-packages 变成垃圾场，包的版本冲突找都找不到原因。
2. **只装 `fastapi` 不装 `[all]`**：`pip install fastapi` → 跑起来发现缺 uvicorn，装了 uvicorn 发现缺 jinja2……一个一个补不如一次性装全。
3. **PyCharm 社区版创建项目不显示 FastAPI 选项**：这是正常的——专业版才有 FastAPI 项目模板，社区版手动创建 Python 项目后一样开发，只是少了一种启动按钮。

## 详细解释
`fastapi[all]` 方括号是 pip 的 extras 语法，表示安装该包的所有可选依赖。对于 FastAPI，`[all]` 包含了 uvicorn、httpx、jinja2、python-multipart、itsdangerous 等常用的周边库。

**退出虚拟环境**：在终端输入 `deactivate`，命令行前的 `(fastapi_env)` 标识消失即已退出。

## 关系
### → 指向
- [[FastAPI路由]] (项目创建后的第一件事就是定义路由)
- [[路由装饰器元数据与启动方式]] (三种启动方式的详细说明)
- [[FastAPI框架]] (FastAPI 框架本身的特性概述)

### ← 被指向
- [[FastAPI导学]] (环境搭建是课程的第一步实操)
