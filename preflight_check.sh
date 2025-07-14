#!/bin/bash

echo "🚀 Mobile Testing Pre-flight Check"
echo "=================================="

# Check command line arguments
PLATFORM=""
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 [ios|android|both]"
    echo "No platform specified, checking both iOS and Android..."
    PLATFORM="both"
else
    PLATFORM="$1"
    if [[ "$PLATFORM" != "ios" && "$PLATFORM" != "android" && "$PLATFORM" != "both" ]]; then
        echo "Error: Platform must be 'ios', 'android', or 'both'"
        exit 1
    fi
fi

echo "📱 Platform: $PLATFORM"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
PREFLIGHT_PASSED=true

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        PREFLIGHT_PASSED=false
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "ℹ️ $1"
}

echo "🔍 Checking system requirements..."

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_status 1 "macOS required for iOS testing"
    exit 1
fi
print_status 0 "Running on macOS"

# Platform-specific checks
if [[ "$PLATFORM" == "ios" || "$PLATFORM" == "both" ]]; then
    echo ""
    echo "🍎 iOS Platform Checks"
    echo "====================="
    
    # Check libimobiledevice
    if command -v idevice_id &> /dev/null; then
        print_status 0 "libimobiledevice installed"
    else
        print_status 1 "libimobiledevice not installed - run: brew install libimobiledevice"
    fi

    # Check iOS device connection
    echo ""
    echo "📱 Checking iOS device connection..."
    DEVICE_COUNT=$(idevice_id -l 2>/dev/null | wc -l)
    if [ "$DEVICE_COUNT" -eq 0 ]; then
        print_status 1 "No iOS device connected"
        print_info "Please connect your iPhone and trust the computer"
    else
        DEVICE_UDID=$(idevice_id -l | head -1)
        print_status 0 "iOS device connected: $DEVICE_UDID"
        
        # Get device info
        DEVICE_NAME=$(ideviceinfo -u "$DEVICE_UDID" -k DeviceName 2>/dev/null)
        IOS_VERSION=$(ideviceinfo -u "$DEVICE_UDID" -k ProductVersion 2>/dev/null)
        DEVICE_TYPE=$(ideviceinfo -u "$DEVICE_UDID" -k ProductType 2>/dev/null)
        
        print_info "Device: $DEVICE_NAME"
        print_info "iOS Version: $IOS_VERSION"
        print_info "Type: $DEVICE_TYPE"
    fi

    # Check if Liveboard app is installed
    echo ""
    echo "📱 Checking Liveboard app on iOS..."
    if [ "$DEVICE_COUNT" -gt 0 ]; then
        if ideviceinstaller -l | grep -q "com.inconceptlabs.liveboard"; then
            LIVEBOARD_VERSION=$(ideviceinstaller -l | grep "com.inconceptlabs.liveboard" | cut -d'"' -f4)
            print_status 0 "Liveboard app installed (version: $LIVEBOARD_VERSION)"
        else
            print_status 1 "Liveboard app not installed"
            print_info "Please install Liveboard app on your device"
        fi
    fi
fi

if [[ "$PLATFORM" == "android" || "$PLATFORM" == "both" ]]; then
    echo ""
    echo "🤖 Android Platform Checks"
    echo "=========================="
    
    # Check ADB
    if command -v adb &> /dev/null; then
        ADB_VERSION=$(adb --version | head -1)
        print_status 0 "ADB installed: $ADB_VERSION"
    else
        print_status 1 "ADB not installed - run: brew install android-platform-tools"
    fi

    # Check Android device connection
    echo ""
    echo "📱 Checking Android device connection..."
    adb start-server 2>/dev/null
    sleep 1
    ANDROID_DEVICE_COUNT=$(adb devices | grep -v "List of devices" | grep -c "device")
    if [ "$ANDROID_DEVICE_COUNT" -eq 0 ]; then
        print_status 1 "No Android device connected"
        print_info "Please connect your Android device and enable USB debugging"
    else
        ANDROID_DEVICE_UDID=$(adb devices | grep -v "List of devices" | grep "device" | head -1 | awk '{print $1}')
        print_status 0 "Android device connected: $ANDROID_DEVICE_UDID"
        
        # Get device info
        ANDROID_DEVICE_NAME=$(adb -s "$ANDROID_DEVICE_UDID" shell getprop ro.product.model 2>/dev/null)
        ANDROID_VERSION=$(adb -s "$ANDROID_DEVICE_UDID" shell getprop ro.build.version.release 2>/dev/null)
        ANDROID_API_LEVEL=$(adb -s "$ANDROID_DEVICE_UDID" shell getprop ro.build.version.sdk 2>/dev/null)
        ANDROID_MANUFACTURER=$(adb -s "$ANDROID_DEVICE_UDID" shell getprop ro.product.manufacturer 2>/dev/null)
        
        print_info "Device: $ANDROID_DEVICE_NAME"
        print_info "Android Version: $ANDROID_VERSION"
        print_info "API Level: $ANDROID_API_LEVEL"
        print_info "Manufacturer: $ANDROID_MANUFACTURER"
    fi

    # Check if Liveboard app is installed
    echo ""
    echo "📱 Checking Liveboard app on Android..."
    if [ "$ANDROID_DEVICE_COUNT" -gt 0 ]; then
        if adb -s "$ANDROID_DEVICE_UDID" shell pm list packages | grep -q "com.inconceptlabs.liveboard"; then
            ANDROID_LIVEBOARD_VERSION=$(adb -s "$ANDROID_DEVICE_UDID" shell dumpsys package com.inconceptlabs.liveboard | grep "versionName" | head -1 | awk -F'=' '{print $2}')
            print_status 0 "Liveboard app installed (version: $ANDROID_LIVEBOARD_VERSION)"
        else
            print_status 1 "Liveboard app not installed"
            print_info "Please install Liveboard app on your device"
        fi
    fi
fi

# Check Node.js and Appium
echo ""
echo "🔧 Checking Appium setup..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status 0 "Node.js installed: $NODE_VERSION"
else
    print_status 1 "Node.js not installed"
fi

if command -v appium &> /dev/null; then
    APPIUM_VERSION=$(appium --version)
    print_status 0 "Appium installed: $APPIUM_VERSION"
    
    # Check platform-specific drivers
    appium driver list --installed > /tmp/drivers_check.txt 2>&1
    
    if [[ "$PLATFORM" == "ios" || "$PLATFORM" == "both" ]]; then
        if grep -q "xcuitest" /tmp/drivers_check.txt; then
            XCUITEST_VERSION=$(grep "xcuitest" /tmp/drivers_check.txt | head -1)
            print_status 0 "XCUITest driver installed: $XCUITEST_VERSION"
        else
            print_status 1 "XCUITest driver not installed - run: appium driver install xcuitest"
        fi
    fi
    
    if [[ "$PLATFORM" == "android" || "$PLATFORM" == "both" ]]; then
        if grep -q "uiautomator2" /tmp/drivers_check.txt; then
            UIAUTOMATOR2_VERSION=$(grep "uiautomator2" /tmp/drivers_check.txt | head -1)
            print_status 0 "UiAutomator2 driver installed: $UIAUTOMATOR2_VERSION"
        else
            print_status 1 "UiAutomator2 driver not installed - run: appium driver install uiautomator2"
        fi
    fi
else
    print_status 1 "Appium not installed"
fi

# Check Python and Poetry
echo ""
echo "🐍 Checking Python setup..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_status 0 "Python3 installed: $PYTHON_VERSION"
else
    print_status 1 "Python3 not installed"
fi

if command -v poetry &> /dev/null; then
    POETRY_VERSION=$(poetry --version)
    print_status 0 "Poetry installed: $POETRY_VERSION"
else
    print_status 1 "Poetry not installed"
fi

# Check project files
echo ""
echo "📁 Checking project files..."
if [ -f "pyproject.toml" ]; then
    print_status 0 "pyproject.toml found"
else
    print_status 1 "pyproject.toml not found"
fi

if [[ "$PLATFORM" == "ios" || "$PLATFORM" == "both" ]]; then
    if [ -f "test_ios_simple.py" ]; then
        print_status 0 "test_ios_simple.py found"
    else
        print_status 1 "test_ios_simple.py not found"
    fi

    if [ -f "tests/test_login_ios.py" ]; then
        print_status 0 "tests/test_login_ios.py found"
    else
        print_status 1 "tests/test_login_ios.py not found"
    fi
fi

if [[ "$PLATFORM" == "android" || "$PLATFORM" == "both" ]]; then
    if [ -f "test_android_simple.py" ]; then
        print_status 0 "test_android_simple.py found"
    else
        print_status 1 "test_android_simple.py not found"
    fi

    if [ -f "tests/test_login_android.py" ]; then
        print_status 0 "tests/test_login_android.py found"
    else
        print_status 1 "tests/test_login_android.py not found"
    fi
fi

# Check GitHub Actions runner
echo ""
echo "🏃 Checking GitHub Actions runner..."
if [ -d "$HOME/actions-runner" ]; then
    print_status 0 "GitHub Actions runner directory found"
    
    if pgrep -f "actions-runner" > /dev/null; then
        print_status 0 "GitHub Actions runner is running"
    else
        print_warning "GitHub Actions runner not running - start with: cd ~/actions-runner && ./run.sh"
    fi
else
    print_status 1 "GitHub Actions runner not found"
fi

# Final summary
echo ""
echo "📊 Pre-flight Check Summary"
echo "=========================="

if [ "$PREFLIGHT_PASSED" = true ]; then
    echo -e "${GREEN}✅ All checks passed! Ready for $PLATFORM testing.${NC}"
    echo ""
    echo "🚀 You can now run the GitHub Actions workflows:"
    if [[ "$PLATFORM" == "ios" || "$PLATFORM" == "both" ]]; then
        echo "   📱 iOS: Go to Actions → 'iOS Real Device Testing'"
    fi
    if [[ "$PLATFORM" == "android" || "$PLATFORM" == "both" ]]; then
        echo "   🤖 Android: Go to Actions → 'Android Real Device Testing'"
    fi
    echo "   1. Go to https://github.com/Arm63/github-actions"
    echo "   2. Click 'Actions' → Select desired workflow"
    echo "   3. Click 'Run workflow'"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please fix the issues above.${NC}"
    echo ""
    echo "🔧 Common fixes:"
    if [[ "$PLATFORM" == "ios" || "$PLATFORM" == "both" ]]; then
        echo "   📱 iOS:"
        echo "     - Install missing tools: brew install libimobiledevice"
        echo "     - Connect and trust your iPhone"
        echo "     - Install XCUITest driver: appium driver install xcuitest"
    fi
    if [[ "$PLATFORM" == "android" || "$PLATFORM" == "both" ]]; then
        echo "   🤖 Android:"
        echo "     - Install missing tools: brew install android-platform-tools"
        echo "     - Connect Android device and enable USB debugging"
        echo "     - Install UiAutomator2 driver: appium driver install uiautomator2"
    fi
    echo "   📱 General:"
    echo "     - Install Liveboard app on device(s)"
    echo "     - Install Appium: npm install -g appium"
    exit 1
fi 