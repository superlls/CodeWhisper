# CodeWhisper 🎤

**为中文社区开发者打造的智能语音转文字工�?* | Speech-to-Text for Developers

基于 OpenAI Whisper模型开发构建，配备**社区术语字典**�?*自主优化引擎**，不仅能根据社区术语字典库进行命中纠正，还能**根据你的从事的具体方向，可持续自主学习优�?*

🤓 **功能说明**�?
- 🧠 **社区字典**：Github共建，协助提示词动态构建与兜底命中纠错双重保障
- 🚀 **自主优化**：本地动态构建提示词，针对你的开发方向进行自主优�?
- 🔧 **极致解�?*：代码与字典极低耦合，可迁移至医疗、法律等其他行业

目前 Mac 已上线一�?MVP，Windows 版本开�?

欢迎大家quick start模块进行体验

**支持的音频格�?*：MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM

**❤️参与共建**：如果你发现在术语字典中缺少你从事方向的某个术语或你遇到了某个术语新的变体，请向我们提Issues或提 PR 到字典库，我们每条都会用心查看并收录 💕 具体请跳转贡献指南～

---

## 核心理念 💡

**我们为什么做 CodeWhisper�?*


其实说实话，做这个项目的动机是我在实习期间用GPT做每日总结时，输入法自带的语音转文字功能和GPT的语音文字功能总是把一些特定术语错误转录�?

比如�?

- �?提测" �? 被识别成 "体测" �?

- �?排期" �? 被识别成 "排气" �?

- �?提PR" �? 被识别成 "TPR" �?

- �?MySQL" �?被识别成 "my circle" �?

- �?JSON" �? 被识别成 "Jason" �?

- �?Nginx" �? 被识别成 "NJX" �?

- �?阿波�? �?想识别成Apollo �?

如果你也被这些问题困扰，那么这个项目希望能给你一点小小的帮助�?

总之，我想做一款高集成度同时极具方便的针对中文社区开发者的语音转文字工具，让大家不管是在像上级汇报工作时，还是在进行日报周报撰写时都能高效的完成～

---


## Features �?

### 🧠 可学习的术语纠错引擎

**双重优化机制**：兜底命�?+ 自适应学习

#### 1️⃣ 术语字典兜底纠错

�?OpenAI的Whisper模型识别错误时，我们的社区字典就会自动命中并修正�?
```
�?"阿波�?  �?�?"Apollo"

�?"my circle" �?�?"MySQL"

�?"排气"     �?�?"排期"

�?"体测"     �?�?"提测"

�?"TPR"     �?�?"提PR"
```

#### 2️⃣ **智能学习系统**

**工作原理**�?

```mermaid
graph LR
    A[用户说话] --> B[根据用户画像构建提示词]
    B --> C[字典兜底命中修正]
    C --> D[检测用户高频词]
    D --> E[持续描绘用户画像]
    E --> F[优化下次个性化识别]
    F --> B
```

**预期效果**�?

| 使用�?                   | 使用�?                          | CodeWhisper的特�?            |
|------------------------|-------------------------------|----------------------------|
| 通用提示�?                 | **通用提示�?用户个性化提示�?*            | �?持续描绘用户画像                 |
| 识别"Redis"可能需字典兜底映射进行纠正 | 改变模型特定方向输出文本的分布概率，直接识别"Redis" | 🎯 无需再走字典兜底命中              |
| 知道你是开发者，但是不知道你的具体方�?   | **根据你说的高频词，本地分析你的具体方�?*       | 🧠 无需进行大模型微调，即可实现本地轻量级自主学�?|

**示例**�?
```bash
# 初始状�?
提示词：计算机行业从业者：提测、联调、排期、上线、Vue、React、数据库、日志、Git�?
       
# 使用一段时间后（你经常�?SpringBoot Dubbo、Redis、Kafka�?
提示词：计算机行业从业者：提测、联调、排期、Dubbo、Redis、Kafka、SpringBoot、MySQL、并发、缓存�?
       �?系统自动学习到你的高频术语，并分析出你是一位资深的后端开发工程师�?
```

**技术细�?*�?
- 📊 **频次统计**：记录每个术语的使用次数和时�?
- 🎯 **智能排序**：高频术语优先进入用户个性化提示词库
- 🗑�?**自动淘汰**：低频术语自动移除，保持词库精简
- 💾 **本地存储**：所有数据本地保存，隐私安全

---

### 📚 社区驱动的术语字�?

**覆盖 12+ 大分类，100+ 条术语规�?*（持续收录大家提供的术语～）�?

| 分类 | 包含术语 |
|------|---------|
| 职场术语 | 提PR、提测、排期、逾期、联调、灰度、验收、Mentor、Leader、工�?.. |
| 大学生术�?| 秋招、春招、校招、社招、offer、CV、笔试、面试、大厂、算法、刷�?.. |
| 编程语言 | Python、Java、Go、JavaScript、TypeScript、Rust、C++、C#、PHP、Ruby、Kotlin... |
| 开发工�?| IDEA、VSCode、WebStorm、PyCharm、Goland、Vim、Emacs... |
| 技术概�?| API、REST、GraphQL、SQL、ORM、CRUD、MVC、日志、RESTful... |
| 前端开�?| （待扩展�?|
| 后端开�?| Spring、SpringBoot、Kafka、Zookeeper、Apollo、Caffeine、CAT、Arthas... |
| 数据�?| MySQL、PostgreSQL、MongoDB、Redis、DB、DBA、数据库、慢SQL... |
| DevOps工具 | Docker、Kubernetes、Git、GitHub、GitLab、Maven、Gradle、npm、Yarn、pip、CI/CD... |
| 运维 | Nginx、Apache... |
| 硬件与嵌入式 | macOS、Windows、Linux、STM32、Arduino、树莓派、ARM、RTOS�?1单片�?.. |
| 通信协议 | HTTP、HTTPS、SSL、会�?.. |
| 其他术语 | （待扩展�?|

**社区字典双重作用**�?
1. �?**兜底纠错**：识别错误时立即命中并修�?
2. �?**自主学习**：检测你常用的术语并构建个人词库，动态识别你的方向，持续优化识别�?

---

### 🔧 低耦合架构

**完全配置文件驱动，代码与业务零耦合**�?

```
config/
├── base_config.json    # 行业配置（前缀、参数）
├── base_dict.json      # 通用术语�?
└── user_dict.json      # 个人学习词库（自动生成）
```

**迁移到其他行业仅需 2 �?*�?

```bash
# �?计算机行�?切换�?医疗行业"

# 1. 修改配置信息，动态提示词，圈定Whisper输出方向
将config/base_config.json �?"计算机行业从业者："改为"医疗行业从业�?: 
将config/base_dict.json 替换医疗常用术语

# 2. 替换字典�?
将dictionaries/programmer_terms.json中的开发者字典库变为医疗行业字典�?

```

**可能的迁移场�?*�?
- 💼 **企业行业**：金融、制造、零售、物�?..
- 🏥 **专业领域**：医疗、法律、教育、建�?..
- 🎮 **兴趣领域**：游戏、电竞、影视、音�?..

---

### 🚀 快速转�?

支持多种 Whisper 模型�?
- `tiny`：最�?
- `base`：较�?
- `small`：平衡性能
- `medium`：推荐，高准确度�?.4GB�?
- `large`：最准，专业场景

**性能建议**：电脑性能�?�?`medium` �?`large`

---

## Quick Start 🚀

### 安装

```bash
git clone https://github.com/superlls/CodeWhisper.git
cd CodeWhisper
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# �?
.venv\Scripts\activate  # Windows
pip install -r requirements.txt  # 已按平台拆分：mac �?rumps，Windows �?PySide6
```

`requirements.txt` 使用平台标记，不需要手动注释依赖�?

### ⚠️ 系统依赖 - FFmpeg

CodeWhisper 依赖 **FFmpeg** 来解析音频文件（MP3、MP4、M4A、WAV 等）�?


#### 🔍 检�?FFmpeg 是否已安�?

```bash
ffmpeg -version
若显示版本信息，则说�?FFmpeg 可正常使用�?

Windows 安装 FFmpeg（使�?winget�?
推荐通过 Windows Package Manager（winget�?安装 FFmpeg，这是最稳定、最安全、最易复现的方式之一�?

�?PowerShell 执行�?
winget install Gyan.FFmpeg

安装完成�?务必关闭并重新打开终端 / IDE，否则系统不会加载新的环境变量�?

验证安装�?
ffmpeg -version
如果看到版本号，则安装成功�?



🍎 macOS 安装 FFmpeg

brew install ffmpeg

```


---

### Mac使用方式


```bash
# 启动菜单栏应�?
python app.py
```

应用启动后，点击菜单栏的 🎙�?图标，选择"开始录�?即可�?

- 🎙�?- 待命状�?
- 🔴 - 正在录音
- �?- 正在转录
- �?- 转录完成（自动复制到剪贴板）

**工作流程**�?
1. 点击菜单�?🎙�?�?"开始录�?
2. 说出你的内容
3. 再次点击 �?"停止录音"
4. 转录结果自动复制到剪贴板
5. 粘贴使用
6. 如果要选择不同Whisper模型，请�?gui/mac_menu_bar_app.py 中设�?

---

### Windows 使用方式

```bash
# 启动悬浮球应�?
python app.py
```

启动后会出现桌面悬浮球：
- 点击开始录音，再次点击停止录音
- 转写完成后自动复制到剪贴�?
- 如果要调整模型、行为，可在 `gui/win_floating_ball_app.py` 中设�?

---

## 注意事项 ⚠️

### 系统要求

- **Python 版本**�?.9+
- **网络**：首次运行需要下�?Whisper 模型�?00MB-3GB，取决于选择的模�?medium初次使用需要下�?.4G的模型）

### 硬件加速支持

Whisper 原生支持 GPU 加速，能根据你的硬件自动选择最优方案：

- **NVIDIA 显卡**（游戏本、台式机）：需要安装匹配驱动和 GPU 版 PyTorch，否则会回落到 CPU
  - 安装 GPU 版 Torch（驱动较旧用 cu118，较新可用 cu121）：  
    `pip uninstall -y torch torchaudio torchvision`  
    `pip install torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cu118`  # 或 cu121
  - 日志出现 `设备选择: device=cuda` 说明已用上 GPU；如果报 `CUBLAS_STATUS_ALLOC_FAILED`请改用更小模型（base/small）。
  - 默认模型在 `gui/mac_menu_bar_app.py` / `gui/win_floating_ball_app.py` 的 `CodeWhisper(model_name="...")`，显存紧张可改为 `small`/`base`。

- **AMD 显卡**（如 RX 6750 等）：
  - Whisper暂不支持Windows下的ROCm环境， 默认只跑 CPU

- **Mac**：使用 CPU 运行；如果想减小占用，也可以把默认模型改成 `small`/`base`


### 常见问题

**Q: 转录效果不理想？**

A: 几个解决方案�?

1. **升级模型**：从 `base` 升级�?`small` �?`medium` 或更高级模型，取决于你的硬件性能

2. **个性化模型外微�?*�?
   - 手动微调：初始配置默认后端工程师，如果你是其他方向，麻烦修改config/base_dict.json的通用提示�?
   - 自动微调：多次使用后，你的方向高频术语自动进入提示词，识别准确度提升

3. **补充字典规则**�?
   - 如果字典没有你的术语，可以通过提PR或者Issue反馈
   - 欢迎贡献新的术语或变�?
   
**Q: 自主纠错学习如何工作�?*

A:
- **自动检�?*：每次转录后，系统检测你使用的术�?
- **频次统计**：本地记录每个术语的使用次数和时间，进行动态排�?
- **动态优�?*：用户的高频术语（≥3次，或者你可以选择更多）会自动进入用户个性化术语�?
- **隐私安全**：所有数据本地存储，不上传云�?

欢迎提交 Issue �?PR�?

- 🐛 报告转录错误和识别问�?
- 📝 添加新的术语修正规则
- 👀 反馈Bug或想添加新功�?
- 📚 联系邮箱�?656839861un@gmail.com

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

## License 📄

MIT License - 详见 [LICENSE](./LICENSE)
