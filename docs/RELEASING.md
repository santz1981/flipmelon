# Release checklist (repeat for every new version)

## Before changing code
- [ ] Create a Git branch for the change.
- [ ] Keep the last confirmed Windows version available for rollback.
- [ ] Agree on release scope and bump the version consistently.

## Before creating binaries
- [ ] Verify all five languages (English first-run default) and the onboarding flow.
- [ ] Verify the original Lottie splash and that scrcpy still starts in parallel.
- [ ] Test mirror and virtual display on real hardware, when supported.
- [ ] Run unit tests and check `git status` for accidental files.
- [ ] Review third-party notices and bundled dependencies.

## Create binaries on Windows
- [ ] Run `scripts/get-scrcpy.ps1` to obtain the official SHA-256 verified scrcpy runtime.
- [ ] Run `build-windows.bat`.
- [ ] Test `dist\Flipmelon\Flipmelon.exe` before installing.
- [ ] Test the portable ZIP and installer on a clean installation where possible.
- [ ] Zip installer EXE and *all* BIN files into one package.
- [ ] Compute SHA-256 checksums of distribution ZIPs.

## Publish
- [ ] Commit and push the source to the `main` branch.
- [ ] Create a matching version tag and GitHub Release.
- [ ] Flag betas as **Pre-release**.
- [ ] Attach the portable Windows ZIP and optional full installer bundle ZIP.
- [ ] Publish release notes, known limitations, third-party notices and checksums.
- [ ] Copy the real GitHub Release URL to the website and social posts.

## After launch
- [ ] Monitor and respond to reproducible GitHub Issues.
- [ ] Correct the README and posts if new limitations are discovered.
- [ ] Never overwrite a released binary without changing the release version and checksums.
