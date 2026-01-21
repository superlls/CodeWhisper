"""
Prompt Engine - 可配置、可扩展、能持续学习用户习惯的个性化提示词构建系统
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Set
from pathlib import Path

from .console import debug, warn


class PromptEngine:
    """智能提示词引擎

    功能：
    1. 从配置文件读取提示词生成规则
    2. 维护固定的通用术语库（base_dict）
    3. 维护动态的用户个性化术语库（user_dict）
    4. 根据用户历史使用情况，动态选取术语
    5. 构建最优的 Whisper initial_prompt
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化提示词引擎

        Args:
            config_path: 配置文件路径，默认使用 config/base_config.json
        """
        # 确定配置文件路径
        if config_path is None:
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "base_config.json"

        self.config_path = Path(config_path)
        self.config = self._load_config()

        # 加载通用术语库和用户术语库
        self.base_dict = self._load_base_dict()
        self.user_dict = self._load_user_dict()

        debug("✓ Prompt Engine 初始化完成")
        debug(f"  通用术语数: {len(self.base_dict)}")
        debug(f"  用户术语数: {len(self.user_dict)}")

    def _load_config(self) -> Dict:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                debug(f"✓ 已加载配置: {self.config_path}")
                return config
        except Exception as e:
            warn(f"❌ 加载配置文件失败: {e}")
            # 返回默认配置
            return {
                "prompt_prefix": "计算机行业从业者：",
                "user_dict_path": "config/user_dict.json",
                "base_dict_path": "config/base_dict.json",
                "max_user_terms": 20,
                "prompt_total_terms": 10,
                "prompt_base_terms": 5,
                "user_term_min_freq": 3
            }

    def _load_base_dict(self) -> List[str]:
        """加载通用术语库（固定不变）"""
        project_root = Path(__file__).parent.parent
        base_dict_path = project_root / self.config.get("base_dict_path", "config/base_dict.json")

        try:
            with open(base_dict_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                terms = data.get("terms", [])
                debug(f"✓ 已加载通用术语库: {len(terms)} 个术语")
                return terms
        except Exception as e:
            warn(f"❌ 加载通用术语库失败: {e}")
            return []

    def _load_user_dict(self) -> List[Dict]:
        """加载用户个性化术语库（动态可学习）"""
        project_root = Path(__file__).parent.parent
        user_dict_path = project_root / self.config.get("user_dict_path", "config/user_dict.json")

        try:
            with open(user_dict_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                terms = data.get("terms", [])
                debug(f"✓ 已加载用户术语库: {len(terms)} 个术语")
                return terms
        except Exception as e:
            debug("⚠️  用户术语库文件不存在或为空，将创建新库")
            return []

    def _save_user_dict(self):
        """保存用户术语库到文件"""
        project_root = Path(__file__).parent.parent
        user_dict_path = project_root / self.config.get("user_dict_path", "config/user_dict.json")

        try:
            with open(user_dict_path, 'w', encoding='utf-8') as f:
                json.dump({"terms": self.user_dict}, f, ensure_ascii=False, indent=2)
            debug(f"💾 用户术语库已保存: {len(self.user_dict)} 个术语")
        except Exception as e:
            warn(f"❌ 保存用户术语库失败: {e}")

    def build_prompt(self) -> str:
        """
        构建 Whisper 提示词（核心算法）

        策略：
        1. 从 base_dict 取前 prompt_base_terms 个术语（固定偏置）
        2. 从 user_dict 取频次最高的个性化术语
        3. 如果个性化术语不足，用 base_dict 补齐
        4. 拼接成：{prefix}{term1}、{term2}、...、{term10}。

        Returns:
            完整的提示词字符串
        """
        prefix = self.config.get("prompt_prefix", "计算机行业从业者：")
        total_terms = self.config.get("prompt_total_terms", 10)
        base_terms_count = self.config.get("prompt_base_terms", 5)
        min_freq = self.config.get("user_term_min_freq", 3)

        selected_terms = []

        # 1. 从 base_dict 取前 N 个通用术语
        base_terms = self.base_dict[:base_terms_count]
        selected_terms.extend(base_terms)

        # 2. 从 user_dict 取高频个性化术语
        # 过滤出 freq >= min_freq 的术语
        qualified_user_terms = [
            term for term in self.user_dict
            if term.get("freq", 0) >= min_freq
        ]

        # 按 freq DESC, last_used DESC 排序
        sorted_user_terms = sorted(
            qualified_user_terms,
            key=lambda x: (x.get("freq", 0), x.get("last_used", "")),
            reverse=True
        )

        # 取需要的个性化术语数量
        user_terms_count = total_terms - base_terms_count
        user_terms = [term["term"] for term in sorted_user_terms[:user_terms_count]]
        selected_terms.extend(user_terms)

        # 3. 如果个性化术语不足，用 base_dict 后续术语补齐
        if len(selected_terms) < total_terms:
            remaining_count = total_terms - len(selected_terms)
            # 从 base_dict 中取未使用的术语
            additional_base_terms = [
                term for term in self.base_dict[base_terms_count:]
                if term not in selected_terms
            ][:remaining_count]
            selected_terms.extend(additional_base_terms)

        # 去重（保持顺序）
        seen = set()
        unique_terms = []
        for term in selected_terms:
            if term not in seen:
                seen.add(term)
                unique_terms.append(term)

        # 4. 拼接成最终 prompt
        terms_str = "、".join(unique_terms[:total_terms])
        prompt = f"{prefix}{terms_str}。"

        return prompt

    def update_user_terms(self, detected_terms: Set[str]):
        """
        更新用户术语库（学习用户习惯）

        Args:
            detected_terms: 从转录文本中检测到的术语集合
        """
        if not detected_terms:
            return

        current_time = datetime.now().isoformat()
        updated = False

        for term in detected_terms:
            # 查找该术语是否已存在
            existing_term = next(
                (t for t in self.user_dict if t["term"] == term),
                None
            )

            if existing_term:
                # 已存在，更新频次和最后使用时间
                existing_term["freq"] += 1
                existing_term["last_used"] = current_time
                updated = True
            else:
                # 不存在，添加新术语
                self.user_dict.append({
                    "term": term,
                    "freq": 1,
                    "last_used": current_time
                })
                updated = True

        if updated:
            # 维护用户术语库（淘汰低频词）
            self._maintain_user_dict()
            # 保存到文件
            self._save_user_dict()

    def _maintain_user_dict(self):
        """
        维护用户术语库（容量控制和淘汰机制）

        规则：
        1. 最多保留 max_user_terms 个术语
        2. 按 freq DESC, last_used DESC 排序
        3. 保留前 N 个，删除多余的
        """
        max_terms = self.config.get("max_user_terms", 20)

        if len(self.user_dict) <= max_terms:
            return

        # 按频次和最后使用时间排序
        sorted_terms = sorted(
            self.user_dict,
            key=lambda x: (x.get("freq", 0), x.get("last_used", "")),
            reverse=True
        )

        # 只保留前 max_terms 个
        removed_count = len(self.user_dict) - max_terms
        self.user_dict = sorted_terms[:max_terms]

        debug(f"🗑️  用户术语库淘汰了 {removed_count} 个低频术语")

    def get_stats(self) -> Dict:
        """获取统计信息"""
        min_freq = self.config.get("user_term_min_freq", 3)
        qualified_terms = [
            term for term in self.user_dict
            if term.get("freq", 0) >= min_freq
        ]

        return {
            "base_terms_count": len(self.base_dict),
            "user_terms_count": len(self.user_dict),
            "qualified_user_terms": len(qualified_terms),
            "current_prompt": self.build_prompt()
        }
