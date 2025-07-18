#!/bin/bash

# Mobile Automation Environment Setup Script
# This script checks and installs all required tools for iOS and Android automation

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if directory exists
directory_exists() {
    [ -d "$1" ]
}

echo "🚀 Mobile Automation Environment Setup"
echo "======================================"
echo

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS. Please run on a macOS system."
    exit 1
fi

print_success "Detected macOS system"

# 1. Check and install Homebrew
print_status "Checking Homebrew..."
if ! command_exists brew; then
    print_warning "Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    print_success "Homebrew installed successfully"
else
    print_success "Homebrew is already installed"
fi

# 2. Check and install Python
print_status "Checking Python..."
if ! command_exists python3; then
    print_warning "Python 3 not found. Installing..."
    brew install python
    print_success "Python 3 installed successfully"
else
    PYTHON_VERSION=$(python3 --version)
    print_success "Python 3 is already installed: $PYTHON_VERSION"
fi

# 3. Check and install Poetry
print_status "Checking Poetry..."
if ! command_exists poetry; then
    print_warning "Poetry not found. Installing..."
    curl -sSL https://install.python-poetry.org | python3 -
    print_success "Poetry installed successfully"
    
    # Add Poetry to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    print_warning "Please restart your terminal or run: export PATH=\"\$HOME/.local/bin:\$PATH\""
else
    POETRY_VERSION=$(poetry --version)
    print_success "Poetry is already installed: $POETRY_VERSION"
fi

# 4. Check and install Node.js
print_status "Checking Node.js..."
if ! command_exists node; then
    print_warning "Node.js not found. Installing..."
    brew install node
    print_success "Node.js installed successfully"
else
    NODE_VERSION=$(node --version)
    print_success "Node.js is already installed: $NODE_VERSION"
fi

# 5. Check and install Appium
print_status "Checking Appium..."
if ! command_exists appium; then
    print_warning "Appium not found. Installing..."
    npm install -g appium
    print_success "Appium installed successfully"
else
    APPIUM_VERSION=$(appium --version)
    print_success "Appium is already installed: $APPIUM_VERSION"
fi

# 6. Check and install Appium drivers
print_status "Checking Appium drivers..."
if ! appium driver list | grep -q "uiautomator2"; then
    print_warning "UiAutomator2 driver not found. Installing..."
    appium driver install uiautomator2
    print_success "UiAutomator2 driver installed successfully"
else
    print_success "UiAutomator2 driver is already installed"
fi

if ! appium driver list | grep -q "xcuitest"; then
    print_warning "XCUITest driver not found. Installing..."
    appium driver install xcuitest
    print_success "XCUITest driver installed successfully"
else
    print_success "XCUITest driver is already installed"
fi

# 7. Check Xcode (for iOS development)
print_status "Checking Xcode..."
if ! command_exists xcodebuild; then
    print_error "Xcode not found. Please install Xcode from the App Store:"
    print_error "https://apps.apple.com/us/app/xcode/id497799835"
    print_warning "After installing Xcode, run: sudo xcode-select --install"
    print_warning "Then run this script again."
    exit 1
else
    XCODE_VERSION=$(xcodebuild -version | head -n 1)
    print_success "Xcode is installed: $XCODE_VERSION"
fi

# 8. Check Xcode Command Line Tools
print_status "Checking Xcode Command Line Tools..."
if ! xcode-select -p >/dev/null 2>&1; then
    print_warning "Xcode Command Line Tools not found. Installing..."
    sudo xcode-select --install
    print_warning "Please complete the Xcode Command Line Tools installation and run this script again."
    exit 1
else
    print_success "Xcode Command Line Tools are installed"
fi

# 9. Check Android SDK
print_status "Checking Android SDK..."
ANDROID_SDK_PATH="$HOME/Library/Android/sdk"
if ! directory_exists "$ANDROID_SDK_PATH"; then
    print_warning "Android SDK not found at $ANDROID_SDK_PATH"
    print_warning "Please install Android Studio and Android SDK:"
    print_warning "https://developer.android.com/studio"
    print_warning "After installation, run this script again."
    exit 1
else
    print_success "Android SDK found at $ANDROID_SDK_PATH"
fi

# 10. Check Android platform-tools
print_status "Checking Android platform-tools..."
if ! command_exists adb; then
    print_warning "Android platform-tools not found in PATH"
    print_warning "Adding Android SDK to PATH..."
    echo 'export ANDROID_HOME=$HOME/Library/Android/sdk' >> ~/.zshrc
    echo 'export ANDROID_SDK_ROOT=$ANDROID_HOME' >> ~/.zshrc
    echo 'export PATH=$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools' >> ~/.zshrc
    export ANDROID_HOME="$ANDROID_SDK_PATH"
    export ANDROID_SDK_ROOT="$ANDROID_SDK_PATH"
    export PATH="$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools"
    print_success "Android SDK environment variables set"
else
    print_success "Android platform-tools are available"
fi

# 11. Check Git
print_status "Checking Git..."
if ! command_exists git; then
    print_warning "Git not found. Installing..."
    brew install git
    print_success "Git installed successfully"
else
    GIT_VERSION=$(git --version)
    print_success "Git is already installed: $GIT_VERSION"
fi

# 12. Install Python dependencies
print_status "Installing Python dependencies..."
if [ -f "pyproject.toml" ]; then
    poetry install
    print_success "Python dependencies installed successfully"
else
    print_warning "pyproject.toml not found. Please ensure you're in the correct directory."
fi

# 13. Check for connected devices
print_status "Checking for connected devices..."
echo

# Check iOS devices
print_status "iOS devices:"
if command_exists xcrun; then
    xcrun devicectl list devices 2>/dev/null | grep -E "(iPhone|iPad)" || print_warning "No iOS devices found"
else
    print_warning "xcrun not available - cannot check iOS devices"
fi

# Check Android devices
print_status "Android devices:"
if command_exists adb; then
    adb devices | grep -v "List of devices" | grep -v "^$" || print_warning "No Android devices found"
else
    print_warning "adb not available - cannot check Android devices"
fi

echo
echo "======================================"
print_success "Environment setup completed!"
echo
print_status "Next steps:"
echo "1. Connect your iOS and Android devices"
echo "2. Trust the developer profile on your iOS device"
echo "3. Enable USB debugging on your Android device"
echo "4. Start Appium servers:"
echo "   - iOS: appium -p 4723"
echo "   - Android: appium -p 4724"
echo "5. Run tests: python test_parallel_mobile.py"
echo
print_warning "Note: You may need to restart your terminal for PATH changes to take effect."
echo
