import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import engine
R = Path(__file__).resolve().parents[1]
class InstallerFallback(unittest.TestCase):
    def test_no_temp_setup_loader(self):
        iss=(R/'Flipmelon.iss').read_text(encoding='utf8')
        self.assertIn('UseSetupLdr=no',iss)
        self.assertIn('PrivilegesRequired=lowest',iss)
        self.assertIn('OutputBaseFilename=Flipmelon_Setup_v1.0.8.9_NoTemp_UNSIGNED',iss)
    def test_original_virtual_display(self):
        flags=engine.command({'mode':'virtual','resolution':'1920x1080','dpi':120,'fullscreen':True},'scrcpy.exe','DEVICE')
        self.assertIn('--new-display=1920x1080/120',flags)
        self.assertNotIn('--no-vd-system-decorations',flags)
    def test_script_checks_build(self):
        b=(R/'build-windows.bat').read_text(encoding='utf8')
        self.assertIn('Flipmelon_Setup_v1.0.8.9_NoTemp_UNSIGNED.exe',b)
        self.assertIn('Compress-Archive',b)
if __name__=='__main__':unittest.main()
