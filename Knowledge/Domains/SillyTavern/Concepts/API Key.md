---
name: API Key
type: discriminant
status: unexplored
source: [[知乎-酒馆EP01]]
---

# ⬜ API Key

## 类型判定
**判别型** — 回答「它属于什么？」——归类/识别

## 是什么
连接AI模型服务的密钥

## 输入-输出空间
- **输入**: 一串密钥字符串
- **输出**: {"有权访问", "无权访问"}
- **映射关系**: 从属关系——每个请求判定权限

## 正例
1. **场景A**: 填入有效OpenAI Key→可调用GPT。没Key→酒馆是空壳。
2. **场景B**: 当月额度用完→API返回429，即使Key正确也被拒。

## 反例/边界
1. **常见误解**: 不是"登录密码"——不能登录ChatGPT网页版，只能API调用。
2. **边界**: 泄露后任何人都能以你身份调用API并计费。

## 详细解释
API Key是访问AI模型服务（如OpenAI、Claude）的密钥。在酒馆中填入API Key后，酒馆才能把组织好的提示词发给AI模型并接收回复。API Key按调用量计费，不是登录密码——不能用来登录ChatGPT网页版。


## 细节备注

### 常见平台
| 平台 | 获取方式 |
|------|---------|
| OpenAI | platform.openai.com |
| DeepSeek | platform.deepseek.com |
| Claude | console.anthropic.com |
| 硅基流动 | siliconflow.cn（国内） |

### 安全提示
- Key泄露 = 别人用你的账户计费
- 不要在截图中暴露Key
- 酒馆中Key本地存储，不上传


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系

### ← 被指向
- [[SillyTavern(酒馆)]] (需要)
