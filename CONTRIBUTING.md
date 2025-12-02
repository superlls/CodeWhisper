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

#### 第一步：Fork 到你的仓库

首先，你需要把 CodeWhisper 仓库复制到自己的账户下（这就叫 **Fork**）。

**什么是 Fork？** 简单说就是把别人的仓库复制一份到自己的账户下。这样你就有了完整的修改权限，可以随意编辑而不会影响原仓库。

**怎样 Fork？** 非常简单：
1. 访问 [CodeWhisper GitHub 主页](https://github.com/superlls/CodeWhisper)
2. 点击右上角的 **"Fork"** 按钮（大约在 Star 按钮旁边）
3. 选择你要 Fork 到哪个账户（通常是你自己的用户名）
4. 等待 Fork 完成（通常几秒钟）

完成后，你会看到你的账户下多了一个 `your-username/CodeWhisper` 的仓库，这就是你的副本！

#### 第二步：Clone 到本地并创建分支

Fork 完成后，将你的副本克隆到本地：

```bash
# Clone 你 Fork 后的仓库（不是原仓库！）
git clone https://github.com/your-username/CodeWhisper.git
cd CodeWhisper

# 创建一个新分支（分支名应该能说明你的改动）
# 例如：你要修复排期识别错误
git checkout -b fix-paiqi-recognition
```

**为什么要创建分支？** 分支就像在原代码的基础上建立一个"平行世界"，你在这个"世界"里做的修改都是独立的，不会影响主分支。这样做的好处是：
- 可以同时做多个不同的改动
- 改动出错了可以轻松撤销
- 便于代码审核

#### 第三步：理解字典结构

编辑 `dictionaries/programmer_terms.json` 文件。字典采用**分类 → 术语 → 变体**的三层结构：

```
dictionaries/programmer_terms.json
│
├─ version: "0.1.0"
├─ categories
│  ├─ work_terms (职场术语)
│  │  └─ terms {}
│  │     ├─ 排期
│  │     │  ├─ correct: "排期"
│  │     │  ├─ description: "根据需求和开发工作量安排完成时间，在此期间需要按计划推进..."
│  │     │  └─ variants []
│  │     │     ├─ {"wrong": "排气", "description": "中文音韵误识别"}
│  │     │     └─ {"wrong": "拍期", "description": "发音近似"}
│  │     │
│  │     ├─ 逾期
│  │     ├─ 提测
│  │     ├─ Mentor
│  │     └─ ... (其他职场术语)
│  │
│  ├─ database (数据库)
│  ├─ language (编程语言)
│  ├─ framework (框架和库)
│  ├─ tools (开发工具)
│  ├─ concept (技术概念)
│  └─ protocol_os (协议和操作系统)
```

#### 第四步：添加新变体

**场景**：发现 "逾期" 又被识别成 "于期"，想添加这个变体

1. 利用全局搜索找到对应的术语（Mac：Command+F）：

```json
"work_terms": {
  "name": "职场术语",
  "terms": {
    "逾期": {
      "correct": "逾期",
      "description": "任务未在排期截止时间前完成的情况，通常需要说明原因并在后续排期中补充处理。",
      "variants": [
        {"wrong": "预期", "description": "中文音韵误识别，最常见"},
        {"wrong": "于期", "description": "同音字且模型常输出"}
      ]
    }
  }
}
```

2. 在 `variants` 数组中添加新变体：

```json
"variants": [
  {"wrong": "预期", "description": "中文音韵误识别，最常见"},
  {"wrong": "于期", "description": "同音字且模型常输出"},
  {"wrong": "语气（这里写新发现的错误）", "description": "你的描述"}
]
```

**每个变体只需要两个字段：**
- `wrong`: 识别错误的文本
- `description`: 简单描述这是什么类型的错误

#### 第五步（可选）：如果你发现字典里没有你想找的这个词，直接添加新术语吧

**场景**：想为 "work_terms" 分类添加一个新术语 "甩锅"（推卸责任）

1. 在相应分类的 `terms` 对象中添加：

```json
"甩锅": {
  "correct": "甩锅",
  "description": "把问题或责任推给别人",
  "variants": [
    {"wrong": "率过", "description": "中文音韵误识别"},
    {"wrong": "甩锅", "description": "正确形式"}
  ]
}
```

**关键点：**
- `correct`: 正确的术语名称
- `description`: 术语的简短说明（1-2句话）
- `variants`: 数组，包含所有可能被错误识别的形式

#### 第六步：提交 PR

编辑完成后，提交你的改动：

```bash
# 查看你修改了哪些文件
git status

# 添加修改的文件
git add dictionaries/programmer_terms.json

# 提交改动
git commit -m "feat: 添加逾期新变体'于期' 识别规则"

# 推送到你的 Fork 仓库
git push origin fix-paiqi-recognition
```

然后访问 GitHub，你会看到一个提示创建 Pull Request 的按钮，点击即可！

**重要**：创建 PR 时，确保你的分支是合并到 **原仓库的 `main` 分支**，而不是你 Fork 的仓库的 main 分支。GitHub 会在 PR 页面清楚地显示合并方向：

```
your-username/CodeWhisper (fix-paiqi-recognition) → superlls/CodeWhisper (main)
```

这样你的改动才能被合并到原项目中！

---

## 常见问题 Q&A

**Q: 怎样判断一个规则是否正确？**

A: 你可以用 CLI 测试，首先按照README文件去走CLI的步骤，并将你的录音文件拖入根目录下（和cli.py同级）：
```bash
python cli.py your_audio.m4a
```

**Q: 为什么有些错误很难修正？**

A: 某些错误是 Whisper 的固有识别特性：
- 中文模式会按音韵识别英文单词
- 不同口音可能导致不同的识别结果
- 某些词的发音确实相似

这时候可以添加多个变体规则来覆盖不同情况。

---

## 代码风格

- Python 3.9+
- 遵循 PEP 8
- JSON 文件使用 **2 个空格缩进**

### 字典编辑规范

#### 1. 格式统一性（非常重要！）

确保你的改动与现有格式保持一致：

**正确示例**（2 个空格缩进，格式对齐）：
```json
"逾期": {
  "correct": "逾期",
  "description": "任务未在排期截止时间前完成的情况",
  "variants": [
    {"wrong": "预期", "description": "中文音韵误识别"}
  ]
}
```

**错误示例**（混用缩进、格式不一致）：
```json
"逾期":{
    "correct":"逾期",
    "description":"任务未在排期截止时间前完成的情况",
    "variants":[
      {"wrong":"预期","description":"中文音韵误识别"}
    ]
}
```

#### 2. 添加新术语前必须检查

**千万不要重复添加！** 在添加新术语之前，请：

1. 在 `dictionaries/programmer_terms.json` 中**全局搜索**（Ctrl+F 或 Cmd+F）
2. 确认这个术语还没被添加过
3. 如果已经存在，就直接在 `variants` 中添加新变体即可

**例子**：
- ❌ 错误：发现没有 "Python"，就添加新术语。（其实已经存在了！）
- ✅ 正确：搜索 "Python" → 找到了 → 直接在 variants 数组末尾添加新变体

#### 3. 添加变体或新术语时，在末尾追加

**重要规则**：永远在对应的末尾追加，不要在中间插入！

**添加新变体的例子**：

原有的：
```json
"Python": {
  "correct": "Python",
  "description": "Python 编程语言",
  "variants": [
    {"wrong": "python", "description": "小写形式"},
    {"wrong": "派森", "description": "中文音韵识别"}
  ]
}
```

发现 "Python" 又被识别成 "蟒蛇" 了，应该在 `variants` 的**末尾追加**：
```json
"Python": {
  "correct": "Python",
  "description": "Python 编程语言",
  "variants": [
    {"wrong": "python", "description": "小写形式"},
    {"wrong": "派森", "description": "中文音韵识别"},
    {"wrong": "蟒蛇", "description": "中文义译识别"}  ← 在这里追加
  ]
}
```

**添加新术语的例子**：

原有的职场术语最后是 "验收"：
```json
"work_terms": {
  "name": "职场术语",
  "terms": {
    "排期": { ... },
    "逾期": { ... },
    ...
    "验收": { ... }
  }
}
```

现在要添加 "甩锅"，应该在 "验收" 之后追加：
```json
"work_terms": {
  "name": "职场术语",
  "terms": {
    "排期": { ... },
    "逾期": { ... },
    ...
    "验收": { ... },
    "甩锅": {           ← 在这里追加
      "correct": "甩锅",
      "description": "把问题或责任推给别人",
      "variants": [
        {"wrong": "率过", "description": "中文音韵误识别"}
      ]
    }
  }
}
```

**为什么要在末尾追加？**
- 避免 Git merge 冲突
- 保持历史记录清晰
- 方便代码审核

---

**感谢你的贡献！** 🎉
