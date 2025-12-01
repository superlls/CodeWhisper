#!/usr/bin/env python3
"""
CodeWhisper CLI - 程序员专用语音转文字工具

使用示例:
  python cli.py demo.m4a                    # 基础转录（中文，默认）！！在控制台执行此命令
  python cli.py demo.m4a --language en      # 英文转录
  python cli.py demo.m4a --model small      # 使用 small 模型 （或者你可以选择其他模型）
  python cli.py --info                      # 显示统计信息
"""

import argparse
import sys
from pathlib import Path

from codewhisper.transcriber import CodeWhisper
from codewhisper.utils import print_result


def main():
    parser = argparse.ArgumentParser(
        description="CodeWhisper - 为中国程序员打造的语音转文字工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python cli.py audio.m4a              # 转录（中文，默认）
  python cli.py audio.m4a --language en # 英文转录
  python cli.py audio.m4a --model small # 使用 small 模型
  python cli.py --info                 # 显示统计信息

提示：CodeWhisper 专为中国程序员设计。发现识别错误？欢迎提 PR！"""
    )

    parser.add_argument("audio_file", nargs="?", help="音频文件路径")
    parser.add_argument("--model", default="base", help="模型: tiny/base/small/medium/large (默认: base)")
    parser.add_argument("--language", default="zh", help="语言代码: zh/en/... (默认: zh)")
    parser.add_argument("--no-fix", action="store_true", help="不修正编程术语")
    parser.add_argument("--verbose", action="store_true", help="显示修正详情")
    parser.add_argument("--segments", action="store_true", help="显示详细分段")
    parser.add_argument("--info", action="store_true", help="显示统计信息")
    parser.add_argument("--dict", help="自定义字典文件路径")

    args = parser.parse_args()

    # 显示信息模式
    if args.info:
        try:
            cw = CodeWhisper(model_name="base", dict_path=args.dict)
            categories = cw.get_dict_categories()

            print("\n" + "=" * 50)
            print("📊 CodeWhisper 统计信息")
            print("=" * 50)
            print("\n字典规则分类：")
            total = sum(categories.values())
            for cat, count in sorted(categories.items()):
                print(f"  {cat:12} : {count:2} 条")
            print(f"  {'总计':12} : {total:2} 条")
            print("\n支持的模型：tiny, base, small, medium, large")
            print("=" * 50 + "\n")
        except Exception as e:
            print(f"❌ 错误: {e}\n")
        return

    # 转录模式
    if not args.audio_file:
        parser.print_help()
        return

    # 检查文件
    audio_path = Path(args.audio_file)
    if not audio_path.exists():
        print(f"❌ 文件不存在: {args.audio_file}\n")
        sys.exit(1)

    try:
        print(f"\n🎙️ 转录中...")
        print(f"  文件: {audio_path.name}")
        print(f"  模型: {args.model} | 语言: {args.language} | 修正: {'✓' if not args.no_fix else '✗'}\n")

        cw = CodeWhisper(model_name=args.model, dict_path=args.dict)
        result = cw.transcribe(
            str(audio_path),
            language=args.language,
            fix_programmer_terms=not args.no_fix,
            verbose=True
        )

        print_result(result, show_segments=args.segments)

        # 显示修正统计
        if not args.no_fix:
            corrections = cw.dict_manager.get_corrections()
            stats = cw.get_dict_stats()

            print(f"📊 修正统计: {stats['replacements_made']} 处修正")

            # 如果指定了 --verbose，显示修正详情
            if args.verbose and corrections:
                print("\n✏️ 修正详情：")
                for correction in corrections:
                    print(f"  '{correction['wrong']}' → '{correction['correct']}' ({correction['category']})")
            print()

    except Exception as e:
        print(f"❌ 错误: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
