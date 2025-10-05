"""
Setup script to create a macOS .app bundle
Usage: python setup.py py2app
"""
from setuptools import setup
import os

APP = ['leaning_control_system.py']
DATA_FILES = []

# Check if icon exists
icon_file = 'icon.icns' if os.path.exists('icon.icns') else None

OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'cv2',
        'mediapipe',
        'numpy',
        'pyautogui',
        'pynput',
        'Quartz',
    ],
    'iconfile': icon_file,
    'plist': {
        'CFBundleName': 'FingerGuns',
        'CFBundleDisplayName': 'FingerGuns',
        'CFBundleIdentifier': 'com.fingerguns.gesturecontrol',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSCameraUsageDescription': 'FingerGuns needs camera access for hand gesture tracking and game control.',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.15.0',
    },
}

setup(
    name='FingerGuns',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
