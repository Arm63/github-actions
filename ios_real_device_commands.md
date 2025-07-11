# iOS Real Device Testing - Complete Command Reference

## 🚀 **One-Command Setup (Recommended)**

```bash
# Run the automated setup script
./complete_ios_setup.sh
```

## 📋 **Manual Step-by-Step Commands**

### **Step 1: Check Device Connection**
```bash
# Check if device is connected via USB
idevice_id -l

# Expected output: 00008101-001D35A23C0A001E
```

### **Step 2: Get Team ID**
```bash
# Get your Apple Developer Team ID
xcrun security find-identity -v -p codesigning

# Look for line like: "Apple Development: armenasatryan1996@gmail.com (2FHJSTZ57U)"
# The Team ID is: 2FHJSTZ57U
```

### **Step 3: Check Appium Installation**
```bash
# Check Appium version
appium --version

# Check XCUITest driver
appium driver list

# Install XCUITest driver if needed
appium driver install xcuitest
```

### **Step 4: Clear Previous Data**
```bash
# Kill existing Appium processes
pkill -f appium

# Clear derived data
rm -rf /tmp/WebDriverAgent
rm -rf ~/Library/Developer/Xcode/DerivedData
```

### **Step 5: Start Appium Server**
```bash
# Start Appium with debug logging
appium --log appium.log --log-level debug
```

### **Step 6: Run Test**
```bash
# In a new terminal, run the test
poetry run python test_ios_real_device.py
```

## 🔧 **Configuration Commands**

### **Update Configuration Files**
```bash
# Update UDID in JSON config
sed -i '' 's/"appium:udid": ".*"/"appium:udid": "00008101-001D35A23C0A001E"/' appium_config_ios_real_device.json

# Update Team ID in JSON config
sed -i '' 's/"appium:xcodeOrgId": ".*"/"appium:xcodeOrgId": "2FHJSTZ57U"/' appium_config_ios_real_device.json

# Update UDID in Python script
sed -i '' 's/options.udid = ".*"/options.udid = "00008101-001D35A23C0A001E"/' test_ios_real_device.py

# Update Team ID in Python script
sed -i '' 's/options.xcode_org_id = ".*"/options.xcode_org_id = "2FHJSTZ57U"/' test_ios_real_device.py
```

## 🧪 **Testing Commands**

### **Quick Test Run**
```bash
# Run the automated test script
./one_command_ios_test.sh
```

### **Manual Test Run**
```bash
# Terminal 1: Start Appium
appium --log appium.log --log-level debug

# Terminal 2: Run test
poetry run python test_ios_real_device.py
```

### **Check Appium Logs**
```bash
# View Appium logs in real-time
tail -f appium.log

# Search for specific errors
grep -i "error" appium.log
grep -i "xcodebuild" appium.log
```

## 🔍 **Debugging Commands**

### **Device Information**
```bash
# List connected devices
idevice_id -l

# Get device info
ideviceinfo

# Check device connection
xcrun devicectl list devices
```

### **Xcode Information**
```bash
# Check Xcode path
xcode-select --print-path

# Check developer certificates
xcrun security find-identity -v -p codesigning

# Check iOS runtimes
xcrun simctl list runtimes
```

### **Appium Information**
```bash
# Check Appium version
appium --version

# List installed drivers
appium driver list

# Check Appium home
echo $APPIUM_HOME
```

## 📱 **Device Trust Commands**

### **Check Device Trust Status**
```bash
# Check if device is trusted
idevicepair validate

# If not trusted, you'll need to manually trust on the device:
# Settings → General → VPN & Device Management → Trust Developer
```

## 🚨 **Troubleshooting Commands**

### **Reset Everything**
```bash
# Kill all Appium processes
pkill -f appium

# Clear all derived data
rm -rf /tmp/WebDriverAgent
rm -rf ~/Library/Developer/Xcode/DerivedData

# Restart Appium
appium --log appium.log --log-level debug
```

### **Check WebDriverAgent**
```bash
# Find WebDriverAgent location
find ~/.appium -name "WebDriverAgent.xcodeproj" 2>/dev/null

# Check if WebDriverAgent is built
ls -la ~/.appium/node_modules/appium-xcuitest-driver/node_modules/appium-webdriveragent/
```

## 📊 **Monitoring Commands**

### **Check System Resources**
```bash
# Check CPU and memory usage
top -pid $(pgrep -f appium)

# Check disk space
df -h

# Check network connections
lsof -i :4723
```

## 🎯 **Quick Reference**

### **Essential Commands (Daily Use)**
```bash
# 1. Connect device and check
idevice_id -l

# 2. Start Appium
appium --log appium.log --log-level debug

# 3. Run test
poetry run python test_ios_real_device.py
```

### **Setup Commands (One-time)**
```bash
# 1. Run setup script
./complete_ios_setup.sh

# 2. Trust device on iPhone
# Settings → General → VPN & Device Management

# 3. Run test
./one_command_ios_test.sh
```

## 📁 **File Locations**

- **Appium Home**: `~/.appium/`
- **WebDriverAgent**: `~/.appium/node_modules/appium-xcuitest-driver/node_modules/appium-webdriveragent/`
- **Logs**: `appium.log` (in current directory)
- **Config**: `appium_config_ios_real_device.json`
- **Test**: `test_ios_real_device.py`

## 💡 **Pro Tips**

1. **Always use USB connection** for real device testing
2. **Use `idevice_id -l`** to get the correct UDID
3. **Trust the developer** on your iPhone
4. **Check Appium logs** for detailed error messages
5. **Use the setup script** for automatic configuration 