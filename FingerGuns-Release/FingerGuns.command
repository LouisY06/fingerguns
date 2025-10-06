#!/bin/bash
# FingerGuns - CS:GO Gesture Control Launcher
# Double-click this file to launch FingerGuns

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Clear screen for clean look
clear

echo "════════════════════════════════════════════════════"
echo "🎮  FingerGuns - CS:GO Gesture Control"
echo "════════════════════════════════════════════════════"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    echo ""
    echo "Please install Python 3 from:"
    echo "https://www.python.org/downloads/"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import cv2, mediapipe, pyautogui, numpy, pynput" 2>/dev/null; then
    echo ""
    echo "⚠️  Some dependencies are missing."
    echo "Installing now (this may take a few minutes)..."
    echo ""
    pip3 install -r "$DIR/requirements.txt" --quiet
    
    if [ $? -eq 0 ]; then
        echo "✓ Dependencies installed successfully!"
    else
        echo "❌ Failed to install dependencies."
        echo ""
        echo "Please run manually:"
        echo "  pip3 install -r requirements.txt"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
else
    echo "✓ All dependencies installed"
fi

echo ""
echo "════════════════════════════════════════════════════"
echo "🚀 Starting FingerGuns..."
echo "════════════════════════════════════════════════════"
echo ""
echo "Controls:"
echo "  'G' - Toggle gesture controls ON/OFF"
echo "  '+/-' - Adjust sensitivity"
echo "  'ESC' - Quit"
echo ""
echo "⚠️  Remember to click on the camera window before pressing 'G'!"
echo "════════════════════════════════════════════════════"
echo ""

# Run FingerGuns
cd "$DIR"
python3 leaning_control_system.py

# After exit
echo ""
echo "════════════════════════════════════════════════════"
echo "FingerGuns has closed."
echo "Thanks for using FingerGuns! 🎮"
echo "════════════════════════════════════════════════════"
echo ""
read -p "Press Enter to close this window..."


