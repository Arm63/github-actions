import pytest
import time
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options

@pytest.fixture(scope="function")
def driver():
    """
    Fixture to create and manage Appium driver for Android tests.
    Scope: function - creates a new driver for each test
    """
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "49181JEKB05794"
    options.automation_name = "UiAutomator2"
    options.app_package = "com.inconceptlabs.liveboard"
    options.app_activity = "com.inconceptlabs.liveboard.pages.activities.SignInActivity"
    options.no_reset = True
    options.auto_grant_permissions = True
    options.new_command_timeout = 300

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    
    # Wait for app to load
    time.sleep(2)
    
    yield driver
    
    # Cleanup after test
    driver.quit() 