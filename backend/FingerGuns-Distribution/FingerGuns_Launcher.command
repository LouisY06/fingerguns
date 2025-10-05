#!/bin/bash
# FingerGuns Launcher
# Double-click this file to launch FingerGuns

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Clear screen
clear

echo "🎮 FingerGuns - Gesture Control System"
echo "======================================"
echo ""
echo "Starting FingerGuns..."
echo ""

# Run the Python script
cd "$DIR"
python3 leaning_control_system.py

echo ""
echo "FingerGuns has closed."
echo "You can close this window now."
