"""
FFmpeg 工具模块 - 检测和管理系统中的 FFmpeg
"""

import platform
import subprocess
import sys
from pathlib import Path


class FFmpegChecker:
    """检查 FFmpeg 是否已安装"""

    @staticmethod
    def is_available() -> bool:
        """
        检查系统中是否安装了 FFmpeg

        Returns:
            True 如果 FFmpeg 可用，False 否则
        """
        try:
            subprocess.run(
                ['ffmpeg', '-version'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5
            )
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    def get_platform() -> str:
        """获取当前系统平台"""
        return platform.system()

    @staticmethod
    def get_install_instructions() -> str:
        """
        根据系统平台返回 FFmpeg 安装说明

        Returns:
            针对当前平台的安装说明
        """
        system = FFmpegChecker.get_platform()

        if system == "Windows":
            return FFmpegChecker._get_windows_instructions()
        elif system == "Darwin":
            return FFmpegChecker._get_macos_instructions()
        elif system == "Linux":
            return FFmpegChecker._get_linux_instructions()
        else:
            return FFmpegChecker._get_generic_instructions()

    @staticmethod
    def _get_windows_instructions() -> str:
        """Windows 系统的安装说明"""
        return """
╔════════════════════════════════════════════════════════════════╗
║           ❌ FFmpeg 未安装 - Windows 系统                       ║
╚════════════════════════════════════════════════════════════════╝

CodeWhisper 需要 FFmpeg 来处理音频文件。

📦 安装方法（选择其一）：

【方法 1】自动安装（推荐）⭐
────────────────────────────
运行自动安装脚本（需要 PowerShell）：

  python scripts/setup_environment.py

或直接运行 PowerShell 脚本：

  powershell -ExecutionPolicy Bypass -File scripts/install_ffmpeg_windows.ps1

【方法 2】使用 Chocolatey（如果已安装）
────────────────────────────
  choco install ffmpeg

【方法 3】使用 Windows Package Manager
────────────────────────────
  winget install ffmpeg

【方法 4】手动下载
────────────────────────────
1. 访问 https://ffmpeg.org/download.html
2. 下载 Windows 版本
3. 解压到某个目录，将该目录添加到 PATH 环境变量

🔗 更多详情：https://ffmpeg.org/download.html

✅ 安装完成后，重新运行 CodeWhisper 即可。
"""

    @staticmethod
    def _get_macos_instructions() -> str:
        """macOS 系统的安装说明"""
        return """
╔════════════════════════════════════════════════════════════════╗
║           ❌ FFmpeg 未安装 - macOS 系统                         ║
╚════════════════════════════════════════════════════════════════╝

CodeWhisper 需要 FFmpeg 来处理音频文件。

📦 安装方法（选择其一）：

【方法 1】自动安装（推荐）⭐
────────────────────────────
运行自动安装脚本：

  python scripts/setup_environment.py

或直接运行 Bash 脚本：

  bash scripts/install_ffmpeg_mac.sh

【方法 2】使用 Homebrew（推荐）
────────────────────────────
如果已安装 Homebrew：

  brew install ffmpeg

如果未安装 Homebrew，先运行：

  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

【方法 3】使用 MacPorts
────────────────────────────
  sudo port install ffmpeg

【方法 4】手动下载
────────────────────────────
访问 https://ffmpeg.org/download.html 下载 macOS 版本

✅ 安装完成后，重新运行 CodeWhisper 即可。
"""

    @staticmethod
    def _get_linux_instructions() -> str:
        """Linux 系统的安装说明"""
        return """
╔════════════════════════════════════════════════════════════════╗
║           ❌ FFmpeg 未安装 - Linux 系统                         ║
╚════════════════════════════════════════════════════════════════╝

CodeWhisper 需要 FFmpeg 来处理音频文件。

📦 安装方法（选择其一）：

【方法 1】自动安装（推荐）⭐
────────────────────────────
运行自动安装脚本：

  python scripts/setup_environment.py

或直接运行 Bash 脚本：

  bash scripts/install_ffmpeg_linux.sh

【方法 2】Debian/Ubuntu
────────────────────────────
  sudo apt update
  sudo apt install ffmpeg

【方法 3】RedHat/CentOS/Fedora
────────────────────────────
  sudo yum install ffmpeg

【方法 4】Arch Linux
────────────────────────────
  sudo pacman -S ffmpeg

【方法 5】Alpine Linux
────────────────────────────
  apk add ffmpeg

✅ 安装完成后，重新运行 CodeWhisper 即可。
"""

    @staticmethod
    def _get_generic_instructions() -> str:
        """通用安装说明"""
        return """
╔════════════════════════════════════════════════════════════════╗
║           ❌ FFmpeg 未安装                                      ║
╚════════════════════════════════════════════════════════════════╝

CodeWhisper 需要 FFmpeg 来处理音频文件。

📦 请访问 FFmpeg 官网安装：

  https://ffmpeg.org/download.html

或运行自动安装脚本：

  python scripts/setup_environment.py

✅ 安装完成后，重新运行 CodeWhisper 即可。
"""

    @staticmethod
    def check_and_exit_if_missing() -> None:
        """
        检查 FFmpeg，如果不存在则输出提示并退出
        """
        if not FFmpegChecker.is_available():
            instructions = FFmpegChecker.get_install_instructions()
            print(instructions)
            sys.exit(1)
