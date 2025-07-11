#!/bin/bash

echo "🚀 One-Command iOS Real Device Test (Dynamic Version)"
echo "===================================================="
echo "This script will setup everything AND run both tests!"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Global variables for device info
DEVICE_NAME=""
DEVICE_UDID=""
PLATFORM_VERSION=""
TEAM_ID=""

# Function to check macOS internet connection
check_macos_internet() {
    print_status "🌐 Checking macOS internet connection..."
    
    # Check if we can reach Apple's servers (required for code signing)
    if ping -c 1 apple.com &> /dev/null; then
        print_success "✅ macOS internet connection: OK"
        return 0
    else
        print_error "❌ macOS internet connection: FAILED"
        echo ""
        echo "🔧 Please check:"
        echo "1. WiFi/Ethernet connection on your Mac"
        echo "2. Firewall settings"
        echo "3. VPN connection if applicable"
        return 1
    fi
}

# Function to check iPhone internet connection
check_iphone_internet() {
    print_status "📱 Checking iPhone internet connection..."
    
    if [ -z "$DEVICE_UDID" ]; then
        print_warning "Device UDID not available, skipping iPhone internet check"
        return 0
    fi
    
    # Try to get device info which requires internet on device
    if ideviceinfo -u "$DEVICE_UDID" -k WiFiAddress &> /dev/null; then
        WIFI_ADDRESS=$(ideviceinfo -u "$DEVICE_UDID" -k WiFiAddress 2>/dev/null)
        if [ ! -z "$WIFI_ADDRESS" ] && [ "$WIFI_ADDRESS" != "(null)" ]; then
            print_success "✅ iPhone WiFi connection: OK ($WIFI_ADDRESS)"
            return 0
        else
            print_error "❌ iPhone WiFi connection: NOT CONNECTED"
            echo ""
            echo "📱 Please:"
            echo "1. Connect your iPhone to WiFi"
            echo "2. Make sure it has internet access"
            echo "3. WebDriverAgent needs internet to build properly"
            return 1
        fi
    else
        print_warning "⚠️  Could not verify iPhone internet connection"
        echo "   This might cause WebDriverAgent build issues"
        return 0
    fi
}

# Function to check both connections
check_network_connectivity() {
    print_status "🔍 Network Connectivity Check"
    echo "========================================"
    
    MACOS_OK=0
    IPHONE_OK=0
    
    # Check macOS internet
    if ! check_macos_internet; then
        MACOS_OK=1
    fi
    
    echo ""
    
    # Check iPhone internet
    if ! check_iphone_internet; then
        IPHONE_OK=1
    fi
    
    echo ""
    
    # Summary
    if [ $MACOS_OK -eq 0 ] && [ $IPHONE_OK -eq 0 ]; then
        print_success "🎉 All network checks passed!"
        return 0
    else
        print_error "❌ Network connectivity issues detected"
        echo ""
        echo "⚠️  Common WebDriverAgent errors are often caused by:"
        echo "   • iPhone not connected to WiFi"
        echo "   • macOS firewall blocking connections"
        echo "   • VPN interfering with Apple's servers"
        echo ""
        echo "🔧 Fix network issues before continuing..."
        return 1
    fi
}

# Check if we need to run setup
check_setup_needed() {
    NEED_SETUP=false
    
    # Check if key tools are missing
    if ! command -v appium &> /dev/null; then
        NEED_SETUP=true
    fi
    
    if ! command -v poetry &> /dev/null; then
        NEED_SETUP=true
    fi
    
    if ! command -v idevice_id &> /dev/null; then
        NEED_SETUP=true
    fi
    
    if [ ! -f "test_ios_real_device.py" ]; then
        NEED_SETUP=true
    fi
    
    if [ ! -f "tests/test_login_ios.py" ]; then
        NEED_SETUP=true
    fi
    
    if [ ! -f "pyproject.toml" ]; then
        NEED_SETUP=true
    fi
    
    echo $NEED_SETUP
}

# Run setup if needed
run_setup_if_needed() {
    if [ "$(check_setup_needed)" = "true" ]; then
        print_status "Setup needed. Running complete setup..."
        ./complete_ios_setup.sh
        
        # Reload shell environment
        source ~/.zprofile 2>/dev/null || true
        export PATH="$HOME/.local/bin:$PATH"
        
        print_success "Setup completed!"
    else
        print_success "Setup already complete!"
    fi
}

# Function to get device information from user
get_device_info() {
    print_status "📱 Device Configuration"
    echo "========================================"
    
    # Auto-detect connected device UDID
    if command -v idevice_id &> /dev/null; then
        AUTO_UDID=$(idevice_id -l)
        if [ ! -z "$AUTO_UDID" ]; then
            print_success "Auto-detected device UDID: $AUTO_UDID"
            echo ""
        fi
    fi
    
    # Get device name
    echo -n "📱 Enter device name (press Enter for default: iPhone SE): "
    read DEVICE_NAME
    if [ -z "$DEVICE_NAME" ]; then
        DEVICE_NAME="iPhone SE"
        print_success "Using default device name: $DEVICE_NAME"
    fi
    
    # Get device UDID
    if [ ! -z "$AUTO_UDID" ]; then
        echo -n "📱 Enter device UDID (press Enter for auto-detected: $AUTO_UDID): "
        read DEVICE_UDID
        if [ -z "$DEVICE_UDID" ]; then
            DEVICE_UDID="$AUTO_UDID"
            print_success "Using auto-detected UDID: $DEVICE_UDID"
        fi
    else
        echo -n "📱 Enter device UDID (get from: xcrun devicectl list devices): "
        read DEVICE_UDID
    fi
    
    if [ -z "$DEVICE_UDID" ]; then
        print_error "Device UDID is required!"
        exit 1
    fi
    
    # Get platform version
    echo -n "📱 Enter iOS platform version (press Enter for default: 17.2): "
    read PLATFORM_VERSION
    if [ -z "$PLATFORM_VERSION" ]; then
        PLATFORM_VERSION="17.2"
        print_success "Using default platform version: $PLATFORM_VERSION"
    fi
    
    # Get team ID
    echo -n "👨‍💻 Enter your Apple Team ID (press Enter for default: 2FHJSTZ57U): "
    read TEAM_ID
    if [ -z "$TEAM_ID" ]; then
        TEAM_ID="2FHJSTZ57U"
        print_success "Using default Team ID: $TEAM_ID"
    fi
    
    echo ""
    print_success "Device configuration completed!"
    echo "Device Name: $DEVICE_NAME"
    echo "Device UDID: $DEVICE_UDID"
    echo "Platform Version: $PLATFORM_VERSION"
    echo "Team ID: $TEAM_ID"
    echo ""
}

# Create dynamic conftest.py for real device testing
create_dynamic_conftest() {
    print_status "Creating dynamic conftest.py for real device testing..."
    
    cat > conftest_ios_real_device.py << EOF
import pytest
import subprocess
import socket
from appium import webdriver
from appium.options.ios.xcuitest.base import XCUITestOptions

def check_network_connectivity():
    """Check network connectivity before running tests"""
    print("🔍 Checking network connectivity...")
    
    # Check macOS internet
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("✅ macOS internet connection: OK")
        macos_ok = True
    except OSError:
        print("❌ macOS internet connection: FAILED")
        macos_ok = False
    
    # Check iPhone WiFi
    device_udid = '$DEVICE_UDID'
    try:
        result = subprocess.run(['ideviceinfo', '-u', device_udid, '-k', 'WiFiAddress'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            wifi_addr = result.stdout.strip()
            if wifi_addr and wifi_addr != "(null)":
                print(f"✅ iPhone WiFi connection: OK ({wifi_addr})")
                iphone_ok = True
            else:
                print("❌ iPhone WiFi connection: NOT CONNECTED")
                iphone_ok = False
        else:
            print("⚠️  Could not verify iPhone WiFi connection")
            iphone_ok = True
    except Exception:
        print("⚠️  Could not verify iPhone WiFi connection")
        iphone_ok = True
    
    if not macos_ok or not iphone_ok:
        print("❌ Network connectivity issues detected!")
        print("💡 Please fix network issues before running tests")
        return False
    
    print("🎉 Network connectivity check passed!")
    return True

@pytest.fixture(scope="function")
def ios_driver():
    """Fixture to create and manage iOS driver for real device testing"""
    
    # Check network connectivity first
    if not check_network_connectivity():
        pytest.fail("Network connectivity check failed. Please ensure both macOS and iPhone have internet access.")
    
    # Create Appium options for real device
    options = XCUITestOptions()
    options.platform_name = 'iOS'
    options.device_name = '$DEVICE_NAME'
    options.platform_version = '$PLATFORM_VERSION'
    options.udid = '$DEVICE_UDID'
    options.automation_name = 'XCUITest'
    options.bundle_id = 'com.inconceptlabs.liveboard'
    options.no_reset = True
    options.auto_accept_alerts = True
    options.new_command_timeout = 300
    options.show_xcode_log = True
    options.xcode_org_id = '$TEAM_ID'
    options.xcode_signing_id = 'iPhone Developer'
    
    try:
    # Create driver
    driver = webdriver.Remote('http://localhost:4723', options=options)
    
    yield driver
        
    except Exception as e:
        error_msg = str(e)
        if "xcodebuild failed with code 65" in error_msg:
            pytest.fail(f"WebDriverAgent build failed. Common causes: iPhone not on WiFi, developer certificate not trusted, or code signing issues. Original error: {error_msg}")
        elif "Unable to launch WebDriverAgent" in error_msg:
            pytest.fail(f"WebDriverAgent launch failed. Check network connectivity and developer certificate trust. Original error: {error_msg}")
        else:
            pytest.fail(f"iOS driver creation failed: {error_msg}")
    
    # Cleanup
    try:
        driver.quit()
    except:
        pass
EOF

    # Copy to tests directory
    cp conftest_ios_real_device.py tests/conftest.py
    
    print_success "Created dynamic conftest.py"
}

# Create dynamic test file
create_dynamic_test_file() {
    print_status "Creating dynamic test file..."
    
    cat > test_ios_real_device.py << EOF
#!/usr/bin/env python3
"""
iOS Real Device Test (Dynamic Version)
Simple test to verify iOS real device automation works
"""

import time
import subprocess
import socket
from appium import webdriver
from appium.options.ios.xcuitest.base import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy

def check_internet_connectivity():
    """Check if both macOS and iPhone have internet connectivity"""
    print("🔍 Checking network connectivity...")
    
    # Check macOS internet
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("✅ macOS internet connection: OK")
        macos_ok = True
    except OSError:
        print("❌ macOS internet connection: FAILED")
        macos_ok = False
    
    # Check iPhone WiFi (if possible)
    device_udid = "$DEVICE_UDID"
    try:
        result = subprocess.run(['ideviceinfo', '-u', device_udid, '-k', 'WiFiAddress'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            wifi_addr = result.stdout.strip()
            if wifi_addr and wifi_addr != "(null)":
                print(f"✅ iPhone WiFi connection: OK ({wifi_addr})")
                iphone_ok = True
            else:
                print("❌ iPhone WiFi connection: NOT CONNECTED")
                iphone_ok = False
        else:
            print("⚠️  Could not verify iPhone WiFi connection")
            iphone_ok = True  # Don't fail if we can't check
    except Exception:
        print("⚠️  Could not verify iPhone WiFi connection")
        iphone_ok = True  # Don't fail if we can't check
    
    if not macos_ok or not iphone_ok:
        print("❌ Network connectivity issues detected!")
        print("💡 Common solutions:")
        print("   • Connect iPhone to WiFi")
        print("   • Check macOS internet connection")
        print("   • Disable VPN if causing issues")
        print("   • Check firewall settings")
        return False
    
    print("🎉 All network checks passed!")
    return True

def test_ios_real_device():
    """Test iOS real device automation"""
    
    # Device configuration (from user input)
    device_name = "$DEVICE_NAME"
    device_udid = "$DEVICE_UDID"
    platform_version = "$PLATFORM_VERSION"
    team_id = "$TEAM_ID"
    
    print(f"Device Name: {device_name}")
    print(f"Device UDID: {device_udid}")
    print(f"Platform Version: {platform_version}")
    print(f"Team ID: {team_id}")
    print()
    
    # Check network connectivity first
    if not check_internet_connectivity():
        print("❌ Network connectivity check failed!")
        return False
    
    print()
    
    # Create Appium options
    options = XCUITestOptions()
    options.platform_name = 'iOS'
    options.device_name = device_name
    options.platform_version = platform_version
    options.udid = device_udid
    options.automation_name = 'XCUITest'
    options.bundle_id = 'com.inconceptlabs.liveboard'
    options.no_reset = True
    options.auto_accept_alerts = True
    options.new_command_timeout = 300
    options.show_xcode_log = True
    options.xcode_org_id = team_id
    options.xcode_signing_id = 'iPhone Developer'
    
    try:
        print("Connecting to Appium server...")
        driver = webdriver.Remote('http://localhost:4723', options=options)
        
        print("✅ Successfully connected to device!")
        print(f"Device: {device_name} (iOS {platform_version})")
        print(f"UDID: {device_udid}")
        
        # Take a screenshot
        screenshot_path = f"ios_test_screenshot_{int(time.time())}.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
        
        # Close the app
        driver.terminate_app('com.inconceptlabs.liveboard')
        print("App terminated successfully")
        
        driver.quit()
        print("✅ Test completed successfully!")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Test failed: {error_msg}")
        
        # Provide specific help for common errors
        if "xcodebuild failed with code 65" in error_msg:
            print()
            print("💡 This error is often caused by:")
            print("   • iPhone not connected to WiFi")
            print("   • Developer certificate not trusted on iPhone")
            print("   • Code signing issues")
            print()
            print("🔧 Try these solutions:")
            print("   1. Connect iPhone to WiFi")
            print("   2. Trust developer certificate: Settings → General → VPN & Device Management")
            print("   3. Check Team ID is correct")
        elif "Unable to launch WebDriverAgent" in error_msg:
            print()
            print("💡 WebDriverAgent launch failed - likely network issues:")
            print("   • Make sure iPhone is connected to WiFi")
            print("   • Check if macOS can reach Apple's servers")
            print("   • Temporarily disable VPN if active")
        
        return False

if __name__ == "__main__":
    test_ios_real_device()
EOF

    print_success "Created dynamic test file"
}

# This function was removed - device info is now gathered dynamically

# Run the tests
run_tests() {
    print_status "Starting iOS real device tests..."
    
    # Kill any existing Appium processes
    pkill -f appium 2>/dev/null || true
    sleep 2
    
    # Start Appium server in background
    print_status "Starting Appium server..."
    appium --log appium.log --log-level debug &
    APPIUM_PID=$!
    
    # Wait for Appium to start
    sleep 5
    
    # Check if Appium started successfully
    if ! kill -0 $APPIUM_PID 2>/dev/null; then
        print_error "Failed to start Appium server"
        exit 1
    fi
    
    print_success "Appium server started (PID: $APPIUM_PID)"
    
    # Get device information from user
    get_device_info
    
    # Check network connectivity before running tests
    echo ""
    if ! check_network_connectivity; then
        print_error "Please fix network connectivity issues before continuing"
        kill $APPIUM_PID 2>/dev/null || true
        exit 1
    fi
    
    # Create dynamic configuration files
    create_dynamic_test_file
    create_dynamic_conftest
    
    # Test 1: Simple connection test
    echo ""
    print_status "🧪 Test 1: Running simple connection test..."
    if poetry run python test_ios_real_device.py; then
        print_success "✅ Simple connection test passed!"
    else
        print_error "❌ Simple connection test failed!"
        echo "Stopping tests due to connection failure..."
        kill $APPIUM_PID 2>/dev/null || true
        exit 1
    fi
    
    # Test 2: Login test
    echo ""
    print_status "🧪 Test 2: Running login test (test_click_composable_ios)..."
    if poetry run pytest tests/test_login_ios.py::test_click_composable_ios -v --tb=short; then
        print_success "✅ Login test completed successfully!"
    else
        print_error "❌ Login test failed!"
        echo ""
        echo "📋 Troubleshooting:"
        echo "1. Check device connection: idevice_id -l"
        echo "2. View Appium logs: tail -f appium.log"
        echo "3. Trust developer on iPhone: Settings → General → VPN & Device Management"
        echo "4. Check if LiveBoard app is installed on device"
    fi
    
    # Stop Appium server
    print_status "Stopping Appium server..."
    kill $APPIUM_PID 2>/dev/null || true
    
    echo ""
    print_success "All tests completed!"
}

# Main execution
main() {
    echo "🔍 Checking current setup..."
    
    # Step 1: Run setup if needed
    run_setup_if_needed
    
    echo ""
    echo "🧪 Running tests..."
    
    # Step 2: Run the tests (device info will be gathered inside)
    run_tests
    
    echo ""
    echo "🎉 All done! Check the results above."
}

# Run main function
main 