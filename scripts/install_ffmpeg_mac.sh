#!/bin/bash

# CodeWhisper FFmpeg 自动安装脚本 (macOS)
# 使用方法: bash scripts/install_ffmpeg_mac.sh

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        CodeWhisper FFmpeg 自动安装脚本 (macOS)                ║"
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

# 检查 Homebrew
if ! command -v brew &> /dev/null; then
    echo "⚠️  Homebrew 未安装，正在安装 Homebrew..."
    echo "这可能需要几分钟...（可能会要求输入密码）"
    echo ""

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Homebrew 安装失败"
        echo "请手动访问: https://brew.sh 安装 Homebrew"
        exit 1
    fi

    echo ""
    echo "✅ Homebrew 安装成功！"
fi

# 安装 FFmpeg
echo ""
echo "📥 使用 Homebrew 安装 FFmpeg..."
echo "这可能需要几分钟..."
echo ""

brew install ffmpeg

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
    echo "请手动运行: brew install ffmpeg"
    exit 1
fi
