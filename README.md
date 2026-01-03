# CodeWhisper 🎤

**本地语音输入，想喂哪个 AI 就喂哪个 AI** | Local Speech-to-Text for Any AI

基于 OpenAI Whisper，专为中文开发者优化。录完直接复制到剪贴板，不绑定任何大模型平台。

---

## 为什么需要 CodeWhisper？

### 痛点 1：打字速度跟不上思维速度

和 AI 高强度对话时，你的思路文思泉涌，但打字成了瓶颈：

```
你的大脑：💨💨💨 "我想让你帮我优化这个算法，用双指针..."
你的手指：🐢 "我...想...让...你..."
```

**键盘成为了 AI 的牢笼。语音输入是解决人机交互带宽瓶颈的最自然方式。**

### 痛点 2：想用语音，但大厂的方案对中文程序员不友好

你想用语音输入解决打字慢的问题，但各大厂商的语音转文字都有坑：

| 厂商 | 问题 | 来源 |
|------|------|------|
| **ChatGPT** | 超过 20 秒经常崩溃；5 分钟以上录音直接丢失；网络波动全没了 | [OpenAI 官方论坛](https://community.openai.com/t/transcription-failures-with-voice-messages-on-chatgpt/705251) |
| **Gemini** | 中文支持差，语音识别不稳定，用户反馈 "Voice Recognition simply does not work" | [Google 支持社区](https://support.google.com/gemini/thread/342537101) |
| **Grok** | 语音模式需要 Premium+ 订阅（付费），普通用户没有 | [Social Media Today](https://www.socialmediatoday.com/news/xai-x-formerly-twitter-adds-grok-voice-mode/740820/) |
| **Mac 自带** | 没有对中文程序员优化，专业术语全错 | - |

> 而且各大厂商针对中文社区并不能做很好的特定优化，加之网络本身就不稳定，更容易出问题。

### 解决思路：Whisper 本地化

发现 ChatGPT 背后用的 **Whisper** 模型转录效果其实很好，问题出在网络和平台限制上。

**所以把 Whisper 提取出来，做成本地工具**：
- 本地运行，不怕断网
- 不绑定任何平台，想喂哪个 AI 就粘贴到哪个

### 兜底思路：大模型可以救场

这里有个关键洞察：**大模型天然具备兜底能力**。

一个句子中即使有一两个词识别错了，并不影响整个语义。下游的大模型能通过上下文捕获你的真实意图：

```
你说的："帮我用双指针解决这个力扣题"
识别成："帮我用双只针解决这个利扣题"
大模型：完全理解 ✅（上下文推断）
```

**所以语音输入层有些小错误没关系，下游大模型会兜底。整体问题不大。**

当然，能更准确肯定更好——这就是为什么 CodeWhisper 还做了术语字典纠正。

---

## CodeWhisper 的解决方案

```
┌─────────────────────────────────────────────────────────┐
│  🎙️ 本地录音（Mac 菜单栏 / Windows 悬浮球）                 │
│       ↓                                                 │
│  🧠 Whisper 本地转录（不怕断网、不会吞文本）                  │
│       ↓                                                 │
│  🔧 程序员术语自动纠正                                     │
│       ↓                                                 │
│  📋 自动复制到剪贴板                                      │
│       ↓                                                 │
│  🤖 粘贴到任意 AI：ChatGPT / Claude / Gemini / Grok / ... │
└─────────────────────────────────────────────────────────┘
```

**核心优势：**
- ✅ **本地运行**：不依赖网络，不会断联吞文本
- ✅ **不绑定平台**：想和哪个 AI 聊就粘贴到哪个
- ✅ **中文程序员优化**：400+ 术语纠正规则，社区共建
- ✅ **可迁移架构**：代码与字典低耦合，可迁移至医疗、法律等行业

---

## Quick Start 🚀

### ⚠️ 系统依赖 - FFmpeg

CodeWhisper 依赖 **FFmpeg** 来解析音频文件。

```bash
# 检查是否已安装
ffmpeg -version

# macOS
brew install ffmpeg

# Windows
winget install ffmpeg
```

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/superlls/CodeWhisper.git
cd CodeWhisper

# 2. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # macOS
# 或 .venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt
```

### 启动

```bash
python app.py
```

---

## 使用方式

### Mac 菜单栏应用

启动后，点击菜单栏的 🎙️ 图标：

| 状态 | 含义 |
|------|------|
| 🎙️ | 待命状态 |
| 🔴 | 正在录音 |
| ⏳ | 正在转录 |
| ✅ | 转录完成（自动复制到剪贴板）|

**工作流程**：
1. 点击菜单栏 🎙️ → "开始录音"
2. 说出你的内容
3. 再次点击 → "停止录音"
4. 转录结果自动复制到剪贴板
5. 粘贴到任意 AI 使用

**模型配置**：默认为 `medium`，如需修改请在 `gui/mac_menu_bar_app.py` 中设置 `CodeWhisper(model_name="...")`

### Windows 悬浮球应用

启动后会出现桌面悬浮球：
- 点击开始录音，再次点击停止录音
- 转写完成后自动复制到剪贴板

**模型配置**：默认为 `small`，如需修改请在 `gui/win_floating_ball_app.py` 中设置 `CodeWhisper(model_name="...")`

---

---

## 硬件加速支持 ⚠️

### 

**默认情况**：依赖包使用 CPU 进行 Whisper 模型推理。如果你有 NVIDIA 显卡，可以启用 GPU 加速。

#### ⚡ NVIDIA 显卡加速（推荐）

```bash
# 1. 检查 CUDA 版本
nvidia-smi

# 2. 安装 GPU 版 PyTorch
pip uninstall -y torch torchaudio torchvision

# CUDA 12.1（较新）
pip install torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cu121

# CUDA 11.8（较旧）
pip install torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cu118

# 3. 验证：启动时显示 "device=cuda" 即成功
python app.py
```

**显存不足处理**：如果报错 `CUBLAS_STATUS_ALLOC_FAILED`，改用更小的模型（`small` 或 `base`）

#### ❌ AMD 显卡

- Windows 下 Whisper 暂不支持 ROCm 环境，只能使用 CPU

#### 🍎 Mac

- 使用 CPU 运行（Apple Silicon 会自动优化）
- 如果想减小 CPU 占用，可将模型改为 `small` 或 `base`


## 误打误撞的附加功能 ✨

> 这个项目本来是想做一个**写日报的工具**。在了解 Whisper 的过程中，发现它对中文转录效果很好，于是基于 Whisper 构建了一套流程：
>
> ```
> 🎙️ 语音输入 → 🧠 Whisper 转录 → 📚 字典兜底命中纠错 → 📋 输出到剪贴板
> ```
>
> 在这个过程中，做了两个针对中文程序员的专门增强：
> 1. **术语字典兜底**：Whisper 识别错的术语，用字典规则纠正
> 2. **动态提示词**：根据你常用的术语，自动优化 Whisper 的识别偏好
>
> 后来发现，这套东西用来和各大 AI 对话也很好用，就变成了现在的样子。

### 🧠 可学习的术语纠错引擎

**双重优化机制**：兜底命中 + 自适应学习

#### 1️⃣ 术语字典兜底纠错

各大语音识别对程序员术语的识别都很差，CodeWhisper 自动纠正：

| 说的话 | 普通识别 | CodeWhisper |
|--------|----------|-------------|
| 提PR | "提皮啊" ❌ | 提PR ✅ |
| 双指针 | "双只针" ❌ | 双指针 ✅ |
| MySQL | "my circle" ❌ | MySQL ✅ |
| 排期 | "排气" ❌ | 排期 ✅ |
| Redis | "瑞迪斯" ❌ | Redis ✅ |

#### 2️⃣ 智能学习系统

```mermaid
graph LR
    A[构建提示词] --> B[用户说话]
    B --> C[字典修正]
    C --> D[检测用户高频词]
    D --> E[描绘用户画像]
    E --> F[优化下次识别]
    F --> B
```

**示例**：
```bash
# 初始状态
提示词：计算机行业从业者：提测、联调、排期、上线、Vue、React、数据库、日志、Git。

# 使用一段时间后（你经常说 SpringBoot、Dubbo、Redis、Kafka）
提示词：计算机行业从业者：提测、联调、Dubbo、Redis、Kafka、SpringBoot、MySQL、并发、缓存。
       ↑ 系统自动检测到你的高频术语，识别出你是后端开发工程师，持续优化相关术语识别率
```

---

### 📚 社区驱动的术语字典

**覆盖 13+ 大分类，400+ 条术语规则**（持续收录大家提供的术语～）：

| 分类 | 示例术语 |
|------|----------|
| 职场术语 | 提PR/提MR、提测、排期、逾期、联调、灰度、验收、权限、工单、复盘、风险评估、需求拆解... |
| 大学、八股文术语 | 秋招、春招、校招、社招、offer、CV、实习、技术栈、笔试、面试、刷题、年包、SP、SSP、上岸... |
| 编程语言 | Python、Java、Go、JavaScript、TypeScript、Rust、C++、C#、PHP、Ruby、Kotlin... |
| 开发工具 | IDEA、VSCode、WebStorm、PyCharm、Goland、Vim、Emacs、Postman、Git、GitHub、GitLab... |
| 技术概念 | API、REST、GraphQL、SQL、ORM、CRUD、MVC、日志、Token、Header、密钥对、设计模式... |
| 前端开发 | Vue（持续补充，欢迎 PR） |
| 后端开发 | Spring、SpringBoot、Kafka、Zookeeper、Apollo、Caffeine、CAT、Arthas、RPC、Cron、QPS、TPS... |
| 数据库 | MySQL、PostgreSQL、MongoDB、Redis、ES、DB、DBA、慢SQL、字段、生产库、缓存击穿、缓存雪崩... |
| DevOps工具 | Docker、Kubernetes、K8s、Git、GitHub、GitLab、Maven、Gradle、npm、Yarn、CI/CD、流水线... |
| 运维 | Nginx、Apache、内网、代理、重启、监控告警、日志追踪、服务治理... |
| 硬件与操作系统 | macOS、Windows、Linux、STM32、ARM、虚拟内存、写时复制... |
| 通信协议 | HTTP、HTTPS、SSL、会话、TCP、UDP、三次握手、四次挥手、KeepAlive... |
| 其他术语 | 依赖、高并发、高可用、高性能、微服务、分布式、容器、心跳机制... |

> 完整规则见 `dictionaries/programmer_terms.json`，如有遗漏欢迎提 Issue/PR 补充～

**社区字典双重作用**：
1. ✅ **兜底纠错**：识别错误时立即命中并修正
2. ✅ **自主学习**：检测你常用的术语并构建个人词库，动态识别你的方向，持续优化识别率

---

### 🔧 低耦合架构

**完全配置文件驱动，代码与业务零耦合**：

```
config/
├── base_config.json    # 行业配置（前缀、参数）
├── base_dict.json      # 通用术语库
└── user_dict.json      # 个人学习词库（自动生成）
```

**迁移到其他行业仅需 2 步**：

```bash
# 从"计算机行业"切换到"医疗行业"

# 1. 修改配置信息
将 config/base_config.json 的 "计算机行业从业者：" 改为 "医疗行业从业者："
将 config/base_dict.json 替换为医疗常用术语

# 2. 替换字典库
将 dictionaries/programmer_terms.json 替换为医疗行业字典库
```

> 你也可以根据自己的方向，边用边调整字典，个性化定制属于自己的语音识别工具。

---

### 🚀 模型选择

| 模型 | 速度 | 准确度 | 适用场景 |
|------|------|--------|----------|
| tiny | 最快 | 一般 | 快速草稿 |
| base | 快 | 较好 | 日常使用 |
| small | 中等 | 好 | Windows 默认 |
| medium | 较慢 | 很好 | Mac 默认，推荐 |
| large | 慢 | 最好 | 专业场景 |



## License 📄

MIT License - 详见 [LICENSE](./LICENSE)

## 参与贡献 ❤️

如果你发现术语字典中缺少某个术语或遇到了新的变体，欢迎提 Issue 或 PR：

- 🐛 报告转录错误和识别问题
- 📝 添加新的术语修正规则
- 👀 反馈 Bug 或添加新功能
- 📚 联系邮箱：1656839861un@gmail.com

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)