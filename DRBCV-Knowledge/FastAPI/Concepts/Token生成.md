---
name: Token生成
type: procedure
status: core
source: "[[44-头条项目-用户注册-生成Token_原文]]"
domain: FastAPI
---

# Token生成

## 类型判定
procedure — 三步生成流程：UUID 生成随机字符串 → 设置 7 天过期时间 → 写入/更新 token 表。

## 类比 ★
### 一句话比喻
Token 就像银行发给你的银行卡——注册或登录成功后，银行（后端）给你一张卡（Token 字符串），以后刷卡（携带 Token）就能证明你的身份，不用每次都输密码。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| UUID 生成 Token | 银行制卡中心随机生成卡号——每张卡号都是唯一的 |
| expires_at（7 天过期） | 银行卡有效期——过期了得重新办 |
| Authorization: Bearer xxx | 刷卡时出示卡片——"看，这是我的卡" |
| 查 token 表 | 银行刷卡时联网验证——"这卡是真的吗？过期没？" |
| HTTP 无状态 | 银行柜员不认人——每次来都得亮卡证明身份 |

## 是什么
Token（访问令牌）是一个由 UUID 生成的随机字符串，存储在 `user_token` 表中，包含用户 ID（外键）、Token 字符串和过期时间（默认 7 天）。它是 HTTP 无状态协议下实现用户登录状态保持的凭证——客户端每次请求在请求头携带 `Authorization: Bearer <token>`，后端验证 Token 有效即可识别当前用户。

## 输入-输出空间（程序型必填）
- **输入**：`user_id: int`（用户主键）、`db: AsyncSession`（数据库会话）
- **输出**：`token: str`（UUID 字符串，如 `a1b2c3d4-...`）
- **前置条件**：`import uuid`、已定义 `UserToken` 模型类（含 user_id、token、expires_at 字段）

## 核心代码 + 步骤表
```python
# ===== models/users.py：Token 表模型类 =====
class UserToken(Base):
    __tablename__ = "user_token"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    token: Mapped[str] = mapped_column(String(255))
    expires_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

# ===== CRUD/users.py：封装 Token 生成方法 =====
import uuid
from datetime import datetime, timedelta

async def create_token(db: AsyncSession, user_id: int) -> str:
    # ① 生成 Token 字符串
    token = str(uuid.uuid4())

    # ② 设置过期时间（当前时间 + 7 天）
    expires_at = datetime.now() + timedelta(days=7)

    # ③ 查库：该用户是否已有 Token
    stmt = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(stmt)
    existing_token = result.scalar_one_or_none()

    if existing_token:
        # 有则更新 Token 和过期时间
        existing_token.token = token
        existing_token.expires_at = expires_at
    else:
        # 无则新增
        new_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(new_token)

    await db.commit()
    return token    # 返回新 Token 给调用方

# ===== routers/users.py：在注册/登录路由中调用 =====
token = await users_crud.create_token(db, user.id)
```

| 步骤 | 代码 | 说明 |
|------|------|------|
| ① 生成 Token | `str(uuid.uuid4())` | UUID4 随机生成，碰撞概率极低 |
| ② 设置过期 | `datetime.now() + timedelta(days=7)` | 7 天有效期，过期需重新登录 |
| ③ 查库判断 | `scalar_one_or_none()` | 有 Token 则更新，无则新增 |
| ④ 写入/更新 | `db.add()` 或直接赋值 + `commit()` | 确保 token 表永远只有一条记录 per user |
| ⑤ 返回 Token | `return token` | 调用方拿到后放入响应 data |

## 正例（≥2 个）
1. **注册即登录**：用户注册成功后立即调用 `create_token()` → 返回 Token，前端保存后可直跳"我的"页面，无需二次登录。
2. **重复登录场景**：用户第二次登录时已有 Token → `existing_token` 不为 None → 更新 Token 和过期时间（刷新有效期），不产生重复记录。
3. **Token 携带方式**：前端每次请求在请求头加 `Authorization: Bearer a1b2c3d4-...`，后端用 `Header` 参数提取验证。

## 反例/边界（≥1 个）
1. **Token 过期**：`expires_at < datetime.now()` → 验证时判定无效，返回"令牌已过期"，前端引导用户重新登录。
2. **Token 伪造**：攻击者随机编一个 Token 发请求 → 查 `user_token` 表找不到 → 返回 401 未授权。
3. **每次新增而不更新**：如果不用"有则更新"逻辑，每次登录都 INSERT 一条 → 一个用户可能有多条 Token 记录，token 表无限膨胀。

## 详细解释
**为什么需要 Token？**
HTTP 是无状态协议——服务器不会记住"上次谁来过了"。Token 就是解决这个问题的通行证：
1. 用户登录/注册 → 后端发 Token
2. 前端存 Token（localStorage / cookie）
3. 每次请求带 Token → 后端验 Token → 知道是谁

**UUID4 的特点**：基于随机数生成，不依赖时间戳或 MAC 地址，碰撞概率约 `3.26 × 10^-16`（基本不可能碰撞）。用 `str()` 转成字符串即可存储和传输。

**过期时间的设计**：
- `timedelta(days=7)`：登录后 7 天内免重新登录
- 过期判断：`db_token.expires_at < datetime.now()` → 已过期
- 安全性：Token 泄露后最多 7 天自动失效（比永久有效安全）

## 关系
### → 指向
- [[用户注册]] (注册成功后生成 Token)
- [[用户登录]] (登录成功后生成 Token)
- [[获取用户信息]] (验证 Token 有效性后才能获取)
- [[UUID模块]] (Token 的生成依赖 UUID)

### ← 被指向
- [[用户模块总结]] (Token 是用户认证链路的核心)
- [[修改用户信息与密码]] (需验证 Token 后才能修改)
