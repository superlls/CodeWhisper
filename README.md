# CodeWhisper 🎤

**为中文社区开发者打造的智能语音转文字工具** | Speech-to-Text for Developers

基于 OpenAI Whisper模型开发构建，配备**社区术语字典**和**自主优化引擎**，不仅能根据社区术语字典库进行命中纠正，还能**根据你的从事的具体方向，可持续自主学习优化**

🤓 **功能说明**：
- 🧠 **社区字典**：Github共建，协助提示词动态构建与兜底命中纠错双重保障
- 🚀 **自主优化**：本地动态构建提示词，针对你的开发方向进行自主优化
- 🔧 **极致解耦**：代码与字典极低耦合，可迁移至医疗、法律等其他行业

目前Mac已上线一个MVP，CLI版本持续优化中，Windows版本开发已提上日程

欢迎大家quick start模块进行体验

**支持的音频格式**：MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM

**❤️参与共建**：如果你发现在术语字典中缺少你从事方向的某个术语或你遇到了某个术语新的变体，请向我们提Issues或提 PR 到字典库，我们每条都会用心查看并收录 💕 具体请跳转贡献指南～

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
    A[用户说话] --> B[根据用户画像构建提示词]
    B --> C[字典兜底命中修正]
    C --> D[检测用户高频词]
    D --> E[持续描绘用户画像]
    E --> F[优化下次个性化识别]
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
       ↑ 系统自动学习到你的高频术语，并分析出你是一位资深的后端开发工程师～ 
```

**技术细节**：
- 📊 **频次统计**：记录每个术语的使用次数和时间
- 🎯 **智能排序**：高频术语优先进入用户个性化提示词库
- 🗑️ **自动淘汰**：低频术语自动移除，保持词库精简
- 💾 **本地存储**：所有数据本地保存，隐私安全

---

### 📚 社区驱动的术语字典

**覆盖 12+ 大分类，100+ 条术语规则**（持续收录大家提供的术语～）：

| 分类 | 包含术语 |
|------|---------|
| 职场术语 | 提PR、提测、排期、逾期、联调、灰度、验收、Mentor、Leader、工单... |
| 大学生术语 | 秋招、春招、校招、社招、offer、CV、笔试、面试、大厂、算法、刷题... |
| 编程语言 | Python、Java、Go、JavaScript、TypeScript、Rust、C++、C#、PHP、Ruby、Kotlin... |
| 开发工具 | IDEA、VSCode、WebStorm、PyCharm、Goland、Vim、Emacs... |
| 技术概念 | API、REST、GraphQL、SQL、ORM、CRUD、MVC、日志、RESTful... |
| 前端开发 | （待扩展） |
| 后端开发 | Spring、SpringBoot、Kafka、Zookeeper、Apollo、Caffeine、CAT、Arthas... |
| 数据库 | MySQL、PostgreSQL、MongoDB、Redis、DB、DBA、数据库、慢SQL... |
| DevOps工具 | Docker、Kubernetes、Git、GitHub、GitLab、Maven、Gradle、npm、Yarn、pip、CI/CD... |
| 运维 | Nginx、Apache... |
| 硬件与嵌入式 | macOS、Windows、Linux、STM32、Arduino、树莓派、ARM、RTOS、51单片机... |
| 通信协议 | HTTP、HTTPS、SSL、会话... |
| 其他术语 | （待扩展） |

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

**可能的迁移场景**：
- 💼 **企业行业**：金融、制造、零售、物流...
- 🏥 **专业领域**：医疗、法律、教育、建筑...
- 🎮 **兴趣领域**：游戏、电竞、影视、音乐...

---

### 🚀 快速转录

支持多种 Whisper 模型：
- `tiny`：最快
- `base`：较快
- `small`：平衡性能
- `medium`：推荐，高准确度（1.4GB）
- `large`：最准，专业场景

**性能建议**：电脑性能好 → `medium` 或 `large`

---

## Quick Start 🚀

### 安装

```bash
# ⚠️ Windows 用户注意：安装依赖前，请在 requirements.txt 中注释或删除掉以下依赖）：
#   - rumps          # macOS 专用菜单栏应用库
1.克隆仓库
git clone https://github.com/superlls/CodeWhisper.git
cd CodeWhisper
2.创建虚拟环境（如果你是Pycharm打开，按照提示创建即可）
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows
3.安装依赖
pip install -r requirements.txt
```

### ⚠️ 系统依赖 - FFmpeg

CodeWhisper 依赖 **FFmpeg** 来解析音频文件（MP3, MP4, M4A, WAV 等）。

**检查 FFmpeg 是否已安装：**

```bash
ffmpeg -version
```

**如果未安装，请选择以下方式之一：**

#### 🚀 ~~方式 1：自动安装（推荐，所有平台）~~

```bash
python scripts/setup_environment.py
```

这个脚本会自动检测你的系统，并安装相应的 FFmpeg。

#### 方式 2：手动安装

**Windows:**
```bash
# 使用 Chocolatey（推荐）
choco install ffmpeg

# 或使用 Windows Package Manager
winget install ffmpeg

# 或访问官网手动下载，并配置到系统环境
https://ffmpeg.org/download.html
```

**macOS:**
```bash
# 使用 Homebrew（推荐）
brew install ffmpeg
```


⚠️ **如未安装 FFmpeg**，运行 CLI 时会提示安装，避免出现 `WinError 2` 或类似错误。

---
### CLI使用方式

1.将你的录音文件拖入项目根目录下（与cli.py）同级

2.在控制台执行 python cli.py demo.m4a（替换成你的文件名，支持文件格式：MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM）    

### Mac使用方式


```bash
# 启动菜单栏应用
python app.py
```

应用启动后，点击菜单栏的 🎙️ 图标，选择"开始录音"即可：

- 🎙️ - 待命状态
- 🔴 - 正在录音
- ⏳ - 正在转录
- ✅ - 转录完成（自动复制到剪贴板）

**工作流程**：
1. 点击菜单栏 🎙️ → "开始录音"
2. 说出你的内容
3. 再次点击 → "停止录音"
4. 转录结果自动复制到剪贴板
5. 粘贴使用
6. 如果要选择不同Whisper模型，请在gui/menu_bar_app.py中设置

---

## 注意事项 ⚠️

### 系统要求

- **Python 版本**：3.9+
- **网络**：首次运行需要下载 Whisper 模型（100MB-3GB，取决于选择的模型,medium初次使用需要下载1.4G的模型）

### 硬件加速支持

Whisper 原生支持 GPU 加速，能根据你的硬件自动选择最优方案：

- **NVIDIA 显卡**（游戏本、台式机）：✅ 自动检测并使用 CUDA
  - 开箱即用，无需额外配置
  - 推荐 RTX 系列或更新的 GTX 显卡

- **AMD 显卡**（如 RX 6750 等）：需要手动配置 ROCm
  - Whisper 无法自动识别，默认使用 CPU ✅
  - 配置相对复杂，建议使用CPU方案，或参考 [AMD ROCm 官方文档](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-pytorch.html)

- **Mac**：使用 CPU 运行


### 常见问题

**Q: 转录效果不理想？**

A: 几个解决方案：

1. **升级模型**：从 `base` 升级到 `small` 或 `medium` 或更高级模型，取决于你的硬件性能

2. **个性化模型外微调**：
   - 手动微调：初始配置默认后端工程师，如果你是其他方向，麻烦修改config/base_dict.json的通用提示词
   - 自动微调：多次使用后，你的方向高频术语自动进入提示词，识别准确度提升

3. **补充字典规则**：
   - 如果字典没有你的术语，可以通过提PR或者Issue反馈
   - 欢迎贡献新的术语或变体
   
**Q: 自主纠错学习如何工作？**

A:
- **自动检测**：每次转录后，系统检测你使用的术语
- **频次统计**：本地记录每个术语的使用次数和时间，进行动态排序
- **动态优化**：用户的高频术语（≥3次，或者你可以选择更多）会自动进入用户个性化术语库
- **隐私安全**：所有数据本地存储，不上传云端

**Q: 运行 CLI 遇到 WinError 2 或 ffmpeg not found？**

A: 这说明 FFmpeg 未安装或未添加到 PATH。解决方案：


1**手动安装**：
   - Windows: 官网下载并添加到你的Path目录
   - macOS: `brew install ffmpeg`

2**验证安装**：
   ```bash
   ffmpeg -version
   ```


欢迎提交 Issue 和 PR：

- 🐛 报告转录错误和识别问题
- 📝 添加新的术语修正规则
- 👀 反馈Bug或想添加新功能
- 📚 联系邮箱：1656839861un@gmail.com

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

## License 📄

MIT License - 详见 [LICENSE](./LICENSE)