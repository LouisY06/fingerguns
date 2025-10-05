# 📦 Distribution Guide

## For Users (Download & Install)

### Installation
1. Download `FingerGuns-macOS.zip`
2. Unzip the file (double-click it)
3. Drag `FingerGuns.app` to your Applications folder
4. Open FingerGuns from Launchpad or Applications

### First Time Setup
macOS may show a security warning because the app isn't code-signed.

**If you see "App is damaged and can't be opened":**
1. Open Terminal
2. Run this command:
```bash
xattr -cr /Applications/FingerGuns.app
```
3. Try opening the app again

**Or:**
- Right-click the app → Open → Open anyway

### Camera Permission
The first time you open the app, macOS will ask for camera permission. Click "OK" to allow.

### Controls
- Press **'G'** to toggle controls ON/OFF
- Press **ESC** or click the red ❌ button to quit
- Press **+/-** to adjust sensitivity

---

## For Developers (Creating Distribution Package)

### Build the App
```bash
cd backend
./build_app.sh
```

### Create Distribution ZIP
```bash
cd dist
zip -r ../FingerGuns-macOS.zip FingerGuns.app
```

### Upload
Upload `FingerGuns-macOS.zip` to:
- GitHub Releases
- Your website download page
- Google Drive / Dropbox

### File Sizes
- Built .app: ~400-600 MB
- Zipped: ~200-300 MB

This is normal for Python apps with OpenCV and MediaPipe.

---

## Optional: Code Signing (For Public Distribution)

To avoid the "damaged app" warning, you need an Apple Developer account ($99/year).

### 1. Sign the App
```bash
codesign --deep --force --sign "Developer ID Application: Your Name" dist/FingerGuns.app
```

### 2. Verify Signature
```bash
codesign --verify --verbose dist/FingerGuns.app
```

### 3. Create DMG (Optional)
```bash
brew install create-dmg

create-dmg \
  --volname "FingerGuns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "FingerGuns.app" 175 120 \
  --hide-extension "FingerGuns.app" \
  --app-drop-link 425 120 \
  "FingerGuns-1.0.0.dmg" \
  "dist/FingerGuns.app"
```

### 4. Notarize (macOS 10.15+)
```bash
xcrun notarytool submit FingerGuns-1.0.0.dmg \
  --apple-id "your@email.com" \
  --password "app-specific-password" \
  --team-id "TEAM_ID" \
  --wait

xcrun stapler staple FingerGuns-1.0.0.dmg
```

---

## Support

If users have issues:
1. Check camera permissions in System Settings → Privacy & Security → Camera
2. Make sure they ran the `xattr -cr` command
3. Check if their macOS version is 10.15+ (Catalina or newer)

