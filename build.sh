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

echo "==> Creating DMG installer..."
DMG_PATH="dist/${APP_NAME}.dmg"
DMG_TMP="dist/${APP_NAME}-tmp.dmg"
DMG_STAGE="dist/dmg-stage"

# Build a staging folder with the app and an Applications symlink
rm -rf "$DMG_STAGE"
mkdir -p "$DMG_STAGE"
cp -R "$APP_PATH" "$DMG_STAGE/"
ln -s /Applications "$DMG_STAGE/Applications"

# Create a read/write DMG so we can position icons via AppleScript
hdiutil create \
    -volname "$APP_NAME" \
    -srcfolder "$DMG_STAGE" \
    -ov \
    -format UDRW \
    "$DMG_TMP"
rm -rf "$DMG_STAGE"

# Mount the r/w DMG
MOUNT_DIR=$(hdiutil attach "$DMG_TMP" -readwrite -noverify -noautoopen | \
    awk 'END {$1=$2=""; print substr($0,3)}' | xargs)

# Use AppleScript to position the app icon (left) and Applications link (right)
osascript << APPLESCRIPT
tell application "Finder"
    tell disk "$APP_NAME"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {400, 200, 900, 500}
        set theViewOptions to the icon view options of container window
        set arrangement of theViewOptions to not arranged
        set icon size of theViewOptions to 100
        set position of item "${APP_NAME}.app" of container window to {150, 150}
        set position of item "Applications" of container window to {350, 150}
        close
        open
        update without registering applications
        delay 2
    end tell
end tell
APPLESCRIPT

# Unmount, convert to compressed read-only, clean up
hdiutil detach "$MOUNT_DIR" -quiet
hdiutil convert "$DMG_TMP" -format UDZO -o "$DMG_PATH" -ov
rm -f "$DMG_TMP"

BUNDLE_SIZE=$(du -sh "$APP_PATH" | cut -f1)
DMG_SIZE=$(du -sh "$DMG_PATH" | cut -f1)
echo ""
echo "====================================================="
echo "  Build complete: $APP_PATH  ($BUNDLE_SIZE)"
echo "  DMG installer: $DMG_PATH  ($DMG_SIZE)"
echo "====================================================="
echo ""
echo "To test app:   open $APP_PATH"
echo "To test DMG:   open $DMG_PATH"
echo ""
echo "NOTE: On first launch on another Mac, right-click the app"
echo "      and choose Open, then click Open in the dialog."
echo "      This is a one-time Gatekeeper bypass (no Developer ID)."
