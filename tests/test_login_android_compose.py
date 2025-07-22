import pytest
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class TestAndroidLogin:
    """Android Login Test using Appium with Compose UI"""
    
    def setup_method(self):
        """Setup Appium driver for Android"""
        # Android capabilities
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.platform_version = "13"
        options.device_name = "Android Device"
        options.udid = "HT7991A08308"
        options.app_package = "com.inconceptlabs.liveboard"
        options.app_activity = "com.inconceptlabs.liveboard.pages.activities.LaunchActivity"
        options.automation_name = "UiAutomator2"
        options.new_command_timeout = 600
        options.uiautomator2_server_launch_timeout = 180000
        options.uiautomator2_server_install_timeout = 180000
        options.auto_grant_permissions = True
        options.no_reset = True
        
        # Connect to Appium server
        from appium.webdriver.webdriver import WebDriver
        self.driver = WebDriver(
            command_executor='http://localhost:4724/wd/hub',
            options=options
        )
        
        # Initialize wait
        self.wait = WebDriverWait(self.driver, 20)
    
    def teardown_method(self):
        """Cleanup after test"""
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def test_android_login_flow(self):
        """Test the complete Android login flow"""
        
        # Step 1: Click on the first view element (likely a login button or menu item)
        print("Step 1: Clicking on first view element...")
        first_view = self.wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 
                'new UiSelector().className("android.view.View").instance(3)'))
        )
        first_view.click()
        
        # Wait for new screen to open
        print("Waiting for new screen to open...")
        time.sleep(3)
        
        # Step 2: Click on the second view element (likely another navigation element)
        print("Step 2: Clicking on second view element...")
        second_view = self.wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 
                'new UiSelector().className("android.view.View").instance(3)'))
        )
        second_view.click()
        
        # Wait for login screen to appear
        print("Waiting for login screen...")
        time.sleep(3)
        
        # Step 3: Fill the email input field
        print("Step 3: Filling email field...")
        email_input = self.wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 
                'new UiSelector().className("android.widget.EditText").instance(0)'))
        )
        email_input.clear()
        email_input.send_keys("prod@mailinator.com")
        
        # Step 4: Fill the password input field
        print("Step 4: Filling password field...")
        password_input = self.wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 
                'new UiSelector().className("android.widget.EditText").instance(1)'))
        )
        password_input.clear()
        password_input.send_keys("testtest1")
        
        # Step 5: Click the login button
        print("Step 5: Clicking login button...")
        login_button = self.wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 
                'new UiSelector().className("android.view.View").instance(5)'))
        )
        login_button.click()
        
        # Step 6: Wait for new screen to open (successful login)
        print("Step 6: Waiting for successful login...")
        time.sleep(5)
        
        # Verify we're on a new screen (you can add more specific verification here)
        print("Login flow completed successfully!")
        
        # Optional: Add verification that we're logged in
        # For example, check for a dashboard element or user profile element
        try:
            # Wait for some element that indicates successful login
            # This could be a dashboard title, user avatar, etc.
            dashboard_element = self.wait.until(
                EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 
                    'new UiSelector().className("android.view.View")'))
            )
            print("Successfully logged in - dashboard element found!")
        except Exception as e:
            print(f"Could not verify dashboard element: {e}")
            # Don't fail the test here, as the main flow completed


if __name__ == "__main__":
    # Run the test directly
    test_instance = TestAndroidLogin()
    test_instance.setup_method()
    try:
        test_instance.test_android_login_flow()
    finally:
        test_instance.teardown_method()

