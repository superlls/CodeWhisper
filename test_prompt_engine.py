#!/usr/bin/env python3
"""
测试 PromptEngine 学习功能的脚本
"""

from codewhisper.prompt_engine import PromptEngine
from codewhisper.dict_manager import DictionaryManager

def test_prompt_engine():
    print("=" * 60)
    print("测试 PromptEngine 学习功能")
    print("=" * 60)

    # 初始化引擎
    engine = PromptEngine()
    dict_manager = DictionaryManager()

    print("\n1️⃣ 初始状态：")
    stats = engine.get_stats()
    print(f"  用户术语数: {stats['user_terms_count']}")
    print(f"  当前提示词: {stats['current_prompt']}")

    # 模拟第一次使用：用户说了一些包含 Dubbo, Redis 的话
    print("\n2️⃣ 模拟转录文本1（包含 Dubbo、Redis、MySQL）：")
    mock_text_1 = "今天我在做Dubbo服务的开发，需要连接Redis和MySQL数据库。"
    detected_terms_1 = dict_manager.detect_terms_in_text(mock_text_1)
    print(f"  检测到术语: {detected_terms_1}")
    engine.update_user_terms(detected_terms_1)

    stats = engine.get_stats()
    print(f"  用户术语数: {stats['user_terms_count']}")

    # 模拟第二次使用：用户又说了 Dubbo, Redis（频次增加）
    print("\n3️⃣ 模拟转录文本2（再次出现 Dubbo、Redis）：")
    mock_text_2 = "Dubbo的配置有问题，Redis缓存也需要优化。"
    detected_terms_2 = dict_manager.detect_terms_in_text(mock_text_2)
    print(f"  检测到术语: {detected_terms_2}")
    engine.update_user_terms(detected_terms_2)

    stats = engine.get_stats()
    print(f"  用户术语数: {stats['user_terms_count']}")

    # 模拟第三次使用：频次达到阈值
    print("\n4️⃣ 模拟转录文本3（第三次出现 Dubbo、Redis）：")
    mock_text_3 = "调试Dubbo服务，优化Redis性能。"
    detected_terms_3 = dict_manager.detect_terms_in_text(mock_text_3)
    print(f"  检测到术语: {detected_terms_3}")
    engine.update_user_terms(detected_terms_3)

    stats = engine.get_stats()
    print(f"  用户术语数: {stats['user_terms_count']}")
    print(f"  有效术语数 (freq>=3): {stats['qualified_user_terms']}")

    print("\n5️⃣ 更新后的提示词：")
    new_prompt = engine.build_prompt()
    print(f"  {new_prompt}")

    print("\n6️⃣ 用户术语库详情：")
    for term in sorted(engine.user_dict, key=lambda x: x['freq'], reverse=True):
        print(f"  {term['term']:15} - 频次: {term['freq']}")

    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_prompt_engine()
