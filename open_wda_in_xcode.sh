#!/bin/bash
# Script to locate and open Appium WebDriverAgent Xcode project for manual configuration

# Try common Homebrew and npm global install locations
WDA_PATH=""

# Search for WebDriverAgent in Homebrew location
if [ -d "/opt/homebrew/lib/node_modules/appium/node_modules/appium-webdriveragent" ]; then
  WDA_PATH="/opt/homebrew/lib/node_modules/appium/node_modules/appium-webdriveragent"
fi

# Search for WebDriverAgent in /usr/local location
if [ -z "$WDA_PATH" ] && [ -d "/usr/local/lib/node_modules/appium/node_modules/appium-webdriveragent" ]; then
  WDA_PATH="/usr/local/lib/node_modules/appium/node_modules/appium-webdriveragent"
fi

# If not found, try to find it dynamically
if [ -z "$WDA_PATH" ]; then
  WDA_PATH=$(find /opt/homebrew/lib /usr/local/lib -type d -name appium-webdriveragent 2>/dev/null | head -1)
fi

if [ -z "$WDA_PATH" ]; then
  echo "❌ WebDriverAgent directory not found. Please check your Appium installation."
  exit 1
fi

# Open the Xcode project
open "$WDA_PATH/WebDriverAgent.xcodeproj"
echo "✅ Opened WebDriverAgent.xcodeproj in Xcode. Please follow manual steps for signing and building." 