import sys
import threading
import tempfile
import numpy as np
import sounddevice as sd
import soundfile as sf
from PySide6.QtCore import Qt, QPoint, Signal, Slot
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QWidget, QToolTip
from codewhisper.transcriber import CodeWhisper


class FloatingBall(QWidget):
    textReady = Signal(str)
    def __init__(self, diameter: int = 80):
        super().__init__()
        self.diameter = diameter
        self.setFixedSize(self.diameter, self.diameter)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Window
        )
        self.setWindowOpacity(1.0)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self._dragging = False
        self._press_pos = QPoint(0, 0)
        self._press_global = QPoint(0, 0)
        self._moved = False
        self.recording = False
        self.audio_data = []
        self.sample_rate = 16000
        self.stream = None
        try:
            self.whisper = CodeWhisper(model_name="medium")
        except Exception as e:
            print(f"模型加载失败: {e}")
            self.whisper = None

        self.textReady.connect(self._copy_to_clipboard)

        screen = QApplication.primaryScreen().availableGeometry()
        center = screen.center()
        x = center.x() - self.width() // 2
        y = center.y() - self.height() // 2
        # 防止多屏环境下越界，简单夹取边界
        x = max(screen.left() + 10, min(x, screen.right() - self.width() - 10))
        y = max(screen.top() + 10, min(y, screen.bottom() - self.height() - 10))
        self.move(x, y)

        print(f"悬浮球已启动，位置: ({x}, {y})，尺寸: {self.width()}x{self.height()}")
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        color = QColor(220, 20, 60, 180) if self.recording else QColor(0, 122, 204, 160)
        painter.setBrush(color)
        painter.drawEllipse(0, 0, self.diameter, self.diameter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._moved = False
            self._press_pos = event.position().toPoint()
            self._press_global = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._dragging:
            delta = event.globalPosition().toPoint() - self._press_global
            if delta.manhattanLength() > 2:
                self._moved = True
            self.move(self.pos() + delta)
            self._press_global = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            was_dragging = self._dragging
            self._dragging = False
            if was_dragging and not self._moved:
                self._toggle_recording()

    def _toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.audio_data = []
            print("开始录音")
            t = threading.Thread(target=self._record_audio, daemon=True)
            t.start()
        else:
            self.recording = False
            print("停止录音")
        self.update()

    def _record_audio(self):
        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype="float32") as s:
                self.stream = s
                while self.recording:
                    data, _ = s.read(1024)
                    self.audio_data.extend(data.flatten().tolist())
            duration = len(self.audio_data) / self.sample_rate if self.sample_rate else 0
            print(f"录音完成: {duration:.2f}s")
            self._transcribe_audio()
        except Exception as e:
            print(f"录音错误: {e}")

    def _transcribe_audio(self):
        temp_audio_file = None
        try:
            audio_array = np.array(self.audio_data, dtype="float32")
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                temp_audio_file = tmp.name
                sf.write(temp_audio_file, audio_array, self.sample_rate)
            if not self.whisper:
                print("模型未加载")
                return
            print("转录中")
            result = self.whisper.transcribe(
                temp_audio_file,
                language="zh",
                fix_programmer_terms=True,
                verbose=True
            )
            text = result.get("text", "")
            print(f"转录完成: {text[:80]}")
            self.textReady.emit(text)
            try:
                stats = self.whisper.get_dict_stats()
                corrections = self.whisper.dict_manager.get_corrections()
                print(f"字典总规则: {stats.get('total_rules')}, 本次修正: {stats.get('replacements_made')}")
                if corrections:
                    for i, c in enumerate(corrections[:5], 1):
                        print(f"修正{i}: {c['wrong']} -> {c['correct']} ({c['category']})")
            except Exception as e:
                print(f"统计错误: {e}")
        except Exception as e:
            print(f"转录错误: {e}")
        finally:
            if temp_audio_file:
                try:
                    import os
                    if os.path.exists(temp_audio_file):
                        os.remove(temp_audio_file)
                except Exception as e:
                    print(f"清理失败: {e}")

    @Slot(str)
    def _copy_to_clipboard(self, text: str):
        try:
            QApplication.clipboard().setText(text)
            print(f"已复制到剪贴板: {text[:80]}")
            pos = self.mapToGlobal(self.rect().center())
            QToolTip.showText(pos, "已复制转写结果")
        except Exception as e:
            print(f"剪贴板错误: {e}")


def main():
    app = QApplication(sys.argv)
    ball = FloatingBall()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
