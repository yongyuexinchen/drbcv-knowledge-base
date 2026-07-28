# GPT-SoVITS — GPT + VITS 混合语音合成

**Category:** Technology
**Date:** 2026-07-23

## Problem
传统端到端 TTS（如 VITS）将文本理解和声学生成揉在一起，导致：训练不稳定（VAE+Flow+GAN 三合一）、少样本微调困难、跨语言泛化差。

## Background
GPT-SoVITS 的设计者在 RVC 项目成功后发现：1）GPT 擅长语义建模，2）VITS 擅长声学合成。为什么不把两者分开训练？

## Existing Solutions
- **VITS**：端到端 TTS，一个模型做所有事（训练困难）
- **RVC**：纯 SVC，只做音色转换不做 TTS
- **Tacotron2 + WaveGlow**：文本→Mel→波形两阶段（音质差）
- **VALL-E**：微软 EnCodec + LM 方案（未完全开源）

## Important Projects
- **GPT-SoVITS** (60k stars, MIT) — 核心项目，当前最高星标 AI 语音项目
- **RVC-Boss** — 同一作者，RVC 生态延续

## Architecture

**两阶段流水线**：
```
Stage 1 (GPT): Text → Semantic Tokens
  Text → 分词 → GPT AR Model → 离散 semantic token (逐 token 自回归生成)
  训练损失: CrossEntropy (next-token prediction)

Stage 2 (SoVITS): Semantic Tokens + Reference → Waveform
  SSL + Mel + Text → SynthesizerTrn → GAN loss + KL + FM + Mel + Commit
```

**核心模块**：
- **SSL 编码器**：HuBERT (768-dim) → ssl_proj (Conv1d) → RVQ 量化 (1024 bins)
- **GPT 模块**：Llama-style AR Transformer，文本→语义 token
- **MRTE**（Multi-Reference Timbre Encoder）：跨模态 cross-attention，同时接受 ssl_features + text_features + speaker_emb 残差
- **SoVITS 解码器**：VITS2 + HiFiGAN V1
- **V3 新增**：Flow Matching (DiT-based CFM)，22 层 DiT (1024-dim, 16 heads)
- **辅助模块**：UVR5 伴奏分离、FunASR 语音识别、音频切片

**关键设计**：
1. **离散化瓶颈**（RVQ）：连续 HuBERT 特征 → 1024 bin 离散 token，强迫语义压缩
2. **MRTE test 模式**：test=0 正常 / test=1 纯音色克隆 / test=2 纯 TTS，一个模型三种模式
3. **渐进式架构演进**：V1→V2(768-dim+MRTE)→V2Pro(SV emb)→V3(Flow Matching)

## Core Innovation
**两阶段解耦 + MRTE 跨模态音色注入**：将复杂问题拆成两个相对简单的子问题，GPT 负责语义（借用 LLM 强大能力），VITS/CFM 负责声学（借用信号处理成熟方案），MRTE 用 cross-attention 优雅地融合文本和音色信息。

## Advantages
- 少样本之王：1 分钟数据即可微调
- 推理极快：RTF 0.028 on 4060Ti（1400 字≈4 分钟语音仅需 3.36 秒）
- Windows 整合包一键启动
- MIT 许可证，商用友好
- 同时支持 TTS 和 VC 模式
- 中文社区最活跃（语雀文档 + B站教程 + QQ群）

## Weakness
- 两阶段信息损失：GPT 生成的 semantic token 可能丢失韵律/情感细节
- 训练流程分散：Stage 1 和 Stage 2 分别准备数据
- 依赖繁重：FunASR + HuBERT + UVR5 等外部模型
- V3 尚未统一：CFM 路径与原有 VITS 并存
- 少样本翻唱局限：歌声翻唱仍需 10 分钟+数据

## My Opportunity
作为面试 Demo 的保底方案——如果 CosyVoice 3 环境配置出问题，GPT-SoVITS 的 Windows 整合包是最快出效果的替代。同时可以对比展示 TTS vs SVC 两种模式的区别。

## Next Action
1. 下载 GPT-SoVITS Windows 整合包备用
2. 测试零样本 TTS（5 秒参考音频）
3. 对比 V2 和 V3 的音质差异
