"""
Setup script to create a macOS .app bundle
Usage: python setup.py py2app
"""
from setuptools import setup

APP = ['leaning_control_system.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'cv2',
        'mediapipe',
        'numpy',
        'pyautogui',
        'pynput',
    ],
    'iconfile': None,  # Add path to .icns file if you have one
    'plist': {
        'CFBundleName': 'FingerGuns',
        'CFBundleDisplayName': 'FingerGuns Gesture Control',
        'CFBundleIdentifier': 'com.fingerguns.gesturecontrol',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSCameraUsageDescription': 'This app needs camera access for gesture control.',
        'NSHighResolutionCapable': True,
    },
}

setup(
    name='FingerGuns',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
