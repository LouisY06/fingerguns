#!/bin/bash
# FingerGuns Installer
# This script sets up FingerGuns on the user's Mac

set -e  # Exit on error

clear
echo "🎮 FingerGuns Installer"
echo "======================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo ""
    echo "Please install Python 3 from:"
    echo "https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo "This may take a few minutes..."
echo ""

pip3 install --quiet mediapipe opencv-python pyautogui numpy pynput

if [ $? -eq 0 ]; then
    echo "✓ All dependencies installed!"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "To launch FingerGuns, double-click:"
echo "  FingerGuns_Launcher.command"
echo ""
echo "Or run from terminal:"
echo "  python3 leaning_control_system.py"
echo ""
read -p "Press Enter to close..."
