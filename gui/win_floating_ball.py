import sys
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QWidget, QToolTip


class FloatingBall(QWidget):
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
            print("开始录音")
        else:
            self.recording = False
            print("停止录音")
            text = "hello world"
            QApplication.clipboard().setText(text)
            print(f"已复制到剪贴板: {text}")
            pos = self.mapToGlobal(self.rect().center())
            QToolTip.showText(pos, f"已复制: {text}")
        self.update()


def main():
    app = QApplication(sys.argv)
    ball = FloatingBall()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
