import pytest
import time
import os
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestLiveboardiOS:
    """Test class for Liveboard iOS application navigation."""
    
    def setup_method(self):
        """Setup method to initialize the driver before each test."""
        # Get device UDID from environment or use default
        device_udid = os.getenv('DEVICE_UDID', 'auto')
        device_name = os.getenv('DEVICE_NAME', 'iPhone SE')
        platform_version = os.getenv('PLATFORM_VERSION', '17.2')
        team_id = os.getenv('TEAM_ID', '2FHJSTZ57U')
        
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
            'updateWDABundleId': f"{team_id}.WebDriverAgentRunner"
        }
        
        # Initialize driver
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4723',
            desired_capabilities=capabilities
        )
        
        # Set implicit wait
        self.driver.implicitly_wait(10)
        
        print(f"✅ Connected to iOS device: {device_name} (UDID: {device_udid})")
        
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
    
    def wait_and_click(self, locator, timeout=10):
        """Wait for element and click it."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            print(f"✅ Clicked element: {locator}")
            return True
        except TimeoutException:
            print(f"❌ Timeout waiting for clickable element: {locator}")
            return False
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be present."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            print(f"✅ Found element: {locator}")
            return element
        except TimeoutException:
            print(f"❌ Timeout waiting for element: {locator}")
            return None
    
    def test_liveboard_navigation(self):
        """Test navigating through Liveboard application screens."""
        print("\n🚀 Starting Liveboard iOS navigation test...")
        
        # Take initial screenshot
        self.take_screenshot("app_launch")
        
        # Wait for app to load
        time.sleep(3)
        
        try:
            # Look for common login/welcome elements
            print("🔍 Looking for login or welcome screen...")
            
            # Try to find login button or email field
            login_elements = [
                (AppiumBy.ACCESSIBILITY_ID, "Log In"),
                (AppiumBy.ACCESSIBILITY_ID, "Sign In"),
                (AppiumBy.ACCESSIBILITY_ID, "Login"),
                (AppiumBy.XPATH, "//XCUIElementTypeButton[contains(@name, 'Log')]"),
                (AppiumBy.XPATH, "//XCUIElementTypeTextField[contains(@name, 'email')]"),
                (AppiumBy.XPATH, "//XCUIElementTypeTextField[contains(@name, 'Email')]"),
                (AppiumBy.CLASS_NAME, "XCUIElementTypeTextField"),
            ]
            
            login_found = False
            for locator in login_elements:
                element = self.wait_for_element(locator, timeout=5)
                if element:
                    print(f"✅ Found login element: {locator}")
                    login_found = True
                    break
            
            if login_found:
                self.take_screenshot("login_screen")
                
                # Try to interact with login elements
                print("🔐 Attempting to interact with login screen...")
                
                # Look for email field and enter test email
                email_selectors = [
                    (AppiumBy.XPATH, "//XCUIElementTypeTextField[contains(@name, 'email')]"),
                    (AppiumBy.XPATH, "//XCUIElementTypeTextField[contains(@name, 'Email')]"),
                    (AppiumBy.CLASS_NAME, "XCUIElementTypeTextField"),
                ]
                
                for selector in email_selectors:
                    email_field = self.wait_for_element(selector, timeout=3)
                    if email_field:
                        try:
                            email_field.clear()
                            email_field.send_keys("test@liveboard.com")
                            print("✅ Entered test email")
                            break
                        except Exception as e:
                            print(f"⚠️ Could not enter email: {e}")
                
                # Look for password field
                password_selectors = [
                    (AppiumBy.XPATH, "//XCUIElementTypeSecureTextField"),
                    (AppiumBy.XPATH, "//XCUIElementTypeTextField[contains(@name, 'password')]"),
                    (AppiumBy.XPATH, "//XCUIElementTypeTextField[contains(@name, 'Password')]"),
                ]
                
                for selector in password_selectors:
                    password_field = self.wait_for_element(selector, timeout=3)
                    if password_field:
                        try:
                            password_field.clear()
                            password_field.send_keys("testpassword")
                            print("✅ Entered test password")
                            break
                        except Exception as e:
                            print(f"⚠️ Could not enter password: {e}")
                
                self.take_screenshot("login_filled")
                
                # Try to click login button
                login_buttons = [
                    (AppiumBy.ACCESSIBILITY_ID, "Log In"),
                    (AppiumBy.ACCESSIBILITY_ID, "Sign In"),
                    (AppiumBy.ACCESSIBILITY_ID, "Login"),
                    (AppiumBy.XPATH, "//XCUIElementTypeButton[contains(@name, 'Log')]"),
                    (AppiumBy.XPATH, "//XCUIElementTypeButton[contains(@name, 'Sign')]"),
                ]
                
                for button_locator in login_buttons:
                    if self.wait_and_click(button_locator, timeout=3):
                        print("✅ Clicked login button")
                        break
                
                # Wait for potential login processing
                time.sleep(5)
                self.take_screenshot("after_login_attempt")
            
            # Look for main app content or dashboard
            print("🏠 Looking for main app content...")
            
            # Common dashboard/main screen elements
            main_elements = [
                (AppiumBy.ACCESSIBILITY_ID, "Dashboard"),
                (AppiumBy.ACCESSIBILITY_ID, "Home"),
                (AppiumBy.ACCESSIBILITY_ID, "Menu"),
                (AppiumBy.XPATH, "//XCUIElementTypeButton[contains(@name, 'Menu')]"),
                (AppiumBy.XPATH, "//XCUIElementTypeButton[contains(@name, 'Dashboard')]"),
                (AppiumBy.CLASS_NAME, "XCUIElementTypeNavigationBar"),
                (AppiumBy.CLASS_NAME, "XCUIElementTypeTabBar"),
            ]
            
            main_found = False
            for locator in main_elements:
                element = self.wait_for_element(locator, timeout=5)
                if element:
                    print(f"✅ Found main app element: {locator}")
                    main_found = True
                    break
            
            if main_found:
                self.take_screenshot("main_screen")
                
                # Try to navigate through tabs or menu items
                print("🧭 Attempting to navigate through app...")
                
                # Look for tab bar items
                try:
                    tab_buttons = self.driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeButton")
                    if tab_buttons:
                        print(f"Found {len(tab_buttons)} buttons to interact with")
                        
                        # Click on different tabs/buttons
                        for i, button in enumerate(tab_buttons[:3]):  # Limit to first 3 buttons
                            try:
                                button_name = button.get_attribute("name") or f"Button {i+1}"
                                print(f"🔘 Clicking button: {button_name}")
                                button.click()
                                time.sleep(2)
                                self.take_screenshot(f"button_{i+1}_{button_name.replace(' ', '_')}")
                            except Exception as e:
                                print(f"⚠️ Could not click button {i+1}: {e}")
                
                except Exception as e:
                    print(f"⚠️ Could not find tab buttons: {e}")
            
            # Final screenshot
            self.take_screenshot("final_state")
            
            print("✅ Liveboard navigation test completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during navigation test: {e}")
            self.take_screenshot("error_state")
            raise
    
    def test_click_composable_ios(self):
        """Test clicking composable elements in iOS Liveboard app."""
        print("\n🎯 Starting composable click test...")
        
        # Take initial screenshot
        self.take_screenshot("composable_test_start")
        
        # Wait for app to load
        time.sleep(3)
        
        try:
            # Look for clickable elements
            print("🔍 Looking for clickable composable elements...")
            
            # Find all clickable elements
            clickable_elements = self.driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeButton")
            clickable_elements.extend(self.driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeCell"))
            clickable_elements.extend(self.driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeOther"))
            
            print(f"Found {len(clickable_elements)} potentially clickable elements")
            
            # Click on a few elements
            clicked_count = 0
            for i, element in enumerate(clickable_elements[:5]):  # Limit to first 5 elements
                try:
                    element_name = element.get_attribute("name") or f"Element {i+1}"
                    if element.is_enabled() and element.is_displayed():
                        print(f"🔘 Clicking element: {element_name}")
                        element.click()
                        time.sleep(2)
                        self.take_screenshot(f"composable_click_{clicked_count+1}")
                        clicked_count += 1
                        
                        if clicked_count >= 3:  # Limit to 3 clicks
                            break
                except Exception as e:
                    print(f"⚠️ Could not click element {i+1}: {e}")
            
            print(f"✅ Successfully clicked {clicked_count} composable elements")
            
        except Exception as e:
            print(f"❌ Error during composable click test: {e}")
            self.take_screenshot("composable_error")
            raise
        
        # Final screenshot
        self.take_screenshot("composable_test_end")
        print("✅ Composable click test completed!")


if __name__ == "__main__":
    # Run the test directly
    test_instance = TestLiveboardiOS()
    test_instance.setup_method()
    try:
        test_instance.test_liveboard_navigation()
        test_instance.test_click_composable_ios()
    finally:
        test_instance.teardown_method() 