# ⚡ MarkItDown Local Frontend

**v0.43.0** — Convert documents, PDFs, Office files & more to Markdown — locally. Available for macOS and Windows.

A self-contained web app built on Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) library. All conversion happens on your machine — no files or URLs are ever sent to an external server.

<img width="1834" height="1454" alt="2026-03-31 17 23 39" src="https://github.com/user-attachments/assets/522d8f44-e24d-4f5d-919f-90c39fe50672" />

---

## Features

- **Drag-and-drop or browse** to upload files
- **URL conversion** — paste a YouTube link or any web page URL
- **Live Markdown preview** alongside the raw output
- **Copy to clipboard** or **download as `.md`**
- **Stats bar** — characters, words, lines, and estimated token range
- **Quit button** — shuts down the server and shows a clean stopped page
- **Auto-quit on tab close** — closing the browser tab automatically exits the app

### Supported formats

| Category | Formats |
|---|---|
| Documents | PDF, DOCX, PPTX, XLSX, XLS, EPUB |
| Data | CSV, JSON, XML |
| Web | HTML, YouTube URLs, web pages |
| Archives | ZIP |
| Images | JPG, PNG |
| Audio | WAV, MP3 |

**Max file size:** 100 MB

---

## Option 1 — Run as a Windows App (recommended)

Download `MarkItDown.exe` from the [Releases](https://github.com/kasey6801/MarkItDown/releases) page. No Python installation required.

### Steps

1. Download `MarkItDown.exe` from the latest release.
2. Double-click `MarkItDown.exe` to launch it.
   > **Windows SmartScreen warning:** Click **More info** → **Run anyway**. This one-time step is required because the app is not code-signed. After the first launch you can double-click as normal.
3. Your default browser opens automatically to `http://127.0.0.1:5001`.
4. To quit, click the **Quit** button in the top-right corner of the UI, or simply close the browser tab — the app exits automatically.

### Requirements

- Windows 10 or Windows 11 (64-bit)

---

## Option 2 — Run as a macOS App (recommended)

Download the `MarkItDown.dmg` installer from the [v0.42.1 Release](https://github.com/kasey6801/MarkItDown/releases/tag/v0.42.1) page. No Python installation required.

### Steps

1. Download `MarkItDown.dmg` from the [v0.42.1 release](https://github.com/kasey6801/MarkItDown/releases/tag/v0.42.1).
2. Double-click the DMG to open it.
3. Drag **MarkItDown.app** (left) into the **Applications** folder (right).
4. Eject the DMG.
5. Open **Applications** in Finder and **right-click** `MarkItDown.app` → **Open** → click **Open** in the dialog.
   > This one-time step is required because the app is not signed with an Apple Developer ID. After the first launch you can double-click as normal.
6. Your default browser opens automatically to `http://127.0.0.1:5001`.
7. To quit, click the **Quit** button in the top-right corner of the UI, or simply close the browser tab — the app exits automatically.

### Requirements

- macOS 12 (Monterey) or later
- Apple Silicon (arm64) or Intel Mac

---

## Option 3 — Run from Source (Python)

Use this if you want to modify the app or the pre-built `.app` doesn't work on your system.

### Requirements

- macOS 12 or later (also works on Windows)
- Python 3.10 or higher

Check your Python version in Terminal:
```bash
python3 --version
```

If you have 3.9 or lower, download the latest Python from [python.org](https://www.python.org/downloads/).

### One-time setup (macOS)

Open **Terminal** (`Cmd + Space` → type Terminal → press Enter) and run each command:

```bash
# 1. Navigate to the project folder
cd /path/to/CC_Markdown

# 2. Create a virtual environment
python3 -m venv .venv

# 3. Activate it (your prompt will show (.venv) when active)
source .venv/bin/activate

# 4. Install dependencies
pip install "markitdown[all]" flask
```

> **Tip:** If you see an Xcode prompt, click Install and wait for it to finish, then re-run the `pip install` command.

### Running the app

```bash
cd /path/to/CC_Markdown
source .venv/bin/activate
python app.py
```

The app starts a local server and opens `http://127.0.0.1:5001` in your browser automatically.

To stop, click the **Quit** button in the UI, close the browser tab, or press `Control + C` in Terminal.

### One-time setup (Windows)

Open **Command Prompt** (`Win + R` → type `cmd` → Enter):

```bat
cd C:\path\to\CC_Markdown
python -m venv .venv
.venv\Scripts\activate
pip install "markitdown[all]" flask
```

> **Note:** If Python is not found, re-run the installer from [python.org](https://www.python.org/downloads/) and check **"Add Python to PATH"**.

Run:
```bat
python app.py
```

---

## Option 4 — Build the Windows EXE Yourself

Use this to rebuild `MarkItDown.exe` after making changes to `app.py`.

### Requirements

- A GitHub account with a fork of this repository (the build runs in GitHub Actions on a Windows runner — no local Windows machine needed)
- Alternatively: a Windows machine with Python 3.10+ and `pip install pyinstaller`

### Build via GitHub Actions

1. Push your changes to your repository.
2. Go to **Actions** → **Build Windows EXE** → **Run workflow**.
3. Download `MarkItDown-Windows-x64.zip` from the completed run's artifacts.
4. Extract the zip — `MarkItDown.exe` is inside.

### Build locally on Windows

Open **Command Prompt** and run:

```bat
cd C:\path\to\CC_Markdown
python -m venv .venv
.venv\Scripts\activate
pip install "markitdown[all]" flask pyinstaller
pyinstaller MarkItDown_win.spec --noconfirm
```

Output: `dist\MarkItDown.exe` (single self-contained executable, ~120 MB)

---

## Option 5 — Build the macOS App Yourself

Use this to rebuild `MarkItDown.app` after making changes to `app.py`.

### Additional requirement

```bash
pip install pyinstaller
```

### Build

```bash
bash build.sh
```

The script will:
1. Kill any running instance on port 5001
2. Clean previous build artifacts
3. Run PyInstaller with `MarkItDown.spec`
4. Ad-hoc sign the `.app` bundle
5. Create a `MarkItDown.dmg` installer with a drag-to-Applications layout
6. Report the bundle and DMG size and location

Output: `dist/MarkItDown.app` (~166 MB) and `dist/MarkItDown.dmg` (~90 MB)

> **First launch on another Mac:** Right-click → Open → Open (one-time Gatekeeper bypass). This is expected for apps without an Apple Developer ID.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "Port 5001 already in use" (macOS) | Run `lsof -ti :5001 \| xargs kill -9` then restart |
| "Port 5001 already in use" (Windows) | Run `netstat -ano \| findstr :5001`, note the PID, then `taskkill /PID <pid> /F` |
| Windows SmartScreen blocks the EXE | Click **More info** → **Run anyway** (one-time, no certificate) |
| App didn't quit after closing tab | The watchdog allows 12 s after the last heartbeat — wait a moment |
| App won't open on another Mac | Right-click → Open → Open (one-time Gatekeeper step) |
| "command not found: pip" | Use `python3 -m pip install ...` instead |
| Xcode prompt on macOS | Click Install, wait for it to finish, re-run `pip install` |
| Conversion returns empty output | Check the error box in the UI for the full Python traceback |

---

## Project structure

```
CC_Markdown/
├── app.py                  # Single-file Flask app (HTML/CSS/JS embedded)
├── MarkItDown.spec         # PyInstaller config — macOS .app bundle
├── MarkItDown_win.spec     # PyInstaller config — Windows .exe (onefile)
├── build.sh                # macOS build script (clean → bundle → sign → DMG)
├── .github/
│   └── workflows/
│       └── build-windows.yml  # GitHub Actions workflow — builds Windows EXE
├── dist/
│   └── MarkItDown.app      # Pre-built macOS application
└── .venv/                  # Python virtual environment (not committed)
```

---

## License

MIT — see [LICENSE](LICENSE).

Built on [Microsoft MarkItDown](https://github.com/microsoft/markitdown) (MIT).
