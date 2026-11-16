<div align="center">

<img src="assets/flipmelon-logo.png" alt="Flipmelon logo" width="340" />

### Your Android phone. A bigger screen.

Open-source Android mirroring for **Windows and Linux Mint**, powered by [scrcpy](https://github.com/Genymobile/scrcpy).

[![Windows x64](https://img.shields.io/badge/Windows-x64-DBFF00?style=flat-square&labelColor=111111)](https://github.com/santz1981/flipmelon/releases/tag/v1.0.8.9-beta.1) [![Linux Mint x64](https://img.shields.io/badge/Linux_Mint-x64-DBFF00?style=flat-square&labelColor=111111)](https://github.com/santz1981/flipmelon/releases/tag/v1.0.8.9-beta.1) [![Beta 1](https://img.shields.io/badge/Release-v1.0.8.9--beta.1-DBFF00?style=flat-square&labelColor=111111)](https://github.com/santz1981/flipmelon/releases/tag/v1.0.8.9-beta.1) [![MIT](https://img.shields.io/badge/Code-MIT-DBFF00?style=flat-square&labelColor=111111)](LICENSE)

[![Download for Windows](https://img.shields.io/badge/Download_for_Windows-Setup_Beta-DBFF00?style=for-the-badge&logo=windows11&logoColor=111111)](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_v1.0.8.9_Windows_Setup_COMPLETE.zip)
[![Download for Linux Mint](https://img.shields.io/badge/Download_for_Linux_Mint-DEB_Beta-DBFF00?style=for-the-badge&logo=linux&logoColor=111111)](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_1.0.8.9_Beta1-2_amd64.deb)

**[Windows Portable](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_v1.0.8.9_Portable_Windows.zip)** · **[Linux ZIP](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_1.0.8.9_Linux.zip)** · **[Release notes](https://github.com/santz1981/flipmelon/releases/tag/v1.0.8.9-beta.1)** · **[Português](docs/README.pt-BR.md)**

</div>

> **Beta:** v1.0.8.9-beta.1 is available for Windows and Linux Mint. The Linux `.deb` was installed and tested by the maintainer on Linux Mint x86-64. Other Linux distributions are not yet verified. Windows binaries are **not code-signed**; do not disable system protections to run them.

## About Flipmelon

Flipmelon helps you connect an Android phone to Windows or Linux Mint over USB, with a guided setup and [scrcpy](https://github.com/Genymobile/scrcpy) mirroring or a virtual display on supported devices. Built with Python and PySide6, it is an independent project — **not Samsung DeX for PC**.

## Features

- **Language first:** English is the default for new installations; select a language before any Android configuration.
- **Five UI languages:** English, Português, Русский, Español and Français.
- **Five-step wizard:** Android developer options, USB debugging, device authorization and display preferences.
- **Custom settings window:** Flipmelon-branded title bar for setup and configuration; the scrcpy mirror window remains native.
- **Display choices:** regular screen mirroring or a virtual Android display when supported.
- **Original Lottie splash:** the animation in assets/animations/logo.json runs via RLottie, not GIF, MP4 or Qt WebEngine.
- **Saved preferences:** local language and display settings.

## Download and install

| Download | Description |
| --- | --- |
| **[Windows Setup — Beta](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_v1.0.8.9_Windows_Setup_COMPLETE.zip)** | ZIP with an installer EXE and two BIN files |
| **[Windows Portable — Beta](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_v1.0.8.9_Portable_Windows.zip)** | No installation required |
| **[Linux Mint DEB — Beta](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_1.0.8.9_Beta1-2_amd64.deb)** | Installer for Linux Mint x86-64 |
| **[Linux ZIP — Beta](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_1.0.8.9_Linux.zip)** | Linux package archive |
| **[Windows SHA-256 checksums](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/SHA256SUMS.txt)** | Verify Windows downloads |
| **[Linux SHA-256 checksums](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_Linux_SHA256SUMS.txt)** | Verify Linux downloads |

**Requirements:** Windows 10/11 x64 or Linux Mint x86-64 (tested), an Android phone, a USB data cable, and USB debugging enabled. Virtual display support varies by phone; other Linux distributions have not yet been verified.

### Install on Windows

1. Download the [Windows Setup ZIP](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_v1.0.8.9_Windows_Setup_COMPLETE.zip) and **extract all files into the same folder**.
2. Keep the setup **EXE and both BIN files together**; do not run the EXE inside the ZIP.
3. Close older Flipmelon and scrcpy processes.
4. Run **Flipmelon_Setup_v1.0.8.9_NoTemp_UNSIGNED.exe**.
5. Open Flipmelon, choose a language (English is the default), and follow the Android setup wizard.

### Windows portable version

Extract the [Portable Windows ZIP](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_v1.0.8.9_Portable_Windows.zip), open the **Flipmelon** folder, and run **Flipmelon.exe**. Keep the whole directory, including **_internal**, intact.

**Security:** Windows binaries are unsigned and may trigger system security warnings. Do not disable protections. Report warnings through [GitHub Issues](https://github.com/santz1981/flipmelon/issues).

### Install on Linux Mint (x86-64)

1. Download the [Linux Mint .deb installer](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_1.0.8.9_Beta1-2_amd64.deb).
2. Double-click the downloaded `.deb` file and install it using the Mint package manager.
3. Launch **Flipmelon** from the applications menu.
4. Connect the phone over USB, enable USB debugging and authorize the connection on the phone.

Alternatively, open a terminal in the folder containing the downloaded file and run:

```bash
sudo apt install ./Flipmelon_1.0.8.9_Beta1-2_amd64.deb
```

The package has been tested by the maintainer on Linux Mint. It remains a **beta**; other Linux distributions are not yet verified. [Linux ZIP](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_1.0.8.9_Linux.zip) and [Linux SHA-256 checksums](https://github.com/santz1981/flipmelon/releases/download/v1.0.8.9-beta.1/Flipmelon_Linux_SHA256SUMS.txt) are also available.

## Preview

<div align="center">
  <img src="assets/flipmelon-splash.png" alt="Official Flipmelon splash artwork, not an app screenshot" width="680" />
  <p><sub>Official splash artwork — not an application screenshot. Real setup and mirroring screenshots will be added after UI verification.</sub></p>
</div>

## Build from source

**Windows source build:** Windows 10/11 x64, Python 3.11+, PowerShell and internet access are required; Inno Setup 6 is optional.

1. Clone/download this repository.
2. Follow [Windows build instructions](docs/BUILD_WINDOWS.md) to download the checksum-verified scrcpy runtime using **scripts/get-scrcpy.ps1**.
3. Run **build-windows.bat**, then test **dist/Flipmelon/Flipmelon.exe**.
4. Find distribution files in **output/**.

A Linux Mint x86-64 `.deb` is available in the beta release and was tested by the maintainer. Linux packaging instructions are not yet documented in this repository. See [release checklist](docs/RELEASING.md).

## Status and roadmap

- **v1.0.8.8:** last Windows version reported working by the maintainer, including the RLottie splash.
- **v1.0.8.9-beta.1:** Windows and Linux Mint builds published. The Linux Mint `.deb` was tested by the maintainer. Further verification is required before a stable release.
- **Next:** verify the beta, add real UI screenshots, improve accessibility and repeatable builds.

See [CHANGELOG.md](CHANGELOG.md) and [all releases](https://github.com/santz1981/flipmelon/releases).

## Contributing

Contributions, translations and bug reports are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md), check [Issues](https://github.com/santz1981/flipmelon/issues), or see [SECURITY.md](SECURITY.md).

## License and acknowledgements

The original Flipmelon source code is published under the [MIT License](LICENSE). The [branding policy](BRANDING.md) is a separate proposal awaiting final owner review. Third-party software has its own license and redistribution requirements; read [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Flipmelon is independent and is not affiliated with or endorsed by Samsung, Google, Genymobile or Qt.
