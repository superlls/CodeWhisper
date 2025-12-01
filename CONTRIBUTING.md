# Contributing to CodeWhisper 🤝

感谢你有兴趣贡献 CodeWhisper

## 我们最需要的贡献

### 1. 报告识别错误（最重要！）⭐⭐⭐⭐⭐

CodeWhisper 默认使用中文模式，但是中文模式在识别英文专有名词时会有误差。

**你的一条 Issue或PR，也许就能帮助所有中国开发者**

如果你发现：
- 说的是 "MySQL"，被识别成了 "My circle"
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

直接编辑 `dictionaries/programmer_terms.json` 文件，在相应分类中添加规则：

```json
{
  "category": "database",
  "rules": [
    {
      "wrong": "错误识别的文本",
      "correct": "正确术语",
      "description": "说明"
    }
  ]
}
```

**例子：**
```json
{
  "category": "database",
  "rules": [
    {
      "wrong": "my circle",
      "correct": "MySQL",
      "description": "常见误识别"
    }
  ]
}
```

**规则说明：**
- `wrong`: Whisper 实际识别出的错误内容（不需要写正则表达式，代码会自动处理）
- `correct`: 正确的术语
- `description`: 说明为什么会有这个错误
- `category`: 分类（database, framework, language, tools, concept, format, other），后续会补充其他


**提交 PR：**
```bash
git checkout -b fix-mysql-recognition
# 编辑 dictionaries/programmer_terms.json
git add dictionaries/programmer_terms.json
git commit -m "Fix: MySQL 被识别成 My circle，添加修正规则"
git push origin fix-mysql-recognition
```

### 3. 改进现有规则

某个规则效果不好？提交改进！

- 修改 `wrong` 的文本使其更准确
- 更新 `description` 说明
- 改进 `correct` 的格式

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

## 正则表达式小知识

> 💡 **重点**：你在 JSON 中只需要写 **plain text**，系统会自动判断是中文还是英文，然后选择合适的处理方式！

### 核心原理

系统根据你的规则中是否包含中文字符来自动处理：

- **包含中文** → 直接匹配
- **只有英文** → 自动添加单词边界，避免误匹配

### 为什么要区分？

**例子：英文不加边界会怎样？**

```
规则：修正 "api" → "API"

如果不加边界：
输入：  "I have an apiary（蜜蜂养殖场）"
输出：  "I have an APIary"  ← 错了！
        不应该改 apiary 里的 api

如果加边界（系统自动做）：
输入：  "I have an apiary"
输出：  "I have an apiary"  ← 正确！
只有单独的 api 才会被修正
```


### 系统自动处理示例

当你写这些规则时：

```json
{
  "category": "database",
  "rules": [
    {
      "wrong": "message core",
      "correct": "MySQL",
      "description": "英文 → 自动加边界"
    },
    {
      "wrong": "api",
      "correct": "API",
      "description": "英文 → 自动加边界"
    },
    {
      "wrong": "门特尔",
      "correct": "Mentor",
      "description": "中文 → 不加边界"
    }
  ]
}
```
### 匹配效果对比

```
修正 "api" → "API"

✅ "call the api"         → "call the API"
✅ "api documentation"     → "API documentation"
❌ "apiary"               → "apiary"（不改，正确）
❌ "APIs"                 → "APIs"（保持原样）



**你就记住：写你想修正的真实文本，系统自动搞定**

---

**感谢你的贡献！** 🎉
