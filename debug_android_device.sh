#!/bin/bash

echo "🚀 Android Device Debug Script Starting..."
echo "========================================"

# Check if adb is installed
if ! command -v adb &> /dev/null; then
    echo "❌ ADB not found in PATH"
    echo "💡 Please install Android SDK Platform Tools"
    echo "   - Download from: https://developer.android.com/studio/releases/platform-tools"
    echo "   - Or install via Homebrew: brew install android-platform-tools"
    exit 1
fi

echo "✅ ADB is installed: $(adb --version | head -1)"

# Start ADB server
echo "🔧 Starting ADB server..."
adb start-server

# Wait a moment for server to start
sleep 2

# List connected devices
echo "📱 Checking connected Android devices..."
adb devices -l

# Get device count
DEVICE_COUNT=$(adb devices | grep -v "List of devices" | grep -c "device")
echo "Found $DEVICE_COUNT Android device(s)"

if [ "$DEVICE_COUNT" -eq 0 ]; then
    echo "❌ No Android device connected via USB"
    echo "💡 Please:"
    echo "   1. Connect your Android device via USB cable"
    echo "   2. Enable Developer Options on your device"
    echo "   3. Enable USB Debugging in Developer Options"
    echo "   4. Allow USB debugging when prompted on device"
    echo "   5. Check cable connection"
    
    echo "🔧 Attempting to fix device connection issues..."
    
    # Try to restart ADB
    echo "Restarting ADB server..."
    adb kill-server
    sleep 2
    adb start-server
    sleep 2
    
    # Check again
    DEVICE_COUNT_RETRY=$(adb devices | grep -v "List of devices" | grep -c "device")
    if [ "$DEVICE_COUNT_RETRY" -eq 0 ]; then
        echo "❌ Still no device found after retry"
        echo "🔍 Troubleshooting tips:"
        echo "   - Check if device appears in 'lsusb' output"
        echo "   - Try different USB cable"
        echo "   - Enable 'Transfer files' mode on device"
        echo "   - Revoke USB debugging authorizations and try again"
        exit 1
    else
        echo "✅ Device found after retry!"
    fi
fi

# Get device information
echo "📋 Device Information:"
echo "----------------------"

# Get first device ID
DEVICE_ID=$(adb devices | grep -v "List of devices" | grep "device" | head -1 | awk '{print $1}')
echo "🆔 Device ID: $DEVICE_ID"

# Get device properties
echo "📱 Device Name: $(adb -s $DEVICE_ID shell getprop ro.product.model)"
echo "🏭 Manufacturer: $(adb -s $DEVICE_ID shell getprop ro.product.manufacturer)"
echo "🤖 Android Version: $(adb -s $DEVICE_ID shell getprop ro.build.version.release)"
echo "📊 API Level: $(adb -s $DEVICE_ID shell getprop ro.build.version.sdk)"
echo "🏗️ Build Number: $(adb -s $DEVICE_ID shell getprop ro.build.display.id)"

# Check if device is rooted
echo "🔐 Root Status: $(adb -s $DEVICE_ID shell su -c 'echo rooted' 2>/dev/null || echo 'not rooted')"

# Check USB debugging status
echo "🐛 USB Debugging: $(adb -s $DEVICE_ID shell getprop persist.sys.usb.config | grep -q adb && echo 'enabled' || echo 'disabled')"

# Check developer options
echo "🛠️ Developer Options: $(adb -s $DEVICE_ID shell getprop persist.sys.usb.config | grep -q adb && echo 'enabled' || echo 'unknown')"

# Check if Liveboard app is installed
echo ""
echo "📦 Liveboard App Status:"
echo "------------------------"
LIVEBOARD_PACKAGE="com.inconceptlabs.liveboard"

if adb -s $DEVICE_ID shell pm list packages | grep -q "$LIVEBOARD_PACKAGE"; then
    echo "✅ Liveboard app is installed"
    
    # Get app info
    echo "📋 App Information:"
    APP_VERSION=$(adb -s $DEVICE_ID shell dumpsys package $LIVEBOARD_PACKAGE | grep "versionName" | head -1 | awk -F'=' '{print $2}')
    echo "   Version: $APP_VERSION"
    
    # Get app permissions
    echo "🔐 App Permissions:"
    adb -s $DEVICE_ID shell dumpsys package $LIVEBOARD_PACKAGE | grep -A 20 "granted permissions:" | head -10
    
    # Check if app is currently running
    if adb -s $DEVICE_ID shell ps | grep -q "$LIVEBOARD_PACKAGE"; then
        echo "🟢 App is currently running"
    else
        echo "🔴 App is not running"
    fi
    
else
    echo "❌ Liveboard app is not installed"
    echo "💡 Please install the Liveboard app on your device"
fi

# Check system resources
echo ""
echo "💻 System Resources:"
echo "--------------------"
echo "📊 CPU Architecture: $(adb -s $DEVICE_ID shell getprop ro.product.cpu.abi)"
echo "💾 Memory Info:"
adb -s $DEVICE_ID shell cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable" | head -3

# Check storage
echo "💽 Storage Info:"
adb -s $DEVICE_ID shell df -h | grep -E "/system|/data" | head -2

# Check network connectivity
echo ""
echo "🌐 Network Status:"
echo "------------------"
WIFI_STATUS=$(adb -s $DEVICE_ID shell dumpsys wifi | grep "Wi-Fi is" | head -1 || echo "unknown")
echo "📶 WiFi: $WIFI_STATUS"

# Check for common issues
echo ""
echo "🔍 Common Issues Check:"
echo "----------------------"

# Check if device is locked
SCREEN_STATE=$(adb -s $DEVICE_ID shell dumpsys power | grep "Display Power" | head -1 || echo "unknown")
echo "🔒 Screen State: $SCREEN_STATE"

if adb -s $DEVICE_ID shell dumpsys power | grep -q "Display Power: state=OFF"; then
    echo "⚠️ Device screen is OFF - please unlock your device"
fi

# Check if device is in USB file transfer mode
USB_MODE=$(adb -s $DEVICE_ID shell getprop sys.usb.state)
echo "🔌 USB Mode: $USB_MODE"

# Check Appium-related services
echo ""
echo "🤖 Appium Compatibility:"
echo "-------------------------"

# Check if UiAutomator2 server can be installed
echo "🔧 Checking UiAutomator2 compatibility..."
if adb -s $DEVICE_ID shell pm list instrumentation | grep -q "uiautomator"; then
    echo "✅ UiAutomator2 framework is available"
else
    echo "⚠️ UiAutomator2 framework not found"
fi

# Check if device supports automation
if adb -s $DEVICE_ID shell service list | grep -q "accessibility"; then
    echo "✅ Accessibility services available"
else
    echo "⚠️ Accessibility services not available"
fi

# Final recommendations
echo ""
echo "💡 Final Recommendations:"
echo "-------------------------"
echo "✅ Ensure device is unlocked and screen is on during testing"
echo "✅ Keep USB debugging enabled"
echo "✅ Use 'File Transfer' or 'MTP' USB mode for best compatibility"
echo "✅ Install Liveboard app if not already installed"
echo "✅ Grant necessary permissions to the app"

# Export device information for CI
echo ""
echo "📤 Exporting device info for CI..."
echo "DEVICE_UDID=$DEVICE_ID" > android_device_info.env
echo "DEVICE_NAME=$(adb -s $DEVICE_ID shell getprop ro.product.model)" >> android_device_info.env
echo "PLATFORM_VERSION=$(adb -s $DEVICE_ID shell getprop ro.build.version.release)" >> android_device_info.env
echo "API_LEVEL=$(adb -s $DEVICE_ID shell getprop ro.build.version.sdk)" >> android_device_info.env

echo "✅ Device info saved to android_device_info.env"

echo ""
echo "🎉 Android device debug completed!"
echo "========================================" 