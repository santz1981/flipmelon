# Changelog

Dates below refer to project milestone documentation, not independently verified public GitHub release dates.

## [1.0.8.9-beta] — 2026-11-16 (release candidate, Windows testing pending)

- Custom dark 48px title bar for the settings/control window only.
- First-run language selection before Android setup; English default.
- Five UI locales: English, Portuguese, Russian, Spanish and French.
- Persistent language preference; fixes to reload chosen language.
- RLottie startup animation retained; scrcpy engine and native scrcpy window preserved.

## [1.0.8.8] — 2026-11-16 (validated locally on Windows)

- Native playback of the original `logo.json` using rlottie-python.
- Keeps the tested mirroring/virtual-display architecture without Qt WebEngine.
- Confirmed working after clean reinstall with the previous instance closed.

## Earlier development iterations

- Previous experimental splash approaches using GIF, PNG and MP4 were not retained due to quality/performance limitations.
