#!/usr/bin/env python3
"""
Enhanced iOS Test with Swipe/Scroll Functionality
Tests various swipe gestures, list scrolling, and navigation patterns
"""

import time
import os
import sys
from typing import Optional, Tuple, List, Dict, Any
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webdriver import WebDriver


class EnhancedIOSSwipeTest:
    """Enhanced iOS test class with comprehensive swipe/scroll functionality"""
    
    def __init__(self):
        self.driver: Optional[WebDriver] = None
        self.device_name = os.getenv('DEVICE_NAME', 'iPhone SE')
        self.platform_version = os.getenv('PLATFORM_VERSION', '17.2')
        self.device_udid = os.getenv('DEVICE_UDID', 'auto')
        self.team_id = os.getenv('TEAM_ID', '2FHJSTZ57U')
        self.screen_size = None
        
    def setup_driver(self) -> bool:
        """Setup iOS driver with optimized capabilities"""
        try:
            print(f"🚀 Setting up iOS driver for {self.device_name}")
            
            from appium.options.ios.xcuitest.base import XCUITestOptions
            
            options = XCUITestOptions()
            options.platform_name = "iOS"
            options.platform_version = self.platform_version
            options.device_name = self.device_name
            options.udid = self.device_udid
            options.bundle_id = "com.inconceptlabs.liveboard"
            options.automation_name = "XCUITest"
            options.new_command_timeout = 600
            options.wda_launch_timeout = 180000
            options.wda_connection_timeout = 180000
            
            # Team ID and WDA configuration
            options.set_capability("xcuitestTeamId", self.team_id)
            options.set_capability("updateWDABundleId", f"{self.team_id}.WebDriverAgentRunner")
            options.set_capability("showXcodeLog", True)
            options.set_capability("usePrebuiltWDA", True)
            
            # Performance optimizations
            options.set_capability("skipLogCapture", True)
            options.set_capability("reduceMotion", True)
            
            self.driver = webdriver.Remote('http://localhost:4723', options=options)
            self.driver.implicitly_wait(10)
            
            # Get screen size for swipe calculations
            self.screen_size = self.driver.get_window_size()
            print(f"📱 Screen size: {self.screen_size['width']}x{self.screen_size['height']}")
            
            print("✅ iOS driver setup completed!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup iOS driver: {e}")
            return False
    
    def take_screenshot(self, name: str = "screenshot") -> str:
        """Take a screenshot with timestamp"""
        timestamp = int(time.time())
        screenshot_name = f"ios_swipe_{name}_{timestamp}.png"
        if self.driver:
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
        """Swipe on a specific element"""
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
    # LIST SCROLLING METHODS
    # =========================
    
    def scroll_to_find_element(self, locator: Tuple[str, str], max_scrolls: int = 5, 
                              scroll_direction: str = 'up') -> Optional[WebElement]:
        """Scroll to find an element in a list"""
        print(f"🔍 Scrolling to find element: {locator}")
        
        for scroll_count in range(max_scrolls):
            # Check if element is already visible
            element = self.find_element_safe(locator)
            if element:
                print(f"✅ Found element after {scroll_count} scrolls")
                return element
            
            # Scroll to reveal more content
            if scroll_direction.lower() == 'up':
                self.swipe_up(duration=800, distance_ratio=0.3)
            elif scroll_direction.lower() == 'down':
                self.swipe_down(duration=800, distance_ratio=0.3)
            else:
                print(f"❌ Invalid scroll direction: {scroll_direction}")
                break
            
            time.sleep(1)
        
        print(f"❌ Element not found after {max_scrolls} scrolls")
        return None
    
    def scroll_list_to_top(self, list_element: Optional[WebElement] = None) -> bool:
        """Scroll a list to the top"""
        print("⬆️ Scrolling list to top...")
        
        # Try multiple swipes to reach the top
        for _ in range(5):
            if list_element:
                self.swipe_on_element(list_element, 'down', duration=500)
            else:
                self.swipe_down(duration=500, distance_ratio=0.4)
            time.sleep(0.5)
        
        return True
    
    def scroll_list_to_bottom(self, list_element: Optional[WebElement] = None) -> bool:
        """Scroll a list to the bottom"""
        print("⬇️ Scrolling list to bottom...")
        
        # Try multiple swipes to reach the bottom
        for _ in range(5):
            if list_element:
                self.swipe_on_element(list_element, 'up', duration=500)
            else:
                self.swipe_up(duration=500, distance_ratio=0.4)
            time.sleep(0.5)
        
        return True
    
    def get_list_items(self, list_locator: Tuple[str, str], 
                      item_locator: Tuple[str, str]) -> List[WebElement]:
        """Get all visible items in a list"""
        try:
            list_element = self.wait_for_element(list_locator, timeout=5)
            if not list_element:
                return []
            
            items = self.find_elements_safe(item_locator)
            print(f"📋 Found {len(items)} list items")
            return items
            
        except Exception as e:
            print(f"❌ Error getting list items: {e}")
            return []
    
    def scroll_through_list(self, list_locator: Tuple[str, str], 
                           item_locator: Tuple[str, str],
                           action_on_item: Optional[callable] = None) -> List[Dict[str, Any]]:
        """Scroll through entire list and optionally perform action on each item"""
        print("📜 Scrolling through entire list...")
        
        all_items = []
        seen_items = set()
        scroll_count = 0
        max_scrolls = 10
        
        # Start from top
        self.scroll_list_to_top()
        
        while scroll_count < max_scrolls:
            # Get current visible items
            items = self.get_list_items(list_locator, item_locator)
            
            if not items:
                print("❌ No items found in list")
                break
            
            # Process each visible item
            new_items_found = False
            for item in items:
                try:
                    # Get item identifier (text, accessibility id, etc.)
                    item_id = item.get_attribute('name') or item.get_attribute('text') or item.get_attribute('value')
                    
                    if item_id and item_id not in seen_items:
                        seen_items.add(item_id)
                        new_items_found = True
                        
                        item_info = {
                            'text': item_id,
                            'location': item.location,
                            'size': item.size,
                            'enabled': item.get_attribute('enabled'),
                            'visible': item.get_attribute('visible')
                        }
                        
                        all_items.append(item_info)
                        print(f"📌 Found item: {item_id}")
                        
                        # Perform action on item if provided
                        if action_on_item:
                            try:
                                action_on_item(item, item_info)
                            except Exception as e:
                                print(f"⚠️ Action failed on item {item_id}: {e}")
                
                except Exception as e:
                    print(f"⚠️ Error processing item: {e}")
            
            # If no new items found, we might have reached the end
            if not new_items_found:
                print("✅ Reached end of list (no new items)")
                break
            
            # Scroll to reveal more items
            self.swipe_up(duration=800, distance_ratio=0.3)
            scroll_count += 1
            time.sleep(1)
        
        print(f"📊 Scrolled through {len(all_items)} unique items")
        return all_items
    
    # =========================
    # NAVIGATION METHODS
    # =========================
    
    def swipe_to_navigate(self, direction: str, steps: int = 1) -> bool:
        """Use swipe gestures for navigation between screens"""
        print(f"🧭 Navigating {direction} with {steps} swipe(s)")
        
        for step in range(steps):
            if direction.lower() == 'back':
                # Swipe right to go back (common iOS gesture)
                self.swipe_right(duration=1000, distance_ratio=0.6)
            elif direction.lower() == 'forward':
                # Swipe left to go forward
                self.swipe_left(duration=1000, distance_ratio=0.6)
            elif direction.lower() == 'next':
                # Swipe up for next content
                self.swipe_up(duration=1000, distance_ratio=0.5)
            elif direction.lower() == 'previous':
                # Swipe down for previous content
                self.swipe_down(duration=1000, distance_ratio=0.5)
            else:
                print(f"❌ Invalid navigation direction: {direction}")
                return False
            
            time.sleep(1)
        
        return True
    
    def pull_to_refresh(self, element: Optional[WebElement] = None) -> bool:
        """Perform pull-to-refresh gesture"""
        print("🔄 Performing pull-to-refresh...")
        
        # Pull down from top of screen or element
        if element:
            self.swipe_on_element(element, 'down', duration=1500)
        else:
            # Start from top quarter of screen
            screen_width = self.screen_size['width']
            screen_height = self.screen_size['height']
            
            start_x = screen_width // 2
            start_y = screen_height // 4
            end_x = screen_width // 2
            end_y = int(screen_height * 0.75)
            
            self.driver.swipe(start_x, start_y, end_x, end_y, 1500)
        
        time.sleep(2)  # Wait for refresh to complete
        return True
    
    # =========================
    # MAIN TEST METHODS
    # =========================
    
    def test_swipe_navigation(self) -> bool:
        """Test various swipe navigation patterns"""
        print("\n🧪 Testing swipe navigation...")
        
        self.take_screenshot("before_swipe_navigation")
        
        # Test basic swipe directions
        print("⬆️ Testing upward swipe...")
        self.swipe_up(duration=1000, distance_ratio=0.4)
        self.take_screenshot("after_swipe_up")
        
        print("⬇️ Testing downward swipe...")
        self.swipe_down(duration=1000, distance_ratio=0.4)
        self.take_screenshot("after_swipe_down")
        
        print("⬅️ Testing left swipe...")
        self.swipe_left(duration=1000, distance_ratio=0.4)
        self.take_screenshot("after_swipe_left")
        
        print("➡️ Testing right swipe...")
        self.swipe_right(duration=1000, distance_ratio=0.4)
        self.take_screenshot("after_swipe_right")
        
        return True
    
    def test_list_scrolling(self) -> bool:
        """Test list scrolling and item finding"""
        print("\n🧪 Testing list scrolling...")
        
        # Common list locators for iOS
        list_locators = [
            (AppiumBy.CLASS_NAME, "XCUIElementTypeTable"),
            (AppiumBy.CLASS_NAME, "XCUIElementTypeCollectionView"),
            (AppiumBy.CLASS_NAME, "XCUIElementTypeScrollView"),
        ]
        
        # Common item locators
        item_locators = [
            (AppiumBy.CLASS_NAME, "XCUIElementTypeCell"),
            (AppiumBy.CLASS_NAME, "XCUIElementTypeButton"),
            (AppiumBy.CLASS_NAME, "XCUIElementTypeStaticText"),
        ]
        
        for list_locator in list_locators:
            list_element = self.find_element_safe(list_locator)
            if list_element:
                print(f"📋 Found list: {list_locator}")
                self.take_screenshot(f"found_list_{list_locator[1]}")
                
                # Test scrolling in the list
                for item_locator in item_locators:
                    items = self.scroll_through_list(list_locator, item_locator)
                    if items:
                        print(f"✅ Successfully scrolled through {len(items)} items")
                        break
                
                break
        
        return True
    
    def test_pull_to_refresh(self) -> bool:
        """Test pull-to-refresh functionality"""
        print("\n🧪 Testing pull-to-refresh...")
        
        self.take_screenshot("before_pull_to_refresh")
        
        # Find scrollable content
        scrollable_elements = [
            (AppiumBy.CLASS_NAME, "XCUIElementTypeScrollView"),
            (AppiumBy.CLASS_NAME, "XCUIElementTypeTable"),
            (AppiumBy.CLASS_NAME, "XCUIElementTypeCollectionView"),
        ]
        
        for locator in scrollable_elements:
            element = self.find_element_safe(locator)
            if element:
                print(f"📱 Found scrollable element: {locator}")
                self.pull_to_refresh(element)
                self.take_screenshot("after_pull_to_refresh")
                break
        else:
            # Try generic pull-to-refresh
            self.pull_to_refresh()
            self.take_screenshot("after_generic_pull_to_refresh")
        
        return True
    
    def test_search_with_scroll(self) -> bool:
        """Test finding elements by scrolling"""
        print("\n🧪 Testing search with scroll...")
        
        # Common elements to search for
        search_elements = [
            (AppiumBy.ACCESSIBILITY_ID, "Settings"),
            (AppiumBy.ACCESSIBILITY_ID, "Profile"),
            (AppiumBy.ACCESSIBILITY_ID, "Search"),
            (AppiumBy.XPATH, "//XCUIElementTypeButton[contains(@name, 'Login')]"),
            (AppiumBy.XPATH, "//XCUIElementTypeButton[contains(@name, 'Sign')]"),
        ]
        
        for locator in search_elements:
            print(f"🔍 Searching for: {locator}")
            element = self.scroll_to_find_element(locator, max_scrolls=3)
            if element:
                print(f"✅ Found element through scrolling: {locator}")
                self.take_screenshot(f"found_element_{locator[1]}")
                
                # Try to interact with the found element
                try:
                    element.click()
                    time.sleep(2)
                    self.take_screenshot(f"after_click_{locator[1]}")
                except Exception as e:
                    print(f"⚠️ Could not click element: {e}")
                
                break
        
        return True
    
    def run_all_swipe_tests(self) -> bool:
        """Run all swipe/scroll tests"""
        print("\n🚀 Starting Enhanced iOS Swipe Tests")
        print("=" * 50)
        
        if not self.setup_driver():
            return False
        
        try:
            # Wait for app to load
            print("⏳ Waiting for app to load...")
            time.sleep(5)
            self.take_screenshot("app_loaded")
            
            # Run all test methods
            tests = [
                self.test_swipe_navigation,
                self.test_list_scrolling,
                self.test_pull_to_refresh,
                self.test_search_with_scroll
            ]
            
            results = []
            for test in tests:
                try:
                    result = test()
                    results.append(result)
                    print(f"✅ {test.__name__}: {'PASSED' if result else 'FAILED'}")
                except Exception as e:
                    print(f"❌ {test.__name__}: FAILED - {e}")
                    results.append(False)
                
                time.sleep(2)
            
            # Summary
            passed = sum(results)
            total = len(results)
            print(f"\n📊 Test Results: {passed}/{total} tests passed")
            
            self.take_screenshot("tests_completed")
            return passed == total
            
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
            return False
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up driver and resources"""
        if self.driver:
            try:
                self.driver.quit()
                print("🧹 Driver cleanup completed")
            except Exception as e:
                print(f"⚠️ Driver cleanup warning: {e}")


def main():
    """Main function to run the enhanced swipe tests"""
    print("🚀 Enhanced iOS Swipe/Scroll Test Suite")
    print("=" * 50)
    
    test = EnhancedIOSSwipeTest()
    success = test.run_all_swipe_tests()
    
    if success:
        print("\n✅ All swipe/scroll tests completed successfully!")
    else:
        print("\n❌ Some swipe/scroll tests failed!")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 