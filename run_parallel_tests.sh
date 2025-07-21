#!/bin/bash

# Start iOS test
poetry run pytest tests/test_login_ios.py::TestLiveboardiOS::test_liveboard_login_flow -v -s > ios_test_result.txt 2>&1 &
IOS_PID=$!

# Start Android test
poetry run pytest tests/test_login_android_compose.py::TestAndroidLogin::test_android_login_flow -v -s > android_test_result.txt 2>&1 &
ANDROID_PID=$!

# Wait for both to finish
wait $IOS_PID
wait $ANDROID_PID

echo "Both iOS and Android tests completed."

echo "--- iOS Test Output ---"
cat ios_test_result.txt

echo "--- Android Test Output ---"
cat android_test_result.txt 