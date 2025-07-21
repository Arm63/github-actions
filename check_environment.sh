#!/bin/bash

# Mobile Automation Environment Check Script
# Checks for all required tools, libraries, and environment variables

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[MISSING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "\n==== Mobile Automation Environment Check ===="

# 1. Homebrew
print_status "Checking Homebrew..."
if command_exists brew; then
    print_success "Homebrew is installed"
else
    print_warning "Homebrew is NOT installed"
fi

# 2. Python 3
print_status "Checking Python 3..."
if command_exists python3; then
    print_success "Python 3 is installed: $(python3 --version)"
else
    print_warning "Python 3 is NOT installed"
fi

# 3. Poetry
print_status "Checking Poetry..."
if command_exists poetry; then
    print_success "Poetry is installed: $(poetry --version)"
else
    print_warning "Poetry is NOT installed"
fi

# 4. Node.js
print_status "Checking Node.js..."
if command_exists node; then
    print_success "Node.js is installed: $(node --version)"
else
    print_warning "Node.js is NOT installed"
fi

# 5. npm
print_status "Checking npm..."
if command_exists npm; then
    print_success "npm is installed: $(npm --version)"
else
    print_warning "npm is NOT installed"
fi

# 6. Appium
print_status "Checking Appium..."
if command_exists appium; then
    print_success "Appium is installed: $(appium --version)"
else
    print_warning "Appium is NOT installed"
fi

# 7. Appium drivers
print_status "Checking Appium drivers..."
if command_exists appium; then
    if appium driver list | grep -q "uiautomator2"; then
        print_success "Appium UiAutomator2 driver is installed"
    else
        print_warning "Appium UiAutomator2 driver is NOT installed"
    fi
    if appium driver list | grep -q "xcuitest"; then
        print_success "Appium XCUITest driver is installed"
    else
        print_warning "Appium XCUITest driver is NOT installed"
    fi
else
    print_warning "Cannot check Appium drivers (Appium not installed)"
fi

# 8. Xcode
print_status "Checking Xcode..."
if command_exists xcodebuild; then
    print_success "Xcode is installed: $(xcodebuild -version | head -n 1)"
else
    print_warning "Xcode is NOT installed"
fi

# 9. Xcode Command Line Tools
print_status "Checking Xcode Command Line Tools..."
if xcode-select -p >/dev/null 2>&1; then
    print_success "Xcode Command Line Tools are installed"
else
    print_warning "Xcode Command Line Tools are NOT installed"
fi

# 10. Android SDK
print_status "Checking Android SDK..."
ANDROID_SDK_PATH="$HOME/Library/Android/sdk"
if [ -d "$ANDROID_SDK_PATH" ]; then
    print_success "Android SDK found at $ANDROID_SDK_PATH"
else
    print_warning "Android SDK NOT found at $ANDROID_SDK_PATH"
fi

# 11. Android platform-tools (adb)
print_status "Checking Android platform-tools (adb)..."
if command_exists adb; then
    print_success "adb is available"
else
    print_warning "adb is NOT available (platform-tools missing from PATH?)"
fi

# 12. Git
print_status "Checking Git..."
if command_exists git; then
    print_success "Git is installed: $(git --version)"
else
    print_warning "Git is NOT installed"
fi

# 13. Environment Variables
print_status "Checking ANDROID_HOME..."
if [ -n "$ANDROID_HOME" ]; then
    print_success "ANDROID_HOME is set: $ANDROID_HOME"
else
    print_warning "ANDROID_HOME is NOT set"
fi

print_status "Checking ANDROID_SDK_ROOT..."
if [ -n "$ANDROID_SDK_ROOT" ]; then
    print_success "ANDROID_SDK_ROOT is set: $ANDROID_SDK_ROOT"
else
    print_warning "ANDROID_SDK_ROOT is NOT set"
fi

print_status "Checking PATH for platform-tools..."
if echo "$PATH" | grep -q "platform-tools"; then
    print_success "PATH includes platform-tools"
else
    print_warning "PATH does NOT include platform-tools"
fi

# 14. Poetry Python dependencies
print_status "Checking Poetry Python dependencies..."
if [ -f "pyproject.toml" ]; then
    if command_exists poetry; then
        poetry check || print_warning "Poetry dependencies are NOT fully installed"
    else
        print_warning "Cannot check Poetry dependencies (Poetry not installed)"
    fi
else
    print_warning "pyproject.toml not found"
fi

echo -e "\n${BLUE}==== Environment check complete! ====${NC}\n" 