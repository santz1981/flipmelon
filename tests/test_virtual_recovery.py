import json, os, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import engine
ROOT = Path(__file__).resolve().parent.parent
class VirtualRecoveryTests(unittest.TestCase):
    def test_v09_profile_exact(self):
        c=dict(mode='virtual', resolution='1920x1080', dpi=120, fullscreen=True)
        self.assertEqual(engine.command(c,'scrcpy','phone'),[
            'scrcpy','--serial','phone','--new-display=1920x1080/120','--no-vd-destroy-content','--fullscreen'])
    def test_macbook_profile(self):
        c=dict(mode='virtual', resolution='1920x1200', dpi=180, fullscreen=True)
        a=engine.command(c,'scrcpy','phone')
        self.assertIn('--new-display=1920x1200/180', a)
    def test_clean_session(self):
        c=dict(mode='virtual', resolution='1920x1080', dpi=120, fullscreen=True, clean_virtual=True)
        a=engine.command(c,'scrcpy','phone')
        self.assertNotIn('--no-vd-destroy-content',a)
        self.assertIn('--new-display=1920x1080/120',a)
    def test_no_hidden_decorations(self):
        for c in [dict(mode='virtual', resolution='1920x1080', dpi=120,fullscreen=True),
                  dict(mode='virtual', resolution='1920x1080', dpi=120, clean_virtual=True,fullscreen=True)]:
            a=engine.command(c,'scrcpy','phone')
            self.assertNotIn('--no-vd-system-decorations',a)
            self.assertNotIn('--start-app', ' '.join(a))
    def test_conventional_mirroring(self):
        a=engine.command(dict(mode='mirror',fullscreen=True),'scrcpy','phone')
        self.assertNotIn('--new-display', ' '.join(a))
        self.assertIn('--fullscreen',a)
    def test_no_os(self):
        code=(ROOT/'Flipmelon.py').read_text(encoding='utf-8')
        self.assertNotIn('import flipmelon_os',code)
        self.assertNotIn('import workspace',code)
        self.assertIn('Restaurar perfil v0.9',code)
    def test_assets(self):
        self.assertTrue((ROOT/'assets/animations/logo.json').exists())
        self.assertTrue((ROOT/'assets/installer-side.bmp').exists())
if __name__=='__main__': unittest.main()
