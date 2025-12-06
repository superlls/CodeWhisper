# CodeWhisper 🎤

**为中文社区开发者打造的智能语音转文字工具** | AI-Powered Speech-to-Text for Developers

基于 OpenAI Whisper，配备**智能学习引擎**，不仅能自动纠正编程术语，还能**学习你的使用习惯，越用越懂你**！

🔥 **核心亮点**：
- 🧠 **智能学习**：自动追踪你常用的术语，动态优化识别准确度
- 🎯 **个性化识别**：分析你的技术栈，甚至能判断你是前端还是后端开发者
- 🚀 **越用越准**：使用次数越多，识别越精准（本地学习，隐私安全）
- 🔧 **极致解耦**：配置文件驱动，轻松迁移到医疗、法律等其他行业

目前Mac已上线一个MVP，CLI版本持续优化中，Windows版本开发已提上日程！

**支持的音频格式**：MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM

**参与共建**：如果你的领域有特定术语希望优化，欢迎提交 PR 到字典库！

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

### 🧠 智能学习引擎（核心亮点）

**双重优化机制**：兜底纠错 + 自适应学习

#### 1️⃣ 术语字典兜底纠错（188+ 条规则）

当 Whisper 识别错误时，字典自动修正：
```
❌ "门特尔"  → ✅ "Mentor"
❌ "my circle" → ✅ "MySQL"
❌ "排气"     → ✅ "排期"
```

#### 2️⃣ **智能学习系统**（🔥 独家特性）

**工作原理**：

```mermaid
graph LR
    A[你说话] --> B[Whisper转录]
    B --> C[术语修正]
    C --> D[检测高频词]
    D --> E[更新个人词库]
    E --> F[优化下次识别]
    F --> B
```

**实际效果**：

| 使用前 | 使用后（3天） | 效果 |
|--------|--------------|------|
| 通用提示词 | **个性化提示词** | ⚡ 识别准确度提升 |
| 识别"Redis"需纠正 | 直接识别"Redis" | 🎯 零纠正 |
| 不知道你的技术栈 | **分析你是后端开发** | 🧠 智能画像 |

**示例**：
```bash
# 初始状态
提示词：计算机行业从业者：提测、联调、排期、上线、复盘、接口、并发、缓存、数据库、日志。

# 使用1周后（你经常说 Dubbo、Redis、Kafka）
提示词：计算机行业从业者：提测、联调、排期、Dubbo、Redis、Kafka、Spring、MySQL、并发、缓存。
       ↑ 系统自动学习到你的高频术语！
```

**技术细节**：
- 📊 **频次统计**：记录每个术语的使用次数和时间
- 🎯 **智能排序**：高频术语优先进入提示词
- 🗑️ **自动淘汰**：低频术语自动移除，保持词库精简
- 💾 **本地存储**：所有数据本地保存，隐私安全

---

### 📚 社区维护的术语字典

**覆盖 11 大分类，188+ 条术语规则**：

| 分类 | 包含术语 | 数量 |
|------|---------|------|
| 职场术语 | 提PR、提测、排期、逾期、联调、灰度、验收... | 26 |
| 大学生术语 | 秋招、春招、校招、社招、offer、CV、笔试、面试... | 20 |
| 编程语言 | Python、Java、Go、JavaScript、TypeScript、Rust、C++... | 22 |
| 开发工具 | IDEA、VSCode、WebStorm、PyCharm、Goland、Vim、Emacs... | 18 |
| 技术概念 | API、REST、GraphQL、SQL、ORM、CRUD、MVC、CI/CD... | 15 |
| 前端开发 | React、Vue、Angular、Webpack、Vite... | - |
| 后端开发 | Spring、SpringBoot、Kafka、Zookeeper、Dubbo、Arthas... | 22 |
| 数据库 | MySQL、PostgreSQL、MongoDB、Redis、DB、DBA... | 13 |
| DevOps工具 | Docker、Kubernetes、Git、GitHub、GitLab、Jenkins... | 19 |
| 运维监控 | Nginx、Apache、Prometheus、Grafana... | 4 |
| 硬件与嵌入式 | macOS、Windows、Linux、STM32、Arduino、树莓派、ARM... | 21 |
| 通信协议 | HTTP、HTTPS、SSL、TLS、DNS、FTP、SMTP、ARP... | 8 |

**字典双重作用**：
1. ✅ **兜底纠错**：Whisper 识别错误时立即修正
2. ✅ **学习素材**：检测你常用的术语，构建个人词库

---

### 🔧 极致解耦架构（行业迁移神器）

**完全配置文件驱动，代码与业务零耦合**：

```
config/
├── base_config.json    # 行业配置（前缀、参数）
├── base_dict.json      # 通用术语库
└── user_dict.json      # 个人学习词库（自动生成）
```

**迁移到其他行业仅需 3 步**：

```bash
# 从"计算机行业"切换到"医疗行业"

# 1. 修改行业前缀
sed -i '' 's/计算机行业/医疗行业/g' config/base_config.json

# 2. 替换术语库
cat > config/base_dict.json <<EOF
{
  "terms": ["病历", "诊断", "处方", "会诊", "CT", "核磁共振", ...]
}
EOF

# 3. 完成！无需改代码
python cli.py --info  # 立即生效
```

**支持的迁移场景**：
- 💼 **企业行业**：金融、制造、零售、物流...
- 🏥 **专业领域**：医疗、法律、教育、建筑...
- 🎮 **兴趣领域**：游戏、电竞、影视、音乐...

---

### 🚀 快速转录

支持多种 Whisper 模型：
- `tiny`：最快，轻量级
- `base`：较快，日常使用
- `small`：平衡性能
- `medium`：推荐，高准确度（1.4GB）
- `large`：最准，专业场景

**性能建议**：电脑性能好 → `medium` 或 `large`

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

## 🧠 智能学习系统使用指南

### 查看学习状态

```bash
python cli.py --info
```

**输出示例**：
```
智能提示词引擎：
  通用术语数   : 15 条
  用户术语数   : 8 条      # ← 你的个人词库术语数
  有效术语数   : 3 条      # ← 高频术语（freq ≥ 3）

当前提示词：
  计算机行业从业者：提测、联调、排期、上线、复盘、Redis、Dubbo、Kafka、并发、缓存。
                                                    ↑ 这些是系统学到的你的高频术语
```

### 理解学习过程

**第 1 次使用**：
```bash
你说："今天我在做 Dubbo 服务的开发"
系统：检测到术语 "Dubbo"，频次 = 1 → 记录到个人词库
```

**第 2 次使用**：
```bash
你说："Dubbo 的配置有问题"
系统：检测到术语 "Dubbo"，频次 = 2 → 更新频次
```

**第 3 次使用**：
```bash
你说："调试 Dubbo 服务"
系统：检测到术语 "Dubbo"，频次 = 3 → ✅ 达到阈值！进入提示词
下次转录：Whisper 会优先识别 "Dubbo"，识别准确度大幅提升！
```

### 查看个人词库

```bash
cat config/user_dict.json
```

**示例输出**：
```json
{
  "terms": [
    {
      "term": "Dubbo",
      "freq": 12,
      "last_used": "2025-12-06T18:30:00"
    },
    {
      "term": "Redis",
      "freq": 8,
      "last_used": "2025-12-06T18:32:15"
    }
  ]
}
```
- `freq`: 使用频次
- `last_used`: 最后使用时间

### 技术栈分析示例

**场景 1：后端开发者**
```bash
经常提到：Dubbo、Redis、MySQL、Kafka、Spring
系统判断：你可能是 Java 后端开发者
优化效果：提示词自动包含这些术语，识别准确度 ↑↑↑
```

**场景 2：前端开发者**
```bash
经常提到：React、Vue、Webpack、TypeScript、Vite
系统判断：你可能是前端开发者
优化效果：提示词自动包含前端术语，识别准确度 ↑↑↑
```

**场景 3：全栈开发者**
```bash
经常提到：Docker、Git、MongoDB、Nginx、API
系统判断：你可能是全栈/运维方向
优化效果：提示词平衡前后端和工具术语
```

### 重置学习数据

如果想重新开始学习：
```bash
echo '{"terms": []}' > config/user_dict.json
```

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

3. **利用智能学习**：
   - **多用几次**！系统会自动学习你的常用术语
   - 查看 `python cli.py --info` 了解学习状态
   - 3次使用后，高频术语自动进入提示词，识别准确度显著提升

4. **补充字典规则**：
   - 如果字典没有你的术语，可以通过提PR或者Issue 反馈
   - 欢迎贡献新的修正规则！

**Q: 智能学习系统如何工作？**

A:
- **自动检测**：每次转录后，系统检测你使用的术语
- **频次统计**：记录每个术语的使用次数和时间
- **动态优化**：高频术语（≥3次）自动进入提示词
- **持续进化**：使用越多，识别越准确
- **隐私安全**：所有数据本地存储，不上传云端

**Q: 为什么说能"分析我是什么方向的开发者"？**

A:
系统通过你的高频术语进行技术栈分析：
- 经常说 `Dubbo、Redis、Kafka` → 判断为后端开发者
- 经常说 `React、Vue、Webpack` → 判断为前端开发者
- 经常说 `Docker、Kubernetes、Jenkins` → 判断为 DevOps 工程师

然后自动优化提示词，让 Whisper 优先识别你领域的术语！

**Q: 多久能看到学习效果？**

A:
- **立即生效**：每次转录后立即更新
- **3次达标**：同一术语出现3次后进入提示词
- **1周显著**：使用1周后，个性化效果明显
- **越用越准**：长期使用，识别准确度持续提升

**Q: 如何迁移到其他行业（医疗、法律等）？**

A:
仅需修改配置文件，无需改代码！详见 [极致解耦架构](#-极致解耦架构行业迁移神器) 部分。

示例：
```bash
# 1. 修改行业前缀
vim config/base_config.json  # 改为 "医疗行业从业者："

# 2. 替换术语库
vim config/base_dict.json    # 替换为医疗术语

# 3. 完成！
python cli.py --info         # 立即生效
```

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
- 💡 功能建议和优化
- 🧠 智能学习系统反馈
- 🔧 行业迁移案例分享

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

**联系方式**：
- 📮 Email: 1656839861un@gmail.com
- 💬 提交 Issue: [GitHub Issues](https://github.com/superlls/CodeWhisper/issues)

---

## 🎉 最新更新

### v0.2.0 - 智能学习引擎（2025-12-06）

🔥 **重大更新**：全新智能提示词引擎上线！

**新增功能**：
- ✅ **智能学习系统**：自动追踪用户常用术语
- ✅ **个性化提示词**：动态优化 Whisper 识别准确度
- ✅ **技术栈分析**：判断用户开发方向（前端/后端/DevOps）
- ✅ **频次统计**：记录术语使用次数和时间
- ✅ **自动淘汰**：智能维护用户词库容量
- ✅ **配置驱动**：完全解耦，支持行业迁移

**效果提升**：
- 📈 识别准确度提升：使用1周后显著改善
- 🎯 零纠正率：高频术语直接识别，无需后期修正
- 🚀 越用越准：持续学习，长期优化

**文档**：
- 📖 [智能学习系统详细文档](docs/PROMPT_ENGINE.md)
- 📝 [升级说明](docs/PROMPT_ENGINE_UPGRADE.md)

---

## 📚 相关文档

- [智能提示词引擎使用指南](docs/PROMPT_ENGINE.md)
- [贡献指南](CONTRIBUTING.md)
- [更新日志](docs/PROMPT_ENGINE_UPGRADE.md)

---

## 💡 设计理念

CodeWhisper 的核心设计理念：

1. **🧠 智能学习优先**
   - 系统应该越用越懂用户
   - 自动化优于手动配置
   - 本地学习，隐私安全

2. **🎯 准确性至上**
   - 双重纠错机制（字典 + 提示词）
   - 专业术语零容忍错误
   - 持续优化识别质量

3. **🔧 架构灵活性**
   - 配置文件驱动
   - 代码与业务解耦
   - 支持行业迁移

4. **🚀 用户体验**
   - 开箱即用
   - 渐进式增强
   - 无感知学习

---

## License 📄

MIT License - 详见 [LICENSE](./LICENSE)