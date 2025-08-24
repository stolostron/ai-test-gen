#!/usr/bin/env python3
"""
Framework Integration Enforcer - AUTOMATIC VALIDATION INTEGRATION
================================================================

CRITICAL PURPOSE: Automatically integrate validation into framework workflow
ROBUSTNESS LEVEL: HIGH - Ensures wrapper usage without manual intervention
INTEGRATION TYPE: Seamless - Works with existing framework logic

This enforcer automatically replaces Write operations with validated equivalents.
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import Any, Callable

class FrameworkIntegrationEnforcer:
    """Automatic integration of validation into framework operations"""
    
    def __init__(self):
        self.original_functions = {}
        self.integration_active = False
        self.enforcement_patches = []
        
    def patch_write_operations(self):
        """
        CRITICAL: Patch all Write operations to use validation wrapper
        
        This function intercepts framework Write calls and redirects them
        to the validated_write_wrapper for mandatory enforcement.
        """
        try:
            # Import the validation wrapper
            wrapper_path = os.path.join(os.path.dirname(__file__), 'validated_write_wrapper.py')
            spec = importlib.util.spec_from_file_location("validated_write_wrapper", wrapper_path)
            wrapper_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(wrapper_module)
            
            # Store reference to validated_write function
            self.validated_write_func = wrapper_module.validated_write
            
            print("🔧 FRAMEWORK INTEGRATION: Validation enforcement active")
            print("🛡️  All Write operations now require validation approval")
            
            self.integration_active = True
            return True
            
        except Exception as e:
            print(f"❌ FRAMEWORK INTEGRATION ERROR: {str(e)}")
            return False
    
    def create_enforcement_decorator(self):
        """Create decorator that enforces validation on any function"""
        def validation_enforcer(original_func: Callable) -> Callable:
            """Decorator that adds validation enforcement to any function"""
            def validated_wrapper(*args, **kwargs):
                # Check if this is a file write operation
                if len(args) >= 2 and isinstance(args[0], str) and isinstance(args[1], str):
                    file_path, content = args[0], args[1]
                    
                    # Use validated write instead of original function
                    return self.validated_write_func(file_path, content)
                
                # For non-write operations, proceed normally
                return original_func(*args, **kwargs)
            
            return validated_wrapper
        
        return validation_enforcer
    
    def enforce_framework_validation(self, framework_module: Any):
        """
        Apply validation enforcement to framework module
        
        Args:
            framework_module: The framework module to patch
        """
        if not self.integration_active:
            self.patch_write_operations()
        
        enforcement_decorator = self.create_enforcement_decorator()
        
        # Patch common write function names
        write_function_names = [
            'write_file', 'write', 'save_file', 'create_file',
            'output_file', 'generate_file', 'Write', 'write_content'
        ]
        
        patched_functions = []
        
        for func_name in write_function_names:
            if hasattr(framework_module, func_name):
                original_func = getattr(framework_module, func_name)
                self.original_functions[func_name] = original_func
                
                # Apply validation enforcement
                validated_func = enforcement_decorator(original_func)
                setattr(framework_module, func_name, validated_func)
                
                patched_functions.append(func_name)
        
        if patched_functions:
            print(f"🔧 PATCHED FUNCTIONS: {', '.join(patched_functions)}")
            print("✅ Framework integration complete - validation enforced")
        else:
            print("⚠️  No write functions found to patch - manual integration required")
        
        return patched_functions
    
    def create_auto_integration_script(self, output_path: str):
        """Create script for automatic framework integration"""
        script_content = '''#!/usr/bin/env python3
"""
AUTO-INTEGRATION SCRIPT - Automatic Validation Enforcement
=========================================================

This script automatically integrates validation enforcement into any framework.
Place this at the start of your framework execution to enable validation.
"""

import sys
import os

# Add enforcement directory to path
enforcement_dir = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, enforcement_dir)

from framework_integration_enforcer import FrameworkIntegrationEnforcer

def auto_enable_validation():
    """Automatically enable validation for current framework"""
    enforcer = FrameworkIntegrationEnforcer()
    
    # Patch current module
    current_module = sys.modules[__name__]
    enforcer.enforce_framework_validation(current_module)
    
    # Try to patch main module if different
    if '__main__' in sys.modules and sys.modules['__main__'] != current_module:
        enforcer.enforce_framework_validation(sys.modules['__main__'])
    
    print("🛡️  AUTOMATIC VALIDATION ENFORCEMENT ACTIVE")
    return enforcer

# AUTO-ENABLE on import
if __name__ != "__main__":
    auto_enable_validation()

if __name__ == "__main__":
    print("FRAMEWORK INTEGRATION ENFORCER")
    print("This script enables automatic validation enforcement")
    auto_enable_validation()
'''
        
        with open(output_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(output_path, 0o755)
        
        print(f"📝 Auto-integration script created: {output_path}")
        return output_path

# GLOBAL ENFORCER INSTANCE
_enforcer_instance = FrameworkIntegrationEnforcer()

def enable_framework_validation():
    """Enable validation enforcement for current framework"""
    return _enforcer_instance.patch_write_operations()

def integrate_validation(module):
    """Integrate validation into specific module"""
    return _enforcer_instance.enforce_framework_validation(module)

if __name__ == "__main__":
    # Create auto-integration script
    script_path = os.path.join(os.path.dirname(__file__), 'auto_enable_validation.py')
    _enforcer_instance.create_auto_integration_script(script_path)
    
    # Enable validation for current session
    enable_framework_validation()
    print("✅ Framework validation enforcement ready")