#!/bin/bash

# CodeWhisper FFmpeg 自动安装脚本 (Linux)
# 使用方法: bash scripts/install_ffmpeg_linux.sh

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        CodeWhisper FFmpeg 自动安装脚本 (Linux)                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# 检查是否已安装 FFmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg 已安装！"
    echo ""
    ffmpeg -version | head -1
    exit 0
fi

echo "🔍 FFmpeg 未找到，开始安装..."
echo ""

# 检测 Linux 发行版
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "❌ 无法检测 Linux 发行版"
    exit 1
fi

echo "📦 检测到 Linux 发行版: $OS"
echo ""

# 根据发行版安装
case "$OS" in
    ubuntu|debian)
        echo "📥 使用 apt 包管理器安装 FFmpeg..."
        echo ""
        sudo apt update
        sudo apt install -y ffmpeg
        ;;
    fedora|rhel|centos)
        echo "📥 使用 yum/dnf 包管理器安装 FFmpeg..."
        echo ""
        if command -v dnf &> /dev/null; then
            sudo dnf install -y ffmpeg
        else
            sudo yum install -y ffmpeg
        fi
        ;;
    arch|manjaro)
        echo "📥 使用 pacman 包管理器安装 FFmpeg..."
        echo ""
        sudo pacman -S --noconfirm ffmpeg
        ;;
    alpine)
        echo "📥 使用 apk 包管理器安装 FFmpeg..."
        echo ""
        sudo apk add ffmpeg
        ;;
    opensuse*|sles)
        echo "📥 使用 zypper 包管理器安装 FFmpeg..."
        echo ""
        sudo zypper install -y ffmpeg
        ;;
    *)
        echo "❌ 不支持的 Linux 发行版: $OS"
        echo ""
        echo "请手动安装 FFmpeg，运行命令（根据你的发行版选择）："
        echo ""
        echo "Debian/Ubuntu:"
        echo "  sudo apt update && sudo apt install -y ffmpeg"
        echo ""
        echo "RedHat/CentOS/Fedora:"
        echo "  sudo yum install -y ffmpeg"
        echo ""
        echo "Arch Linux:"
        echo "  sudo pacman -S ffmpeg"
        echo ""
        echo "Alpine Linux:"
        echo "  apk add ffmpeg"
        echo ""
        exit 1
        ;;
esac

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ FFmpeg 安装成功！"
    echo ""
    echo "✓ 验证 FFmpeg 安装..."
    ffmpeg -version | head -1
    echo ""
    echo "🎉 FFmpeg 已准备就绪，现在可以运行 CodeWhisper 了！"
    echo ""
    exit 0
else
    echo ""
    echo "❌ FFmpeg 安装失败"
    echo "请手动安装，或访问: https://ffmpeg.org/download.html"
    exit 1
fi
