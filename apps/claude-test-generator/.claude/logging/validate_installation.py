#!/usr/bin/env python3
"""
Framework Logging Installation Validator

Purpose: Quick validation script to verify the comprehensive logging system
is properly installed and functional.

Author: AI Systems Suite
Version: 1.0.0
"""

import sys
import json
from pathlib import Path
import tempfile
import shutil
import traceback

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        from framework_debug_logger import FrameworkDebugLogger
        print("  ✅ FrameworkDebugLogger")
    except Exception as e:
        print(f"  ❌ FrameworkDebugLogger: {e}")
        return False
    
    try:
        from framework_hooks import FrameworkHookIntegration
        print("  ✅ FrameworkHookIntegration")
    except Exception as e:
        print(f"  ❌ FrameworkHookIntegration: {e}")
        return False
    
    try:
        from log_analyzer import FrameworkLogAnalyzer
        print("  ✅ FrameworkLogAnalyzer")
    except Exception as e:
        print(f"  ❌ FrameworkLogAnalyzer: {e}")
        return False
    
    try:
        from realtime_monitor import RealTimeFrameworkMonitor
        print("  ✅ RealTimeFrameworkMonitor")
    except Exception as e:
        print(f"  ❌ RealTimeFrameworkMonitor: {e}")
        return False
    
    try:
        from enable_framework_logging import FrameworkLoggingIntegration
        print("  ✅ FrameworkLoggingIntegration")
    except Exception as e:
        print(f"  ❌ FrameworkLoggingIntegration: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    config_file = current_dir.parent / "config" / "logging-config.json"
    
    if not config_file.exists():
        print(f"  ❌ Configuration file not found: {config_file}")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        if 'framework_debug_logging' not in config:
            print("  ❌ Invalid configuration format")
            return False
        
        print("  ✅ Configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False

def test_basic_functionality():
    """Test basic logging functionality"""
    print("\n⚙️ Testing basic functionality...")
    
    test_dir = None
    try:
        # Import required modules
        from framework_debug_logger import FrameworkDebugLogger
        from framework_hooks import FrameworkHookIntegration
        from enable_framework_logging import FrameworkLoggingIntegration
        
        # Create temporary directory
        test_dir = tempfile.mkdtemp()
        
        # Test logger
        logger = FrameworkDebugLogger("validation-test", test_dir)
        logger.log_info("VALIDATION_TEST", "Testing basic logging functionality")
        
        # Verify log file was created
        master_log = logger.log_dir / 'framework_debug_master.jsonl'
        if not master_log.exists():
            print("  ❌ Master log file not created")
            return False
        
        print("  ✅ Basic logging works")
        
        # Test hooks
        hooks = FrameworkHookIntegration(logger, enable_all_hooks=False)
        hooks.install_claude_code_tool_hooks()
        
        if 'bash_tool' not in hooks.hook_registry:
            print("  ❌ Hooks not installed properly")
            return False
        
        print("  ✅ Hook installation works")
        
        # Test integration
        integration = FrameworkLoggingIntegration()
        status = integration.get_status()
        
        if not isinstance(status, dict):
            print("  ❌ Integration status error")
            return False
        
        print("  ✅ Integration works")
        
        # Cleanup
        hooks.finalize_framework_logging()
        logger.finalize_logging()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Basic functionality test failed: {e}")
        print(f"     {traceback.format_exc()}")
        return False
        
    finally:
        if test_dir and Path(test_dir).exists():
            shutil.rmtree(test_dir)

def test_demo_functionality():
    """Test demo functionality"""
    print("\n🧪 Testing demo functionality...")
    
    test_dir = None
    try:
        from enable_framework_logging import FrameworkLoggingIntegration
        
        # Create test configuration
        test_dir = tempfile.mkdtemp()
        config_file = Path(test_dir) / "test_config.json"
        
        config = {
            "framework_debug_logging": {
                "enabled": True,
                "global_settings": {
                    "default_log_level": "DEBUG"
                },
                "log_destinations": {
                    "base_directory": str(Path(test_dir) / "logs")
                },
                "hook_configuration": {
                    "auto_install_hooks": True,
                    "enabled_hooks": {
                        "claude_code_tools": True,
                        "framework_phases": True
                    }
                },
                "real_time_monitoring": {
                    "enabled": False
                }
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Test demo
        integration = FrameworkLoggingIntegration(str(config_file))
        result = integration.enable_framework_logging("demo-test", "DEMO-123", False)
        
        if not result['success']:
            print(f"  ❌ Demo enable failed: {result.get('error')}")
            return False
        
        integration.create_demo_logs()
        
        # Verify logs were created
        log_dir = Path(result['log_directory'])
        master_log = log_dir / 'framework_debug_master.jsonl'
        
        if not master_log.exists():
            print("  ❌ Demo logs not created")
            return False
        
        # Check log content
        with open(master_log, 'r') as f:
            log_lines = f.readlines()
        
        if len(log_lines) < 5:
            print("  ❌ Insufficient demo logs created")
            return False
        
        print("  ✅ Demo functionality works")
        
        integration.disable_framework_logging()
        return True
        
    except Exception as e:
        print(f"  ❌ Demo test failed: {e}")
        print(f"     {traceback.format_exc()}")
        return False
        
    finally:
        if test_dir and Path(test_dir).exists():
            shutil.rmtree(test_dir)

def test_analysis_tools():
    """Test analysis tools"""
    print("\n📊 Testing analysis tools...")
    
    test_dir = None
    try:
        from framework_debug_logger import FrameworkDebugLogger
        from log_analyzer import FrameworkLogAnalyzer
        from realtime_monitor import RealTimeFrameworkMonitor
        
        # Create test logs
        test_dir = tempfile.mkdtemp()
        logger = FrameworkDebugLogger("analysis-test", test_dir)
        
        # Generate test data
        logger.log_phase_start("test_phase")
        logger.log_agent_spawn("test_agent", "Test task")
        logger.log_tool_execution("test_tool", "test_action")
        logger.log_validation_checkpoint("test_validation", "passed", 0.9)
        logger.log_error("TEST_ERROR", "Test error")
        logger.finalize_logging()
        
        # Test analyzer
        analyzer = FrameworkLogAnalyzer(str(logger.log_dir))
        
        if len(analyzer.logs) == 0:
            print("  ❌ Analyzer found no logs")
            return False
        
        # Test analysis
        timeline = analyzer.analyze_execution_timeline()
        if not timeline or 'total_events' not in timeline:
            print("  ❌ Timeline analysis failed")
            return False
        
        print("  ✅ Log analysis works")
        
        # Test monitor
        monitor = RealTimeFrameworkMonitor(str(logger.log_dir), 0.1)
        status = monitor.get_current_status()
        
        if not isinstance(status, dict) or 'current_state' not in status:
            print("  ❌ Monitor status failed")
            return False
        
        print("  ✅ Real-time monitor works")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Analysis tools test failed: {e}")
        print(f"     {traceback.format_exc()}")
        return False
        
    finally:
        if test_dir and Path(test_dir).exists():
            shutil.rmtree(test_dir)

def run_validation():
    """Run complete validation"""
    print("🚀 FRAMEWORK LOGGING INSTALLATION VALIDATION")
    print("=" * 55)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("Basic Functionality", test_basic_functionality),
        ("Demo Functionality", test_demo_functionality),
        ("Analysis Tools", test_analysis_tools)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 55)
    print("📋 VALIDATION RESULTS")
    print("=" * 55)
    
    passed = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:20} {status}")
        if result:
            passed += 1
    
    success_rate = (passed / len(tests)) * 100
    print(f"\nSuccess Rate: {passed}/{len(tests)} ({success_rate:.1f}%)")
    
    if success_rate == 100:
        print("\n🎉 ALL VALIDATIONS PASSED!")
        print("✅ Framework logging system is properly installed and functional.")
        print("\n📚 Next Steps:")
        print("  1. Review README.md for usage instructions")
        print("  2. Run comprehensive tests: python test_logging_system.py --all")
        print("  3. Try demo: python enable_framework_logging.py demo")
        print("  4. Integrate with framework execution")
        return True
    else:
        print("\n❌ SOME VALIDATIONS FAILED!")
        print("🔧 Please check the error messages above and fix any issues.")
        print("\n📚 Troubleshooting:")
        print("  1. Ensure all required files are present")
        print("  2. Check Python path and imports")
        print("  3. Verify configuration file format")
        print("  4. Review error messages for specific issues")
        return False

def print_system_info():
    """Print system information"""
    print("\n📋 SYSTEM INFORMATION")
    print("=" * 30)
    print(f"Python Version: {sys.version}")
    print(f"Current Directory: {Path.cwd()}")
    print(f"Script Location: {current_dir}")
    print(f"Config Location: {current_dir.parent / 'config' / 'logging-config.json'}")
    
    # Check file structure
    print(f"\n📁 File Structure:")
    expected_files = [
        "framework_debug_logger.py",
        "framework_hooks.py", 
        "log_analyzer.py",
        "realtime_monitor.py",
        "enable_framework_logging.py",
        "test_logging_system.py",
        "../config/logging-config.json"
    ]
    
    for file_name in expected_files:
        file_path = current_dir / file_name
        if file_name.startswith("../"):
            file_path = current_dir.parent / file_name[3:]
        
        status = "✅" if file_path.exists() else "❌"
        print(f"  {status} {file_name}")

def main():
    """Main validation function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--info":
        print_system_info()
        return 0
    
    success = run_validation()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--verbose":
        print_system_info()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())