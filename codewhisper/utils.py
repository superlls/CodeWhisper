
"""
工具函数
"""

import os
from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent.parent


def get_dict_path(dict_name: str = "programmer_dict.json") -> Path:
    """获取字典文件路径"""
    return get_project_root() / "dictionaries" / dict_name


def ensure_dict_exists(dict_path: Optional[str] = None) -> Path:
    """确保字典文件存在，如果不存在则创建"""
    if dict_path:
        path = Path(dict_path)
    else:
        path = get_dict_path()

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        print(f"⚠ 字典文件不存在: {path}")
        print(f"使用内置字典")

    return path


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
