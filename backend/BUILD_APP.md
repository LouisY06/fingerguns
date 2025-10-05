# 📦 Building FingerGuns as a macOS App

## Option 1: py2app (Recommended for macOS)

### Install py2app
```bash
pip install py2app
```

### Build the App
```bash
cd backend
python setup.py py2app
```

This creates:
- `dist/FingerGuns.app` - Your packaged app!
- `build/` - Temporary build files (can delete)

### Run the App
```bash
open dist/FingerGuns.app
```

Or drag it to your Applications folder!

### Clean Build (if you need to rebuild)
```bash
rm -rf build dist
python setup.py py2app
```

---

## Option 2: PyInstaller (Cross-platform)

### Install PyInstaller
```bash
pip install pyinstaller
```

### Build the App (macOS)
```bash
cd backend
pyinstaller --name="FingerGuns" \
            --windowed \
            --onefile \
            --add-data=".:." \
            --hidden-import=cv2 \
            --hidden-import=mediapipe \
            --hidden-import=numpy \
            --hidden-import=pyautogui \
            --hidden-import=pynput \
            leaning_control_system.py
```

This creates:
- `dist/FingerGuns.app` - Your packaged app!

### Run the App
```bash
open dist/FingerGuns.app
```

---

## Distributing the App

### Create a DMG (Disk Image) for Distribution

#### Method 1: Using create-dmg (recommended)
```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "FingerGuns" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "FingerGuns.app" 175 120 \
  --hide-extension "FingerGuns.app" \
  --app-drop-link 425 120 \
  "FingerGuns-1.0.0.dmg" \
  "dist/FingerGuns.app"
```

#### Method 2: Manual DMG creation
```bash
# Create DMG
hdiutil create -volname "FingerGuns" -srcfolder dist/FingerGuns.app -ov -format UDZO FingerGuns-1.0.0.dmg
```

### Zip for Distribution
```bash
cd dist
zip -r ../FingerGuns-1.0.0-macOS.zip FingerGuns.app
```

---

## Troubleshooting

### "App is damaged and can't be opened"
This happens because the app isn't code-signed. Users can fix it with:
```bash
xattr -cr /Applications/FingerGuns.app
```

Or right-click → Open → Open anyway

### Camera Permission Issues
Make sure the `NSCameraUsageDescription` is set in setup.py (already included).

### Missing Dependencies
If the app crashes, check console logs:
```bash
open dist/FingerGuns.app
# Check Console.app for errors
```

Rebuild with explicit includes:
```bash
# For py2app
python setup.py py2app --packages=cv2,mediapipe,numpy

# For PyInstaller
pyinstaller --hidden-import=missing_module leaning_control_system.py
```

### App is Too Large
The app will be large (~500MB+) due to MediaPipe and OpenCV. This is normal.

To reduce size:
- Use `--onedir` instead of `--onefile` with PyInstaller
- Remove unused dependencies from requirements.txt before building

---

## Code Signing (Optional, for Distribution)

If you want to distribute publicly without the "damaged" warning:

### 1. Get Apple Developer Account ($99/year)

### 2. Sign the App
```bash
codesign --deep --force --sign "Developer ID Application: Your Name" dist/FingerGuns.app
```

### 3. Notarize (for macOS 10.15+)
```bash
# Create DMG first
# Submit for notarization
xcrun notarytool submit FingerGuns-1.0.0.dmg \
  --apple-id "your@email.com" \
  --password "app-specific-password" \
  --team-id "TEAM_ID"

# Staple the ticket
xcrun stapler staple FingerGuns-1.0.0.dmg
```

---

## Creating an Icon (Optional)

### 1. Create icon.png (1024x1024)
Use any image editor

### 2. Convert to .icns
```bash
# Create iconset directory
mkdir icon.iconset

# Generate all required sizes
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png

# Create .icns
iconutil -c icns icon.iconset
```

Then update setup.py:
```python
'iconfile': 'icon.icns',
```

---

## Quick Start

**Simplest build:**
```bash
cd /Users/louisyu/fingerguns/backend
pip install py2app
python setup.py py2app
open dist/FingerGuns.app
```

**For distribution:**
```bash
cd dist
zip -r ../FingerGuns-macOS.zip FingerGuns.app
```

Upload `FingerGuns-macOS.zip` to your website/GitHub!

---

## File Sizes

- **Source code**: ~50 KB
- **Built .app**: 400-600 MB (includes Python, OpenCV, MediaPipe)
- **Zipped**: ~200-300 MB

This is normal for Python apps with computer vision libraries.
