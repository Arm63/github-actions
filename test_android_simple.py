#!/usr/bin/env python3
"""
Simple Android test for Liveboard application.
This test connects to the device and navigates through the app.
"""

import time
import os
import sys

def test_android_connection():
    """Test Android device connection and Liveboard app navigation."""
    print("🚀 Starting Android Liveboard test...")
    
    # Get device configuration from environment
    device_udid = os.getenv('DEVICE_UDID', 'auto')
    device_name = os.getenv('DEVICE_NAME', 'Android Device')
    platform_version = os.getenv('PLATFORM_VERSION', '13')
    
    print(f"📱 Device: {device_name}")
    print(f"🆔 UDID: {device_udid}")
    print(f"🤖 Android: {platform_version}")
    
    try:
        # Try to import and use Appium
        from appium import webdriver
        from appium.webdriver.webdriver import WebDriver
        from appium.webdriver.common.appiumby import AppiumBy
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Configure Android capabilities
        capabilities = {
            'platformName': 'Android',
            'platformVersion': platform_version,
            'deviceName': device_name,
            'udid': device_udid,
            'appPackage': 'com.inconceptlabs.liveboard',
            'appActivity': 'com.inconceptlabs.liveboard.MainActivity',
            'automationName': 'UiAutomator2',
            'newCommandTimeout': 300,
            'uiautomator2ServerLaunchTimeout': 60000,
            'uiautomator2ServerInstallTimeout': 60000,
            'autoGrantPermissions': True,
            'noReset': True
        }
        
        print("🔗 Connecting to Appium server...")
        
        # Create driver with newer Appium syntax
        from appium.options.android.uiautomator2.base import UiAutomator2Options
        
        options = UiAutomator2Options()
        options.platform_name = capabilities['platformName']
        options.platform_version = capabilities['platformVersion']
        options.device_name = capabilities['deviceName']
        options.udid = capabilities['udid']
        options.app_package = capabilities['appPackage']
        options.app_activity = capabilities['appActivity']
        options.automation_name = capabilities['automationName']
        options.new_command_timeout = capabilities['newCommandTimeout']
        options.uiautomator2_server_launch_timeout = capabilities['uiautomator2ServerLaunchTimeout']
        options.uiautomator2_server_install_timeout = capabilities['uiautomator2ServerInstallTimeout']
        options.auto_grant_permissions = capabilities['autoGrantPermissions']
        options.no_reset = capabilities['noReset']
        
        # Initialize driver
        driver = WebDriver('http://localhost:4723', options=options)
        
        print("✅ Successfully connected to Android device!")
        
        # Wait for app to load
        time.sleep(5)
        
        # Take initial screenshot
        timestamp = int(time.time())
        screenshot_name = f"android_test_launch_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
        print(f"📸 Launch screenshot saved: {screenshot_name}")
        
        # Get current activity
        current_activity = driver.current_activity
        print(f"📱 Current activity: {current_activity}")
        
        # Get app package
        current_package = driver.current_package
        print(f"📦 Current package: {current_package}")
        
        # Wait for any element to ensure app is loaded
        wait = WebDriverWait(driver, 20)
        
        # Try to find common Android elements
        try:
            # Look for any clickable element
            clickable_elements = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
            print(f"🔍 Found {len(clickable_elements)} clickable elements")
            
            if clickable_elements:
                # Click the first clickable element
                first_element = clickable_elements[0]
                element_text = first_element.get_attribute('text') or first_element.get_attribute('content-desc') or 'Unknown element'
                print(f"👆 Clicking element: {element_text}")
                
                first_element.click()
                time.sleep(2)
                
                # Take screenshot after click
                screenshot_name = f"android_test_click_1_{timestamp}.png"
                driver.save_screenshot(screenshot_name)
                print(f"📸 Click screenshot saved: {screenshot_name}")
                
        except Exception as e:
            print(f"⚠️ Could not find clickable elements: {e}")
            
        # Try to find text elements
        try:
            text_elements = driver.find_elements(AppiumBy.XPATH, "//*[@text]")
            print(f"📝 Found {len(text_elements)} text elements")
            
            for i, element in enumerate(text_elements[:5]):  # Show first 5 text elements
                text = element.get_attribute('text')
                if text:
                    print(f"   {i+1}. {text}")
                    
        except Exception as e:
            print(f"⚠️ Could not find text elements: {e}")
            
        # Look for buttons
        try:
            buttons = driver.find_elements(AppiumBy.XPATH, "//*[@class='android.widget.Button']")
            print(f"🔘 Found {len(buttons)} buttons")
            
            if buttons:
                button = buttons[0]
                button_text = button.get_attribute('text') or button.get_attribute('content-desc') or 'Unknown button'
                print(f"🔘 First button: {button_text}")
                
                # Click the button if it exists
                if button.is_enabled():
                    button.click()
                    time.sleep(2)
                    
                    screenshot_name = f"android_test_button_click_{timestamp}.png"
                    driver.save_screenshot(screenshot_name)
                    print(f"📸 Button click screenshot saved: {screenshot_name}")
                    
        except Exception as e:
            print(f"⚠️ Could not find buttons: {e}")
            
        # Final screenshot
        screenshot_name = f"android_test_final_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
        print(f"📸 Final screenshot saved: {screenshot_name}")
        
        print("✅ Android test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure to install: poetry add appium-python-client selenium")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
        
    finally:
        try:
            if 'driver' in locals():
                driver.quit()
                print("🔌 Driver closed")
        except:
            pass

if __name__ == "__main__":
    success = test_android_connection()
    sys.exit(0 if success else 1) 