import pytest
import time
import os
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sys
sys.path.append('..')


class TestLiveboardiOS:
    """Test class for Liveboard iOS application login flow."""
    
    def setup_method(self):
        """Setup method to initialize the driver before each test."""
        # Get device UDID from environment or use default
        device_udid = os.getenv('DEVICE_UDID', '00008030-000151561A85402E')
        device_name = os.getenv('DEVICE_NAME', 'iPhone SE')
        platform_version = os.getenv('PLATFORM_VERSION', '17.2')
        team_id = os.getenv('TEAM_ID', '2FHJSTZ57U')
        
        # Store device info
        self.device_name = device_name
        self.platform_version = platform_version
        
        # Configure iOS capabilities using dictionary
        capabilities = {
            'platformName': 'iOS',
            'platformVersion': platform_version,
            'deviceName': device_name,
            'udid': device_udid,
            'bundleId': 'com.inconceptlabs.liveboard',
            'automationName': 'XCUITest',
            'newCommandTimeout': 600,
            'wdaLaunchTimeout': 180000,
            'wdaConnectionTimeout': 180000,
            'xcuitestTeamId': team_id,
            'updateWDABundleId': f"{team_id}.WebDriverAgentRunner",
            'fullReset': True,  # Reset all app data to start fresh
            'noReset': False,   # Allow reset
            'shouldTerminateApp': True,  # Terminate app before starting
            'app': '/path/to/app.ipa',  # Will be ignored if not provided
            'autoLaunch': True,  # Launch app automatically
            'forceAppLaunch': True  # Force app launch even if already running
        }
        
        # Initialize driver
        from appium.options.ios.xcuitest.base import XCUITestOptions
        
        options = XCUITestOptions()
        options.platform_name = capabilities['platformName']
        options.platform_version = capabilities['platformVersion']
        options.device_name = capabilities['deviceName']
        options.udid = capabilities['udid']
        options.bundle_id = capabilities['bundleId']
        options.automation_name = capabilities['automationName']
        options.new_command_timeout = capabilities['newCommandTimeout']
        options.wda_launch_timeout = capabilities['wdaLaunchTimeout']
        options.wda_connection_timeout = capabilities['wdaConnectionTimeout']
        
        # Set additional capabilities
        options.set_capability("xcuitestTeamId", capabilities['xcuitestTeamId'])
        options.set_capability("updateWDABundleId", capabilities['updateWDABundleId'])
        
        from appium.webdriver.webdriver import WebDriver
        self.driver = WebDriver(
            command_executor='http://localhost:4723',
            options=options
        )
        
        # Set implicit wait
        self.driver.implicitly_wait(10)
        
        print(f"✅ Connected to iOS device: {device_name} (UDID: {device_udid})")
        
        # Explicitly terminate and reset the app
        try:
            print("🔄 Terminating app to ensure fresh start...")
            self.driver.terminate_app('com.inconceptlabs.liveboard')
            time.sleep(2)
            
            print("🚀 Launching app fresh...")
            self.driver.activate_app('com.inconceptlabs.liveboard')
            time.sleep(3)
            
            print("✅ App reset and launched fresh")
        except Exception as e:
            print(f"⚠️ App reset warning: {e}")
            print("🔄 Continuing with current app state...")
        
    def teardown_method(self):
        """Teardown method to quit the driver after each test."""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
            print("✅ Driver session ended")
    
    def take_screenshot(self, name="screenshot"):
        """Take a screenshot and save it with timestamp."""
        timestamp = int(time.time())
        filename = f"ios_test_{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"📸 Screenshot saved: {filename}")
        return filename
    
    def wait_and_click(self, by, locator, timeout=10):
        """Wait for element and click it."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, locator))
            )
            element.click()
            print(f"✅ Clicked element: {locator}")
            return True
        except TimeoutException:
            print(f"❌ Timeout waiting for clickable element: {locator}")
            return False
    
    def wait_for_element(self, by, locator, timeout=10):
        """Wait for element to be present."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
            print(f"✅ Found element: {locator}")
            return element
        except TimeoutException:
            print(f"❌ Timeout waiting for element: {locator}")
            return None
    
    def test_liveboard_login_flow(self):
        """Test the complete Liveboard iOS login flow."""
        print("\n🚀 Starting Liveboard iOS login flow test...")
        
        # Take initial screenshot
        self.take_screenshot("app_launch")
        
        # Wait for app to load
        time.sleep(3)
        
        try:
            # STEP 1: Click on "Log in" button using iOS Predicate String (most unique)
            print("🔍 Step 1: Looking for 'Log in' button...")
            
            # Using iOS Predicate String (removed coordinates for flexibility)
            log_in_predicate = "name == 'Log in' AND label == 'Log in' AND type == 'XCUIElementTypeButton'"
            
            if self.wait_and_click(AppiumBy.IOS_PREDICATE, log_in_predicate, timeout=15):
                print("✅ Successfully clicked 'Log in' button")
                self.take_screenshot("after_log_in_click")
                
                # Wait for new screen to load
                print("⏳ Waiting for new screen to load...")
                time.sleep(3)
                
                # STEP 2: Click on "Continue with Email" button
                print("🔍 Step 2: Looking for 'Continue with Email' button...")
                
                # Using iOS Predicate String (most unique from your options)
                continue_email_predicate = "name == 'Continue with Email' AND label == 'Continue with Email' AND type == 'XCUIElementTypeButton'"
                
                if self.wait_and_click(AppiumBy.IOS_PREDICATE, continue_email_predicate, timeout=15):
                    print("✅ Successfully clicked 'Continue with Email' button")
                    self.take_screenshot("after_continue_email_click")
                    
                    # Wait for email/password screen to load
                    print("⏳ Waiting for email/password screen to load...")
                    time.sleep(3)
                    
                    # STEP 3: Fill email field
                    print("🔍 Step 3: Looking for email input field...")
                    
                    # Using iOS Predicate String for email field
                    email_predicate = "value == 'Email address'"
                    email_field = self.wait_for_element(AppiumBy.IOS_PREDICATE, email_predicate, timeout=15)
                    
                    if email_field:
                        print("✅ Found email field")
                        email_field.clear()
                        email_field.send_keys("prod@mailinator.com")
                        print("✅ Entered email: prod@mailinator.com")
                        self.take_screenshot("email_filled")
                        
                        # STEP 4: Fill password field
                        print("🔍 Step 4: Looking for password input field...")
                        
                        # Using iOS Predicate String for password field
                        password_predicate = "value == 'Password'"
                        password_field = self.wait_for_element(AppiumBy.IOS_PREDICATE, password_predicate, timeout=15)
                        
                        if password_field:
                            print("✅ Found password field")
                            password_field.clear()
                            password_field.send_keys("testtest1")
                            print("✅ Entered password: testtest1")
                            self.take_screenshot("password_filled")
                            
                            # Wait a moment to see the filled form
                            time.sleep(2)
                            
                            # STEP 5: Click the final "Log in" button to submit the form
                            print("🔍 Step 5: Looking for final 'Log in' button to submit...")
                            
                            # Using iOS Predicate String for the submit button
                            submit_login_predicate = "name == 'Log in' AND label == 'Log in' AND type == 'XCUIElementTypeButton'"
                            
                            if self.wait_and_click(AppiumBy.IOS_PREDICATE, submit_login_predicate, timeout=15):
                                print("✅ Successfully clicked final 'Log in' button")
                                self.take_screenshot("after_login_submit")
                                
                                # Wait 4 seconds as requested
                                print("⏳ Waiting 4 seconds after login submission...")
                                time.sleep(4)
                                
                                print("✅ Login form completed successfully!")
                                self.take_screenshot("login_form_completed")
                            else:
                                print("❌ Could not click final 'Log in' button")
                                self.take_screenshot("login_submit_not_found")
                            
                        else:
                            print("❌ Could not find password field")
                            self.take_screenshot("password_field_not_found")
                            
                    else:
                        print("❌ Could not find email field")
                        self.take_screenshot("email_field_not_found")
                        
                else:
                    print("❌ Could not click 'Continue with Email' button")
                    self.take_screenshot("continue_email_not_found")
                    
            else:
                print("❌ Could not click 'Log in' button")
                self.take_screenshot("log_in_not_found")
            
            # Final screenshot
            self.take_screenshot("test_final_state")
            
            print("✅ Liveboard iOS login flow test completed!")
            
        except Exception as e:
            print(f"❌ Error during login flow test: {e}")
            self.take_screenshot("error_state")
            raise


if __name__ == "__main__":
    # Run the test directly
    test_instance = TestLiveboardiOS()
    test_instance.setup_method()
    try:
        test_instance.test_liveboard_login_flow()
    finally:
        test_instance.teardown_method()

