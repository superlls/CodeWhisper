# Contributing to CodeWhisper 🤝

感谢你有兴趣贡献 CodeWhisper！

## 我们最需要的贡献

### 1. 报告识别错误（最重要！）⭐⭐⭐

CodeWhisper 默认使用中文模式，因为我们的工具就是为中国程序员做的。但是中文模式在识别英文专有名词时会有误差。**这是我们进步的动力！**

**你的一条 Issue，就能帮助所有中国开发者！**

如果你发现：
- 说的是 "MySQL"，被识别成了 "Message Core"
- 说的是 "PostgreSQL"，被识别成了其他的
- 或任何其他识别错误

请：
1. **提交 Issue**：告诉我们你说的是什么，被识别成了什么
   ```
   标题：MySQL 被识别成 Message Core
   描述：当我说 "MySQL" 时，转录结果是 "Message Core"
   ```

2. **或者直接提 PR**：自己修正！（见下面的步骤）

### 2. 添加修正规则

找到了识别错误，你可以直接提交 PR 来修正！

**如何做：**

1. 编辑 `codewhisper/dict_manager.py`
2. 在 `_get_builtin_dict()` 方法的相应分类中添加规则：

```python
{"wrong": r"\b错误识别\b", "correct": "正确术语", "category": "分类"},
```

**例子：**
```python
# 中文模式识别错误的例子
{"wrong": r"\bmessage\s+core\b", "correct": "MySQL", "category": "database"},
{"wrong": r"\bmy\s+s\s+q\s+l\b", "correct": "MySQL", "category": "database"},  # 分开读音
```

**规则说明：**
- `wrong`: 正则表达式模式（Whisper 实际识别出的错误内容）
- `correct`: 正确的术语
- `category`: 分类（database, framework, language, tools, concept, format, other）

**提交 PR：**
```bash
git checkout -b fix-mysql-recognition
# 编辑 codewhisper/dict_manager.py
git add codewhisper/dict_manager.py
git commit -m "Fix: MySQL 被识别成 Message Core，添加修正规则"
git push origin fix-mysql-recognition
```

### 3. 改进现有规则

某个规则不够准确？提交改进！

- 修改正则表达式使其更精准
- 修改分类
- 添加注释说明原因

---

## 开发流程

### 设置开发环境

```bash
git clone https://github.com/yourusername/codewhisper.git
cd codewhisper

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 测试你的改动

```bash
# 测试字典规则
python cli.py your_audio.m4a

# 查看统计
python cli.py --info
```

### 提交 PR 前的检查清单

- [ ] 代码格式整洁
- [ ] 测试过你的改动
- [ ] 更新了相关文档（如有必要）
- [ ] Commit message 清晰

---

## 术语分类指南

添加新规则时，请选择正确的分类：

| 分类 | 例子 |
|------|------|
| **database** | MySQL, PostgreSQL, MongoDB, Redis |
| **framework** | React, Vue, Django, Flask, Express |
| **language** | Python, JavaScript, TypeScript, Go |
| **tools** | Docker, Git, Kubernetes, Nginx |
| **concept** | API, REST, GraphQL, CI/CD |
| **format** | JSON, XML, YAML, CSV |
| **other** | HTTP, HTTPS, Linux, Ubuntu |

---

## 正则表达式小提示

- `\b` 是单词边界（避免匹配子串）
- `\s*` 匹配空格（处理分词错误）
- `\s+` 匹配一个或多个空格

**例子：**
```python
# ❌ 不好：会误匹配
{"wrong": r"mysql", "correct": "MySQL"}

# ✅ 好：只匹配完整单词
{"wrong": r"\bmysql\b", "correct": "MySQL"}

# ✅ 很好：处理分词错误
{"wrong": r"\bmy\s+sql\b", "correct": "MySQL"}

# ✅ 最好：处理中文模式的音韵拟合
{"wrong": r"\bmessage\s+core\b", "correct": "MySQL"}
```

---

## 代码风格

- Python 3.8+
- 遵循 PEP 8
- 添加清晰的注释（特别是复杂的正则表达式）

---

## 问题或疑问？

- 提交 Issue 讨论
- 在 Pull Request 中描述你的想法

---

**感谢你的贡献！** 🎉

让我们一起打造最好的中国程序员语音识别工具！
