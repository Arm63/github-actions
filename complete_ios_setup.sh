#!/bin/bash

echo "🚀 Complete iOS Real Device Setup - From Scratch"
echo "================================================="
echo "This script will install everything needed for iOS testing"
echo "Works on fresh computer after restart!"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Homebrew if not exists
install_homebrew() {
    if ! command_exists brew; then
        print_status "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH for Apple Silicon Macs
        if [[ $(uname -m) == "arm64" ]]; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
        
        print_success "Homebrew installed"
    else
        print_success "Homebrew already installed"
    fi
}

# Function to install Node.js
install_nodejs() {
    if ! command_exists node; then
        print_status "Installing Node.js..."
        brew install node
        print_success "Node.js installed"
    else
        NODE_VERSION=$(node --version)
        print_success "Node.js already installed: $NODE_VERSION"
    fi
}

# Function to install Python and Poetry
install_python_poetry() {
    if ! command_exists python3; then
        print_status "Installing Python..."
        brew install python
        print_success "Python installed"
    else
        PYTHON_VERSION=$(python3 --version)
        print_success "Python already installed: $PYTHON_VERSION"
    fi
    
    if ! command_exists poetry; then
        print_status "Installing Poetry..."
        curl -sSL https://install.python-poetry.org | python3 -
        
        # Add Poetry to PATH
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zprofile
        export PATH="$HOME/.local/bin:$PATH"
        
        print_success "Poetry installed"
    else
        POETRY_VERSION=$(poetry --version)
        print_success "Poetry already installed: $POETRY_VERSION"
    fi
}

# Function to install Xcode command line tools
install_xcode_tools() {
    if ! command_exists xcode-select; then
        print_status "Installing Xcode Command Line Tools..."
        xcode-select --install
        print_warning "Please complete Xcode installation in the popup window"
        print_warning "Press Enter when Xcode installation is complete..."
        read -r
    else
        print_success "Xcode Command Line Tools already installed"
    fi
}

# Function to install libimobiledevice
install_libimobiledevice() {
    if ! command_exists idevice_id; then
        print_status "Installing libimobiledevice..."
        brew install libimobiledevice
        print_success "libimobiledevice installed"
    else
        print_success "libimobiledevice already installed"
    fi
}

# Function to install Appium
install_appium() {
    if ! command_exists appium; then
        print_status "Installing Appium..."
        npm install -g appium
        print_success "Appium installed"
    else
        APPIUM_VERSION=$(appium --version)
        print_success "Appium already installed: $APPIUM_VERSION"
    fi
    
    # Install XCUITest driver
    print_status "Installing XCUITest driver..."
    appium driver install xcuitest
    print_success "XCUITest driver installed"
}

# Function to setup Poetry project
setup_poetry_project() {
    if [ ! -f "pyproject.toml" ]; then
        print_status "Initializing Poetry project..."
        poetry init --name "liveboard-test" --description "iOS Real Device Testing" --author "Your Name <your.email@example.com>" --python "^3.8" --no-interaction
        print_success "Poetry project initialized"
    else
        print_success "Poetry project already exists"
    fi
    
    # Add dependencies
    print_status "Adding Python dependencies..."
    poetry add appium-python-client pytest pytest-html
    print_success "Python dependencies added"
}

# Function to create test files
create_test_files() {
    print_status "Creating test files..."
    
    # Create test directory if not exists
    mkdir -p tests
    
    # Create __init__.py
    touch tests/__init__.py
    
    # Create test file
    cat > test_ios_real_device.py << 'EOF'
#!/usr/bin/env python3
"""
iOS Real Device Test
Simple test to verify iOS real device automation works
"""

import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

def test_ios_real_device():
    """Test iOS real device automation"""
    
    # Get device UDID
    import subprocess
    try:
        result = subprocess.run(['idevice_id', '-l'], capture_output=True, text=True, check=True)
        device_udid = result.stdout.strip()
        print(f"Device UDID: {device_udid}")
    except subprocess.CalledProcessError:
        print("Error: No device connected via USB")
        print("Please connect your iPhone via USB and trust the computer")
        return False
    
    # Get Team ID
    try:
        result = subprocess.run(['xcrun', 'security', 'find-identity', '-v', '-p', 'codesigning'], 
                              capture_output=True, text=True, check=True)
        team_id = None
        for line in result.stdout.split('\n'):
            if 'Apple Development' in line and '(' in line:
                team_id = line.split('(')[1].split(')')[0]
                break
        print(f"Team ID: {team_id}")
    except subprocess.CalledProcessError:
        print("Error: Could not find Team ID")
        return False
    
    # Appium capabilities
    options = {
        'platformName': 'iOS',
        'appium:deviceName': 'iPhone',
        'appium:platformVersion': '17.2.1',  # Updated to your iOS version
        'appium:udid': device_udid,
        'appium:automationName': 'XCUITest',
        'appium:bundleId': 'com.inconceptlabs.liveboard',
        'appium:noReset': True,
        'appium:autoAcceptAlerts': True,
        'appium:newCommandTimeout': 300,
        'appium:showXcodeLog': True,
        'appium:xcodeOrgId': team_id,
        'appium:xcodeSigningId': 'iPhone Developer'
    }
    
    try:
        print("Connecting to Appium server...")
        driver = webdriver.Remote('http://localhost:4723', options)
        
        print("✅ Successfully connected to device!")
        print(f"App: {driver.current_package}")
        print(f"Activity: {driver.current_activity}")
        
        # Take a screenshot
        screenshot_path = f"ios_test_screenshot_{int(time.time())}.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
        
        # Close the app
        driver.terminate_app('com.inconceptlabs.liveboard')
        print("App terminated successfully")
        
        driver.quit()
        print("✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_ios_real_device()
EOF

    # Create Appium config
    cat > appium_config_ios_real_device.json << 'EOF'
{
  "platformName": "iOS",
  "appium:deviceName": "iPhone",
  "appium:platformVersion": "17.2.1",
  "appium:udid": "AUTO_DETECT",
  "appium:automationName": "XCUITest",
  "appium:bundleId": "com.inconceptlabs.liveboard",
  "appium:noReset": true,
  "appium:autoAcceptAlerts": true,
  "appium:newCommandTimeout": 300,
  "appium:showXcodeLog": true,
  "appium:xcodeOrgId": "AUTO_DETECT",
  "appium:xcodeSigningId": "iPhone Developer"
}
EOF

    # Create run script
    cat > run_test.sh << 'EOF'
#!/bin/bash
echo "🧪 Running iOS Real Device Test"
echo "================================"

# Check if device is connected
if ! idevice_id -l > /dev/null 2>&1; then
    echo "❌ No device connected via USB"
    echo "Please connect your iPhone via USB and trust the computer"
    exit 1
fi

# Start Appium server in background
echo "Starting Appium server..."
appium --log appium.log --log-level debug &
APPIUM_PID=$!

# Wait for Appium to start
sleep 5

# Run the test
echo "Running test..."
poetry run python test_ios_real_device.py

# Stop Appium server
echo "Stopping Appium server..."
kill $APPIUM_PID

echo "Test completed!"
EOF

    chmod +x run_test.sh
    chmod +x test_ios_real_device.py
    
    print_success "Test files created"
}

# Function to update configuration with actual values
update_configuration() {
    print_status "Updating configuration with actual values..."
    
    # Get device UDID
    DEVICE_UDID=$(idevice_id -l)
    if [ -z "$DEVICE_UDID" ]; then
        print_warning "No device connected. Configuration will use AUTO_DETECT"
        return
    fi
    
    # Use the correct Team ID
    TEAM_ID="2FHJSTZ57U"  # Your correct Team ID
    print_success "Team ID: $TEAM_ID"
    
    # Update JSON config
    sed -i '' "s/\"appium:udid\": \".*\"/\"appium:udid\": \"$DEVICE_UDID\"/" appium_config_ios_real_device.json
    sed -i '' "s/\"appium:xcodeOrgId\": \".*\"/\"appium:xcodeOrgId\": \"$TEAM_ID\"/" appium_config_ios_real_device.json
    
    # Update Python script
    sed -i '' "s/options.udid = \".*\"/options.udid = \"$DEVICE_UDID\"/" test_ios_real_device.py
    sed -i '' "s/options.xcode_org_id = \".*\"/options.xcode_org_id = \"$TEAM_ID\"/" test_ios_real_device.py
    
    print_success "Configuration updated with actual values"
}

# Function to create README
create_readme() {
    cat > README_COMPLETE_SETUP.md << 'EOF'
# 🚀 Complete iOS Real Device Testing Setup

## What This Setup Includes

✅ **Node.js** - For Appium  
✅ **Python & Poetry** - For test automation  
✅ **Xcode Command Line Tools** - For iOS development  
✅ **libimobiledevice** - For device communication  
✅ **Appium** - Mobile automation framework  
✅ **XCUITest Driver** - iOS automation driver  
✅ **Test Scripts** - Ready-to-run tests  
✅ **Configuration Files** - Appium Inspector config  

## Quick Start

### First Time Setup
```bash
./complete_ios_setup.sh
```

### Daily Testing
```bash
# Connect your iPhone via USB
./run_test.sh
```

## Requirements

- macOS (required for iOS development)
- iPhone with iOS 17.2.1+ (or update version in config)
- USB cable
- Apple Developer account (free)

## What the Script Does

1. **Installs Homebrew** (package manager)
2. **Installs Node.js** (for Appium)
3. **Installs Python & Poetry** (for test framework)
4. **Installs Xcode Command Line Tools** (for iOS development)
5. **Installs libimobiledevice** (for device communication)
6. **Installs Appium** (automation framework)
7. **Installs XCUITest Driver** (iOS driver)
8. **Creates Poetry project** (test environment)
9. **Creates test files** (ready-to-run tests)
10. **Updates configuration** (with your device info)

## Files Created

- `test_ios_real_device.py` - Main test script
- `appium_config_ios_real_device.json` - Appium Inspector config
- `run_test.sh` - One-command test runner
- `pyproject.toml` - Poetry project config
- `poetry.lock` - Dependency lock file

## Troubleshooting

### Device Not Found
```bash
# Check device connection
idevice_id -l

# Trust the computer on your iPhone:
# Settings → General → VPN & Device Management
```

### Appium Issues
```bash
# Check Appium installation
appium --version

# Check XCUITest driver
appium driver list

# View logs
tail -f appium.log
```

### Code Signing Issues
```bash
# Check certificates
xcrun security find-identity -v -p codesigning

# Trust developer on iPhone:
# Settings → General → VPN & Device Management
```

## Next Steps

1. **Connect your iPhone via USB**
2. **Trust the computer on your iPhone**
3. **Run the test**: `./run_test.sh`
4. **Create more test cases**
5. **Set up CI/CD pipeline**

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. View Appium logs: `tail -f appium.log`
3. Ensure device is connected via USB
4. Verify developer is trusted on iPhone
EOF

    print_success "README created"
}

# Main execution
main() {
    echo "Starting complete iOS setup..."
    echo ""
    
    # Step 1: Install Homebrew
    install_homebrew
    
    # Step 2: Install Node.js
    install_nodejs
    
    # Step 3: Install Python and Poetry
    install_python_poetry
    
    # Step 4: Install Xcode Command Line Tools
    install_xcode_tools
    
    # Step 5: Install libimobiledevice
    install_libimobiledevice
    
    # Step 6: Install Appium
    install_appium
    
    # Step 7: Setup Poetry project
    setup_poetry_project
    
    # Step 8: Create test files
    create_test_files
    
    # Step 9: Update configuration
    update_configuration
    
    # Step 10: Create README
    create_readme
    
    echo ""
    echo "🎉 Complete Setup Finished!"
    echo "=========================="
    echo ""
    echo "📱 Next Steps:"
    echo "1. Connect your iPhone via USB"
    echo "2. Trust the computer on your iPhone"
    echo "3. Run: ./run_test.sh"
    echo ""
    echo "📁 Files created:"
    echo "- test_ios_real_device.py (main test)"
    echo "- appium_config_ios_real_device.json (Appium Inspector config)"
    echo "- run_test.sh (one-command test runner)"
    echo "- pyproject.toml (Poetry project)"
    echo "- README_COMPLETE_SETUP.md (this guide)"
    echo ""
    echo "🚀 You're ready to test iOS real devices!"
}

# Run main function
main 