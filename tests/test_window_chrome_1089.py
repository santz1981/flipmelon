"""Checks the branded native window frame without requiring PySide6 locally."""
import ast, unittest, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/'Flipmelon.py').read_text(encoding='utf8')
CHROME=(ROOT/'window_chrome.py').read_text(encoding='utf8')
class ChromeTests(unittest.TestCase):
    def test_syntax(self):
        ast.parse(APP)
        ast.parse(CHROME)
        ast.parse((ROOT/'visualizar_janela.py').read_text(encoding='utf8'))
    def test_custom_window_and_widgets(self):
        self.assertIn('self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)', APP)
        self.assertIn('self.title_bar = FlipmelonTitleBar(', APP)
        self.assertIn('self.root = QStackedWidget(self.shell)', APP)
        for string in ['class FlipmelonTitleBar', 'class WindowControl',
                       'startSystemMove()', 'startSystemResize(self.edges)',
                       'mouseDoubleClickEvent', 'resized_geometry',
                       'class ResizeGrip', 'def arrange_resize_grips']:
            self.assertIn(string, CHROME)
    def test_no_new_rendering_dependencies(self):
        for term in ['QtWebEngine', 'QMovie', 'QMediaPlayer', 'GIF', 'FFmpeg']:
            self.assertNotIn(term, CHROME)
        self.assertIn('rlottie-python', (ROOT/'build-windows.bat').read_text())
    def test_mirroring_functions_preserved(self):
        code = ast.parse((ROOT/'engine.py').read_text(encoding='utf-8'))
        checks = {
            'binary': '071bca4cafc251a8b2e2f067b59bb79877ff39a5a133b624133c3488534a2720',
            'run': '01417b99ac47cb5be820ecd6901560b02340f449d7e6fbc677ac4007facbda86',
            'devices': '1d737f727752f6d5a0729d4785452b11ca7d053dc025a915e167deef16e5dae1',
            'command': '9adb4b00ae79fc3334345cf6213a29598f4f525d529982d424a0b4fe33516d95',
        }
        for name, expected in checks.items():
            function = next(n for n in code.body if isinstance(n, ast.FunctionDef) and n.name == name)
            fingerprint = hashlib.sha256(ast.dump(function, include_attributes=False).encode()).hexdigest()
            self.assertEqual(fingerprint, expected, name)
    def test_packaging_versions(self):
        self.assertIn('VERSION = "1.0.8.9-beta"', APP)
        self.assertIn('#define MyAppVersion "1.0.8.9"', (ROOT/'Flipmelon.iss').read_text())
        self.assertIn('Flipmelon_Setup_v1.0.8.9_NoTemp_UNSIGNED', (ROOT/'build-windows.bat').read_text())
if __name__=='__main__': unittest.main()
