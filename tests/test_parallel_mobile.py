import subprocess
import multiprocessing
import sys

ANDROID_TEST = "tests/test_login_android_compose.py"
IOS_TEST = "tests/test_login_ios.py"


def run_pytest(test_path, result_queue):
    """Run pytest for the given test file and put the result in the queue."""
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', test_path, '-v'
        ], capture_output=True, text=True)
        result_queue.put((test_path, result.returncode, result.stdout, result.stderr))
    except Exception as e:
        result_queue.put((test_path, 1, '', str(e)))


def main():
    print("\n=== Running Android and iOS tests in parallel ===\n")
    result_queue = multiprocessing.Queue()

    android_proc = multiprocessing.Process(target=run_pytest, args=(ANDROID_TEST, result_queue))
    ios_proc = multiprocessing.Process(target=run_pytest, args=(IOS_TEST, result_queue))

    android_proc.start()
    ios_proc.start()

    android_proc.join()
    ios_proc.join()

    # Collect results
    results = [result_queue.get() for _ in range(2)]

    print("\n=== Test Results Summary ===\n")
    all_passed = True
    for test_path, returncode, stdout, stderr in results:
        print(f"--- {test_path} ---")
        print(stdout)
        if returncode == 0:
            print(f"✅ {test_path} PASSED")
        else:
            print(f"❌ {test_path} FAILED")
            if stderr:
                print(stderr)
            all_passed = False
        print("\n--------------------------\n")

    if not all_passed:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main() 