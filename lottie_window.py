"""Flipmelon splash using the SAME rlottie-python playback confirmed by the user.

Renders the artist's original assets/animations/logo.json via native RLottie.
The animation is generated on a daemon worker, never on Qt's GUI thread.
No GIF, MP4, Qt Multimedia, Qt WebEngine, raster frame assets or video decoder.
"""
from __future__ import annotations

import os
import threading
import time
from pathlib import Path

from PySide6.QtCore import Qt, QObject, Signal, QTimer, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QColor, QImage, QPainter
from PySide6.QtWidgets import QApplication, QWidget
from animation_scale import logo_width

DURATION_MS = 5000
FADE_MS = 850


class RLottieRenderer(QObject):
    frameReady = Signal(object)
    failure = Signal(str)

    def __init__(self, logo_json: Path, started_at: float, size: tuple[int, int], stop: threading.Event):
        super().__init__()
        self.logo_json = Path(logo_json)
        self.started_at = started_at
        self.size = size
        self.stop = stop

    def render(self):
        try:
            # Import in the worker so missing runtime dependencies cannot crash
            # the application during module import or basic mirroring.
            from rlottie_python import LottieAnimation
            anim = LottieAnimation.from_file(str(self.logo_json))
            frame_count = int(anim.lottie_animation_get_totalframe())
            fps = float(anim.lottie_animation_get_framerate())
            if frame_count <= 0 or fps <= 0:
                raise RuntimeError('Arquivo Lottie sem quadros válidos')
            last_frame = -1
            width, height = self.size
            while not self.stop.is_set():
                elapsed = time.monotonic() - self.started_at
                if elapsed * 1000 >= DURATION_MS:
                    break
                # Never slow down the artist's timeline when a render is late:
                # skip to the correct frame using monotonic clock time.
                frame_number = min(frame_count - 1, int(elapsed * fps))
                if frame_number != last_frame:
                    buffer = anim.lottie_animation_render(frame_num=frame_number,
                                                          width=width, height=height)
                    image = QImage(buffer, width, height, width * 4,
                                   QImage.Format.Format_ARGB32).copy()
                    if image.isNull():
                        raise RuntimeError('RLottie devolveu um quadro inválido')
                    self.frameReady.emit(image)
                    last_frame = frame_number
                self.stop.wait(0.007)
        except Exception as error:
            self.failure.emit(str(error))


class LottieFullscreen(QWidget):
    """Drop-in replacement for the proven v1.0.8.2 splash API.

    show_for_screen -> scrcpy starts behind it -> mark_mirror_ready ->
    5s Lottie concludes -> 850ms fade -> scrcpy window is focused.
    """
    finished = Signal()

    def __init__(self, assets_dir: Path, parent=None):
        super().__init__(None)
        self.assets_dir = Path(assets_dir)
        self.logo_json = self.assets_dir / 'animations' / 'logo.json'
        self.setWindowTitle('Flipmelon — Conectando')
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self._finished = False
        self._min_time_done = False
        self._mirror_ready = False
        self._mirror_hwnd = None
        self._fade = None
        self._image = None
        self._render_error = ''
        self._thread = None
        self._renderer = None
        self._stop = threading.Event()
        self._keep_on_top = QTimer(self)
        self._keep_on_top.setInterval(200)
        self._keep_on_top.timeout.connect(self._raise_overlay)

    def show_for_screen(self, screen=None):
        screen = screen or QApplication.primaryScreen()
        if screen is not None:
            self.setGeometry(screen.geometry())
        self.setWindowOpacity(1.0)
        self.showFullScreen()
        self._raise_overlay()
        self._keep_on_top.start()
        self._stop.clear()
        w = logo_width(max(1, self.width()), max(1, self.height()))
        h = max(1, round(w * 300 / 1400))
        if not self.logo_json.is_file():
            self._render_error = 'Arquivo logo.json não encontrado'
        else:
            started = time.monotonic()
            self._renderer = RLottieRenderer(self.logo_json, started, (w, h), self._stop)
            self._renderer.frameReady.connect(self._on_frame)
            self._renderer.failure.connect(self._on_error)
            self._thread = threading.Thread(target=self._renderer.render,
                                            name='Flipmelon-RLottie', daemon=True)
            self._thread.start()
        QTimer.singleShot(DURATION_MS, self._animation_complete)
        QTimer.singleShot(23000, self._watchdog)

    def _on_frame(self, image):
        if self._finished:
            return
        self._image = image
        self.update()

    def _on_error(self, message):
        if self._finished:
            return
        self._render_error = f'Animação indisponível: {message}'
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor('#000000'))
        if self._image is not None:
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            w = logo_width(max(1, self.width()), max(1, self.height()))
            h = w * 300 / 1400
            painter.drawImage(QRectF((self.width()-w)/2, (self.height()-h)/2,
                                     w, h), self._image)
        elif self._render_error:
            # Never silently replace an animation error with a static logo.
            painter.setPen(QColor('#DBFF00'))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._render_error)
        painter.end()

    def _animation_complete(self):
        if self._finished:
            return
        self._min_time_done = True
        self._stop.set()
        self._maybe_fade()

    def mark_mirror_ready(self, hwnd=None):
        if self._finished:
            return
        self._mirror_ready = True
        self._mirror_hwnd = hwnd
        self._maybe_fade()

    def _maybe_fade(self):
        if self._finished or self._fade is not None or not (self._min_time_done and self._mirror_ready):
            return
        self._fade = QPropertyAnimation(self, b'windowOpacity', self)
        self._fade.setDuration(FADE_MS)
        self._fade.setStartValue(1.0)
        self._fade.setEndValue(0.0)
        self._fade.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._fade.finished.connect(self._close_overlay)
        self._fade.start()

    def _raise_overlay(self):
        if self._finished:
            return
        if os.name == 'nt':
            try:
                import ctypes
                ctypes.windll.user32.SetWindowPos(int(self.winId()), -1, 0, 0, 0, 0,
                                                 0x0001 | 0x0002 | 0x0010)
            except (AttributeError, OSError, ValueError, TypeError):
                pass
        else:
            self.raise_()

    def _watchdog(self):
        if not self._finished:
            self._close_overlay()

    def close_immediately(self):
        self._close_overlay()

    def _close_overlay(self):
        if self._finished:
            return
        self._finished = True
        self._stop.set()
        self._keep_on_top.stop()
        if self._fade is not None:
            self._fade.stop()
        self.close()
        if self._mirror_ready and self._mirror_hwnd and os.name == 'nt':
            try:
                import ctypes
                ctypes.windll.user32.ShowWindow(self._mirror_hwnd, 5)
                ctypes.windll.user32.SetForegroundWindow(self._mirror_hwnd)
            except (AttributeError, OSError, ValueError, TypeError):
                pass
        self.finished.emit()

    def mousePressEvent(self, event):
        event.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self._close_overlay()
        else:
            super().keyPressEvent(event)
