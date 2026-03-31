#!/usr/bin/env bash
set -euo pipefail

APP_NAME="MarkItDown"
SPEC_FILE="MarkItDown.spec"
VENV_PYINSTALLER=".venv/bin/pyinstaller"

echo "==> Checking environment..."
if [ ! -f "$VENV_PYINSTALLER" ]; then
    echo "ERROR: .venv not found. Run setup first:"
    echo "  python3 -m venv .venv"
    echo "  .venv/bin/pip install 'markitdown[all]' flask pyinstaller"
    exit 1
fi

if [ ! -f "$SPEC_FILE" ]; then
    echo "ERROR: $SPEC_FILE not found."
    exit 1
fi

echo "==> Stopping any running instance on port 5001..."
lsof -ti :5001 | xargs kill -9 2>/dev/null || true

echo "==> Cleaning previous builds..."
# Clear extended attributes first so macOS doesn't block deletion of .DS_Store etc.
xattr -cr build/ dist/ 2>/dev/null || true
rm -rf build/ dist/

echo "==> Running PyInstaller (this may take a few minutes)..."
"$VENV_PYINSTALLER" "$SPEC_FILE" --noconfirm

APP_PATH="dist/${APP_NAME}.app"
if [ ! -d "$APP_PATH" ]; then
    echo "ERROR: Expected $APP_PATH was not created. Check PyInstaller output above."
    exit 1
fi

echo "==> Ad-hoc signing the app bundle..."
# Remove all xattrs first to avoid stale quarantine flags
xattr -cr "$APP_PATH"
# Sign the Python framework explicitly first — it has a python.org Team ID that
# conflicts with ad-hoc signing if left as-is. Must be done before the deep sign.
PYTHON_FW="$APP_PATH/Contents/Frameworks/Python.framework/Versions/3.14/Python"
if [ -f "$PYTHON_FW" ]; then
    codesign --force --sign - "$PYTHON_FW"
fi
# Sign the full bundle (no --options runtime — hardened runtime enforces Team ID
# matching which breaks when the bundled Python.framework was signed by python.org)
codesign --deep --force --sign - "$APP_PATH"

echo "==> Verifying signature..."
codesign --verify --deep --strict "$APP_PATH" && echo "    Signature OK"

BUNDLE_SIZE=$(du -sh "$APP_PATH" | cut -f1)
echo ""
echo "====================================================="
echo "  Build complete: $APP_PATH  ($BUNDLE_SIZE)"
echo "====================================================="
echo ""
echo "To test:       open $APP_PATH"
echo ""
echo "NOTE: On first launch on another Mac, right-click the app"
echo "      and choose Open, then click Open in the dialog."
echo "      This is a one-time Gatekeeper bypass (no Developer ID)."
