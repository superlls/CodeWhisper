# CodeWhisper 🎤

**为中文社区开发者打造的语音转文字工具** | Programmer-friendly speech-to-text for developers

基于 OpenAI Whisper，优先使用中文语音模型，自动纠正编程术语识别错误。让你在做报告、做总结时快速准确地转录代码和技术术语～

目前项目仍在开发中，已在CLI和Mac上已实现一个MVP，方法在quick start大家可以尝试体验一下～

支持的音频格式：MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM

欢迎大家提些建议，并共建我们的字典库（dictionaries/programmer_terms.json）哦～



---

## 核心理念 💡

**我们为什么做 CodeWhisper？**


其实说实话，做这个项目的动机是我在实习期间用ChatGPT做总结时，输入法自带的语音转文字老把专有单词错误转录，啊当然也可能是我发音不准哈哈哈
比如：

- 说"Mentor" →  被识别成 "门特尔" ❌ （这个好像是语音转文字的通病了，走中文模型就会按照音韵去识别对应的汉字。所以如果识别后出现这种的情况，就正是需要用到我们的纠正字典库，我认为也正是这个项目的意义所在）

- 说"Docker" → 被识别成 "到克尔" ❌

- 说"MySQL" → 被识别成 "my circle" ❌

- 另外还有一种情况：读出来和写出来的情况完全不一致无法映射的：获取到的 c sharp  → C# !!



---

## 中文模式的局限性 ⚠️

使用中文模式转录时，Whisper 的识别结果**不确定**：

```
用户说话：我用 MySQL 和 Redis 做数据库

Whisper 中文模式可能识别为：
✅ MySQL 和 Redis （幸运）
✅ message core 和 瑞迪斯 （中文音韵）
✅ my sql 和 re dis （分隔形式）
❓ 或其他组合...（随机！）
```

**为什么？** 中文模型会优先识别成中文，英文词汇会被转换成同音的中文或拆分成多个词。

**我们的解决方案：** 在字典中收集**所有可能的变体**，覆盖各种识别形式。

```
// 例如 MySQL 的各种变体
"MySQL": {
  "variants": [
    {"wrong": "mysql", "type": "lowercase"},
    {"wrong": "my sql", "type": "split"},
    {"wrong": "message core", "type": "chinese_phonetic"},
    {"wrong": "我的秋儿", "type": "chinese_phonetic_variant"}
  ]
}
```



---



## Features ✨

- 🎯 **中文优先设计**：专为中文社区程序员工作场景优化

  - 日常记录工作总结？语音输入，准确识别
  - 和领导汇报不想打字？语音输入，排版微调

- 📚 **社区维护的术语字典**：欢迎大家共同建设～
  - 数据库：MySQL, MongoDB, Redis... 
  - 框架：React, Vue, Spring, Flask...
  - 编程语言：Python, Java, C++...
  - 工具：Docker, Git, Nginx... 
  - 概念：API, REST, 提PR, CI/CD...
  - 以及还有其他其他其他...比如工作中的一些常用缩写

- 🚀 **快速转录**：支持多种模型大小
  - `tiny`：最快（40MB，效果有点拉）
  - `base`：较快（平衡速度和准确度，效果还是有点拉）
  - `small`/`medium`/`large`（推荐）

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

pip install -r requirements.txt
```

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
- **网络**：首次运行需要下载 Whisper 模型（100MB-3GB，取决于选择的模型）

### 常见问题

**Q: 转录效果不理想？**

A: 几个解决方案：
1. **升级模型**：从 `base` 升级到 `small` 或 `medium`或更高级模型，取决于你的硬件性能

2. **改进说话方式**：
   - 说话清楚，语速正常
   - 减少背景噪音

3. **补充字典规则**：
   - 如果字典没有你的术语，可以通过 Issue 反馈
   - 欢迎贡献新的修正规则！

**Q: 菜单栏应用启动失败？**

A: 检查以下几点：
```bash
# 1. 确保依赖安装完整
pip install -r requirements.txt

# 2. 检查 Python 版本
python --version  # 应该是 3.9+


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


### 性能提示

| 模型 | 大小 | 速度 | 准确度 | 内存占用 | 首次下载 |
|------|------|------|--------|---------|---------|
| tiny | 40MB | ⚡⚡⚡ | ⭐ | 512MB | 1 分钟 |
| base | 140MB | ⚡⚡ | ⭐⭐ | 1GB | 5 分钟 |
| small | 244MB | ⚡ | ⭐⭐⭐ | 2GB | 10 分钟 |
| medium | 769MB | 🐢 | ⭐⭐⭐⭐ | 5GB | 30 分钟 |
| large | 2.9GB | 🐌 | ⭐⭐⭐⭐⭐ | 10GB | 1+ 小时 |

> 💡 首次下载时间取决于网速。之后会使用缓存，无需重复下载。


欢迎提交 Issue 和 PR：

- 🐛 报告转录错误和识别问题
- 📝 添加新的术语修正规则
- 🎯 改进转录准确度
- 📚 完善文档
- 📝 bug修复及功能优化

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## License 📄

MIT License - 详见 [LICENSE](./LICENSE)