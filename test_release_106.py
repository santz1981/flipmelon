import unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import engine
ROOT=Path(__file__).resolve().parents[1]
class ReleaseTests(unittest.TestCase):
    def test_original_virtual(self):
        c={"mode":"virtual","resolution":"1920x1080","dpi":120,"fullscreen":True}
        self.assertEqual(engine.command(c,"scrcpy.exe","ABC"),["scrcpy.exe","--serial","ABC","--new-display=1920x1080/120","--no-vd-destroy-content","--fullscreen"])
    def test_alternative_dpi(self):
        c={"mode":"virtual","resolution":"1920x1080","dpi":284,"fullscreen":True}
        flags=engine.command(c,"scrcpy.exe","ABC")
        self.assertIn("--new-display=1920x1080/284",flags)
        self.assertNotIn("--no-vd-system-decorations",flags)
    def test_normal_mirroring(self):
        c={"mode":"mirror","fullscreen":True}
        self.assertEqual(engine.command(c,"scrcpy.exe","ABC"),["scrcpy.exe","--serial","ABC","--fullscreen"])
    def test_no_workspace_or_android_mutation(self):
        code=(ROOT/"Flipmelon.py").read_text(encoding="utf-8")
        self.assertNotIn("import flipmelon_os",code)
        self.assertNotIn('"settings", "put"',code)
        self.assertIn("def try_samsung_density",code)
    def test_installer_explicitly_unsigned(self):
        conf=(ROOT/"Flipmelon.iss").read_text(encoding="utf-8")
        self.assertIn("_UNSIGNED",conf)
        build=(ROOT/"build-windows.bat").read_text(encoding="utf-8")
        self.assertIn("Compress-Archive",build)
        self.assertIn("Portable_Windows.zip",build)
if __name__=="__main__":unittest.main()
