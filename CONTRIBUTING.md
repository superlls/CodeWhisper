# Contributing to CodeWhisper 🤝

感谢你有兴趣贡献 CodeWhisper！

## 我们最需要的贡献

### 1. 报告识别错误（最重要！）⭐⭐⭐⭐⭐

CodeWhisper 默认使用中文模式，但是中文模式在识别英文专有名词时会有误差。

**你的一条 Issue 或 PR，也许就能帮助所有中文社区开发者**

如果你发现：
- 说的是 "MySQL"，被识别成了 "My circle"
- 说的是 "Python"，被识别成了 "派森"
- 说的是 "Mentor"，被识别成了 "门特尔"
- 或任何其他识别错误

请：
1. **提交 Issue**：告诉我们你说的是什么，被识别成了什么
   ```
   标题：MySQL 被识别成 My circle
   描述：当我说 "MySQL" 时，转录结果是 "My circle" （或者你可以写写今天发生了啥2333）
   ```

2. **或者直接提 PR**：（见下面的步骤）

### 2. 添加修正规则

找到了识别错误，你可以直接提交 PR 来修正！

**字典结构**

编辑 `dictionaries/programmer_terms.json` 文件。字典采用**分类 → 术语 → 变体**的三层结构：

```
dictionaries/programmer_terms.json
│
├─ version: "2.0"
├─ categories               # 分类层
│  ├─ protocol_os
│  ├─ language
│  ├─ framework
│  ├─ tools
│  ├─ concept
│  └─ database
│     │
│     └─ terms {}          # 术语层
│        ├─ Redis
│        ├─ PostgreSQL
│        └─ MySQL
│           │
│           └─ variants []  # 变体层
│              ├─ mysql (小写)
│              ├─ my sql (分隔)
│              ├─ message core (中文音韵)
│              └─ my circle (中文音韵变体)
```

### 添加新变体的步骤

**场景**：发现 "Python" 被识别成 "派森"，想添加这个变体

1. 找到对应的术语，例如：

```json
"language": {
  "name": "编程语言",
  "terms": {
    "Python": {
      "correct": "Python",
      "description": "Python 编程语言",
      "variants": [
        {"wrong": "python", "description": "小写形式"}
      ]
    }
  }
}
```

2. 在 `variants` 数组中添加新变体：

```json
"variants": [
  {"wrong": "python", "description": "小写形式"},
  {"wrong": "派森", "description": "中文音韵识别"}
]
```

就这么简单！每个变体只需要两个字段：
- `wrong`: 识别错误的文本
- `description`: 简单描述这是什么类型的错误

### 添加新术语的步骤

**场景**：想为 "database" 分类添加 "Elasticsearch"

1. 在相应分类的 `terms` 对象中添加：

```json
"Elasticsearch": {
  "correct": "Elasticsearch",
  "description": "搜索和分析引擎",
  "variants": [
    {"wrong": "elasticsearch", "description": "小写形式"},
    {"wrong": "elastic search", "description": "英文分隔"}
  ]
}
```

关键点：
- `correct`: 正确的术语名称
- `description`: 术语的简短说明
- `variants`: 数组，包含所有可能被错误识别的形式

### 提交 PR

```bash
git checkout -b add-elasticsearch-support
# 编辑 dictionaries/programmer_terms.json
git add dictionaries/programmer_terms.json
git commit -m "Feat: 添加 Elasticsearch 术语及其变体"
git push origin add-elasticsearch-support
```

---

## 开发流程

### 设置开发环境

```bash
git clone https://github.com/superlls/CodeWhisper.git
cd CodeWhisper

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 测试你的改动

```bash
# 测试字典规则，将你的录音文件放到根目录下
python cli.py your_audio.m4a

# 查看统计信息
python cli.py --info
```

---

## 常见问题 Q&A

**Q: 怎样判断一个规则是否正确？**

A: 你可以用 CLI 测试：
```bash
python cli.py your_audio.m4a
```

**Q: 为什么有些错误很难修正？**

A: 某些错误是 Whisper 的固有识别特性：
- 中文模式会按音韵识别英文单词
- 不同口音可能导致不同的识别结果
- 某些词的发音确实相似

这时候可以添加多个变体规则来覆盖不同情况。

**Q: 我想添加一个全新的术语分类，可以吗？**

A: 可以！直接在 JSON 中添加新的 `category` 即可。但建议先检查是否可以归入现有分类。

---

## 代码风格

- Python 3.9+
- 遵循 PEP 8
- JSON 文件使用 2 个空格缩进

---

**感谢你的贡献！** 🎉
