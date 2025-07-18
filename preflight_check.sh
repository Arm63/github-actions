#!/bin/bash

# Pre-flight Check Script for Mobile Automation
# Quick verification that everything is ready for testing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[CHECK]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

echo "🔍 Pre-flight Check for Mobile Automation"
echo "========================================"
echo

# Initialize counters
total_checks=0
passed_checks=0
failed_checks=0

# 1. Check Python
print_status "Checking Python..."
total_checks=$((total_checks + 1))
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python 3: $PYTHON_VERSION"
    passed_checks=$((passed_checks + 1))
else
    print_error "Python 3 not found"
    failed_checks=$((failed_checks + 1))
fi

# 2. Check Poetry
print_status "Checking Poetry..."
total_checks=$((total_checks + 1))
if command_exists poetry; then
    POETRY_VERSION=$(poetry --version)
    print_success "Poetry: $POETRY_VERSION"
    passed_checks=$((passed_checks + 1))
else
    print_error "Poetry not found"
    failed_checks=$((failed_checks + 1))
fi

# 3. Check Node.js
print_status "Checking Node.js..."
total_checks=$((total_checks + 1))
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_success "Node.js: $NODE_VERSION"
    passed_checks=$((passed_checks + 1))
else
    print_error "Node.js not found"
    failed_checks=$((failed_checks + 1))
fi

# 4. Check Appium
print_status "Checking Appium..."
total_checks=$((total_checks + 1))
if command_exists appium; then
    APPIUM_VERSION=$(appium --version)
    print_success "Appium: $APPIUM_VERSION"
    passed_checks=$((passed_checks + 1))
else
    print_error "Appium not found"
    failed_checks=$((failed_checks + 1))
fi

# 5. Check Appium drivers
print_status "Checking Appium drivers..."
total_checks=$((total_checks + 1))
DRIVERS_OUTPUT="$(appium driver list)"
if [[ "$DRIVERS_OUTPUT" == *"uiautomator2"* && "$DRIVERS_OUTPUT" == *"xcuitest"* ]]; then
    print_success "Appium drivers: UiAutomator2 and XCUITest (present in driver list)"
    passed_checks=$((passed_checks + 1))
else
    print_error "Appium drivers missing (not found in driver list)"
    failed_checks=$((failed_checks + 1))
fi

# 6. Check Xcode
print_status "Checking Xcode..."
total_checks=$((total_checks + 1))
if command_exists xcodebuild; then
    XCODE_VERSION=$(xcodebuild -version | head -n 1)
    print_success "Xcode: $XCODE_VERSION"
    passed_checks=$((passed_checks + 1))
else
    print_error "Xcode not found"
    failed_checks=$((failed_checks + 1))
fi

# 7. Check Android SDK
print_status "Checking Android SDK..."
total_checks=$((total_checks + 1))
if [ -d "$HOME/Library/Android/sdk" ]; then
    print_success "Android SDK found"
    passed_checks=$((passed_checks + 1))
else
    print_error "Android SDK not found"
    failed_checks=$((failed_checks + 1))
fi

# 8. Check Android environment variables
print_status "Checking Android environment variables..."
total_checks=$((total_checks + 1))
if [ -n "$ANDROID_HOME" ] && [ -n "$ANDROID_SDK_ROOT" ]; then
    print_success "Android environment variables set"
    passed_checks=$((passed_checks + 1))
else
    print_warning "Android environment variables not set"
    print_warning "Run: export ANDROID_HOME=\$HOME/Library/Android/sdk"
    print_warning "Run: export ANDROID_SDK_ROOT=\$ANDROID_HOME"
    failed_checks=$((failed_checks + 1))
fi

# 9. Check adb
print_status "Checking ADB..."
total_checks=$((total_checks + 1))
if command_exists adb; then
    print_success "ADB available"
    passed_checks=$((passed_checks + 1))
else
    print_error "ADB not found"
    failed_checks=$((failed_checks + 1))
fi

# 10. Check iOS Appium server (port 4723)
print_status "Checking iOS Appium server (port 4723)..."
total_checks=$((total_checks + 1))
if port_in_use 4723; then
    print_success "iOS Appium server running on port 4723"
    passed_checks=$((passed_checks + 1))
else
    print_error "iOS Appium server not running on port 4723"
    print_warning "Start with: appium -p 4723"
    failed_checks=$((failed_checks + 1))
fi

# 11. Check Android Appium server (port 4724)
print_status "Checking Android Appium server (port 4724)..."
total_checks=$((total_checks + 1))
if port_in_use 4724; then
    print_success "Android Appium server running on port 4724"
    passed_checks=$((passed_checks + 1))
else
    print_error "Android Appium server not running on port 4724"
    print_warning "Start with: appium -p 4724"
    failed_checks=$((failed_checks + 1))
fi

# 12. Check connected devices
print_status "Checking connected devices..."
echo

# Check iOS devices
print_status "iOS devices:"
if command_exists xcrun; then
    IOS_DEVICES=$(xcrun devicectl list devices 2>/dev/null | grep -E "(iPhone|iPad)" | wc -l)
    if [ "$IOS_DEVICES" -gt 0 ]; then
        print_success "Found $IOS_DEVICES iOS device(s)"
        xcrun devicectl list devices 2>/dev/null | grep -E "(iPhone|iPad)" | while read line; do
            echo "  $line"
        done
        passed_checks=$((passed_checks + 1))
    else
        print_warning "No iOS devices found"
        failed_checks=$((failed_checks + 1))
    fi
else
    print_error "xcrun not available"
    failed_checks=$((failed_checks + 1))
fi
total_checks=$((total_checks + 1))

# Check Android devices
print_status "Android devices:"
if command_exists adb; then
    ANDROID_DEVICES=$(adb devices | grep -v "List of devices" | grep -v "^$" | wc -l)
    if [ "$ANDROID_DEVICES" -gt 0 ]; then
        print_success "Found $ANDROID_DEVICES Android device(s)"
        adb devices | grep -v "List of devices" | grep -v "^$" | while read line; do
            echo "  $line"
        done
        passed_checks=$((passed_checks + 1))
    else
        print_warning "No Android devices found"
        failed_checks=$((failed_checks + 1))
    fi
else
    print_error "adb not available"
    failed_checks=$((failed_checks + 1))
fi
total_checks=$((total_checks + 1))

# 13. Check Python dependencies
print_status "Checking Python dependencies..."
total_checks=$((total_checks + 1))
if [ -f "pyproject.toml" ]; then
    if poetry show >/dev/null 2>&1; then
        print_success "Python dependencies installed"
        passed_checks=$((passed_checks + 1))
    else
        print_warning "Python dependencies not installed"
        print_warning "Run: poetry install"
        failed_checks=$((failed_checks + 1))
    fi
else
    print_error "pyproject.toml not found"
    failed_checks=$((failed_checks + 1))
fi

echo
echo "========================================"
echo "📊 Pre-flight Check Summary"
echo "========================================"
echo "Total Checks: $total_checks"
echo "Passed: $passed_checks"
echo "Failed: $failed_checks"
echo

if [ $failed_checks -eq 0 ]; then
    print_success "All checks passed! Ready to run tests."
    echo
    print_status "You can now run:"
    echo "  python test_parallel_mobile.py"
    exit 0
else
    print_error "Some checks failed. Please fix the issues above."
    echo
    print_status "To fix setup issues, run:"
    echo "  ./setup_environment.sh"
    exit 1
fi 