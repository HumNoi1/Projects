import os
import pytest
import sys

def run_tests():
    """
    รันทดสอบทั้งหมดในโฟลเดอร์ tests
    """
    print("Running backend tests...")
    # กำหนดให้รันทดสอบในโฟลเดอร์ tests
    args = ["-xvs", "tests"]
    
    # เพิ่ม coverage report ถ้าต้องการ
    if "--coverage" in sys.argv:
        args.extend(["--cov=app", "--cov-report=term", "--cov-report=html"])
    
    # รัน pytest ด้วย arguments ที่กำหนด
    exit_code = pytest.main(args)
    
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ Tests failed with exit code: {exit_code}")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(run_tests())