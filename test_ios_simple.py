#!/usr/bin/env python3
"""
Simple iOS test for Liveboard application.
This test connects to the device and navigates through the app.
"""

import time
import os
import sys

def test_ios_connection():
    """Test iOS device connection and Liveboard app navigation."""
    print("🚀 Starting iOS Liveboard test...")
    
    # Get device configuration from environment
    device_udid = os.getenv('DEVICE_UDID', '00008030-000151561A85402E')
    device_name = os.getenv('DEVICE_NAME', 'iPhone SE')
    platform_version = os.getenv('PLATFORM_VERSION', '17.2')
    team_id = os.getenv('TEAM_ID', '2FHJSTZ57U')
    
    print(f"📱 Device: {device_name}")
    print(f"🆔 UDID: {device_udid}")
    print(f"📱 iOS: {platform_version}")
    print(f"👥 Team ID: {team_id}")
    
    try:
        # Try to import and use Appium
        from appium import webdriver
        from appium.webdriver.common.appiumby import AppiumBy
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Configure iOS capabilities
        capabilities = {
            'platformName': 'iOS',
            'platformVersion': platform_version,
            'deviceName': device_name,
            'udid': device_udid,
            'bundleId': 'com.liveboard.LiveBoard',
            'automationName': 'XCUITest',
            'newCommandTimeout': 300,
            'wdaLaunchTimeout': 60000,
            'wdaConnectionTimeout': 60000,
            'xcuitestTeamId': team_id,
            'updateWDABundleId': f"{team_id}.WebDriverAgentRunner"
        }
        
        print("🔗 Connecting to Appium server...")
        
        # Create driver with newer Appium syntax
        from appium.options.ios.xcuitest.base import XCUITestOptions
        
        options = XCUITestOptions()
        options.platform_name = "iOS"
        options.platform_version = platform_version
        options.device_name = device_name
        options.udid = device_udid
        options.bundle_id = "com.inconceptlabs.liveboard"
        options.automation_name = "XCUITest"
        options.new_command_timeout = 600
        options.wda_launch_timeout = 180000
        options.wda_connection_timeout = 180000
        
        # Add team ID and WDA bundle ID using set_capability
        options.set_capability("xcuitestTeamId", team_id)
        options.set_capability("updateWDABundleId", f"{team_id}.WebDriverAgentRunner")
        options.set_capability("showXcodeLog", True)
        options.set_capability("usePrebuiltWDA", True)
        
        driver = webdriver.Remote('http://localhost:4723', options=options)
        driver.implicitly_wait(10)
        
        print("✅ Connected to iOS device successfully!")
        
        # Take initial screenshot
        timestamp = int(time.time())
        screenshot_name = f"ios_test_launch_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
        print(f"📸 Screenshot saved: {screenshot_name}")
        
        # Wait for app to load
        time.sleep(5)
        
        # Try to find any elements on screen
        print("🔍 Looking for UI elements...")
        
        # Get page source for debugging
        try:
            page_source = driver.page_source
            print("✅ Successfully retrieved page source")
            
            # Look for common iOS elements
            elements = driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeButton")
            print(f"Found {len(elements)} buttons")
            
            elements = driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeTextField")
            print(f"Found {len(elements)} text fields")
            
            elements = driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeStaticText")
            print(f"Found {len(elements)} text elements")
            
        except Exception as e:
            print(f"⚠️ Could not analyze page elements: {e}")
        
        # Try to interact with the app
        print("🎯 Attempting to interact with app...")
        
        # Find all clickable elements
        try:
            clickable_elements = driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeButton")
            
            if clickable_elements:
                print(f"Found {len(clickable_elements)} clickable elements")
                
                # Click on first few elements
                for i, element in enumerate(clickable_elements[:3]):
                    try:
                        element_name = element.get_attribute("name") or f"Button {i+1}"
                        if element.is_enabled() and element.is_displayed():
                            print(f"🔘 Clicking: {element_name}")
                            element.click()
                            time.sleep(2)
                            
                            # Take screenshot after click
                            screenshot_name = f"ios_test_click_{i+1}_{timestamp}.png"
                            driver.save_screenshot(screenshot_name)
                            print(f"📸 Screenshot saved: {screenshot_name}")
                            
                    except Exception as e:
                        print(f"⚠️ Could not click element {i+1}: {e}")
            else:
                print("No clickable elements found")
                
        except Exception as e:
            print(f"⚠️ Error finding clickable elements: {e}")
        
        # Final screenshot
        screenshot_name = f"ios_test_final_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
        print(f"📸 Final screenshot saved: {screenshot_name}")
        
        # Cleanup
        driver.quit()
        print("✅ Test completed successfully!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure Appium Python client is installed: pip install Appium-Python-Client")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_ios_connection()
    sys.exit(0 if success else 1) 