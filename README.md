# ⚡ MarkItDown Local Frontend

**v0.42** — Convert documents, PDFs, Office files & more to Markdown — locally.

A self-contained web app built on Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) library. All conversion happens on your machine — no files or URLs are ever sent to an external server.

---

## Features

- **Drag-and-drop or browse** to upload files
- **URL conversion** — paste a YouTube link or any web page URL
- **Live Markdown preview** alongside the raw output
- **Copy to clipboard** or **download as `.md`**
- **Stats bar** — characters, words, lines, and estimated token range
- **Quit button** — shuts down the server cleanly from the browser

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

## Option 1 — Run as a macOS App (recommended)

A pre-built `MarkItDown.app` is included in `dist/`. No Python installation required.

### Steps

1. Download or clone this repository.
2. Open `dist/` in Finder.
3. **Right-click** `MarkItDown.app` → **Open** → click **Open** in the dialog.
   > This one-time step is required because the app is not signed with an Apple Developer ID. After the first launch you can double-click as normal.
4. Your default browser opens automatically to `http://127.0.0.1:5001`.
5. To quit, click the **Quit** button in the top-right corner of the UI.

### Requirements

- macOS 12 (Monterey) or later
- Apple Silicon (arm64) or Intel Mac

---

## Option 2 — Run from Source (Python)

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

To stop, click the **Quit** button in the UI, or press `Control + C` in Terminal.

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

## Option 3 — Build the macOS App Yourself

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
5. Report the bundle size and location

Output: `dist/MarkItDown.app` (~166 MB, all dependencies bundled)

> **First launch on another Mac:** Right-click → Open → Open (one-time Gatekeeper bypass). This is expected for apps without an Apple Developer ID.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "Port 5001 already in use" | Run `lsof -ti :5001 \| xargs kill -9` then restart |
| App won't open on another Mac | Right-click → Open → Open (one-time Gatekeeper step) |
| "command not found: pip" | Use `python3 -m pip install ...` instead |
| Xcode prompt on macOS | Click Install, wait for it to finish, re-run `pip install` |
| Conversion returns empty output | Check the error box in the UI for the full Python traceback |

---

## Project structure

```
CC_Markdown/
├── app.py              # Single-file Flask app (HTML/CSS/JS embedded)
├── MarkItDown.spec     # PyInstaller build configuration
├── build.sh            # Build script (clean → bundle → sign)
├── dist/
│   └── MarkItDown.app  # Pre-built macOS application
└── .venv/              # Python virtual environment (not committed)
```

---

## License

MIT — see [LICENSE](LICENSE).

Built on [Microsoft MarkItDown](https://github.com/microsoft/markitdown) (MIT).
