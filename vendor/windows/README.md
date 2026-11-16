# Windows vendor runtime (not tracked)

This folder is populated locally with the **official scrcpy v5.0.1 win64 release archive** and its ADB/FFmpeg/SDL runtime dependencies. These files are intentionally excluded from Git source control.

From the repository root in Windows PowerShell:

```powershell
powershell -ExecutionPolicy RemoteSigned -File scripts/get-scrcpy.ps1
```

The script downloads from `github.com/Genymobile/scrcpy`, pins the version and verifies the published SHA-256 before copying files. `LICENSE.txt` from the archive is retained in the runtime package.

Do not commit your local vendor runtime to Git. Review `THIRD_PARTY_NOTICES.md` before distributing compiled releases.
