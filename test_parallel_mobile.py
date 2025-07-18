#!/usr/bin/env python3
"""
Parallel Mobile Test Runner for iOS and Android
This script runs comprehensive iOS and Android tests simultaneously using threading.
Uses the same test files as separate real device runs:
- iOS: tests/test_login_ios.py (TestLiveboardiOS::test_liveboard_login_flow)
- Android: tests/test_login_android_compose.py (TestAndroidLogin::test_android_login_flow)

IMPORTANT: This script uses the working test code from your backup files.
DO NOT MODIFY the test logic - only update paths/class/method names if needed.
"""

import threading
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

def run_ios_test():
    """Run iOS test in a separate thread."""
    print("🍎 Starting iOS test thread...")
    start_time = time.time()
    
    try:
        # Run the comprehensive iOS test using pytest
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', 'tests/test_login_ios.py::TestLiveboardiOS::test_liveboard_login_flow', '-v'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ iOS test completed successfully in {duration:.2f} seconds")
            return {
                'platform': 'iOS',
                'success': True,
                'duration': duration,
                'output': result.stdout,
                'error': result.stderr
            }
        else:
            print(f"❌ iOS test failed in {duration:.2f} seconds")
            return {
                'platform': 'iOS',
                'success': False,
                'duration': duration,
                'output': result.stdout,
                'error': result.stderr
            }
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ iOS test exception: {str(e)}")
        return {
            'platform': 'iOS',
            'success': False,
            'duration': duration,
            'output': '',
            'error': str(e)
        }

def run_android_test():
    """Run Android test in a separate thread."""
    print("🤖 Starting Android test thread...")
    start_time = time.time()
    
    try:
        # Set up Android environment variables
        env = os.environ.copy()
        env['ANDROID_HOME'] = '/Users/armen/Library/Android/sdk'
        env['ANDROID_SDK_ROOT'] = '/Users/armen/Library/Android/sdk'
        env['PATH'] = env['PATH'] + ':' + env['ANDROID_HOME'] + '/platform-tools:' + env['ANDROID_HOME'] + '/tools'
        
        # Run the Android test using pytest
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', 'tests/test_login_android_compose.py::TestAndroidLogin::test_android_login_flow', '-v'],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
            env=env
        )
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ Android test completed successfully in {duration:.2f} seconds")
            return {
                'platform': 'Android',
                'success': True,
                'duration': duration,
                'output': result.stdout,
                'error': result.stderr
            }
        else:
            print(f"❌ Android test failed in {duration:.2f} seconds")
            return {
                'platform': 'Android',
                'success': False,
                'duration': duration,
                'output': result.stdout,
                'error': result.stderr
            }
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ Android test exception: {str(e)}")
        return {
            'platform': 'Android',
            'success': False,
            'duration': duration,
            'output': '',
            'error': str(e)
        }

def check_prerequisites():
    """Check if both Appium servers are running."""
    print("🔍 Checking prerequisites...")
    
    # Check if iOS Appium server is running (port 4723)
    ios_server_running = False
    android_server_running = False
    
    try:
        import socket
        
        # Check iOS server (port 4723)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('localhost', 4723))
        if result == 0:
            ios_server_running = True
            print("✅ iOS Appium server (port 4723) is running")
        else:
            print("❌ iOS Appium server (port 4723) is not running")
        sock.close()
        
        # Check Android server (port 4724)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('localhost', 4724))
        if result == 0:
            android_server_running = True
            print("✅ Android Appium server (port 4724) is running")
        else:
            print("❌ Android Appium server (port 4724) is not running")
        sock.close()
        
    except Exception as e:
        print(f"❌ Error checking servers: {str(e)}")
    
    return ios_server_running, android_server_running

def run_parallel_tests():
    """Run both iOS and Android tests in parallel."""
    print("🚀 Starting Parallel Mobile Test Execution")
    print("=" * 50)
    
    # Check prerequisites
    ios_server_ok, android_server_ok = check_prerequisites()
    
    if not ios_server_ok:
        print("⚠️  Warning: iOS Appium server not detected. iOS test may fail.")
    if not android_server_ok:
        print("⚠️  Warning: Android Appium server not detected. Android test may fail.")
    
    print()
    
    # Start timing
    overall_start_time = time.time()
    
    # Run tests in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Submit both tests
        futures = []
        
        if ios_server_ok:
            futures.append(executor.submit(run_ios_test))
        else:
            print("⏭️  Skipping iOS test (server not running)")
            
        if android_server_ok:
            futures.append(executor.submit(run_android_test))
        else:
            print("⏭️  Skipping Android test (server not running)")
        
        if not futures:
            print("❌ No tests to run. Please start at least one Appium server.")
            return
        
        # Wait for completion and collect results
        results = []
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"❌ Test execution error: {str(e)}")
    
    # Calculate overall duration
    overall_duration = time.time() - overall_start_time
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 PARALLEL TEST EXECUTION SUMMARY")
    print("=" * 50)
    
    successful_tests = 0
    failed_tests = 0
    
    for result in results:
        platform = result['platform']
        success = result['success']
        duration = result['duration']
        
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{platform:8} | {status} | {duration:6.2f}s")
        
        if success:
            successful_tests += 1
        else:
            failed_tests += 1
            # Print error details for failed tests
            if result['error']:
                print(f"         Error: {result['error'][:100]}...")
    
    print("-" * 50)
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {successful_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Overall Duration: {overall_duration:.2f}s")
    
    # Print detailed results if requested
    print("\n💡 Tip: For detailed output, check individual test logs above")
    
    # Return success status
    return failed_tests == 0

if __name__ == "__main__":
    print("🔧 Parallel Mobile Test Runner")
    print("This script runs iOS and Android tests simultaneously")
    print("Using working test code from backup files:")
    print("- iOS: TestLiveboardiOS::test_liveboard_login_flow")
    print("- Android: TestAndroidLogin::test_android_login_flow")
    print()
    
    success = run_parallel_tests()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Check the output above for details.")
        sys.exit(1) 