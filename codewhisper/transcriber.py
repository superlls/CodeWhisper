"""
转录引擎 - 基于 OpenAI Whisper 的转录核心
"""

import whisper
import torch
from typing import Dict, Optional
from .dict_manager import DictionaryManager
from .prompt_engine import PromptEngine
from .utils import convert_to_simplified_chinese


class CodeWhisper:
    """主转录引擎"""

    def __init__(self, model_name: str = "medium", dict_path: Optional[str] = None):
        """
         CodeWhisper 初始化，同时预加载字典的特定术语并将其构建为提示词喂给Whisper进行预热；模型默认medium
        Args:
            model_name: Whisper 模型 (tiny, base, small, medium, large)
            dict_path: 自定义字典路径，支持后续拓展todo
        """
        print(f"📦 加载 Whisper 模型: {model_name}")

        # 显式设定设备与精度：优先使用 NVIDIA CUDA，其次回退 CPU
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"  设备选择: device={device},如您使用CUDA报 `CUBLAS_STATUS_ALLOC_FAILED` ，请改用更小模型（base/small）")

        # openai-whisper 会在 CUDA 上自动使用 fp16，在 CPU 上用 fp32
        self.model = whisper.load_model(model_name, device=device)
        self.model_name = model_name

        print(f"📚 加载字典管理器")
        self.dict_manager = DictionaryManager(dict_path)

        print(f"🚀 加载智能提示词引擎")
        self.prompt_engine = PromptEngine()

        # 使用新的 PromptEngine 构建提示词
        self.programmer_prompt = self.prompt_engine.build_prompt()
        print(f"💡 当前提示词 {self.programmer_prompt}")

        print(f"✅CodeWhisper 初始化完成\n")

    def transcribe(
        self,
        audio_file: str,
        language: Optional[str] = "zh",
        fix_programmer_terms: bool = True,
        verbose: bool = True,
        temperature: float = 0.0,
    ) -> Dict:
        """
        转录音频文件

        Args:
            audio_file: 音频文件路径
            language: 语言代码 (默认zh中文模型)
            fix_programmer_terms: 是否修正程序员术语默认为True
            verbose: 是否打印详细信息 默认为True (打印输出状态、提示词加载、繁简转换、术语修正等步骤)
            temperature: 控制模型的“随机性”，范围通常在0—1。默认为0，数值越高，输出越有随机性（不推荐用于语音转录）


        Returns:
            包含转录结果的字典
        """
        if verbose:
            print(f"🎙️ 转录中 {audio_file} (语言: {language})")

        # 调用 Whisper 进行转录（使用初始化时缓存的提示词）
        # 注意：这里verbose=False 是指 OpenAI 的Whisper 自身的调试日志（解码进度等）
        # 而用户的 verbose 参数控制的是 CodeWhisper 的进度日志（上面的if verbose）
        result = self.model.transcribe(
            audio_file,
            language=language,
            initial_prompt=self.programmer_prompt,
            verbose=False,  # Whisper 内部日志关闭，由 CodeWhisper 的verbose 控制外部日志
            temperature=temperature
        )

        if verbose:
            print(f"✅转录完成")

        # 将繁体转换为简体
        if verbose:
            print(f"🧹 转换繁体为简体")

        result["text"] = convert_to_simplified_chinese(result["text"])
        for segment in result["segments"]:
            segment["text"] = convert_to_simplified_chinese(segment["text"])

        # 替换术语
        if fix_programmer_terms:
            if verbose:
                print(f"🛠 修正为开发者术语")

            # 只修正正文文本一次，避免重复修正
            result["text"] = self.dict_manager.fix_text(result["text"], accumulate=False)

        # 学习用户习惯：检测文本中出现的术语并更新用户术语库
        if verbose:
            print(f"🧠 学习用户习惯")

        # 方法1：从修正记录中获取术语（优先，更精准）
        detected_terms = self.dict_manager.get_detected_terms_from_corrections()

        # 方法2：从最终文本中检测术语（补充）
        detected_terms_from_text = self.dict_manager.detect_terms_in_text(result["text"])
        detected_terms.update(detected_terms_from_text)

        if detected_terms:
            if verbose:
                print(f"  检测到术语: {', '.join(list(detected_terms)[:5])}{'...' if len(detected_terms) > 5 else ''}")
            # 更新用户术语库
            self.prompt_engine.update_user_terms(detected_terms)

            # 重新构建提示词（下次转录使用）
            self.programmer_prompt = self.prompt_engine.build_prompt()

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

    def get_prompt_stats(self) -> Dict:
        """获取提示词引擎统计信息"""
        return self.prompt_engine.get_stats()
