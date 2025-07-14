import pytest
import time
import os
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestLiveboardAndroid:
    """Test class for Liveboard Android application navigation."""
    
    def setup_method(self):
        """Setup method to initialize the driver before each test."""
        # Get device UDID from environment or use default
        device_udid = os.getenv('DEVICE_UDID', 'auto')
        device_name = os.getenv('DEVICE_NAME', 'Android Device')
        platform_version = os.getenv('PLATFORM_VERSION', '13')
        
        # Configure Android capabilities using dictionary
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
            'noReset': True
        }
        
        # Initialize driver
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
        
        # Create driver instance
        self.driver = WebDriver('http://localhost:4723', options=options)
        print(f"✅ Android driver initialized for device: {device_name}")
        
        # Wait for app to load
        time.sleep(5)
        
    def teardown_method(self):
        """Teardown method to clean up after each test."""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
            print("🔌 Android driver closed")
    
    def take_screenshot(self, name="screenshot"):
        """Take a screenshot with timestamp."""
        timestamp = int(time.time())
        screenshot_name = f"{name}_{timestamp}.png"
        self.driver.save_screenshot(screenshot_name)
        print(f"📸 Screenshot saved: {screenshot_name}")
        return screenshot_name
    
    def wait_and_click(self, locator, timeout=10):
        """Wait for element and click it."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            print(f"✅ Clicked element: {locator}")
            return True
        except TimeoutException:
            print(f"❌ Element not clickable within {timeout}s: {locator}")
            return False
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be present."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            print(f"✅ Element found: {locator}")
            return element
        except TimeoutException:
            print(f"❌ Element not found within {timeout}s: {locator}")
            return None
    
    def test_liveboard_navigation(self):
        """Test basic navigation in Liveboard Android app."""
        print("🚀 Starting Android Liveboard navigation test...")
        
        # Take initial screenshot
        self.take_screenshot("android_test_launch")
        
        # Get current activity and package
        current_activity = self.driver.current_activity
        current_package = self.driver.current_package
        print(f"📱 Current activity: {current_activity}")
        print(f"📦 Current package: {current_package}")
        
        # Wait for app to fully load
        time.sleep(3)
        
        # Find and interact with UI elements
        try:
            # Look for clickable elements
            clickable_elements = self.driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
            print(f"🔍 Found {len(clickable_elements)} clickable elements")
            
            if clickable_elements:
                # Click the first clickable element
                first_element = clickable_elements[0]
                element_text = first_element.get_attribute('text') or first_element.get_attribute('content-desc') or 'Unknown element'
                print(f"👆 Clicking element: {element_text}")
                
                first_element.click()
                time.sleep(2)
                self.take_screenshot("android_test_click_1")
                
        except Exception as e:
            print(f"⚠️ Could not interact with clickable elements: {e}")
            
        # Try to find text elements
        try:
            text_elements = self.driver.find_elements(AppiumBy.XPATH, "//*[@text]")
            print(f"📝 Found {len(text_elements)} text elements")
            
            for i, element in enumerate(text_elements[:5]):  # Show first 5 text elements
                text = element.get_attribute('text')
                if text:
                    print(f"   {i+1}. {text}")
                    
        except Exception as e:
            print(f"⚠️ Could not find text elements: {e}")
            
        # Look for buttons
        try:
            buttons = self.driver.find_elements(AppiumBy.XPATH, "//*[@class='android.widget.Button']")
            print(f"🔘 Found {len(buttons)} buttons")
            
            if buttons:
                button = buttons[0]
                button_text = button.get_attribute('text') or button.get_attribute('content-desc') or 'Unknown button'
                print(f"🔘 First button: {button_text}")
                
                # Click the button if it exists
                if button.is_enabled():
                    button.click()
                    time.sleep(2)
                    self.take_screenshot("android_test_button_click")
                    
        except Exception as e:
            print(f"⚠️ Could not find buttons: {e}")
            
        # Final screenshot
        self.take_screenshot("android_test_final")
        print("✅ Android navigation test completed!")
        
    def test_click_composable_android(self):
        """Test clicking composable elements in Android Liveboard app."""
        print("🚀 Starting Android Composable Click Test...")
        
        # Take initial screenshot
        self.take_screenshot("android_composable_launch")
        
        # Wait for app to load
        time.sleep(5)
        
        # Get current state
        current_activity = self.driver.current_activity
        current_package = self.driver.current_package
        print(f"📱 Current activity: {current_activity}")
        print(f"📦 Current package: {current_package}")
        
        # Test different element finding strategies
        strategies = [
            ("ID", AppiumBy.ID),
            ("CLASS_NAME", AppiumBy.CLASS_NAME),
            ("XPATH", AppiumBy.XPATH),
            ("ACCESSIBILITY_ID", AppiumBy.ACCESSIBILITY_ID),
            ("ANDROID_UIAUTOMATOR", AppiumBy.ANDROID_UIAUTOMATOR)
        ]
        
        for strategy_name, strategy in strategies:
            print(f"\n🔍 Testing {strategy_name} strategy...")
            
            try:
                if strategy == AppiumBy.ID:
                    # Try common Android IDs
                    common_ids = [
                        "android:id/button1",
                        "android:id/button2",
                        "android:id/content",
                        "com.inconceptlabs.liveboard:id/main_button",
                        "com.inconceptlabs.liveboard:id/login_button"
                    ]
                    
                    for element_id in common_ids:
                        try:
                            element = self.driver.find_element(strategy, element_id)
                            print(f"✅ Found element by ID: {element_id}")
                            if element.is_enabled():
                                element.click()
                                time.sleep(2)
                                self.take_screenshot(f"android_click_{strategy_name}_{element_id.split(':')[-1]}")
                                break
                        except NoSuchElementException:
                            continue
                            
                elif strategy == AppiumBy.CLASS_NAME:
                    # Try common Android classes
                    common_classes = [
                        "android.widget.Button",
                        "android.widget.TextView",
                        "android.widget.EditText",
                        "android.widget.ImageView",
                        "android.view.View"
                    ]
                    
                    for class_name in common_classes:
                        try:
                            elements = self.driver.find_elements(strategy, class_name)
                            if elements:
                                print(f"✅ Found {len(elements)} elements of class: {class_name}")
                                # Click the first clickable element
                                for element in elements:
                                    if element.is_enabled() and element.get_attribute('clickable') == 'true':
                                        element_text = element.get_attribute('text') or element.get_attribute('content-desc') or 'Unknown'
                                        print(f"👆 Clicking {class_name}: {element_text}")
                                        element.click()
                                        time.sleep(2)
                                        self.take_screenshot(f"android_click_{strategy_name}_{class_name.split('.')[-1]}")
                                        break
                                break
                        except NoSuchElementException:
                            continue
                            
                elif strategy == AppiumBy.XPATH:
                    # Try common XPath expressions
                    common_xpaths = [
                        "//*[@clickable='true']",
                        "//*[@text and @clickable='true']",
                        "//android.widget.Button[@enabled='true']",
                        "//*[@class='android.widget.Button']",
                        "//*[@content-desc and @clickable='true']"
                    ]
                    
                    for xpath in common_xpaths:
                        try:
                            elements = self.driver.find_elements(strategy, xpath)
                            if elements:
                                print(f"✅ Found {len(elements)} elements with XPath: {xpath}")
                                # Click the first element
                                element = elements[0]
                                element_text = element.get_attribute('text') or element.get_attribute('content-desc') or 'Unknown'
                                print(f"👆 Clicking XPath element: {element_text}")
                                element.click()
                                time.sleep(2)
                                self.take_screenshot(f"android_click_{strategy_name}_xpath_{len(elements)}")
                                break
                        except NoSuchElementException:
                            continue
                            
                elif strategy == AppiumBy.ACCESSIBILITY_ID:
                    # Try to find elements by accessibility ID
                    try:
                        elements = self.driver.find_elements(strategy, "")
                        # This might not work directly, so let's find elements with content-desc
                        elements_with_desc = self.driver.find_elements(AppiumBy.XPATH, "//*[@content-desc]")
                        if elements_with_desc:
                            print(f"✅ Found {len(elements_with_desc)} elements with content-desc")
                            element = elements_with_desc[0]
                            desc = element.get_attribute('content-desc')
                            print(f"👆 Clicking accessibility element: {desc}")
                            element.click()
                            time.sleep(2)
                            self.take_screenshot(f"android_click_{strategy_name}_desc")
                    except Exception as e:
                        print(f"⚠️ Accessibility ID strategy failed: {e}")
                        
                elif strategy == AppiumBy.ANDROID_UIAUTOMATOR:
                    # Try UiAutomator selectors
                    uiautomator_queries = [
                        'new UiSelector().clickable(true)',
                        'new UiSelector().className("android.widget.Button")',
                        'new UiSelector().textContains("Login")',
                        'new UiSelector().textContains("Sign")',
                        'new UiSelector().descriptionContains("button")'
                    ]
                    
                    for query in uiautomator_queries:
                        try:
                            element = self.driver.find_element(strategy, query)
                            print(f"✅ Found element with UiAutomator: {query}")
                            element_text = element.get_attribute('text') or element.get_attribute('content-desc') or 'Unknown'
                            print(f"👆 Clicking UiAutomator element: {element_text}")
                            element.click()
                            time.sleep(2)
                            self.take_screenshot(f"android_click_{strategy_name}_uiautomator")
                            break
                        except NoSuchElementException:
                            continue
                        except Exception as e:
                            print(f"⚠️ UiAutomator query failed: {query} - {e}")
                            continue
                            
            except Exception as e:
                print(f"❌ {strategy_name} strategy failed: {e}")
                continue
        
        # Final screenshot
        self.take_screenshot("android_composable_final")
        print("✅ Android composable click test completed!")
        
    def test_app_info_android(self):
        """Test getting app information on Android."""
        print("🚀 Starting Android App Info Test...")
        
        # Take initial screenshot
        self.take_screenshot("android_info_launch")
        
        # Get app information
        print(f"📱 Current activity: {self.driver.current_activity}")
        print(f"📦 Current package: {self.driver.current_package}")
        
        # Get device information
        try:
            device_info = self.driver.get_device_time()
            print(f"🕐 Device time: {device_info}")
        except Exception as e:
            print(f"⚠️ Could not get device time: {e}")
            
        # Get app state
        try:
            app_state = self.driver.query_app_state('com.inconceptlabs.liveboard')
            print(f"📱 App state: {app_state}")
        except Exception as e:
            print(f"⚠️ Could not get app state: {e}")
            
        # Get page source for debugging
        try:
            page_source = self.driver.page_source
            print(f"📄 Page source length: {len(page_source)} characters")
            
            # Save page source to file for debugging
            with open(f"android_page_source_{int(time.time())}.xml", 'w') as f:
                f.write(page_source)
            print("📄 Page source saved to XML file")
            
        except Exception as e:
            print(f"⚠️ Could not get page source: {e}")
            
        # Final screenshot
        self.take_screenshot("android_info_final")
        print("✅ Android app info test completed!") 