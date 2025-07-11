#!/usr/bin/env python3
"""
Minimal iOS Test using only requests library
This replaces 21 packages with just 2!
"""

import requests
import json
import time

def create_session():
    """Create Appium session using raw HTTP requests"""
    
    # Session capabilities
    capabilities = {
        "platformName": "iOS",
        "appium:deviceName": "iPhone SE",
        "appium:platformVersion": "17.2",
        "appium:udid": "00008030-000151561A85402E",
        "appium:automationName": "XCUITest",
        "appium:bundleId": "com.inconceptlabs.liveboard",
        "appium:noReset": True,
        "appium:autoAcceptAlerts": True,
        "appium:newCommandTimeout": 300,
        "appium:showXcodeLog": True,
        "appium:xcodeOrgId": "2FHJSTZ57U",
        "appium:xcodeSigningId": "iPhone Developer"
    }
    
    # Create session
    session_data = {
        "capabilities": {
            "alwaysMatch": capabilities
        }
    }
    
    response = requests.post(
        "http://localhost:4723/session",
        json=session_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        session_info = response.json()
        session_id = session_info["value"]["sessionId"]
        print(f"✅ Session created: {session_id}")
        return session_id
    else:
        print(f"❌ Failed to create session: {response.text}")
        return None

def take_screenshot(session_id):
    """Take screenshot using raw HTTP request"""
    
    response = requests.get(f"http://localhost:4723/session/{session_id}/screenshot")
    
    if response.status_code == 200:
        screenshot_data = response.json()
        import base64
        
        # Save screenshot
        screenshot_path = f"minimal_test_screenshot_{int(time.time())}.png"
        with open(screenshot_path, "wb") as f:
            f.write(base64.b64decode(screenshot_data["value"]))
        
        print(f"📸 Screenshot saved: {screenshot_path}")
        return True
    else:
        print(f"❌ Failed to take screenshot: {response.text}")
        return False

def terminate_app(session_id, bundle_id):
    """Terminate app using raw HTTP request"""
    
    response = requests.post(
        f"http://localhost:4723/session/{session_id}/appium/device/terminate_app",
        json={"bundleId": bundle_id},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print("📱 App terminated successfully")
        return True
    else:
        print(f"❌ Failed to terminate app: {response.text}")
        return False

def delete_session(session_id):
    """Delete session using raw HTTP request"""
    
    response = requests.delete(f"http://localhost:4723/session/{session_id}")
    
    if response.status_code == 200:
        print("🗑️ Session deleted successfully")
        return True
    else:
        print(f"❌ Failed to delete session: {response.text}")
        return False

def minimal_ios_test():
    """Run minimal iOS test with just HTTP requests"""
    
    print("🧪 Starting minimal iOS test...")
    print("📦 Using only 'requests' library (no heavy dependencies!)")
    print()
    
    # Create session
    session_id = create_session()
    if not session_id:
        return False
    
    # Take screenshot
    if not take_screenshot(session_id):
        delete_session(session_id)
        return False
    
    # Terminate app
    if not terminate_app(session_id, "com.inconceptlabs.liveboard"):
        delete_session(session_id)
        return False
    
    # Delete session
    if not delete_session(session_id):
        return False
    
    print("✅ Minimal test completed successfully!")
    print("💡 This used only 2 packages instead of 21!")
    return True

if __name__ == "__main__":
    minimal_ios_test() 