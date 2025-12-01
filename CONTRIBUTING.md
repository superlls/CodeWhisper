# Contributing to CodeWhisper 🤝

感谢你有兴趣贡献 CodeWhisper

## 我们最需要的贡献

### 1. 报告识别错误（最重要！）⭐⭐⭐⭐⭐

CodeWhisper 默认使用中文模式，但是中文模式在识别英文专有名词时会有误差。

**你的一条 Issue或PR，也许就能帮助所有中文社区开发者**

如果你发现：
- 说的是 "MySQL"，被识别成了 "My circle"
- 说的是 "C sharp"，没被识别成C#，而被识别成了其他的
- 或任何其他识别错误

请：
1. **提交 Issue**：告诉我们你说的是什么，被识别成了什么
   ```
   标题：MySQL 被识别成 Message Core
   描述：当我说 "MySQL" 时，转录结果是 "Message Core"
   ```

2. **或者直接提 PR**：（见下面的步骤）

### 2. 添加修正规则

找到了识别错误，你可以直接提交 PR 来修正！

**如何做：**

编辑 `dictionaries/programmer_terms.json` 文件。新格式采用**分类 → 术语 → 变体**的三层结构，更清晰易维护：

```json
{
  "categories": {
    "database": {
      "name": "数据库",
      "terms": {
        "MySQL": {
          "correct": "MySQL",
          "description": "关系型数据库",
          "variants": [
            {"wrong": "mysql", "type": "lowercase", "reason": "小写形式"},
            {"wrong": "message core", "type": "chinese_phonetic", "reason": "中文音韵识别"},
            {"wrong": "my sql", "type": "split_english", "reason": "英文分隔"}
          ]
        }
      }
    }
  }
}
```

### 字典结构说明

```
dictionaries/programmer_terms.json
│
├─ version: "2.0"               # 字典版本
├─ categories                   # 分类层
│  ├─ database (数据库)
│  ├─ language (编程语言)
│  ├─ framework (框架和库)
│  ├─ tools (开发工具)
│  ├─ concept (技术概念)
│  └─ protocol_os (协议和操作系统)
│     │
│     └─ terms: {}              # 术语层
│        ├─ MySQL
│        ├─ PostgreSQL
│        └─ Redis
│           │
│           └─ variants: []     # 变体层
│              ├─ mysql (小写)
│              ├─ my sql (分隔)
│              ├─ message core (中文音韵)
│              └─ my circle (中文音韵变体)
```

### 添加新变体的步骤

**场景**：发现用户说 "Python" 被识别成 "派松"，想添加这个变体

1. 找到对应的术语位置：

```
"language": {
  "terms": {
    "Python": {
      "correct": "Python",
      "variants": [
        {"wrong": "python", "type": "lowercase"}
      ]
    }
  }
}
```

2. 在 `variants` 数组中添加新变体：

```
"variants": [
  {"wrong": "python", "type": "lowercase", "reason": "小写形式"},
  {"wrong": "派松", "type": "chinese_phonetic", "reason": "中文音韵识别"}
]
```

### 添加新术语的步骤

**场景**：想为 "database" 分类添加 "Elasticsearch"

1. 在相应分类的 `terms` 对象中添加：

```
"Elasticsearch": {
  "correct": "Elasticsearch",
  "description": "搜索和分析引擎",
  "variants": [
    {"wrong": "elasticsearch", "type": "lowercase", "reason": "小写形式"},
    {"wrong": "elastic search", "type": "split_english", "reason": "英文分隔"}
  ]
}
```

### 变体类型说明

| 类型 | 说明 | 例子 |
|------|------|------|
| `lowercase` | 小写形式 | python → Python |
| `split_english` | 英文分隔（空格） | java script → JavaScript |
| `split_english_short` | 部分分隔 | post gres → PostgreSQL |
| `chinese_phonetic` | 中文音韵识别 | 派松 → Python |
| `chinese_phonetic_variant` | 中文音韵变体 | 我的秋儿 → MySQL |
| `chinese_translation` | 中文翻译 | 烧瓶 → Flask |
| `chinese_similar` | 中文同音词 | 快递 → Express |
| `pronunciation` | 发音相似 | sequel → SQL |
| `full_name` | 全名形式 | golang → Go |
| `abbreviation` | 缩写形式 | k8s → Kubernetes |
| `spelled_out` | 拼写形式 | c plus plus → C++ |
| `similar_english` | 相似英文 | view → Vue |
| `mixed` | 混合形式 | java 脚本 → JavaScript |

### 提交 PR：

```bash
git checkout -b add-elasticsearch-support
# 编辑 dictionaries/programmer_terms.json
git add dictionaries/programmer_terms.json
git commit -m "Feat: 添加 Elasticsearch 术语及其变体"
git push origin add-elasticsearch-support
```

### 3. 改进现有规则

某个变体效果不好？提交改进！

- 修改 `wrong` 的文本使其更准确
- 更新 `reason` 说明为什么有这个识别
- 添加遗漏的变体形式

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
# 测试字典规则 将你的录音文件放到根目录下
python cli.py your_audio.m4a

# 查看统计
python cli.py --info
```

---

## 常见问题 Q&A

**Q: 怎样判断一个规则是否正确？**

A: 你可以用 CLI 测试：
```bash
# 把识别错误的文本转录到文件，然后转录
python cli.py your_audio.m4a

```

**Q: 为什么有些错误很难修正？**

A: 某些错误是 Whisper 的固有识别特性，比如：
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


---

**感谢你的贡献！** 🎉
