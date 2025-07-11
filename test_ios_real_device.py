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
    device_udid = "00008030-000151561A85402E"
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
    device_name = "iPhone SE"
    device_udid = "00008030-000151561A85402E"
    platform_version = "17.2"
    team_id = "2FHJSTZ57U"
    
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
