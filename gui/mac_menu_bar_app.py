"""
CodeWhisper MenuBar Application - macOS 菜单栏应用（使用 rumps）
"""

import os
import threading
import tempfile
import subprocess

import rumps
import sounddevice as sd
import soundfile as sf
import numpy as np

from codewhisper.transcriber import CodeWhisper


class CodeWhisperApp(rumps.App):
    """CodeWhisper Mac菜单栏应用"""

    def __init__(self):
        super(CodeWhisperApp, self).__init__(
            "🎙️",
            menu=[
                rumps.MenuItem("开始录音", self.start_recording),
            ]
        )

        self.is_recording = False
        self.audio_data = []
        self.sample_rate = 16000
        self.stream = None

        try:
            print("📦 加载 CodeWhisper 模型...")
            self.whisper = CodeWhisper(model_name="medium", use_prompt=True) #模型可选择 tiny base small medium large
            print("✅ 模型加载完成")
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            self.whisper = None

    @rumps.clicked("开始录音")
    def start_recording(self, sender):
        """开始录音"""
        if self.is_recording:
            self.stop_recording(sender)
            return

        self.is_recording = True
        self.audio_data = []
        sender.title = "停止录音"
        self.title = "🔴"

        # 后台启动线程进行录音
        recording_thread = threading.Thread(target=self._record_audio)
        recording_thread.daemon = True #定义守护线程
        recording_thread.start()

    def _record_audio(self):
        """后台线程：录音"""
        try:
            print("🎙️ 开始录音...")

            # 使用 sounddevice 录音 获取麦克风权限 单声道 默认定义采样率
            with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype="float32") as stream:
                while self.is_recording:
                    data, _ = stream.read(1024)
                    self.audio_data.extend(data.flatten().tolist())

            duration = len(self.audio_data) / self.sample_rate
            print(f"✓ 录音完成，共 {duration:.2f} 秒")
            print(f"✓ 录音数据点数: {len(self.audio_data)}")
            self.title = "🎙️"

            # 转录音频
            self._transcribe_audio()

        except Exception as e:
            print(f"❌ 录音错误: {e}")
            import traceback
            traceback.print_exc()
            self.title = "❌"


    def _transcribe_audio(self):
        """转录音频"""
        temp_audio_file = None
        try:
            print("🔄 转录中...")
            self.title = "⏳"

            # 将累积的 Python 列表转为 Whisper 所需要的一维 float32 波形数组
            audio_array = np.array(self.audio_data, dtype="float32")
            print(f"📊 音频数组形状: {audio_array.shape}")

            #创建包装成临时WAV文件，准备喂给Whisper模型
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                temp_audio_file = tmp_file.name
                sf.write(temp_audio_file, audio_array, self.sample_rate)
                print(f"💾 音频已保存到: {temp_audio_file}")

            #兜底保护
            if not self.whisper:
                print("❌ 模型未加载")
                self.title = "❌"
                return

            # 使用 CodeWhisper 转录
            print("🔊（Whisper中文模型）CodeWhisper开始转录...")
            result = self.whisper.transcribe(
                temp_audio_file,
                language="zh",#走中文模型
                fix_programmer_terms=True,
                verbose=True
            )

            transcribed_text = result["text"]
            print(f"✓ 转录完成: {transcribed_text}")

            # 复制到剪切板
            self._copy_to_clipboard(transcribed_text)
            self.title = "✅"

            # 打印字典修正统计信息
            self._print_dict_stats()

        except Exception as e:
            print(f"❌ 转录错误: {e}")
            import traceback
            traceback.print_exc()
            self.title = "❌"

        finally:
            # 清理临时文件
            if temp_audio_file:
                try:
                    if os.path.exists(temp_audio_file):
                        os.remove(temp_audio_file)
                        print(f"🗑️ 已删除临时文件")
                except Exception as e:
                    print(f"删除临时文件失败: {e}")

    def _copy_to_clipboard(self, text):
        """复制文本到剪切板"""
        try:
            #创建调用剪切板进程，通过管道和python连接
            process = subprocess.Popen(
                ["pbcopy"],
                stdin=subprocess.PIPE,
                text=True
            )
            process.communicate(text)
            print(f"📋 已复制到剪切板: {text[:50]}...")
        except Exception as e:
            print(f"❌ 复制到剪切板失败: {e}")

    def _print_dict_stats(self):
        """打印字典修正的统计信息"""
        try:
            stats = self.whisper.get_dict_stats()
            corrections = self.whisper.dict_manager.get_corrections()

            print(f"\n📊 字典修正统计信息:")
            print(f"  📚 总规则数: {stats['total_rules']}")
            print(f"  🔧 修正次数: {stats['replacements_made']}")

            if corrections:
                print(f"\n✏️ 修正详情:")
                for i, correction in enumerate(corrections, 1):
                    print(f"  {i}. {correction['wrong']} → {correction['correct']} ({correction['category']})")
            else:
                print(f"  (无修正)")

        except Exception as e:
            print(f"❌ 打印统计信息失败: {e}")

    def stop_recording(self, sender):
        """停止录音"""
        if self.is_recording:
            self.is_recording = False
            # 直接更新菜单项标题
            sender.title = "开始录音"


def main():
    """主函数"""
    app = CodeWhisperApp()
    print("🚀 应用启动中，请检查菜单栏")
    print("⚠️ 请注意术语字典库是否报错，报错会导致字典加载失败，术语命中失效")

    app.run()


if __name__ == "__main__":
    main()
