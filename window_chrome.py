"""Flipmelon window chrome: self-contained PySide6 title bar + resize grips.

Only PySide6 is used for the window frame. The existing RLottie fullscreen
overlay and scrcpy window are unchanged.
"""
from __future__ import annotations

from pathlib import Path
from PySide6.QtCore import Qt, QPoint, QRect, QRectF
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget, QComboBox
from i18n import LANGUAGES, tr, language

CHROME_HEIGHT = 48
GRIP_WIDTH = 7
CORNER_WIDTH = 12


def resized_geometry(original: QRect, delta: QPoint, edges, min_width: int, min_height: int) -> QRect:
    """Compute a manual-resize fallback when the window manager declines.

    Kept separate from any GUI state so dragging logic is testable.
    """
    left, top = original.x(), original.y()
    right = left + original.width()
    bottom = top + original.height()
    if edges & Qt.Edge.LeftEdge:
        left = min(left + delta.x(), right - min_width)
    if edges & Qt.Edge.RightEdge:
        right = max(right + delta.x(), left + min_width)
    if edges & Qt.Edge.TopEdge:
        top = min(top + delta.y(), bottom - min_height)
    if edges & Qt.Edge.BottomEdge:
        bottom = max(bottom + delta.y(), top + min_height)
    return QRect(left, top, right - left, bottom - top)


class WindowControl(QPushButton):
    """Paint title-bar controls consistently across Windows theme versions."""
    def __init__(self, action: str, host: QWidget, parent=None):
        super().__init__(parent)
        self.action = action
        self.host = host
        self.setObjectName('windowControl_' + action)
        self.setFixedSize(42, 33)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setToolTip(tr({'minimize': 'Minimizar', 'maximize': 'Maximizar ou restaurar',
                            'close': 'Fechar Flipmelon'}[action]))
        self.setAccessibleName(self.toolTip())
        if action == 'minimize':
            self.clicked.connect(host.showMinimized)
        elif action == 'maximize':
            self.clicked.connect(self.toggle_maximize)
        else:
            self.clicked.connect(host.close)

    def toggle_maximize(self):
        self.host.showNormal() if self.host.isMaximized() else self.host.showMaximized()
        self.update()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.update()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        hovered = self.underMouse()
        if self.action == 'close' and (hovered or self.isDown()):
            bg = '#C93243' if not self.isDown() else '#9E2535'
        elif self.isDown():
            bg = '#353539'
        elif hovered:
            bg = '#29292D'
        else:
            bg = '#18181B'
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(bg))
        p.drawRoundedRect(QRectF(0.5, 0.5, self.width()-1, self.height()-1), 16, 16)
        ink = '#FFFFFF' if self.action == 'close' and hovered else '#D3D3D8'
        p.setPen(QPen(QColor(ink), 1.6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                      Qt.PenJoinStyle.RoundJoin))
        cx = self.width() / 2
        cy = self.height() / 2
        if self.action == 'minimize':
            p.drawLine(round(cx-6), round(cy+3), round(cx+6), round(cy+3))
        elif self.action == 'close':
            p.drawLine(round(cx-5), round(cy-5), round(cx+5), round(cy+5))
            p.drawLine(round(cx+5), round(cy-5), round(cx-5), round(cy+5))
        elif self.host.isMaximized():
            p.drawRect(QRectF(cx-3, cy-6, 9, 9))
            p.drawLine(round(cx-6), round(cy-3), round(cx-3), round(cy-3))
            p.drawLine(round(cx-6), round(cy-3), round(cx-6), round(cy+6))
            p.drawLine(round(cx-6), round(cy+6), round(cx+3), round(cy+6))
        else:
            p.drawRect(QRectF(cx-5, cy-5, 10, 10))
        if self.hasFocus():
            p.setPen(QPen(QColor('#DBFF00'), 1))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(QRectF(2.5, 2.5, self.width()-5, self.height()-5), 13, 13)
        p.end()


class FlipmelonTitleBar(QFrame):
    """48 px branded draggable title bar, used only on the main app window."""
    def __init__(self, host: QWidget, icon_path: Path, parent=None):
        super().__init__(parent)
        self.host = host
        self._drag_offset = None
        self.setObjectName('flipTitleBar')
        self.setFixedHeight(CHROME_HEIGHT)
        self.setMouseTracking(True)
        self.setStyleSheet('QFrame#flipTitleBar { background:#121214; '
                           'border-bottom: 1px solid #2C2C30; }')
        bar = QHBoxLayout(self)
        bar.setContentsMargins(19, 0, 11, 0)
        bar.setSpacing(10)
        icon = QLabel(self)
        pix = QPixmap(str(icon_path))
        if not pix.isNull():
            icon.setPixmap(pix.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation))
        icon.setFixedSize(25, 25)
        icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        bar.addWidget(icon)
        name = QLabel('Flipmelon', self)
        name.setStyleSheet('color:#F8F8F9; font-size:14px; font-weight:700;')
        name.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        bar.addWidget(name)
        self.subtitle = QLabel('  /  ' + tr('Sua estação Android'), self)
        self.subtitle.setStyleSheet('color:#77777F; font-size:12px;')
        self.subtitle.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        bar.addWidget(self.subtitle)
        bar.addStretch(1)
        self.language_combo = QComboBox(self)
        self.language_combo.setObjectName('languagePicker')
        self.language_combo.setFixedSize(125, 30)
        self.language_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.language_combo.setToolTip(tr('Idioma'))
        self.language_combo.setAccessibleName(tr('Idioma'))
        self.language_combo.setStyleSheet(
            'QComboBox#languagePicker { background:#1F1F23; color:#F7F7F8; '
            'border:1px solid #38383C; border-radius:10px; padding:3px 9px; '
            'font-size:12px; } '
            'QComboBox#languagePicker QAbstractItemView { background:#202023; '
            'color:#F7F7F8; selection-background-color:#3A3A3E; }')
        for code, title in LANGUAGES:
            self.language_combo.addItem(title, code)
        self.language_combo.currentIndexChanged.connect(self._language_selected)
        bar.addWidget(self.language_combo)
        bar.addSpacing(9)
        self.minimize = WindowControl('minimize', host, self)
        self.maximize = WindowControl('maximize', host, self)
        self.close_control = WindowControl('close', host, self)
        for control in (self.minimize, self.maximize, self.close_control):
            bar.addWidget(control)
            bar.setSpacing(6)

    def select_language(self, code: str):
        self.language_combo.blockSignals(True)
        try:
            for index in range(self.language_combo.count()):
                if self.language_combo.itemData(index) == code:
                    self.language_combo.setCurrentIndex(index)
                    break
        finally:
            self.language_combo.blockSignals(False)
        self.subtitle.setText('  /  ' + tr('Sua estação Android'))
        self.language_combo.setToolTip(tr('Idioma'))
        self.language_combo.setAccessibleName(tr('Idioma'))
        for control in (self.minimize, self.maximize, self.close_control):
            control.setToolTip(tr({'minimize': 'Minimizar',
                                   'maximize': 'Maximizar ou restaurar',
                                   'close': 'Fechar Flipmelon'}[control.action]))
            control.setAccessibleName(control.toolTip())

    def _language_selected(self, index: int):
        code = self.language_combo.itemData(index)
        if isinstance(code, str) and hasattr(self.host, 'change_language'):
            self.host.change_language(code)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            native = self.host.windowHandle()
            if native is not None and native.startSystemMove():
                event.accept()
                return
            self._drag_offset = event.globalPosition().toPoint() - self.host.frameGeometry().topLeft()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_offset is not None and event.buttons() & Qt.MouseButton.LeftButton:
            if not self.host.isMaximized():
                self.host.move(event.globalPosition().toPoint() - self._drag_offset)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_offset = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.maximize.toggle_maximize()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)


class ResizeGrip(QWidget):
    """Transparent 7 px edge / 12 px corner handles using system resize."""
    def __init__(self, host: QWidget, edges, cursor_shape):
        super().__init__(host)
        self.host = host
        self.edges = edges
        self._fallback = None
        self.setCursor(cursor_shape)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton or self.host.isMaximized():
            return super().mousePressEvent(event)
        native = self.host.windowHandle()
        if native is not None and native.startSystemResize(self.edges):
            event.accept()
            return
        self._fallback = (event.globalPosition().toPoint(), self.host.geometry())
        event.accept()

    def mouseMoveEvent(self, event):
        if self._fallback and event.buttons() & Qt.MouseButton.LeftButton:
            start, rect = self._fallback
            delta = event.globalPosition().toPoint() - start
            self.host.setGeometry(resized_geometry(rect, delta, self.edges,
                                                    self.host.minimumWidth(),
                                                    self.host.minimumHeight()))
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._fallback = None
        super().mouseReleaseEvent(event)


def create_resize_grips(host: QWidget) -> dict:
    T, B, L, R = Qt.Edge.TopEdge, Qt.Edge.BottomEdge, Qt.Edge.LeftEdge, Qt.Edge.RightEdge
    H = Qt.CursorShape.SizeHorCursor
    V = Qt.CursorShape.SizeVerCursor
    F = Qt.CursorShape.SizeFDiagCursor
    D = Qt.CursorShape.SizeBDiagCursor
    return {
        'top_left': ResizeGrip(host, T | L, F),
        'top': ResizeGrip(host, T, V),
        'top_right': ResizeGrip(host, T | R, D),
        'right': ResizeGrip(host, R, H),
        'bottom_right': ResizeGrip(host, B | R, F),
        'bottom': ResizeGrip(host, B, V),
        'bottom_left': ResizeGrip(host, B | L, D),
        'left': ResizeGrip(host, L, H),
    }


def arrange_resize_grips(host: QWidget, grips: dict):
    """Reposition grips when resizing; don't cover toolbar controls or content."""
    maximized = host.isMaximized() or host.isFullScreen()
    if maximized:
        for grip in grips.values():
            grip.hide()
        return
    w, h, border, corner = host.width(), host.height(), GRIP_WIDTH, CORNER_WIDTH
    positions = {
        'top_left': (0, 0, corner, corner),
        'top': (corner, 0, max(0, w-2*corner), border),
        'top_right': (w-corner, 0, corner, corner),
        'right': (w-border, corner, border, max(0, h-2*corner)),
        'bottom_right': (w-corner, h-corner, corner, corner),
        'bottom': (corner, h-border, max(0, w-2*corner), border),
        'bottom_left': (0, h-corner, corner, corner),
        'left': (0, corner, border, max(0, h-2*corner)),
    }
    for key, grip in grips.items():
        grip.setGeometry(*positions[key])
        grip.show()
        grip.raise_()
