#!/usr/bin/env python3
"""
CodeWhisper CLI - 程序员专用语音转文字工具

使用示例:
  python cli.py demo.m4a                           # 基础转录（中文，默认）
  python cli.py demo.m4a --language en             # 转录英文音频
  python cli.py demo.m4a --model tiny              # 使用 tiny 模型（最快）
  python cli.py demo.m4a --segments                # 显示详细分段
  python cli.py --info                             # 显示信息和统计
CodeWhisper 默认使用中文模式，专为中国程序员设计。
发现术语识别错误？欢迎提 Issue 或 PR 帮助完善词典！
"""

import argparse
import sys
from pathlib import Path

from codewhisper.transcriber import CodeWhisper
from codewhisper.utils import print_result, format_seconds


def main():
    parser = argparse.ArgumentParser(
        description="CodeWhisper - Programmer-friendly speech-to-text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python cli.py demo.m4a                    # 转录 demo.m4a（中文，默认）
  python cli.py demo.m4a --language en      # 转录英文音频
  python cli.py demo.m4a --model tiny       # 使用 tiny 模型（最快）
  python cli.py --info                      # 显示信息和统计

提示：CodeWhisper 默认使用中文模式，专为中国程序员设计。
发现识别错误？欢迎提 Issue 或 PR 帮我们完善术语字典！
        """
    )

    parser.add_argument("audio_file", nargs="?", help="音频文件路径")
    parser.add_argument("--model", default="base", help="模型大小 (tiny/base/small/medium/large)")
    parser.add_argument("--language", default="zh", help="语言代码 (zh, en, etc，默认中文)")
    parser.add_argument("--no-fix", action="store_true", help="不修正程序员术语")
    parser.add_argument("--segments", action="store_true", help="显示详细分段")
    parser.add_argument("--info", action="store_true", help="显示信息和统计")
    parser.add_argument("--dict", help="自定义字典文件路径")

    args = parser.parse_args()

    # 显示信息模式
    if args.info:
        print("\n" + "=" * 60)
        print("CodeWhisper v0.1.0")
        print("=" * 60)
        print("Programmer-friendly speech-to-text tool")
        print("基于 OpenAI Whisper 构建")
        print()

        # 初始化以获取统计信息
        try:
            cw = CodeWhisper(model_name="base", dict_path=args.dict)
            print("📊 字典统计")
            print("-" * 60)
            categories = cw.get_dict_categories()
            total = 0
            for cat, count in sorted(categories.items()):
                print(f"  {cat:15} : {count:3} 条规则")
                total += count
            print(f"  {'总计':15} : {total:3} 条规则")
            print()

            print("📋 支持的模型")
            print("-" * 60)
            for model in cw.get_supported_models():
                print(f"  - {model}")
            print()
            print("=" * 60 + "\n")
        except Exception as e:
            print(f"❌ 错误: {e}\n")
        return

    # 转录模式
    if not args.audio_file:
        parser.print_help()
        return

    # 检查文件是否存在
    audio_path = Path(args.audio_file)
    if not audio_path.exists():
        print(f"❌ 错误: 文件不存在 - {args.audio_file}\n")
        sys.exit(1)

    try:
        # 初始化 CodeWhisper
        print(f"\n🚀 开始转录")
        print(f"   文件: {args.audio_file}")
        print(f"   模型: {args.model}")
        print(f"   语言: {args.language}")
        if not args.no_fix:
            print(f"   修正: ✓ 启用")
        print()

        cw = CodeWhisper(model_name=args.model, dict_path=args.dict)

        # 进行转录
        result = cw.transcribe(
            str(audio_path),
            language=args.language,
            fix_programmer_terms=not args.no_fix,
            verbose=True
        )

        # 打印结果
        print_result(result, show_segments=args.segments)

        # 显示统计
        if not args.no_fix:
            stats = cw.get_dict_stats()
            print(f"📊 修正统计")
            print(f"   应用规则: {stats['total_rules']} 条")
            print(f"   修正次数: {stats['replacements_made']} 处")
            print()

    except Exception as e:
        print(f"\n❌ 错误: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
