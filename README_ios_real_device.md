# iOS Real Device Testing - Official Guide

Based on [Appium XCUITest Driver documentation](https://appium.github.io/appium-xcuitest-driver/4.19/real-device-config/)

## 🎯 **Step-by-Step Setup**

### **Step 1: Verify Your Setup**
- ✅ Device connected: "Jeremy's iPhone" (00008101-001D35A23C0A001E)
- ✅ Xcode installed and configured
- ✅ Developer certificates found
- ✅ Team ID: 2FHJSTZ57U

### **Step 2: Trust Developer on iPhone**
1. **On your iPhone:**
   - Go to Settings → General → VPN & Device Management
   - Look for "Apple Development: armenasatryan1996@gmail.com"
   - Tap "Trust" for this developer certificate

### **Step 3: Start Appium Server**
```bash
# Kill any existing Appium processes
pkill -f appium

# Start Appium with debug logs
appium --log appium.log --log-level debug
```

### **Step 4: Use Configuration in Appium Inspector**
Use this configuration in Appium Inspector:

```json
{
  "platformName": "iOS",
  "appium:deviceName": "iPhone",
  "appium:platformVersion": "18.5",
  "appium:udid": "00008101-001D35A23C0A001E",
  "appium:automationName": "XCUITest",
  "appium:bundleId": "com.inconceptlabs.liveboard",
  "appium:noReset": true,
  "appium:autoAcceptAlerts": true,
  "appium:newCommandTimeout": 300,
  "appium:showXcodeLog": true,
  "appium:xcodeOrgId": "2FHJSTZ57U",
  "appium:xcodeSigningId": "iPhone Developer"
}
```

### **Step 5: Run Test**
```bash
# Run the test script
poetry run python test_ios_real_device.py
```

## 🔧 **Key Configuration Details**

### **Code Signing (Required)**
- `xcodeOrgId`: "2FHJSTZ57U" (Your Team ID)
- `xcodeSigningId`: "iPhone Developer" (Your signing certificate)

### **Device Configuration**
- `udid`: "00008101-001D35A23C0A001E" (Your device)
- `bundleId`: "com.inconceptlabs.liveboard" (Your app)

## 🚨 **If You Get xcodebuild Error 65**

According to the official docs, this means code signing is not set up correctly. The solution is:

1. **Trust the developer** on your iPhone (Step 2 above)
2. **Make sure the app is installed** on the device
3. **Check Appium logs** for detailed error messages

## 📋 **Files Created**
- `appium_config_ios_real_device.json` - Configuration for Appium Inspector
- `test_ios_real_device.py` - Test script
- `README_ios_real_device.md` - This guide

## 🎯 **Expected Result**
With proper code signing and device trust, WebDriverAgent should:
1. ✅ Build successfully
2. ✅ Install on your device
3. ✅ Connect to the LiveBoard app
4. ✅ Allow automation

The key difference from before: **Proper code signing configuration** with your Team ID. 