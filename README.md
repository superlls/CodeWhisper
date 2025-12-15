# CodeWhisper 🎤

**为中文社区开发者打造的智能语音转文字工具** | Speech-to-Text for Developers

基于 OpenAI Whisper模型开发构建，配备**社区术语字典**和**自主优化引擎**，不仅能根据社区术语字典库进行命中纠正，还能**根据你的从事的具体方向，可持续自主学习优化**

🤓 **功能说明**：
- 🧠 **社区字典**：Github共建，协助提示词动态构建与兜底命中纠错双重保障
- 🚀 **自主优化**：本地动态构建提示词，针对你的开发方向进行自主优化
- 🔧 **极致解耦**：代码与字典低耦合，可迁移至医疗、法律等其他行业

目前已支持 **Mac** 和 **Windows** 两个平台

欢迎大家quick start模块进行体验


**❤️参与共建**：如果你发现在术语字典中缺少你从事方向的某个术语或你遇到了某个术语新的变体，请向我们提Issues或提 PR 到字典库，我们每条都会用心查看并收录 💕 具体请跳转贡献指南～

---

## Quick Start 🚀

### ⚠️ 系统依赖 - FFmpeg

CodeWhisper 依赖 **FFmpeg** 来解析音频文件(MP3, MP4, M4A, WAV 等)。

**如未安装 FFmpeg**,会出现 `WinError 2` 或类似错误。

**检查 FFmpeg 是否已安装:**

```bash
ffmpeg -version
```

**如果未安装,请选择以下方式之一:**

#### 🚀方式:

**Windows:**
```bash
# 或用 Windows Package Manager
winget install ffmpeg

```

**macOS:**
```bash
# 使用 Homebrew(推荐)
brew install ffmpeg
```

---

### 安装

```bash
1.克隆仓库
git clone https://github.com/superlls/CodeWhisper.git
cd CodeWhisper
2.创建虚拟环境(如果Pycharm打开,按照提示创建即可)
python -m venv .venv
source .venv/bin/activate  # macOS
# 或
.venv\Scripts\activate  # Windows
3.安装依赖
pip install -r requirements.txt
依赖会自动根据你的操作系统选择下载相应的版本依赖
```

---

### Mac使用方式

```bash
# 启动菜单栏应用
python app.py
```

应用启动后,点击菜单栏的 🎙️ 图标,选择"开始录音"即可:

- 🎙️ - 待命状态
- 🔴 - 正在录音
- ⏳ - 正在转录
- ✅ - 转录完成(自动复制到剪贴板)

**工作流程**:
1. 点击菜单栏 🎙️ → "开始录音"
2. 说出你的内容
3. 再次点击 → "停止录音"
4. 转录结果自动复制到剪贴板
5. 粘贴使用
6. **模型配置**:默认为 `medium`,如需修改请在 `gui/mac_menu_bar_app.py` 中设置 `CodeWhisper(model_name="...")`

---

### Windows使用方式

```bash
# 启动悬浮球应用
python app.py
```

启动后会出现桌面悬浮球:
- 点击开始录音,再次点击停止录音
- 转写完成后自动复制到剪贴板
- **模型配置**:默认为 `small`,如需修改请在 `gui/win_floating_ball_app.py` 中设置 `CodeWhisper(model_name="...")`

---

## 注意事项 ⚠️

### 系统要求

- **Python 版本**：3.11
- **网络**：首次运行需要下载 Whisper 模型（100MB-3GB，取决于选择的模型,medium初次使用需要下载1.4G的模型）

### 硬件加速支持

**默认情况**：依赖包使用 CPU 进行 Whisper 模型推理。如果你有 NVIDIA 显卡，可以通过以下步骤启用 GPU 加速：

#### ⚡ NVIDIA 显卡加速（推荐）

如果你有 NVIDIA 显卡（游戏本、台式机），安装 GPU 版 PyTorch 后可显著加快转录速度：

**1️⃣ 检查你的 CUDA 版本**

在 PowerShell 或 CMD 中运行：
```bash
nvidia-smi
```

输出示例：
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 545.23.06    Driver Version: 545.23.06   CUDA Version: 12.1     |
+-----------------------------------------------------------------------------+
```

查看 `CUDA Version` 的值，根据版本选择对应的 Torch：
- CUDA 12.1（较新） → 用 `cu121`
- CUDA 11.8 及以下（较旧） → 用 `cu118`

**2️⃣ 根据驱动版本安装对应的 GPU 版 Torch**
```bash
# 先卸载 CPU 版本
pip uninstall -y torch torchaudio torchvision

# 驱动较旧（2024年前）→ cu118
pip install torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cu118

# 驱动较新（2024年后）→ cu121
pip install torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cu121
```

**3️⃣ 验证 GPU 是否启用**
```bash
# 运行应用，查看日志
python app.py
# 如果显示 "设备选择: device=cuda"，说明已成功启用 GPU ✅
```

**4️⃣ 显存不足的处理**
- 如果报错 `CUBLAS_STATUS_ALLOC_FAILED`，说明显存不足
- 解决方案：改用更小的模型（`small` 或 `base`）
- 在 `gui/mac_menu_bar_app.py` 或 `gui/win_floating_ball_app.py` 中修改 `CodeWhisper(model_name="small")`

---

#### ❌ AMD 显卡

- **Windows**：Whisper 暂不支持 Windows 下的 ROCm 环境，目前只能使用 CPU
- **Linux**：可尝试配置 ROCm，但需要额外的环境配置

---

#### 🍎 Mac

- 使用 CPU 运行（Apple Silicon 会自动优化，无需额外配置）
- 如果想减小 CPU 占用，可将默认模型改为 `small` 或 `base`

---

## 核心理念 💡

**我们为什么做 CodeWhisper？**


其实说实话，做这个项目的动机是我在实习期间用GPT做每日总结时，输入法自带的语音转文字功能和GPT的语音文字功能总是把一些特定术语错误转录。

比如：

- 说"提测" →  被识别成 "体测" ❌

- 说"排期" →  被识别成 "排气" ❌

- 说"提PR" →  被识别成 "TPR" ❌

- 说"MySQL" → 被识别成 "my circle" ❌

- 说"JSON" →  被识别成 "Jason" ❌

- 说"Nginx" →  被识别成 "NJX" ❌

- 说"阿波罗" → 想识别成Apollo ❓

如果你也被这些问题困扰，那么这个项目希望能给你一点小小的帮助～

总之，我想做一款高集成度同时极具方便的针对中文社区开发者的语音转文字工具，让大家不管是在像上级汇报工作时，还是在进行日报周报撰写时都能高效的完成～

---

## Features ✨

### 🧠 可学习的术语纠错引擎

**双重优化机制**：兜底命中 + 自适应学习

#### 1️⃣ 术语字典兜底纠错

当 OpenAI的Whisper模型识别错误时，我们的社区字典就会自动命中并修正：
```
❌ "阿波罗"  → ✅ "Apollo"

❌ "my circle" → ✅ "MySQL"

❌ "排气"     → ✅ "排期"

❌ "体测"     → ✅ "提测"

❌ "TPR"     → ✅ "提PR"
```

#### 2️⃣ **智能学习系统**

**工作原理**：

```mermaid
graph LR
    A[构建提示词] --> B[用户说话]
    B --> C[字典修正]
    C --> D[检测用户高频词]
    D --> E[描绘用户画像]
    E --> F[优化下次识别]
    F --> B
```

**预期效果**：

| 使用前                    | 使用后                           | CodeWhisper的特点             |
|------------------------|-------------------------------|----------------------------|
| 通用提示词                  | **通用提示词+用户个性化提示词**            | ⚡ 持续描绘用户画像                 |
| 识别"Redis"可能需字典兜底映射进行纠正 | 改变模型特定方向输出文本的分布概率，直接识别"Redis" | 🎯 无需再走字典兜底命中              |
| 知道你是开发者，但是不知道你的具体方向    | **根据你说的高频词，本地分析你的具体方向**       | 🧠 无需进行大模型微调，即可实现本地轻量级自主学习 |

**示例**：
```bash
# 初始状态
提示词：计算机行业从业者：提测、联调、排期、上线、Vue、React、数据库、日志、Git。
       
# 使用一段时间后（你经常说 SpringBoot Dubbo、Redis、Kafka）
提示词：计算机行业从业者：提测、联调、排期、Dubbo、Redis、Kafka、SpringBoot、MySQL、并发、缓存。
       ↑ 系统自动检测到你的高频术语，并分析出你是一位资深的后端开发工程师～ 
```


---

### 📚 社区驱动的术语字典

**覆盖 12+ 大分类，100+ 条术语规则**（持续收录大家提供的术语～）：

| 分类 | 示例术语 |
|------|---------|
| 职场术语 | 提PR/提MR、提测、排期、逾期、联调、灰度、验收、权限、工单、用例... |
| 大学术语 | 秋招、春招、校招、社招、offer、CV、实习、技术栈、笔试、面试、刷题... |
| 编程语言 | Python、Java、Go、JavaScript、TypeScript、Rust、C++、C#、PHP、Ruby、Kotlin... |
| 开发工具 | IDEA、VSCode、WebStorm、PyCharm、Goland、Vim、Emacs、Postman、master... |
| 技术概念 | API、REST、GraphQL、SQL、ORM、CRUD、MVC、日志、Token、Header、密钥对... |
| 前端开发 | （持续补充，欢迎 PR） |
| 后端开发 | Spring、SpringBoot、Kafka、Zookeeper、Apollo、Caffeine、CAT、Arthas、RPC、Cron... |
| 数据库 | MySQL、PostgreSQL、MongoDB、Redis、ES、DB、DBA、慢SQL、字段、生产库... |
| DevOps工具 | Docker、Kubernetes、K8s、Git、GitHub、GitLab、Maven、Gradle、npm、Yarn、CI/CD、流水线... |
| 运维 | Nginx、Apache、内网、代理、重启... |
| 硬件与嵌入式 | macOS、Windows、Linux、STM32、ARM... |
| 通信协议 | HTTP、HTTPS、SSL、会话... |
| 其他术语 | 依赖（持续扩展） |

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

# 1. 修改配置信息，动态提示词，圈定Whisper输出方向
将config/base_config.json 的 "计算机行业从业者："改为"医疗行业从业者": 
将config/base_dict.json 替换医疗常用术语

# 2. 替换字典库
将dictionaries/programmer_terms.json中的开发者字典库变为医疗行业字典库

```

---

### 🚀 快速转录

支持多种 Whisper 模型：
- `tiny`：最快
- `base`：较快
- `small`：平衡性能
- `medium`：推荐，高准确度（1.4GB）
- `large`：最准，专业场景

**默认模型配置**：
- **Mac**：默认为 `medium`（性能充足）
- **Windows**：默认为 `small`（兼容性考虑）

**如果你想升级模型**，在以下文件中修改 `CodeWhisper(model_name="...")` 参数：
- Mac：`gui/mac_menu_bar_app.py`
- Windows：`gui/win_floating_ball_app.py`

例如改为 `CodeWhisper(model_name="large")` 即可使用更高精度的模型。

## License 📄

MIT License - 详见 [LICENSE](./LICENSE)

欢迎提交 Issue 和 PR：

- 🐛 报告转录错误和识别问题
- 📝 添加新的术语修正规则
- 👀 反馈Bug或想添加新功能
- 📚 联系邮箱：1656839861un@gmail.com

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)
