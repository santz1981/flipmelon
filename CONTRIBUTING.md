# Contributing to Flipmelon 🍈

Thank you for your interest! Contributions are welcome, including UI fixes, accessibility, translations and Windows build improvements.

## Before proposing a change

- Read `README.md` and `docs/BUILD_WINDOWS.md`.
- Open an Issue for major changes before investing in a large implementation.
- Keep the **scrcpy process and its native window** separate from the custom settings window.
- Preserve the **original `assets/animations/logo.json`** and native RLottie playback (no GIF/MP4 conversion).
- Language selection comes before onboarding; English is the fallback default; maintain all five locale files.
- Do not commit build output, bundled vendor binaries, API keys, user settings or personal device identifiers.

## Development and checks

1. Set up Python 3.11+ on Windows; download verified scrcpy binaries with `scripts/get-scrcpy.ps1` if testing the full app.
2. Install dependencies with `py -m pip install PySide6 rlottie-python pyinstaller`.
3. Run tests: `py -m unittest discover -s tests -v`.
4. Build with `build-windows.bat` and manually validate the first-run language selector, 5-step onboarding, RLottie splash and actual mirroring.
5. Submit a pull request with a short explanation, screenshots only if they do not expose device/user information, and a test plan.

## Languages

Locale files live at `locales/en.json`, `pt.json`, `ru.json`, `es.json`, and `fr.json`. Translation keys currently use the original Portuguese strings. Confirm all five UI translations for any newly added labels.

## Pull request checklist

- [ ] Tests passed
- [ ] Five-language flow verified for affected screens
- [ ] RLottie/scrcpy engine unchanged unless explicitly required
- [ ] No third-party binaries, tokens, private data or build artifacts committed
- [ ] Windows smoke test documented when behavior changes
