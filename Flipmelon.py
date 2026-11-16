"""Flipmelon 1.0.8.9-beta — Figma-aligned Qt interface for an Android lapdock.

Maintains scrcpy + ADB integration from v0.7 while reproducing the six
user-supplied 1040×690 Figma screens. Windows binaries are bundled under vendor/.
"""
from __future__ import annotations

import os
import re
import sys
import shutil
import threading
import subprocess
from pathlib import Path

from PySide6.QtCore import Qt, QObject, Signal, QThread, QTimer, QEvent
from PySide6.QtGui import QIcon, QPixmap, QFont, QFontDatabase, QPainter, QColor, QPen, QBrush
from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QFrame, QComboBox, QCheckBox, QSpinBox,
    QMessageBox, QProgressBar, QSizePolicy, QScrollArea,
)

import engine
from window_chrome import FlipmelonTitleBar, create_resize_grips, arrange_resize_grips
from i18n import tr, set_language, language, LANGUAGES

VERSION = "1.0.8.9-beta"
ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
ASSETS = ROOT / "assets"
WIN = os.name == "nt"
VENDOR = ROOT / "vendor" / ("windows" if WIN else "linux")
LIME = "#DBFF00"

STYLES = """
* { font-family: 'Inter'; font-size: 14px; color: #F7F7F8; }
QMainWindow, QWidget#root, QWidget#page, QWidget#main, QStackedWidget { background: #0A0A0C; }
QFrame#sidebar { background: #141416; border-right: 1px solid #29292D; }
QLabel { background: transparent; }
QLabel#title { font-size: 32px; font-weight: 700; color: #F8F8F8; }
QLabel#section { font-size: 22px; font-weight: 700; }
QLabel#body { font-size: 15px; color: #F3F3F3; }
QLabel#muted { font-size: 14px; color: #96969F; }
QLabel#subtle { font-size: 12px; color: #96969F; }
QLabel#tiny { font-size: 12px; color: #9E9EA6; }
QLabel#headline { font-size: 24px; font-weight: 700; }
QLabel#logoFallback { color: #DBFF00; font-weight: 800; font-size: 22px; }
QLabel#success { color: #00BC84; font-size: 14px; }
QLabel#warning { color: #F1A600; font-size: 13px; }
QLabel#number { background: #29292C; color: #F4F4F5; border-radius: 8px; font-size: 14px; }
QLabel#checkCircle { background: #063326; color: #00C58D; border-radius: 14px; font-size: 14px; }
QLabel#stepActive { color: #DBFF00; font-size: 12px; }
QLabel#stepNormal { color: #9C9BA4; font-size: 12px; }
QLabel#stepDone { color: #09BF8B; font-size: 13px; }
QFrame#card { background: #18181B; border: 1px solid #29292D; border-radius: 16px; }
QFrame#outlineCard { background: #0A0A0C; border: 1px solid #2C2C31; border-radius: 17px; }
QFrame#notice { background: #19191C; border: none; border-radius: 9px; }
QFrame#rule { background: #29292D; min-height: 1px; max-height: 1px; border: none; }
/* All buttons and connection badges are painted with QPainter.
   No QSS button backgrounds: Windows/Qt style engines were drawing squares. */
QComboBox, QSpinBox { background: #09090B; color: #F3F3F3; border: 1px solid #2C2C31;
    border-radius: 12px; padding: 7px 15px; min-height: 28px; }
QComboBox QAbstractItemView { background: #202023; color: #F3F3F3;
    border: 1px solid #303035; selection-background-color: #36363A; }
QComboBox::drop-down { width: 30px; border: 0;
    border-top-right-radius: 12px; border-bottom-right-radius: 12px; }
QSpinBox::up-button { background: transparent; border: 0; width: 19px;
    border-top-right-radius: 10px; }
QSpinBox::down-button { background: transparent; border: 0; width: 19px;
    border-bottom-right-radius: 10px; }
QCheckBox { spacing: 13px; font-size: 14px; }
QCheckBox::indicator { width: 21px; height: 21px; border-radius: 5px; background: #111113;
    border: 1px solid #343438; }
QCheckBox::indicator:checked { background: #DBFF00; border: 1px solid #DBFF00; }
QProgressBar { background: #2A2A2E; border: none; height: 4px; max-height: 4px;
    border-radius: 2px; }
QProgressBar::chunk { background: #DBFF00; border-radius: 2px; }
"""



def setup_inter_font(application: QApplication) -> str:
    """Load user-supplied OFL Inter fonts embedded under assets/fonts.

    Fall back to an Inter font installed on the computer. Never require
    a remote font download when the app starts.
    """
    fonts = ASSETS / "fonts"
    if fonts.is_dir():
        for path in sorted(fonts.iterdir()):
            if path.suffix.lower() in (".ttf", ".otf"):
                QFontDatabase.addApplicationFont(str(path))
    available = set(QFontDatabase.families())
    family = "Inter" if "Inter" in available else ("Segoe UI" if WIN else "DejaVu Sans")
    application.setFont(QFont(family, 10))
    return family

class PillButton(QPushButton):
    """True pill button painted independently of the Windows / Qt stylesheet engine.

    The outer shape is a mathematically rounded capsule: radius = height / 2.
    All visible button variants, including disabled/hover/pressed, use the same
    renderer. Paint geometry never depends on the OS default QPushButton style.
    """
    COLORS = {
        "primary": ("#DBFF00", "#0A0A0C", "#DBFF00"),
        "ghost": ("#0A0A0C", "#F5F5F5", "#2C2C31"),
        "flat": ("#29292C", "#F7F7F8", "#29292C"),
        "wide": ("#09090B", "#F7F7F8", "#2C2C31"),
    }

    def __init__(self, title: str, variant="ghost", parent=None):
        super().__init__(title, parent)
        self.variant = variant
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(48)
        self.setMinimumWidth(90)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.update()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.update()

    def changeEvent(self, event):
        super().changeEvent(event)
        self.update()

    def paintEvent(self, event):
        # Avoid calling QPushButton.paintEvent, which can draw square native fills.
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        fill, foreground, border = self.COLORS.get(self.variant, self.COLORS["ghost"])
        if not self.isEnabled():
            fill, foreground, border = "#29292C", "#96969E", "#29292C"
        elif self.isDown():
            if self.variant == "primary":
                fill, border = "#C2E300", "#C2E300"
            else:
                fill = "#343439"
        elif self.underMouse():
            if self.variant == "primary":
                fill, border = "#E5FF42", "#E5FF42"
            elif self.variant == "flat":
                fill, border = "#3A3A3E", "#3A3A3E"
            else:
                fill = "#232327"
        rect = self.rect().adjusted(1, 1, -1, -1)
        radius = rect.height() / 2.0
        painter.setPen(QPen(QColor(border), 1))
        painter.setBrush(QBrush(QColor(fill)))
        painter.drawRoundedRect(rect, radius, radius)
        painter.setPen(QColor(foreground))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        if self.hasFocus() and self.isEnabled():
            # A thin inner focus indicator doesn't change the pill silhouette.
            focus = self.rect().adjusted(4, 4, -4, -4)
            painter.setPen(QPen(QColor("#858585" if self.variant != "primary" else "#313600"), 1))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(focus, focus.height() / 2.0, focus.height() / 2.0)
        painter.end()


class StatusPill(QLabel):
    """Render USB badges as true pills instead of square Windows labels."""
    THEMES = {
        "pillConnected": ("#063026", "#05BE8B"),
        "pillWait": ("#382B11", "#E8A900"),
        "pillError": ("#4A2426", "#FFAAAA"),
    }

    def __init__(self, text, theme):
        super().__init__(text)
        self.theme = theme
        self.setFixedHeight(30)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_pill(self, value, theme):
        self.setText(value)
        self.theme = theme
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        bg, fg = self.THEMES.get(self.theme, self.THEMES["pillWait"])
        rect = self.rect().adjusted(0, 0, -1, -1)
        radius = rect.height() / 2.0
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(bg))
        painter.drawRoundedRect(rect, radius, radius)
        painter.setPen(QColor(fg))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        painter.end()


class NavPillFrame(QFrame):
    """Paint selected onboarding steps with an actual capsule background."""
    def paintEvent(self, event):
        if self.objectName() == "navSelected":
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#29292C"))
            rect = self.rect().adjusted(0, 0, -1, -1)
            painter.drawRoundedRect(rect, rect.height()/2.0, rect.height()/2.0)
            painter.end()


def set_translated(widget, original: str):
    """Set source text and render the selected locale. Used by live USB updates."""
    widget.setProperty("i18n_source", original)
    widget.setText(tr(original))
    widget.update()
    return widget


def label(value: str, style="body", wrap=True):
    item = StatusPill(tr(value), style) if style.startswith("pill") else QLabel(tr(value))
    item.setProperty("i18n_source", value)
    if not isinstance(item, StatusPill):
        item.setObjectName(style)
    item.setWordWrap(wrap)
    return item


def hline():
    ln = QFrame()
    ln.setObjectName("rule")
    ln.setFixedHeight(1)
    return ln


def make_button(value, callback, style="ghost", width=None):
    btn = PillButton(tr(value), style)
    btn.setProperty("i18n_source", value)
    btn.clicked.connect(callback)
    if width:
        btn.setFixedWidth(width)
    return btn


def make_card(style="card", margins=(23, 22, 23, 22), spacing=15):
    out = QFrame()
    out.setObjectName(style)
    layout = QVBoxLayout(out)
    layout.setContentsMargins(*margins)
    layout.setSpacing(spacing)
    return out


def logo(width=155):
    img = QLabel()
    source = ASSETS / "flipmelon-logo.png"
    if source.exists():
        pix = QPixmap(str(source))
        img.setPixmap(pix.scaledToWidth(width, Qt.TransformationMode.SmoothTransformation))
        img.setFixedSize(width, int(width/4)+2)
    else:
        img.setText("◉ flipmelon")
        img.setObjectName("logoFallback")
    return img


def executable(name):
    bundled = VENDOR / name
    return str(bundled) if bundled.is_file() else shutil.which(name)


def startup_file():
    if WIN:
        return Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs/Startup/Flipmelon.vbs"
    return Path.home()/".config/autostart/flipmelon.desktop"


def startup_enabled():
    return startup_file().exists()


def configure_startup(enabled):
    target = startup_file()
    old_paths = (
        [target.parent/"AutoDock.vbs", target.parent/"AutoDock.lnk"]
        if WIN else [target.parent/"autodock.desktop"]
    )
    for old in old_paths:
        if old.exists():
            try: old.unlink()
            except OSError: pass
    if not enabled:
        if target.exists(): target.unlink()
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if getattr(sys, "frozen", False):
        cmd = f'"{sys.executable}" --autostart'
    else:
        cmd = f'"{sys.executable}" "{Path(__file__).resolve()}" --autostart'
    if WIN:
        # windowless launch (user logs in), not a permanent Windows service
        cmd_quoted = cmd.replace('"', '""')
        target.write_text('Set sh = CreateObject("WScript.Shell")\n'
                          f'sh.Run "{cmd_quoted}", 0, False\n', encoding="utf-8")
    else:
        target.write_text('[Desktop Entry]\nType=Application\nName=Flipmelon\n'
                          f'Exec={cmd}\nTerminal=false\nX-GNOME-Autostart-enabled=true\n',
                          encoding="utf-8")


def scrcpy_window_for_pid(pid: int) -> int | None:
    """Return a *visible* desktop window owned by this scrcpy process.

    Use Windows APIs instead of guessing the window title (the title differs
    between Android devices and scrcpy releases). Called from the worker thread.
    On other platforms readiness is approximated by process liveness.
    """
    if not WIN or not pid:
        return None
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        get_pid = user32.GetWindowThreadProcessId
        get_pid.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.DWORD))
        get_pid.restype = wintypes.DWORD
        user32.IsWindowVisible.argtypes = (wintypes.HWND,)
        user32.IsWindowVisible.restype = wintypes.BOOL
        user32.GetWindowRect.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.RECT))
        user32.GetWindowRect.restype = wintypes.BOOL
        candidates = []

        @callback_type
        def visit(hwnd, _):
            process_id = wintypes.DWORD()
            get_pid(hwnd, ctypes.byref(process_id))
            if process_id.value != pid or not user32.IsWindowVisible(hwnd):
                return True
            rect = wintypes.RECT()
            if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                return True
            width = rect.right - rect.left
            height = rect.bottom - rect.top
            if width >= 320 and height >= 240:
                candidates.append((width * height, int(hwnd)))
            return True

        user32.EnumWindows.argtypes = (callback_type, wintypes.LPARAM)
        user32.EnumWindows.restype = wintypes.BOOL
        user32.EnumWindows(visit, 0)
        return max(candidates)[1] if candidates else None
    except (AttributeError, OSError, ValueError, TypeError):
        return None


def focus_mirror_window(hwnd: int | None) -> None:
    """Best-effort reveal of the already-open fullscreen scrcpy window."""
    if not WIN or not hwnd:
        return
    try:
        import ctypes
        user32 = ctypes.windll.user32
        user32.ShowWindow(hwnd, 5)  # SW_SHOW
        user32.SetForegroundWindow(hwnd)
    except (AttributeError, OSError, ValueError, TypeError):
        pass


class Signals(QObject):
    devices = Signal(dict)
    report = Signal(str)


class Monitor(QObject):
    status = Signal(str, str)
    before_launch = Signal()
    window_ready = Signal(object)
    window_wait_timeout = Signal()
    finished = Signal()

    def __init__(self, configuration):
        super().__init__()
        self.configuration = configuration
        self.halt = threading.Event()
        self.launch_allowed = threading.Event()
        self.proc = None

    def stop(self):
        self.halt.set()
        if self.proc is not None and self.proc.poll() is None:
            try: self.proc.terminate()
            except OSError: pass

    def run(self):
        adb = executable("adb.exe" if WIN else "adb")
        scrcpy = executable("scrcpy.exe" if WIN else "scrcpy")
        if not adb or not scrcpy:
            self.status.emit("error", "ADB ou scrcpy não encontrado no pacote.")
            self.finished.emit()
            return
        flags = subprocess.CREATE_NO_WINDOW if WIN else 0
        try:
            subprocess.run([adb, "start-server"], capture_output=True, timeout=12, creationflags=flags)
        except (OSError, subprocess.TimeoutExpired):
            pass
        previous = None
        while not self.halt.is_set():
            devices = engine.devices(adb)
            state = tuple(sorted(devices.items()))
            if state != previous:
                if not devices: self.status.emit("waiting", "Nenhum celular detectado.")
                elif "unauthorized" in devices.values(): self.status.emit("waiting", "Autorize a depuração USB no celular.")
                elif "device" in devices.values(): self.status.emit("ready", "Celular conectado e autorizado.")
                else: self.status.emit("waiting", "Dispositivo indisponível.")
                previous = state
            ready = [sn for sn, status in devices.items() if status == "device"]
            if len(ready) != 1:
                if len(ready) > 1: self.status.emit("waiting", "Mantenha somente um Android conectado.")
                self.halt.wait(2)
                continue
            sn = ready[0]
            # Make the fullscreen overlay visible *before* scrcpy starts.
            # Do not wait 5 seconds: launch the normal mirroring command
            # immediately behind the artwork while Lottie is playing.
            self.launch_allowed.clear()
            self.before_launch.emit()
            while not self.halt.is_set() and not self.launch_allowed.wait(0.10):
                pass
            if self.halt.is_set():
                break
            if engine.devices(adb).get(sn) != "device":
                previous = None
                continue
            env = os.environ.copy()
            env["PATH"] = str(VENDOR) + os.pathsep + env.get("PATH", "")
            env["ADB"] = adb
            engine.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            logfile = engine.CONFIG_DIR / "scrcpy.log"
            try:
                if logfile.exists() and logfile.stat().st_size > 1_000_000:
                    logfile.unlink()
                with logfile.open("ab") as output:
                    self.proc = subprocess.Popen(
                        engine.command(self.configuration, scrcpy, sn),
                        env=env, cwd=str(VENDOR) if VENDOR.exists() else None,
                        creationflags=flags, stdout=output, stderr=subprocess.STDOUT,
                    )
                    session_start = __import__("time").monotonic()
                    revealed = False
                    self.status.emit("active", "Iniciando espelhamento em segundo plano…")
                    while self.proc.poll() is None and not self.halt.wait(0.3):
                        elapsed = __import__("time").monotonic() - session_start
                        if not revealed:
                            hwnd = scrcpy_window_for_pid(self.proc.pid) if WIN else None
                            if hwnd or (not WIN and elapsed >= 1.2):
                                self.window_ready.emit(hwnd)
                                revealed = True
                                self.status.emit("active", "Espelhamento ativo. Flipmelon conectado!")
                            elif elapsed >= 16:
                                # Never leave a black fullscreen overlay forever
                                # if the SDL window could not be identified.
                                self.window_wait_timeout.emit()
                                revealed = True
                                self.status.emit("error", "Não foi possível confirmar a janela do scrcpy. Confira o espelhamento.")
                        if engine.devices(adb).get(sn) != "device":
                            self.proc.terminate()
                            break
                    if self.proc.poll() is None:
                        self.proc.terminate()
                        try: self.proc.wait(timeout=3)
                        except subprocess.TimeoutExpired: self.proc.kill()
                    if not self.halt.is_set() and engine.devices(adb).get(sn) == "device":
                        if self.proc.poll() not in (0, None):
                            self.status.emit("error", "O scrcpy foi encerrado. Tente Espelhamento nas preferências.")
                        else:
                            self.status.emit("stopped", "Sessão encerrada. Reconecte o USB para reabrir.")
            except OSError as error:
                self.status.emit("error", f"Não foi possível iniciar o scrcpy: {error}")
            finally:
                self.proc = None
            # Respect a manual close: only try again on USB reconnection.
            while not self.halt.wait(2) and engine.devices(adb).get(sn) == "device":
                pass
            previous = None
        self.finished.emit()


class Flipmelon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conf = engine.load()
        set_language(self.conf.get("language", "en"))
        self._monitor_description = ""
        self.thread = None
        self.worker = None
        self.usb_check_running = False
        self.current_devices = {}
        self.signals = Signals()
        self.signals.devices.connect(self.update_devices)
        self.signals.report.connect(self.show_android_report)
        self._mirror_opening = None
        self._mirror_opening_worker = None
        self._closing = False
        self.monitor_state = "waiting"
        self.restart_on_finish = False
        self.setWindowTitle("Flipmelon — " + tr("Seu celular. Uma tela maior."))
        # Custom chrome belongs ONLY to the control panel; scrcpy remains native.
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.resize(1040, 740)  # 690 px designed content + 48 px title bar
        self.setMinimumSize(940, 710)
        self.shell = QWidget(self)
        self.shell.setObjectName("flipWindowShell")
        shell_layout = QVBoxLayout(self.shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)
        self.title_bar = FlipmelonTitleBar(self, ASSETS / "flipmelon-icon.png", self.shell)
        self.title_bar.select_language(language())
        shell_layout.addWidget(self.title_bar)
        self.root = QStackedWidget(self.shell)
        shell_layout.addWidget(self.root, 1)
        self.setCentralWidget(self.shell)
        self._resize_grips = create_resize_grips(self)
        self.create_wizard()
        self.create_dashboard()
        self.create_language_screen()  # root page 2: ALWAYS precedes the setup guide
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_usb)
        # ADB authorization is NOT equivalent to completing the setup guide.
        # Inno Setup launches the app with --setup after installation, so a
        # reinstall shows the whole wizard even if AppData/config.json survived
        # uninstall. Preserve screen settings but let the user review each step.
        self.show_setup = "--setup" in sys.argv or not self.conf.get("onboarding_complete", False)
        if self.show_setup:
            # No USB polling or configuration work happens before language choice.
            self.root.setCurrentIndex(2)
        else:
            self.root.setCurrentIndex(1)
            self.timer.start(2600)
            self.check_usb()

    def create_language_screen(self):
        """Language is a separate first screen, outside the five Android setup steps.

        New installations start in English. Existing users retain their saved
        choice; '--setup' still shows this page before the Android wizard.
        """
        page = QWidget()
        page.setObjectName("page")
        outside = QVBoxLayout(page)
        outside.setContentsMargins(45, 28, 45, 28)
        outside.setSpacing(0)
        header = QHBoxLayout()
        header.addWidget(logo(160))
        header.addStretch()
        outside.addLayout(header)
        outside.addStretch(1)

        content = QVBoxLayout()
        content.setSpacing(15)
        cap = label("IDIOMA DA INTERFACE", "tiny")
        content.addWidget(cap)
        content.addWidget(label("Escolha seu idioma", "title"))
        content.addWidget(label("Selecione o idioma antes de iniciar a configuração do seu Android.", "muted"))
        content.addSpacing(10)
        self.language_buttons = {}
        names = dict(LANGUAGES)
        for code in ("en", "pt", "ru", "es", "fr"):
            option = PillButton(names[code], "wide")
            option.setFixedHeight(43)
            option.setMinimumWidth(350)
            option.setAccessibleName(names[code])
            option.clicked.connect(lambda checked=False, chosen=code: self.change_language(chosen))
            content.addWidget(option)
            self.language_buttons[code] = option
        content.addSpacing(5)
        content.addWidget(label("Você poderá mudar o idioma depois na barra superior.", "subtle"))
        content.addSpacing(13)
        self.language_continue = make_button("Continuar com este idioma →", self.continue_after_language, "primary")
        self.language_continue.setMinimumWidth(350)
        content.addWidget(self.language_continue)
        wrapper = QHBoxLayout()
        wrapper.addStretch(1)
        wrapper.addLayout(content)
        wrapper.addStretch(1)
        outside.addLayout(wrapper)
        outside.addStretch(2)
        self.root.addWidget(page)
        self._refresh_language_options()

    def _refresh_language_options(self):
        if not hasattr(self, "language_buttons"):
            return
        for code, option in self.language_buttons.items():
            option.variant = "primary" if code == language() else "wide"
            option.setAccessibleDescription("Selected" if code == language() else "")
            option.update()

    def continue_after_language(self):
        """Proceed only after the user has seen the language selection screen."""
        self.root.setCurrentIndex(0)
        self.goto_step(0)
        if not self.timer.isActive():
            self.timer.start(2600)
            self.check_usb()

    def change_language(self, code: str):
        """Live translation without rebuilding screens or restarting ADB/scrcpy.

        Changing language is independent of the display preferences currently
        being edited. The language is persisted immediately for next launch.
        """
        chosen = set_language(code)
        self.conf["language"] = chosen
        try:
            engine.save(self.conf)
        except OSError as error:
            QMessageBox.warning(self, "Flipmelon", str(error))
        self.title_bar.select_language(chosen)
        self._refresh_language_options()
        self.setWindowTitle("Flipmelon — " + tr("Seu celular. Uma tela maior."))
        for widget in self.root.findChildren(QWidget):
            source = widget.property("i18n_source")
            if isinstance(source, str) and isinstance(widget, (QLabel, QPushButton, QCheckBox)):
                widget.setText(tr(source))
                widget.update()
        self.mode.setItemText(0, tr("Tela virtual (recomendado)"))
        self.mode.setItemText(1, tr("Espelhamento convencional"))
        self.version_label.setText(f"Flipmelon {VERSION} • " + tr("Primeira\nconfiguração"))
        self.goto_step(getattr(self, "step", 0))
        self.update_devices(self.current_devices)
        if self.monitor_state in ("active", "ready", "error", "stopped") and self._monitor_description:
            self.update_monitor(self.monitor_state, self._monitor_description)

    def create_wizard(self):
        page = QWidget()
        page.setObjectName("page")
        root = QHBoxLayout(page)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(245)
        side = QVBoxLayout(self.sidebar)
        side.setContentsMargins(16, 25, 16, 28)
        side.setSpacing(0)
        brandline = QHBoxLayout()
        brandline.setContentsMargins(12, 0, 0, 0)
        brandline.addWidget(logo(154))
        brandline.addStretch()
        side.addLayout(brandline)
        side.addSpacing(26)
        intro = QVBoxLayout()
        intro.setContentsMargins(12, 0, 12, 0)
        intro.setSpacing(18)
        intro.addWidget(label("Transforme qualquer\nnotebook compatível em\num lapdock para Android.", "body"))
        intro.addWidget(label("Instalação guiada, conexão\nautomática e tela cheia.", "subtle"))
        side.addLayout(intro)
        side.addSpacing(53)
        self.menu_rows = []
        names = ["Boas-vindas", "Modo desenvolvedor", "Depuração USB", "Conectar celular", "Preferências de tela"]
        for index, name in enumerate(names):
            item = NavPillFrame()
            item.setObjectName("navNormal")
            row = QHBoxLayout(item)
            row.setContentsMargins(12, 0, 7, 0)
            row.setSpacing(14)
            number = label(f"{index + 1:02d}", "stepNormal", False)
            number.setFixedWidth(22)
            title = label(name, "stepNormal", False)
            row.addWidget(number)
            row.addWidget(title)
            row.addStretch()
            item.setFixedHeight(37)
            side.addWidget(item)
            side.addSpacing(7)
            self.menu_rows.append((item, number, title))
        side.addStretch()
        progress_name = label("ETAPA {n} DE 5", "tiny")
        progress_name.setText(tr("ETAPA {n} DE 5").format(n=1))
        progress_line = QProgressBar()
        progress_line.setRange(0, 5)
        progress_line.setTextVisible(False)
        progress_line.setValue(1)
        side.addWidget(progress_name)
        side.addSpacing(16)
        side.addWidget(progress_line)
        side.addSpacing(24)
        self.version_label = label("Primeira\nconfiguração", "subtle")
        self.version_label.setText(f"Flipmelon {VERSION} • " + tr("Primeira\nconfiguração"))
        side.addWidget(self.version_label)
        self.progress_name = progress_name
        self.progress_line = progress_line
        root.addWidget(self.sidebar)

        main = QWidget()
        main.setObjectName("main")
        body = QVBoxLayout(main)
        body.setContentsMargins(39, 39, 40, 32)
        body.setSpacing(0)
        self.steps = QStackedWidget()
        body.addWidget(self.steps, 1)
        body.addWidget(hline())
        body.addSpacing(26)
        footer = QHBoxLayout()
        self.back_button = make_button("← Voltar", self.previous_step, "ghost", 112)
        self.footer_hint = label("Vamos começar?", "subtle")
        self.next_button = make_button("Começar →", self.next_step, "primary", 168)
        footer.addWidget(self.back_button)
        footer.addWidget(self.footer_hint)
        footer.addStretch()
        footer.addWidget(self.next_button)
        body.addLayout(footer)
        root.addWidget(main, 1)
        self.root.addWidget(page)

        self.build_welcome()
        self.build_developer()
        self.build_debugging()
        self.build_connection()
        self.build_preferences()

    def page_start(self, heading, subheading):
        page = QWidget()
        page.setObjectName("page")
        v = QVBoxLayout(page)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)
        v.addWidget(label("CONFIGURAÇÃO INICIAL", "tiny"))
        v.addSpacing(25)
        v.addWidget(label(heading, "title"))
        v.addSpacing(16)
        v.addWidget(label(subheading, "muted"))
        v.addSpacing(45)
        self.steps.addWidget(page)
        return v

    def build_welcome(self):
        v = self.page_start(
            "Bem-vindo ao Flipmelon",
            "Vamos preparar seu celular para usar a tela, o teclado e o mouse deste computador.",
        )
        c = make_card()
        c.layout().addWidget(label("Simples desde o primeiro passo.", "section"))
        c.layout().addSpacing(10)
        for line in (
            "Nada para instalar no celular.",
            "ADB e scrcpy já acompanham o aplicativo.",
            "Conexão via USB e configuração em poucos passos.",
        ):
            row = QHBoxLayout()
            tick = label("✓", "checkCircle", False)
            tick.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tick.setFixedSize(28, 28)
            row.addWidget(tick)
            row.addSpacing(3)
            row.addWidget(label(line, "body"), 1)
            c.layout().addLayout(row)
            c.layout().addSpacing(5)
        c.setMinimumHeight(268)
        v.addWidget(c)
        v.addSpacing(34)
        v.addWidget(label("Seu Android, com a praticidade de uma tela maior.", "muted"))
        v.addStretch()
        self.welcome_bottom = label("Vamos começar?", "subtle")

    def numbered_card(self, rows):
        c = make_card("outlineCard", (23, 3, 23, 3), 0)
        for n, instruction in enumerate(rows):
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            number = label(str(n + 1), "number", False)
            number.setFixedSize(32, 32)
            number.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row.addWidget(number)
            row.addSpacing(4)
            row.addWidget(label(instruction, "body"), 1)
            group = QWidget()
            group.setLayout(row)
            group.setFixedHeight(85)
            c.layout().addWidget(group)
            if n < len(rows) - 1:
                c.layout().addWidget(hline())
        return c

    def build_developer(self):
        v = self.page_start(
            "Ative as opções de desenvolvedor",
            "No celular, siga as instruções abaixo. Isso é necessário apenas na primeira configuração.",
        )
        v.addWidget(self.numbered_card([
            "Abra Configurações → Sobre o telefone.",
            "Em Samsung, abra Informações do software.",
            "Toque 7 vezes em Número da compilação.",
        ]))
        v.addSpacing(16)
        note = make_card("notice", (16, 16, 16, 16))
        note.layout().addWidget(label("Em Motorola, Xiaomi e outras marcas, os nomes dos menus podem variar.", "muted"))
        v.addWidget(note)
        v.addStretch()

    def build_debugging(self):
        v = self.page_start(
            "Permita a depuração USB",
            "O Flipmelon usa ADB para reconhecer e controlar seu Android autorizado.",
        )
        v.addWidget(self.numbered_card([
            "Volte às Configurações e abra Opções do desenvolvedor.",
            "Ative Depuração USB.",
            "Conecte o celular com um cabo USB que transmita dados.",
        ]))
        v.addSpacing(16)
        note = make_card("notice", (16, 16, 16, 16))
        note.setMinimumHeight(70)
        note.layout().addWidget(label("Autorize somente computadores confiáveis. Desative a depuração quando não precisar.", "muted"))
        v.addWidget(note)
        v.addStretch()

    def build_connection(self):
        v = self.page_start(
            "Conecte e autorize seu celular",
            "Desbloqueie o Android e aceite a janela de autorização USB exibida nele.",
        )
        c = make_card("outlineCard", (23, 17, 23, 23), 15)
        top = QHBoxLayout()
        top.addWidget(label("VERIFICAÇÃO DA CONEXÃO", "tiny"))
        top.addStretch()
        self.connection_pill = label("Aguardando celular", "pillWait", False)
        self.connection_pill.setFixedWidth(168)
        self.connection_pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top.addWidget(self.connection_pill)
        c.layout().addLayout(top)
        c.layout().addSpacing(16)
        self.connection_title = label("Nenhum celular detectado.", "headline")
        c.layout().addWidget(self.connection_title)
        self.connection_message = label("Conecte um cabo USB de dados.", "muted")
        c.layout().addWidget(self.connection_message)
        c.layout().addSpacing(1)
        self.connection_help = label("Se não aparecer nada, confira o cabo USB e a Depuração USB.", "muted")
        c.layout().addWidget(self.connection_help)
        c.layout().addSpacing(2)
        c.layout().addWidget(make_button("Verificar novamente", self.check_usb, "flat"))
        c.setMinimumHeight(284)
        v.addWidget(c)
        v.addSpacing(18)
        v.addWidget(label("O próximo passo será liberado após a conexão e a autorização no Android.", "muted"))
        v.addStretch()

    def build_preferences(self):
        v = self.page_start(
            "Escolha como usar a tela",
            "Estas preferências podem ser alteradas depois.",
        )
        c = make_card("card", (23, 17, 23, 25), 12)
        c.layout().addWidget(label("Modo de exibição", "body"))
        self.mode = QComboBox()
        self.mode.addItem(tr("Tela virtual (recomendado)"), "virtual")
        self.mode.addItem(tr("Espelhamento convencional"), "mirror")
        self.mode.setCurrentIndex(0 if self.conf.get("mode", "virtual") == "virtual" else 1)
        c.layout().addWidget(self.mode)
        c.layout().addWidget(label("A barra inferior depende do launcher Android/DeX; o Flipmelon não a desenha.", "subtle"))
        c.layout().addSpacing(13)
        row = QHBoxLayout()
        left = QVBoxLayout()
        left.setSpacing(9)
        left.addWidget(label("Resolução", "body"))
        self.res = QComboBox()
        self.res.setEditable(True)
        self.res.addItems(["1920x1080", "1920x1200", "1600x900", "1366x768", "1280x720"])
        self.res.setCurrentText(self.conf.get("resolution", "1920x1080"))
        left.addWidget(self.res)
        right = QVBoxLayout()
        right.setSpacing(9)
        right.addWidget(label("Densidade (DPI)", "body"))
        self.dpi = QSpinBox()
        self.dpi.setRange(100, 600)
        self.dpi.setValue(int(self.conf.get("dpi", 120)))
        right.addWidget(self.dpi)
        row.addLayout(left, 1)
        row.addSpacing(9)
        row.addLayout(right, 1)
        c.layout().addLayout(row)
        c.layout().addSpacing(11)
        c.layout().addWidget(label("Recuperação da tela virtual", "body"))
        c.layout().addWidget(label(
            "Se a barra inferior sumiu, restaure os parâmetros de uma versão anterior. "
            "As decorações do Android permanecem habilitadas por padrão.", "subtle"))
        c.layout().addWidget(make_button(
            "Restaurar perfil v0.9 (1920×1080 · 120 DPI)",
            self.restore_v09, "ghost"))
        c.layout().addWidget(make_button(
            "Perfil original MacBook (1920×1200 · 180 DPI)",
            self.restore_macbook, "ghost"))
        c.layout().addWidget(make_button(
            "Testar interface Samsung (1920×1080 · 284 DPI)",
            self.try_samsung_density, "ghost"))
        c.layout().addWidget(label(
            "Teste experimental: a densidade pode mudar o layout, mas não força o DeX "
            "nem os indicadores de apps abertos no dock Samsung.", "subtle"))
        c.layout().addWidget(make_button(
            "Verificar Android / One UI (somente leitura)",
            self.inspect_android, "ghost"))
        self.clean_virtual = QCheckBox()
        set_translated(self.clean_virtual, "Criar sessão limpa (não preservar apps ao fechar)")
        self.clean_virtual.setChecked(bool(self.conf.get("clean_virtual", False)))
        c.layout().addWidget(self.clean_virtual)
        c.layout().addWidget(label(
            "A sessão limpa fecha os apps dessa tela quando você sai; não altera o celular "
            "nem garante a barra do launcher Samsung.", "subtle"))
        c.layout().addSpacing(9)
        c.layout().addWidget(hline())
        c.layout().addSpacing(10)
        self.autostart = QCheckBox()
        set_translated(self.autostart, "Iniciar Flipmelon automaticamente após o login")
        self.autostart.setChecked(bool(self.conf.get("start_with_windows", True)))
        c.layout().addWidget(self.autostart)
        v.addWidget(c)
        v.addStretch()
        # This screen includes recovery controls; scroll instead of clipping
        # Save/Connect and the last options on 1366x768 laptops or Windows DPI > 100%.
        original = v.parentWidget()
        position = self.steps.indexOf(original)
        self.steps.removeWidget(original)
        scroller = QScrollArea(self.steps)
        scroller.setWidgetResizable(True)
        scroller.setFrameShape(QFrame.Shape.NoFrame)
        scroller.setStyleSheet("QScrollArea {border:0; background:#0A0A0C;}"
                              "QScrollBar:vertical {width:10px; background:#17171A;}"
                              "QScrollBar::handle:vertical {background:#45454A; border-radius:5px;}")
        scroller.setWidget(original)
        self.steps.insertWidget(position, scroller)

    def restore_v09(self):
        """Restore known v0.9 display geometry; save only via Salvar e conectar."""
        self.mode.setCurrentIndex(0)
        self.res.setCurrentText("1920x1080")
        self.dpi.setValue(120)
        self.clean_virtual.setChecked(False)

    def restore_macbook(self):
        """Restore the previously tested MacBook profile."""
        self.mode.setCurrentIndex(0)
        self.res.setCurrentText("1920x1200")
        self.dpi.setValue(180)
        self.clean_virtual.setChecked(False)

    def try_samsung_density(self):
        """Optional DPI experiment. Never mutates the phone settings."""
        self.mode.setCurrentIndex(0)
        self.res.setCurrentText("1920x1080")
        self.dpi.setValue(284)
        self.clean_virtual.setChecked(False)

    def create_dashboard(self):
        page = QWidget()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 25, 40, 32)
        layout.setSpacing(0)
        layout.addWidget(logo(154))
        layout.addSpacing(34)
        layout.addWidget(label("Seu celular. Uma tela maior.", "title"))
        layout.addSpacing(20)
        layout.addWidget(label("Quando conectado, seu Android pode utilizar a tela, o teclado e o mouse do computador.", "muted"))
        layout.addSpacing(40)
        c = make_card("outlineCard", (23, 20, 23, 23), 12)
        top = QHBoxLayout()
        top.addWidget(label("CONEXÃO USB", "tiny"))
        top.addStretch()
        self.dashboard_pill = label("Aguardando celular", "pillWait", False)
        self.dashboard_pill.setFixedWidth(142)
        self.dashboard_pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top.addWidget(self.dashboard_pill)
        c.layout().addLayout(top)
        c.layout().addSpacing(13)
        self.dashboard_title = label("Aguardando seu Android.", "headline")
        c.layout().addWidget(self.dashboard_title)
        self.dashboard_hint = label("Conecte o celular por USB e autorize este computador.", "muted")
        c.layout().addWidget(self.dashboard_hint)
        actions = QHBoxLayout()
        actions.addWidget(make_button("Iniciar Flipmelon", self.start_session, "primary", 188))
        actions.addSpacing(1)
        actions.addWidget(make_button("Parar sessão", self.stop_session, "ghost", 155))
        actions.addStretch()
        c.layout().addLayout(actions)
        c.setMinimumHeight(216)
        layout.addWidget(c)
        layout.addSpacing(16)
        options = make_card("card", (23, 21, 23, 19), 12)
        options.layout().addWidget(label("Sua estação, do seu jeito.", "section"))
        options.layout().addWidget(label("Para alterar a resolução, o modo de exibição ou revisar o guia, use o botão abaixo.", "muted"))
        options.layout().addWidget(make_button("Configurações e guia", self.open_preferences, "wide"))
        options.layout().addWidget(make_button("Refazer passo a passo", self.restart_guide, "ghost"))
        options.setMinimumHeight(157)
        layout.addWidget(options)
        layout.addStretch()
        layout.addWidget(label(f"Flipmelon {VERSION}", "subtle"))
        self.root.addWidget(page)

    def goto_step(self, index):
        self.step = index
        self.steps.setCurrentIndex(index)
        self.progress_name.setText(tr("ETAPA {n} DE 5").format(n=index + 1))
        self.progress_line.setValue(index + 1)
        for i, (frame, number, title) in enumerate(self.menu_rows):
            frame.setObjectName("navSelected" if i == index else "navNormal")
            number.setText("✓" if i < index else f"{i + 1:02d}")
            number.setObjectName("stepDone" if i < index else ("stepActive" if i == index else "stepNormal"))
            title.setObjectName("stepActive" if i == index else "stepNormal")
            for w in (frame, number, title):
                w.style().unpolish(w)
                w.style().polish(w)
        self.back_button.setVisible(index > 0)
        self.footer_hint.setVisible(index == 0)
        set_translated(self.next_button, "Começar →" if index == 0 else "Salvar e conectar →" if index == 4 else "Continuar →")
        self.next_button.setEnabled(index != 3 or self.authorized())
        if index == 3:
            self.check_usb()

    def authorized(self):
        return len([k for k, v in self.current_devices.items() if v == "device"]) == 1

    def previous_step(self):
        if self.step > 0:
            self.goto_step(self.step - 1)

    def next_step(self):
        if self.step == 3 and not self.authorized():
            return
        if self.step < 4:
            self.goto_step(self.step + 1)
            return
        resolution = self.res.currentText().strip()
        if not re.fullmatch(r"[1-9]\d{2,4}x[1-9]\d{2,4}", resolution):
            QMessageBox.warning(self, tr("Resolução inválida"), tr("Informe uma resolução como 1920x1080."))
            return
        self.conf.update(
            mode=self.mode.currentData(), resolution=resolution, dpi=self.dpi.value(),
            clean_virtual=self.clean_virtual.isChecked(),
            fullscreen=True, onboarding_complete=True,
            start_with_windows=self.autostart.isChecked(),
        )
        try:
            engine.save(self.conf)
            configure_startup(self.autostart.isChecked())
        except OSError as error:
            QMessageBox.warning(self, tr("Não foi possível salvar"), str(error))
            return
        self.root.setCurrentIndex(1)
        # Stop the previous session if user changed settings: restart with new parameters.
        if self.thread and self.thread.isRunning():
            self.restart_on_finish = True
            self.stop_session()
        else:
            self.start_session()

    def open_preferences(self):
        self.root.setCurrentIndex(0)
        self.goto_step(4)

    def restart_guide(self):
        """Restart from language choice, before the five Android setup steps."""
        self.root.setCurrentIndex(2)

    def inspect_android(self):
        """Read a few non-identifying Android properties without changing settings."""
        adb = executable("adb.exe" if WIN else "adb")
        # Read the cached ADB state; never block the GUI while enumerating USB.
        devices = self.current_devices if adb else {}
        ready = [sn for sn, state in devices.items() if state == "device"]
        if len(ready) != 1:
            QMessageBox.information(self, "Flipmelon", tr("Conecte e autorize apenas um Android antes do diagnóstico."))
            return
        serial = ready[0]
        def work():
            props = [
                ("Fabricante", "ro.product.manufacturer"),
                ("Versão Android", "ro.build.version.release"),
                ("Propriedade One UI", "ro.build.version.oneui"),
            ]
            lines = []
            for title, key in props:
                response = engine.run([adb, "-s", serial, "shell", "getprop", key], 6)
                value = response.stdout.strip() if response and response.returncode == 0 else ""
                lines.append(f"{tr(title)}: {value or tr('(não informado pelo telefone)')}")
            lines += ["", tr("A barra de tarefas e os indicadores de apps ativos são do Android/DeX."),
                      tr("O scrcpy exibe a tela virtual, mas não desenha nem controla esses indicadores."),
                      tr("Nenhuma configuração do telefone foi alterada.")]
            self.signals.report.emit("\n".join(lines))
        threading.Thread(target=work, daemon=True).start()

    def show_android_report(self, text):
        QMessageBox.information(self, tr("Diagnóstico Android (somente leitura)"), text)

    def check_usb(self):
        if self.usb_check_running:
            return
        adb = executable("adb.exe" if WIN else "adb")
        if not adb:
            self.signals.devices.emit({})
            return
        self.usb_check_running = True
        def run():
            try:
                devices = engine.devices(adb)
            except Exception:
                devices = {}
            self.signals.devices.emit(devices)
        threading.Thread(target=run, daemon=True).start()

    def update_devices(self, devices):
        self.usb_check_running = False
        self.current_devices = devices
        if not devices:
            title, hint, helptext = (
                "Nenhum celular detectado.", "Conecte um cabo USB de dados.",
                "Se não aparecer nada, confira o cabo USB e a Depuração USB.",
            )
            pill, pill_style = "Aguardando celular", "pillWait"
        elif len([d for d, s in devices.items() if s == "device"]) > 1:
            title, hint, helptext = (
                "Mais de um celular autorizado.", "Mantenha apenas um celular conectado.",
                "Desconecte os demais dispositivos para continuar.",
            )
            pill, pill_style = "Verificar conexão", "pillWait"
        elif self.authorized():
            title, hint, helptext = (
                "Celular conectado e autorizado!", "Seu Android está pronto para usar.",
                "Agora você pode continuar para as preferências da tela.",
            )
            pill, pill_style = "✓ Conectado", "pillConnected"
        elif "unauthorized" in devices.values():
            title, hint, helptext = (
                "Autorize este computador.", "Desbloqueie o Android e aceite o pedido de depuração USB.",
                "A janela de autorização aparece na tela do telefone.",
            )
            pill, pill_style = "Autorização pendente", "pillWait"
        else:
            title, hint, helptext = (
                "Dispositivo indisponível.", "Confira a conexão e desbloqueie o celular.",
                "Se necessário, reconecte o cabo USB.",
            )
            pill, pill_style = "Verificar conexão", "pillWait"
        set_translated(self.connection_title, title)
        set_translated(self.connection_message, hint)
        set_translated(self.connection_help, helptext)
        self.set_pill(self.connection_pill, pill, pill_style)
        if self.root.currentIndex() == 0 and self.step == 3:
            self.next_button.setEnabled(self.authorized())
        if self.monitor_state != "active":
            self.set_pill(self.dashboard_pill, pill, pill_style)
            set_translated(self.dashboard_title, title)
            set_translated(self.dashboard_hint, hint)

    @staticmethod
    def set_pill(widget, value, style):
        if isinstance(widget, StatusPill):
            widget.update_pill(tr(value), style)
            widget.setProperty("i18n_source", value)
        else:
            set_translated(widget, value)
            widget.setObjectName(style)
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    def start_session(self):
        if self.thread and self.thread.isRunning():
            return
        self.thread = QThread(self)
        self.worker = Monitor(dict(self.conf))
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.status.connect(self.update_monitor)
        self.worker.before_launch.connect(self.show_mirror_opening)
        worker = self.worker
        self.worker.window_ready.connect(lambda hwnd, w=worker: self.mirror_window_ready(w, hwnd))
        self.worker.window_wait_timeout.connect(lambda w=worker: self.mirror_window_timeout(w))
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.monitor_finished)
        self.thread.start()
        self.monitor_state = "waiting"
        set_translated(self.dashboard_title, "Aguardando seu Android.")
        set_translated(self.dashboard_hint, "O Flipmelon abrirá a tela quando o USB for autorizado.")

    def show_mirror_opening(self):
        """Show the overlay and immediately authorize the scrcpy subprocess.

        scrcpy starts BEHIND the topmost fullscreen Lottie. Five seconds is
        the animation's minimum duration, not a startup delay. Once both the
        five seconds and the SDL window are ready, fade to the real screen.
        """
        worker = self.worker
        if worker is None or worker.halt.is_set() or self._closing:
            return
        self._close_mirror_opening()
        try:
            from lottie_window import LottieFullscreen
            opening = LottieFullscreen(ASSETS)
            self._mirror_opening = opening
            self._mirror_opening_worker = worker
            opening.finished.connect(lambda: self._finish_mirror_opening(opening))
            opening.show_for_screen(self.screen() or QApplication.primaryScreen())
            set_translated(self.dashboard_title, "Abrindo tela cheia…")
            set_translated(self.dashboard_hint, "A tela virtual está iniciando durante a animação.")
        except Exception as error:
            print(f"Animação indisponível; iniciando espelhamento: {error}")
            self._close_mirror_opening()
        finally:
            # Release the worker NOW, rather than after the 5s animation.
            if not worker.halt.is_set() and not self._closing:
                worker.launch_allowed.set()

    def mirror_window_ready(self, worker, hwnd):
        if (self._mirror_opening is not None and
                self._mirror_opening_worker is worker and not self._closing):
            self._mirror_opening.mark_mirror_ready(hwnd)

    def mirror_window_timeout(self, worker):
        if self._mirror_opening is not None and self._mirror_opening_worker is worker:
            # Remove the black overlay: don't trap the user in a splash.
            self._close_mirror_opening()

    def _finish_mirror_opening(self, opening):
        if self._mirror_opening is not opening:
            return
        self._mirror_opening = None
        self._mirror_opening_worker = None
        opening.deleteLater()

    def _close_mirror_opening(self):
        if self._mirror_opening is not None:
            opening = self._mirror_opening
            self._mirror_opening = None
            self._mirror_opening_worker = None
            opening.close_immediately()
            opening.deleteLater()

    def monitor_finished(self):
        if self.restart_on_finish:
            self.restart_on_finish = False
            QTimer.singleShot(100, self.start_session)

    def update_monitor(self, state, description):
        self.monitor_state = state
        self._monitor_description = description
        if state in ("error", "stopped"):
            self._close_mirror_opening()
        if state == "active":
            self.set_pill(self.dashboard_pill, "✓ Conectado", "pillConnected")
            set_translated(self.dashboard_title, description)
            set_translated(self.dashboard_hint, "Flipmelon está monitorando o cabo USB.")
        elif state == "error":
            self.set_pill(self.dashboard_pill, "Falha na sessão", "pillError")
            set_translated(self.dashboard_title, "Não foi possível iniciar a tela.")
            set_translated(self.dashboard_hint, description)
        elif state == "ready":
            self.set_pill(self.dashboard_pill, "✓ Conectado", "pillConnected")
            set_translated(self.dashboard_title, description)
            set_translated(self.dashboard_hint, "Preparando a sessão do scrcpy…")
        elif state == "stopped":
            self.set_pill(self.dashboard_pill, "Sessão encerrada", "pillWait")
            set_translated(self.dashboard_title, description)
            set_translated(self.dashboard_hint, "Para abrir novamente, desconecte e reconecte o aparelho.")
        else:
            self.set_pill(self.dashboard_pill, "Aguardando celular", "pillWait")
            set_translated(self.dashboard_title, description)
            set_translated(self.dashboard_hint, "Conecte e autorize seu Android para continuar.")

    def stop_session(self):
        self._close_mirror_opening()
        if self.worker and self.thread and self.thread.isRunning():
            self.worker.stop()
        self.monitor_state = "waiting"
        set_translated(self.dashboard_title, "Sessão encerrada.")
        set_translated(self.dashboard_hint, "Clique em Iniciar Flipmelon para usar novamente.")
        self.set_pill(self.dashboard_pill, "Desconectado", "pillWait")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "_resize_grips"):
            arrange_resize_grips(self, self._resize_grips)

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.Type.WindowStateChange:
            if hasattr(self, "_resize_grips"):
                arrange_resize_grips(self, self._resize_grips)
            if hasattr(self, "title_bar"):
                self.title_bar.maximize.update()

    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, "_resize_grips"):
            arrange_resize_grips(self, self._resize_grips)

    def closeEvent(self, event):
        self._closing = True
        self._close_mirror_opening()
        if self.worker and self.thread and self.thread.isRunning():
            self.worker.stop()
            if not self.thread.wait(9000):
                event.ignore()
                QMessageBox.information(self, "Flipmelon", tr("Aguarde o encerramento da sessão."))
                return
        event.accept()



def main():
    application = QApplication(sys.argv)
    application.setApplicationName("Flipmelon")
    ico = ROOT / "flipmelon.ico"
    if ico.is_file():
        application.setWindowIcon(QIcon(str(ico)))
    family = setup_inter_font(application)
    application.setStyleSheet(STYLES if family == "Inter" else
                              STYLES.replace("font-family: 'Inter';", f"font-family: '{family}';"))
    window = Flipmelon()
    window.show()
    if (window.conf.get("onboarding_complete", False)
            and "--autostart" in sys.argv and "--setup" not in sys.argv):
        QTimer.singleShot(500, window.start_session)
    return application.exec()

if __name__ == '__main__':
    sys.exit(main())
