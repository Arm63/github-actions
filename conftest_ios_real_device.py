import pytest
import subprocess
import socket
from appium import webdriver
from appium.options.ios.xcuitest.base import XCUITestOptions

def check_network_connectivity():
    """Check network connectivity before running tests"""
    print("🔍 Checking network connectivity...")
    
    # Check macOS internet
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("✅ macOS internet connection: OK")
        macos_ok = True
    except OSError:
        print("❌ macOS internet connection: FAILED")
        macos_ok = False
    
    # Check iPhone WiFi
    device_udid = '00008030-000151561A85402E'
    try:
        result = subprocess.run(['ideviceinfo', '-u', device_udid, '-k', 'WiFiAddress'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            wifi_addr = result.stdout.strip()
            if wifi_addr and wifi_addr != "(null)":
                print(f"✅ iPhone WiFi connection: OK ({wifi_addr})")
                iphone_ok = True
            else:
                print("❌ iPhone WiFi connection: NOT CONNECTED")
                iphone_ok = False
        else:
            print("⚠️  Could not verify iPhone WiFi connection")
            iphone_ok = True
    except Exception:
        print("⚠️  Could not verify iPhone WiFi connection")
        iphone_ok = True
    
    if not macos_ok or not iphone_ok:
        print("❌ Network connectivity issues detected!")
        print("💡 Please fix network issues before running tests")
        return False
    
    print("🎉 Network connectivity check passed!")
    return True

@pytest.fixture(scope="function")
def ios_driver():
    """Fixture to create and manage iOS driver for real device testing"""
    
    # Check network connectivity first
    if not check_network_connectivity():
        pytest.fail("Network connectivity check failed. Please ensure both macOS and iPhone have internet access.")
    
    # Create Appium options for real device
    options = XCUITestOptions()
    options.platform_name = 'iOS'
    options.device_name = 'iPhone SE'
    options.platform_version = '17.2'
    options.udid = '00008030-000151561A85402E'
    options.automation_name = 'XCUITest'
    options.bundle_id = 'com.inconceptlabs.liveboard'
    options.no_reset = True
    options.auto_accept_alerts = True
    options.new_command_timeout = 300
    options.show_xcode_log = True
    options.xcode_org_id = '2FHJSTZ57U'
    options.xcode_signing_id = 'iPhone Developer'
    
    try:
        # Create driver
        driver = webdriver.Remote('http://localhost:4723', options=options)
        
        yield driver
        
    except Exception as e:
        error_msg = str(e)
        if "xcodebuild failed with code 65" in error_msg:
            pytest.fail(f"WebDriverAgent build failed. Common causes: iPhone not on WiFi, developer certificate not trusted, or code signing issues. Original error: {error_msg}")
        elif "Unable to launch WebDriverAgent" in error_msg:
            pytest.fail(f"WebDriverAgent launch failed. Check network connectivity and developer certificate trust. Original error: {error_msg}")
        else:
            pytest.fail(f"iOS driver creation failed: {error_msg}")
    
    # Cleanup
    try:
        driver.quit()
    except:
        pass
