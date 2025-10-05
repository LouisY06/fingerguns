"""
LEANING CONTROL SYSTEM
Combines:
- Dual hand tracking (from dual_hand_tracking.py)
- Body leaning detection for WASD movement (modified from head tracking)
- Tongue tracking for spray emote (from tongue_tracking.py)

Controls:
- 't' to toggle control ON/OFF
- 'q' or ESC to quit
"""

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import threading
from pynput.mouse import Controller as MouseController
import Quartz
from Quartz import (
    CGEventCreateMouseEvent, CGEventPost, CGEventSourceCreate,
    kCGEventMouseMoved, kCGEventLeftMouseDown, kCGEventLeftMouseUp,
    kCGEventSourceStateHIDSystemState, kCGHIDEventTap,
    CGEventSetIntegerValueField, kCGEventSourceStatePrivate
)

# PyAutoGUI Configuration for continuous key holding
pyautogui.PAUSE = 0  # Remove pause for continuous operation
pyautogui.FAILSAFE = False  # Disable failsafe for gesture control

# MediaPipe initialization
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(point1, point2, point3):
    vector1 = np.array([point1[0] - point2[0], point1[1] - point2[1]])
    vector2 = np.array([point3[0] - point2[0], point3[1] - point2[1]])
    cosine = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2) + 1e-6)
    angle = np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))
    return angle

def is_finger_extended(landmarks, finger_tip_id, finger_pip_id, finger_mcp_id):
    tip = [landmarks[finger_tip_id].x, landmarks[finger_tip_id].y]
    pip = [landmarks[finger_pip_id].x, landmarks[finger_pip_id].y]
    mcp = [landmarks[finger_mcp_id].x, landmarks[finger_mcp_id].y]
    angle = calculate_angle(tip, pip, mcp)
    return angle > 140  # Increased threshold to be more strict

def calculate_head_pose(face_landmarks, w, h):
    """Calculate head yaw (left/right tilt) and pitch (forward/backward) from face landmarks"""
    try:
        landmarks = face_landmarks.landmark
        
        # Key face landmarks for head pose estimation
        left_eye = landmarks[33]
        right_eye = landmarks[263]
        nose_tip = landmarks[1]
        chin = landmarks[152]
        forehead = landmarks[10]
        
        # Head tilt (left/right) - using eye height difference
        left_eye_y = left_eye.y
        right_eye_y = right_eye.y
        # Calculate tilt: positive = tilt right, negative = tilt left
        tilt = (right_eye_y - left_eye_y) * 200  # Scale factor for sensitivity
        yaw = tilt  # Use tilt value as yaw for A/D movement
        
        # Pitch (forward/backward) - using nose position relative to eyes
        nose_y = nose_tip.y
        chin_y = chin.y
        forehead_y = forehead.y
        
        # Calculate pitch based on nose position relative to face height (better method)
        face_height = chin_y - forehead_y
        if face_height > 0:
            nose_position = (nose_y - forehead_y) / face_height
            pitch = (nose_position - 0.5) * 100  # Center around 0
        else:
            pitch = 0
        
        # Debug output
        if not hasattr(calculate_head_pose, 'debug_counter'):
            calculate_head_pose.debug_counter = 0
        calculate_head_pose.debug_counter += 1
        if calculate_head_pose.debug_counter % 30 == 0:
            print(f"📊 Pitch: {pitch:.1f} (W threshold: {12}, S threshold: {-5})")
        
        return yaw, pitch
        
    except Exception as e:
        print(f"Head pose calculation error: {e}")
        return 0, 0

def is_gun_gesture(hand_landmarks):
    """Detect gun gesture (index out, bottom 3 curled)"""
    if hand_landmarks is None:
        return False
    landmarks = hand_landmarks.landmark
    index_extended = is_finger_extended(landmarks, 8, 6, 5)
    middle_curled = not is_finger_extended(landmarks, 12, 10, 9)
    ring_curled = not is_finger_extended(landmarks, 16, 14, 13)
    pinky_curled = not is_finger_extended(landmarks, 20, 18, 17)
    is_gun = index_extended and middle_curled and ring_curled and pinky_curled
    return is_gun

def is_thumb_down(hand_landmarks):
    """Detect if thumb is pressed down (shooting position)"""
    landmarks = hand_landmarks.landmark
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    thumb_mcp = landmarks[2]
    
    # Thumb pointing down if tip is below IP joint
    return thumb_tip.y > thumb_ip.y

def are_bottom_fingers_curled(hand_landmarks):
    """Check if bottom 3 fingers are curled (rotation-proof) - from finger_tracking.py"""
    landmarks = hand_landmarks.landmark
    wrist = landmarks[0]
    
    middle_tip = landmarks[12]
    middle_mcp = landmarks[9]
    middle_dist = ((middle_tip.x - wrist.x)**2 + (middle_tip.y - wrist.y)**2)**0.5
    middle_mcp_dist = ((middle_mcp.x - wrist.x)**2 + (middle_mcp.y - wrist.y)**2)**0.5
    middle_curled = middle_dist < middle_mcp_dist * 1.8
    
    ring_tip = landmarks[16]
    ring_mcp = landmarks[13]
    ring_dist = ((ring_tip.x - wrist.x)**2 + (ring_tip.y - wrist.y)**2)**0.5
    ring_mcp_dist = ((ring_mcp.x - wrist.x)**2 + (ring_mcp.y - wrist.y)**2)**0.5
    ring_curled = ring_dist < ring_mcp_dist * 1.8
    
    pinky_tip = landmarks[20]
    pinky_mcp = landmarks[17]
    pinky_dist = ((pinky_tip.x - wrist.x)**2 + (pinky_tip.y - wrist.y)**2)**0.5
    pinky_mcp_dist = ((pinky_mcp.x - wrist.x)**2 + (pinky_mcp.y - wrist.y)**2)**0.5
    pinky_curled = pinky_dist < pinky_mcp_dist * 1.8
    
    curled_count = sum([middle_curled, ring_curled, pinky_curled])
    return curled_count >= 2


def detect_left_hand_gestures(hand_landmarks):
    """Detect left hand gestures for crouch/jump"""
    try:
        if not hasattr(hand_landmarks, 'landmark') or len(hand_landmarks.landmark) < 21:
            return "invalid", None
            
        landmarks = hand_landmarks.landmark
        
        # Check individual finger states - for palm-facing camera, we check if fingers are DOWN
        thumb_down = not is_finger_extended(landmarks, 4, 3, 2)
        index_down = not is_finger_extended(landmarks, 8, 6, 5)
        middle_down = not is_finger_extended(landmarks, 12, 10, 9)
        ring_down = not is_finger_extended(landmarks, 16, 14, 13)
        pinky_down = not is_finger_extended(landmarks, 20, 18, 17)
        
        # Gesture detection based on fingers DOWN
        fingers_down = [thumb_down, index_down, middle_down, ring_down, pinky_down]
        num_fingers_down = sum(fingers_down)
        
        if num_fingers_down == 1:  # One finger down
            return "one_down", "ctrl"  # Crouch
        elif num_fingers_down == 4:  # Four fingers down (thumb up)
            return "four_down", "space"  # Jump
        else:
            return "unknown", None
            
    except Exception as e:
        print(f"Error in detect_left_hand_gestures: {e}")
        return "error", None


def calculate_lean_pose(pose_landmarks, frame_width, frame_height):
    """Calculate body lean for A/D movement based on shoulder and hip positions"""
    try:
        # Get key landmarks
        left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        
        # Calculate shoulder and hip centers
        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
        hip_center_x = (left_hip.x + right_hip.x) / 2
        
        # Calculate torso center
        torso_center_x = (shoulder_center_x + hip_center_x) / 2
        
        # Left/Right lean (A/D) - based on torso center position relative to frame center
        left_right = (torso_center_x - 0.5) * 100  # Positive = leaning right, Negative = leaning left
        
        return left_right
        
    except Exception as e:
        print(f"Error calculating lean pose: {e}")
        return 0

def detect_mouth_open(face_landmarks):
    """Detect if tongue is out (mouth open)"""
    try:
        landmarks = face_landmarks.landmark
        
        # Use specific lip landmarks for mouth opening detection
        upper_lip_bottom = landmarks[13]  # Upper lip bottom
        lower_lip_top = landmarks[14]     # Lower lip top
        
        # Calculate vertical separation between lips
        lip_separation = abs(upper_lip_bottom.y - lower_lip_top.y)
        
        # Threshold for mouth opening (adjustable)
        threshold = 0.015
        
        return lip_separation > threshold
    except:
        return False

class StickyGunDetector:
    """Gun gesture detector with sticky behavior (from dual_hand_tracking.py)"""
    def __init__(self, grace_period=30):
        self.is_locked = False
        self.lock_frames = 0
        self.grace_period = grace_period
        self.frames_without_hand = 0
        
    def update(self, hand_landmarks):
        if hand_landmarks is None:
            if self.is_locked:
                self.frames_without_hand += 1
                if self.frames_without_hand > self.grace_period:
                    self.is_locked = False
                    self.lock_frames = 0
                    self.frames_without_hand = 0
                    print("🔫 Gun UNLOCKED! (no hand)")
                    return False
                else:
                    return True
            else:
                self.frames_without_hand = 0
                return False
        
        self.frames_without_hand = 0
        gun_detected = is_gun_gesture(hand_landmarks)
        bottom_fingers_curled = are_bottom_fingers_curled(hand_landmarks)
        
        if not self.is_locked:
            if gun_detected:
                self.is_locked = True
                self.lock_frames = 0
                print("🔫 Gun LOCKED!")
                return True
            else:
                return False
        else:
            self.lock_frames += 1
            if not bottom_fingers_curled:
                self.is_locked = False
                self.lock_frames = 0
                print("🔫 Gun UNLOCKED!")
                return False
            else:
                return True

class ThumbShootingController:
    """Mouse click controller based on thumb position (from dual_hand_tracking.py)"""
    def __init__(self):
        self.is_pressed = False
        self.last_thumb_down = False
        
    def update(self, hand_landmarks, gun_active):
        if not gun_active or hand_landmarks is None:
            self.force_release()
            return False, "Gun not active"
        
        thumb_down = is_thumb_down(hand_landmarks)
        
        # Detect thumb press (transition from up to down)
        if thumb_down and not self.last_thumb_down:
            if not self.is_pressed:
                pyautogui.mouseDown()
                self.is_pressed = True
                return True, "FIRING!"
        
        # Detect thumb release (transition from down to up)
        elif not thumb_down and self.last_thumb_down:
            if self.is_pressed:
                pyautogui.mouseUp()
                self.is_pressed = False
                return False, "Ready"
        
        self.last_thumb_down = thumb_down
        
        if self.is_pressed:
            return True, "FIRING!"
        else:
            return False, "Ready"
    
    def force_release(self):
        if self.is_pressed:
            pyautogui.mouseUp()
            self.is_pressed = False

class KrunkerStyleMouseController:
    """Mouse controller with high-frequency cursor thread for smooth finger gun tracking"""
    def __init__(self):
        self.sensitivity = 2.5
        self.last_x = None
        self.last_y = None
        self.debug_counter = 0
        
        # Target position (updated by hand tracking at 30 FPS)
        self.target_delta_x = 0
        self.target_delta_y = 0
        
        # Current interpolated position (updated by cursor thread at 120+ FPS)
        self.current_delta_x = 0
        self.current_delta_y = 0
        
        # Velocity for smooth interpolation
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Dead zone for filtering hand tremors
        self.dead_zone = 0.8  # Increased to prevent spasms from small hand movements
        
        # Thread control
        self.cursor_thread = None
        self.thread_running = False
        self.thread_lock = threading.Lock()
        
        # Interpolation settings
        self.cursor_update_rate = 120  # Hz - cursor updates per second
        self.interpolation_speed = 0.15  # How fast to interpolate (0-1, lower = smoother, less overshoot)
        
    def _move_mouse_native(self, delta_x, delta_y):
        """Use native macOS CGEvent with delta fields"""
        try:
            from Quartz.CoreGraphics import (
                CGEventCreate, CGEventGetLocation, CGEventCreateMouseEvent,
                CGEventSetIntegerValueField, CGEventPost, kCGHIDEventTap,
                kCGEventMouseMoved, kCGMouseEventDeltaX, kCGMouseEventDeltaY
            )
            
            # Get current mouse position
            event = CGEventCreate(None)
            current_pos = CGEventGetLocation(event)
            
            # Calculate new position
            new_x = current_pos.x + delta_x
            new_y = current_pos.y + delta_y
            
            # Create mouse move event
            move_event = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (new_x, new_y), 0)
            
            # Set the delta fields explicitly
            CGEventSetIntegerValueField(move_event, kCGMouseEventDeltaX, int(delta_x))
            CGEventSetIntegerValueField(move_event, kCGMouseEventDeltaY, int(delta_y))
            
            # Post the event
            CGEventPost(kCGHIDEventTap, move_event)
            
        except Exception as e:
            print(f"Native mouse error: {e}")
    
    def _cursor_update_thread(self):
        """High-frequency cursor update thread (runs at 120+ FPS)"""
        update_interval = 1.0 / self.cursor_update_rate
        
        while self.thread_running:
            start_time = time.time()
            
            with self.thread_lock:
                # Check if there's any target movement to apply
                if abs(self.target_delta_x) > 0.1 or abs(self.target_delta_y) > 0.1:
                    # Take a fraction of the target movement each frame for smoothness
                    move_x = self.target_delta_x * self.interpolation_speed
                    move_y = self.target_delta_y * self.interpolation_speed
                    
                    # Apply the movement
                    if abs(move_x) >= 1.0 or abs(move_y) >= 1.0:
                        self._move_mouse_native(int(move_x), int(move_y))
                        
                        # Subtract what we applied from the target (drain the queue)
                        self.target_delta_x -= move_x
                        self.target_delta_y -= move_y
                    else:
                        # Movement too small, clear it to prevent buildup
                        self.target_delta_x = 0
                        self.target_delta_y = 0
            
            # Sleep to maintain update rate
            elapsed = time.time() - start_time
            sleep_time = max(0, update_interval - elapsed)
            time.sleep(sleep_time)
    
    def start_cursor_thread(self):
        """Start the high-frequency cursor update thread"""
        if not self.thread_running:
            self.thread_running = True
            self.cursor_thread = threading.Thread(target=self._cursor_update_thread, daemon=True)
            self.cursor_thread.start()
            print(f"🎯 Started cursor thread at {self.cursor_update_rate} Hz")
    
    def stop_cursor_thread(self):
        """Stop the cursor update thread and clear all pending movements"""
        # Immediately clear all pending movements
        with self.thread_lock:
            self.target_delta_x = 0
            self.target_delta_y = 0
            self.current_delta_x = 0
            self.current_delta_y = 0
        
        if self.thread_running:
            self.thread_running = False
            if self.cursor_thread:
                self.cursor_thread.join(timeout=0.5)
            print("🎯 Stopped cursor thread")
    
    def update(self, hand_landmarks, gun_active):
        """Update target position from hand tracking (30 FPS) - cursor thread handles smooth movement (120 FPS)"""
        if not gun_active or hand_landmarks is None:
            # Stop cursor thread when gun inactive but keep last position
            self.stop_cursor_thread()
            # Don't reset last_x and last_y - keep them for continuity
            with self.thread_lock:
                self.target_delta_x = 0
                self.target_delta_y = 0
                self.current_delta_x = 0
                self.current_delta_y = 0
            return
        
        # Start cursor thread if not running
        if not self.thread_running:
            self.start_cursor_thread()
            
        try:
            index_tip = hand_landmarks.landmark[8]
            
            # Convert to pixels for tracking
            current_x = index_tip.x * 1920
            current_y = index_tip.y * 1080
            
            if self.last_x is not None and self.last_y is not None:
                # Calculate raw delta movement
                raw_delta_x = (current_x - self.last_x) * self.sensitivity
                raw_delta_y = (current_y - self.last_y) * self.sensitivity
                
                # Apply dead zone filter
                movement_magnitude = (raw_delta_x**2 + raw_delta_y**2)**0.5
                if movement_magnitude < self.dead_zone:
                    raw_delta_x = 0
                    raw_delta_y = 0
                
                # Update target for cursor thread to interpolate toward
                with self.thread_lock:
                    self.target_delta_x += raw_delta_x
                    self.target_delta_y += raw_delta_y
                
                # Debug output
                self.debug_counter += 1
                if self.debug_counter % 30 == 0:
                    print(f"📍 Cursor Thread: raw=({int(raw_delta_x)},{int(raw_delta_y)}) "
                          f"target=({int(self.target_delta_x)},{int(self.target_delta_y)}) "
                          f"current=({int(self.current_delta_x)},{int(self.current_delta_y)})")
            
            self.last_x = current_x
            self.last_y = current_y
            
        except Exception as e:
            print(f"Mouse control error: {e}")

class SmoothMouseController:
    """Mouse controller using Krunker-style approach with smooth movement"""
    def __init__(self, sensitivity=1.5):
        self.krunker_controller = KrunkerStyleMouseController()
        self.krunker_controller.sensitivity = sensitivity
        print(f"🎮 Using smooth Krunker-style mouse controller with sensitivity: {sensitivity}")
        
    def update(self, hand_landmarks, gun_active):
        """Use Krunker-style mouse controller for better browser compatibility"""
        self.krunker_controller.update(hand_landmarks, gun_active)

class LeftHandGestureController:
    """Left hand gesture controller for crouch/jump"""
    def __init__(self):
        self.last_gesture = None
        self.last_gesture_time = 0
        self.gesture_debounce = 0.1
        
    def update(self, hand_landmarks, control_enabled):
        try:
            if not control_enabled or hand_landmarks is None:
                return None, "Control Disabled"
            
            current_time = time.time()
            gesture_name, action_key = detect_left_hand_gestures(hand_landmarks)
            
            if gesture_name == "error" or gesture_name == "invalid":
                return None, "Gesture detection error"
            
            # Handle gestures (crouch/jump) - single press
            if action_key and gesture_name != self.last_gesture:
                if current_time - self.last_gesture_time > self.gesture_debounce:
                    pyautogui.press(action_key)
                    self.last_gesture = gesture_name
                    self.last_gesture_time = current_time
                    return action_key, f"Pressed '{action_key}' - {gesture_name}"
                else:
                    return None, f"Gesture detected (debounced): {gesture_name}"
            elif gesture_name == self.last_gesture:
                return None, f"Holding: {gesture_name}"
            else:
                return None, "Left hand ready"
                
        except Exception as e:
            print(f"Error in LeftHandGestureController: {e}")
            return None, "Error"

class WASDController:
    """Hybrid controller: Head tilt for A/D, head pose for W/S"""
    def __init__(self, lean_threshold=3, pitch_threshold=5, pitch_threshold_back=12, hysteresis=0.7):
        self.lean_threshold = lean_threshold  # For A/D (left/right lean)
        self.pitch_threshold = pitch_threshold  # For W (head forward)
        self.pitch_threshold_back = pitch_threshold_back  # For S (head backward)
        self.hysteresis = hysteresis  # Multiplier for release threshold
        self.current_keys = set()  # Currently pressed keys
        
        # Gradual movement for A/D (left/right lean)
        self.lean_press_timer = 0
        self.small_lean_hold_duration = 1.0  # Hold key for 1 second for small leans
        self.small_lean_wait_duration = 0.075  # Wait 75ms between presses
        self.strong_lean_threshold = 8  # Threshold for holding down key (lowered for better response)
        self.last_lean_press_time = {'a': 0, 'd': 0}
        self.lean_key_state = {'a': False, 'd': False}  # Track if key is currently held
        self.lean_key_press_start = {'a': 0, 'd': 0}  # Track when key was pressed
        self.debug_counter = 0
        
    def update(self, head_yaw, head_pitch, control_enabled):
        """
        Update WASD keys based on head tilt (A/D) and head pose (W/S)
        Returns: (active_keys, key_states)
        """
        if not control_enabled:
            # Release all keys if control disabled
            self.release_all_keys()
            # Also release small lean keys
            if self.lean_key_state['a']:
                pyautogui.keyUp('a')
                self.lean_key_state['a'] = False
            if self.lean_key_state['d']:
                pyautogui.keyUp('d')
                self.lean_key_state['d'] = False
            return set(), {'w': False, 'a': False, 's': False, 'd': False}
        
        desired_keys = set()
        current_time = time.time()
        
        # Calculate release thresholds (closer to center)
        lean_release = self.lean_threshold * self.hysteresis
        pitch_release = self.pitch_threshold * self.hysteresis
        pitch_release_back = self.pitch_threshold_back * self.hysteresis
        
        # Release small lean keys if user returns to center
        if head_yaw >= -self.lean_threshold and head_yaw <= self.lean_threshold:
            if self.lean_key_state['a']:
                pyautogui.keyUp('a')
                self.lean_key_state['a'] = False
                print(f"🔄 Returned to center - Released 'A'")
            if self.lean_key_state['d']:
                pyautogui.keyUp('d')
                self.lean_key_state['d'] = False
                print(f"🔄 Returned to center - Released 'D'")
        
        # Determine which keys should be pressed (with hysteresis)
        # Left/Right tilt (A/D) - using head tilt with gradual movement
        if 'a' in self.current_keys:
            # Already pressing A
            if head_yaw > -lean_release:
                pass  # Release A
            else:
                desired_keys.add('a')  # Keep pressing A
        elif head_yaw < -self.lean_threshold:
            # Check if we should press A
            if head_yaw < -self.strong_lean_threshold:
                # Strong lean - hold down continuously
                desired_keys.add('a')
            else:
                # Small lean - hold for 1 second, wait 75ms, repeat
                if not self.lean_key_state['a']:
                    # Key is not currently held - check if we can start a new press
                    time_since_last_release = current_time - self.last_lean_press_time['a']
                    if time_since_last_release >= self.small_lean_wait_duration:
                        # Start holding the key
                        pyautogui.keyDown('a')
                        self.lean_key_state['a'] = True
                        self.lean_key_press_start['a'] = current_time
                        print(f"🔄 Small lean LEFT: {head_yaw:.1f}° - Holding 'A' for 1s")
                else:
                    # Key is currently held - check if we should release it
                    hold_duration = current_time - self.lean_key_press_start['a']
                    if hold_duration >= self.small_lean_hold_duration:
                        # Release the key after 1 second
                        pyautogui.keyUp('a')
                        self.lean_key_state['a'] = False
                        self.last_lean_press_time['a'] = current_time
                        print(f"🔄 Small lean LEFT: {head_yaw:.1f}° - Released 'A', waiting 75ms")
            
        if 'd' in self.current_keys:
            # Already pressing D
            if head_yaw < lean_release:
                pass  # Release D
            else:
                desired_keys.add('d')  # Keep pressing D
        elif head_yaw > self.lean_threshold:
            # Check if we should press D
            if head_yaw > self.strong_lean_threshold:
                # Strong lean - hold down continuously
                desired_keys.add('d')
            else:
                # Small lean - hold for 1 second, wait 75ms, repeat
                if not self.lean_key_state['d']:
                    # Key is not currently held - check if we can start a new press
                    time_since_last_release = current_time - self.last_lean_press_time['d']
                    if time_since_last_release >= self.small_lean_wait_duration:
                        # Start holding the key
                        pyautogui.keyDown('d')
                        self.lean_key_state['d'] = True
                        self.lean_key_press_start['d'] = current_time
                        print(f"🔄 Small lean RIGHT: {head_yaw:.1f}° - Holding 'D' for 1s")
                else:
                    # Key is currently held - check if we should release it
                    hold_duration = current_time - self.lean_key_press_start['d']
                    if hold_duration >= self.small_lean_hold_duration:
                        # Release the key after 1 second
                        pyautogui.keyUp('d')
                        self.lean_key_state['d'] = False
                        self.last_lean_press_time['d'] = current_time
                        print(f"🔄 Small lean RIGHT: {head_yaw:.1f}° - Released 'D', waiting 75ms")
            
        # Forward/Backward (W/S) - using head pose (switched W and S)
        if 'w' in self.current_keys:
            # Already pressing W
            if head_pitch < pitch_release_back:
                pass  # Release W
            else:
                desired_keys.add('w')  # Keep pressing W
        elif head_pitch > self.pitch_threshold_back:
            desired_keys.add('w')  # Start pressing W (head backward)
            
        if 's' in self.current_keys:
            # Already pressing S
            if head_pitch > -pitch_release:
                pass  # Release S
            else:
                desired_keys.add('s')  # Keep pressing S
        elif head_pitch < -self.pitch_threshold:
            desired_keys.add('s')  # Start pressing S (head forward)
        
        # Release keys that should no longer be pressed
        keys_to_release = self.current_keys - desired_keys
        for key in keys_to_release:
            pyautogui.keyUp(key)
            print(f"Released: {key.upper()}")
        
        # Press keys that should be pressed
        keys_to_press = desired_keys - self.current_keys
        for key in keys_to_press:
            pyautogui.keyDown(key)
            print(f"Pressed: {key.upper()}")
            
        # Continuously hold down keys that should remain pressed
        for key in desired_keys:
            pyautogui.keyDown(key)  # Keep pressing the key to ensure it stays down
        
        self.current_keys = desired_keys
        
        # Create key state dict for display
        key_states = {
            'w': 'w' in desired_keys,
            'a': 'a' in desired_keys,
            's': 's' in desired_keys,
            'd': 'd' in desired_keys
        }
        
        return desired_keys, key_states
    
    def release_all_keys(self):
        """Release all currently pressed keys"""
        for key in self.current_keys:
            pyautogui.keyUp(key)
        if self.current_keys:
            print(f"Released all keys: {', '.join([k.upper() for k in self.current_keys])}")
        self.current_keys = set()

class TongueController:
    """Tongue detection controller for spray emote (from tongue_tracking.py)"""
    def __init__(self, sensitivity=0.015, debounce_frames=10):
        self.sensitivity = sensitivity
        self.debounce_frames = debounce_frames
        self.frames_held = 0
        self.last_tongue_out = False
        
    def update(self, face_landmarks, control_enabled):
        if not control_enabled or face_landmarks is None:
            self.frames_held = 0
            self.last_tongue_out = False
            return False, "Control Disabled"
        
        tongue_out = detect_mouth_open(face_landmarks)
        
        if tongue_out:
            self.frames_held += 1
            if self.frames_held >= self.debounce_frames and not self.last_tongue_out:
                pyautogui.press('t')
                self.last_tongue_out = True
                return True, "Tongue out - T pressed!"
        else:
            self.frames_held = 0
            self.last_tongue_out = False
        
        return tongue_out, "Tongue ready"

class LeaningControlSystem:
    """Complete leaning-based CS:GO control system"""
    def __init__(self):
        # Initialize MediaPipe (optimized for 30 FPS)
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        self.pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=0,  # Reduced from 1 for faster processing
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=False,  # Disabled refinement for speed
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Sensitivity control (0.1 to 1.0)
        self.sensitivity = 0.5
        
        # Initialize controllers
        self.wasd_controller = WASDController()
        self.gun_detector = StickyGunDetector()
        self.shooting_controller = ThumbShootingController()
        self.mouse_controller = SmoothMouseController()
        self.left_hand_controller = LeftHandGestureController()
        self.tongue_controller = TongueController()
        
        # Apply initial sensitivity to mouse controller
        self.mouse_controller.krunker_controller.sensitivity = self.sensitivity * 2.5
        
        # Control state
        self.control_enabled = False
        
        print("Hybrid Control System initialized!")
        print("Movement: Head tilt for A/D + Head pose for W/S")
        print("Right hand: Gun control + shooting + Krunker-style mouse")
        print("Left hand: Crouch/jump")
        print("Tongue: Spray emote")
    
    
    def identify_hands(self, hand_landmarks_list):
        """Identify which hand is left vs right based on position (from dual_hand_tracking.py)"""
        if len(hand_landmarks_list) == 0:
            return None, None
        elif len(hand_landmarks_list) == 1:
            # Only one hand detected, assume it's the right hand
            return None, hand_landmarks_list[0]
        else:
            # Two hands detected, identify by x position
            hand1 = hand_landmarks_list[0]
            hand2 = hand_landmarks_list[1]
            
            # Get wrist positions
            wrist1_x = hand1.landmark[0].x
            wrist2_x = hand2.landmark[0].x
            
            # Left hand is on the left side of screen (lower x value)
            if wrist1_x < wrist2_x:
                return hand1, hand2  # hand1 is left, hand2 is right
            else:
                return hand2, hand1  # hand2 is left, hand1 is right
    
    def run(self):
        """Main control loop"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        print("Camera initialized successfully")
        print("Hybrid Control System")
        print("=" * 50)
        print("Controls:")
        print("  'g' - Toggle control ON/OFF")
        print("  '+' - Increase sensitivity")
        print("  '-' - Decrease sensitivity")
        print("  'q' - Quit")
        print("\nMovement (WASD - Hybrid):")
        print("  - Head FORWARD → Press 'S' (move forward)")
        print("  - Head BACKWARD → Press 'W' (move backward)")
        print("  - Body Lean LEFT (small) → Hold 'A' for 1s, wait 75ms, repeat")
        print("  - Body Lean LEFT (strong) → Hold 'A' down continuously")
        print("  - Body Lean RIGHT (small) → Hold 'D' for 1s, wait 75ms, repeat")
        print("  - Body Lean RIGHT (strong) → Hold 'D' down continuously")
        print("\nRight Hand (Gun Control):")
        print("  - Gun gesture (index out, bottom 3 curled)")
        print("  - Thumb UP = ready to shoot")
        print("  - Thumb DOWN = START FIRING")
        print("  - Index finger controls cursor")
        print("\nLeft Hand (Palm-Facing Controls):")
        print("  - One finger down = Press 'CTRL' (Crouch)")
        print("  - Four fingers down = Press 'SPACE' (Jump)")
        print("  - Other positions = No action")
        print("\nTongue:")
        print("  - Stick out tongue = Press 'T' (Spray emote)")
        print("\nPerfect for hybrid CS:GO control!")
        print("=" * 50)
        print("⚠️  IMPORTANT: Click on the camera window to enable keyboard controls!")
        print("   The 'g' key will only work when the window is focused.")
        print("=" * 50)
        
        frame_count = 0
        last_frame_time = time.time()
        
        # Cache for pose and face results (updated less frequently)
        pose_results = None
        face_results = None
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    time.sleep(0.001)  # Reduced sleep time
                    continue
                
                frame_count += 1
                current_time = time.time()
                if current_time - last_frame_time >= 1.0:
                    fps = frame_count / (current_time - last_frame_time)
                    print(f"Frame {frame_count}: Running... FPS: {fps:.1f}")
                    frame_count = 0
                    last_frame_time = current_time
                
                frame = cv2.flip(frame, 1)
                h, w, _ = frame.shape
                
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process hands EVERY frame (critical for smooth cursor)
                hand_results = self.hands.process(rgb_frame)
                
                # Process pose and face every 3 frames (WASD/tongue don't need high FPS)
                if frame_count % 3 == 0:
                    pose_results = self.pose.process(rgb_frame)
                    face_results = self.face_mesh.process(rgb_frame)
                
                # Initialize status variables
                head_yaw, head_pitch = 0, 0
                active_wasd_keys = set()
                wasd_states = {'w': False, 'a': False, 's': False, 'd': False}
                
                gun_active = False
                is_shooting = False
                shoot_status = "No right hand"
                left_action = None
                left_status = "No left hand"
                tongue_out = False
                tongue_status = "No face"
                
                # Process pose for body leaning (A/D only)
                if pose_results and pose_results.pose_landmarks:
                    try:
                        # Draw pose landmarks
                        mp_drawing.draw_landmarks(
                            frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
                        )
                        
                        # No body lean needed - using head tilt for A/D
                        
                    except Exception as e:
                        print(f"Error processing pose: {e}")
                
                # Process face for head pose (W/S) and tongue detection
                if face_results and face_results.multi_face_landmarks:
                    try:
                        face_landmarks = face_results.multi_face_landmarks[0]
                        
                        # Draw face mesh
                        mp_drawing.draw_landmarks(
                            frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS,
                            None, mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                        )
                        
                        # Head pose for W/S movement
                        head_yaw, head_pitch = calculate_head_pose(face_landmarks, w, h)
                        
                        # Tongue detection for spray emote
                        tongue_out, tongue_status = self.tongue_controller.update(
                            face_landmarks, self.control_enabled
                        )
                        
                    except Exception as e:
                        print(f"Error processing face: {e}")
                
                # Update WASD controller with head tilt (A/D) and head pose (W/S)
                active_wasd_keys, wasd_states = self.wasd_controller.update(
                    head_yaw, head_pitch, self.control_enabled
                )
                
                # Debug output for hybrid detection
                # print(f"DEBUG: Head Yaw (A/D)={head_yaw:.1f}, Head Pitch (W/S)={head_pitch:.1f}")
                
                # Process hands
                if hand_results and hand_results.multi_hand_landmarks:
                    try:
                        # Draw hand landmarks
                        for hand_landmarks in hand_results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2)
                            )
                        
                        # Identify left and right hands
                        left_hand, right_hand = self.identify_hands(hand_results.multi_hand_landmarks)
                        
                        # Process right hand (gun control)
                        if right_hand:
                            try:
                                # Only detect gun gesture if controls are enabled
                                if self.control_enabled:
                                    gun_active = self.gun_detector.update(right_hand)
                                    
                                    if gun_active:
                                        # Thumb shooting
                                        is_shooting, shoot_status = self.shooting_controller.update(
                                            right_hand, gun_active
                                        )
                                        
                                        # Mouse movement
                                        self.mouse_controller.update(right_hand, gun_active)
                                    else:
                                        # Gun not active - release mouse if held
                                        self.shooting_controller.force_release()
                                else:
                                    # Controls disabled - force release everything and reset gun detector
                                    self.shooting_controller.force_release()
                                    self.gun_detector.is_locked = False  # Reset gun detector
                                    self.gun_detector.lock_frames = 0
                                    gun_active = False
                                    
                            except Exception as e:
                                print(f"Error processing right hand: {e}")
                        
                        # Process left hand (gesture controls)
                        if left_hand:
                            try:
                                left_action, left_status = self.left_hand_controller.update(
                                    left_hand, self.control_enabled
                                )
                                
                            except Exception as e:
                                print(f"Error processing left hand: {e}")
                        
                    except Exception as e:
                        print(f"Error processing hands: {e}")
                
                # Display status overlay
                self.display_status(frame, wasd_states, gun_active, shoot_status, 
                                  left_status, tongue_status, head_yaw, head_pitch, tongue_out)
                
                # Add HUGE flashing reminder to toggle
                reminder_color = (0, 255, 255) if (frame_count // 5) % 2 == 0 else (255, 0, 255)
                cv2.putText(frame, ">>> CLICK HERE THEN PRESS 'G' <<<", (w//2 - 300, h - 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, reminder_color, 3)
                
                # Show frame
                cv2.imshow('Hybrid Control System', frame)
                # Try to bring window to front
                cv2.setWindowProperty('Hybrid Control System', cv2.WND_PROP_TOPMOST, 1)
                cv2.setWindowProperty('Hybrid Control System', cv2.WND_PROP_TOPMOST, 0)
                
                # Handle keyboard input (minimal wait for maximum FPS)
                try:
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q') or key == 27:  # 'q' or ESC to quit
                        print("Quit key pressed - exiting...")
                        break
                    elif key == ord('g'):
                        self.control_enabled = not self.control_enabled
                        if not self.control_enabled:
                            self.shooting_controller.force_release()
                            self.wasd_controller.release_all_keys()
                        print(f"\n{'='*50}")
                        print(f"Control {'ENABLED ✓' if self.control_enabled else 'DISABLED ✗'}")
                        print(f"{'='*50}\n")
                    elif key == ord('+') or key == ord('='):
                        self.sensitivity = min(1.0, self.sensitivity + 0.1)
                        # Apply sensitivity to mouse controller (finger gun cursor)
                        self.mouse_controller.krunker_controller.sensitivity = self.sensitivity * 2.5
                        print(f"🎯 Mouse Sensitivity: {self.sensitivity:.1f} (multiplier: {self.mouse_controller.krunker_controller.sensitivity:.2f})")
                    elif key == ord('-') or key == ord('_'):
                        self.sensitivity = max(0.1, self.sensitivity - 0.1)
                        # Apply sensitivity to mouse controller (finger gun cursor)
                        self.mouse_controller.krunker_controller.sensitivity = self.sensitivity * 2.5
                        print(f"🎯 Mouse Sensitivity: {self.sensitivity:.1f} (multiplier: {self.mouse_controller.krunker_controller.sensitivity:.2f})")
                except Exception as e:
                    print(f"Error handling keyboard input: {e}")
                    
        except KeyboardInterrupt:
            print("Interrupted by user")
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            # Cleanup
            try:
                print("Cleaning up resources...")
                self.shooting_controller.force_release()
                self.wasd_controller.release_all_keys()
                # Stop cursor thread
                self.mouse_controller.krunker_controller.stop_cursor_thread()
                # Clean up mouse controller
                self.mouse_controller.krunker_controller.last_x = None
                self.mouse_controller.krunker_controller.last_y = None
                cap.release()
                cv2.destroyAllWindows()
                self.hands.close()
                self.pose.close()
                self.face_mesh.close()
                print("Camera released")
                print("Windows closed")
                print("MediaPipe closed")
                print("Cursor thread stopped")
                print("\n🎉 Hybrid control system finished!")
            except Exception as e:
                print(f"Error during cleanup: {e}")
    
    def display_status(self, frame, wasd_states, gun_active, shoot_status, 
                      left_status, tongue_status, head_yaw, head_pitch, tongue_out):
        """Display clean, organized status overlay"""
        h, w = frame.shape[:2]
        
        # Create semi-transparent background panels
        self._draw_panel(frame, 10, 10, 300, 120, "CONTROL STATUS", alpha=0.8)
        self._draw_panel(frame, w - 200, 10, 180, 100, "MOVEMENT", alpha=0.8)
        self._draw_panel(frame, 10, h - 150, 350, 130, "GESTURE STATUS", alpha=0.8)
        
        # Main control status (top left)
        control_status = "CONTROL: ON ✓" if self.control_enabled else "CONTROL: OFF ✗"
        control_color = (0, 255, 0) if self.control_enabled else (0, 0, 255)
        cv2.putText(frame, control_status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, control_color, 2)
        
        # Sensitivity display
        cv2.putText(frame, f"Mouse Sens: {self.sensitivity:.1f}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Toggle instruction
        cv2.putText(frame, "Press 'G' to toggle (click window first!)", (20, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.putText(frame, "Press 'Q' to quit | +/- to change sensitivity", (20, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
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
    
    def _draw_panel(self, frame, x, y, width, height, title, alpha=0.7):
        """Draw a semi-transparent panel with title"""
        # Create overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (x, y), (x + width, y + height), (0, 0, 0), -1)
        cv2.rectangle(overlay, (x, y), (x + width, y + height), (255, 255, 255), 2)
        
        # Blend overlay
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        # Add title
        cv2.putText(frame, title, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
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

if __name__ == "__main__":
    system = LeaningControlSystem()
    system.run()
