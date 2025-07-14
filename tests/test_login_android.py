import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_click_login_button_only(driver):
    """Test that only clicks the login button"""
    wait = WebDriverWait(driver, 10)
    
    # Click on login button
    login_btn = wait.until(EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").instance(3)'
    )))
    login_btn.click()
    
    # Wait a moment to see the result
    time.sleep(2)

def test_invalid_login_credentials(driver):
    """Test invalid login credentials and verify error message"""
    wait = WebDriverWait(driver, 10)
    
    # Step 1: Click on login button
    login_btn = wait.until(EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").instance(3)'
    )))
    login_btn.click()
    
    # Step 2: Click on "continue with email" button
    continue_email_btn = wait.until(EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").instance(3)'
    )))
    continue_email_btn.click()
    
    # Step 3: Fill in invalid email
    email_input = wait.until(EC.presence_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(0)'
    )))
    email_input.send_keys("prod@mailinator.com")
    
    # Step 4: Fill in invalid password
    password_input = wait.until(EC.presence_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(1)'
    )))
    password_input.send_keys("testtest1")
    
    # Step 5: Click login button to submit
    login_btn_second = wait.until(EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").instance(5)'
    )))
    login_btn_second.click()
    
    # Step 6: Verify error message appears
    error_message = wait.until(EC.visibility_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Invalid email address or password")'
    )))
    
    # Assert that error message is displayed
    assert error_message.is_displayed(), "Error message should be visible"
    
    # Optional: Verify the text content
    assert "Invalid email address or password" in error_message.text

def test_click_composable(driver):
    wait = WebDriverWait(driver, 10)  # 10 second timeout
    
    # Step 1: Click on login button
    login_btn = wait.until(EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").instance(3)'
    )))
    login_btn.click()
    
    # Step 2: Click on "continue with email" button
    continue_email_btn = wait.until(EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").instance(3)'
    )))
    continue_email_btn.click()
    
    # Step 3: Fill in email field
    email_input = wait.until(EC.presence_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(0)'
    )))
    email_input.send_keys("prod@mailinatorO.com")
    
    # Step 4: Fill in password field
    password_input = wait.until(EC.presence_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(1)'
    )))
    password_input.send_keys("testtest1")
    
    # Click the second login button
    login_btn_second = wait.until(EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").instance(5)'
    )))
    login_btn_second.click()

    # Wait a moment and add more email text
    time.sleep(1)  # Keep this one as it's for user observation
    email_input.send_keys("prod@mailinator.com")

    login_btn_second.click()