# Third-party components and redistribution notices

Flipmelon is an independent GUI application and relies on external projects. **Do not represent these components as authored by Flipmelon.** Licenses below apply to the relevant third-party materials, regardless of the license chosen for Flipmelon code.

| Component | Used for | Known license / reference |
|---|---|---|
| [scrcpy](https://github.com/Genymobile/scrcpy) | Android screen mirroring / virtual display | Apache License 2.0 |
| [Android Debug Bridge (ADB)](https://developer.android.com/tools/adb) | Android device discovery and connection | See Android SDK/platform-tools distribution terms |
| [rlottie-python](https://pypi.org/project/rlottie-python/) | Python native Lottie playback | LGPL (as published on PyPI) |
| [Samsung/rlottie](https://github.com/Samsung/rlottie) | Native Lottie rendering engine | MIT and bundled-component notices; review exact distributed version |
| [PySide6 / Qt](https://www.qt.io/licensing/open-source-lgpl-obligations) | Desktop GUI | LGPL/GPL/commercial, depending on components and distribution |
| [FFmpeg](https://ffmpeg.org/legal.html) and [SDL](https://www.libsdl.org/license.php) | Runtime libraries in the official scrcpy Windows package | FFmpeg LGPL/GPL depending on build; SDL zlib |
| [Inno Setup](https://jrsoftware.org/isinfo.php) | Optional Windows installer build tool | Separate installer/compiler license |

## Release checklist — compliance

1. Do not commit third-party `.exe`/`.dll` binaries to Git just to make builds easier. The official scrcpy package is obtained by `scripts/get-scrcpy.ps1` with a pinned SHA-256 hash.
2. When distributing a compiled installer/portable ZIP, include the original scrcpy `LICENSE.txt` and all required third-party notices/source offers, including obligations associated with Qt/PySide6, rlottie-python, ADB, FFmpeg and SDL.
3. Verify the exact packaged Python wheels and DLLs. Their applicable license versions and any relinking/source-code requirements depend on the actual shipped binaries.
4. Do not remove copyright notices from third-party files.
5. Keep third-party attribution visible in the GitHub README and release notes.

**This document is a starting checklist, not a legal compliance certification.** Review all third-party redistribution requirements before publicly shipping the Windows installer.
