# CodeWhisper Scripts 说明

这个目录包含用于初始化 CodeWhisper 环境的自动化脚本。

## 📝 脚本列表

### 1. `setup_environment.py`（推荐使用）

**跨平台自动初始化脚本**，会自动检测系统平台并安装相应的 FFmpeg。

**使用方法：**
```bash
python scripts/setup_environment.py
```

**特点：**
- ✅ 自动检测操作系统（Windows/macOS/Linux）
- ✅ 自动调用相应平台的安装脚本
- ✅ 安装完成后自动验证

**支持的系统：**
- Windows 10/11
- macOS 10.15+
- Linux (Debian, Ubuntu, RedHat, CentOS, Fedora, Arch, Alpine 等)

---

### 2. `install_ffmpeg_windows.ps1`

**Windows 系统专用脚本**，使用 PowerShell 安装 FFmpeg。

**使用方法：**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_ffmpeg_windows.ps1
```

**特点：**
- ✅ 自动检查管理员权限，不足时自动请求
- ✅ 自动安装 Chocolatey（如果未安装）
- ✅ 使用 Chocolatey 安装 FFmpeg
- ✅ 自动验证安装结果

**注意：**
- 需要 PowerShell 5.0 以上
- 可能需要输入管理员密码

---

### 3. `install_ffmpeg_mac.sh`

**macOS 系统专用脚本**，使用 Homebrew 安装 FFmpeg。

**使用方法：**
```bash
bash scripts/install_ffmpeg_mac.sh
```

**特点：**
- ✅ 自动检查并安装 Homebrew（如果未安装）
- ✅ 使用 Homebrew 安装 FFmpeg
- ✅ 自动验证安装结果

**注意：**
- 需要 Bash 3.0 以上
- 可能需要输入密码

---

### 4. `install_ffmpeg_linux.sh`

**Linux 系统专用脚本**，自动检测发行版并使用相应的包管理器安装 FFmpeg。

**使用方法：**
```bash
bash scripts/install_ffmpeg_linux.sh
```

**支持的包管理器：**
- `apt` (Debian, Ubuntu)
- `yum/dnf` (RedHat, CentOS, Fedora)
- `pacman` (Arch Linux, Manjaro)
- `apk` (Alpine Linux)
- `zypper` (openSUSE, SLES)

**特点：**
- ✅ 自动检测 Linux 发行版
- ✅ 调用相应的包管理器安装 FFmpeg
- ✅ 自动验证安装结果

**注意：**
- 需要 Bash 3.0 以上
- 可能需要输入密码

---

## 🚀 快速开始

### 推荐方式（所有平台）

```bash
# 1. Clone 项目
git clone https://github.com/superlls/CodeWhisper.git
cd CodeWhisper

# 2. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows

# 3. 安装 Python 依赖
pip install -r requirements.txt

# 4. 自动安装 FFmpeg（推荐）
python scripts/setup_environment.py

# 5. 开始使用
python cli.py your_audio.m4a
```

---

## ⚠️ 故障排除

### 问题：脚本执行失败

**Windows PowerShell：**
```powershell
# 确保以管理员身份运行 PowerShell
# 然后执行：
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
powershell -ExecutionPolicy Bypass -File scripts/install_ffmpeg_windows.ps1
```

**macOS/Linux Bash：**
```bash
# 确保脚本有执行权限
chmod +x scripts/*.sh

# 然后执行
bash scripts/install_ffmpeg_mac.sh
```

### 问题：找不到 Chocolatey（Windows）

Windows 脚本会自动安装 Chocolatey。如果自动安装失败，可以手动安装：
https://chocolatey.org/install

### 问题：找不到 Homebrew（macOS）

macOS 脚本会自动安装 Homebrew。如果自动安装失败，可以手动安装：
https://brew.sh

---

## 📖 更多信息

完整的安装说明请参考：[README.md](../README.md)
