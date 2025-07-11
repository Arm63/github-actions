#!/bin/bash

echo "🚀 iOS Testing Pre-flight Check"
echo "================================"

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
echo "📱 Checking Liveboard app..."
if [ "$DEVICE_COUNT" -gt 0 ]; then
    if ideviceinstaller -l | grep -q "com.inconceptlabs.liveboard"; then
        LIVEBOARD_VERSION=$(ideviceinstaller -l | grep "com.inconceptlabs.liveboard" | cut -d'"' -f4)
        print_status 0 "Liveboard app installed (version: $LIVEBOARD_VERSION)"
    else
        print_status 1 "Liveboard app not installed"
        print_info "Please install Liveboard app on your device"
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
    
    # Check XCUITest driver
    appium driver list --installed > /tmp/drivers_check.txt 2>&1
    if grep -q "xcuitest" /tmp/drivers_check.txt; then
        XCUITEST_VERSION=$(grep "xcuitest" /tmp/drivers_check.txt | head -1)
        print_status 0 "XCUITest driver installed: $XCUITEST_VERSION"
    else
        print_status 1 "XCUITest driver not installed - run: appium driver install xcuitest"
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
    echo -e "${GREEN}✅ All checks passed! Ready for iOS testing.${NC}"
    echo ""
    echo "🚀 You can now run the GitHub Actions workflow:"
    echo "   1. Go to https://github.com/Arm63/github-actions"
    echo "   2. Click 'Actions' → 'iOS Real Device Testing'"
    echo "   3. Click 'Run workflow'"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please fix the issues above.${NC}"
    echo ""
    echo "🔧 Common fixes:"
    echo "   - Install missing tools: brew install libimobiledevice"
    echo "   - Connect and trust your iPhone"
    echo "   - Install Liveboard app on device"
    echo "   - Install Appium: npm install -g appium"
    echo "   - Install XCUITest driver: appium driver install xcuitest"
    exit 1
fi 