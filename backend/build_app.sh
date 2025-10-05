#!/bin/bash
# Quick build script for FingerGuns app

echo "🎮 Building FingerGuns App..."
echo "================================"

# Check if py2app is installed
if ! python -c "import py2app" 2>/dev/null; then
    echo "📦 Installing py2app..."
    pip install py2app
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Build the app
echo "🔨 Building app..."
python setup.py py2app

# Check if build succeeded
if [ -d "dist/FingerGuns.app" ]; then
    echo ""
    echo "✅ Build successful!"
    echo "📁 App location: dist/FingerGuns.app"
    echo ""
    echo "To run: open dist/FingerGuns.app"
    echo "To distribute: cd dist && zip -r ../FingerGuns-macOS.zip FingerGuns.app"
    echo ""
    
    # Get app size
    APP_SIZE=$(du -sh dist/FingerGuns.app | cut -f1)
    echo "📦 App size: $APP_SIZE"
else
    echo "❌ Build failed! Check errors above."
    exit 1
fi
