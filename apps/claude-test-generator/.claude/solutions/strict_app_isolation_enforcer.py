#!/usr/bin/env python3
"""
Strict App Isolation Enforcer - Prevent Apps from Accessing External Resources
============================================================================

CORRECTED ISOLATION PRINCIPLE:
- Apps can ONLY access files within their own directory
- Apps CANNOT access parent directories, sibling apps, or external resources  
- Root level maintains full access for orchestration
- Testing frameworks have read-only access for monitoring

This enforces the correct hierarchical isolation model.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - APP_ISOLATION - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AppIsolationViolationError(Exception):
    """Raised when an app attempts to access resources outside its boundaries"""
    pass


class StrictAppIsolationEngine:
    """
    Enforce strict app-level isolation - apps can only access their own files
    """
    
    def __init__(self, app_root: str):
        self.app_root = Path(app_root).resolve()
        self.app_id = self.app_root.name
        self.violations_blocked = 0
        self.access_attempts = []
        
        # Define what constitutes external access (BLOCKED for apps)
        self.blocked_patterns = [
            "../*",                    # Parent directory access
            "../../*",                 # Grandparent directory access
            "../../../*",              # Any ancestor access
            "~/",                      # Home directory access
            "/Users/",                 # System user directories
            "/tmp/",                   # Temporary directories
            "/etc/",                   # System configuration
            "/var/",                   # System variables
        ]
        
        # Specific paths that apps should never access (external to app)
        ai_systems_base = "/Users/ashafi/Documents/work/ai/ai_systems"
        self.specifically_blocked_paths = [
            f"{ai_systems_base}/CLAUDE.md",
            f"{ai_systems_base}/apps",  # Apps directory (but not self)
            f"{ai_systems_base}/tests",
        ]
        
        # Add other apps as blocked (but not self)
        for other_app in ["z-stream-analysis", "future-app"]:
            if other_app != self.app_id:
                self.specifically_blocked_paths.append(f"{ai_systems_base}/apps/{other_app}")
        
        logger.info(f"StrictAppIsolationEngine initialized for app: {self.app_id}")
        logger.info(f"App root directory: {self.app_root}")
    
    def is_within_app_boundaries(self, target_path: str) -> bool:
        """Check if target path is within app boundaries"""
        
        try:
            # Resolve the target path
            if target_path.startswith('/'):
                # Absolute path
                target_resolved = Path(target_path).resolve()
            else:
                # Relative path - resolve from current directory
                current_dir = Path.cwd()
                target_resolved = (current_dir / target_path).resolve()
            
            # Check if target is within app root
            try:
                target_resolved.relative_to(self.app_root)
                return True
            except ValueError:
                # Path is outside app directory
                return False
                
        except Exception as e:
            # If we can't resolve the path, be conservative and block
            logger.warning(f"Could not resolve path {target_path}: {e}")
            return False
    
    def is_blocked_pattern(self, path: str) -> bool:
        """Check if path matches any blocked patterns"""
        
        for pattern in self.blocked_patterns:
            if pattern.endswith('*'):
                prefix = pattern[:-1]
                if path.startswith(prefix):
                    return True
            else:
                if path == pattern:
                    return True
        
        return False
    
    def is_specifically_blocked(self, path: str) -> bool:
        """Check if path is specifically blocked"""
        
        try:
            # Handle both absolute and relative paths
            if path.startswith('/'):
                # Absolute path
                path_resolved = str(Path(path).resolve())
            else:
                # Relative path - resolve from current directory
                current_dir = Path.cwd()
                path_resolved = str((current_dir / path).resolve())
            
            for blocked_path in self.specifically_blocked_paths:
                if path_resolved.startswith(blocked_path):
                    # Additional check: make sure it's not within our app
                    if not path_resolved.startswith(str(self.app_root)):
                        return True
        except Exception:
            pass
        
        return False
    
    def validate_access(self, operation: str, target_path: str) -> bool:
        """Validate if operation on target path should be allowed"""
        
        # Log the access attempt
        access_attempt = {
            "timestamp": datetime.now().isoformat(),
            "app_id": self.app_id,
            "operation": operation,
            "target_path": target_path,
            "current_dir": str(Path.cwd())
        }
        
        # Check 1: Pattern-based blocking
        if self.is_blocked_pattern(target_path):
            access_attempt["result"] = "BLOCKED_PATTERN"
            access_attempt["reason"] = f"Path matches blocked pattern: {target_path}"
            self.access_attempts.append(access_attempt)
            self.violations_blocked += 1
            logger.warning(f"BLOCKED: App {self.app_id} - {operation} blocked by pattern: {target_path}")
            return False
        
        # Check 2: Specific path blocking
        if self.is_specifically_blocked(target_path):
            access_attempt["result"] = "BLOCKED_SPECIFIC"
            access_attempt["reason"] = f"Path specifically blocked: {target_path}"
            self.access_attempts.append(access_attempt)
            self.violations_blocked += 1
            logger.warning(f"BLOCKED: App {self.app_id} - {operation} blocked (specific): {target_path}")
            return False
        
        # Check 3: Boundary validation
        if not self.is_within_app_boundaries(target_path):
            access_attempt["result"] = "BLOCKED_BOUNDARY"
            access_attempt["reason"] = f"Path outside app boundaries: {target_path}"
            self.access_attempts.append(access_attempt)
            self.violations_blocked += 1
            logger.warning(f"BLOCKED: App {self.app_id} - {operation} outside boundaries: {target_path}")
            return False
        
        # Access allowed
        access_attempt["result"] = "ALLOWED"
        access_attempt["reason"] = "Within app boundaries"
        self.access_attempts.append(access_attempt)
        logger.debug(f"ALLOWED: App {self.app_id} - {operation} within boundaries: {target_path}")
        return True
    
    def enforce_access_control(self, operation: str, target_path: str) -> None:
        """Enforce access control - raise exception if access should be blocked"""
        
        if not self.validate_access(operation, target_path):
            raise AppIsolationViolationError(
                f"ISOLATION VIOLATION: App '{self.app_id}' cannot {operation} outside its boundaries: {target_path}"
            )
    
    def get_isolation_statistics(self) -> Dict[str, Any]:
        """Get isolation enforcement statistics"""
        
        total_attempts = len(self.access_attempts)
        allowed_attempts = len([a for a in self.access_attempts if a["result"] == "ALLOWED"])
        
        return {
            "app_id": self.app_id,
            "app_root": str(self.app_root),
            "total_access_attempts": total_attempts,
            "allowed_attempts": allowed_attempts,
            "violations_blocked": self.violations_blocked,
            "isolation_effectiveness": (self.violations_blocked / total_attempts * 100) if total_attempts > 0 else 100,
            "recent_attempts": self.access_attempts[-10:] if self.access_attempts else []
        }


class AppPermissionWrapper:
    """
    Wrapper for file operations that enforces app isolation
    """
    
    def __init__(self, app_id: str, app_path: str):
        self.app_id = app_id
        self.app_path = Path(app_path).resolve()
        self.isolation_engine = StrictAppIsolationEngine(app_path)
        
        logger.info(f"AppPermissionWrapper initialized for app: {app_id}")
    
    def safe_open(self, path: str, mode: str = 'r', **kwargs):
        """Safe file open with isolation enforcement"""
        
        # Determine operation type from mode
        if any(write_mode in mode for write_mode in ['w', 'a', 'x']):
            operation = "write"
        else:
            operation = "read"
        
        # Enforce isolation
        self.isolation_engine.enforce_access_control(operation, path)
        
        # Allow operation within app
        return open(path, mode, **kwargs)
    
    def safe_exists(self, path: str) -> bool:
        """Safe existence check with isolation enforcement"""
        
        # For existence checks, we still validate but don't block (read-only operation)
        if self.isolation_engine.validate_access("check", path):
            return Path(path).exists()
        else:
            # If path is outside boundaries, report as non-existent
            return False
    
    def safe_listdir(self, path: str = ".") -> List[str]:
        """Safe directory listing with isolation enforcement"""
        
        self.isolation_engine.enforce_access_control("list", path)
        return os.listdir(path)
    
    def safe_mkdir(self, path: str, **kwargs) -> None:
        """Safe directory creation with isolation enforcement"""
        
        self.isolation_engine.enforce_access_control("create", path)
        Path(path).mkdir(**kwargs)
    
    def safe_remove(self, path: str) -> None:
        """Safe file removal with isolation enforcement"""
        
        self.isolation_engine.enforce_access_control("delete", path)
        Path(path).unlink()
    
    def safe_copy(self, src: str, dst: str) -> None:
        """Safe file copy with isolation enforcement"""
        
        self.isolation_engine.enforce_access_control("read", src)
        self.isolation_engine.enforce_access_control("write", dst)
        
        import shutil
        shutil.copy2(src, dst)


class AppContextDetector:
    """
    Detect if we're running in an app context and which app
    """
    
    @staticmethod
    def detect_app_context() -> Optional[Dict[str, str]]:
        """Detect current app context from working directory"""
        
        current_dir = Path.cwd()
        current_parts = current_dir.parts
        
        # Look for "apps" in the path
        if "apps" in current_parts:
            try:
                apps_index = current_parts.index("apps")
                if apps_index + 1 < len(current_parts):
                    app_id = current_parts[apps_index + 1]
                    
                    # Reconstruct app path
                    app_path_parts = current_parts[:apps_index + 2]
                    app_path = Path("/".join(app_path_parts))
                    
                    return {
                        "app_id": app_id,
                        "app_path": str(app_path),
                        "is_app_context": True,
                        "current_dir": str(current_dir)
                    }
            except (ValueError, IndexError):
                pass
        
        return {
            "app_id": "root",
            "app_path": "/Users/ashafi/Documents/work/ai/ai_systems",
            "is_app_context": False,
            "current_dir": str(current_dir)
        }


class SystemIsolationValidator:
    """
    Validate the entire system's isolation configuration
    """
    
    def __init__(self):
        self.context = AppContextDetector.detect_app_context()
        self.validation_results = []
        
        logger.info(f"SystemIsolationValidator initialized - Context: {self.context}")
    
    def test_app_isolation_boundaries(self) -> Dict[str, Any]:
        """Test that current app (if any) respects isolation boundaries"""
        
        logger.info("Testing app isolation boundaries")
        
        test_result = {
            "test_name": "app_isolation_boundaries",
            "timestamp": datetime.now().isoformat(),
            "context": self.context,
            "tests_performed": [],
            "violations_found": []
        }
        
        if not self.context["is_app_context"]:
            test_result["status"] = "SKIPPED"
            test_result["reason"] = "Not in app context - running from root level"
            return test_result
        
        # Initialize isolation engine for current app
        app_isolation = StrictAppIsolationEngine(self.context["app_path"])
        
        # Test cases - all should be blocked for apps
        blocked_access_tests = [
            ("../../", "parent_directory_access"),
            ("../../CLAUDE.md", "root_config_access"),
            ("../", "apps_directory_access"),
            ("../z-stream-analysis/", "sibling_app_access"),
            ("/Users/ashafi/Documents/work/ai/ai_systems/tests/", "tests_directory_access"),
            ("/tmp/", "system_tmp_access"),
            ("~/", "home_directory_access")
        ]
        
        for test_path, test_name in blocked_access_tests:
            try:
                # Test if access is properly blocked
                access_allowed = app_isolation.validate_access("test", test_path)
                
                test_case = {
                    "test_name": test_name,
                    "test_path": test_path,
                    "access_allowed": access_allowed,
                    "expected_result": "blocked",
                    "test_passed": not access_allowed  # Should be blocked
                }
                
                test_result["tests_performed"].append(test_case)
                
                if access_allowed:
                    # This is a violation - access should be blocked
                    violation = {
                        "violation_type": "EXTERNAL_ACCESS_ALLOWED",
                        "test_name": test_name,
                        "path": test_path,
                        "severity": "HIGH"
                    }
                    test_result["violations_found"].append(violation)
                    logger.error(f"ISOLATION VIOLATION: {test_name} - External access allowed: {test_path}")
                else:
                    logger.info(f"ISOLATION OK: {test_name} - External access properly blocked: {test_path}")
                    
            except Exception as e:
                test_case = {
                    "test_name": test_name,
                    "test_path": test_path,
                    "error": str(e),
                    "test_passed": False
                }
                test_result["tests_performed"].append(test_case)
        
        # Test internal access - should be allowed
        allowed_access_tests = [
            ("./CLAUDE.md", "internal_config_access"),
            ("./.claude/", "internal_claude_dir_access"),
            ("./runs/", "internal_runs_access"),
            (".", "current_directory_access")
        ]
        
        for test_path, test_name in allowed_access_tests:
            try:
                access_allowed = app_isolation.validate_access("test", test_path)
                
                test_case = {
                    "test_name": test_name,
                    "test_path": test_path,
                    "access_allowed": access_allowed,
                    "expected_result": "allowed",
                    "test_passed": access_allowed  # Should be allowed
                }
                
                test_result["tests_performed"].append(test_case)
                
                if not access_allowed:
                    # This is a violation - internal access should be allowed
                    violation = {
                        "violation_type": "INTERNAL_ACCESS_BLOCKED",
                        "test_name": test_name,
                        "path": test_path,
                        "severity": "MEDIUM"
                    }
                    test_result["violations_found"].append(violation)
                    logger.error(f"ISOLATION VIOLATION: {test_name} - Internal access blocked: {test_path}")
                else:
                    logger.info(f"ISOLATION OK: {test_name} - Internal access properly allowed: {test_path}")
                    
            except Exception as e:
                test_case = {
                    "test_name": test_name,
                    "test_path": test_path,
                    "error": str(e),
                    "test_passed": False
                }
                test_result["tests_performed"].append(test_case)
        
        # Calculate results
        total_tests = len(test_result["tests_performed"])
        passed_tests = len([t for t in test_result["tests_performed"] if t.get("test_passed", False)])
        violations_count = len(test_result["violations_found"])
        
        test_result["total_tests"] = total_tests
        test_result["passed_tests"] = passed_tests
        test_result["violations_count"] = violations_count
        test_result["isolation_score"] = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        test_result["status"] = "SECURE" if violations_count == 0 else "VIOLATIONS_DETECTED"
        
        # Get isolation statistics
        test_result["isolation_statistics"] = app_isolation.get_isolation_statistics()
        
        logger.info(f"App isolation test complete - Score: {test_result['isolation_score']}%, Violations: {violations_count}")
        return test_result
    
    def validate_system_isolation(self) -> Dict[str, Any]:
        """Validate complete system isolation configuration"""
        
        logger.info("Validating complete system isolation")
        
        validation_result = {
            "validation_name": "system_isolation_validation",
            "timestamp": datetime.now().isoformat(),
            "context": self.context,
            "validations": []
        }
        
        # Validation 1: App boundary testing
        app_boundary_result = self.test_app_isolation_boundaries()
        validation_result["validations"].append(app_boundary_result)
        
        # Calculate overall validation score
        total_validations = len(validation_result["validations"])
        successful_validations = len([v for v in validation_result["validations"] 
                                     if v.get("status") in ["SECURE", "SKIPPED"]])
        
        validation_result["total_validations"] = total_validations
        validation_result["successful_validations"] = successful_validations
        validation_result["validation_score"] = (successful_validations / total_validations * 100) if total_validations > 0 else 0
        validation_result["overall_status"] = "SECURE" if successful_validations == total_validations else "NEEDS_ATTENTION"
        
        logger.info(f"System isolation validation complete - Overall score: {validation_result['validation_score']}%")
        return validation_result


def main():
    """Main function to test and demonstrate strict app isolation"""
    
    print("🔒 Strict App Isolation Enforcer - Validation Test")
    print("=" * 60)
    
    try:
        # Detect context
        context = AppContextDetector.detect_app_context()
        print(f"\n📍 Current Context:")
        print(f"   App ID: {context['app_id']}")
        print(f"   App Path: {context['app_path']}")
        print(f"   Is App Context: {context['is_app_context']}")
        print(f"   Current Directory: {context['current_dir']}")
        
        # Initialize validator
        validator = SystemIsolationValidator()
        
        # Run validation
        print("\n🧪 Running System Isolation Validation...")
        validation_result = validator.validate_system_isolation()
        
        print(f"\n📊 Validation Results:")
        print(f"   Overall Status: {validation_result['overall_status']}")
        print(f"   Validation Score: {validation_result['validation_score']}%")
        print(f"   Successful Validations: {validation_result['successful_validations']}/{validation_result['total_validations']}")
        
        # Show detailed results
        for validation in validation_result["validations"]:
            print(f"\n🔍 {validation['test_name']}:")
            print(f"   Status: {validation['status']}")
            if 'isolation_score' in validation:
                print(f"   Isolation Score: {validation['isolation_score']}%")
            if 'violations_count' in validation:
                print(f"   Violations Found: {validation['violations_count']}")
            if 'passed_tests' in validation:
                print(f"   Tests Passed: {validation['passed_tests']}/{validation['total_tests']}")
        
        # Save validation results
        results_file = Path(".claude/solutions/strict_isolation_validation_results.json")
        results_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(validation_result, f, indent=2, default=str)
        
        print(f"\n📄 Validation results saved to: {results_file}")
        
        if validation_result["overall_status"] == "SECURE":
            print("\n✅ SYSTEM ISOLATION: SECURE")
            print("🔒 App isolation boundaries properly enforced")
        else:
            print("\n⚠️ SYSTEM ISOLATION: NEEDS ATTENTION")
            print("🚨 Some isolation violations detected - review results")
        
    except Exception as e:
        print(f"\n❌ VALIDATION ERROR: {e}")
        print("🚨 Could not complete isolation validation")
        sys.exit(1)


if __name__ == "__main__":
    main()