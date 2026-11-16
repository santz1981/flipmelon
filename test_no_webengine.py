"""Regression test: Qt WebEngine was introduced after working v0.9.0."""
import unittest, ast
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class NoWebEngineRegression(unittest.TestCase):
    def test_splash_is_native(self):
        code=(ROOT/'lottie_window.py').read_text(encoding='utf-8')
        ast.parse(code)
        self.assertIn('class LottieFullscreen(QWidget)',code)
        self.assertIn('QPropertyAnimation',code)
        self.assertNotIn('QWebEngine',code)
    def test_build_excludes_webengine(self):
        build=(ROOT/'build-windows.bat').read_text(encoding='utf-8')
        self.assertIn('--exclude-module PySide6.QtWebEngineWidgets',build)
        self.assertNotIn('--hidden-import PySide6.QtWebEngineWidgets',build)
        self.assertNotIn('prepare_lottie.py',build)
        self.assertNotIn('PySide6-Addons pyinstaller',build)
    def test_original_animation_files_preserved_for_future(self):
        self.assertTrue((ROOT/'assets/animations/logo.json').is_file())
        self.assertTrue((ROOT/'assets/animations/icon.json').is_file())
if __name__=='__main__':unittest.main()
