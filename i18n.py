"""Runtime Portuguese-source localization for Flipmelon UI.

All five locales are packaged as JSON. Untranslated tokens fall back to the
original Portuguese string instead of crashing the app. Language changes are
explicit and persist in config.json via the main window. English is the default.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

LANGUAGES = (("en", "English"), ("pt", "Português"), ("ru", "Русский"),
             ("es", "Español"), ("fr", "Français"))
CODES = {code for code, _ in LANGUAGES}
_ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
_CATALOGS = {}
_current = "en"


def set_language(code: str) -> str:
    global _current
    _current = code if code in CODES else "en"
    return _current


def language() -> str:
    return _current


def catalog(code: str) -> dict[str, str]:
    if code not in _CATALOGS:
        try:
            path = _ROOT / "locales" / f"{code}.json"
            _CATALOGS[code] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _CATALOGS[code] = {}
    return _CATALOGS[code]


def tr(portuguese: str) -> str:
    value = str(portuguese)
    if _current == "pt":
        return value
    translations = catalog(_current)
    translated = translations.get(value)
    if translated is not None:
        return translated
    # Error detail is OS-provided, keep it intact after translating prefix.
    prefix = "Não foi possível iniciar o scrcpy: "
    if value.startswith(prefix):
        return translations.get(prefix, prefix) + value[len(prefix):]
    return value
