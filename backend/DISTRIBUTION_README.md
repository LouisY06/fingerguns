# 📦 How to Distribute FingerGuns

The packaged `.app` has issues with OpenCV windows. Here's a better way to distribute:

## Recommended: Python Script Distribution

### What to Include

Create a zip file with these files:
```
FingerGuns-v1.0.zip
├── leaning_control_system.py
├── requirements.txt (create from current dependencies)
├── INSTALL.sh (installer script)
├── FingerGuns_Launcher.command (double-click launcher)
└── README.md (user instructions)
```

### Create the Distribution Package

```bash
cd /Users/louisyu/fingerguns/backend

# Create a clean copy
mkdir -p FingerGuns-Distribution
cp leaning_control_system.py FingerGuns-Distribution/
cp INSTALL.sh FingerGuns-Distribution/
cp FingerGuns_Launcher.command FingerGuns-Distribution/

# Create requirements.txt
echo "mediapipe>=0.10.0
opencv-python>=4.8.0
pyautogui>=0.9.54
numpy>=1.24.0
pynput>=1.7.6" > FingerGuns-Distribution/requirements.txt

# Create README
cat > FingerGuns-Distribution/README.md << 'EOF'
# 🎮 FingerGuns - CS:GO Gesture Control

Control CS:GO with hand gestures, head movements, and tongue!

## Installation

1. **Run the installer**:
   ```
   Double-click: INSTALL.sh
   ```
   This will install Python dependencies automatically.

2. **Launch FingerGuns**:
   ```
   Double-click: FingerGuns_Launcher.command
   ```

## Controls

- **G** - Toggle gesture controls ON/OFF
- **Right Hand**: Gun gesture (index out, other fingers curled)
  - Thumb down = shoot
  - Index finger = aim
- **Head**: Tilt for movement (WASD)
- **Left Hand**: Gestures for jump, knife, interact
- **Tongue**: Spray emote
- **ESC** - Quit

## Requirements

- macOS 10.14+
- Python 3.8+
- Webcam

Enjoy! 🎮
EOF

# Zip it up
cd ..
zip -r FingerGuns-v1.0.zip FingerGuns-Distribution/

echo "✓ Created: FingerGuns-v1.0.zip"
ls -lh FingerGuns-v1.0.zip
```

### User Experience

1. Download `FingerGuns-v1.0.zip`
2. Unzip
3. Double-click `INSTALL.sh` (one-time setup)
4. Double-click `FingerGuns_Launcher.command` to play

## Alternative: Just the Python Script

If users have Python already:

1. Share just `leaning_control_system.py`
2. They run:
   ```bash
   pip install mediapipe opencv-python pyautogui numpy pynput
   python3 leaning_control_system.py
   ```

## Why Not .app/.dmg?

OpenCV's `cv2.imshow()` doesn't work reliably in packaged macOS apps because:
- GUI frameworks conflict
- Window management issues
- PyInstaller bundle environment differences

The Python script approach is:
- ✅ More reliable
- ✅ Smaller file size
- ✅ Easier to update
- ✅ Better debugging

## For Hackathon Demo

Just run the Python script directly:
```bash
python3 backend/leaning_control_system.py
```

No packaging needed! 🎯
