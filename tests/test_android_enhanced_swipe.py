#!/usr/bin/env python3
"""
Enhanced Android Test with Swipe/Scroll Functionality
Tests various swipe gestures, list scrolling, and navigation patterns for Jetpack Compose
"""

import pytest
import time
import os
from typing import Optional, Tuple, List, Dict, Any
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from appium.webdriver.webdriver import WebDriver


class TestAndroidEnhancedSwipe:
    """Enhanced Android test class with comprehensive swipe/scroll functionality for Compose"""
    
    def setup_method(self):
        """Setup Android driver with optimized capabilities"""
        # Get device configuration from environment
        device_udid = os.getenv('DEVICE_UDID', 'auto')
        device_name = os.getenv('DEVICE_NAME', 'Android Device')
        platform_version = os.getenv('PLATFORM_VERSION', '13')
        
        self.device_name = device_name
        self.platform_version = platform_version
        
        print(f"🚀 Setting up Android driver for {device_name}")
        
        # Configure Android capabilities for Compose testing
        from appium.options.android.uiautomator2.base import UiAutomator2Options
        
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.platform_version = platform_version
        options.device_name = device_name
        options.udid = device_udid
        options.app_package = 'com.inconceptlabs.liveboard'
        options.app_activity = 'com.inconceptlabs.liveboard.MainActivity'
        options.automation_name = 'UiAutomator2'
        options.new_command_timeout = 600
        options.uiautomator2_server_launch_timeout = 180000
        options.uiautomator2_server_install_timeout = 180000
        options.auto_grant_permissions = True
        options.no_reset = True
        options.disable_id_locator_autocompletion = True  # Better for Compose
        options.should_terminate_app = False
        
        # Performance optimizations
        options.set_capability("skipServerInstallation", True)
        options.set_capability("skipDeviceInitialization", True)
        options.set_capability("skipLogcatCapture", True)
        
        # Create driver instance
        self.driver = WebDriver('http://localhost:4723', options=options)
        print(f"✅ Android driver initialized for device: {device_name}")
        
        # Get screen size for swipe calculations
        self.screen_size = self.driver.get_window_size()
        print(f"📱 Screen size: {self.screen_size['width']}x{self.screen_size['height']}")
        
        # Wait for app to load
        time.sleep(5)
        
    def teardown_method(self):
        """Teardown method to clean up after each test"""
        if hasattr(self, 'driver') and self.driver:
            try:
                self.driver.quit()
                print("🧹 Android driver cleanup completed")
            except Exception as e:
                print(f"⚠️ Driver cleanup warning: {e}")
    
    def take_screenshot(self, name: str = "screenshot") -> str:
        """Take a screenshot with timestamp"""
        timestamp = int(time.time())
        screenshot_name = f"android_swipe_{name}_{timestamp}.png"
        self.driver.save_screenshot(screenshot_name)
        print(f"📸 Screenshot saved: {screenshot_name}")
        return screenshot_name
    
    def wait_for_element(self, locator: Tuple[str, str], timeout: int = 10) -> Optional[WebElement]:
        """Wait for element to be present with timeout"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            print(f"✅ Found element: {locator}")
            return element
        except TimeoutException:
            print(f"❌ Timeout waiting for element: {locator}")
            return None
    
    def find_element_safe(self, locator: Tuple[str, str]) -> Optional[WebElement]:
        """Find element safely without throwing exceptions"""
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException:
            return None
    
    def find_elements_safe(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Find elements safely without throwing exceptions"""
        try:
            return self.driver.find_elements(*locator)
        except NoSuchElementException:
            return []
    
    # =========================
    # SWIPE GESTURE METHODS
    # =========================
    
    def swipe_up(self, duration: int = 1000, distance_ratio: float = 0.5) -> bool:
        """Swipe up on screen"""
        try:
            screen_width = self.screen_size['width']
            screen_height = self.screen_size['height']
            
            start_x = screen_width // 2
            start_y = int(screen_height * (0.5 + distance_ratio / 2))
            end_x = screen_width // 2
            end_y = int(screen_height * (0.5 - distance_ratio / 2))
            
            print(f"⬆️ Swiping up: ({start_x}, {start_y}) → ({end_x}, {end_y})")
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"❌ Swipe up failed: {e}")
            return False
    
    def swipe_down(self, duration: int = 1000, distance_ratio: float = 0.5) -> bool:
        """Swipe down on screen"""
        try:
            screen_width = self.screen_size['width']
            screen_height = self.screen_size['height']
            
            start_x = screen_width // 2
            start_y = int(screen_height * (0.5 - distance_ratio / 2))
            end_x = screen_width // 2
            end_y = int(screen_height * (0.5 + distance_ratio / 2))
            
            print(f"⬇️ Swiping down: ({start_x}, {start_y}) → ({end_x}, {end_y})")
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"❌ Swipe down failed: {e}")
            return False
    
    def swipe_left(self, duration: int = 1000, distance_ratio: float = 0.5) -> bool:
        """Swipe left on screen"""
        try:
            screen_width = self.screen_size['width']
            screen_height = self.screen_size['height']
            
            start_x = int(screen_width * (0.5 + distance_ratio / 2))
            start_y = screen_height // 2
            end_x = int(screen_width * (0.5 - distance_ratio / 2))
            end_y = screen_height // 2
            
            print(f"⬅️ Swiping left: ({start_x}, {start_y}) → ({end_x}, {end_y})")
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"❌ Swipe left failed: {e}")
            return False
    
    def swipe_right(self, duration: int = 1000, distance_ratio: float = 0.5) -> bool:
        """Swipe right on screen"""
        try:
            screen_width = self.screen_size['width']
            screen_height = self.screen_size['height']
            
            start_x = int(screen_width * (0.5 - distance_ratio / 2))
            start_y = screen_height // 2
            end_x = int(screen_width * (0.5 + distance_ratio / 2))
            end_y = screen_height // 2
            
            print(f"➡️ Swiping right: ({start_x}, {start_y}) → ({end_x}, {end_y})")
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"❌ Swipe right failed: {e}")
            return False
    
    def swipe_on_element(self, element: WebElement, direction: str, duration: int = 1000) -> bool:
        """Swipe on a specific element (useful for Compose lists)"""
        try:
            location = element.location
            size = element.size
            
            center_x = location['x'] + size['width'] // 2
            center_y = location['y'] + size['height'] // 2
            
            swipe_distance = min(size['width'], size['height']) // 3
            
            if direction.lower() == 'up':
                start_x, start_y = center_x, center_y + swipe_distance
                end_x, end_y = center_x, center_y - swipe_distance
            elif direction.lower() == 'down':
                start_x, start_y = center_x, center_y - swipe_distance
                end_x, end_y = center_x, center_y + swipe_distance
            elif direction.lower() == 'left':
                start_x, start_y = center_x + swipe_distance, center_y
                end_x, end_y = center_x - swipe_distance, center_y
            elif direction.lower() == 'right':
                start_x, start_y = center_x - swipe_distance, center_y
                end_x, end_y = center_x + swipe_distance, center_y
            else:
                print(f"❌ Invalid swipe direction: {direction}")
                return False
            
            print(f"📱 Swiping {direction} on element: ({start_x}, {start_y}) → ({end_x}, {end_y})")
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            time.sleep(0.5)
            return True
            
        except Exception as e:
            print(f"❌ Swipe on element failed: {e}")
            return False
    
    # =========================
    # COMPOSE-SPECIFIC METHODS
    # =========================
    
    def find_compose_element(self, content_desc: str = None, text: str = None, 
                           class_name: str = None, timeout: int = 10) -> Optional[WebElement]:
        """Find compose elements using various strategies"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            
            # Try content description first (most reliable for Compose)
            if content_desc:
                locator = (AppiumBy.XPATH, f"//*[@content-desc='{content_desc}']")
                element = wait.until(EC.presence_of_element_located(locator))
                return element
            
            # Try text content
            if text:
                locator = (AppiumBy.XPATH, f"//*[@text='{text}']")
                element = wait.until(EC.presence_of_element_located(locator))
                return element
            
            # Try class name
            if class_name:
                locator = (AppiumBy.CLASS_NAME, class_name)
                element = wait.until(EC.presence_of_element_located(locator))
                return element
            
            return None
            
        except TimeoutException:
            print(f"❌ Compose element not found: content_desc={content_desc}, text={text}, class={class_name}")
            return None
    
    def scroll_compose_list(self, list_content_desc: str = None, direction: str = 'up', 
                          scrolls: int = 3) -> bool:
        """Scroll a Compose LazyColumn or LazyRow"""
        try:
            # Find the scrollable Compose list
            if list_content_desc:
                list_element = self.find_compose_element(content_desc=list_content_desc)
            else:
                # Try to find any scrollable element
                scrollable_locators = [
                    (AppiumBy.XPATH, "//android.widget.ScrollView"),
                    (AppiumBy.XPATH, "//androidx.recyclerview.widget.RecyclerView"),
                    (AppiumBy.XPATH, "//androidx.compose.ui.platform.AndroidComposeView"),
                ]
                
                list_element = None
                for locator in scrollable_locators:
                    list_element = self.find_element_safe(locator)
                    if list_element:
                        break
            
            if not list_element:
                print("❌ No scrollable list found")
                return False
            
            print(f"📜 Scrolling Compose list {direction} for {scrolls} times")
            
            # Perform scrolling
            for i in range(scrolls):
                if direction.lower() == 'up':
                    self.swipe_on_element(list_element, 'up', duration=800)
                elif direction.lower() == 'down':
                    self.swipe_on_element(list_element, 'down', duration=800)
                else:
                    print(f"❌ Invalid scroll direction: {direction}")
                    return False
                
                time.sleep(0.5)
            
            return True
            
        except Exception as e:
            print(f"❌ Compose list scroll failed: {e}")
            return False
    
    def find_compose_list_items(self, max_scrolls: int = 5) -> List[Dict[str, Any]]:
        """Find all items in a Compose list by scrolling"""
        print("🔍 Finding Compose list items...")
        
        all_items = []
        seen_items = set()
        
        # Common Compose item patterns
        item_patterns = [
            "//android.view.View[contains(@content-desc, 'item')]",
            "//android.view.View[contains(@content-desc, 'row')]",
            "//android.view.View[contains(@content-desc, 'card')]",
            "//android.widget.TextView",
            "//android.widget.Button",
        ]
        
        for scroll_count in range(max_scrolls):
            print(f"📜 Scroll {scroll_count + 1}/{max_scrolls}")
            
            # Look for items using different patterns
            for pattern in item_patterns:
                elements = self.find_elements_safe((AppiumBy.XPATH, pattern))
                
                for element in elements:
                    try:
                        # Get element info
                        content_desc = element.get_attribute('content-desc') or ''
                        text = element.get_attribute('text') or ''
                        class_name = element.get_attribute('class') or ''
                        
                        # Create unique identifier
                        item_id = f"{content_desc}_{text}_{element.location['y']}"
                        
                        if item_id not in seen_items:
                            seen_items.add(item_id)
                            
                            item_info = {
                                'content_desc': content_desc,
                                'text': text,
                                'class_name': class_name,
                                'location': element.location,
                                'size': element.size,
                                'enabled': element.get_attribute('enabled'),
                                'displayed': element.get_attribute('displayed')
                            }
                            
                            all_items.append(item_info)
                            print(f"📌 Found item: {content_desc or text or class_name}")
                    
                    except Exception as e:
                        print(f"⚠️ Error processing element: {e}")
            
            # Scroll to find more items
            if scroll_count < max_scrolls - 1:
                self.swipe_up(duration=800, distance_ratio=0.3)
                time.sleep(1)
        
        print(f"📊 Found {len(all_items)} unique items")
        return all_items
    
    # =========================
    # NAVIGATION METHODS
    # =========================
    
    def navigate_with_swipe(self, direction: str) -> bool:
        """Navigate using swipe gestures"""
        print(f"🧭 Navigating with swipe: {direction}")
        
        if direction.lower() == 'back':
            # Android back gesture - swipe from left edge
            start_x = 50
            start_y = self.screen_size['height'] // 2
            end_x = self.screen_size['width'] // 2
            end_y = start_y
            
            self.driver.swipe(start_x, start_y, end_x, end_y, 300)
            
        elif direction.lower() == 'drawer':
            # Open navigation drawer - swipe from left edge
            start_x = 50
            start_y = self.screen_size['height'] // 2
            end_x = self.screen_size['width'] // 2
            end_y = start_y
            
            self.driver.swipe(start_x, start_y, end_x, end_y, 500)
            
        elif direction.lower() == 'close_drawer':
            # Close navigation drawer - swipe left
            self.swipe_left(duration=500, distance_ratio=0.6)
            
        elif direction.lower() == 'tab_next':
            # Swipe to next tab
            self.swipe_left(duration=800, distance_ratio=0.4)
            
        elif direction.lower() == 'tab_previous':
            # Swipe to previous tab
            self.swipe_right(duration=800, distance_ratio=0.4)
            
        else:
            print(f"❌ Invalid navigation direction: {direction}")
            return False
        
        time.sleep(1)
        return True
    
    def pull_to_refresh(self) -> bool:
        """Perform pull-to-refresh gesture"""
        print("🔄 Performing pull-to-refresh...")
        
        # Start from top quarter of screen and pull down
        start_x = self.screen_size['width'] // 2
        start_y = self.screen_size['height'] // 4
        end_x = start_x
        end_y = int(self.screen_size['height'] * 0.75)
        
        self.driver.swipe(start_x, start_y, end_x, end_y, 1500)
        time.sleep(2)  # Wait for refresh animation
        
        return True
    
    # =========================
    # TEST METHODS
    # =========================
    
    def test_basic_swipe_gestures(self):
        """Test basic swipe gestures in all directions"""
        print("\n🧪 Testing basic swipe gestures...")
        
        self.take_screenshot("before_swipe_test")
        
        # Test all directions
        directions = ['up', 'down', 'left', 'right']
        
        for direction in directions:
            print(f"⚡ Testing {direction} swipe...")
            
            if direction == 'up':
                self.swipe_up(duration=1000, distance_ratio=0.4)
            elif direction == 'down':
                self.swipe_down(duration=1000, distance_ratio=0.4)
            elif direction == 'left':
                self.swipe_left(duration=1000, distance_ratio=0.4)
            elif direction == 'right':
                self.swipe_right(duration=1000, distance_ratio=0.4)
            
            self.take_screenshot(f"after_swipe_{direction}")
            time.sleep(1)
        
        print("✅ Basic swipe gestures test completed")
    
    def test_compose_list_scrolling(self):
        """Test scrolling in Compose lists"""
        print("\n🧪 Testing Compose list scrolling...")
        
        self.take_screenshot("before_list_scroll")
        
        # Find and scroll through lists
        items = self.find_compose_list_items(max_scrolls=3)
        
        if items:
            print(f"✅ Found {len(items)} items in lists")
            
            # Test targeted scrolling
            self.scroll_compose_list(direction='up', scrolls=2)
            self.take_screenshot("after_scroll_up")
            
            self.scroll_compose_list(direction='down', scrolls=2)
            self.take_screenshot("after_scroll_down")
            
        else:
            print("⚠️ No list items found, testing general scrolling")
            self.swipe_up(duration=1000, distance_ratio=0.5)
            self.take_screenshot("general_scroll_up")
            
            self.swipe_down(duration=1000, distance_ratio=0.5)
            self.take_screenshot("general_scroll_down")
        
        print("✅ Compose list scrolling test completed")
    
    def test_navigation_gestures(self):
        """Test navigation-specific gestures"""
        print("\n🧪 Testing navigation gestures...")
        
        self.take_screenshot("before_navigation")
        
        # Test drawer navigation
        print("📱 Testing drawer navigation...")
        self.navigate_with_swipe('drawer')
        self.take_screenshot("drawer_opened")
        
        self.navigate_with_swipe('close_drawer')
        self.take_screenshot("drawer_closed")
        
        # Test tab navigation
        print("📱 Testing tab navigation...")
        self.navigate_with_swipe('tab_next')
        self.take_screenshot("tab_next")
        
        self.navigate_with_swipe('tab_previous')
        self.take_screenshot("tab_previous")
        
        print("✅ Navigation gestures test completed")
    
    def test_pull_to_refresh_gesture(self):
        """Test pull-to-refresh functionality"""
        print("\n🧪 Testing pull-to-refresh...")
        
        self.take_screenshot("before_pull_refresh")
        
        # Perform pull-to-refresh
        self.pull_to_refresh()
        self.take_screenshot("after_pull_refresh")
        
        print("✅ Pull-to-refresh test completed")
    
    def test_element_interaction_with_scroll(self):
        """Test finding and interacting with elements through scrolling"""
        print("\n🧪 Testing element interaction with scroll...")
        
        # Common elements to look for
        target_elements = [
            {'content_desc': 'Login', 'text': None},
            {'content_desc': 'Sign In', 'text': None},
            {'content_desc': None, 'text': 'Login'},
            {'content_desc': None, 'text': 'Sign In'},
            {'content_desc': 'Settings', 'text': None},
            {'content_desc': 'Profile', 'text': None},
        ]
        
        for target in target_elements:
            print(f"🔍 Looking for element: {target}")
            
            # Try to find element with scrolling
            element = None
            for scroll_attempt in range(3):
                element = self.find_compose_element(
                    content_desc=target['content_desc'],
                    text=target['text'],
                    timeout=3
                )
                
                if element:
                    print(f"✅ Found element: {target}")
                    self.take_screenshot(f"found_{target['content_desc'] or target['text']}")
                    
                    # Try to interact with element
                    try:
                        element.click()
                        time.sleep(2)
                        self.take_screenshot(f"clicked_{target['content_desc'] or target['text']}")
                        print(f"✅ Successfully clicked element")
                        break
                    except Exception as e:
                        print(f"⚠️ Could not click element: {e}")
                    
                    break
                else:
                    # Scroll to find more elements
                    self.swipe_up(duration=800, distance_ratio=0.3)
                    time.sleep(1)
            
            if element:
                break
        
        print("✅ Element interaction with scroll test completed")
    
    def test_click_composable_android(self):
        """Main test method that runs all swipe/scroll tests"""
        print("\n🚀 Starting Enhanced Android Swipe/Scroll Tests")
        print("=" * 60)
        
        try:
            # Run all test methods
            self.test_basic_swipe_gestures()
            self.test_compose_list_scrolling()
            self.test_navigation_gestures()
            self.test_pull_to_refresh_gesture()
            self.test_element_interaction_with_scroll()
            
            print("\n✅ All swipe/scroll tests completed successfully!")
            self.take_screenshot("all_tests_completed")
            
        except Exception as e:
            print(f"\n❌ Test execution failed: {e}")
            self.take_screenshot("test_failed")
            raise


if __name__ == "__main__":
    # Run the test directly
    test = TestAndroidEnhancedSwipe()
    test.setup_method()
    
    try:
        test.test_click_composable_android()
        print("\n🎉 Direct test execution completed!")
    except Exception as e:
        print(f"\n💥 Direct test execution failed: {e}")
    finally:
        test.teardown_method() 