"""Checks the original Lottie integration cannot regress to GIF/MP4 or WebEngine."""
import unittest, ast, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STABLE=Path('/mnt/data/_integrate_stable/Flipmelon_v1082_Sem_WebEngine')
class NativeRLottie(unittest.TestCase):
    def test_renderer_is_original(self):
        text=(ROOT/'lottie_window.py').read_text(encoding='utf-8')
        ast.parse(text)
        self.assertIn('from rlottie_python import LottieAnimation',text)
        self.assertIn("'animations' / 'logo.json'",text)
        self.assertIn('elapsed * fps',text)
        self.assertIn('DURATION_MS = 5000',text)
        self.assertIn('FADE_MS = 850',text)
        self.assertIn('self._min_time_done and self._mirror_ready',text)
        self.assertNotIn('QWebEngine',text)
        self.assertNotIn('QMediaPlayer',text)
        self.assertNotIn('QMovie',text)
    def test_packaging(self):
        build=(ROOT/'build-windows.bat').read_text(encoding='utf-8')
        self.assertIn('rlottie-python',build)
        self.assertIn('--collect-all rlottie_python',build)
        self.assertIn('--exclude-module PySide6.QtWebEngineWidgets',build)
    def test_real_json(self):
        import json
        src=ROOT/'assets/animations/logo.json'
        info=json.loads(src.read_text(encoding='utf-8'))
        self.assertEqual(info['fr'],60)
        self.assertEqual((info['w'],info['h']),(1400,300))
        self.assertTrue((ROOT/'assets/animations/icon.json').exists())
    def test_mirroring_functions_unchanged(self):
        self.assertTrue((ROOT/'engine.py').is_file())
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
if __name__=='__main__':unittest.main()
