# 🎮 FingerGuns

**Computer-vision-powered FPS control** - Play first-person shooter games using only your head and hands. No mouse, keyboard, or controller required.

Built with MediaPipe hand & head tracking, powered by a standard webcam.

🏆 **1st Place Winner** at Columbia Divhacks 2025

---

## 🚀 Quick Setup

### Prerequisites
- **Python 3.8+** (Python 3.12 recommended)
- **macOS** (10.15+)
- **Webcam**

### Installation

1. **Download the latest release**
   - Go to [Releases](https://github.com/LouisY06/fingerguns/releases)
   - Download `FingerGuns-Release.zip`
   - Extract the zip file

2. **Double-click `FingerGuns.command`**
   - The launcher will automatically install dependencies and start the app

3. **If macOS blocks the app:**
   - Go to **System Settings** → **Privacy & Security**
   - Scroll down and click **"Open Anyway"**
   - Double-click `FingerGuns.command` again

That's it! 🎉

---

## 🎮 How to Use

1. **Launch the program** - A camera window will open showing your webcam feed
2. **Click on the camera window** (important for keyboard input to work!)
3. **Press `G`** to toggle gesture controls ON/OFF
4. **Start playing** your favorite FPS game!

### Controls

**Right Hand (Gun Gesture):**
- 👉 Index finger extended, other fingers curled = Aim mode active
- 👆 Move index finger = Control cursor/aim
- 👍 Thumb up = Ready
- 👎 Thumb down = Shoot

**Head Movement (WASD):**
- 🔺 Head forward = Move forward (W)
- 🔻 Head backward = Move backward (S)
- ◀️ Lean left = Strafe left (A)
- ▶️ Lean right = Strafe right (D)

**Left Hand Gestures:**
- ☝️ Index finger only = Jump (Space)
- 🤘 Pinky + Index + Thumb = Knife (Q)
- 👌 Pinky + Thumb = Interact (E)

**Keyboard Shortcuts:**
- `G` = Toggle controls ON/OFF
- `+`/`-` = Adjust mouse sensitivity
- `ESC` = Quit

---



FingerGuns uses a unique dual-threaded architecture:

- **Computer Vision Thread (30 FPS)**: MediaPipe processes hand and head tracking
- **Cursor Control Thread (120 Hz)**: High-frequency interpolation for smooth cursor movement

This architecture reduces latency to **8-10ms** and provides fluid, responsive control by continuously interpolating micro-movements between CV frames.

We use the macOS **Quartz** library to generate low-level mouse input, bypassing synthetic input filters that most FPS games use to block simulated controls.

The interpolation uses a **fractional drain model** (α=0.15), where each cursor update applies 15% of the remaining delta, creating exponentially smoothed motion.

---

## 🎯 Tips for Best Performance

- Position webcam at eye level
- Ensure good, even lighting
- Keep hands fully visible within camera frame
- Make clear, distinct gestures
- Calibrate sensitivity with `+`/`-` keys to match your preference
- For best results, use a 1080p webcam

---

## 🧑‍💻 Team

Built by:
- **Louis Yu**
- **Chuhan Wang**
- **Felix Fan**
- **Alana Kwan**


---

## 🤝 Contributing

Contributions welcome! Feel free to open issues or submit PRs.

---

## 🐛 Troubleshooting

**Controls not responding?**
→ Make sure to click on the camera window first!

**Camera not working?**
→ Grant camera permission in System Settings → Privacy & Security → Camera

**Laggy performance?**
→ Close other applications using the camera, ensure good lighting

**"Damaged app" error (macOS)?**
→ Run: `xattr -cr /Applications/FingerGuns.app`

---

**Enjoy gaming with FingerGuns!** 🎮👋
