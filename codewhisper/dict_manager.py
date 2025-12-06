"""
字典管理器 - 管理中文社区开发者术语字典和文本修正
"""

import json
import os
import re
from typing import Dict, List, Optional, Set

from .utils import get_project_root


class DictionaryManager:
    """管理术语字典"""

    def __init__(self, dict_path: Optional[str] = None):
        """
        初始化字典管理器

        Args:
            dict_path: 字典文件路径，如果为None则使用默认字典，支持后期其他行业如律师、医生专用术语改造 todo
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
        # 如果指定了自定义路径，使用自定义路径，支持后续用户拓展自定义字典
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

                    # 构建正则表达式：短词（≤3字符）添加单词边界 \b，防止子串误匹配
                    # 例如：避免 "Cat" 被误纠正为 "TomCat"，
                    # 长词不用边界，保留原有的灵活性，能匹配格式不固定的内容（如 "Spring Boat"）
                    escaped_text = re.escape(wrong_text)

                    # 判断是否为短词（仅包含字母/数字，长度≤3）
                    if re.match(r'^[a-zA-Z0-9]+$', wrong_text) and len(wrong_text) <= 3:
                        regex_pattern = r'\b' + escaped_text + r'\b'
                    else:
                        regex_pattern = escaped_text

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
                    print(f" 🔧替换: '{matches[0]}' → '{replacement}' ({category})")
                    replacement_count += len(matches)

        self.stats["replacements_made"] += replacement_count
        return text

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

    def build_prompt_terms(self) -> str:
        """
        从字典动态生成 Whisper 提示词

        提取字典中所有术语（correct 字段），生成逗号分隔的提示词字符串。
        这样可以让 Whisper 在转录时优先识别编程术语，无需手动维护术语列表。

        Returns:
            逗号分隔的术语字符串，如 "Python, JavaScript, MySQL, Docker, ..."
        """
        terms = set()

        for rule in self.replacements:
            correct_term = rule.get('correct', '')
            if correct_term and correct_term not in terms:
                terms.add(correct_term)

        # 返回逗号分隔的术语列表
        # 排序后可以保证稳定性，限制数量避免 prompt 过长
        prompt_terms = ", ".join(sorted(terms))
        return prompt_terms

    def detect_terms_in_text(self, text: str) -> Set[str]:
        """
        检测文本中出现的术语（用于学习用户习惯）

        Args:
            text: 转录后的文本

        Returns:
            检测到的术语集合（correct 形式）
        """
        detected_terms = set()

        for rule in self.replacements:
            correct_term = rule.get('correct', '')
            if not correct_term:
                continue

            # 检查文本中是否包含该术语（大小写不敏感）
            # 使用简单的包含检查，避免复杂的正则
            if correct_term.lower() in text.lower():
                detected_terms.add(correct_term)

        return detected_terms

    def get_detected_terms_from_corrections(self) -> Set[str]:
        """
        从最近的修正记录中获取被修正的术语

        这个方法用于获取用户在本次转录中实际使用的术语。
        当某个术语被修正（wrong → correct），说明用户提到了它。

        Returns:
            被修正的术语集合（correct 形式）
        """
        detected_terms = set()

        for correction in self.corrections:
            correct_term = correction.get('correct', '')
            if correct_term:
                detected_terms.add(correct_term)

        return detected_terms
