#!/usr/bin/env python3
"""
Simple Test Runner for Claude Test Generator
Runs comprehensive unit tests and integration tests
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run comprehensive tests"""
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    test_runner = script_dir / "tests" / "run_comprehensive_tests.py"
    
    # Change to the project directory
    os.chdir(script_dir)
    
    print("🚀 Claude Test Generator - Comprehensive Test Suite")
    print("=" * 60)
    print(f"📁 Working Directory: {script_dir}")
    print(f"🧪 Test Runner: {test_runner}")
    print("=" * 60)
    
    # Run the comprehensive tests
    try:
        result = subprocess.run([sys.executable, str(test_runner)], 
                              cwd=script_dir, 
                              check=False)
        return result.returncode
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())