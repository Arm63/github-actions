# 🤖 Android Compose Testing Automation

One-command automation for testing your Liveboard Android app with Jetpack Compose screens.

## 🚀 One-Command Usage

```bash
# Run all Android Compose tests
./run_android_compose_test.sh

# Run specific test types
./run_android_compose_test.sh login
./run_android_compose_test.sh navigation  
./run_android_compose_test.sh text_input
./run_android_compose_test.sh all
```

## 📋 Prerequisites

The script automatically checks and guides you through setup, but ensure you have:

1. **Android device** connected via USB with USB debugging enabled
2. **Liveboard app** installed on the device
3. **Basic tools** (the script will guide you if anything is missing):
   - ADB (Android Platform Tools)
   - Python 3 + Poetry
   - Node.js + Appium
   - UiAutomator2 driver

## 🎯 What the Script Does

1. **✅ System Check** - Validates all required tools
2. **📱 Device Check** - Connects to your Android device
3. **📦 App Check** - Verifies Liveboard app installation
4. **🔧 Setup** - Installs dependencies and drivers
5. **🚀 Launch** - Starts Appium and launches the app
6. **🧪 Test** - Runs comprehensive Compose tests
7. **📊 Report** - Generates detailed results and artifacts

## 📁 Generated Results

After running, you'll find everything in `android_compose_results/`:

```
android_compose_results/
├── summary_TIMESTAMP.md           # Executive summary
├── test_results_TIMESTAMP.txt     # Detailed test output  
├── appium_TIMESTAMP.log          # Appium server logs
├── device_info_TIMESTAMP.env     # Device configuration
├── android_compose_*.png         # Screenshots
└── android_page_source_*.xml     # UI hierarchy dumps
```

## 🎪 Test Types

| Type | Description | Command |
|------|-------------|---------|
| `login` | Tests the complete login flow | `./run_android_compose_test.sh login` |
| `navigation` | Tests navigation elements (tabs, menus, FAB) | `./run_android_compose_test.sh navigation` |
| `text_input` | Tests text input fields and interactions | `./run_android_compose_test.sh text_input` |
| `all` | Runs all tests above (default) | `./run_android_compose_test.sh` |

## 🔧 Advanced Usage

### Environment Variables
```bash
# Override device selection
export DEVICE_UDID="your-device-id"

# Override device name  
export DEVICE_NAME="Your Device Name"

# Override Android version
export PLATFORM_VERSION="13"
```

### Custom Results Directory
```bash
# Results go to android_compose_results/ by default
# Modify RESULTS_DIR in the script to change location
```

### Debug Mode
```bash
# For troubleshooting, check these files:
tail -f android_compose_results/appium_TIMESTAMP.log
cat android_compose_results/test_results_TIMESTAMP.txt
```

## 🚨 Troubleshooting

### Device Not Found
```bash
# Check device connection
adb devices

# If not listed, check:
# 1. USB cable connection
# 2. Developer options enabled
# 3. USB debugging enabled
# 4. Allow USB debugging prompt on device
```

### App Not Found  
```bash
# Check if Liveboard is installed
adb shell pm list packages | grep liveboard

# If not found, install the APK on your device first
```

### Appium Issues
```bash
# Check Appium installation
appium --version
appium driver list

# Reinstall if needed
npm install -g appium
appium driver install uiautomator2
```

### Test Failures
1. Check screenshots in results directory
2. Review test output in `test_results_TIMESTAMP.txt`
3. Analyze Appium logs for detailed error info
4. Ensure app is in expected state before testing

## 🎉 Success Example

```bash
$ ./run_android_compose_test.sh login

🤖 Android Compose Testing Automation
=====================================
ℹ️ Test Type: login
ℹ️ Timestamp: 20241201_143022
ℹ️ Results Directory: android_compose_results

🚀 Step 1: Checking system requirements...
✅ Running on macOS
✅ ADB is available: Android Debug Bridge version 1.0.41
✅ Python3 is available: Python 3.11.6
✅ Poetry is available: Poetry (version 1.6.1)
✅ Node.js is available: v18.17.1
✅ Appium is available: 2.2.1

🚀 Step 2: Checking Android device connection...
✅ Android device connected: 1A2B3C4D5E6F
ℹ️ Device: Pixel 7
ℹ️ Android: 13 (API 33)

🚀 Step 3: Checking Liveboard app...
✅ Liveboard app is installed
ℹ️ App version: 2.1.0

[... more steps ...]

✅ All Android Compose tests passed! 🎉
ℹ️ Results Location: android_compose_results
ℹ️ Open results: open android_compose_results
```

## 🔄 Integration with CI/CD

You can also integrate this into your GitHub Actions workflow by calling:

```yaml
- name: Run Android Compose Tests
  run: ./run_android_compose_test.sh all
```

---

**Happy Testing!** 🎯 Your Android Compose automation is ready to go! 