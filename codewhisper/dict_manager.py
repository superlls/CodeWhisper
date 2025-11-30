"""
字典管理器 - 管理程序员术语字典和文本修正
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional


class DictionaryManager:
    """管理程序员术语字典"""

    def __init__(self, dict_path: Optional[str] = None):
        """
        初始化字典管理器

        Args:
            dict_path: 字典文件路径，如果为None则使用默认字典
        """
        self.dict_path = Path(dict_path) if dict_path else None
        self.replacements = self._load_dict()
        self.stats = {
            "total_rules": len(self.replacements),
            "replacements_made": 0
        }

    def _load_dict(self) -> List[Dict]:
        """加载字典"""
        # 如果提供了路径，先尝试加载
        if self.dict_path and self.dict_path.exists():
            try:
                with open(self.dict_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✓ 已加载字典: {self.dict_path}")
                    return data.get('replacements', [])
            except Exception as e:
                print(f"⚠ 加载字典失败: {e}，使用内置字典")

        # 使用内置的基础程序员词典
        return self._get_builtin_dict()

    def _get_builtin_dict(self) -> List[Dict]:
        """从 JSON 文件读取内置字典"""
        try:
            # 优先读取用户自定义字典
            dict_path = self.dict_path or self._get_default_dict_path()

            if dict_path and os.path.exists(dict_path):
                with open(dict_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 扁平化数据结构：将分类下的规则展开
                    rules = []
                    for category_group in data:
                        category = category_group.get('category', 'other')
                        for rule in category_group.get('rules', []):
                            # 转换为正则表达式格式
                            wrong_text = rule.get('wrong', '')

                            # 检查是否包含中文
                            if self._contains_chinese(wrong_text):
                                # 中文：直接使用，不加单词边界
                                regex_pattern = re.escape(wrong_text)
                            else:
                                # 英文：添加单词边界和转义
                                regex_pattern = r'\b' + re.escape(wrong_text) + r'\b'

                            rules.append({
                                'wrong': regex_pattern,
                                'correct': rule.get('correct', ''),
                                'category': category
                            })
                    return rules
        except Exception as e:
            print(f"⚠️  读取字典文件失败: {e}，使用内置默认字典")

        # 如果文件不存在或读取失败，返回硬编码的默认字典
        return self._get_default_dict()

    def _contains_chinese(self, text: str) -> bool:
        """检查文本是否包含中文"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False

    def _get_default_dict(self) -> List[Dict]:
        """硬编码的默认字典（备用）"""
        return [
            # ========== 数据库 ==========
            {"wrong": r"\bmy\s+circle\b", "correct": "MySQL", "category": "database"},
            {"wrong": r"\bmy\s+sql\b", "correct": "MySQL", "category": "database"},
            {"wrong": r"\bmessage\s+core\b", "correct": "MySQL", "category": "database"},  # 中文模式误识别
            {"wrong": r"\bmy\s+s\s+q\s+l\b", "correct": "MySQL", "category": "database"},  # 分开读音
            {"wrong": r"\bsequel\b", "correct": "SQL", "category": "database"},
            {"wrong": r"\bpost\s*gres\b", "correct": "PostgreSQL", "category": "database"},
            {"wrong": r"\bpost\s+gres\s+sql\b", "correct": "PostgreSQL", "category": "database"},
            {"wrong": r"\bmongo\s*db\b", "correct": "MongoDB", "category": "database"},
            {"wrong": r"\bredis\b", "correct": "Redis", "category": "database"},
            {"wrong": r"\bmariadb\b", "correct": "MariaDB", "category": "database"},

            # ========== 数据格式 ==========
            {"wrong": r"\bj\s*son\b", "correct": "JSON", "category": "format"},
            {"wrong": r"\bjson\b", "correct": "JSON", "category": "format"},
            {"wrong": r"\bx\s*ml\b", "correct": "XML", "category": "format"},
            {"wrong": r"\byaml\b", "correct": "YAML", "category": "format"},
            {"wrong": r"\bcsv\b", "correct": "CSV", "category": "format"},

            # ========== 编程语言 ==========
            {"wrong": r"\bpython\b", "correct": "Python", "category": "language"},
            {"wrong": r"\bjava\s*script\b", "correct": "JavaScript", "category": "language"},
            {"wrong": r"\bj\s*s\b", "correct": "JS", "category": "language"},
            {"wrong": r"\btype\s*script\b", "correct": "TypeScript", "category": "language"},
            {"wrong": r"\bgolang\b", "correct": "Go", "category": "language"},
            {"wrong": r"\brust\b", "correct": "Rust", "category": "language"},
            {"wrong": r"\bjava\b", "correct": "Java", "category": "language"},
            {"wrong": r"\bc\+\+\b", "correct": "C++", "category": "language"},
            {"wrong": r"\bc\s*sharp\b", "correct": "C#", "category": "language"},
            {"wrong": r"\bphp\b", "correct": "PHP", "category": "language"},
            {"wrong": r"\bruby\b", "correct": "Ruby", "category": "language"},
            {"wrong": r"\bkotlin\b", "correct": "Kotlin", "category": "language"},

            # ========== 前端框架 ==========
            {"wrong": r"\breact\b", "correct": "React", "category": "framework"},
            {"wrong": r"\bvue\b", "correct": "Vue", "category": "framework"},
            {"wrong": r"\bangular\b", "correct": "Angular", "category": "framework"},
            {"wrong": r"\bsvelte\b", "correct": "Svelte", "category": "framework"},
            {"wrong": r"\bnode\s*\.?\s*js\b", "correct": "Node.js", "category": "framework"},
            {"wrong": r"\bexpress\b", "correct": "Express", "category": "framework"},

            # ========== 后端框架 ==========
            {"wrong": r"\bdjango\b", "correct": "Django", "category": "framework"},
            {"wrong": r"\bflask\b", "correct": "Flask", "category": "framework"},
            {"wrong": r"\bfast\s*api\b", "correct": "FastAPI", "category": "framework"},
            {"wrong": r"\bspring\b", "correct": "Spring", "category": "framework"},

            # ========== 工具 ==========
            {"wrong": r"\bdocker\b", "correct": "Docker", "category": "tools"},
            {"wrong": r"\bkubernetes\b", "correct": "Kubernetes", "category": "tools"},
            {"wrong": r"\bkubectl\b", "correct": "kubectl", "category": "tools"},
            {"wrong": r"\bgit\s+hub\b", "correct": "GitHub", "category": "tools"},
            {"wrong": r"\bgit\s+lab\b", "correct": "GitLab", "category": "tools"},
            {"wrong": r"\bgit\b", "correct": "Git", "category": "tools"},
            {"wrong": r"\bnginx\b", "correct": "Nginx", "category": "tools"},
            {"wrong": r"\bapache\b", "correct": "Apache", "category": "tools"},
            {"wrong": r"\bgradle\b", "correct": "Gradle", "category": "tools"},
            {"wrong": r"\bmaven\b", "correct": "Maven", "category": "tools"},
            {"wrong": r"\bnpm\b", "correct": "npm", "category": "tools"},
            {"wrong": r"\byarn\b", "correct": "Yarn", "category": "tools"},
            {"wrong": r"\bpip\b", "correct": "pip", "category": "tools"},

            # ========== 概念 ==========
            {"wrong": r"\bapi\b", "correct": "API", "category": "concept"},
            {"wrong": r"\brest\b", "correct": "REST", "category": "concept"},
            {"wrong": r"\bgraph\s*ql\b", "correct": "GraphQL", "category": "concept"},
            {"wrong": r"\brest\s*ful\b", "correct": "RESTful", "category": "concept"},
            {"wrong": r"\bsql\b", "correct": "SQL", "category": "concept"},
            {"wrong": r"\borm\b", "correct": "ORM", "category": "concept"},
            {"wrong": r"\bcicd\b", "correct": "CI/CD", "category": "concept"},
            {"wrong": r"\bci\s*cd\b", "correct": "CI/CD", "category": "concept"},
            {"wrong": r"\bcrud\b", "correct": "CRUD", "category": "concept"},
            {"wrong": r"\bmvc\b", "correct": "MVC", "category": "concept"},
            {"wrong": r"\baws\b", "correct": "AWS", "category": "concept"},
            {"wrong": r"\bgcp\b", "correct": "GCP", "category": "concept"},
            {"wrong": r"\bazure\b", "correct": "Azure", "category": "concept"},

            # ========== 其他 ==========
            {"wrong": r"\bhttp\b", "correct": "HTTP", "category": "other"},
            {"wrong": r"\bhttps\b", "correct": "HTTPS", "category": "other"},
            {"wrong": r"\bssl\b", "correct": "SSL", "category": "other"},
            {"wrong": r"\btls\b", "correct": "TLS", "category": "other"},
            {"wrong": r"\blinux\b", "correct": "Linux", "category": "other"},
            {"wrong": r"\bubuntu\b", "correct": "Ubuntu", "category": "other"},
            {"wrong": r"\bdebian\b", "correct": "Debian", "category": "other"},
            {"wrong": r"\bcentos\b", "correct": "CentOS", "category": "other"},
        ]

    def _get_default_dict_path(self) -> Optional[str]:
        """获取默认字典文件路径"""
        try:
            root = get_project_root()
            dict_file = os.path.join(root, 'dictionaries', 'programmer_terms.json')
            return dict_file if os.path.exists(dict_file) else None
        except:
            return None

    def fix_text(self, text: str) -> str:
        """
        修正文本中的程序员术语

        Args:
            text: 输入文本

        Returns:
            修正后的文本
        """
        original_text = text
        replacement_count = 0

        for item in self.replacements:
            pattern = item["wrong"]
            replacement = item["correct"]

            # 使用正则表达式进行替换，case-insensitive
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            if matches:
                replacement_count += len(matches)

            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

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

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"replacements": self.replacements}, f, indent=2, ensure_ascii=False)

        print(f"✓ 字典已保存: {output_path}")

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats

    def list_categories(self):
        """列出所有分类"""
        categories = {}
        for rule in self.replacements:
            cat = rule.get("category", "unknown")
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        return categories
