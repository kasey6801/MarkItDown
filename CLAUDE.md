# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
source .venv/bin/activate
python app.py
```

Opens automatically at `http://127.0.0.1:5001`. Stop with the Quit button in the UI, closing the browser tab, or `Ctrl+C`.

## Building

### macOS `.app` + `.dmg`
```bash
bash build.sh
```
Requires `.venv` with `pip install -r requirements.txt` (pinned; includes PyInstaller and Pillow). Outputs `dist/MarkItDown.app` and `dist/MarkItDown.dmg`.

### Windows `.exe`
Triggered via GitHub Actions (`.github/workflows/build-windows.yml`) on tag push or manual dispatch. To build locally on Windows:
```bat
.venv\Scripts\activate
pyinstaller MarkItDown_win.spec --noconfirm
```
Outputs `dist\MarkItDown.exe` (single self-contained file).

### Dependencies

`requirements.txt` is the dependency source of truth (runtime and build tooling, pinned to the known-working versions). Python: minimum 3.10, local development on 3.14, Windows CI on 3.12. The CI Python is the known-working Windows build version; validate with a manual `workflow_dispatch` run before changing it.

## Architecture

The app is intentionally a single file (`app.py`, ~1150 lines). There are no templates directory, static assets, or separate modules.

**Key design decisions:**

- **Entire HTML/CSS/JS UI** is embedded as a raw string constant `HTML` (lines 164–1088). `marked.js` is inlined inside that string for offline use. When editing the frontend, work inside this string.
- **`MarkItDown` is instantiated once at module level** (`md_converter = MarkItDown()`) and reused across all requests — not per-request.
- **File conversion uses in-memory `BytesIO`** — files are never written to disk. `stream.name` is set to the original filename so MarkItDown can detect the file type.
- **Watchdog thread** (`_watchdog()`) monitors browser heartbeats (POST `/heartbeat` every 5 s from JS). If no heartbeat arrives for 12 s, it calls `os._exit(0)`. This is what closes the app when the browser tab is closed.
- **`debug=False` is required** — Flask's debug reloader spawns a second process, which breaks PyInstaller bundles. Do not enable debug mode.
- **`host='0.0.0.0'`** is intentional — required on macOS Sequoia where `localhost` may resolve to `::1` instead of `127.0.0.1`.

**Flask routes:**

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Serves the embedded HTML UI |
| `/convert` | POST | Accepts multipart file upload, returns `{"markdown": "..."}` |
| `/convert-url` | POST | Accepts `{"url": "..."}`, returns `{"markdown": "..."}` |
| `/quit` | POST | Calls `os._exit(0)` after redirecting browser to `/stopped` |
| `/stopped` | GET | Static "app has stopped" page |
| `/heartbeat` | POST | Resets the watchdog timer |

## PyInstaller specs

Two specs exist — do not merge them:

- `MarkItDown.spec` — macOS: uses `COLLECT` + `BUNDLE` pattern, produces `.app` bundle with `info_plist`
- `MarkItDown_win.spec` — Windows: onefile mode, passes `a.binaries` and `a.datas` directly into `EXE()`, no `COLLECT`/`BUNDLE`

Both use `upx=False` — UPX corrupts Python extension modules (`.dylib`/`.pyd`) on both platforms.

## Releasing

- macOS releases (`MarkItDown.dmg`) are built locally with `bash build.sh` and attached to the GitHub release manually. Current macOS release: **v0.42.1**.
- Windows releases (`MarkItDown.exe`) are built automatically by GitHub Actions on tag push. The workflow creates the release if it doesn't exist, then uploads the EXE. Current Windows release: **v0.43.0**.
- To trigger a Windows release: `git tag vX.Y.Z && git push origin vX.Y.Z`
- The app version displayed in the UI is defined in `app.py` (the header `Version:` line and the `#version` element in the embedded HTML). `app.py` is the single source of truth for the app version. Release tags are per-platform packaging events and may differ from the app version (the Windows v0.43.0 release ships app v0.42.1).

## Documentation Standard

Every project in `ClaudeDev/` should have:
- **`README.md`** — project overview, features, setup instructions, file structure
- **`MarkItDown_WORKFLOW.md`** — executive overview, step-by-step build log (user prompts + Claude actions), user guide. Workflow files are named `<ProjectName>_WORKFLOW.md`.

Follow the format established in `CC_9to5_AI/WORKFLOW.md`.
Create or update these files whenever a significant feature is added or the project is first set up.

## Flask App Standard Features

Every Flask app in `ClaudeDev/` **must** include:
- **Quit button** — visible in the UI (top-right), sends `POST /quit` → `os._exit(0)`
- **Heartbeat** — JS sends `POST /heartbeat` every 5 s via `setInterval`
- **Watchdog thread** — daemon thread checks heartbeat; calls `os._exit(0)` if no heartbeat received for 12 s (frees the port when the browser tab is closed)
- **`debug=False`** — required for PyInstaller compatibility
- **`host='0.0.0.0'`** — required on macOS Sequoia (localhost may resolve to `::1`)
