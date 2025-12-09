# Contributing to CodeWhisper 🤝

感谢你有兴趣贡献 CodeWhisper

## 为什么你的贡献很重要？

CodeWhisper 本质上就是用**社区驱动的术语字典**来纠正 Whisper 模型的识别错误。每一条你提交的术语修正规则，都会直接帮助所有中文社区开发者获得更准确的转录结果。

无论你是刚接触编程的新朋友，还是已经有一些经验，我们都非常欢迎你的加入与贡献！

**兴许你的一条 Issue 或 PR，就能帮助成千上万的开发者** ⭐

## 我们最需要的贡献

### 报告识别错误⭐⭐⭐⭐⭐

CodeWhisper 使用 OpenAI Whisper 模型进行语音识别，虽然很强大，但在识别中文术语时仍然会有误差，特别是：

- **英文专有名词**被按中文音韵识别（如 "MySQL" → "My circle"）
- **中文术语**被识别成相似读音的其他词（如 "排期" → "排气"）
- **混合术语**识别不稳定（如 "提PR" → "TPR"）


如果你发现：
- 说的是 "MySQL"，被识别成了 "My circle"
- 说的是 "Python"，被识别成了 "派森"
- 说的是 "Mentor"，被识别成了 "门特尔"
- 或者字典里压根就没有你的术语！

**你可以选择以下方式参与：**

#### 方式 1：提交 Issue
```
标题：MySQL 被识别成 My circle

描述：
- 说的词：MySQL
- 识别结果：My circle
- 简单描述术语的定义：常用数据库之一
```

#### 方式 2：直接提 PR 添加修正规则


#### 第一步：Fork 到你的仓库

1. 访问 [CodeWhisper GitHub 主页](https://github.com/superlls/CodeWhisper)
2. 点击右上角的 **"Fork"** 按钮
3. 等待完成

完成后，你的账户下会有 `your-username/CodeWhisper`

#### 第二步：编辑 JSON 文件

##### 方案 A：在 GitHub 网页上直接编辑（快速方案）

1. Fork 完成后，进入你的 `your-username/CodeWhisper` 仓库
2. 找到 `dictionaries/programmer_terms.json` 文件，点击编辑按钮（铅笔图标）
3. 找到对应的术语分类，编辑或添加内容
4. 完成后，点击 **"Commit changes"**

##### 方案 B：在本地 PyCharm 中编辑

1. Clone 你的 Fork 仓库到本地：
   - 打开 PyCharm → **File（文件）** → **New（新建）** → **Project from Version Control（来自版本控制的项目）**
   - 输入你的仓库地址：`https://github.com/your-username/CodeWhisper.git`
   - 点击 **Clone**

2. **提交前先同步原仓库**：
   - 打开 PyCharm 终端或 Git 菜单
   - 在 PyCharm Git 菜单中选择 **Update Project(更新项目)** 拉取最新的 `superlls/main`

3. 编辑 `dictionaries/programmer_terms.json`：
   - 找到对应的术语分类
   - 编辑或添加新术语/变体
   - 保存文件

#### 第三步：提交改动到 GitHub

##### 如果你用的是方案 A（网页编辑）：

直接跳到第四步创建 PR，GitHub 会自动检测到你的改动。

##### 如果你用的是方案 B（PyCharm 本地编辑）：

1. 在 PyCharm 中，打开菜单 **Git** → **Commit（提交）**
2. 确认修改的文件（应该只有 `dictionaries/programmer_terms.json`）
3. 在 **Commit Message** 输入框中输入提交信息，例如：
   - `feat: 添加"排期"变体 "排气"`
   - `feat: 新增术语"甩锅"`
4. 点击 **Commit（提交）** 按钮
5. 打开菜单 **Git** → **Push（推送）** 推送到你的 Fork 仓库

#### 第四步：提交 Pull Request

1. 推送完成后（或网页提交后），访问你的 GitHub 页面：`https://github.com/your-username/CodeWhisper`
2. 你会看到 **"Compare & pull request"** 按钮，点击它
3. 确认合并方向：`your-username/CodeWhisper (你的分支)` → `superlls/CodeWhisper (main)`
4. 填写 PR 描述，说明你改了什么，例如：
   - `新增变体：排期 的 排气`
   - `新增术语：甩锅`
5. 点击 **"Create pull request"**

完成！等待维护者审核合并。

---

### 理解字典结构

需要了解字典采用**分类 → 术语 → 变体**的三层结构：

**字段说明：**
- `correct`: 正确的术语名称
- `description`: 术语的简短说明
- `variants`: 数组，包含所有可能被错误识别的形式
  - `wrong`: 识别错误的文本
  - `description`: 错误的类型（如"中文音韵误识别"）

**示例 - 添加新变体**：

原有的逾期术语：
```json
"逾期": {
  "correct": "逾期",
  "description": "任务未在排期截止时间前完成的情况",
  "variants": [
    {
      "wrong": "预期",
      "description": "中文音韵误识别"
    }
  ]
}
```

发现又被识别成 "于期"，在 `variants` **末尾追加**：
```json
"variants": [
  {
    "wrong": "预期",
    "description": "中文音韵误识别"
  },
  {
    "wrong": "于期",
    "description": "同音字且模型常输出"
  }
]
```

**示例 - 添加新术语**：

为职场术语添加 "甩锅"：
```json
"甩锅": {
  "correct": "甩锅",
  "description": "把问题或责任推给别人",
  "variants": [
    {
      "wrong": "率过",
      "description": "中文音韵误识别"
    }
  ]
}
```

### 分类参考

| 分类 | 适用场景        | 例子 |
|------|-------------|------|
| **职场术语** | 工作相关的中文或中英混合术语 | 排期、逾期、提PR、联调、灰度、验收、工单 |
| **大学生术语** | 招聘、实习、面试相关  | 秋招、春招、校招、offer、CV、笔试、刷题 |
| **编程语言** | 编程语言名称      | Python、Java、Go、JavaScript、TypeScript |
| **开发工具** | IDE、编辑器、开发工具 | IDEA、VSCode、PyCharm、WebStorm、Vim |
| **技术概念** | 通用的技术原理和设计模式 | API、REST、GraphQL、SQL、ORM、CRUD、MVC |
| **前端开发** | 前端框架、库和工具   | React、Vue、Angular、Webpack、Vite |
| **后端开发** | 后端框架、库、消息队列等 | Spring、Kafka、Zookeeper、CAT、Arthas |
| **数据库** | 数据库系统和管理员   | MySQL、PostgreSQL、MongoDB、Redis、DBA |
| **DevOps工具** | CI/CD、容器、包管理工具 | Docker、Kubernetes、Git、GitHub、Maven、npm |
| **运维** | Web服务器、日志、监控 | Nginx、Apache |
| **硬件与嵌入式** | 操作系统、微控制器、开发板 | macOS、Windows、Linux、STM32、Arduino |
| **通信协议** | 网络通信相关协议    | HTTP、HTTPS、SSL、会话 |
| **其他术语** | 不属于以上分类的术语  | （待社区扩展） |

---

## 编辑建议

- **添加前先搜索**：在添加新术语前，用 Ctrl+F（或 Cmd+F）搜索确保还没被添加过
- **在末尾追加**：添加新变体或新术语时，始终在末尾追加，避免产生冲突
- **保持格式一致**：使用 2 个空格缩进，参考现有术语的格式复制即可

---

## 其他贡献方式

除了字典贡献，我们还欢迎以下形式的贡献：

### 📝 文档和使用指南
- 完善 README 和文档
- 添加更详细的使用教程

### 🐛 Bug 报告和功能建议
- 报告使用中遇到的问题
- 提出改进建议
- 分享使用体验


---

## 联系我们

- 📧 **Email**: 1656839861un@gmail.com
- 🐙 **GitHub Issues**: [提交问题或建议](https://github.com/superlls/CodeWhisper/issues)
- 💬 **讨论**: [参与讨论](https://github.com/superlls/CodeWhisper/discussions)

---

**感谢你的贡献！一起让 CodeWhisper 变得更好！** 🎉

每一条修正规则、每一个 Bug 报告、每一个改进建议，也许都在帮助成千上万的开发者获得更好的开发体验～
