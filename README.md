# CodeWhisper 🎤

**为中国程序员打造的语音转文字工具** | Programmer-friendly speech-to-text for Chinese developers

基于 OpenAI Whisper，优先使用中文语音模型，自动纠正编程术语识别错误。让你在开会、技术分享时快速准确地转录代码和技术术语～

目前项目仍在开发中，已在Mac上已实现一个MVP，方法在文末大家可以尝试用用，但是估计转录效果会很差...

欢迎大家提些建议，并共建我们的字典库哦～


---

## 核心理念 💡

**我们为什么做 CodeWhisper？**


其实说实话，做这个项目的动机是我在实习期间每天晚上ChatGPT做实习总结时，手机自带的语音转文字老是把我说的一些专有单词错误转录，啊当然也可能是我发音不准2333
比如：

- 说"Mentor" →  被识别成 "门特尔" ❌（这个好像是走中文模型就会按照音韵去识别对应的汉字，所以识别成这种的情况就正式需要用到我们的纠正字典库，我认为也正是这个项目的意义所在）
- 说"MySQL" → 被识别成 "my circle" ❌
- 说"Docker" → 被识别成 "到克尔" ❌


**我们的方案**：**始终使用中文模型** + **社区维护的纠错字典库**

CodeWhisper 默认用中文模型转录你的语音，然后通过不断完善的术语字典库自动纠正这些高频错误。
大家遇到的新错误，可以通过 Issue 或 PR 反馈给社区。
人越多这个项目越完善哈哈哈～

---

## Features ✨

- 🎯 **中文优先设计**：专为中国程序员工作场景优化

  - 日常记录工作总结？语音输入，准确识别
  - 和领导汇报不想打字？语音输入，排版微调

- 📚 **社区维护的术语字典**：欢迎大家共同建设～
  - 数据库：MySQL, MongoDB, Redis... 
  - 框架：React, Vue, Spring, Flask...
  - 编程语言：Python, Java, C++...
  - 工具：Docker, Git, Nginx... 
  - 概念：API, REST, 提PR, CI/CD...
  - 以及还有其他其他其他...比如工作中的一些常用缩写（好可恶怎么这么多词汇）

- 🚀 **快速转录**：支持多种模型大小
  - `tiny`：最快（40MB，效果有点拉）
  - `base`：较快（平衡速度和准确度，效果还是有点拉）
  - `small`/`medium`/`large`：更准确
  - 推荐用small

---

## Quick Start 🚀

### 安装

```bash
git clone https://github.com/superlls/codewhisper.git
cd codewhisper

python -m venv . venv
source .venv/bin/activate  # macOS/Linux
# 或
. venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Mac使用方式


**支持的音频格式**：MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM


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