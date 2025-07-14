import pytest
import time
import os
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestLiveboardAndroidCompose:
    """Test class for Liveboard Android application with Jetpack Compose screens."""
    
    def setup_method(self):
        """Setup method to initialize the driver before each test."""
        # Get device configuration from environment
        device_udid = os.getenv('DEVICE_UDID', 'auto')
        device_name = os.getenv('DEVICE_NAME', 'Android Device')
        platform_version = os.getenv('PLATFORM_VERSION', '13')
        
        # Configure Android capabilities for Compose testing
        capabilities = {
            'platformName': 'Android',
            'platformVersion': platform_version,
            'deviceName': device_name,
            'udid': device_udid,
            'appPackage': 'com.inconceptlabs.liveboard',
            'appActivity': 'com.inconceptlabs.liveboard.MainActivity',
            'automationName': 'UiAutomator2',
            'newCommandTimeout': 600,
            'uiautomator2ServerLaunchTimeout': 180000,
            'uiautomator2ServerInstallTimeout': 180000,
            'autoGrantPermissions': True,
            'noReset': True,
            'disableIdLocatorAutocompletion': True,  # Better for Compose
            'shouldTerminateApp': False
        }
        
        # Initialize driver with Compose-optimized options
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
        options.disable_id_locator_autocompletion = capabilities['disableIdLocatorAutocompletion']
        options.should_terminate_app = capabilities['shouldTerminateApp']
        
        # Create driver instance
        self.driver = WebDriver('http://localhost:4723', options=options)
        print(f"✅ Android Compose driver initialized for device: {device_name}")
        
        # Wait for app to load
        time.sleep(5)
        
    def teardown_method(self):
        """Teardown method to clean up after each test."""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
            print("🔌 Android Compose driver closed")
    
    def take_screenshot(self, name="screenshot"):
        """Take a screenshot with timestamp."""
        timestamp = int(time.time())
        screenshot_name = f"android_compose_{name}_{timestamp}.png"
        self.driver.save_screenshot(screenshot_name)
        print(f"📸 Screenshot saved: {screenshot_name}")
        return screenshot_name
    
    def wait_and_click_compose(self, locator, timeout=10):
        """Wait for compose element and click it."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            print(f"✅ Clicked compose element: {locator}")
            return True
        except TimeoutException:
            print(f"❌ Compose element not clickable within {timeout}s: {locator}")
            return False
    
    def find_compose_element(self, content_desc=None, text=None, class_name=None, timeout=10):
        """Find compose elements using various strategies."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            
            # Try content description first (most reliable for Compose)
            if content_desc:
                locator = (AppiumBy.XPATH, f"//*[@content-desc='{content_desc}']")
                element = wait.until(EC.presence_of_element_located(locator))
                print(f"✅ Found compose element by content-desc: {content_desc}")
                return element
            
            # Try text content
            if text:
                locator = (AppiumBy.XPATH, f"//*[@text='{text}']")
                element = wait.until(EC.presence_of_element_located(locator))
                print(f"✅ Found compose element by text: {text}")
                return element
            
            # Try class name
            if class_name:
                locator = (AppiumBy.CLASS_NAME, class_name)
                element = wait.until(EC.presence_of_element_located(locator))
                print(f"✅ Found compose element by class: {class_name}")
                return element
                
        except TimeoutException:
            print(f"❌ Compose element not found within {timeout}s")
            return None
    
    def test_liveboard_compose_login_flow(self):
        """Test the complete login flow on Jetpack Compose screens."""
        print("🚀 Starting Android Compose Login Flow Test...")
        
        # Take initial screenshot
        self.take_screenshot("login_flow_start")
        
        # Get current state
        current_activity = self.driver.current_activity
        current_package = self.driver.current_package
        print(f"📱 Current activity: {current_activity}")
        print(f"📦 Current package: {current_package}")
        
        # Wait for app to fully load
        time.sleep(5)
        
        # Step 1: Look for login screen elements
        print("\n🔍 Step 1: Looking for login screen...")
        
        # Common Compose login screen selectors
        login_selectors = [
            # Content description based (most reliable for Compose)
            (AppiumBy.XPATH, "//*[@content-desc='Login']"),
            (AppiumBy.XPATH, "//*[@content-desc='Sign In']"),
            (AppiumBy.XPATH, "//*[@content-desc='Log In']"),
            (AppiumBy.XPATH, "//*[@content-desc='Email']"),
            (AppiumBy.XPATH, "//*[@content-desc='Email Field']"),
            (AppiumBy.XPATH, "//*[@content-desc='Username']"),
            # Text based
            (AppiumBy.XPATH, "//*[@text='Login']"),
            (AppiumBy.XPATH, "//*[@text='Sign In']"),
            (AppiumBy.XPATH, "//*[@text='Log In']"),
            (AppiumBy.XPATH, "//*[@text='Email']"),
            # UiAutomator selectors for Compose
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Login")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Email")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Login")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Sign")'),
        ]
        
        login_element_found = False
        for selector in login_selectors:
            try:
                element = self.driver.find_element(selector[0], selector[1])
                print(f"✅ Found login element: {selector[1]}")
                login_element_found = True
                break
            except NoSuchElementException:
                continue
        
        if login_element_found:
            self.take_screenshot("login_screen_found")
            
            # Step 2: Fill email field
            print("\n📧 Step 2: Looking for email field...")
            email_selectors = [
                (AppiumBy.XPATH, "//*[@content-desc='Email']"),
                (AppiumBy.XPATH, "//*[@content-desc='Email Field']"),
                (AppiumBy.XPATH, "//*[@content-desc='Email Input']"),
                (AppiumBy.XPATH, "//*[@text='Email']"),
                (AppiumBy.XPATH, "//*[@text='Enter email']"),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Email")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Email")'),
                (AppiumBy.CLASS_NAME, "android.widget.EditText"),
            ]
            
            for selector in email_selectors:
                try:
                    email_field = self.driver.find_element(selector[0], selector[1])
                    print(f"✅ Found email field: {selector[1]}")
                    email_field.clear()
                    email_field.send_keys("test@liveboard.com")
                    print("✅ Entered test email")
                    self.take_screenshot("email_entered")
                    break
                except NoSuchElementException:
                    continue
                except Exception as e:
                    print(f"⚠️ Could not enter email: {e}")
            
            # Step 3: Fill password field
            print("\n🔐 Step 3: Looking for password field...")
            password_selectors = [
                (AppiumBy.XPATH, "//*[@content-desc='Password']"),
                (AppiumBy.XPATH, "//*[@content-desc='Password Field']"),
                (AppiumBy.XPATH, "//*[@content-desc='Password Input']"),
                (AppiumBy.XPATH, "//*[@text='Password']"),
                (AppiumBy.XPATH, "//*[@text='Enter password']"),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Password")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Password")'),
                (AppiumBy.CLASS_NAME, "android.widget.EditText"),
            ]
            
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(selector[0], selector[1])
                    print(f"✅ Found password field: {selector[1]}")
                    password_field.clear()
                    password_field.send_keys("testpassword123")
                    print("✅ Entered test password")
                    self.take_screenshot("password_entered")
                    break
                except NoSuchElementException:
                    continue
                except Exception as e:
                    print(f"⚠️ Could not enter password: {e}")
            
            # Step 4: Click login button
            print("\n🔘 Step 4: Looking for login button...")
            login_button_selectors = [
                (AppiumBy.XPATH, "//*[@content-desc='Login Button']"),
                (AppiumBy.XPATH, "//*[@content-desc='Sign In Button']"),
                (AppiumBy.XPATH, "//*[@content-desc='Log In Button']"),
                (AppiumBy.XPATH, "//*[@text='Login' and @clickable='true']"),
                (AppiumBy.XPATH, "//*[@text='Sign In' and @clickable='true']"),
                (AppiumBy.XPATH, "//*[@text='Log In' and @clickable='true']"),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Login").clickable(true)'),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Login").clickable(true)'),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").textContains("Login")'),
            ]
            
            for selector in login_button_selectors:
                try:
                    login_button = self.driver.find_element(selector[0], selector[1])
                    print(f"✅ Found login button: {selector[1]}")
                    login_button.click()
                    print("✅ Clicked login button")
                    self.take_screenshot("login_button_clicked")
                    break
                except NoSuchElementException:
                    continue
                except Exception as e:
                    print(f"⚠️ Could not click login button: {e}")
            
            # Step 5: Wait for login processing
            print("\n⏳ Step 5: Waiting for login processing...")
            time.sleep(5)
            self.take_screenshot("login_processing")
            
            # Step 6: Look for main screen or dashboard
            print("\n🏠 Step 6: Looking for main screen...")
            main_screen_selectors = [
                (AppiumBy.XPATH, "//*[@content-desc='Dashboard']"),
                (AppiumBy.XPATH, "//*[@content-desc='Home']"),
                (AppiumBy.XPATH, "//*[@content-desc='Main Screen']"),
                (AppiumBy.XPATH, "//*[@content-desc='Navigation']"),
                (AppiumBy.XPATH, "//*[@text='Dashboard']"),
                (AppiumBy.XPATH, "//*[@text='Home']"),
                (AppiumBy.XPATH, "//*[@text='Welcome']"),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Dashboard")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Home")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Dashboard")'),
            ]
            
            main_screen_found = False
            for selector in main_screen_selectors:
                try:
                    main_element = self.driver.find_element(selector[0], selector[1])
                    print(f"✅ Found main screen element: {selector[1]}")
                    main_screen_found = True
                    self.take_screenshot("main_screen_found")
                    break
                except NoSuchElementException:
                    continue
            
            if not main_screen_found:
                print("⚠️ Main screen not found, checking current state...")
                current_activity = self.driver.current_activity
                print(f"📱 Current activity after login: {current_activity}")
                self.take_screenshot("post_login_state")
                
        else:
            print("⚠️ No login screen found, checking current state...")
            self.take_screenshot("no_login_screen")
        
        # Final screenshot
        self.take_screenshot("login_flow_complete")
        print("✅ Android Compose login flow test completed!")
    
    def test_compose_navigation_elements(self):
        """Test navigation through Compose UI elements."""
        print("🚀 Starting Compose Navigation Test...")
        
        # Take initial screenshot
        self.take_screenshot("navigation_start")
        
        # Wait for app to load
        time.sleep(5)
        
        # Look for navigation elements
        print("🧭 Looking for navigation elements...")
        
        # Common Compose navigation selectors
        nav_selectors = [
            # Bottom navigation
            (AppiumBy.XPATH, "//*[@content-desc='Bottom Navigation']"),
            (AppiumBy.XPATH, "//*[@content-desc='Tab']"),
            (AppiumBy.XPATH, "//*[@content-desc='Navigation Tab']"),
            # Top app bar
            (AppiumBy.XPATH, "//*[@content-desc='Top App Bar']"),
            (AppiumBy.XPATH, "//*[@content-desc='Menu']"),
            (AppiumBy.XPATH, "//*[@content-desc='Navigation Menu']"),
            # Floating action button
            (AppiumBy.XPATH, "//*[@content-desc='Floating Action Button']"),
            (AppiumBy.XPATH, "//*[@content-desc='FAB']"),
            # Generic clickable elements
            (AppiumBy.XPATH, "//*[@clickable='true']"),
            # UiAutomator selectors
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Navigation")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Tab")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Menu")'),
        ]
        
        nav_elements_found = []
        for selector in nav_selectors:
            try:
                elements = self.driver.find_elements(selector[0], selector[1])
                if elements:
                    nav_elements_found.extend(elements)
                    print(f"✅ Found {len(elements)} navigation elements: {selector[1]}")
            except Exception as e:
                print(f"⚠️ Could not find elements with selector {selector[1]}: {e}")
        
        # Remove duplicates
        nav_elements_found = list(set(nav_elements_found))
        print(f"🔍 Total unique navigation elements found: {len(nav_elements_found)}")
        
        # Click on navigation elements
        clicked_count = 0
        for i, element in enumerate(nav_elements_found[:5]):  # Limit to first 5 elements
            try:
                element_desc = element.get_attribute('content-desc') or element.get_attribute('text') or f"Element {i+1}"
                print(f"🔘 Clicking navigation element: {element_desc}")
                element.click()
                time.sleep(2)
                self.take_screenshot(f"nav_click_{clicked_count + 1}")
                clicked_count += 1
            except Exception as e:
                print(f"⚠️ Could not click navigation element {i+1}: {e}")
        
        print(f"✅ Successfully clicked {clicked_count} navigation elements")
        
        # Final screenshot
        self.take_screenshot("navigation_complete")
        print("✅ Compose navigation test completed!")
    
    def test_compose_text_input_elements(self):
        """Test text input elements in Compose screens."""
        print("🚀 Starting Compose Text Input Test...")
        
        # Take initial screenshot
        self.take_screenshot("text_input_start")
        
        # Wait for app to load
        time.sleep(5)
        
        # Look for text input elements
        print("📝 Looking for text input elements...")
        
        # Compose text input selectors
        text_input_selectors = [
            (AppiumBy.XPATH, "//*[@content-desc='Text Field']"),
            (AppiumBy.XPATH, "//*[@content-desc='Input']"),
            (AppiumBy.XPATH, "//*[@content-desc='Search']"),
            (AppiumBy.XPATH, "//*[@content-desc='Search Field']"),
            (AppiumBy.CLASS_NAME, "android.widget.EditText"),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Field")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Input")'),
        ]
        
        text_inputs_found = []
        for selector in text_input_selectors:
            try:
                elements = self.driver.find_elements(selector[0], selector[1])
                if elements:
                    text_inputs_found.extend(elements)
                    print(f"✅ Found {len(elements)} text input elements: {selector[1]}")
            except Exception as e:
                print(f"⚠️ Could not find text inputs with selector {selector[1]}: {e}")
        
        # Remove duplicates
        text_inputs_found = list(set(text_inputs_found))
        print(f"📝 Total unique text input elements found: {len(text_inputs_found)}")
        
        # Interact with text inputs
        input_count = 0
        for i, element in enumerate(text_inputs_found[:3]):  # Limit to first 3 inputs
            try:
                element_desc = element.get_attribute('content-desc') or element.get_attribute('text') or f"Input {i+1}"
                print(f"⌨️ Interacting with text input: {element_desc}")
                element.clear()
                element.send_keys(f"Test input {i+1}")
                time.sleep(1)
                self.take_screenshot(f"text_input_{input_count + 1}")
                input_count += 1
            except Exception as e:
                print(f"⚠️ Could not interact with text input {i+1}: {e}")
        
        print(f"✅ Successfully interacted with {input_count} text input elements")
        
        # Final screenshot
        self.take_screenshot("text_input_complete")
        print("✅ Compose text input test completed!")


if __name__ == "__main__":
    # Run the test directly
    test_instance = TestLiveboardAndroidCompose()
    test_instance.setup_method()
    try:
        test_instance.test_liveboard_compose_login_flow()
        test_instance.test_compose_navigation_elements()
        test_instance.test_compose_text_input_elements()
    finally:
        test_instance.teardown_method() 