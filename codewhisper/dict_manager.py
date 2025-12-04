"""
字典管理器 - 管理程序员术语字典和文本修正
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from .utils import get_project_root


class DictionaryManager:
    """管理程序员术语字典"""

    def __init__(self, dict_path: Optional[str] = None):
        """
        初始化字典管理器

        Args:
            dict_path: 字典文件路径，如果为None则使用默认字典，支持后期其他行业如律师、医生专用术语改造
        """
        self.dict_path = dict_path
        self.replacements = self._load_dict()
        self.stats = {
            "total_rules": len(self.replacements),
            "replacements_made": 0
        }
        self.corrections = []  # 记录每次修正的详情

    def _load_dict(self) -> List[Dict]:
        """加载字典，优先使用自定义路径，否则使用默认路径"""
        # 确定字典文件路径
        dict_file = self._get_dict_file_path()

        if not dict_file or not os.path.exists(dict_file):
            print(f"❌ 字典文件不存在: {dict_file}")
            return []

        try:
            with open(dict_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✓ 已加载字典: {dict_file}")
                return self._parse_dict(data)
        except Exception as e:
            print(f"❌ 加载字典失败: {e}")
            return []

    def _get_dict_file_path(self) -> Optional[str]:
        """获取字典文件路径"""
        # 如果指定了自定义路径，使用自定义路径
        if self.dict_path:
            return self.dict_path

        # 否则使用默认路径
        root = get_project_root()
        default_path = os.path.join(root, 'dictionaries', 'programmer_terms.json')
        return default_path if os.path.exists(default_path) else None

    def _parse_dict(self, data: List[Dict]) -> List[Dict]:
        """解析字典数据"""
        rules = []

        # 按字典的类别->术语->变体结构获取字典数据
        for category_name, category_data in data.get("categories", {}).items():
            for term_name, term_data in category_data.get("terms", {}).items():
                for variant in term_data.get("variants", []):
                    wrong_text = variant.get("wrong", "")
                    correct_text = term_data.get("correct", "")

                    # 使用整体文本替换：对错误写法仅做 escape，不加 \b 边界。
                    # 好处：能稳定匹配语音转文字中格式不固定的内容（如 "Spring Boat"）。
                    # 局限：短词可能被误替换为词中子串，例如 "cat" 会匹配到 "Tomcat"，造成识别为“TomCat”
                    # 若需避免此类情况，可对短词启用严格边界匹配，待后续优化todo
                    regex_pattern = re.escape(wrong_text)

                    rules.append({
                        'wrong': regex_pattern,
                        'correct': correct_text,
                        'category': category_name
                    })

        return rules

    def fix_text(self, text: str, accumulate: bool = True) -> str:
        """
        修正文本中的开发者术语，CodeWhisper术语纠正的核心算法

        Args:
            text: 经录音后待纠正的文本
            accumulate: 是否累积修正记录。
                True  → 将本次修正追加到已有记录之后，用于连续多次调用时保留完整的修正历史。
                False → 调用前清空历史记录，仅保留本次修正结果，适合单次处理或独立批次分析。

        Returns:
            修正后的文本
        """
        # 如果手动设置追加记录为false，则清空之前的历史记录
        if not accumulate:
            self.corrections = []  # 清空上次的修正记录

        replacement_count = 0

        for item in self.replacements:
            pattern = item["wrong"]
            replacement = item["correct"]
            category = item.get("category", "unknown") # unknown兜底，防止没有这个类

            # 使用正则表达式进行替换，case-insensitive
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            if matches:
                # 替换前的文本
                text_before = text
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

                # 只有文本实际改变了，才记录和打印
                if text_before != text:
                    # 记录每个匹配的词
                    for match in matches:
                        self.corrections.append({
                            "wrong": match,
                            "correct": replacement,
                            "category": category
                        })
                    print(f"    🔧 替换: '{matches[0]}' → '{replacement}' ({category})")
                    replacement_count += len(matches)

        self.stats["replacements_made"] += replacement_count
        return text

    def add_replacement(self, wrong: str, correct: str, category: str = "custom"):
        """添加新的替换规则"""
        self.replacements.append({
            "wrong": wrong,
            "correct": correct,
            "category": category
        })
        self.stats["total_rules"] = len(self.replacements)

    def save_dict(self, output_path: str):
        """保存字典到文件"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # 按分类重新组织数据
        categories = {}
        for rule in self.replacements:
            category = rule.get('category', 'other')
            if category not in categories:
                categories[category] = []
            categories[category].append({
                'wrong': rule['wrong'],
                'correct': rule['correct'],
                'description': rule.get('description', '')
            })

        # 按分类构建输出格式
        output_data = [
            {
                'category': cat,
                'rules': rules
            }
            for cat, rules in sorted(categories.items())
        ]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"✓ 字典已保存: {output_path}")

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats

    def get_corrections(self) -> List[Dict]:
        """获取最近一次修正的详细列表"""
        return self.corrections

    def list_categories(self):
        """列出所有分类"""
        categories = {}
        for rule in self.replacements:
            cat = rule.get("category", "unknown")
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        return categories
