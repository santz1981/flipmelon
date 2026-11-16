"""Prevent loss of languages and regression of the RLottie integration."""
import ast
import json
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'Flipmelon.py').read_text(encoding='utf-8')
CHROME = (ROOT / 'window_chrome.py').read_text(encoding='utf-8')

class LocalizationTests(unittest.TestCase):
    def test_five_locales_complete_with_matching_keys(self):
        catalogs = {code: json.loads((ROOT/'locales'/f'{code}.json').read_text(encoding='utf-8'))
                    for code in ('pt','en','ru','es','fr')}
        keys = set(catalogs['pt'])
        self.assertGreater(len(keys), 120)
        for code, contents in catalogs.items():
            self.assertEqual(set(contents), keys, code)
            self.assertTrue(all(isinstance(x, str) and x.strip() for x in contents.values()), code)
            self.assertEqual(contents['ETAPA {n} DE 5'].count('{n}'), 1)

    def test_visible_static_texts_are_translated(self):
        tree = ast.parse(APP)
        keys = set(json.loads((ROOT/'locales'/'pt.json').read_text(encoding='utf-8')))
        names = {'label', 'make_button', 'page_start', 'QCheckBox'}
        missing=[]
        for call in (x for x in ast.walk(tree) if isinstance(x, ast.Call)):
            if isinstance(call.func, ast.Name) and call.func.id in names:
                args = call.args[:2] if call.func.id == 'page_start' else call.args[:1]
                for arg in args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        if len(arg.value)>2 and not arg.value.startswith(('pill', 'step')) and arg.value not in keys:
                            missing.append((call.lineno, arg.value))
        self.assertEqual(missing, [])

    def test_build_bundles_all_language_files(self):
        self.assertIn('--add-data "locales;locales"', (ROOT/'build-windows.bat').read_text())
        self.assertIn('language_combo', CHROME)
        self.assertIn('def change_language(self, code:', APP)
        self.assertIn('self.conf["language"]', APP)
        self.assertIn('engine.save(self.conf)', APP)


    def test_language_choice_is_first_screen_and_english_default(self):
        self.assertIn('self.create_language_screen()', APP)
        self.assertIn('self.root.setCurrentIndex(2)', APP)
        self.assertIn('self.continue_after_language', APP)
        self.assertIn('self.conf.get("language", "en")', APP)
        self.assertIn('self.timer.start(2600)', APP)
        self.assertIn('self._refresh_language_options()', APP)
        import sys
        sys.path.insert(0,str(ROOT))
        import engine, i18n
        self.assertEqual(engine.DEFAULT['language'], 'en')
        self.assertEqual(i18n.set_language('unknown'), 'en')
        self.assertEqual(i18n.set_language('ru'), 'ru')
        i18n.set_language('en')

    def test_saved_language_survives_engine_load(self):
        import sys, tempfile
        from unittest.mock import patch
        sys.path.insert(0,str(ROOT))
        import engine
        with tempfile.TemporaryDirectory() as work:
            from pathlib import Path
            path = Path(work)/'config.json'
            with patch.object(engine, 'CONFIG_FILE', path), patch.object(engine, 'LEGACY_FILE', Path(work)/'old.json'):
                for code in ('en','pt','ru','es','fr'):
                    data = engine.load()
                    data['language'] = code
                    engine.save(data)
                    self.assertEqual(engine.load()['language'], code)
                path.write_text('{"language":"unknown"}',encoding='utf-8')
                self.assertEqual(engine.load()['language'], 'en')

    def test_translation_runtime_fallback_and_prefix(self):
        import sys
        sys.path.insert(0,str(ROOT))
        import i18n
        try:
            for code in ('pt','en','ru','es','fr'):
                i18n.set_language(code)
                self.assertTrue(i18n.tr('Bem-vindo ao Flipmelon'))
                self.assertEqual(i18n.tr('NON_TRANSLATABLE_TOKEN'), 'NON_TRANSLATABLE_TOKEN')
            i18n.set_language('en')
            self.assertEqual(i18n.tr('Não foi possível iniciar o scrcpy: file not found'),
                             'Could not start scrcpy: file not found')
        finally:
            i18n.set_language('en')

if __name__ == '__main__': unittest.main()
