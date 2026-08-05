---
name: GPT-SoVITS
type: discriminant
status: core
source: "[[AI伴侣技术栈概述]]"
domain: AI伴侣-语音
---

# GPT-SoVITS

## 类型判定
判别型 — 开源中文声音克隆系统，GPT + SoVITS 双引擎驱动，低门槛高相似度的声音复制方案。

## 类比 ★
### 一句话比喻
GPT-SoVITS 像一个天才模仿艺人的训练营——先用「语言大师」（GPT）学说话的自然节奏，再用「声乐教练」（SoVITS）磨音色，最后 5 秒钟你就能得到一个以假乱真的声音分身。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| GPT 阶段处理文本语义 | 编剧分析台词——理解哪里该停顿、哪里该重读 |
| SoVITS 阶段合成音频 | 声优拿到分析好的剧本——只管用指定音色表演 |
| 5 秒 Zero-shot 克隆 | 综艺节目的「一分钟模仿赛」——听几句就上台模仿 |

## 是什么
GPT-SoVITS 是一个开源的中文声音克隆系统，将声音克隆拆为两个阶段：① GPT 阶段——用 AR（自回归）Transformer 将文本/音素转换为语义 tokens，捕捉语言的韵律和节奏；② SoVITS 阶段——基于 VITS 架构，将 GPT 输出的语义 tokens + 参考音色 embedding 合成为目标音频。这种拆分让它在少量参考音频下也能达到很高的相似度。

## 输入-输出空间
- **输入**: 参考音频（≥5 秒）+ 目标文本 + 可选参考文本（提高准确度）
- **输出**: 以参考音色朗读的音频
- **关键能力**: Zero-shot（不需要训练），Few-shot（微调后相似度更高）

## 正例（≥2 个）
1. **AI 伴侣个性化音色**: 用户上传自己或喜欢的声音 → GPT-SoVITS 克隆 → 伴侣用克隆音色对话
2. **内容创作**: 用特定人物音色朗读文章/解说视频——低门槛 AI 配音工具

## 反例/边界（≥1 个）
1. **ElevenLabs**: 商业声音克隆服务，效果好但闭源、收费、依赖云端——GPT-SoVITS 开源、免费、可本地部署
2. **边界 — 参考音频质量**: 参考音频若有背景噪声、混响或太短（< 3 秒），克隆相似度急剧下降——需要干净、自然的干声

## 详细解释
GPT-SoVITS 的推理流程：
```mermaid
文本 → GPT（AR Transformer） → 语义 tokens（含韵律信息）
参考音频 → Speaker Encoder → 音色 embedding
        ↓                           ↓
    [SoVITS] → HiFi-GAN 声码器 → 目标音频
```
GPT 模型在这里不是「生成文本」而是「将文本转为离散语音 token」，这些 token 编码了发音和韵律。SoVITS 接收这些 token + 音色信息，生成 Mel 频谱，最后由 HiFi-GAN 转波形。社区生态极其活跃，有一键包、Colab、API 封装等大量衍生项目。

## 关系
### → 指向
- [[VITS]] — SoVITS 模块基于 VITS 架构，继承了其端到端高质量合成能力
- [[Voice Cloning]] — GPT-SoVITS 是声音克隆的标杆实现

### ← 被指向
- [[CosyVoice]] — CosyVoice 和 GPT-SoVITS 是中文声音克隆的双雄，各擅胜场
- [[Voice Conversion]] — 声音转换常与 GPT-SoVITS 配合，先转换后合成
