import unittest, ast
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CODE = (ROOT / "Flipmelon.py").read_text(encoding="utf-8")
ISS = (ROOT / "Flipmelon.iss").read_text(encoding="utf-8")
BUILD = (ROOT / "build-windows.bat").read_text(encoding="utf-8")
class Onboarding(unittest.TestCase):
    def test_python_syntax(self):
        ast.parse(CODE)
    def test_setup_run_parameter(self):
        self.assertIn('Parameters: "--setup"', ISS)
        self.assertIn('Flags: nowait postinstall skipifsilent', ISS)
    def test_setup_forces_first_page_even_after_config_saved(self):
        self.assertIn('self.show_setup = "--setup" in sys.argv or not self.conf.get("onboarding_complete", False)', CODE)
        self.assertIn('self.goto_step(0)', CODE)
    def test_step_four_checks_authorization_but_does_not_jump_steps(self):
        self.assertIn('self.next_button.setEnabled(index != 3 or self.authorized())', CODE)
        self.assertIn('def restart_guide(self):', CODE)
        self.assertIn('Refazer passo a passo', CODE)
    def test_version_consistency(self):
        self.assertIn('VERSION = "1.0.8.9-beta"', CODE)
        self.assertIn('#define MyAppVersion "1.0.8.9"', ISS)
        self.assertIn('Flipmelon_Setup_v1.0.8.9_NoTemp_UNSIGNED', BUILD)
    def test_no_os_reintroduced(self):
        self.assertNotIn('import flipmelon_os', CODE)
if __name__ == '__main__': unittest.main()
