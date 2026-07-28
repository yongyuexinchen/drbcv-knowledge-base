# GPT-SoVITS — 最强中文语音合成开源项目

**Category:** OpenSource
**Date:** 2026-07-23

## Problem
需要一个能同时支持 TTS（文本→语音）和 SVC（语音→语音），且对中文和少样本场景最优化的开源项目。传统的 TTS 和 SVC 是两套独立工具，用户需要在它们之间切换。

## Background
GPT-SoVITS 的创始人也是 RVC 的作者（RVC-Boss），在 RVC 成功后意识到：如果能用语言模型（GPT）处理文本→语义，用 VITS 处理语义→语音，就能用一个框架统一 TTS 和 SVC。

## Existing Solutions
- **RVC**：纯 SVC，不支持 TTS
- **so-vits-svc**：纯 SVC，已 Archive
- **CosyVoice**：纯 TTS（LLM-based），不做 SVC
- **VITS**：端到端 TTS，但少样本效果差

## Project Analysis

| 维度 | 详情 |
|------|------|
| **仓库** | RVC-Boss/GPT-SoVITS |
| **Star** | 60,048（行业最高） |
| **Fork** | 6,542 |
| **License** | MIT |
| **语言** | Python |
| **更新状态** | 非常活跃（2026-07-23） |
| **Issues** | 873 开放 |

**硬件需求**：
- 训练：8-12GB VRAM
- 推理：4-6GB VRAM
- RTF 0.028 on RTX 4060Ti（推理极快）
- 支持 CPU / Apple Silicon

**WebUI**：✅ 完整 + Windows 一键整合包

**核心模块**：
- GPT 模块：文本→语义 token（AR 语言模型）
- SoVITS 模块：语义 token→Mel→波形（VITS2 + HiFiGAN）
- ASR 模块：FunASR/SenseVoice 语音识别
- 预处理模块：UVR5 伴奏分离 + 音频切片

**关键依赖**：
- PyTorch 2.5+
- FunASR / SenseVoice
- HiFiGAN / NSF-HiFiGAN

## Architecture
```
两阶段流水线：
  Stage 1 (GPT): Text → Semantic Tokens
  Stage 2 (SoVITS): Tokens + Ref Audio → Waveform

训练数据需求：
  零样本 TTS: 5 秒参考音频
  少样本微调: 1 分钟录音
  歌声翻唱: 10 分钟+ 数据

版本迭代：
  V1 → V2(768-dim+MRTE) → V2Pro(SV emb) → V3(Flow Matching)
```

## Core Innovation
**统一 TTS+SVC 框架**：一个项目同时解决文本→语音和语音→语音的问题。零样本 TTS + 少样本微调的双模式让用户可以根据场景灵活选择效果和准备成本的平衡点。

**Windows 整合包**：下载→双击→浏览器打开，内置全套数据预处理工具（UVR5 伴奏分离、FunASR 标注、自动切片），不需要任何命令行操作。

## Advantages
- GitHub AI 语音项目最高星标（60k）
- Windows 整合包，开箱即用
- 推理速度极快（RTF 0.028）
- 语雀中文文档 + B站教程 + QQ群
- MIT 许可证
- 跨语言支持（中/英/日/韩/粤）
- 同时支持 TTS 和 VC 模式

## Weakness
- 零样本 TTS 音色相似度不如 RVC（后者需训练）
- 情感/表现力控制不如 CosyVoice 3
- 长文本韵律一致性偶有问题
- V3 与 V2 代码并存，未统一
- 概念多，学习曲线陡

## My Opportunity
面试保底方案：如果 CosyVoice 3 环境出问题，GPT-SoVITS 整合包是最快出效果的替代。同时可以展示"我有两个方案，选型有思考"——CosyVoice 选技术前沿，GPT-SoVITS 选社区成熟度。

## Next Action
1. 下载整合包备用
2. 测试零样本 + 少样本微调效果
3. 对比 CosyVoice 和 GPT-SoVITS 的差异
