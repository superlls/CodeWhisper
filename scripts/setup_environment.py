#!/usr/bin/env python3
"""
CodeWhisper 环境初始化脚本 - 自动检测平台并安装 FFmpeg

使用方法:
  python scripts/setup_environment.py
"""

import platform
import subprocess
import sys
import os
from pathlib import Path


class EnvironmentSetup:
    """环境设置类"""

    def __init__(self):
        self.system = platform.system()
        self.script_dir = Path(__file__).parent.absolute()

    def print_header(self):
        """打印标题"""
        print("\n" + "=" * 70)
        print("  CodeWhisper 环境初始化脚本")
        print("=" * 70)
        print(f"\n🖥️  系统平台: {self.system}\n")

    def check_ffmpeg(self) -> bool:
        """检查 FFmpeg 是否已安装"""
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

    def run_setup(self):
        """运行相应的安装脚本"""
        # 检查 FFmpeg
        if self.check_ffmpeg():
            print("✅ FFmpeg 已安装，无需重复安装\n")
            return True

        print("🔍 FFmpeg 未检测到，开始安装...\n")

        if self.system == "Windows":
            return self._setup_windows()
        elif self.system == "Darwin":
            return self._setup_macos()
        elif self.system == "Linux":
            return self._setup_linux()
        else:
            print(f"❌ 不支持的系统: {self.system}")
            return False

    def _setup_windows(self) -> bool:
        """Windows 安装"""
        ps_script = self.script_dir / "install_ffmpeg_windows.ps1"

        if not ps_script.exists():
            print(f"❌ PowerShell 脚本不存在: {ps_script}")
            return False

        print(f"📥 运行 Windows PowerShell 安装脚本...")
        print(f"   脚本位置: {ps_script}\n")

        try:
            subprocess.run([
                'powershell',
                '-ExecutionPolicy', 'Bypass',
                '-File', str(ps_script)
            ], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n❌ 安装失败: {e}")
            return False
        except FileNotFoundError:
            print("❌ PowerShell 未找到，请确保 Windows 系统已安装 PowerShell")
            return False

    def _setup_macos(self) -> bool:
        """macOS 安装"""
        sh_script = self.script_dir / "install_ffmpeg_mac.sh"

        if not sh_script.exists():
            print(f"❌ Bash 脚本不存在: {sh_script}")
            return False

        print(f"📥 运行 macOS Bash 安装脚本...")
        print(f"   脚本位置: {sh_script}\n")

        # 使脚本可执行
        os.chmod(sh_script, 0o755)

        try:
            subprocess.run(['bash', str(sh_script)], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n❌ 安装失败: {e}")
            return False

    def _setup_linux(self) -> bool:
        """Linux 安装"""
        sh_script = self.script_dir / "install_ffmpeg_linux.sh"

        if not sh_script.exists():
            print(f"❌ Bash 脚本不存在: {sh_script}")
            return False

        print(f"📥 运行 Linux Bash 安装脚本...")
        print(f"   脚本位置: {sh_script}\n")

        # 使脚本可执行
        os.chmod(sh_script, 0o755)

        try:
            subprocess.run(['bash', str(sh_script)], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n❌ 安装失败: {e}")
            return False

    def print_success(self):
        """打印成功信息"""
        print("\n" + "=" * 70)
        print("✅ 环境初始化成功！")
        print("=" * 70)
        print("\n现在你可以运行 CodeWhisper:")
        print("  python cli.py your_audio.m4a\n")

    def print_failure(self):
        """打印失败信息"""
        print("\n" + "=" * 70)
        print("❌ 环境初始化失败！")
        print("=" * 70)
        print("\n请手动安装 FFmpeg:")

        if self.system == "Windows":
            print("  • 访问: https://ffmpeg.org/download.html")
            print("  • 或运行: choco install ffmpeg")
            print("  • 或运行: winget install ffmpeg")
        elif self.system == "Darwin":
            print("  • 运行: brew install ffmpeg")
        elif self.system == "Linux":
            print("  • Debian/Ubuntu: sudo apt install ffmpeg")
            print("  • RedHat/CentOS: sudo yum install ffmpeg")
            print("  • Arch: sudo pacman -S ffmpeg")

        print()


def main():
    """主函数"""
    setup = EnvironmentSetup()
    setup.print_header()

    success = setup.run_setup()

    if success and setup.check_ffmpeg():
        setup.print_success()
        return 0
    else:
        setup.print_failure()
        return 1


if __name__ == "__main__":
    sys.exit(main())
