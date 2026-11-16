<div align="center">
  <img src="assets/flipmelon-logo.png" alt="Flipmelon" width="330" />
  <h1>Flipmelon</h1>
  <p><strong>Use your Android phone on a bigger screen.</strong></p>
  <p>Windows companion application with guided setup, native Lottie splash, and scrcpy-powered Android mirroring.</p>
</div>

[Leia em português](docs/README.pt-BR.md) · [Build on Windows](docs/BUILD_WINDOWS.md) · [Contributing](CONTRIBUTING.md) · [Third-party notices](THIRD_PARTY_NOTICES.md)

## About

Flipmelon provides a guided desktop interface for connecting an Android phone to a computer via USB and using **scrcpy** for mirroring or a virtual display. Its original `logo.json` animation is played with **rlottie-python**. The application is written in Python with **PySide6**.

### Features

- Five-step Android/USB setup wizard, preceded by language selection.
- Five UI languages: **English (default)**, **Português**, **Русский**, **Español**, **Français**.
- Custom title bar for the settings/control window; the scrcpy window remains native.
- Mirroring and virtual display options (depending on Android device capabilities).
- Original vector Lottie startup animation, without Qt WebEngine.
- User preferences stored locally.

### Project status

- **v1.0.8.8**: last version reported working on Windows by the maintainer, with the native Lottie animation.
- **v1.0.8.9-beta**: source in this repository, including custom window controls and the language-first flow. **Windows release testing is pending.**
- Windows x64 is the initial release target. Linux is not yet covered by a verified release build.
- The Windows app is currently **unsigned**. Do not disable security protections if a build is blocked; report the error instead.

## Download for end users

Check **GitHub Releases** for a verified Windows package. A source-code ZIP is **not** the Windows installer.

No public Windows installer is bundled with the repository source. The project maintainer builds and verifies release binaries on Windows, then uploads the portable ZIP and/or installer package as Release assets.

## Build from source (Windows)

Requirements: Windows 10/11 x64, Python 3.11+, PowerShell, Internet to install Python dependencies, and (optionally) Inno Setup 6.

1. Clone or download the repository.
2. In PowerShell, run `powershell -ExecutionPolicy RemoteSigned -File scripts/get-scrcpy.ps1` to download the **official, checksum-verified scrcpy 5.0.1** Windows package. Alternatively, download the same archive from the official [scrcpy releases](https://github.com/Genymobile/scrcpy/releases) and place its contents in `vendor/windows/`.
3. Run `build-windows.bat` from the project folder.
4. Test `dist\Flipmelon\Flipmelon.exe` **before** creating or distributing a release.
5. Find the portable ZIP, and (if Inno Setup was found) the multi-file installer in `output\`.

**Important:** The current Inno Setup format uses `UseSetupLdr=no`. Its setup `.exe` must be shipped **together with all generated `.bin` files**. Zip the entire installer output set; do not upload the setup `.exe` alone. See [Windows build and publishing details](docs/BUILD_WINDOWS.md).

## Contribute

Bug reports, translations, accessibility improvements, and fixes are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

## Licenses and acknowledgements

The original Flipmelon **source code** is proposed under the [MIT License](LICENSE) (maintainer to approve before initial publication). The Flipmelon name, logo, and original artwork are not granted for unrelated branding or product endorsement by this license; see [BRANDING.md](BRANDING.md). Third-party components carry **their own** licenses, including scrcpy (Apache-2.0), rlottie-python (LGPL), PySide6/Qt, and the bundled scrcpy runtime dependencies. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Flipmelon is an independent project, **not affiliated with or endorsed by** Genymobile, Samsung, Google, or Qt.
