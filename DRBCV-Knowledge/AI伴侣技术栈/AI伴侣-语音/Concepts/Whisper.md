---
name: Whisper
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-语音
---

# Whisper

## 类型判定
判别型 — OpenAI 开源的多语言语音识别模型，ASR 领域的事实标准。

## 类比 ★
### 一句话比喻
Whisper 像一个精通 99 种语言的联合国翻译实习生——你说什么语言它都听得懂，还能告诉你哪句话在音频的第几秒说的，唯一的缺点是偶尔把「吃饭」听成「痴汉」。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| Whisper 多语言识别 | 联合国翻译——99 种语言无缝切换，还能告诉你每句话的时间点 |
| 时间戳输出 | 视频字幕组打轴员——精确标注每句话的起止时间 |
| 本地运行+开源 | 社区图书馆——不用付费也能用，想怎么改就怎么改 |

## 是什么
Whisper 是 OpenAI 于 2022 年开源的通用语音识别模型。基于 Encoder-Decoder Transformer 架构，在 68 万小时多语言、多任务监督数据上训练。独特之处：不是纯 ASR，而是统一处理多语言转录、翻译到英语、语言识别、时间戳四个任务。支持 tiny 到 large 多种尺寸，可在消费级 GPU 甚至 CPU 上运行。

## 输入-输出空间
- **输入**: 音频文件（支持多种格式，内部转为 16kHz 单声道）
- **输出**: 转录文本 + 语言标签 + 逐段/逐词时间戳
- **模型尺寸**: tiny (39M) → base (74M) → small (244M) → medium (769M) → large (1550M)

## 正例（≥2 个）
1. **AI 伴侣语音输入**: 用户说「我今天心情不好」→ Whisper 转录为文本 → LLM 生成安慰回应——端到端延迟 < 1s（用 small 模型 + GPU）
2. **播客/会议转录**: 长音频输入 → Whisper 输出全文 + 时间戳 → 可用于构建可搜索的记忆库

## 反例/边界（≥1 个）
1. **纯中文商业 ASR（如讯飞）**: 在中文识别率上可能略优于同尺寸 Whisper，且支持流式识别——Whisper 原生不支持流式，需要第三方改造（如 faster-whisper + VAD 分段）
2. **边界 — 幻觉问题**: Whisper 在静音段有时会「脑补」文字（如重复上一句），需要后处理过滤

## 详细解释
Whisper 的架构：
```python
# 输入：30秒的 80 通道 Log-Mel 频谱图
# Encoder：处理音频 → 生成音频特征
# Decoder：用特殊的 prompt token 控制任务模式
#   <|en|><|transcribe|> → 英语转录
#   <|zh|><|translate|> → 翻译为英语
```
在 AI 伴侣中的典型集成：
```
麦克风 → VAD 切片 → Whisper (faster-whisper) → 文本 → LLM
```
社区优化：faster-whisper（CTranslate2 后端，速度提升 4x）、whisper.cpp（纯 C++，移动端可用）。

## 关系
### → 指向
- [[ASR]] — Whisper 是 ASR 的具体实现，定义了现代 ASR 的质量标准
- [[VAD]] — Whisper 依赖 VAD 做音频分段，两者常搭配使用

### ← 被指向
- [[AI Agent]] — 语音 Agent 用 Whisper 做语音到文本的转换
- [[TTS]] — 与 TTS 配对构成完整的语音交互管线
