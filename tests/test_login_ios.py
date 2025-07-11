# Appium config for iOS simulator with LiveBoard.app
# Use this JSON in Appium Inspector or your test setup:
# {
#   "platformName": "iOS",
#   "appium:deviceName": "iPhone 16",
#   "appium:platformVersion": "18.5",
#   "appium:udid": "6A37736F-D32F-4E71-AC30-D934BD80AB7E",
#   "appium:automationName": "XCUITest",
#   "appium:app": "/Users/armen/Library/Developer/Xcode/DerivedData/LiveBoard-bojpbtdllofaxifidpajscttqolv/Build/Products/Debug-iphonesimulator/LiveBoard.app",
#   "appium:noReset": true,
#   "appium:autoAcceptAlerts": true,
#   "appium:newCommandTimeout": 300,
#   "appium:autoGrantPermissions": true,
#   "appium:allowInsecureLocalhost": true
# }
#
# To run this test from the terminal:
#   pytest tests/test_login_ios.py
#
# Make sure your Appium server is running and the simulator is booted!

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# def test_click_login_button_only_ios(ios_driver):
#     """Test that only clicks the login button (iOS version, using predicate string)"""
#     wait = WebDriverWait(ios_driver, 10)
#     login_btn = wait.until(EC.element_to_be_clickable((
#         AppiumBy.IOS_PREDICATE,
#         'name == "Log in" AND label == "Log in" AND value == "Log in"'
#     )))
#     login_btn.click()
#     time.sleep(2)

# def test_invalid_login_credentials_ios(ios_driver):
#     """Test invalid login credentials and verify error message (iOS version)"""
#     wait = WebDriverWait(ios_driver, 10)
#     # Step 1: Click on login button
#     login_btn = wait.until(EC.element_to_be_clickable((
#         AppiumBy.IOS_PREDICATE,
#         'name == "Log in" AND label == "Log in" AND value == "Log in"'
#     )))
#     login_btn.click()
#     # Step 2: Click on "continue with email" button
#     continue_email_btn = wait.until(EC.element_to_be_clickable((
#         AppiumBy.ACCESSIBILITY_ID, 'continue_with_email_accessibility_id'  # Placeholder
#     )))
#     continue_email_btn.click()
#     # Step 3: Fill in invalid email
#     email_input = wait.until(EC.presence_of_element_located((
#         AppiumBy.IOS_PREDICATE, 'type == "XCUIElementTypeTextField"'  # Placeholder
#     )))
#     email_input.send_keys("prod@mailinator.com")
#     # Step 4: Fill in invalid password
#     password_input = wait.until(EC.presence_of_element_located((
#         AppiumBy.IOS_PREDICATE, 'type == "XCUIElementTypeSecureTextField"'  # Placeholder
#     )))
#     password_input.send_keys("testtest1")
#     # Step 5: Click login button to submit
#     login_btn_second = wait.until(EC.element_to_be_clickable((
#         AppiumBy.ACCESSIBILITY_ID, 'submit_login_accessibility_id'  # Placeholder
#     )))
#     login_btn_second.click()
#     # Step 6: Verify error message appears
#     error_message = wait.until(EC.visibility_of_element_located((
#         AppiumBy.IOS_PREDICATE, 'label == "Invalid email address or password"'  # Placeholder
#     )))
#     assert error_message.is_displayed(), "Error message should be visible"
#     assert "Invalid email address or password" in error_message.text

def test_click_composable_ios(ios_driver):
    wait = WebDriverWait(ios_driver, 10)
    # Step 1: Click on login button
    login_btn = wait.until(EC.element_to_be_clickable((
        AppiumBy.IOS_PREDICATE,
        'name == "Log in" AND label == "Log in" AND value == "Log in"'
    )))
    login_btn.click()
    # Step 2: Click on "continue with email" button
    continue_email_btn = wait.until(EC.element_to_be_clickable((
        AppiumBy.IOS_PREDICATE,
        'name == "Continue with Email" AND label == "Continue with Email" AND type == "XCUIElementTypeButton"'
    )))
    continue_email_btn.click()
    # Step 3: Fill in email field
    email_input = wait.until(EC.presence_of_element_located((
        AppiumBy.IOS_PREDICATE, 'value == "Email address"'
    )))
    email_input.send_keys("prod@mailinatorO.com")
    # Step 4: Fill in password field
    password_input = wait.until(EC.presence_of_element_located((
        AppiumBy.IOS_PREDICATE, 'value == "Password"'
    )))
    password_input.send_keys("testtest1")
 
    login_btn_second = wait.until(EC.element_to_be_clickable((
        AppiumBy.IOS_PREDICATE,
        'name == "Log in" AND label == "Log in" AND type == "XCUIElementTypeButton"'
    )))
    login_btn_second.click()
    time.sleep(1)
    email_input.send_keys("prod@mailinator.com")
    login_btn_second.click() 