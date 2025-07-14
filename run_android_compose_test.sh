#!/bin/bash

# =============================================================================
# 🚀 Android Compose Testing Automation Script
# =============================================================================
# One-command Android Compose testing for Liveboard app
# Usage: ./run_android_compose_test.sh [test_type]
# Test types: login, navigation, text_input, all (default)
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
LIVEBOARD_PACKAGE="com.inconceptlabs.liveboard"
APPIUM_PORT="4723"
TEST_TYPE="${1:-all}"
RESULTS_DIR="android_compose_results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

print_step() {
    echo -e "${PURPLE}🚀 $1${NC}"
}

print_header() {
    echo -e "${CYAN}"
    echo "============================================================================="
    echo "$1"
    echo "============================================================================="
    echo -e "${NC}"
}

# Cleanup function
cleanup() {
    print_step "Cleaning up..."
    
    # Kill Appium if we started it
    if [ ! -z "$APPIUM_PID" ]; then
        print_info "Stopping Appium server (PID: $APPIUM_PID)"
        kill $APPIUM_PID 2>/dev/null || true
        wait $APPIUM_PID 2>/dev/null || true
    fi
    
    # Kill any remaining Appium processes
    pkill -f "appium" 2>/dev/null || true
    
    print_status "Cleanup completed"
}

# Set trap for cleanup on script exit
trap cleanup EXIT

# Main execution starts here
print_header "🤖 Android Compose Testing Automation"

print_info "Test Type: $TEST_TYPE"
print_info "Timestamp: $TIMESTAMP"
print_info "Results Directory: $RESULTS_DIR"

# Step 1: Check system requirements
print_step "Step 1: Checking system requirements..."

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script requires macOS for development setup"
    exit 1
fi
print_status "Running on macOS"

# Check ADB
if ! command -v adb &> /dev/null; then
    print_error "ADB not found. Install with: brew install android-platform-tools"
    exit 1
fi
print_status "ADB is available: $(adb --version | head -1)"

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python3 not found"
    exit 1
fi
print_status "Python3 is available: $(python3 --version)"

# Check Poetry
if ! command -v poetry &> /dev/null; then
    print_error "Poetry not found. Install from: https://python-poetry.org/"
    exit 1
fi
print_status "Poetry is available: $(poetry --version)"

# Check Node.js and Appium
if ! command -v node &> /dev/null; then
    print_error "Node.js not found"
    exit 1
fi
print_status "Node.js is available: $(node --version)"

if ! command -v appium &> /dev/null; then
    print_error "Appium not found. Install with: npm install -g appium"
    exit 1
fi
print_status "Appium is available: $(appium --version)"

# Step 2: Check Android device connection
print_step "Step 2: Checking Android device connection..."

# Start ADB server
adb start-server
sleep 2

# Check connected devices
DEVICE_COUNT=$(adb devices | grep -v "List of devices" | grep -c "device")
if [ "$DEVICE_COUNT" -eq 0 ]; then
    print_error "No Android device connected"
    print_info "Please:"
    print_info "  1. Connect your Android device via USB"
    print_info "  2. Enable Developer Options"
    print_info "  3. Enable USB Debugging"
    print_info "  4. Allow USB debugging on device"
    exit 1
fi

DEVICE_UDID=$(adb devices | grep -v "List of devices" | grep "device" | head -1 | awk '{print $1}')
print_status "Android device connected: $DEVICE_UDID"

# Get device info
DEVICE_NAME=$(adb -s "$DEVICE_UDID" shell getprop ro.product.model 2>/dev/null || echo "Unknown Device")
ANDROID_VERSION=$(adb -s "$DEVICE_UDID" shell getprop ro.build.version.release 2>/dev/null || echo "Unknown")
API_LEVEL=$(adb -s "$DEVICE_UDID" shell getprop ro.build.version.sdk 2>/dev/null || echo "Unknown")

print_info "Device: $DEVICE_NAME"
print_info "Android: $ANDROID_VERSION (API $API_LEVEL)"

# Export device info for tests
export DEVICE_UDID="$DEVICE_UDID"
export DEVICE_NAME="$DEVICE_NAME"
export PLATFORM_VERSION="$ANDROID_VERSION"

# Step 3: Check Liveboard app
print_step "Step 3: Checking Liveboard app..."

if adb -s "$DEVICE_UDID" shell pm list packages | grep -q "$LIVEBOARD_PACKAGE"; then
    print_status "Liveboard app is installed"
    
    # Get app version
    APP_VERSION=$(adb -s "$DEVICE_UDID" shell dumpsys package $LIVEBOARD_PACKAGE | grep "versionName" | head -1 | awk -F'=' '{print $2}' || echo "Unknown")
    print_info "App version: $APP_VERSION"
else
    print_error "Liveboard app not installed"
    print_info "Please install the Liveboard app on your device first"
    exit 1
fi

# Step 4: Check UiAutomator2 driver
print_step "Step 4: Checking UiAutomator2 driver..."

appium driver list --installed > /tmp/drivers_check.txt 2>&1
if grep -q "uiautomator2" /tmp/drivers_check.txt; then
    DRIVER_VERSION=$(grep "uiautomator2" /tmp/drivers_check.txt | head -1)
    print_status "UiAutomator2 driver installed: $DRIVER_VERSION"
else
    print_warning "UiAutomator2 driver not found, installing..."
    appium driver install uiautomator2
    print_status "UiAutomator2 driver installed"
fi

# Step 5: Setup Python environment
print_step "Step 5: Setting up Python environment..."

# Install dependencies
poetry install --no-root
print_status "Python dependencies installed"

# Step 6: Create results directory
print_step "Step 6: Creating results directory..."

mkdir -p "$RESULTS_DIR"
print_status "Results directory created: $RESULTS_DIR"

# Step 7: Start Appium server
print_step "Step 7: Starting Appium server..."

# Kill any existing Appium processes
pkill -f appium 2>/dev/null || true
sleep 2

# Check if port is available
if lsof -Pi :$APPIUM_PORT -sTCP:LISTEN -t >/dev/null ; then
    print_warning "Port $APPIUM_PORT is already in use, killing process..."
    lsof -ti:$APPIUM_PORT | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Start Appium in background
APPIUM_LOG="$RESULTS_DIR/appium_$TIMESTAMP.log"
appium --log "$APPIUM_LOG" --log-level debug --port $APPIUM_PORT &
APPIUM_PID=$!

print_info "Appium server starting (PID: $APPIUM_PID)"
print_info "Log file: $APPIUM_LOG"

# Wait for Appium to start
sleep 8

# Check if Appium is running
if ! kill -0 $APPIUM_PID 2>/dev/null; then
    print_error "Failed to start Appium server"
    print_info "Check log file: $APPIUM_LOG"
    exit 1
fi
print_status "Appium server is running"

# Step 8: Launch Liveboard app
print_step "Step 8: Launching Liveboard app..."

adb -s "$DEVICE_UDID" shell am start -n "$LIVEBOARD_PACKAGE/.MainActivity" 2>/dev/null || \
adb -s "$DEVICE_UDID" shell monkey -p "$LIVEBOARD_PACKAGE" -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1

sleep 3
print_status "Liveboard app launched"

# Step 9: Run Android Compose tests
print_step "Step 9: Running Android Compose tests..."

cd "$(dirname "$0")"

# Determine which tests to run
case "$TEST_TYPE" in
    "login")
        TEST_METHOD="test_liveboard_compose_login_flow"
        ;;
    "navigation")
        TEST_METHOD="test_compose_navigation_elements"
        ;;
    "text_input")
        TEST_METHOD="test_compose_text_input_elements"
        ;;
    "all"|*)
        TEST_METHOD=""
        ;;
esac

# Run the tests
if [ -z "$TEST_METHOD" ]; then
    print_info "Running all Android Compose tests..."
    PYTEST_CMD="poetry run pytest tests/test_login_android_compose.py -v -s --tb=short"
else
    print_info "Running specific test: $TEST_METHOD"
    PYTEST_CMD="poetry run pytest tests/test_login_android_compose.py::TestLiveboardAndroidCompose::$TEST_METHOD -v -s --tb=short"
fi

# Create test results file
TEST_RESULTS="$RESULTS_DIR/test_results_$TIMESTAMP.txt"

print_info "Executing: $PYTEST_CMD"
echo "Android Compose Test Results - $TIMESTAMP" > "$TEST_RESULTS"
echo "==========================================" >> "$TEST_RESULTS"
echo "Device: $DEVICE_NAME ($DEVICE_UDID)" >> "$TEST_RESULTS"
echo "Android: $ANDROID_VERSION (API $API_LEVEL)" >> "$TEST_RESULTS"
echo "Test Type: $TEST_TYPE" >> "$TEST_RESULTS"
echo "" >> "$TEST_RESULTS"

# Run tests and capture output
if eval "$PYTEST_CMD" 2>&1 | tee -a "$TEST_RESULTS"; then
    TEST_EXIT_CODE=0
    print_status "Android Compose tests completed successfully!"
else
    TEST_EXIT_CODE=$?
    print_warning "Android Compose tests completed with issues (exit code: $TEST_EXIT_CODE)"
fi

# Step 10: Collect artifacts
print_step "Step 10: Collecting test artifacts..."

# Move screenshots to results directory
if ls *.png 1> /dev/null 2>&1; then
    mv *.png "$RESULTS_DIR/" 2>/dev/null || true
    SCREENSHOT_COUNT=$(ls "$RESULTS_DIR"/*.png 2>/dev/null | wc -l)
    print_status "Moved $SCREENSHOT_COUNT screenshots to results directory"
fi

# Move XML files (page sources) to results directory
if ls *.xml 1> /dev/null 2>&1; then
    mv *.xml "$RESULTS_DIR/" 2>/dev/null || true
    XML_COUNT=$(ls "$RESULTS_DIR"/*.xml 2>/dev/null | wc -l)
    print_status "Moved $XML_COUNT XML files to results directory"
fi

# Copy device info
echo "DEVICE_UDID=$DEVICE_UDID" > "$RESULTS_DIR/device_info_$TIMESTAMP.env"
echo "DEVICE_NAME=$DEVICE_NAME" >> "$RESULTS_DIR/device_info_$TIMESTAMP.env"
echo "PLATFORM_VERSION=$ANDROID_VERSION" >> "$RESULTS_DIR/device_info_$TIMESTAMP.env"
echo "API_LEVEL=$API_LEVEL" >> "$RESULTS_DIR/device_info_$TIMESTAMP.env"

# Step 11: Generate summary report
print_step "Step 11: Generating summary report..."

SUMMARY_REPORT="$RESULTS_DIR/summary_$TIMESTAMP.md"

cat > "$SUMMARY_REPORT" << EOF
# 🤖 Android Compose Test Summary

**Timestamp:** $TIMESTAMP  
**Test Type:** $TEST_TYPE  
**Exit Code:** $TEST_EXIT_CODE  

## 📱 Device Information
- **Device:** $DEVICE_NAME
- **UDID:** $DEVICE_UDID
- **Android:** $ANDROID_VERSION (API $API_LEVEL)
- **App:** $LIVEBOARD_PACKAGE ($APP_VERSION)

## 📊 Test Results
$(if [ $TEST_EXIT_CODE -eq 0 ]; then echo "✅ **PASSED** - All tests completed successfully"; else echo "⚠️ **ISSUES** - Tests completed with exit code $TEST_EXIT_CODE"; fi)

## 📁 Generated Files
- Test Results: \`test_results_$TIMESTAMP.txt\`
- Appium Log: \`appium_$TIMESTAMP.log\`
- Device Info: \`device_info_$TIMESTAMP.env\`
- Screenshots: \`android_compose_*.png\`
- Page Sources: \`android_page_source_*.xml\`

## 🚀 Next Steps
1. Review test results in \`$TEST_RESULTS\`
2. Check screenshots for visual verification
3. Analyze Appium logs if needed: \`$APPIUM_LOG\`

---
*Generated by Android Compose Testing Automation*
EOF

print_status "Summary report generated: $SUMMARY_REPORT"

# Final summary
print_header "🎉 Test Execution Complete"

print_info "Results Location: $RESULTS_DIR"
print_info "Summary Report: $SUMMARY_REPORT"
print_info "Test Results: $TEST_RESULTS"
print_info "Screenshots: $RESULTS_DIR/*.png"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    print_status "All Android Compose tests passed! 🎉"
else
    print_warning "Tests completed with issues. Check results for details."
fi

print_info "Open results: open $RESULTS_DIR"

exit $TEST_EXIT_CODE 