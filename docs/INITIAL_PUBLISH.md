# First publication on GitHub — step by step

## 1. Create the repository
1. Sign in to [GitHub](https://github.com).
2. Open [New repository](https://github.com/new).
3. Repository name: `flipmelon` (if available). Visibility: **Public**.
4. Description: `Open-source Android desktop companion for Windows, powered by scrcpy and native Lottie.`
5. **Do not** add a README, .gitignore, or license in the GitHub creation screen — this source package already includes them.
6. Click **Create repository**.

## 2. Upload the initial source

Extract this repository folder to a directory on your own Windows computer. Open PowerShell/Git Bash inside that folder and run the following commands, replacing `YOUR_GITHUB_USERNAME` with your actual GitHub username:

```bash
git init
git add .
git status
git commit -m "Initial open-source Flipmelon source"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/flipmelon.git
git push -u origin main
```

Before running `git add .`, ensure you are inside the **`flipmelon` source folder**, not a folder full of old installers or ZIPs. `git status` should not list `.exe`, `.dll`, `.bin`, secrets, machine settings or PyInstaller output.

If Git asks for authentication, follow the GitHub sign-in instructions. A GitHub password alone is not used for HTTPS Git authentication; use Git Credential Manager or other supported authentication.

## 3. Make it a useful open-source repository

- Enable **Issues** and optionally **Discussions**.
- Set Topics such as `android`, `scrcpy`, `python`, `pyside6`, `lottie`, `desktop-app`, `windows`, `open-source`.
- Add a short About description and optionally the project's verified website domain.
- Read and explicitly approve the proposed code license and brand policy before going public.
- Enable private vulnerability reporting if available.

## 4. Prepare the first GitHub Release

The last confirmed Windows working baseline is **v1.0.8.8**. The current source folder is **v1.0.8.9-beta**, which should **not** be advertised as stable before you personally test the final Windows build.

To release the current beta after validation, build it on Windows using `docs/BUILD_WINDOWS.md`, then:

- Open the repository → **Releases** → **Draft a new release**.
- Create tag `v1.0.8.9-beta.1` **only for a commit whose version and code match the build**.
- Use title `Flipmelon v1.0.8.9 Beta — Windows`.
- Select **Set as a pre-release**.
- Upload the portable ZIP and (optional) the ZIP containing the complete multi-file installer `.exe` **plus `.bin` files**.
- Include version highlights, installation instructions, known limitations, dependency attributions and checksums.

**Important:** Do not publish the older v1.0.8.8 binary under a v1.0.8.9 tag. Keep the source-to-binary version linkage exact.

## 5. Link the release to marketing

Once a **real public Release URL** exists, copy it into the draft Instagram, LinkedIn and Facebook copy in `../launch/POSTS_SOCIAIS.md`. Never publish a placeholder or an unverified download URL.
