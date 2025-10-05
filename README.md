# MediaPipe Gesture Control System

A real-time gesture control system using MediaPipe for hands, pose, and face detection. Control games and applications using natural gestures and body movements.

## Features

- **Hand Gesture Control**: Gun gesture for mouse control, thumb for shooting
- **Body Movement**: Head pose for forward/backward, body lean for left/right movement
- **Left Hand Gestures**: Finger gestures for crouch/jump actions
- **Tongue Detection**: Spray emote activation
- **Interactive UI Overlay**: Real-time configuration and help panels
- **Configurable Settings**: Adjustable sensitivity, smoothing, and thresholds

## Project Structure

```
fingerguns/
├── backend/
│   ├── leaning_control_system.py    # Main application
│   └── ui/
│       ├── __init__.py
│       ├── overlay.py               # UI overlay rendering
│       └── config_manager.py        # Configuration management
├── gesture_config.json              # User configuration
├── requirements.txt                 # Python dependencies
└── venv/                           # Virtual environment
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fingerguns
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application**:
   ```bash
   python backend/leaning_control_system.py
   ```

2. **Basic Controls**:
   - Press `G` to toggle gesture control on/off
   - Press `C` to open configuration panel
   - Press `H` to open help panel
   - Press `M` to open gesture mapping panel
   - Press `Q` or `ESC` to quit

3. **Configuration Panel**:
   - Use arrow keys or WASD to navigate
   - Press `Enter` to edit selected setting
   - Use arrow keys to adjust values
   - Press `Enter` again to finish editing

## Gesture Controls

### Right Hand (Gun Control)
- **Gun Gesture**: Index finger extended, other fingers curled
- **Thumb Up**: Ready to shoot
- **Thumb Down**: Fire weapon
- **Index Finger**: Controls mouse cursor

### Left Hand (Action Gestures)
- **One Finger**: Press `Ctrl` (Crouch)
- **Four Fingers**: Press `Space` (Jump)

### Body Movement
- **Head Forward**: Press `S` (Move forward)
- **Head Backward**: Press `W` (Move backward)
- **Lean Left**: Press `A` (Move left)
- **Lean Right**: Press `D` (Move right)

### Tongue
- **Tongue Out**: Press `T` (Spray emote)

## Configuration

The system uses `gesture_config.json` for configuration. Key settings include:

- `mouse_sensitivity`: Mouse movement sensitivity (0.1-5.0)
- `mouse_smoothing`: Mouse movement smoothing (0.1-1.0)
- `mouse_deadzone`: Mouse dead zone (0.0-2.0)
- `lean_threshold`: Body lean sensitivity (1.0-20.0)
- `pitch_threshold_forward`: Head forward threshold (1.0-30.0)
- `pitch_threshold_backward`: Head backward threshold (1.0-30.0)

## Requirements

- Python 3.9-3.12
- OpenCV
- MediaPipe
- PyAutoGUI
- pynput
- macOS: Quartz framework

## Troubleshooting

1. **Camera not working**: Ensure camera permissions are granted
2. **Gesture detection issues**: Adjust lighting and ensure clear view of hands/face
3. **Performance issues**: Reduce camera resolution or adjust MediaPipe confidence thresholds
4. **Configuration not saving**: Check file permissions for `gesture_config.json`

## Development

The project is modularized with separate UI and configuration management:

- `backend/leaning_control_system.py`: Main application logic
- `backend/ui/overlay.py`: UI rendering and interaction
- `backend/ui/config_manager.py`: Configuration management

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
