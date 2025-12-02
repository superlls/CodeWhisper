"""
CodeWhisper MenuBar Application - macOS 菜单栏应用（使用 rumps）
"""

import os
import threading
import tempfile
from pathlib import Path
import subprocess

import rumps
import sounddevice as sd
import soundfile as sf
import numpy as np

from codewhisper.transcriber import CodeWhisper


class CodeWhisperApp(rumps.App):
    """CodeWhisper 菜单栏应用"""

    def __init__(self):
        super(CodeWhisperApp, self).__init__(
            "🎙️",
            menu=[
                rumps.MenuItem("开始录音", self.start_recording),
                None,  # 分隔线
                rumps.MenuItem("退出", self.quit_app),
            ]
        )

        self.is_recording = False
        self.audio_data = []
        self.sample_rate = 16000
        self.stream = None

        try:
            print("📦 加载 CodeWhisper 模型...")
            self.whisper = CodeWhisper(model_name="small") #模型选择
            print("✓ 模型加载完成")
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            self.whisper = None

    @rumps.clicked("开始录音")
    def start_recording(self, sender):
        """开始录音"""
        if self.is_recording:
            self.stop_recording()
            return

        self.is_recording = True
        self.audio_data = []
        sender.title = "停止录音"
        self.title = "🔴"

        # 在后台线程中进行录音
        recording_thread = threading.Thread(target=self._record_audio)
        recording_thread.daemon = True
        recording_thread.start()

    def _record_audio(self):
        """后台线程：录音"""
        try:
            print("🎙️ 开始录音...")

            # 使用 sounddevice 录音
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

    def stop_recording(self):
        """停止录音"""
        if self.is_recording:
            self.is_recording = False
            # 更新菜单项标题
            for item in self.menu:
                if item and hasattr(item, 'title') and item.title == "停止录音":
                    item.title = "开始录音"

    def _transcribe_audio(self):
        """转录音频"""
        temp_audio_file = None
        try:
            print("🔄 转录中...")
            self.title = "⏳"

            # 保存音频文件
            audio_array = np.array(self.audio_data, dtype="float32")
            print(f"📊 音频数组形状: {audio_array.shape}")

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                temp_audio_file = tmp_file.name
                sf.write(temp_audio_file, audio_array, self.sample_rate)
                print(f"💾 音频已保存到: {temp_audio_file}")

            if not self.whisper:
                print("❌ 模型未加载")
                self.title = "❌"
                return

            # 使用 CodeWhisper 转录
            print("🔊 开始转录（中文模式）...")
            result = self.whisper.transcribe(
                temp_audio_file,
                language="zh",
                fix_programmer_terms=True,
                verbose=True  # 改成 True 看看 Whisper 的详细输出
            )

            transcribed_text = result["text"]
            print(f"✓ 转录完成: {transcribed_text}")

            # 复制到剪切板
            self._copy_to_clipboard(transcribed_text)
            self.title = "✅"

            # 显示系统通知
            self._show_notification("转录完成", transcribed_text)

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
            process = subprocess.Popen(
                ["pbcopy"],
                stdin=subprocess.PIPE,
                text=True
            )
            process.communicate(text)
            print(f"📋 已复制到剪切板: {text[:50]}...")
        except Exception as e:
            print(f"❌ 复制到剪切板失败: {e}")

    def _show_notification(self, title, message):
        """显示 macOS 系统通知"""
        try:
            script = f'display notification "{message[:100]}" with title "{title}"'
            subprocess.run(
                ["osascript", "-e", script],
                check=False
            )
        except Exception as e:
            print(f"通知显示失败: {e}")

    def quit_app(self, sender):
        """退出应用"""
        rumps.quit_app()


def main():
    """主函数"""
    app = CodeWhisperApp()
    print("🚀 应用启动中，请检查菜单栏...")
    app.run()


if __name__ == "__main__":
    main()
