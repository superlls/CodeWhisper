"""
工具函数
"""

import os
from pathlib import Path
from typing import Optional

try:
    from hanziconv import HanziConv
    HANZICONV_AVAILABLE = True
except ImportError:
    HANZICONV_AVAILABLE = False


def normalize_zh_punctuation(text: str) -> str:
    """
    规范化中文输出的标点符号。

    目前仅处理：英文逗号 `,` -> 中文逗号 `，`。
    """
    if not text:
        return text

    return text.replace(",", "，")


def convert_to_simplified_chinese(text: str) -> str:
    """
    将繁体中文转换为简体中文

    Args:
        text: 输入文本

    Returns:
        转换后的简体中文文本
    """
    if not text:
        return text

    if HANZICONV_AVAILABLE:
        return HanziConv.toSimplified(text)
    else:
        # 如果 hanziconv 不可用，返回原文本并打印警告
        print("⚠️  hanziconv 库未安装，无法进行繁体转简体转换")
        print("📦 请运行: pip install hanziconv")
        return text


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent.parent


def format_seconds(seconds: float) -> str:
    """格式化秒数为时间字符串"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m{secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h{minutes}m"


def print_result(result: dict, show_segments: bool = False):
    """打印转录结果"""
    print("\n" + "=" * 60)
    print("📝 转录结果")
    print("=" * 60)
    print(result["text"])

    if show_segments:
        print("\n" + "=" * 60)
        print("📋 详细分段")
        print("=" * 60)
        for segment in result.get("segments", []):
            start = format_seconds(segment["start"])
            end = format_seconds(segment["end"])
            print(f"[{start} - {end}] {segment['text']}")

    print("=" * 60 + "\n")
