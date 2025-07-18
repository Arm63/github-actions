# Mobile Automation Testing Framework

A comprehensive mobile automation testing framework for iOS and Android applications using Appium, Python, and Poetry.

## 🚀 Features

- **Parallel Testing**: Run iOS and Android tests simultaneously
- **Real Device Support**: Test on actual iOS and Android devices
- **Comprehensive Setup**: Automated environment setup script
- **Cross-Platform**: Support for both iOS and Android platforms
- **Modern Stack**: Uses Appium 2.x, Python 3.x, and Poetry

## 📋 Prerequisites

- **macOS** (required for iOS development)
- **Xcode** (for iOS automation)
- **Android Studio** (for Android SDK)
- **Physical iOS and Android devices** (for real device testing)

## 🛠️ Quick Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd github-actions
```

### 2. Run the Setup Script

The setup script will automatically check and install all required tools:

```bash
./setup_environment.sh
```

This script will:
- ✅ Check and install Homebrew
- ✅ Check and install Python 3
- ✅ Check and install Poetry
- ✅ Check and install Node.js
- ✅ Check and install Appium
- ✅ Check and install Appium drivers (UiAutomator2, XCUITest)
- ✅ Check Xcode installation
- ✅ Check Android SDK
- ✅ Set up environment variables
- ✅ Install Python dependencies
- ✅ Check for connected devices

### 3. Manual Setup (if needed)

If you prefer to set up manually or the script fails:

#### Install Required Tools

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3
brew install python

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install Node.js
brew install node

# Install Appium
npm install -g appium

# Install Appium drivers
appium driver install uiautomator2
appium driver install xcuitest
```

#### Set up Environment Variables

Add these to your `~/.zshrc` file:

```bash
export ANDROID_HOME=$HOME/Library/Android/sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
export PATH=$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools
```

#### Install Python Dependencies

```bash
poetry install
```

## 📱 Device Setup

### iOS Device Setup

1. **Connect your iOS device** via USB
2. **Trust the computer** on your device
3. **Enable Developer Mode**:
   - Go to Settings > Privacy & Security > Developer Mode
   - Enable Developer Mode
4. **Trust the developer profile**:
   - Go to Settings > General > VPN & Device Management
   - Trust your developer certificate

### Android Device Setup

1. **Connect your Android device** via USB
2. **Enable Developer Options**:
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
3. **Enable USB Debugging**:
   - Go to Settings > Developer Options
   - Enable "USB Debugging"
4. **Trust the computer** when prompted

## 🏃‍♂️ Running Tests

### 1. Start Appium Servers

Open two terminal windows and run:

**Terminal 1 (iOS):**
```bash
appium -p 4723
```

**Terminal 2 (Android):**
```bash
appium -p 4724
```

### 2. Run Tests

#### Run Parallel Tests (Recommended)
```bash
python test_parallel_mobile.py
```

#### Run Individual Tests

**iOS Test:**
```bash
python -m pytest tests/test_login_ios.py::TestLiveboardiOS::test_liveboard_login_flow -v
```

**Android Test:**
```bash
python -m pytest tests/test_login_android_compose.py::TestAndroidLogin::test_android_login_flow -v
```

#### Run with Poetry
```bash
poetry run python test_parallel_mobile.py
```

## 📁 Project Structure

```
github-actions/
├── setup_environment.sh          # Environment setup script
├── test_parallel_mobile.py       # Parallel test runner
├── tests/
│   ├── test_login_ios.py         # iOS login test
│   └── test_login_android_compose.py  # Android login test
├── pyproject.toml                # Poetry configuration
└── README.md                     # This file
```

## 🔧 Configuration

### iOS Configuration

The iOS test uses these default settings:
- **Device UDID**: `00008030-000151561A85402E` (can be overridden with `DEVICE_UDID` env var)
- **Device Name**: `iPhone SE` (can be overridden with `DEVICE_NAME` env var)
- **Platform Version**: `17.2` (can be overridden with `PLATFORM_VERSION` env var)
- **Team ID**: `2FHJSTZ57U` (can be overridden with `TEAM_ID` env var)
- **Bundle ID**: `com.inconceptlabs.liveboard`

### Android Configuration

The Android test uses these default settings:
- **Device UDID**: `HT7991A08308`
- **Platform Version**: `13`
- **App Package**: `com.inconceptlabs.liveboard`
- **App Activity**: `com.inconceptlabs.liveboard.pages.activities.LaunchActivity`

## 🐛 Troubleshooting

### Common Issues

#### 1. "Neither ANDROID_HOME nor ANDROID_SDK_ROOT environment variable was exported"

**Solution:**
```bash
export ANDROID_HOME=$HOME/Library/Android/sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
```

#### 2. "Xcode not found"

**Solution:**
- Install Xcode from the App Store
- Run: `sudo xcode-select --install`

#### 3. "No devices found"

**Solution:**
- Ensure devices are connected via USB
- Trust the computer on both devices
- Enable USB debugging on Android
- Trust developer profile on iOS

#### 4. "Appium server not running"

**Solution:**
- Start iOS server: `appium -p 4723`
- Start Android server: `appium -p 4724`

#### 5. "Poetry not found"

**Solution:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
```

### Getting Device UDIDs

#### iOS Device UDID
```bash
xcrun devicectl list devices
```

#### Android Device UDID
```bash
adb devices
```

## 📊 Test Results

The parallel test runner provides:
- Individual test results and timing
- Overall execution summary
- Success/failure status for each platform
- Total execution time

Example output:
```
📊 PARALLEL TEST EXECUTION SUMMARY
==================================================
Android  | ✅ PASSED |  19.72s
iOS      | ✅ PASSED |  56.67s
--------------------------------------------------
Total Tests: 2
Passed: 2
Failed: 0
Overall Duration: 56.67s
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Run the setup script: `./setup_environment.sh`
3. Verify device connections
4. Check Appium server status
5. Review test logs for specific errors

## 🔄 Updates

To update the project:

```bash
git pull origin main
poetry install
./setup_environment.sh
```

---

**Happy Testing! 🎯**
