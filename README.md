# CodeWhisper 🎤

**为中文社区开发者打造的语音转文字工具** | Programmer-friendly speech-to-text for developers

基于 OpenAI Whisper，优先使用中文语音模型，自动纠正编程术语识别错误。让你在做日报周报、回复上级消息或是做总结时快速准确地转录职场和技术术语～

目前Mac已上线一个MVP，方法在quick start大家可以尝试体验一下，

（ClI版本仍在开发中，目前仅支持录音文件的优化）

（Windows版本开发已提上日程，预计年底前上线一个MVP）

支持的音频格式：MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM

如果在你的开发领域有一些特定术语希望得到优化，欢迎在此项目的字典里加入你的这个术语，并提交PR！

---

## 核心理念 💡

**我们为什么做 CodeWhisper？**


其实说实话，做这个项目的动机是我在实习期间用ChatGPT做日报总结时，输入法自带的语音转文字老把特定术语错误转录，啊当然也可能是我发音不准哈哈哈
比如：

- 说"Mentor" →  被识别成 "门特尔" ❌ （这个是语音转文字的通病了，走中文模型就会按照音韵去识别对应的汉字。所以如果识别后出现这种的情况，就正是需要用到我们的纠正字典库，我认为也正是这个项目的意义所在）

- 说"MySQL" → 被识别成 "my circle" ❌

- 说"阿波罗" → 想识别成Apollo ❓

- 读出来和写出来的情况完全不一致无法映射的：获取到的 c sharp  → C# ❗

总而言之，我们是想做一款高集成度的针对中文社区开发者的语音转文字工具，让大家不管是在像上级汇报工作时，还是在进行日报周报撰写时都能高效的完成！

---


## Features ✨

- 🎯 **中文优先设计**：专为中文社区程序员工作场景优化

  - 日常记录工作总结？语音输入，准确识别
  - 和领导汇报不想打字？语音输入，排版微调

- 📚 **社区维护的术语字典**：欢迎大家共同建设～
    - 职场特定术语：提PR,提测,排期...(这三个市面上的语音转文字几乎就没对过...特别是中英混合而且英文还是缩写的...对应的错误转录则是TPR,体测，排气) 
    - 数据库：MySQL, MongoDB, Redis... 
    - 框架：React, Vue, Spring, Flask...
    - 编程语言：Python, Java, C++...
    - 工具：Docker, Git, Nginx... 
    - 概念：API, REST, 提PR, CI/CD...
    - 以及还有其他其他其他...

- 🚀 **快速转录**：支持多种模型大小
  - `tiny`：最快
  - `base`：较快
  - `small`/`medium`/`large`
  - 如果你的电脑性能还不错，就使用medium模型吧！

---

## Quick Start 🚀

### 安装

```bash
git clone https://github.com/superlls/CodeWhisper.git
cd CodeWhisper

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows

# ⚠️ Windows 用户注意：安装依赖前，请在 requirements.txt 中注释掉以下两行（在行前加 #）：
#   - rumps          # macOS 专用菜单栏应用库
#   - pyobjc-framework-cocoa  # macOS Objective-C 框架（如有）
# 然后再执行下面的 pip install 命令

pip install -r requirements.txt
```

### ⚠️ 系统依赖 - FFmpeg

CodeWhisper 依赖 **FFmpeg** 来解析音频文件（MP3, MP4, M4A, WAV 等）。

**检查 FFmpeg 是否已安装：**

```bash
ffmpeg -version
```

**如果未安装，请选择以下方式之一：**

#### 🚀 方式 1：自动安装（推荐，所有平台）

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

# 或访问官网手动下载
https://ffmpeg.org/download.html
```

**macOS:**
```bash
# 使用 Homebrew（推荐）
brew install ffmpeg
```


⚠️ **如未安装 FFmpeg**，运行 CLI 时会提示安装，避免出现 `WinError 2` 或类似错误。

---

⚠️ **重要提示**：确保项目文件夹命名为 `CodeWhisper`（不是 `whisper`），避免与 OpenAI Whisper 库包名冲突导致导入错误。
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
- ❌ - 出错

**工作流程**：
1. 点击菜单栏 🎙️ → "开始录音"
2. 说出你的内容
3. 再次点击 → "停止录音"
4. 转录结果自动复制到剪贴板
5. 粘贴使用！
6. 如果要选择不同Whisper模型，请在gui/menu_bar_app.py中设置

---

## 注意事项 ⚠️

### 系统要求

- **Python 版本**：3.9+
- **网络**：首次运行需要下载 Whisper 模型（100MB-3GB，取决于选择的模型,medium初次使用需要下载1.4个G的模型,注意你的流量哦）

### 硬件加速支持

Whisper 原生支持 GPU 加速，能根据你的硬件自动选择最优方案：

- **NVIDIA 显卡**（游戏本、台式机）：✅ 自动检测并使用 CUDA
  - 开箱即用，无需额外配置
  - 推荐 RTX 系列或更新的 GTX 显卡

- **AMD 显卡**（如 RX 6750 等）：需要手动配置 ROCm
  - Whisper 无法自动识别，默认使用 CPU
  - 配置相对复杂，建议参考 [AMD ROCm 官方文档](https://rocm.docs.amd.com/projects/radeon/en/latest/docs/install/native_linux/install-pytorch.html)

- **Mac**：使用 CPU 运行
  - Whisper 暂不支持 Metal 加速
  - 可使用更小的模型（`tiny`/`base`）以提升速度

- **无显卡 / 仅 CPU 运行**：✅ 完全支持
  - 推荐使用 `base` 或 `small` 模型
  - `medium` 模型在 CPU 上运行较慢

### 常见问题

**Q: 转录效果不理想？**

A: 几个解决方案：

1. **升级模型**：从 `base` 升级到 `small` 或 `medium` 或更高级模型，取决于你的硬件性能

   > **💡 为什么大模型更准？** Whisper 的语音识别质量主要取决于模型规模（参数量），而不是原始音频采样率。所有输入音频都会自动重采样到 16kHz，因此录音采样率超过 16kHz 不会提升识别准确度。大模型之所以更准，是因为：
   > - 更强的语言建模能力
   > - 更多训练数据（参数量越大，模型见过的语言现象越多）
   > - 更深的 Transformer 结构
   >
   > 简单来说：**买硬件升级模型，不用买麦克风升级采样率** 😄

2. **改进说话方式**：
   - 说话清楚，语速正常
   - 减少背景噪音

3. **补充字典规则**：
   - 如果字典没有你的术语，可以通过提PR或者Issue 反馈
   - 欢迎贡献新的修正规则！

**Q: 菜单栏应用启动失败？**

A: 检查以下几点：
```bash
# 1. 确保依赖安装完整
pip install -r requirements.txt

# 2. 检查 Python 版本
python --version  # 应该是 3.9+

# 3. 检查 FFmpeg 是否安装
ffmpeg -version
```

**Q: 运行 CLI 遇到 WinError 2 或 ffmpeg not found？**

A: 这说明 FFmpeg 未安装或未添加到 PATH。解决方案：

1. **自动安装（推荐）**：
   ```bash
   python scripts/setup_environment.py
   ```

2. **手动安装**：
   - Windows: `choco install ffmpeg` 或 `winget install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` (Debian/Ubuntu)

3. **验证安装**：
   ```bash
   ffmpeg -version
   ```

**Q: 模型下载太慢？**

A: 这是网络问题，几个办法：
- 使用更小的模型先测试：`tiny` → `base` → `small`
- 科学上网提升网速

**Q: 能否离线使用？**

A: 可以！
- 模型下载后（第一次需要网络）
- 之后就可以完全离线使用
- 字典修正不需要网络

欢迎提交 Issue 和 PR：

- 🐛 报告转录错误和识别问题
- 📝 添加新的术语修正规则
- 🎯 改进转录准确度
- 📚 完善文档
- 📝 bug修复及功能优化
- 🎯 反馈建议：1656839861un@gmail.com

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## License 📄

MIT License - 详见 [LICENSE](./LICENSE)