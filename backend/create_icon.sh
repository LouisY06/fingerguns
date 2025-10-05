#!/bin/bash

# Script to convert applogo.PNG to .icns format for macOS app

echo "🎨 Converting applogo.PNG to icon.icns..."

# Create iconset directory
mkdir -p icon.iconset

# Generate all required icon sizes
sips -z 16 16     applogo.PNG --out icon.iconset/icon_16x16.png
sips -z 32 32     applogo.PNG --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     applogo.PNG --out icon.iconset/icon_32x32.png
sips -z 64 64     applogo.PNG --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   applogo.PNG --out icon.iconset/icon_128x128.png
sips -z 256 256   applogo.PNG --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   applogo.PNG --out icon.iconset/icon_256x256.png
sips -z 512 512   applogo.PNG --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   applogo.PNG --out icon.iconset/icon_512x512.png
sips -z 1024 1024 applogo.PNG --out icon.iconset/icon_512x512@2x.png

# Create .icns file
iconutil -c icns icon.iconset

# Clean up iconset directory
rm -rf icon.iconset

echo "✅ Icon created: icon.icns"

