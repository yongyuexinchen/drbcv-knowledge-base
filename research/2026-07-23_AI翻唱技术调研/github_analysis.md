# AI 翻唱/语音转换 开源项目 GitHub 全景扫描

> 扫描日期: 2026-07-23
> 目标: 为 demo 应聘选型，面向消费级 GPU（RTX 4060/4070 16GB VRAM）
> 扫描范围: 6 大类别，覆盖 20+ 项目，深度分析 8 个一线项目 + 5 个聚合平台

---

## 一、项目总览 (按 Star 排序)

| # | 项目 | Star | 类别 | License | 定位 |
|---|------|------|------|---------|------|
| 1 | GPT-SoVITS | 60,048 | So-VITS/TTS | MIT | 1 分钟数据即可训练 TTS 模型 |
| 2 | ChatTTS | 39,657 | 对话 TTS | AGPLv3+ | 对话场景生成式语音模型 |
| 3 | OpenVoice | 37,004 | 声音克隆 | MIT | 零样本即时声音克隆（MIT x MyShell） |
| 4 | RVC-WebUI | 36,603 | RVC | MIT | 经典 AI 翻唱/变声 WebUI |
| 5 | Fish-Speech S2 | 31,358 | TTS/SVC | Fish Audio RL | SOTA 开源 TTS，80+ 语言 |
| 6 | so-vits-svc | 28,149 | SVC | AGPLv3 | 歌声转换框架（已 Archive） |
| 7 | CosyVoice 3 | 22,358 | TTS/SVC | Apache-2.0 | 阿里开源多语言语音大模型 |
| 8 | F5-TTS | 14,991 | TTS | MIT | Flow Matching 零样本 TTS |
| 9 | voice-pro | 11,199 | 聚合 WebUI | GPL-3.0 | 集成 E2/F5-TTS/CosyVoice 的 WebUI |
| 10 | voicepaw/so-vits-svc-fork | 9,325 | SVC | NOASSERTION | so-vits-svc 实时版，改进 UI |
| 11 | Bert-VITS2 | 8,778 | TTS/SVC | AGPLv3 | VITS2 + 多语言 BERT |
| 12 | MeloTTS | 7,550 | TTS | MIT | 高质量多语言 TTS (MyShell) |
| 13 | StyleTTS2 | 6,315 | TTS | MIT | 人类级别 TTS（扩散+对抗） |
| 14 | aigcpanel | 5,345 | 聚合平台 | Apache-2.0 | 一站式 AI 数字人系统 |
| 15 | Applio | 3,509 | RVC 分支 | MIT | RVC 的易用版本 |
| 16 | TTS-WebUI | 3,211 | 聚合 WebUI | MIT | Gradio+React 多引擎 TTS 前端 |
| 17 | whisper-vits-svc | 2,863 | SVC | MIT | 歌声转换核心引擎 |
| 18 | diff-svc | 2,714 | DiffSVC | AGPLv3 | 扩散模型歌声转换 |

---

## 二、核心项目深度分析

### 1. GPT-SoVITS ⭐ 推荐度: ★★★★★

```
项目: GPT-SoVITS
GitHub: https://github.com/RVC-Boss/GPT-SoVITS
Star: 60,048 | 语言: Python | 最近更新: 2026-07-23 (活跃)
定位: 强大的少样本语音转换和文本到语音 WebUI
技术栈: GPT + SoVITS + VITS2 + FunASR/SenseVoice ASR
硬件需求: RTF 0.028 on 4060Ti; 支持 CPU/Apple Silicon
          最低 6GB VRAM 可推理; 训练推荐 8GB+
WebUI: ✅ 完整 WebUI，Windows 集成包一键启动 (.bat)
        国内用户可通过语雀文档下载镜像包
社区活跃度:
  - Issues: 873 开放 | Forks: 6,542
  - Bilibili 演示视频，语雀中文文档完善
  - HuggingFace 在线 Demo
核心模块:
  - GPT 模块: 文本→语义 token 转换 (AR 语言模型)
  - SoVITS 模块: 语义 token→Mel 频谱→波形 (VITS2 + HiFiGAN)
  - ASR 模块: 语音识别/伴奏分离/训练集分割
关键依赖:
  - PyTorch 2.5+: 深度学习框架
  - FunASR / SenseVoice: 多语言语音识别
  - HiFiGAN / NSF-HiFiGAN: 声码器
运行方式: 下载集成包 → 双击 go-webui.bat → 浏览器打开
         或 pip install + 启动 webui.py
适用场景:
  - ✅ 最佳: 少样本声音克隆（1 分钟录音→高拟真度）
  - ✅ 零样本 TTS（5 秒样本即可）
  - ✅ 跨语言（中英日韩粤）
  - ⚠️ 歌声翻唱需要更多训练数据（10 分钟+）
demo 就绪度: 🟢 极高
  - Windows 集成包开箱即用，4060Ti 推理速度 0.028 RTF
  - 中文社区最活跃，文档最全
  - 面试展示: 现场用自己声音做 TTS demo → 即时有说服力
```

### 2. ChatTTS ⭐ 推荐度: ★★★★

```
项目: ChatTTS
GitHub: https://github.com/2noise/ChatTTS
Star: 39,657 | 语言: Python | 最近更新: 2026-07-23 (活跃)
定位: 面向日常对话的生成式语音模型
技术栈: LLM + VQ-VAE (DVAE) + 韵律控制
硬件需求: 推理 4GB+ VRAM; 支持 CPU 推理
          开源版为 40k 小时预训练模型
WebUI: ❌ 需要第三方前端 (ChatTTS-ui 7.6k stars)
        官方仅提供 Python API + Colab
社区活跃度:
  - Issues: 62 | Forks: 4,249
  - Discord + QQ 群 (Group 1-4)
  - Awesome-ChatTTS 社区索引项目
核心模块:
  - DVAE: 音频压缩/解压 (VQ-VAE)
  - GPT: 文本→音频 token (自回归)
  - Token-to-Speech: 含韵律预测 (笑声/停顿/插话)
关键依赖:
  - PyTorch
  - vocos: 梅尔频谱转波形
  - vector_quantize_pytorch
运行方式: pip install ChatTTS → Python 脚本推理
适用场景:
  - ✅ 对话式 TTS (高自然度、有情感韵律)
  - ✅ LLM 助手的语音输出
  - ⚠️ 不擅长唱歌/音乐性语音
  - ⚠️ 开源版为 40k 小时基础模型 (非 SFT 版)，有高频噪声水印
demo 就绪度: 🟡 中等
  + 音色自然度业界顶尖
  - 无官方 WebUI，需配合 ChatTTS-ui
  - 模型含噪声水印（防滥用），demo 前需确认效果
  - 适合做"对话助手语音输出"类 demo
```

### 3. OpenVoice ⭐ 推荐度: ★★★

```
项目: OpenVoice
GitHub: https://github.com/myshell-ai/OpenVoice
Star: 37,004 | 语言: Python | 最近更新: 2026-07-23
定位: MIT 开源的零样本即时语音克隆（MIT + 清华 + MyShell）
技术栈: TTS + VITS + VITS2
硬件需求: 推理 4GB+ VRAM
WebUI: ❌ 仅有 Python API
社区活跃度:
  - Issues: 307 | Forks: 4,137
  - 论文 arXiv 2312.01479
核心模块:
  - 基础 TTS 模型: 多语言多说话人语音合成
  - 音色转换器: 源音色→目标音色 (零样本)
  - 风格控制: 情感/口音/节奏/停顿粒度控制
关键依赖:
  - coqui-ai/TTS
  - jaywalnut310/vits
  - daniilrobnikov/vits2
运行方式: pip install openvoice → Python 脚本
适用场景:
  - ✅ 零样本跨语言声音克隆
  - ✅ 商业友好 (MIT License)
  - ⚠️ V2 质量仍不如 GPT-SoVITS/ CosyVoice
  - ⚠️ 学术原型，维护频率低于商业竞品
demo 就绪度: 🟡 中等偏低
  + MIT 协议无商业顾虑
  - 无 WebUI，需自建前端
  - 实际听感不如 GPT-SoVITS
  - 适合论文复现/学术展示
```

### 4. RVC-WebUI ⭐ 推荐度: ★★★★

```
项目: Retrieval-based-Voice-Conversion-WebUI
GitHub: https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI
Star: 36,603 | 语言: Python | 最近更新: 2026-07-23 (活跃)
定位: 简单易用的语音音色转换/变声器框架
技术栈: ContentVec/Hubert + RMVPE + HiFiGAN + top1 检索
硬件需求: 6GB+ VRAM 训练; 支持 CPU/AMD/Intel
          CUDA 11.8 / 12.8 两套依赖
          "即便在较差的显卡上也能快速训练"
WebUI: ✅ 完整 WebUI (训练 + 实时变声 90-170ms 延迟)
        训练推理界面 + 实时变声界面 (两个独立 bat 启动)
社区活跃度:
  - Issues: 551 | Forks: 5,144
  - Bilibili 演示视频
  - AutoDL 云端教程 (5毛钱训练 AI 歌手)
  - RVCv3 预告: 更大参数、更少数据
核心模块:
  - ContentVec/Hubert: 内容特征提取 (防音色泄漏的 top1 检索替换)
  - RMVPE: 人声音高提取 (InterSpeech2023, 根治哑音)
  - HiFiGAN: 声码器
  - 模型融合 (ckpt-merge) + pymss/MSST 伴奏分离
关键依赖:
  - PyTorch 2.7.1+ (RTX 50 系需 CUDA 12.8)
  - fairseq / transformers (Hubert)
  - RMVPE / pymss
运行方式: 安装依赖 → 下载模型 → go-webui.bat
适用场景:
  - ✅ 最佳: AI 翻唱 (训练一个歌手的音色模型 → 替换干声)
  - ✅ 实时变声 (端到端 90ms 延迟)
  - ✅ 少量数据即可 (10 分钟低底噪语音)
  - ⚠️ 不涉及 TTS，纯音色转换
demo 就绪度: 🟢 极高
  + AI 翻唱领域的事实标准，B 站最多教程
  + 效果惊艳 (10 分钟数据 → 高拟真度翻唱)
  + 面试展示: 用自己的歌声换音色 → 视觉+听觉冲击力强
```

### 5. Fish-Speech S2 Pro ⭐ 推荐度: ★★★

```
项目: Fish-Speech
GitHub: https://github.com/fishaudio/fish-speech
Star: 31,358 | 语言: Python | 最近更新: 2026-07-23 (活跃)
定位: SOTA 开源多语言 TTS (Fish Audio 商业公司)
技术栈: Dual-AR (4B+400M) + RVQ 音频编解码 + GRPO RL 对齐
硬件需求: 推理需 8GB+ VRAM (4B 模型)
          官方基准 H200 GPU, RTF 0.195
          SGLang 推理加速可降低延迟
WebUI: ✅ WebUI + CLI + Docker + SGLang Server
社区活跃度:
  - Issues: 9 | Forks: 2,692
  - Discord + QQ 频道
  - HuggingFace 模型 + 官方文档
核心模块:
  - Slow AR (4B): 时间轴主语义码本预测 (Decoder-only)
  - Fast AR (400M): 残差码本生成 (9 个 codebooks)
  - RL 对齐: GRPO 多维度奖励 (语义/指令/音色/偏好)
  - 15,000+ Inline 情感标签 (自然语言控制)
关键依赖:
  - PyTorch
  - SGLang / vLLM-Omni (生产推理)
  - vocos / DAC (音频编解码)
运行方式: pip install fish-speech → WebUI / CLI
适用场景:
  - ✅ 高质量多语言 TTS (80+ 语言, Seed-TTS Eval SOTA)
  - ✅ 精细情感控制 (whisper, excited, angry 等)
  - ✅ 多说话人对话生成
  - ⚠️ 4B 参数重，消费级 GPU 推理慢
  - ⚠️ Fish Audio Research License (非标准开源协议)
demo 就绪度: 🟡 中等
  + 效果在 Seed-TTS Eval 上超越多数商业系统
  - 4B 参数，4060/4070 推理可能卡顿
  - 协议并非 MIT/Apache，商业使用有风险
  - 适合展示最强效果，但硬件门槛偏高
```

### 6. so-vits-svc ⭐ 推荐度: ★★

```
项目: so-vits-svc
GitHub: https://github.com/svc-develop-team/so-vits-svc
Star: 28,149 | 语言: Python | 最近更新: 2026-07-23
定位: SoftVC VITS 歌声转换 (非 TTS，纯音色替换)
技术栈: SoftVC Content Encoder + VITS + NSF HiFiGAN
         4.1 版新增 Whisper-PPG、shallow diffusion、RVC 检索融合
硬件需求: 6GB+ VRAM (推理); 10GB+ VRAM (训练推荐)
WebUI: ❌ 无官方 WebUI
        可用 MoeVoiceStudio 或 voicepaw/so-vits-svc-fork 的 UI
        实时变声可用 w-okada/voice-changer
社区活跃度:
  - Issues: 27 | Forks: 5,048
  - 已进入 Archive 状态！
  - 多个活跃 fork: voicepaw (9.3k) / 34j fork
核心模块:
  - SoftVC/ContentVec: 语音内容特征提取
  - VITS: 语音合成 (无文本中间表示，保音高)
  - NSF HiFiGAN: 声码器 (解决声音中断)
  - Shallow Diffusion: 提升音质
关键依赖:
  - fairseq
  - pyworld / parselmouth (F0)
  - Whisper (Whisper-PPG 模式)
运行方式: Python 脚本 + 预训练模型
适用场景:
  - ✅ 歌声转换 (翻唱)
  - ⚠️ 仓库 Archive，不再维护
  - ⚠️ 对新手不友好，无 WebUI
demo 就绪度: 🔴 低
  - Archive 状态，不推荐新项目使用
  - 建议改用 RVC (同生态) 或 voicepaw fork
  - 仅学术参考价值
```

### 7. CosyVoice 3 ⭐ 推荐度: ★★★★★

```
项目: CosyVoice
GitHub: https://github.com/FunAudioLLM/CosyVoice
Star: 22,358 | 语言: Python | 最近更新: 2026-07-23 (非常活跃)
定位: 阿里达摩院多语言零样本语音合成大模型
技术栈: LLM + Flow Matching + SenseVoice
硬件需求: 0.5B 模型推理 4GB+ VRAM
          TensorRT-LLM 可 4x 加速
          vLLM 支持高并发部署
WebUI: ✅ webui.py (Gradio)
        支持 fastapi/grpc 生产部署 + Docker
社区活跃度:
  - Issues: 757 | Forks: 2,583
  - 钉钉群 + GitHub Issues
  - 论文 + ModelScope + HuggingFace 模型
  - FunAudioLLM 生态 (FunASR, SenseVoice, FunClip)
核心模块:
  - LLM: 文本→语义 token (0.5B 参数, 9 语言 + 18 方言)
  - Flow Matching: 语义 token→Mel 频谱
  - HiFiGAN: Mel→波形
  - 拼音/CMU 音素注音修复 (生产可用)
  - 指令支持: 语种/方言/情感/语速/音量
关键依赖:
  - PyTorch
  - modelscope / huggingface_hub
  - vLLM (可选, 用于生产部署)
运行方式: 克隆仓库 → 下载模型 → python webui.py --port 50000
适用场景:
  - ✅ 零样本语音克隆 (3 秒样本即可)
  - ✅ 多语言 (9 语种 + 18 中文方言)
  - ✅ 流式推理 (150ms 延迟)
  - ✅ 生产部署 (vLLM/TensorRT-LLM/gRPC/Docker)
  - ✅ 中文最强 (阿里达摩院, 中文方言支持业界独一无二)
demo 就绪度: 🟢 极高
  + 中文支持最好 (普通话+18 方言)
  + 流式输出, demo 体验流畅
  + 阿里背书, 持续更新 (6个月从 v1→v3)
  + 面试展示: 多方言语音克隆 → 展示技术深度
```

### 8. F5-TTS ⭐ 推荐度: ★★★★

```
项目: F5-TTS
GitHub: https://github.com/SWivid/F5-TTS
Star: 14,991 | 语言: Python | 最近更新: 2026-07-23 (活跃)
定位: 基于 Flow Matching 的零样本 TTS
技术栈: Diffusion Transformer (DiT) + ConvNeXt V2 + Flow Matching
硬件需求: 推理 4GB+ VRAM; v1 Base 模型
          L20 GPU: RTF 0.0394, 延迟 253ms
          TensorRT-LLM: RTF 0.0402
WebUI: ✅ Gradio WebUI (f5-tts_infer-gradio)
        CLI + Docker + pip 包
社区活跃度:
  - Issues: 59 | Forks: 2,183
  - MLX/ONNX 社区移植版本
  - HuggingFace Space 在线 Demo
核心模块:
  - DiT (Diffusion Transformer): 文本+参考音频→Mel 频谱
  - ConvNeXt V2: 文本特征提取
  - Vocos/BigVGAN: Mel→波形 (可选声码器)
  - Sway Sampling: 推理时步采样优化
关键依赖:
  - PyTorch (支持 NVIDIA/AMD/Intel/Apple Silicon)
  - vocos / BigVGAN
  - FunASR / faster-whisper (评估工具)
运行方式: pip install f5-tts → f5-tts_infer-gradio
适用场景:
  - ✅ 零样本 TTS (不需要微调)
  - ✅ 多风格/多说话人生成
  - ✅ 学术研究 (代码简洁, 论文清晰)
  - ⚠️ 中文效果不如 CosyVoice
demo 就绪度: 🟢 高
  + pip install 即用，对开发者最友好
  + Gradio WebUI 美观
  - 中文效果逊于 CosyVoice/GPT-SoVITS
  - 适合做多语言展示 + 技术架构讲解
```

---

## 三、聚合平台/工具类项目

这类项目本身不开发模型，而是将多个引擎打包在一起提供统一 WebUI。

| 项目 | Star | 集成引擎 | 适用场景 |
|------|------|----------|----------|
| **voice-pro** | 11,199 | E2/F5-TTS, CosyVoice, Edge-TTS, Kokoro, Whisper, Demucs | 创作者一站式工具 |
| **aigcpanel** | 5,345 | 声音合成+声音克隆+视频合成 | AI 数字人系统 |
| **TTS-WebUI** | 3,211 | GPT-SoVITS, CosyVoice, XTTSv2, OpenVoice, StyleTTS2, RVC, Bark 等 20+ | TTS 多引擎前端 |
| **TTS-Audio-Suite** | 1,113 | RVC, CosyVoice 3, F5-TTS, IndexTTS-2, Chatterbox 等 (ComfyUI 节点) | ComfyUI 工作流集成 |
| **ChatTTS-ui** | 7,625 | ChatTTS + API 接口 | ChatTTS 专属 WebUI |

---

## 四、对比决策矩阵

### 4.1 按应用场景推荐

| 应用场景 | 首选 | 次选 | 理由 |
|----------|------|------|------|
| **AI 翻唱** (demo) | RVC-WebUI | GPT-SoVITS | RVC 是该领域标准, 10 分钟数据效果好 |
| **少样本声音克隆** | GPT-SoVITS | CosyVoice 3 | 1 分钟数据即可, WebUI 开箱即用 |
| **零样本声音克隆** | CosyVoice 3 | F5-TTS | CosyVoice 中文最强, 3 秒样本 |
| **对话式 TTS** | ChatTTS | GPT-SoVITS | ChatTTS 韵律自然度无可匹敌 |
| **多语言展示** | CosyVoice 3 | Fish-Speech | 9 语言+18 方言 vs 80+ 语言 |
| **实时变声** | RVC-WebUI | voicepaw fork | RVC 端到端 90ms, 生态最完善 |
| **学术/论文复现** | F5-TTS | OpenVoice | 代码最简洁, pip 安装, 论文清晰 |

### 4.2 按硬件适配 (RTX 4060/4070 16GB VRAM)

| 项目 | 推理 VRAM | 训练 VRAM | 4060/4070 可行? |
|------|-----------|-----------|-----------------|
| GPT-SoVITS | 4-6GB | 8-12GB | ✅ 完美 (RTF 0.028 on 4060Ti) |
| ChatTTS | 4GB | - | ✅ 轻量 |
| OpenVoice | 4GB | 8GB | ✅ |
| RVC-WebUI | 4-6GB | 6-8GB | ✅ 完美 (官方支持 4060 级别) |
| Fish-Speech | 8-12GB | - | ⚠️ 勉强 (4B 参数) |
| CosyVoice 3 | 4-6GB | 8-12GB | ✅ 0.5B 模型完美适配 |
| F5-TTS | 4GB | 8GB | ✅ |
| so-vits-svc | 6GB | 10GB+ | ✅ 推理可行 |

### 4.3 Demo 展示效果评估

| 项目 | WOW 效应 | 准备时间 | 可控性 | 稳定性 | 综合 |
|------|---------|---------|--------|--------|------|
| GPT-SoVITS | ⭐⭐⭐⭐⭐ | 10 分钟 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🥇 |
| CosyVoice 3 | ⭐⭐⭐⭐⭐ | 5 分钟 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🥇 |
| RVC-WebUI | ⭐⭐⭐⭐⭐ | 30 分钟 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 🥈 |
| ChatTTS | ⭐⭐⭐⭐ | 5 分钟 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 🥈 |
| F5-TTS | ⭐⭐⭐⭐ | 5 分钟 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 🥈 |

---

## 五、面试 Demo 推荐方案

### 方案 A: 声音克隆 + 方言 TTS (推荐 ⭐⭐⭐⭐⭐)

**选型**: CosyVoice 3 (主) + GPT-SoVITS (辅)

**Demo 流程**:
1. CosyVoice 3 零样本: 现场录音 3 秒 → 生成普通话→四川话/粤语 TTS
2. CosyVoice 3 指令控制: 同一句话用不同情感/语速/方言播放
3. GPT-SoVITS 少样本: 展示 1 分钟数据微调后的提升效果

**优势**: 技术深度 (LLM-based TTS)、中文特色、阿里背书
**硬件**: RTX 4060 完美适配 (0.5B 模型)
**准备**: 30 分钟 (下载模型 + 安装依赖)

### 方案 B: AI 翻唱 + 实时变声 (视觉冲击 ⭐⭐⭐⭐)

**选型**: RVC-WebUI (主)

**Demo 流程**:
1. 用自己唱的干声 → RVC 转成知名歌手音色
2. 展示实时变声 (90ms 延迟)
3. 模型融合 (ckpt-merge 创造混合音色)

**优势**: 视听冲击力强, B 站风格 demo
**硬件**: RTX 4060 完美适配
**准备**: 1 小时 (需准备干声素材 + 训练 10 分钟数据)

### 方案 C: 对话助手语音交互 (工程展示 ⭐⭐⭐⭐)

**选型**: ChatTTS (主) + ChatTTS-ui

**Demo 流程**:
1. LLM 生成文本 → ChatTTS 自然语音 (有笑声/停顿)
2. 展示多说话人对话
3. 对比传统 TTS vs ChatTTS 的自然度差异

**优势**: 工程化强, 可集成到 AI 伴侣体系
**硬件**: RTX 4060 完美适配
**准备**: 30 分钟

---

## 六、关键发现与建议

### 6.1 行业趋势
1. **从 SVC 向 TTS 融合**: GPT-SoVITS 和 CosyVoice 模糊了 TTS/SVC 边界，一个模型搞定
2. **LLM-based 是未来**: CosyVoice 3、Fish-Speech S2 都采用 LLM 架构，自然度碾压传统方案
3. **中文生态爆发**: CosyVoice (阿里)、GPT-SoVITS (国人主导)、ChatTTS 中文支持均属顶级
4. **流式/实时化**: CosyVoice 150ms 流式、RVC 90ms 实时变声
5. **协议收紧**: ChatTTS CC-BY-NC、Fish-Speech 自有协议，MIT 项目更珍贵

### 6.2 Demo 选型建议
- **面试 JavaScript/全栈岗位** → 方案 A (CosyVoice + GPT-SoVITS)，展示 AI 产品化能力
- **面试 AI/ML 岗位** → 方案 A + 深入讲解 LLM-based TTS 架构
- **面试创意/产品岗位** → 方案 B (RVC 翻唱)，展示产品感觉
- **面试后端/工程岗位** → 方案 C (ChatTTS 集成 LLM)，展示系统集成能力

### 6.3 避坑指南
- ❌ so-vits-svc: Archive 状态，停止维护
- ❌ Fish-Speech S2: 4B 参数太重，单卡 4060 推理慢
- ❌ OpenVoice: V2 效果不如新方案，更新停滞
- ⚠️ ChatTTS: 开源版含水印，demo 前需测试效果
- ⚠️ 协议注意: ChatTTS (CC-BY-NC)、Fish-Speech (自有协议) 不可商用

---

*扫猫完成于 2026-07-23，数据来自 GitHub API + README 深度分析*
