
import subprocess
import sys
import re
import os

TEST_FILES = [
    "test_input_validation.py",
    "test_invalid_input_formats.py",
    "test_conversation_recovery.py",
    "test_intent_responses.py",
    "test_workflow_switching.py",
    "test_reset_workflow.py",
    "test_unexpected_messages.py",
    "test_end_to_end.py"
]

results = []

print("=" * 75)
print("              STAGE 6.10 - FINAL REGRESSION TESTING")
print("=" * 75)

for test_file in TEST_FILES:

    print(f"\nRUNNING: {test_file}")
    print("-" * 75)

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env
        )

        output = result.stdout + result.stderr
        print(output)

        # Detect common test-summary formats
        passed = (
            result.returncode == 0
            and (
                re.search(r"Failed:\s*0\b", output, re.I)
                or re.search(r"\b0\s+failed\b", output, re.I)
                or re.search(r"All .* passed!", output, re.I)
                or re.search(r"\b25/25\b", output)
            )
        )

        if passed:
            results.append((test_file, "PASS"))
        else:
            results.append((test_file, "CHECK"))

    except Exception as error:
        print("ERROR:", error)
        results.append((test_file, "ERROR"))


print("\n" + "=" * 75)
print("                 FINAL REGRESSION SUMMARY")
print("=" * 75)

for test_file, status in results:
    print(f"{test_file:<40} {status}")

total = len(results)
passed_count = sum(
    1 for _, status in results if status == "PASS"
)

print("-" * 75)
print("Total test files:", total)
print("Passed:", passed_count)
print("Need checking:", total - passed_count)

if passed_count == total:
    print("\nALL REGRESSION TEST FILES PASSED!")
else:
    print("\nSome tests need manual inspection.")

print("=" * 75)
