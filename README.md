# CodeWhisper 🎤

**Programmer-friendly speech-to-text tool** | 程序员专用语音转文字工具

基于 OpenAI Whisper，针对程序员优化的语音识别工具。自动识别和修正常见的编程术语，让你在开会或演讲时快速准确地转录代码和技术术语。

[English](#english) | [中文](#chinese)

---

## Features ✨

- 🎯 **程序员友好**：内置 68 条编程术语规则
  - 数据库：MySQL, PostgreSQL, MongoDB, Redis...
  - 框架：React, Vue, Django, Flask...
  - 语言：Python, JavaScript, TypeScript...
  - 工具：Docker, Kubernetes, Git, Nginx...
  - 概念：API, REST, GraphQL, CI/CD...

- 🚀 **快速转录**：支持多种模型大小
  - `tiny`：最快（40MB）
  - `base`：平衡（140MB）
  - `small`/`medium`/`large`：更准确

- 📝 **智能修正**：自动识别常见的语音识别错误
  - "my circle" → MySQL
  - "j son" → JSON
  - "graph ql" → GraphQL

- 🔧 **易于扩展**：支持自定义字典
- 🌍 **多语言**：支持 99 种语言

---

## Quick Start 🚀

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/codewhisper.git
cd codewhisper

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 使用

```bash
# 基础转录（中文，默认）
python cli.py audio.m4a

# 转录英文音频
python cli.py audio.m4a --language en

# 使用 tiny 模型（最快）
python cli.py audio.m4a --model tiny

# 显示详细分段信息
python cli.py audio.m4a --segments

# 查看字典统计
python cli.py --info

# 不修正术语（看原始转录）
python cli.py audio.m4a --no-fix
```

**💡 设计理念**：CodeWhisper 默认使用中文模式，因为我们的工具就是为中国程序员设计的。当你说中文时，就直接转录成中文。

---

## 项目结构

```
codewhisper/
├── __init__.py          # 模块入口
├── dict_manager.py      # 字典管理器（核心：68条规则）
├── transcriber.py       # Whisper 转录引擎
└── utils.py             # 工具函数

cli.py                   # 命令行工具
requirements.txt         # 依赖列表
README.md               # 本文件
dictionaries/           # 字典库
└── README.md           # 字典贡献指南
```

---

## 字典规则

目前内置 **68 条** 编程术语规则：

| 分类 | 数量 | 例子 |
|------|------|------|
| 数据库 | 7 | MySQL, PostgreSQL, MongoDB |
| 框架 | 10 | React, Vue, Django, Flask |
| 编程语言 | 12 | Python, JavaScript, TypeScript |
| 工具 | 13 | Docker, Kubernetes, Git |
| 概念 | 13 | API, REST, GraphQL, CI/CD |
| 数据格式 | 5 | JSON, XML, YAML |
| 其他 | 8 | HTTP, HTTPS, Linux |

---

## 贡献 🤝

我们欢迎社区贡献！特别是：

1. **添加更多术语** - 编程术语越多越好
2. **改进规则** - 使正则表达式更准确
3. **支持更多语言** - 中文、日文等

### 如何贡献

1. Fork 本仓库
2. 创建新分支 (`git checkout -b add-new-terms`)
3. 编辑 `codewhisper/dict_manager.py` 或创建自定义字典
4. 提交 PR

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 常见问题

**Q: 为什么有些专有名词识别不准确（如 MySQL → Message Core）？**
A: 这是 Whisper 中文模式的一个已知限制。当中文解码器遇到英文发音时，它会尝试用中文音韵来拟合，导致识别错误。这正是我们需要社区帮助的地方！

**Q: 发现识别错误了怎么办？**
A: 太好了！这正是我们改进的机会。请：
1. 提交一个 Issue，描述你说的是什么，被识别成了什么
2. 我们会在字典里添加这个修正规则
3. 或者直接提 PR，添加修正规则到 `codewhisper/dict_manager.py`

例如：
```
我说的：MySQL
被识别成：Message Core
修正规则：{"wrong": r"\bmessage\s+core\b", "correct": "MySQL", "category": "database"}
```

**Q: 为什么不用英文模式？**
A: 我们的理念是：工具是为中国程序员做的，你说中文就应该转成中文。不要为了迎合工具而改变说话方式。用中文模式 + 社区维护的修正字典，这样的组合最自然。

**Q: 支持离线使用吗？**
A: 支持！第一次下载模型后，后续可以完全离线使用。

**Q: 支持实时转录吗？**
A: 目前支持批量文件转录。实时转录计划在未来版本实现。

**Q: 可以用在 Android/iOS 上吗？**
A: 目前是 macOS/Linux/Windows CLI 工具。移动端适配计划中。

**Q: 准确度如何？**
A: 取决于音质和模型大小。base 模型在中文上准确度约 90%+，通过修正字典能进一步提高。

---

## License

MIT License - 详见 [LICENSE](LICENSE)

---

## 致谢

- [OpenAI Whisper](https://github.com/openai/whisper) - 核心转录模型
- 社区贡献者

---

<div id="chinese"></div>

## 中文说明

### 快速开始

```bash
# 转录音频文件
python cli.py 你的音频.m4a

# 查看统计信息
python cli.py --info
```

### 支持的模型

- `tiny`：最快，文件最小
- `base`：推荐，速度和准确度平衡
- `small`/`medium`/`large`：更准确，更慢

### 常见术语修正

```
输入（错误识别）      →  输出（修正）
"my circle"         →  MySQL
"j son"             →  JSON
"graph ql"          →  GraphQL
"docker"            →  Docker
"python"            →  Python
```

---

## 联系方式

- 提交 Issue 报告 bug
- 提交 PR 贡献代码
- 讨论区讨论想法

---

**Made with ❤️ for programmers**
