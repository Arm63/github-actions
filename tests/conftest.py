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
    
    # Support different Appium ports for parallel execution
    appium_port = os.getenv('APPIUM_PORT', '4723')  # Default to 4723 for iOS
    appium_url = f'http://localhost:{appium_port}/wd/hub'
    
    driver = webdriver.Remote(appium_url, options.to_capabilities())
    driver.implicitly_wait(10)
    
    print(f"✅ Connected to iOS device: {device_name} (UDID: {device_udid})")
    
    yield driver
    
    # Cleanup
    driver.quit()
    print("✅ iOS driver session ended")


@pytest.fixture(scope="session")
def driver():
    """Create Android driver for testing."""
    # Get device configuration from environment
    device_udid = os.getenv('ANDROID_DEVICE_UDID', 'auto')
    device_name = os.getenv('ANDROID_DEVICE_NAME', 'Android Device')
    platform_version = os.getenv('ANDROID_PLATFORM_VERSION', '11.0')
    
    # Configure Android capabilities
    capabilities = {
        'platformName': 'Android',
        'platformVersion': platform_version,
        'deviceName': device_name,
        'udid': device_udid,
        'appPackage': 'com.inconceptlabs.liveboard',
        'appActivity': '.pages.activities.LaunchActivity',
        'automationName': 'UiAutomator2',
        'newCommandTimeout': 600,
        'uiautomator2ServerLaunchTimeout': 180000,
        'uiautomator2ServerInstallTimeout': 180000,
        'autoGrantPermissions': True,
        'noReset': True,
        'fullReset': False
    }
    
    from appium.options.android.uiautomator2.base import UiAutomator2Options
    
    options = UiAutomator2Options()
    options.load_capabilities(capabilities)
    
    # Support different Appium ports for parallel execution
    appium_port = os.getenv('APPIUM_PORT', '4724')  # Default to 4724 for Android
    appium_url = f'http://localhost:{appium_port}'
    
    driver = webdriver.Remote(appium_url, options=options)
    driver.implicitly_wait(10)
    
    print(f"✅ Connected to Android device: {device_name} (UDID: {device_udid})")
    
    yield driver
    
    # Cleanup
    driver.quit()
    print("✅ Android driver session ended")


def take_screenshot(driver, name="screenshot"):
    """Take a screenshot and save it with timestamp."""
    timestamp = int(time.time())
    filename = f"android_test_{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"📸 Screenshot saved: {filename}")
    return filename 