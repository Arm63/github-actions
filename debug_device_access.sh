#!/bin/bash

echo "🔍 Device Access Debug Script"
echo "============================="

echo "📍 Script context:"
echo "User: $(whoami)"
echo "Shell: $SHELL"
echo "TTY: $(tty 2>/dev/null || echo 'No TTY')"
echo "Session: ${SSH_TTY:-'Local'}"
echo "Interactive: ${PS1:+'Yes'}"

echo ""
echo "🔧 Environment:"
echo "PATH: $PATH"
echo "HOME: $HOME"
echo "PWD: $PWD"

echo ""
echo "📱 Device Access Test:"
echo "idevice_id location: $(which idevice_id)"
echo "idevice_id permissions: $(ls -la $(which idevice_id))"

echo ""
echo "Testing device access..."
echo "Direct idevice_id call:"
idevice_id -l 2>&1 || echo "Failed to list devices"

echo ""
echo "Testing with explicit PATH:"
/opt/homebrew/bin/idevice_id -l 2>&1 || echo "Failed with explicit path"

echo ""
echo "USB System Info:"
system_profiler SPUSBDataType | grep -A 5 -B 2 "iPhone\|iPad" || echo "No iOS devices in USB system info"

echo ""
echo "Process tree:"
ps -ef | grep -E "(Runner|actions|idevice)" | grep -v grep || echo "No relevant processes"

echo ""
echo "🔒 Security & Permissions:"
echo "Security assessment:"
/usr/bin/security list-keychains || echo "Cannot access keychain"

echo ""
echo "🔄 Re-pairing attempt:"
echo "Attempting to re-establish device connection..."
idevicepair pair 2>&1 || echo "Pairing failed or not needed"

echo ""
echo "Final device check:"
idevice_id -l 2>&1 && echo "✅ Device access successful" || echo "❌ Device access failed" 