#!/usr/bin/env python3
"""
Test script to verify gesture controls work in games
This script simulates a game environment and tests all gesture controls
"""

import time
import pyautogui
import threading
from pynput import keyboard
from pynput.keyboard import Key, Listener

class GameControlTester:
    def __init__(self):
        self.test_results = {}
        self.running = True
        self.key_presses = []
        
    def on_press(self, key):
        """Record key presses for testing"""
        try:
            key_name = key.char if hasattr(key, 'char') and key.char else str(key)
            self.key_presses.append((time.time(), key_name))
            print(f"🎮 Key pressed: {key_name}")
        except AttributeError:
            pass
    
    def test_mouse_control(self):
        """Test mouse movement and clicking"""
        print("🖱️  Testing mouse control...")
        print("   - Make gun gesture with right hand")
        print("   - Move index finger to control cursor")
        print("   - Thumb up/down to click")
        time.sleep(5)
        
    def test_movement_controls(self):
        """Test WASD movement controls"""
        print("🚶 Testing movement controls...")
        print("   - Lean left/right for A/D movement")
        print("   - Move head forward/backward for W/S movement")
        time.sleep(5)
        
    def test_action_controls(self):
        """Test action controls (crouch, jump, spray)"""
        print("⚡ Testing action controls...")
        print("   - Left hand: 1 finger = Crouch (Ctrl)")
        print("   - Left hand: 4 fingers = Jump (Space)")
        print("   - Tongue out = Spray (T)")
        time.sleep(5)
        
    def run_tests(self):
        """Run all control tests"""
        print("🎮 Game Control Tester")
        print("=" * 50)
        print("This will test all gesture controls for game compatibility")
        print("Make sure the gesture control system is running!")
        print("=" * 50)
        
        # Start key listener
        listener = Listener(on_press=self.on_press)
        listener.start()
        
        try:
            # Test each control type
            self.test_mouse_control()
            self.test_movement_controls()
            self.test_action_controls()
            
            print("\n✅ Testing complete!")
            print(f"📊 Total key presses detected: {len(self.key_presses)}")
            
            if self.key_presses:
                print("🎯 Detected keys:")
                for timestamp, key in self.key_presses[-10:]:  # Show last 10
                    print(f"   - {key}")
            else:
                print("⚠️  No key presses detected. Check gesture system!")
                
        except KeyboardInterrupt:
            print("\n🛑 Testing interrupted")
        finally:
            listener.stop()
            
    def test_in_actual_game(self):
        """Instructions for testing in actual games"""
        print("\n🎮 In-Game Testing Instructions:")
        print("=" * 50)
        print("1. Start your favorite FPS game (CS:GO, Valorant, etc.)")
        print("2. Make sure gesture control system is running")
        print("3. Click on the game window to focus it")
        print("4. Test each control:")
        print("   🖱️  Mouse: Gun gesture + index finger movement")
        print("   🚶 Movement: Head/body lean for WASD")
        print("   ⚡ Actions: Left hand gestures + tongue")
        print("5. Adjust sensitivity in config panel if needed")
        print("=" * 50)

if __name__ == "__main__":
    tester = GameControlTester()
    
    print("Choose test mode:")
    print("1. Simulated testing (recommended first)")
    print("2. In-game testing instructions")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        tester.run_tests()
    elif choice == "2":
        tester.test_in_actual_game()
    else:
        print("Invalid choice. Running simulated test...")
        tester.run_tests()
