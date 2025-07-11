import pytest
import os
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy


@pytest.fixture(scope="session")
def ios_driver():
    """Create iOS driver for testing."""
    # Get device configuration from environment
    device_udid = os.getenv('DEVICE_UDID', 'auto')
    device_name = os.getenv('DEVICE_NAME', 'iPhone SE')
    platform_version = os.getenv('PLATFORM_VERSION', '17.2')
    team_id = os.getenv('TEAM_ID', '2FHJSTZ57U')
    
    # Configure iOS capabilities
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
    
    # Create driver
    driver = webdriver.Remote('http://localhost:4723/wd/hub', capabilities)
    driver.implicitly_wait(10)
    
    print(f"✅ Connected to iOS device: {device_name} (UDID: {device_udid})")
    
    yield driver
    
    # Cleanup
    driver.quit()
    print("✅ iOS driver session ended")


def take_screenshot(driver, name="screenshot"):
    """Take a screenshot and save it with timestamp."""
    timestamp = int(time.time())
    filename = f"ios_test_{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"📸 Screenshot saved: {filename}")
    return filename 