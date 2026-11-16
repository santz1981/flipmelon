"""Protect against the specific "5s black screen then launch scrcpy" regression."""
import ast, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'Flipmelon.py').read_text(encoding='utf-8')
SPLASH = (ROOT / 'lottie_window.py').read_text(encoding='utf-8')
class ParallelSplash(unittest.TestCase):
    def test_syntax(self):
        ast.parse(APP)
        ast.parse(SPLASH)
    def test_scrcpy_launch_is_released_after_overlay_is_shown(self):
        b = APP[APP.index('    def show_mirror_opening(self):'):APP.index('    def mirror_window_ready(self,')]
        self.assertLess(b.index('opening.show_for_screen'), b.index('worker.launch_allowed.set()'))
        self.assertNotIn('opening.finished.connect(lambda: worker.launch_allowed.set()', b)
    def test_visible_scrcpy_window_and_5_seconds_are_required(self):
        self.assertIn('self.window_ready.emit(hwnd)', APP)
        self.assertIn('self._min_time_done', SPLASH)
        self.assertIn('self._mirror_ready', SPLASH)
        self.assertIn('QPropertyAnimation', SPLASH)
        self.assertIn('self._fade.setDuration(FADE_MS)', SPLASH)
    def test_timeouts_do_not_leave_overlay_up(self):
        self.assertIn('self.window_wait_timeout.emit()', APP)
        self.assertIn('QTimer.singleShot(23000, self._watchdog)', SPLASH)
    def test_original_command_not_modified(self):
        import sys
        sys.path.insert(0, str(ROOT))
        import engine
        conf = dict(mode='virtual',resolution='1920x1080',dpi=120,fullscreen=True)
        self.assertEqual(engine.command(conf,'scrcpy','SERIAL'),
                         ['scrcpy','--serial','SERIAL','--new-display=1920x1080/120',
                          '--no-vd-destroy-content','--fullscreen'])
    def test_setup_reopens_wizard(self):
        self.assertIn('"--setup" in sys.argv or not self.conf.get("onboarding_complete", False)', APP)
    def test_version_consistent(self):
        self.assertIn('VERSION = "1.0.8.9-beta"', APP)
        self.assertIn('1.0.8', (ROOT/'Flipmelon.iss').read_text(encoding='utf-8'))
if __name__ == '__main__': unittest.main()
