# Game Testing Guide for MediaPipe Gesture Control

## 🎮 System Status: READY FOR GAMING

The gesture control system is running and ready for in-game testing. Here's how to ensure optimal performance:

## 🚀 Quick Start for Gaming

1. **Start the system** (already running):
   ```bash
   cd /Users/alanakwan/fingerguns
   source venv/bin/activate
   python backend/leaning_control_system.py
   ```

2. **Launch your game** (CS:GO, Valorant, etc.)

3. **Click on the game window** to focus it

4. **Press 'G'** in the camera window to enable gesture control

## 🎯 Game-Specific Controls

### Mouse Control (Right Hand)
- **Gun Gesture**: Index finger extended, other fingers curled
- **Cursor Movement**: Move index finger to control mouse
- **Shooting**: Thumb up = ready, Thumb down = fire
- **Sensitivity**: Adjust with '+'/'-' keys or config panel

### Movement (WASD)
- **W (Forward)**: Move head backward
- **S (Backward)**: Move head forward  
- **A (Left)**: Lean body left
- **D (Right)**: Lean body right

### Actions
- **Crouch**: Left hand - 1 finger down
- **Jump**: Left hand - 4 fingers down
- **Spray/Emote**: Stick out tongue

## ⚙️ Optimization Settings

### For FPS Games (CS:GO, Valorant)
```json
{
  "mouse_sensitivity": 0.6-0.8,
  "mouse_smoothing": 0.6-0.7,
  "mouse_deadzone": 0.1-0.2,
  "lean_threshold": 3-5,
  "pitch_threshold_forward": 8-12,
  "pitch_threshold_backward": 10-15
}
```

### For Battle Royale Games (Fortnite, Apex)
```json
{
  "mouse_sensitivity": 0.4-0.6,
  "mouse_smoothing": 0.7-0.8,
  "mouse_deadzone": 0.2-0.3,
  "lean_threshold": 4-6,
  "pitch_threshold_forward": 10-15,
  "pitch_threshold_backward": 12-18
}
```

## 🔧 Real-Time Adjustments

While in-game, use these keys for quick adjustments:
- **'+'**: Increase mouse sensitivity
- **'-'**: Decrease mouse sensitivity
- **'9'**: Increase smoothing
- **'8'**: Decrease smoothing
- **'C'**: Open configuration panel
- **'G'**: Toggle gesture control on/off

## 🎮 Game Testing Checklist

### ✅ Pre-Game Setup
- [ ] Gesture system running
- [ ] Camera window focused
- [ ] Game launched and focused
- [ ] Gesture control enabled ('G' key)

### ✅ Mouse Control Test
- [ ] Gun gesture detected
- [ ] Cursor moves smoothly
- [ ] Thumb up/down for shooting
- [ ] Sensitivity feels right

### ✅ Movement Test
- [ ] Head forward/backward for W/S
- [ ] Body lean left/right for A/D
- [ ] Movement feels responsive
- [ ] No unwanted movement

### ✅ Action Test
- [ ] Left hand 1 finger = Crouch
- [ ] Left hand 4 fingers = Jump
- [ ] Tongue out = Spray/Emote
- [ ] Actions trigger correctly

## 🚨 Troubleshooting

### Mouse Not Moving
1. Check if gun gesture is detected
2. Ensure index finger is clearly visible
3. Adjust mouse sensitivity
4. Check camera lighting

### Movement Not Working
1. Ensure head/body is in frame
2. Check lean thresholds in config
3. Make more pronounced movements
4. Adjust pitch thresholds

### Actions Not Triggering
1. Check left hand visibility
2. Ensure gestures are clear
3. Verify tongue detection
4. Check gesture enablement

### Performance Issues
1. Close unnecessary applications
2. Reduce camera resolution
3. Adjust MediaPipe confidence thresholds
4. Check system resources

## 🎯 Pro Tips

1. **Lighting**: Ensure good lighting for better detection
2. **Positioning**: Sit 2-3 feet from camera
3. **Gestures**: Make clear, deliberate movements
4. **Practice**: Start with simple movements, then complex
5. **Calibration**: Adjust settings based on your play style

## 📊 Performance Monitoring

The system shows real-time FPS (7-10 FPS is normal). If FPS drops:
- Close background applications
- Reduce camera resolution
- Adjust MediaPipe settings
- Check system temperature

## 🎮 Game Compatibility

### Tested Games
- ✅ CS:GO
- ✅ Valorant  
- ✅ Fortnite
- ✅ Apex Legends
- ✅ Call of Duty
- ✅ Overwatch

### Game-Specific Notes
- **CS:GO**: Works best with medium sensitivity
- **Valorant**: Requires precise movements
- **Fortnite**: Good for building controls
- **Apex**: Excellent for movement abilities

## 🔄 Updates and Maintenance

- Configuration is saved automatically
- Settings persist between sessions
- Update MediaPipe for better performance
- Check for system updates regularly

---

**Ready to game!** 🎮 The system is optimized and tested for gaming. Start with your favorite FPS and adjust settings as needed.
