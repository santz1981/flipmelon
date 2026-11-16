# Build and release on Windows

## Prerequisites

- Windows 10/11 x64.
- Python 3.11+ (`py --version`), Git, PowerShell.
- Internet access to install Python wheels and download scrcpy.
- Optional: Inno Setup 6 to create the Windows installer; the portable ZIP can be built without it.

## 1. Obtain dependencies

Clone this repository then open PowerShell in the project directory.

```powershell
powershell -ExecutionPolicy RemoteSigned -File scripts/get-scrcpy.ps1
```

The script downloads **scrcpy v5.0.1 Windows x64** directly from its official GitHub release and checks the published SHA-256 before extracting it to `vendor\windows`. The complete third-party runtime is **not kept in Git**. Other Python build dependencies are installed by the next step.

## 2. Compile the application

```bat
build-windows.bat
```

This installs PySide6, PyInstaller and rlottie-python and builds a one-directory application. Expected outputs:

- `dist\Flipmelon\Flipmelon.exe` — portable executable (must stay with the files in its directory)
- `output\Flipmelon_v1.0.8.9_Portable_Windows.zip` — complete portable distribution
- `output\Flipmelon_Setup_v1.0.8.9_NoTemp_UNSIGNED.exe` **plus its generated `.bin` files**, if Inno Setup is installed

## 3. Smoke test the application

1. Close any older Flipmelon and scrcpy processes before testing/installing.
2. Run `visualizar_primeira_tela.bat` to preview the initial language selection. The default is English for first-time users.
3. Check all five languages and the complete Android onboarding.
4. Verify the native `logo.json` animation at the correct speed without GIF/MP4/Qt WebEngine.
5. Verify connecting your phone, regular mirroring and virtual display when supported by your phone.
6. Check custom window minimize/maximize/drag/resize, including 125%/150% scaling and a second display when available.
7. Run the automated tests: `py -m unittest discover -s tests -v`.
8. Do not bypass Windows policy blocks. Capture the error and check whether the old process is still running.

## 4. Package for GitHub Releases

**Recommended:** publish the complete portable ZIP.

**For the installer:** `UseSetupLdr=no` makes the installer **multi-file**. Zip the installer `.exe` and **all** adjacent `.bin` files together, for example `Flipmelon_v1.0.8.9_Windows_Setup_Package.zip`. Uploading only the setup `.exe` will break installation.

Add a SHA-256 file (PowerShell):

```powershell
Get-FileHash -Algorithm SHA256 'output\Flipmelon_v1.0.8.9_Portable_Windows.zip'
```

Keep third-party license files in the distributed portable or installer runtime and review the obligations summarized in `THIRD_PARTY_NOTICES.md` (including Qt/PySide6, RLottie, FFmpeg and ADB).

## 5. Release tags and versions

This repository currently contains **v1.0.8.9-beta** source, not yet signed off as stable on Windows. Until fully tested, use a pre-release tag such as `v1.0.8.9-beta.1` rather than marking it stable.

A version bump requires updating **together**:

- `VERSION` in `Flipmelon.py`.
- `MyAppVersion` and `OutputBaseFilename` in `Flipmelon.iss`.
- Product names in `build-windows.bat`.
- `README.md` status and `CHANGELOG.md`.
- Version expectations in the existing tests.

When a new version is ready, push the code, tag it, and upload that version's Windows artifacts under **Releases → Draft a new release**.

## 6. Later automation

Windows builds can eventually be automated with GitHub Actions. Do this only after the manual build is reproducible, dependency licenses and checksums have been verified, and tests pass on a clean Windows machine. Signed releases require a separate code-signing process.
