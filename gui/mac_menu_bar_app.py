"""
CodeWhisper MenuBar Application - macOS 菜单栏应用（使用 rumps）
"""

import os
import queue
import threading
import tempfile
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import rumps
import sounddevice as sd
import soundfile as sf
import numpy as np

from codewhisper.transcriber import CodeWhisper
from codewhisper.history_manager import HistoryManager


class CodeWhisperApp(rumps.App):
    """CodeWhisper Mac菜单栏应用"""

    def __init__(self):
        self.history_menu_item = rumps.MenuItem("最近记录 (History)")
        super(CodeWhisperApp, self).__init__(
            "🎙️",
            menu=[
                rumps.MenuItem("开始录音", self.start_recording),
                self.history_menu_item,
                None,  # 分隔线
                rumps.MenuItem("快速添加术语", self.quick_add_term),
            ]
        )

        self.is_recording = False
        self.sample_rate = 16000
        self.stream = None
        self.recording_thread = None
        self.history_manager = HistoryManager()
        self._ui_queue: "queue.Queue[str]" = queue.Queue()
        self._ui_timer = rumps.Timer(self._process_ui_queue, 0.3)
        self._ui_timer.start()
        self.transcribe_executor = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="cw-transcribe"
        )

        try:
            print("📦 加载 CodeWhisper 模型...")
            self.whisper = CodeWhisper(model_name="medium") #模型可选择 tiny base small medium large
            print("✅ 模型加载完成")
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            self.whisper = None

        self._refresh_history_menu()

    @rumps.clicked("开始录音")
    def start_recording(self, sender):
        """开始录音"""
        if self.is_recording:
            self.stop_recording(sender)
            return

        if self.recording_thread and self.recording_thread.is_alive():
            print("⚠️ 上一次录音线程正在退出，请稍后再试")
            return

        self.is_recording = True
        sender.title = "停止录音"
        self.title = "🔴"

        # 后台启动线程进行录音
        self.recording_thread = threading.Thread(
            target=self._record_audio,
            name="cw-record"
        )
        self.recording_thread.daemon = True #定义守护线程
        self.recording_thread.start()

    def _record_audio(self):
        """后台线程：录音"""
        audio_buffer = []
        try:
            print("🎙️ 开始录音...")

            def callback(indata, frames, time_info, status):
                if status:
                    print(f"⚠️ 输入流状态: {status}")
                if self.is_recording:
                    audio_buffer.extend(indata[:, 0].copy())

            # 使用回调模式录音，便于及时响应停止信号
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
                blocksize=512,
                callback=callback
            )

            with self.stream:
                while self.is_recording:
                    sd.sleep(20)

            duration = len(audio_buffer) / self.sample_rate if self.sample_rate else 0
            print(f"✓ 录音完成，共 {duration:.2f} 秒")
            print(f"✓ 录音数据点数: {len(audio_buffer)}")
            self.title = "🎙️"

            # 转录音频（在独立线程池中）
            if audio_buffer:
                self.transcribe_executor.submit(
                    self._transcribe_audio,
                    np.array(audio_buffer, dtype="float32")
                )
            else:
                print("⚠️ 未捕获到音频，跳过转录")

        except Exception as e:
            print(f"❌ 录音错误: {e}")
            import traceback
            traceback.print_exc()
            self.title = "❌"
        finally:
            self.stream = None
            self.recording_thread = None
            self.is_recording = False


    def _transcribe_audio(self, audio_array: np.ndarray):
        """转录音频"""
        temp_audio_file = None
        try:
            print("🔄 转录中...")
            self.title = "⏳"

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

            # 写入历史记录并刷新菜单（通过主线程 Timer）
            self.history_manager.add(transcribed_text)
            self._enqueue_history_refresh()
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

    def _enqueue_history_refresh(self) -> None:
        """从后台线程请求 UI 刷新（主线程执行）。"""
        try:
            self._ui_queue.put_nowait("refresh_history")
        except Exception:
            pass

    def _process_ui_queue(self, _timer) -> None:
        """rumps Timer 回调：运行在主线程，安全地更新菜单 UI。"""
        need_refresh = False
        while True:
            try:
                event = self._ui_queue.get_nowait()
            except queue.Empty:
                break
            if event == "refresh_history":
                need_refresh = True

        if need_refresh:
            self._refresh_history_menu()

    def _refresh_history_menu(self) -> None:
        """刷新“最近记录”子菜单内容（主线程调用）。"""
        try:
            # MenuItem 在第一次添加子项前没有 submenu；避免对 None 调 clear()
            if getattr(self.history_menu_item, "_menu", None) is not None:
                self.history_menu_item.clear()

            records = self.history_manager.list()
            if not records:
                self.history_menu_item.add(rumps.MenuItem("（空）"))
                return

            # 最新的放最上面
            for idx, record in enumerate(reversed(records), 1):
                preview = (record.text or "").replace("\n", " ").strip()
                if len(preview) > 20:
                    preview = preview[:20] + "…"
                title = f"{idx}. {preview}"
                item = rumps.MenuItem(title, callback=self._copy_history_item)
                setattr(item, "_cw_full_text", record.text)
                self.history_menu_item.add(item)
        except Exception as e:
            print(f"❌ 刷新历史菜单失败: {e}")

    def _copy_history_item(self, sender) -> None:
        """点击历史记录：复制该条内容到剪贴板。"""
        text = getattr(sender, "_cw_full_text", None)
        if not isinstance(text, str) or not text.strip():
            return
        self._copy_to_clipboard(text)

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
            if self.stream:
                try:
                    self.stream.abort()
                except Exception:
                    try:
                        self.stream.stop()
                    except Exception:
                        pass
            # 直接更新菜单项标题
            sender.title = "开始录音"

    @rumps.clicked("快速添加术语")
    def quick_add_term(self, sender):
        """快速添加术语到字典"""
        # 使用 AppleScript 对话框（更稳定）
        script = '''
        tell application "System Events"
            activate
            set userInput to text returned of (display dialog "格式：错误变体 正确术语\n例如：瑞迪斯 Redis" default answer "" with title "快速添加术语" buttons {"取消", "添加"} default button "添加")
            return userInput
        end tell
        '''
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return  # 用户取消

            text = result.stdout.strip()
            if not text:
                return

            # 用空格分隔
            parts = text.split()
            if len(parts) != 2:
                subprocess.run(['osascript', '-e', 'display notification "请输入：错误变体 正确术语" with title "格式错误"'])
                return

            wrong_variant = parts[0]
            correct_term = parts[1]

            # 保存到字典
            if self._save_term_to_dict(correct_term, wrong_variant):
                # 用 AppleScript 显示通知
                notify_script = f'display notification "重启后生效" with title "添加成功" subtitle "{wrong_variant} → {correct_term}"'
                subprocess.run(['osascript', '-e', notify_script])
            else:
                subprocess.run(['osascript', '-e', 'display notification "保存出错" with title "添加失败"'])

        except Exception as e:
            print(f"❌ 快速添加失败: {e}")

    def _save_term_to_dict(self, correct_term: str, wrong_variant: str) -> bool:
        """保存术语到字典的 other 分类"""
        import json
        from pathlib import Path

        try:
            # 字典文件路径
            project_root = Path(__file__).parent.parent
            dict_path = project_root / "dictionaries" / "programmer_terms.json"

            # 读取字典
            with open(dict_path, 'r', encoding='utf-8') as f:
                dict_data = json.load(f)

            # 获取 other 分类
            other_category = dict_data["categories"].get("other", {})
            terms = other_category.setdefault("terms", {})

            # 检查术语是否已存在
            if correct_term in terms:
                # 已存在，添加变体
                variants = terms[correct_term].setdefault("variants", [])
                # 检查变体是否已存在
                for v in variants:
                    if v.get("wrong") == wrong_variant:
                        print(f"变体已存在: {wrong_variant}")
                        return True
                variants.append({
                    "wrong": wrong_variant,
                    "description": "通过快速添加添加"
                })
            else:
                # 不存在，创建新术语
                terms[correct_term] = {
                    "correct": correct_term,
                    "description": "通过快速添加添加",
                    "variants": [{
                        "wrong": wrong_variant,
                        "description": "通过快速添加添加"
                    }]
                }

            # 保存字典
            with open(dict_path, 'w', encoding='utf-8') as f:
                json.dump(dict_data, f, ensure_ascii=False, indent=2)

            print(f"✅ 已添加术语: {wrong_variant} → {correct_term}")
            return True

        except Exception as e:
            print(f"❌ 保存术语失败: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """主函数"""
    app = CodeWhisperApp()
    print("🚀 应用启动中，请检查菜单栏")
    print("⚠️ 请注意术语字典库是否报错，报错会导致字典加载失败，术语命中失效")

    app.run()


if __name__ == "__main__":
    main()
