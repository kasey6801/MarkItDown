# MarkItDown - Workflow Documentation

---

## Executive Overview

**MarkItDown Local Frontend** is a local web app that converts documents to Markdown using Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) library. It accepts PDF, DOCX, PPTX, XLSX, XLS, EPUB, CSV, JSON, XML, HTML, ZIP, images, audio, and URLs (including YouTube transcripts), with a 100 MB upload limit. All conversion happens on the user's machine; no file or URL is sent to an external server.

The app is a single Python file (`app.py`, ~1,150 lines): a Flask backend plus the entire HTML/CSS/JS interface embedded as one string constant, with `marked.js` inlined for offline preview rendering. Files are converted in memory (`BytesIO`), never written to disk. A heartbeat/watchdog pair shuts the server down automatically when the browser tab closes. The app is packaged with PyInstaller as a macOS `.app`/`.dmg` (built locally by `build.sh`) and a Windows `.exe` (built by GitHub Actions). Current releases: macOS v0.42.1, Windows v0.43.0 (pre-release, ships app v0.42.1). `app.py` is the single source of truth for the app version.

---

## How This Project Was Built

Prompts below are reconstructed from commit history; the original session transcripts were not retained.

### Step 1: Initial release v0.42 (2026-03-30)

**User prompt** *(reconstructed)*:
> Build a local frontend for Microsoft's MarkItDown library: a Flask app with drag-and-drop upload, URL conversion, live Markdown preview, and packaging as a macOS app.

**Claude actions** (commit `c4d0194`):
- Wrote `app.py`: Flask backend with `/convert` (multipart upload) and `/convert-url` routes, single embedded HTML/CSS/JS interface, in-memory `BytesIO` conversion, inlined `marked.js` for offline preview
- Added `MarkItDown.spec` (PyInstaller COLLECT + BUNDLE) and `build.sh` (clean, bundle, ad-hoc sign)
- Added `README.md` and MIT `LICENSE`

### Step 2: Tab/server lifecycle, v0.42.1 (2026-03-30)

**User prompt** *(reconstructed)*:
> The app should quit cleanly: add a Quit button, and make the server exit automatically when the browser tab is closed.

**Claude actions** (commits `e15d417`, `c0666e2`):
- Added the `/quit` route and a Quit button in the UI
- Added a JS heartbeat (POST `/heartbeat` every 5 s) and a watchdog daemon thread that calls `os._exit(0)` after 12 s without a heartbeat
- Added the `/stopped` page and updated the README for v0.42.1

### Step 3: Drag-to-install DMG (2026-03-30)

**User prompt** *(reconstructed)*:
> Distribute the macOS build as a proper DMG installer with the drag-to-Applications layout.

**Claude actions** (commit `ef07b7d`):
- Extended `build.sh` to build a DMG: staging folder with an Applications symlink, AppleScript window/icon layout, UDZO compression
- Documented the install steps (right-click, Open on first launch, no Developer ID)

### Step 4: App-reopen fix (2026-03-31)

**User prompt** *(reconstructed)*:
> The app fails to reopen after it has been quit or killed by the watchdog. Fix it.

**Claude actions** (commits `8a95d2d`, `25b982f`):
- Fixed the reopen error that followed a watchdog or quit `os._exit(0)`
- Updated the README version references and screenshot

### Step 5: Windows build (2026-03-31)

**User prompt** *(reconstructed)*:
> Add a Windows 11 version built as a single .exe, using GitHub Actions so no local Windows machine is needed.

**Claude actions** (commit `9727f29`):
- Added `MarkItDown_win.spec` (PyInstaller onefile: `a.binaries` and `a.datas` passed directly into `EXE()`, no COLLECT/BUNDLE)
- Added `.github/workflows/build-windows.yml`: Windows runner, Python 3.12, builds and uploads `MarkItDown.exe` as an artifact

### Step 6: CI hardening, five iterations (2026-03-31)

**User prompt** *(reconstructed)*:
> The release upload step keeps failing on the Windows runner. Get the workflow to create the GitHub Release and upload the EXE reliably.

**Claude actions** (commits `3388421`, `b44e91e`, `f442ad6`, `d7a4110`, `c887fbb`):
- Opted the runner into Node.js 24
- Made the workflow create the GitHub Release if it does not exist before uploading
- Fixed a `/dev/null` incompatibility, then rewrote the release step in native PowerShell
- Granted `contents: write` permission so the workflow can create releases

### Step 7: Windows documentation pass (2026-03-31 to 2026-04-01)

**User prompt** *(reconstructed)*:
> Document how to install the Windows app and how to build the EXE from source. Clarify which versions are released on each platform.

**Claude actions** (commits `abf0ad5`, `2a3a84a`, `942994d`, `808e7e0`, `7ac745a`):
- Added Windows install and build-from-source instructions to the README
- Reorganized the README around numbered install options with the macOS app recommended
- Pointed the macOS DMG link at the v0.42.1 release and marked the Windows version as pre-release

### Step 8: CLAUDE.md added (2026-04-01 to 2026-04-06)

**User prompt** *(reconstructed)*:
> Add a CLAUDE.md so future Claude Code sessions understand the architecture and build process.

**Claude actions** (commits `772f7cf`, `2104d5f`):
- Wrote `CLAUDE.md`: run/build commands, the single-file architecture and its key design decisions, the route table, the two-spec PyInstaller policy, and the release process
- Follow-up README touch-up

### Step 9: Monkey plush app icon (2026-04-19)

**User prompt** *(reconstructed)*:
> Give the app a custom icon: the monkey plush design, generated programmatically so it is reproducible from source.

**Claude actions** (commit `a235afe`):
- Added `make_icon.py` (Pillow drawing of the monkey-plush icon, 1024x1024 RGBA)
- Wired the PNG-to-`.icns` pipeline (`sips` + `iconutil`) into `build.sh` and the spec

### Step 10: Documentation and Flask standards (2026-04-19)

**User prompt** *(reconstructed)*:
> Record the ClaudeDev documentation standard and the standard features every Flask app must have.

**Claude actions** (commit `54911d6`):
- Added the Documentation Standard and Flask App Standard Features sections to `CLAUDE.md` (Quit button, heartbeat, watchdog, `debug=False`, `host='0.0.0.0'`)

### Step 11: Maintenance pass (2026-07-14)

**User prompt:**
> This session will focus on updating the project in the folder CC_Markdown. Review the program.

**Claude actions:**
- Reviewed the project and removed leftovers: legacy `markitdown_app.py`, a stale git worktree and branch, an unreachable `break` in the watchdog, a wrong docstring in `make_icon.py`
- Removed a plaintext GitHub token from the local Claude Code settings allowlist, replaced by `gh` CLI usage
- Added `requirements.txt` pinned to the known-working environment (including `lxml` and `Pillow`, which the PyInstaller specs need but markitdown 0.0.2 does not pull in) and wired it into the README, `CLAUDE.md`, `build.sh`, and the CI workflow
- Documented the Python matrix (minimum 3.10, local 3.14, Windows CI 3.12) and the version truth model (`app.py` defines the app version; release tags are per-platform)
- Created this workflow document

---

## User Guide

### Install (macOS, recommended)

1. Download `MarkItDown.dmg` from the [v0.42.1 release](https://github.com/kasey6801/MarkItDown/releases/tag/v0.42.1).
2. Drag **MarkItDown.app** into **Applications**, then eject the DMG.
3. First launch only: right-click the app, choose **Open**, then click **Open** (the app is not signed with an Apple Developer ID).
4. The browser opens `http://127.0.0.1:5001` automatically.

### Install (Windows, pre-release)

1. Download `MarkItDown.exe` from the [v0.43.0 release](https://github.com/kasey6801/MarkItDown/releases/tag/v0.43.0).
2. Double-click to launch. If SmartScreen appears: **More info**, then **Run anyway** (one time).

### Run from source

```bash
cd CC_Markdown
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Using the app

- Drag a file onto the drop zone (or click to browse), or paste a URL and click **Convert**.
- The left pane shows raw Markdown; the right pane shows the rendered preview.
- The stats bar shows characters, words, lines, and an estimated token range.
- **Copy** puts the Markdown on the clipboard; **Download** saves a `.md` file.
- Quit with the **Quit** button, by closing the tab (the app exits itself within about 12 seconds), or with `Ctrl+C` in Terminal when running from source.

### Troubleshooting

| Problem | Fix |
|---|---|
| Port 5001 already in use (macOS) | `lsof -ti :5001 \| xargs kill -9`, then restart |
| Port 5001 already in use (Windows) | `netstat -ano \| findstr :5001`, note the PID, then `taskkill /PID <pid> /F` |
| App will not open on another Mac | Right-click, **Open**, **Open** (one-time Gatekeeper step) |
| SmartScreen blocks the EXE | **More info**, then **Run anyway** |
| Conversion returns empty output | Check the error box in the UI for the full Python traceback |
