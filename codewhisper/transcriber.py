"""
转录引擎 - 基于 OpenAI Whisper 的转录核心
"""

import whisper
from typing import Dict, Optional
from .dict_manager import DictionaryManager


class CodeWhisper:
    """主转录引擎"""

    def __init__(self, model_name: str = "base", dict_path: Optional[str] = None):
        """
        初始化 CodeWhisper

        Args:
            model_name: Whisper 模型大小 (tiny, base, small, medium, large)
            dict_path: 自定义字典路径
        """
        print(f"📦 加载 Whisper 模型: {model_name}")
        self.model = whisper.load_model(model_name)
        self.model_name = model_name

        print(f"📚 加载字典管理器")
        self.dict_manager = DictionaryManager(dict_path)

        print(f"✓ CodeWhisper 初始化完成\n")

    def transcribe(
        self,
        audio_file: str,
        language: Optional[str] = "en",
        fix_programmer_terms: bool = True,
        verbose: bool = True,
        temperature: float = 0.0,
    ) -> Dict:
        """
        转录音频文件

        Args:
            audio_file: 音频文件路径
            language: 语言代码 (en, zh, etc). For mixed Chinese-English, 'en' mode works best
            fix_programmer_terms: 是否修正程序员术语
            verbose: 是否打印详细信息
            temperature: 采样温度

        Returns:
            包含转录结果的字典
        """
        # 创建提示词，帮助模型识别技术术语
        programmer_prompt = (
            "MySQL, PostgreSQL, MongoDB, Redis, "
            "Python, JavaScript, TypeScript, Go, C++, "
            "React, Vue, Angular, Django, Flask, Express, "
            "Docker, Kubernetes, GitHub, GitLab, "
            "API, REST, GraphQL, JSON, XML, YAML, "
            "HTTP, HTTPS, SSL, TLS, "
            "Linux, Ubuntu, Debian, CentOS"
        )

        # 优化语言处理：默认中文模式，专为中国程序员设计
        transcribe_language = language

        if verbose:
            print(f"🎙️  转录中: {audio_file}")

        # 调用 Whisper 进行转录
        result = self.model.transcribe(
            audio_file,
            language=transcribe_language,
            initial_prompt=programmer_prompt,
            verbose=False,
            temperature=temperature
        )

        if verbose:
            print(f"✓ 转录完成")

        # 修正程序员术语
        if fix_programmer_terms:
            if verbose:
                print(f"🔧 修正程序员术语")

            result["text"] = self.dict_manager.fix_text(result["text"])

            for segment in result["segments"]:
                segment["text"] = self.dict_manager.fix_text(segment["text"])

        return result

    def get_supported_models(self) -> list:
        """获取支持的模型列表"""
        return ["tiny", "base", "small", "medium", "large"]

    def get_dict_stats(self) -> Dict:
        """获取字典统计信息"""
        return self.dict_manager.get_stats()

    def get_dict_categories(self) -> Dict:
        """获取字典分类统计"""
        return self.dict_manager.list_categories()
