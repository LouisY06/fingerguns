#!/bin/bash
# Quick build script for FingerGuns app

echo "🎮 Building FingerGuns App..."
echo "================================"
echo ""

# Check if py2app is installed
if ! python -c "import py2app" 2>/dev/null; then
    echo "📦 Installing py2app..."
    pip install py2app
fi

# Create icon from applogo.PNG if it exists and icon.icns doesn't
if [ -f "applogo.PNG" ] && [ ! -f "icon.icns" ]; then
    echo "🎨 Creating app icon from applogo.PNG..."
    chmod +x create_icon.sh
    ./create_icon.sh
    echo ""
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist
echo ""

# Build the app
echo "🔨 Building app with py2app..."
python setup.py py2app

echo ""

# Check if build succeeded
if [ -d "dist/FingerGuns.app" ]; then
    echo "✅ Build successful!"
    echo ""
    echo "📁 App location: dist/FingerGuns.app"
    echo ""
    
    # Get app size
    APP_SIZE=$(du -sh dist/FingerGuns.app | cut -f1)
    echo "📦 App size: $APP_SIZE"
    echo ""
    
    echo "📝 Next steps:"
    echo "  • Test the app: open dist/FingerGuns.app"
    echo "  • Move to Applications: cp -r dist/FingerGuns.app /Applications/"
    echo "  • Create ZIP for distribution: cd dist && zip -r ../FingerGuns-macOS.zip FingerGuns.app"
    echo ""
    echo "⚠️  If users get 'damaged app' error, they should run:"
    echo "     xattr -cr /Applications/FingerGuns.app"
    echo ""
else
    echo "❌ Build failed! Check errors above."
    exit 1
fi
