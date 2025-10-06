# 🎮 FingerGuns - CS:GO Gesture Control

Control CS:GO using hand gestures, head movements, and facial expressions!

## 🚀 Quick Start

### Installation

**Double-click**: `FingerGuns.command`

The launcher will:
1. Check if Python 3 is installed
2. Auto-install any missing dependencies
3. Launch FingerGuns automatically

That's it! 🎉

---

## 🎮 Controls

### Getting Started
1. A camera window will open showing your webcam
2. **Click on the camera window** (important!)
3. Press **`G`** to enable gesture controls
4. Start gaming!

### Right Hand (Gun Gesture)
- **Make gun gesture**: Index finger out, bottom 3 fingers curled
- **Index finger** = Aim/move cursor
- **Thumb DOWN** = Shoot (left click)
- **Thumb UP** = Ready to fire

### Head Movement (WASD)
- **Head FORWARD** = Move forward (S key)
- **Head BACKWARD** = Move backward (W key)  
- **Lean LEFT** = Strafe left (A key)
- **Lean RIGHT** = Strafe right (D key)

### Left Hand Gestures
- **Index finger only** = Jump (Space)
- **Pinky + Index + Thumb** = Switch to Knife (Q)
- **Pinky + Thumb** = Interact (E)
- **Index + Thumb** = Spray (T)

### Mouth
- **Open mouth** = Scope/Aim (right click held)
- **Close mouth** = Unscope

### Keyboard
- **`G`** = Toggle controls ON/OFF
- **`+` / `-`** = Increase/decrease sensitivity
- **`ESC`** = Quit

---

## 📋 Requirements

- **macOS** 10.14 or later
- **Python 3.8+** (download from [python.org](https://www.python.org/downloads/))
- **Webcam**
- **~500 MB** free space for dependencies

---

## 💡 Tips

- Position webcam at eye level for best tracking
- Ensure good lighting
- Keep hands visible in camera frame
- Make clear, distinct gestures
- Start with sensitivity around 0.9 (use +/- to adjust)
- Practice gestures before playing!

---

## 🐛 Troubleshooting

**"Python 3 not found"**
→ Download and install from [python.org](https://www.python.org/downloads/)

**"Permission denied"**
→ Right-click `FingerGuns.command` → Open → Open

**Camera not working**
→ Allow camera permission in System Settings → Privacy & Security → Camera

**Controls not responding**
→ Click on the camera window to give it focus first!

**'G' key doesn't work**
→ Make sure you clicked the camera window (not the terminal)

**Gestures not detected**
→ Ensure good lighting and hand is fully visible

---

## 🎯 Gesture Tips

**Gun Gesture (Right Hand):**
- Keep index finger straight and pointing
- Curl bottom 3 fingers tightly
- Thumb position controls shooting

**Left Hand Gestures:**
- Make gestures clear and distinct
- Hold for a moment for detection
- Return to neutral between gestures

**Movement:**
- Small head tilts for precise strafing
- Larger tilts for continuous movement
- Keep head centered when not moving

---

## 📁 Files Included

- `FingerGuns.command` - Double-click launcher
- `leaning_control_system.py` - Main application
- `requirements.txt` - Python dependencies
- `README.md` - This file

---

## 🔧 Advanced

### Manual Launch
```bash
python3 leaning_control_system.py
```

### Install Dependencies Manually
```bash
pip3 install -r requirements.txt
```

### Sensitivity Tuning
Default is 0.9. Press `+` or `-` while running to adjust.

---

## 📝 Credits

Created for CS:GO gesture control using:
- MediaPipe (hand & face tracking)
- OpenCV (camera feed)
- PyAutoGUI (input control)

---

## 🎉 Enjoy!

Have fun controlling CS:GO with your hands! 🎮👋

For issues or questions, visit: https://github.com/LouisY06/fingerguns



