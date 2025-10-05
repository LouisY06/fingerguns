"""
MediaPipe UI Overlay Module
Handles all UI drawing and interaction for the gesture control system
"""

import cv2
import json
import os


class MediaPipeOverlay:
    """Handles all UI overlay drawing and interaction for MediaPipe gesture control"""
    
    def __init__(self, config_manager):
        """Initialize the overlay with configuration manager"""
        self.config_manager = config_manager
        self.config_panel_height = 200
        
        # UI state
        self.ui_mode = "overlay"
        self.show_config_panel = False
        self.show_gesture_mapping = False
        self.show_help_panel = False
        self.ui_panel = "main"
        self.selected_gesture = None
        self.editing_key = None
        self.selected_config_item = 0
        self.editing_mode = False
        
        # Configuration items for the config panel
        self.config_items = [
            "mouse_sensitivity",
            "mouse_smoothing", 
            "mouse_deadzone",
            "lean_threshold",
            "pitch_threshold_forward",
            "pitch_threshold_backward"
        ]
    
    def draw_gesture_overlay(self, frame, results):
        """Draw gesture detection overlay on the frame"""
        if not results:
            return frame
            
        h, w = frame.shape[:2]
        
        # Extract gesture states
        left_hand_gesture = results.get('left_hand_gesture', [None, None])
        right_hand_gesture = results.get('right_hand_gesture', [None, None])
        head_pose = results.get('head_pose', {})
        body_lean = results.get('body_lean', {})
        tongue_out = results.get('tongue_out', False)
        
        # Determine active states
        gun_active = right_hand_gesture[0] == "gun"
        shoot_status = "READY" if right_hand_gesture[1] == "thumb_up" else "FIRING" if right_hand_gesture[1] == "thumb_down" else "INACTIVE"
        left_status = left_hand_gesture[0] if left_hand_gesture[0] else "INACTIVE"
        tongue_status = "OUT" if tongue_out else "IN"
        
        # WASD movement states
        wasd_states = {
            'w': head_pose.get('pitch', 0) < -self.config_manager.get_config().get('pitch_threshold_backward', 12),
            's': head_pose.get('pitch', 0) > self.config_manager.get_config().get('pitch_threshold_forward', 8),
            'a': body_lean.get('lean', 0) < -self.config_manager.get_config().get('lean_threshold', 3),
            'd': body_lean.get('lean', 0) > self.config_manager.get_config().get('lean_threshold', 3)
        }
        
        # Draw gesture status overlay
        self._draw_gesture_status(frame, gun_active, shoot_status, left_status, tongue_status, wasd_states, tongue_out)
        
        return frame
    
    def _draw_gesture_status(self, frame, gun_active, shoot_status, left_status, tongue_status, wasd_states, tongue_out):
        """Draw gesture status information on frame"""
        h, w = frame.shape[:2]
        
        # Title overlay (top left)
        cv2.putText(frame, "Hybrid Control System", (20, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, "UI: C=Config H=Help M=Gestures", (20, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 255), 1)
        
        # Movement overlay (top right) - Clean WASD display
        self._draw_wasd_overlay(frame, w - 190, 30, wasd_states)
        
        # Gesture status panel (bottom left) - Organized layout
        y_start = h - 130
        
        # Right hand (gun)
        gun_color = (0, 255, 0) if gun_active else (128, 128, 128)
        cv2.putText(frame, f"🔫 Gun: {'ACTIVE' if gun_active else 'INACTIVE'}", (20, y_start + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, gun_color, 2)
        if gun_active:
            cv2.putText(frame, f"   Shoot: {shoot_status}", (20, y_start + 45), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Left hand
        cv2.putText(frame, f"✋ Left: {left_status}", (20, y_start + 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Tongue
        tongue_color = (0, 255, 0) if tongue_out else (128, 128, 128)
        cv2.putText(frame, f"👅 Tongue: {tongue_status}", (20, y_start + 95), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, tongue_color, 2)
    
    def _draw_wasd_overlay(self, frame, x, y, wasd_states):
        """Draw clean WASD movement indicator"""
        # Draw key indicators in a clean layout
        key_positions = {
            'w': (x + 80, y + 25),
            'a': (x + 40, y + 50),
            's': (x + 80, y + 50),
            'd': (x + 120, y + 50)
        }
        
        # Draw active keys
        active_keys = [key for key, active in wasd_states.items() if active]
        if active_keys:
            cv2.putText(frame, f"Moving: {' '.join([k.upper() for k in active_keys])}", 
                       (x + 10, y + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Draw key circles
        for key, (kx, ky) in key_positions.items():
            color = (0, 255, 0) if wasd_states[key] else (60, 60, 60)
            cv2.circle(frame, (kx, ky), 12, color, -1)
            cv2.circle(frame, (kx, ky), 12, (255, 255, 255), 1)
            cv2.putText(frame, key.upper(), (kx - 6, ky + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    def draw_config_panel(self, frame):
        """Draw enhanced configuration panel with interactive controls"""
        h, w = frame.shape[:2]
        
        # Create gradient background
        overlay = frame.copy()
        panel_height = self.config_panel_height
        cv2.rectangle(overlay, (0, h - panel_height), (w, h), (20, 20, 40), -1)
        cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
        
        # Draw panel border with gradient effect
        cv2.rectangle(frame, (0, h - panel_height), (w, h), (100, 150, 255), 2)
        cv2.rectangle(frame, (2, h - panel_height + 2), (w - 2, h - 2), (50, 100, 200), 1)
        
        # Panel title with icon
        title_y = h - panel_height + 30
        cv2.putText(frame, "⚙️ CONFIGURATION", (15, title_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Status indicator
        status_text = "EDITING" if self.editing_mode else "NAVIGATING"
        status_color = (0, 255, 100) if self.editing_mode else (255, 255, 100)
        cv2.putText(frame, f"[{status_text}]", (w - 120, title_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        # Configuration items in a clean grid
        y_start = h - panel_height + 55
        x_start = 15
        
        # Get current config
        current_config = self.config_manager.get_config()
        
        # Draw configuration items
        for i, item in enumerate(self.config_items):
            item_y = y_start + i * 22
            is_selected = (i == self.selected_config_item)
            is_editing = (is_selected and self.editing_mode)
            
            # Item background
            if is_selected:
                cv2.rectangle(frame, (x_start - 5, item_y - 15), (w - 15, item_y + 5), 
                             (100, 100, 200) if is_editing else (60, 60, 120), -1)
            
            # Item name
            display_name = item.replace('_', ' ').title()
            color = (255, 255, 100) if is_editing else ((255, 255, 255) if is_selected else (200, 200, 200))
            cv2.putText(frame, display_name, (x_start, item_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            # Value with visual bar
            value = current_config.get(item, 0.0)
            
            # Define ranges for visual representation
            ranges = {
                "mouse_sensitivity": (0.1, 5.0),
                "mouse_smoothing": (0.1, 1.0),
                "mouse_deadzone": (0.0, 2.0),
                "lean_threshold": (1.0, 20.0),
                "pitch_threshold_forward": (1.0, 30.0),
                "pitch_threshold_backward": (1.0, 30.0)
            }
            
            min_val, max_val = ranges.get(item, (0.0, 10.0))
            normalized_value = (value - min_val) / (max_val - min_val)
            
            # Value bar
            bar_width = 200
            bar_height = 12
            bar_x = w - bar_width - 100
            bar_y = item_y - 8
            
            # Bar background
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (40, 40, 40), -1)
            
            # Bar fill
            fill_width = int(normalized_value * bar_width)
            if fill_width > 0:
                bar_color = (0, 255, 100) if is_editing else (100, 200, 255)
                cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), bar_color, -1)
            
            # Value text
            value_text = f"{value:.3f}" if item.startswith('mouse_') else f"{value:.1f}"
            cv2.putText(frame, value_text, (w - 80, item_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Instructions
        inst_y = h - 25
        if self.editing_mode:
            cv2.putText(frame, "↑↓/WS: Adjust | ←→/AD: Fine | Enter: Stop | C: Close | ESC: Quit", 
                       (x_start, inst_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 100), 1)
        else:
            cv2.putText(frame, "↑↓/WS: Navigate | Enter: Edit | C: Close | ESC: Quit", 
                       (x_start, inst_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    
    def draw_gesture_mapping_panel(self, frame):
        """Draw gesture mapping configuration panel"""
        h, w = frame.shape[:2]
        
        # Create semi-transparent background
        overlay = frame.copy()
        panel_height = self.config_panel_height
        cv2.rectangle(overlay, (0, h - panel_height), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Draw panel border
        cv2.rectangle(frame, (0, h - panel_height), (w, h), (255, 255, 255), 2)
        
        # Panel title
        cv2.putText(frame, "GESTURE MAPPING", (10, h - panel_height + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Gesture categories
        y_start = h - panel_height + 50
        x_start = 10
        
        current_config = self.config_manager.get_config()
        gestures = current_config.get('gestures', {})
        
        # Left Hand Gestures
        cv2.putText(frame, "Left Hand:", (x_start, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        left_gestures = [k for k in gestures.keys() if k.startswith('left_hand')]
        for i, gesture in enumerate(left_gestures[:2]):  # Show first 2
            config = gestures[gesture]
            action = config.get('action', 'unknown')
            key = config.get('key', '')
            enabled = "ON" if config.get('enabled', True) else "OFF"
            cv2.putText(frame, f"  {gesture.replace('left_hand_', '')}: {action}({key}) [{enabled}]", 
                       (x_start + 100, y_start + i * 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        # Right Hand Gestures
        y_start += 35
        cv2.putText(frame, "Right Hand:", (x_start, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        right_gestures = [k for k in gestures.keys() if k.startswith('right_hand')]
        for i, gesture in enumerate(right_gestures[:2]):  # Show first 2
            config = gestures[gesture]
            action = config.get('action', 'unknown')
            key = config.get('key', '')
            button = config.get('button', '')
            enabled = "ON" if config.get('enabled', True) else "OFF"
            display_key = key if key else button
            cv2.putText(frame, f"  {gesture.replace('right_hand_', '')}: {action}({display_key}) [{enabled}]", 
                       (x_start + 100, y_start + i * 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        # Body Movement
        y_start += 35
        cv2.putText(frame, "Body Movement:", (x_start, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        body_gestures = [k for k in gestures.keys() if k.startswith(('head_', 'body_lean'))]
        for i, gesture in enumerate(body_gestures[:2]):  # Show first 2
            config = gestures[gesture]
            action = config.get('action', 'unknown')
            key = config.get('key', '')
            enabled = "ON" if config.get('enabled', True) else "OFF"
            cv2.putText(frame, f"  {gesture}: {action}({key}) [{enabled}]", 
                       (x_start + 100, y_start + i * 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        # Instructions
        y_start += 35
        cv2.putText(frame, "Press 'M' to close | Use arrow keys to navigate | Press Enter to edit", 
                   (x_start, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)
    
    def draw_help_panel(self, frame):
        """Draw help panel with controls and gestures"""
        h, w = frame.shape[:2]
        
        # Create semi-transparent background
        overlay = frame.copy()
        panel_height = self.config_panel_height
        cv2.rectangle(overlay, (0, h - panel_height), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Draw panel border
        cv2.rectangle(frame, (0, h - panel_height), (w, h), (255, 255, 255), 2)
        
        # Panel title
        cv2.putText(frame, "HELP & CONTROLS", (10, h - panel_height + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Help sections
        y_start = h - panel_height + 50
        x_start = 10
        
        # Basic Controls
        cv2.putText(frame, "Controls:", (x_start, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "G=Toggle Control  C=Config  H=Help  M=Gestures  Q=Quit", 
                   (x_start + 80, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        # Movement
        y_start += 20
        cv2.putText(frame, "Movement:", (x_start, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Head Forward=S  Head Back=S  Lean Left=A  Lean Right=D", 
                   (x_start + 80, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        # Gestures
        y_start += 20
        cv2.putText(frame, "Gestures:", (x_start, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Left: 1 finger=Ctrl 4 fingers=Space", 
                   (x_start + 80, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        y_start += 15
        cv2.putText(frame, "Right: Gun gesture=Mouse  Thumb=Shoot", 
                   (x_start + 80, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        y_start += 15
        cv2.putText(frame, "Tongue: Out=T", 
                   (x_start + 80, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        # Sensitivity Controls
        y_start += 20
        cv2.putText(frame, "Config Panel:", (x_start, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "C=Config ↑↓=Adjust ←→=Fine +/-=Legacy", 
                   (x_start + 80, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        # Instructions
        y_start += 20
        cv2.putText(frame, "Press 'H' to close this help panel", 
                   (x_start, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)
    
    def handle_keyboard_input(self, key, mouse_controller=None):
        """Handle keyboard input for UI interaction"""
        if key == ord('c') or key == ord('C'):
            self.show_config_panel = not self.show_config_panel
            print(f"⚙️ Configuration panel {'opened' if self.show_config_panel else 'closed'}")
            return True
        elif key == ord('h') or key == ord('H'):
            self.show_help_panel = not self.show_help_panel
            print(f"❓ Help panel {'opened' if self.show_help_panel else 'closed'}")
            return True
        elif key == ord('m') or key == ord('M'):
            self.show_gesture_mapping = not self.show_gesture_mapping
            print(f"🎮 Gesture mapping {'opened' if self.show_gesture_mapping else 'closed'}")
            return True
        elif key == 9:  # Tab key
            self.switch_ui_panel()
            return True
        elif key == 13:  # Enter key
            self.confirm_ui_selection()
            return True
        elif key == 82 or key == 0:  # Up arrow
            if self.show_config_panel and self.editing_mode:
                print("🔧 Up arrow detected - adjusting value up")
                self.adjust_config_value(0.05, mouse_controller)
            else:
                self.navigate_ui(-1)
            return True
        elif key == 84 or key == 1:  # Down arrow
            if self.show_config_panel and self.editing_mode:
                print("🔧 Down arrow detected - adjusting value down")
                self.adjust_config_value(-0.05, mouse_controller)
            else:
                self.navigate_ui(1)
            return True
        elif key == 81 or key == 2:  # Left arrow
            if self.show_config_panel and self.editing_mode:
                print("🔧 Left arrow detected - fine adjustment down")
                self.adjust_config_value(-0.01, mouse_controller)
            return True
        elif key == 83 or key == 3:  # Right arrow
            if self.show_config_panel and self.editing_mode:
                print("🔧 Right arrow detected - fine adjustment up")
                self.adjust_config_value(0.01, mouse_controller)
            return True
        # Alternative arrow key detection for different systems
        elif key == 2555904:  # Up arrow (extended key)
            if self.show_config_panel and self.editing_mode:
                print("🔧 Up arrow (extended) detected - adjusting value up")
                self.adjust_config_value(0.05, mouse_controller)
            else:
                self.navigate_ui(-1)
            return True
        elif key == 2555906:  # Down arrow (extended key)
            if self.show_config_panel and self.editing_mode:
                print("🔧 Down arrow (extended) detected - adjusting value down")
                self.adjust_config_value(-0.05, mouse_controller)
            else:
                self.navigate_ui(1)
            return True
        elif key == 2555905:  # Left arrow (extended key)
            if self.show_config_panel and self.editing_mode:
                print("🔧 Left arrow (extended) detected - fine adjustment down")
                self.adjust_config_value(-0.01, mouse_controller)
            return True
        elif key == 2555907:  # Right arrow (extended key)
            if self.show_config_panel and self.editing_mode:
                print("🔧 Right arrow (extended) detected - fine adjustment up")
                self.adjust_config_value(0.01, mouse_controller)
            return True
        # Alternative controls using letter keys
        elif key == ord('w') or key == ord('W'):  # W key for up
            if self.show_config_panel and self.editing_mode:
                print("🔧 W key detected - adjusting value up")
                self.adjust_config_value(0.05, mouse_controller)
            else:
                self.navigate_ui(-1)
            return True
        elif key == ord('s') or key == ord('S'):  # S key for down
            if self.show_config_panel and self.editing_mode:
                print("🔧 S key detected - adjusting value down")
                self.adjust_config_value(-0.05, mouse_controller)
            else:
                self.navigate_ui(1)
            return True
        elif key == ord('a') or key == ord('A'):  # A key for left (fine decrease)
            if self.show_config_panel and self.editing_mode:
                print("🔧 A key detected - fine adjustment down")
                self.adjust_config_value(-0.01, mouse_controller)
            return True
        elif key == ord('d') or key == ord('D'):  # D key for right (fine increase)
            if self.show_config_panel and self.editing_mode:
                print("🔧 D key detected - fine adjustment up")
                self.adjust_config_value(0.01, mouse_controller)
            return True
        
        return False
    
    def switch_ui_panel(self):
        """Switch between UI panels"""
        panels = ["main", "config", "gestures", "help"]
        current_index = panels.index(self.ui_panel)
        self.ui_panel = panels[(current_index + 1) % len(panels)]
        print(f"🔄 Switched to {self.ui_panel} panel")
    
    def navigate_ui(self, direction):
        """Navigate UI elements (up/down)"""
        if self.show_config_panel:
            self.selected_config_item = (self.selected_config_item + direction) % len(self.config_items)
            print(f"⬆️⬇️ Selected config item: {self.config_items[self.selected_config_item]}")
        elif self.show_gesture_mapping:
            print(f"⬆️⬇️ Navigated gesture mapping")
        else:
            print(f"⬆️⬇️ Navigated UI {direction}")
    
    def confirm_ui_selection(self):
        """Confirm current UI selection"""
        if self.show_config_panel:
            self.editing_mode = not self.editing_mode
            if self.editing_mode:
                print(f"✅ Editing {self.config_items[self.selected_config_item]}")
                print(f"💡 Use ↑↓ arrows to adjust value, ←→ for fine adjustments")
            else:
                print(f"✅ Finished editing")
        else:
            print(f"✅ Confirmed selection in {self.ui_panel} panel")
    
    def adjust_config_value(self, delta, mouse_controller=None):
        """Adjust the currently selected configuration value"""
        if not self.show_config_panel:
            return
        
        # If not in editing mode, don't adjust
        if not self.editing_mode:
            print(f"⚠️ Not in editing mode. Press Enter to start editing.")
            return
        
        item = self.config_items[self.selected_config_item]
        current_config = self.config_manager.get_config()
        current_value = current_config.get(item, 0.0)
        
        # Define value ranges for different config items
        ranges = {
            "mouse_sensitivity": (0.1, 5.0),
            "mouse_smoothing": (0.1, 1.0),
            "mouse_deadzone": (0.0, 2.0),
            "lean_threshold": (1.0, 20.0),
            "pitch_threshold_forward": (1.0, 30.0),
            "pitch_threshold_backward": (1.0, 30.0)
        }
        
        min_val, max_val = ranges.get(item, (0.0, 10.0))
        new_value = max(min_val, min(max_val, current_value + delta))
        
        # Only update if value actually changed
        if new_value != current_value:
            # Update config through config manager
            self.config_manager.update_config({item: new_value})
            
            # Update live controllers if applicable
            if mouse_controller and hasattr(mouse_controller, 'krunker_controller'):
                if item == "mouse_sensitivity":
                    mouse_controller.krunker_controller.sensitivity = new_value
                elif item == "mouse_smoothing":
                    mouse_controller.krunker_controller.smoothing_factor = new_value
                elif item == "mouse_deadzone":
                    mouse_controller.krunker_controller.dead_zone = new_value
            
            print(f"🔧 {item}: {new_value:.3f}")
    
    def draw_all_panels(self, frame):
        """Draw all active UI panels"""
        if self.show_config_panel:
            self.draw_config_panel(frame)
        if self.show_gesture_mapping:
            self.draw_gesture_mapping_panel(frame)
        if self.show_help_panel:
            self.draw_help_panel(frame)
