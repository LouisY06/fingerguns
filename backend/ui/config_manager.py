"""
Configuration Manager for MediaPipe Gesture Control
Handles loading, saving, and updating configuration settings
"""

import json
import os


class ConfigManager:
    """Manages configuration for the gesture control system"""
    
    def __init__(self, config_file="gesture_config.json"):
        """Initialize configuration manager"""
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default"""
        default_config = {
            "mouse_sensitivity": 0.5,
            "mouse_smoothing": 0.7,
            "mouse_deadzone": 0.1,
            "lean_threshold": 3,
            "pitch_threshold_forward": 8,
            "pitch_threshold_backward": 12,
            "gestures": {
                "left_hand_one_finger": {"action": "key_press", "key": "ctrl", "enabled": True},
                "left_hand_four_fingers": {"action": "key_press", "key": "space", "enabled": True},
                "right_hand_gun": {"action": "mouse_control", "enabled": True},
                "right_hand_thumb": {"action": "mouse_click", "button": "left", "enabled": True},
                "head_forward": {"action": "key_hold", "key": "s", "enabled": True},
                "head_backward": {"action": "key_hold", "key": "w", "enabled": True},
                "body_lean_left": {"action": "key_hold", "key": "a", "enabled": True},
                "body_lean_right": {"action": "key_hold", "key": "d", "enabled": True},
                "tongue_out": {"action": "key_press", "key": "t", "enabled": True}
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                print(f"Configuration loaded from {self.config_file}")
                return config
            else:
                self.save_config(default_config)
                print(f"Default configuration created and saved to {self.config_file}")
                return default_config
        except Exception as e:
            print(f"Error loading config: {e}, using defaults")
            return default_config
    
    def save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_config(self):
        """Get current configuration"""
        return self.config
    
    def update_config(self, updates):
        """Update configuration with new values"""
        for key, value in updates.items():
            if '.' in key:
                # Handle nested keys like 'gestures.left_hand_one_finger.enabled'
                keys = key.split('.')
                current = self.config
                for k in keys[:-1]:
                    if k not in current:
                        current[k] = {}
                    current = current[k]
                current[keys[-1]] = value
            else:
                self.config[key] = value
        
        # Save updated config
        self.save_config()
    
    def get_gesture_config(self, gesture_name):
        """Get configuration for a specific gesture"""
        return self.config.get('gestures', {}).get(gesture_name, {})
    
    def set_gesture_config(self, gesture_name, config):
        """Set configuration for a specific gesture"""
        if 'gestures' not in self.config:
            self.config['gestures'] = {}
        self.config['gestures'][gesture_name] = config
        self.save_config()
    
    def is_gesture_enabled(self, gesture_name):
        """Check if a gesture is enabled"""
        gesture_config = self.get_gesture_config(gesture_name)
        return gesture_config.get('enabled', True)
    
    def enable_gesture(self, gesture_name, enabled=True):
        """Enable or disable a gesture"""
        gesture_config = self.get_gesture_config(gesture_name)
        gesture_config['enabled'] = enabled
        self.set_gesture_config(gesture_name, gesture_config)
