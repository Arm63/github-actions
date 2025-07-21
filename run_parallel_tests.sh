#!/bin/bash

# Start iOS test
poetry run pytest tests/test_login_ios.py::TestLiveboardiOS::test_liveboard_login_flow -v -s > ios_test_result.txt 2>&1 &
IOS_PID=$!

# Start Android test
poetry run pytest tests/test_login_android_compose.py::TestAndroidLogin::test_android_login_flow -v -s > android_test_result.txt 2>&1 &
ANDROID_PID=$!

# Wait for both to finish and capture exit codes
wait $IOS_PID
IOS_EXIT_CODE=$?
wait $ANDROID_PID
ANDROID_EXIT_CODE=$?

echo "Both iOS and Android tests completed."

echo "--- iOS Test Output ---"
cat ios_test_result.txt
if [ $IOS_EXIT_CODE -eq 0 ]; then
  echo "✅ iOS tests PASSED"
else
  echo "❌ iOS tests FAILED (exit code $IOS_EXIT_CODE)"
fi

echo "--- Android Test Output ---"
cat android_test_result.txt
if [ $ANDROID_EXIT_CODE -eq 0 ]; then
  echo "✅ Android tests PASSED"
else
  echo "❌ Android tests FAILED (exit code $ANDROID_EXIT_CODE)"
fi

# Exit nonzero if either test failed
if [ $IOS_EXIT_CODE -ne 0 ] || [ $ANDROID_EXIT_CODE -ne 0 ]; then
  exit 1
else
  exit 0
fi 