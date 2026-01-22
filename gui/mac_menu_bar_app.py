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
from codewhisper.console import preview_text


class CodeWhisperApp(rumps.App):
    """CodeWhisper Mac菜单栏应用"""

    def __init__(self):
        self.history_menu_item = rumps.MenuItem("最近记录 (History)")
        self.record_menu_item = rumps.MenuItem("开始录音", self.start_recording)
        self.transcribe_mode_menu = rumps.MenuItem("转录模式")
        self.mode_fast_item = rumps.MenuItem("极速模式（边录边转）", callback=self.set_mode_fast)
        self.mode_full_item = rumps.MenuItem("全量模式（录完再转，带标点）", callback=self.set_mode_full)
        self.transcribe_mode_menu.add(self.mode_fast_item)
        self.transcribe_mode_menu.add(self.mode_full_item)

        super(CodeWhisperApp, self).__init__(
            "🎙️",
            menu=[
                self.record_menu_item,
                self.transcribe_mode_menu,
                self.history_menu_item,
                None,  # 分隔线
                rumps.MenuItem("清除历史记录", self.clear_history),
                rumps.MenuItem("快速添加术语", self.quick_add_term),
            ]
        )

        self.is_recording = False
        self.sample_rate = 16000
        self.stream = None
        self.recording_thread = None
        self.history_manager = HistoryManager()
        # rumps/Cocoa 的 UI 更新需要在主线程执行；后台线程通过 queue 投递事件。
        self._ui_queue: "queue.Queue[object]" = queue.Queue()
        # 既用于刷新历史菜单，也用于从非主线程（例如全局热键监听）安全触发录音开始/停止。
        self._ui_timer = rumps.Timer(self._process_ui_queue, 0.05)
        self._ui_timer.start()
        self.transcribe_executor = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="cw-transcribe"
        )
        self._hotkey_pressed = False
        self._recording_seq = 0
        self._chunk_text_lock = threading.Lock()
        self._chunk_texts = {}
        self.transcribe_mode = self._load_gui_config().get("transcribe_mode", "fast")
        self._refresh_mode_menu_state()

        try:
            print("📦 加载 CodeWhisper 模型...")
            self.whisper = CodeWhisper(model_name="medium") #模型可选择 tiny base small medium large
            print("✅ 模型加载完成")
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            self.whisper = None

        self._refresh_history_menu()
        self._start_hold_to_record_hotkey()

    def _gui_config_path(self):
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        return project_root / "config" / "gui_config.json"

    def _load_gui_config(self) -> dict:
        import json
        path = self._gui_config_path()
        try:
            if not path.exists():
                return {}
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _save_gui_config(self, data: dict) -> None:
        import json
        path = self._gui_config_path()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _refresh_mode_menu_state(self) -> None:
        # rumps 用 state=1 显示勾选
        self.mode_fast_item.state = 1 if self.transcribe_mode == "fast" else 0
        self.mode_full_item.state = 1 if self.transcribe_mode == "full" else 0

    def _set_transcribe_mode(self, mode: str) -> None:
        if self.is_recording:
            try:
                subprocess.run(
                    ["osascript", "-e", 'display notification "请先停止录音再切换转录模式" with title "CodeWhisper"'],
                    capture_output=True,
                    text=True,
                )
            except Exception:
                pass
            return

        if mode not in {"fast", "full"}:
            return
        self.transcribe_mode = mode
        self._refresh_mode_menu_state()
        cfg = self._load_gui_config()
        cfg["transcribe_mode"] = mode
        self._save_gui_config(cfg)

    def set_mode_fast(self, _sender) -> None:
        self._set_transcribe_mode("fast")

    def set_mode_full(self, _sender) -> None:
        self._set_transcribe_mode("full")

    def start_recording(self, sender):
        """开始录音"""
        if self.is_recording:
            self.stop_recording(sender)
            return

        if self.recording_thread and self.recording_thread.is_alive():
            print("⚠️ 上一次录音线程正在退出，请稍后再试")
            return

        # 每次录音递增 session id，用于丢弃过期的后台转录任务
        self._recording_seq += 1
        with self._chunk_text_lock:
            self._chunk_texts = {}

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
        buffer_lock = threading.Lock()
        recording_seq = self._recording_seq
        try:
            print("🎙️ 开始录音...")

            def callback(indata, frames, time_info, status):
                if status:
                    print(f"⚠️ 输入流状态: {status}")
                if self.is_recording:
                    # callback 在音频线程里运行，避免与分块调度/切片并发冲突
                    with buffer_lock:
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
                next_chunk_start = 0
                chunk_index = 0

                # 极速模式：边录边分块转录，减少录音结束后的等待
                if self.transcribe_mode == "fast":
                    chunk_seconds = float(os.environ.get("CODEWHISPER_CHUNK_SECONDS", "10"))
                    min_final_seconds = float(os.environ.get("CODEWHISPER_MIN_FINAL_SECONDS", "1.5"))
                    chunk_samples = max(1, int(self.sample_rate * chunk_seconds))
                    min_final_samples = max(1, int(self.sample_rate * min_final_seconds))
                else:
                    # 全量模式：录完再统一转录
                    chunk_samples = None
                    min_final_samples = None

                while self.is_recording:
                    sd.sleep(20)
                    if self.transcribe_mode == "fast":
                        # 录音进行中：只要累计超过一个 chunk，就切一段出来异步转录
                        while True:
                            with buffer_lock:
                                available = len(audio_buffer) - next_chunk_start
                                if available < chunk_samples:
                                    break
                                chunk = np.array(
                                    audio_buffer[next_chunk_start: next_chunk_start + chunk_samples],
                                    dtype="float32",
                                )
                                next_chunk_start += chunk_samples

                            self.transcribe_executor.submit(
                                self._transcribe_chunk_store,
                                recording_seq,
                                chunk_index,
                                chunk,
                            )
                            chunk_index += 1

            if self.transcribe_mode == "fast":
                # 录音停止后，把剩余未处理的尾巴也丢去转录；太短则不转，避免浪费开销
                with buffer_lock:
                    tail = np.array(audio_buffer[next_chunk_start:], dtype="float32")

                if len(tail) >= min_final_samples:
                    self.transcribe_executor.submit(
                        self._transcribe_chunk_store,
                        recording_seq,
                        chunk_index,
                        tail,
                    )
                    chunk_index += 1

            duration = len(audio_buffer) / self.sample_rate if self.sample_rate else 0
            print(f"✓ 录音完成，共 {duration:.2f} 秒")
            print(f"✓ 录音数据点数: {len(audio_buffer)}")
            self._enqueue_set_title("⏳")

            if not audio_buffer:
                print("⚠️ 未捕获到音频，跳过转录")
                self._enqueue_set_title("🎙️")
                return

            if self.transcribe_mode == "fast":
                # 最终拼接/复制/写历史：排在 executor 队列尾部，确保先跑完所有分块
                self.transcribe_executor.submit(self._finalize_chunked_transcription, recording_seq)
            else:
                # 全量模式：一次性转录整段，标点/上下文更好
                self.transcribe_executor.submit(
                    self._transcribe_audio,
                    np.array(audio_buffer, dtype="float32"),
                )

        except Exception as e:
            print(f"❌ 录音错误: {e}")
            import traceback
            traceback.print_exc()
            self._enqueue_set_title("❌")
        finally:
            self.stream = None
            self.recording_thread = None
            self.is_recording = False


    def _transcribe_chunk_store(self, recording_seq: int, chunk_index: int, audio_array: np.ndarray) -> None:
        """
        转录一个音频分块并存入累计结果（不更新 UI/剪贴板/历史；用于“边录边转录”）。

        用 chunk_index 保证最终拼接顺序稳定，也避免“只剩最后一段”的问题。
        """
        # 录音 session 已切换，丢弃旧任务
        if recording_seq != self._recording_seq:
            return
        if audio_array is None or audio_array.size == 0:
            return
        if not self.whisper:
            return

        temp_audio_file = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                temp_audio_file = tmp_file.name
                sf.write(temp_audio_file, audio_array, self.sample_rate)

            result = self.whisper.transcribe(
                temp_audio_file,
                language="zh",
                fix_programmer_terms=True,
                verbose=False,
                # 分块转录时关闭 initial_prompt，能明显减少“提示词术语列表”幻觉
                use_initial_prompt=False,
                # 分块转录不做用户术语学习，避免频繁写盘/扰动 prompt
                learn_user_terms=False,
                # 分块更容易遇到静音/半句，适当提高静音阈值减少幻觉
                silence_rms_threshold=0.0035,
                silence_peak_threshold=0.03,
            )
            text = (result.get("text") or "").strip()
            if not text:
                return

            with self._chunk_text_lock:
                # executor 默认单线程，但这里仍用锁以防未来调整并发
                self._chunk_texts[int(chunk_index)] = text
        except Exception as e:
            print(f"❌ 分块转录失败: {e}")
        finally:
            if temp_audio_file:
                try:
                    if os.path.exists(temp_audio_file):
                        os.remove(temp_audio_file)
                except Exception:
                    pass


    def _finalize_chunked_transcription(self, recording_seq: int) -> None:
        """录音结束后：取累计文本，复制到剪贴板并写入历史。"""
        if recording_seq != self._recording_seq:
            return

        try:
            with self._chunk_text_lock:
                texts = [self._chunk_texts[k] for k in sorted(self._chunk_texts.keys())]
                final_text = "".join([t for t in texts if isinstance(t, str)]).strip()

            if not final_text:
                print("⚠️ 最终文本为空，跳过复制/写入历史")
                self._enqueue_set_title("🎙️")
                return

            print(f'📝 最终转录预览: "{preview_text(final_text, 120)}"')
            self._copy_to_clipboard(final_text)
            self.history_manager.add(final_text)
            self._enqueue_history_refresh()
            self._enqueue_set_title("✅")
            self._print_dict_stats()
        except Exception as e:
            print(f"❌ 最终收尾失败: {e}")
            self._enqueue_set_title("❌")


    def _transcribe_audio(self, audio_array: np.ndarray):
        """转录音频"""
        temp_audio_file = None
        try:
            print("🔄 转录中...")
            self._enqueue_set_title("⏳")

            print(f"📊 音频数组形状: {audio_array.shape}")

            #创建包装成临时WAV文件，准备喂给Whisper模型
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                temp_audio_file = tmp_file.name
                sf.write(temp_audio_file, audio_array, self.sample_rate)
                print(f"💾 音频已保存到: {temp_audio_file}")

            #兜底保护
            if not self.whisper:
                print("❌ 模型未加载")
                self._enqueue_set_title("❌")
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
            self._enqueue_set_title("✅")

            # 打印字典修正统计信息
            self._print_dict_stats()

        except Exception as e:
            print(f"❌ 转录错误: {e}")
            import traceback
            traceback.print_exc()
            self._enqueue_set_title("❌")

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

    def _enqueue_set_title(self, title: str) -> None:
        """从后台线程请求更新菜单栏图标（主线程执行）。"""
        try:
            self._ui_queue.put_nowait(("set_title", title))
        except Exception:
            pass

    def _process_ui_queue(self, _timer) -> None:
        """rumps Timer 回调：运行在主线程，安全地更新菜单 UI。"""
        need_refresh = False
        need_start = False
        need_stop = False
        need_toggle = False
        need_hotkey_warn = False
        pending_title: Optional[str] = None
        while True:
            try:
                event = self._ui_queue.get_nowait()
            except queue.Empty:
                break
            if isinstance(event, tuple) and len(event) == 2 and event[0] == "set_title":
                pending_title = str(event[1])
                continue
            if event == "refresh_history":
                need_refresh = True
            elif event == "start_recording":
                need_start = True
            elif event == "stop_recording":
                need_stop = True
            elif event == "toggle_recording":
                need_toggle = True
            elif event == "hotkey_permission_warning":
                need_hotkey_warn = True

        if pending_title is not None:
            self.title = pending_title
        if need_toggle:
            if self.is_recording:
                self.stop_recording(self.record_menu_item)
            else:
                self.start_recording(self.record_menu_item)
        if need_start:
            # 避免“按住”重复触发导致录音被 toggle 掉
            if not self.is_recording:
                self.start_recording(self.record_menu_item)
        if need_stop:
            if self.is_recording:
                self.stop_recording(self.record_menu_item)
        if need_hotkey_warn:
            try:
                subprocess.run(
                    ["osascript", "-e", 'display notification "请在 系统设置 → 隐私与安全性 → 辅助功能 中允许本应用，否则 Command+M 热键无法工作" with title "CodeWhisper"'],
                    capture_output=True,
                    text=True,
                )
            except Exception:
                pass
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

    def clear_history(self, _sender):
        """清除本地历史记录（带确认）。"""
        try:
            response = rumps.alert(
                title="清除历史记录",
                message="确定要清除所有历史记录吗？此操作不可撤销。",
                ok="清除",
                cancel="取消",
            )
            if response != 1:
                return

            self.history_manager.clear()
            self._refresh_history_menu()
            subprocess.run(
                ["osascript", "-e", 'display notification "已清除历史记录" with title "CodeWhisper"'],
                capture_output=True,
                text=True,
            )
        except Exception as e:
            print(f"❌ 清除历史记录失败: {e}")

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
        # 允许重复调用：无论当前状态如何，都尽量把 UI 恢复到“开始录音”
        # 避免跨线程强行 abort/stop PortAudio（在 macOS 上偶发不稳定/崩溃）；
        # callback 录音模式下，设置标志位后录音线程会很快自行退出并关闭 stream。
        self.is_recording = False
        sender.title = "开始录音"

    def _start_hold_to_record_hotkey(self) -> None:
        """
        启动 macOS 全局热键监听：Command+M 单击切换录音（开始/停止并转录）。

        依赖 PyObjC（rumps 在 macOS 上通常已带上）。若未授权“辅助功能”，事件监听将不可用。
        """
        try:
            import Quartz
        except Exception as e:
            print(f"⚠️ 全局热键不可用（Quartz 导入失败）: {e}")
            return

        # M 键硬件 keycode；大多数 ANSI 键盘为 46。若用户使用非标准布局，可后续做可配置化。
        keycode_m = 46

        # 先做一次可用性提示；尽量触发系统授权提示（不保证一定弹出）
        try:
            if hasattr(Quartz, "AXIsProcessTrustedWithOptions"):
                # 在 PyObjC 里该 key 有时是常量，有时使用字符串；两者都尝试。
                try:
                    is_trusted = bool(Quartz.AXIsProcessTrustedWithOptions({Quartz.kAXTrustedCheckOptionPrompt: True}))
                except Exception:
                    is_trusted = bool(Quartz.AXIsProcessTrustedWithOptions({"AXTrustedCheckOptionPrompt": True}))
            else:
                is_trusted = bool(getattr(Quartz, "AXIsProcessTrusted", lambda: True)())
            if not is_trusted:
                print("⚠️ 未授予“辅助功能”权限：Command+M 全局热键可能无法工作。")
                print("   请在 系统设置 -> 隐私与安全性 -> 辅助功能 中允许本应用。")
                try:
                    self._ui_queue.put_nowait("hotkey_permission_warning")
                except Exception:
                    pass
        except Exception:
            pass

        def _enqueue(event: str) -> None:
            try:
                self._ui_queue.put_nowait(event)
            except Exception:
                pass

        def _tap_callback(_proxy, _type, event, _refcon):
            try:
                event_type = Quartz.CGEventGetType(event)
                if event_type not in (Quartz.kCGEventKeyDown, Quartz.kCGEventKeyUp):
                    return event

                keycode = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
                if keycode != keycode_m:
                    return event

                if event_type == Quartz.kCGEventKeyDown:
                    flags = Quartz.CGEventGetFlags(event)
                    has_cmd = bool(flags & Quartz.kCGEventFlagMaskCommand)
                    if not has_cmd:
                        return event
                    # 按住时系统会重复触发 keyDown；只在首次按下时触发一次“切换”
                    if not self._hotkey_pressed:
                        self._hotkey_pressed = True
                        _enqueue("toggle_recording")
                else:  # kCGEventKeyUp
                    # 仅用于“抬起”复位，防止按住时重复触发
                    if self._hotkey_pressed:
                        self._hotkey_pressed = False
            except Exception:
                # 监听器异常不影响主程序
                pass
            return event

        def _run_event_tap() -> None:
            try:
                mask = (
                    (1 << Quartz.kCGEventKeyDown) |
                    (1 << Quartz.kCGEventKeyUp)
                )
                tap = Quartz.CGEventTapCreate(
                    Quartz.kCGSessionEventTap,
                    Quartz.kCGHeadInsertEventTap,
                    Quartz.kCGEventTapOptionListenOnly,
                    mask,
                    _tap_callback,
                    None,
                )
                if not tap:
                    print("⚠️ 全局热键监听启动失败：可能缺少“辅助功能”权限。")
                    return

                run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
                run_loop = Quartz.CFRunLoopGetCurrent()
                Quartz.CFRunLoopAddSource(run_loop, run_loop_source, Quartz.kCFRunLoopCommonModes)
                Quartz.CGEventTapEnable(tap, True)

                print("⌨️ 已启用全局热键：Command+M 开始录音，再按一次停止并转录")
                Quartz.CFRunLoopRun()
            except Exception as e:
                print(f"⚠️ 全局热键监听线程异常退出: {e}")

        t = threading.Thread(target=_run_event_tap, name="cw-hotkey", daemon=True)
        t.start()

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
