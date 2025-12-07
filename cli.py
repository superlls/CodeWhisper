#!/usr/bin/env python3
"""
CodeWhisper CLI - 为中文社区开发者打造的语音转文字工具

使用示例:
  python cli.py demo.m4a（你的音频文件，支持MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM ）      #基础转录（中文，默认）请在控制台执行此命令～
  python cli.py demo.m4a --language en      # 英文转录
  python cli.py demo.m4a --model base      # 使用 base 模型 （或者你可以选择其他模型）
  python cli.py --info                      # 显示统计信息
"""

import argparse
import sys
from pathlib import Path

from codewhisper.transcriber import CodeWhisper
from codewhisper.utils import print_result
from codewhisper.ffmpeg_utils import FFmpegChecker


def main():
    parser = argparse.ArgumentParser(
        description="CodeWhisper - 为中文社区开发者打造的语音转文字工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python cli.py audio.m4a（你的音频文件）  # 转录（默认走OpenAI开源的Whisper中文模型）（音频文件格式支持MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM ）
  python cli.py audio.m4a --language en # 英文转录
  python cli.py audio.m4a --model base # 使用 base 模型 或者你也可以改成其他
  python cli.py --info                 # 显示统计信息

 CodeWhisper 为中文社区开发者设计，发现新的错误映射？欢迎提 PR！"""
    )

    parser.add_argument("audio_file", nargs="?", help="音频文件路径")
    parser.add_argument("--model", default="base", help="可选模型：tiny/base/small/medium/large")
    parser.add_argument("--language", default="zh", help="语言代码: zh/en/... (默认走zh中文识别)")
    parser.add_argument("--no-fix", action="store_true", help="不修正编程术语")
    parser.add_argument("--verbose", action="store_true", help="显示修正详情")
    parser.add_argument("--segments", action="store_true", help="显示详细分段")
    parser.add_argument("--info", action="store_true", help="显示统计信息")
    parser.add_argument("--dict", help="自定义字典文件路径")#后续支持用户添加自定义个性化字典todo


    args = parser.parse_args()

    # 检查 FFmpeg（仅在需要转录音频时检查）
    if args.audio_file or (not args.info and not args.audio_file and len(sys.argv) > 1):
        # 用户想要转录音频，检查 FFmpeg
        FFmpegChecker.check_and_exit_if_missing()

    # 显示信息模式
    if args.info:
        try:
            cw = CodeWhisper(model_name="base", dict_path=args.dict) #默认CLI使用base模型，后续支持用户使用命令添加自定义个性化字典todo
            categories = cw.get_dict_categories()
            prompt_stats = cw.get_prompt_stats()

            print("\n" + "=" * 50)
            print("📊 CodeWhisper 统计信息")
            print("=" * 50)
            print("\n字典规则分类：")
            total = sum(categories.values())
            for cat, count in sorted(categories.items()):
                print(f"  {cat:12} : {count:2} 条")
            print(f"  {'总计':12} : {total:2} 条")

            print("\n智能提示词引擎：")
            print(f"  通用术语数   : {prompt_stats['base_terms_count']} 条")
            print(f"  用户术语数   : {prompt_stats['user_terms_count']} 条")
            print(f"  有效术语数   : {prompt_stats['qualified_user_terms']} 条")
            print(f"\n当前提示词：")
            print(f"  {prompt_stats['current_prompt']}")

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
