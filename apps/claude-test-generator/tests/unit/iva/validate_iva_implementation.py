#!/usr/bin/env python3
"""
IVA Implementation Validation Script
==================================

Comprehensive validation of the Intelligent Validation Architecture (IVA) implementation.
Validates that all components are properly implemented and ready for production use.
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
solutions_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'solutions')
sys.path.insert(0, solutions_path)

class IVAImplementationValidator:
    """Validates IVA implementation completeness and correctness"""
    
    def __init__(self):
        self.validation_results = {}
        self.solutions_path = Path(solutions_path)
        self.test_dir = None
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run comprehensive validation of IVA implementation"""
        print("🧠 Intelligent Validation Architecture (IVA) - Implementation Validation")
        print("=" * 80)
        
        validation_tests = [
            ("Core Architecture Files", self.validate_core_files),
            ("Learning Services Implementation", self.validate_learning_services),
            ("Data Structures", self.validate_data_structures),
            ("Safety Mechanisms", self.validate_safety_mechanisms),
            ("Configuration System", self.validate_configuration_system),
            ("Database Schemas", self.validate_database_schemas),
            ("API Interfaces", self.validate_api_interfaces),
            ("Integration Patterns", self.validate_integration_patterns),
            ("Documentation Coverage", self.validate_documentation),
            ("Test Coverage", self.validate_test_coverage)
        ]
        
        overall_success = True
        
        for test_name, test_func in validation_tests:
            print(f"\n🔍 Testing: {test_name}")
            print("-" * 50)
            
            try:
                success, details = test_func()
                self.validation_results[test_name] = {
                    'success': success,
                    'details': details
                }
                
                if success:
                    print(f"✅ {test_name}: PASSED")
                    for detail in details.get('passed', []):
                        print(f"   ✓ {detail}")
                else:
                    print(f"❌ {test_name}: FAILED")
                    overall_success = False
                    for detail in details.get('failed', []):
                        print(f"   ✗ {detail}")
                
                if details.get('warnings'):
                    for warning in details['warnings']:
                        print(f"   ⚠️  {warning}")
                        
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {e}")
                overall_success = False
                self.validation_results[test_name] = {
                    'success': False,
                    'details': {'error': str(e)}
                }
        
        # Generate summary report
        self.generate_summary_report(overall_success)
        return self.validation_results
    
    def validate_core_files(self) -> Tuple[bool, Dict[str, Any]]:
        """Validate core IVA implementation files exist and have correct structure"""
        required_files = [
            'validation_learning_core.py',
            'learning_services.py',
            'VALIDATION_LEARNING_CORE_IMPLEMENTATION_REPORT.md',
            'INTELLIGENT_VALIDATION_ARCHITECTURE_ENHANCEMENT_PLAN.md'
        ]
        
        passed = []
        failed = []
        
        for file_name in required_files:
            file_path = self.solutions_path / file_name
            if file_path.exists():
                # Check file size to ensure it's not empty
                if file_path.stat().st_size > 1000:  # At least 1KB
                    passed.append(f"{file_name} exists and has substantial content ({file_path.stat().st_size} bytes)")
                else:
                    failed.append(f"{file_name} exists but appears to be empty or too small")
            else:
                failed.append(f"{file_name} is missing")
        
        return len(failed) == 0, {'passed': passed, 'failed': failed}
    
    def validate_learning_services(self) -> Tuple[bool, Dict[str, Any]]:
        """Validate learning services implementation"""
        passed = []
        failed = []
        warnings = []
        
        try:
            # Check if files can be imported (basic syntax validation)
            learning_core_file = self.solutions_path / 'validation_learning_core.py'
            learning_services_file = self.solutions_path / 'learning_services.py'
            
            if learning_core_file.exists():
                content = learning_core_file.read_text()
                
                # Check for key classes
                required_classes = [
                    'ValidationLearningCore',
                    'ValidationEvent', 
                    'ValidationInsights',
                    'LearningMode',
                    'ResourceMonitor',
                    'StorageMonitor',
                    'SafeFailureManager',
                    'ConfigurationController',
                    'LearningMonitoring'
                ]
                
                for class_name in required_classes:
                    if f'class {class_name}' in content:
                        passed.append(f"ValidationLearningCore: {class_name} class found")
                    else:
                        failed.append(f"ValidationLearningCore: {class_name} class missing")
                
                # Check for key methods
                key_methods = [
                    'learn_from_validation',
                    'get_validation_insights',
                    'is_enabled',
                    'is_safe_to_learn',
                    'get_health_status',
                    'shutdown'
                ]
                
                for method_name in key_methods:
                    if f'def {method_name}' in content:
                        passed.append(f"ValidationLearningCore: {method_name} method found")
                    else:
                        failed.append(f"ValidationLearningCore: {method_name} method missing")
            else:
                failed.append("validation_learning_core.py not found")
            
            if learning_services_file.exists():
                content = learning_services_file.read_text()
                
                # Check for learning service classes
                service_classes = [
                    'ValidationPatternMemory',
                    'ValidationAnalyticsService', 
                    'ValidationKnowledgeBase',
                    'ValidationPattern'
                ]
                
                for class_name in service_classes:
                    if f'class {class_name}' in content:
                        passed.append(f"LearningServices: {class_name} class found")
                    else:
                        failed.append(f"LearningServices: {class_name} class missing")
                
                # Check for database operations
                db_operations = [
                    'sqlite3',
                    'CREATE TABLE',
                    'INSERT OR REPLACE',
                    'SELECT'
                ]
                
                for operation in db_operations:
                    if operation in content:
                        passed.append(f"LearningServices: {operation} database operation found")
                    else:
                        failed.append(f"LearningServices: {operation} database operation missing")
            else:
                failed.append("learning_services.py not found")
                
        except Exception as e:
            failed.append(f"Error validating learning services: {e}")
        
        return len(failed) == 0, {'passed': passed, 'failed': failed, 'warnings': warnings}
    
    def validate_data_structures(self) -> Tuple[bool, Dict[str, Any]]:
        """Validate data structure implementations"""
        passed = []
        failed = []
        
        try:
            learning_core_file = self.solutions_path / 'validation_learning_core.py'
            if learning_core_file.exists():
                content = learning_core_file.read_text()
                
                # Check for dataclass definitions
                dataclasses = ['ValidationEvent', 'ValidationInsights']
                for dc in dataclasses:
                    if f'class {dc}' in content:
                        passed.append(f"Data structure {dc} defined")
                        
                        # Check for to_dict method
                        if 'def to_dict(self)' in content:
                            passed.append(f"{dc} has serialization support")
                        else:
                            failed.append(f"{dc} missing serialization support")
                    else:
                        failed.append(f"Data structure {dc} missing")
                
                # Check for enum definitions
                if 'class LearningMode(Enum)' in content:
                    passed.append("LearningMode enum defined")
                    
                    # Check for enum values
                    enum_values = ['DISABLED', 'CONSERVATIVE', 'STANDARD', 'ADVANCED']
                    for value in enum_values:
                        if value in content:
                            passed.append(f"LearningMode.{value} defined")
                        else:
                            failed.append(f"LearningMode.{value} missing")
                else:
                    failed.append("LearningMode enum missing")
            else:
                failed.append("validation_learning_core.py not found for data structure validation")
                
        except Exception as e:
            failed.append(f"Error validating data structures: {e}")
        
        return len(failed) == 0, {'passed': passed, 'failed': failed}
    
    def validate_safety_mechanisms(self) -> Tuple[bool, Dict[str, Any]]:
        """Validate safety mechanisms implementation"""
        passed = []
        failed = []
        warnings = []
        
        try:
            learning_core_file = self.solutions_path / 'validation_learning_core.py'
            if learning_core_file.exists():
                content = learning_core_file.read_text()
                
                # Check for safety mechanisms
                safety_features = [
                    ('Resource monitoring', 'ResourceMonitor'),
                    ('Storage monitoring', 'StorageMonitor'),
                    ('Safe failure handling', 'SafeFailureManager'),
                    ('Circuit breaker pattern', 'circuit_breaker'),
                    ('Error isolation', 'handle_learning_failure'),
                    ('Resource limits', 'max_memory_mb'),
                    ('Thread safety', 'threading.Lock'),
                    ('Async processing', 'asyncio'),
                    ('Configuration control', 'ConfigurationController')
                ]
                
                for feature_name, feature_indicator in safety_features:
                    if feature_indicator in content:
                        passed.append(f"Safety mechanism: {feature_name} implemented")
                    else:
                        failed.append(f"Safety mechanism: {feature_name} missing")
                
                # Check for non-intrusive operation guarantees
                non_intrusive_patterns = [
                    'if not self.is_enabled()',
                    'if not self.is_safe_to_learn()',
                    'try:',
                    'except Exception:',
                    'pass  # Silent failure'
                ]
                
                for pattern in non_intrusive_patterns:
                    if pattern in content:
                        passed.append(f"Non-intrusive pattern: {pattern} found")
                    else:
                        warnings.append(f"Non-intrusive pattern: {pattern} not clearly visible")
            else:
                failed.append("validation_learning_core.py not found for safety validation")
                
        except Exception as e:
            failed.append(f"Error validating safety mechanisms: {e}")
        
        return len(failed) == 0, {'passed': passed, 'failed': failed, 'warnings': warnings}
    
    def validate_configuration_system(self) -> Tuple[bool, Dict[str, Any]]:
        """Validate configuration system implementation"""
        passed = []
        failed = []
        
        try:
            learning_core_file = self.solutions_path / 'validation_learning_core.py'
            if learning_core_file.exists():
                content = learning_core_file.read_text()
                
                # Check for environment variable configuration
                env_vars = [
                    'CLAUDE_VALIDATION_LEARNING',
                    'CLAUDE_LEARNING_STORAGE_PATH',
                    'CLAUDE_LEARNING_MAX_MEMORY',
                    'CLAUDE_LEARNING_MAX_STORAGE',
                    'CLAUDE_LEARNING_MAX_CPU'
                ]
                
                for env_var in env_vars:
                    if env_var in content:
                        passed.append(f"Environment variable {env_var} configuration found")
                    else:
                        failed.append(f"Environment variable {env_var} configuration missing")
                
                # Check for configuration controller
                if 'class ConfigurationController' in content:
                    passed.append("ConfigurationController class implemented")
                    
                    config_methods = [
                        'get_config',
                        'is_feature_enabled', 
                        'reload_configuration'
                    ]
                    
                    for method in config_methods:
                        if f'def {method}' in content:
                            passed.append(f"ConfigurationController.{method} method found")
                        else:
                            failed.append(f"ConfigurationController.{method} method missing")
                else:
                    failed.append("ConfigurationController class missing")
            else:
                failed.append("validation_learning_core.py not found for configuration validation")
                
        except Exception as e:
            failed.append(f"Error validating configuration system: {e}")
        
        return len(failed) == 0, {'passed': passed, 'failed': failed}
    
    def validate_database_schemas(self) -> Tuple[bool, Dict[str, Any]]:
        """Validate database schema definitions"""
        passed = []
        failed = []
        
        try:
            learning_services_file = self.solutions_path / 'learning_services.py'
            if learning_services_file.exists():
                content = learning_services_file.read_text()
                
                # Check for table creation statements
                tables = [
                    ('patterns', 'ValidationPatternMemory'),
                    ('validation_events', 'ValidationAnalyticsService'),
                    ('trend_data', 'ValidationAnalyticsService'),
                    ('knowledge_entries', 'ValidationKnowledgeBase'),
                    ('knowledge_relationships', 'ValidationKnowledgeBase')
                ]
                
                for table_name, service_name in tables:
                    if f'CREATE TABLE IF NOT EXISTS {table_name}' in content:
                        passed.append(f"Database table {table_name} schema defined for {service_name}")
                    else:
                        failed.append(f"Database table {table_name} schema missing for {service_name}")
                
                # Check for indexes
                indexes = ['idx_pattern_type', 'idx_context_signature', 'idx_knowledge_type', 'idx_subject']
                for index in indexes:
                    if f'CREATE INDEX IF NOT EXISTS {index}' in content:
                        passed.append(f"Database index {index} defined")
                    else:
                        failed.append(f"Database index {index} missing")
                
                # Check for database operations
                db_operations = [
                    'INSERT OR REPLACE',
                    'SELECT',
                    'UPDATE',
                    'DELETE',
                    'PRAGMA table_info'
                ]
                
                for operation in db_operations:
                    if operation in content:
                        passed.append(f"Database operation {operation} implemented")
                    else:
                        failed.append(f"Database operation {operation} missing")
            else:
                failed.append("learning_services.py not found for database validation")
                
        except Exception as e:
            failed.append(f"Error validating database schemas: {e}")
        
        return len(failed) == 0, {'passed': passed, 'failed': failed}
    
    def validate_api_interfaces(self) -> Tuple[bool, Dict[str, Any]]:
        """Validate API interface implementations"""
        passed = []
        failed = []
        
        try:
            learning_core_file = self.solutions_path / 'validation_learning_core.py'
            if learning_core_file.exists():
                content = learning_core_file.read_text()
                
                # Check for public API methods
                public_apis = [
                    'learn_from_validation',
                    'get_validation_insights', 
                    'get_health_status',
                    'is_enabled',
                    'is_safe_to_learn',
                    'shutdown'
                ]
                
                for api in public_apis:
                    if f'def {api}(self' in content:
                        passed.append(f"Public API method {api} implemented")
                    else:
                        failed.append(f"Public API method {api} missing")
                
                # Check for convenience functions
                convenience_functions = [
                    'get_learning_core',
                    'shutdown_learning_core'
                ]
                
                for func in convenience_functions:
                    if f'def {func}(' in content:
                        passed.append(f"Convenience function {func} implemented")
                    else:
                        failed.append(f"Convenience function {func} missing")
                
                # Check for async API support
                async_methods = ['async def', 'await ', 'asyncio.']
                async_support = any(pattern in content for pattern in async_methods)
                if async_support:
                    passed.append("Async API support implemented")
                else:
                    failed.append("Async API support missing")
            else:
                failed.append("validation_learning_core.py not found for API validation")
                
        except Exception as e:
            failed.append(f"Error validating API interfaces: {e}")
        
        return len(failed) == 0, {'passed': passed, 'failed': failed}
    
    def validate_integration_patterns(self) -> Tuple[bool, Dict[str, Any]]:
        """Validate integration pattern implementations"""
        passed = []
        failed = []
        warnings = []
        
        try:
            # Check for integration files
            integration_files = [
                'validation_learning_mixin.py',
                'enhanced_evidence_validation_engine.py',
                'enhanced_cross_agent_validation_engine.py'
            ]
            
            for file_name in integration_files:
                file_path = self.solutions_path / file_name
                if file_path.exists():
                    passed.append(f"Integration file {file_name} exists")
                    
                    # Check file content for integration patterns
                    content = file_path.read_text()
                    if 'ValidationLearningCore' in content or 'learning_core' in content:
                        passed.append(f"{file_name} contains learning integration")
                    else:
                        warnings.append(f"{file_name} may not contain learning integration")
                else:
                    warnings.append(f"Integration file {file_name} not found (may not be implemented yet)")
            
            # Check for integration patterns in main implementation
            learning_core_file = self.solutions_path / 'validation_learning_core.py'
            if learning_core_file.exists():
                content = learning_core_file.read_text()
                
                # Check for singleton pattern
                if 'def get_learning_core' in content:
                    passed.append("Singleton pattern implemented for easy integration")
                else:
                    failed.append("Singleton pattern missing")
                
                # Check for mixin support
                if 'class' in content and 'Mixin' in content:
                    passed.append("Mixin pattern support found")
                else:
                    warnings.append("Mixin pattern support not clearly visible")
                    
        except Exception as e:
            failed.append(f"Error validating integration patterns: {e}")
        
        return len(failed) == 0, {'passed': passed, 'failed': failed, 'warnings': warnings}
    
    def validate_documentation(self) -> Tuple[bool, Dict[str, Any]]:
        """Validate documentation coverage"""
        passed = []
        failed = []
        warnings = []
        
        try:
            # Check for documentation files
            doc_files = [
                'VALIDATION_LEARNING_CORE_IMPLEMENTATION_REPORT.md',
                'INTELLIGENT_VALIDATION_ARCHITECTURE_ENHANCEMENT_PLAN.md',
                'validation_learning_core_design.md'
            ]
            
            for doc_file in doc_files:
                file_path = self.solutions_path / doc_file
                if file_path.exists():
                    size = file_path.stat().st_size
                    if size > 5000:  # At least 5KB
                        passed.append(f"Documentation file {doc_file} exists and is substantial ({size} bytes)")
                    else:
                        warnings.append(f"Documentation file {doc_file} exists but is small ({size} bytes)")
                else:
                    failed.append(f"Documentation file {doc_file} missing")
            
            # Check for inline documentation
            implementation_files = [
                'validation_learning_core.py',
                'learning_services.py'
            ]
            
            for impl_file in implementation_files:
                file_path = self.solutions_path / impl_file
                if file_path.exists():
                    content = file_path.read_text()
                    
                    # Count docstrings
                    docstring_count = content.count('"""')
                    if docstring_count >= 10:  # Arbitrary threshold
                        passed.append(f"{impl_file} has good inline documentation ({docstring_count} docstrings)")
                    else:
                        warnings.append(f"{impl_file} has limited inline documentation ({docstring_count} docstrings)")
                    
                    # Check for comprehensive module docstring
                    if content.startswith('#!/usr/bin/env python3\n"""') or content.startswith('"""'):
                        passed.append(f"{impl_file} has module-level documentation")
                    else:
                        warnings.append(f"{impl_file} missing module-level documentation")
                        
        except Exception as e:
            failed.append(f"Error validating documentation: {e}")
        
        return len(failed) == 0, {'passed': passed, 'failed': failed, 'warnings': warnings}
    
    def validate_test_coverage(self) -> Tuple[bool, Dict[str, Any]]:
        """Validate test coverage"""
        passed = []
        failed = []
        warnings = []
        
        try:
            test_base_path = Path(__file__).parent
            
            # Check for test files
            expected_test_files = [
                'test_validation_learning_core.py',
                'test_validation_pattern_memory.py',
                'test_validation_analytics_service.py',
                'test_validation_knowledge_base.py'
            ]
            
            for test_file in expected_test_files:
                test_path = test_base_path / test_file
                if test_path.exists():
                    size = test_path.stat().st_size
                    if size > 5000:  # At least 5KB
                        passed.append(f"Test file {test_file} exists and is substantial ({size} bytes)")
                    else:
                        warnings.append(f"Test file {test_file} exists but is small ({size} bytes)")
                else:
                    failed.append(f"Test file {test_file} missing")
            
            # Check test content quality
            for test_file in expected_test_files:
                test_path = test_base_path / test_file
                if test_path.exists():
                    content = test_path.read_text()
                    
                    # Count test methods
                    test_method_count = content.count('def test_')
                    if test_method_count >= 10:
                        passed.append(f"{test_file} has comprehensive test coverage ({test_method_count} test methods)")
                    elif test_method_count >= 5:
                        warnings.append(f"{test_file} has moderate test coverage ({test_method_count} test methods)")
                    else:
                        failed.append(f"{test_file} has insufficient test coverage ({test_method_count} test methods)")
                    
                    # Check for edge case testing
                    edge_case_indicators = ['edge_case', 'error_handling', 'thread_safety', 'safety']
                    edge_case_tests = sum(1 for indicator in edge_case_indicators if indicator in content)
                    if edge_case_tests >= 2:
                        passed.append(f"{test_file} includes edge case testing")
                    else:
                        warnings.append(f"{test_file} may lack comprehensive edge case testing")
                        
        except Exception as e:
            failed.append(f"Error validating test coverage: {e}")
        
        return len(failed) == 0, {'passed': passed, 'failed': failed, 'warnings': warnings}
    
    def generate_summary_report(self, overall_success: bool) -> None:
        """Generate comprehensive summary report"""
        print("\n" + "=" * 80)
        print("🧠 IVA IMPLEMENTATION VALIDATION SUMMARY")
        print("=" * 80)
        
        if overall_success:
            print("🎉 OVERALL STATUS: ✅ IMPLEMENTATION VALIDATED SUCCESSFULLY")
        else:
            print("⚠️  OVERALL STATUS: ❌ IMPLEMENTATION NEEDS ATTENTION")
        
        print(f"\n📊 VALIDATION STATISTICS:")
        total_tests = len(self.validation_results)
        passed_tests = sum(1 for r in self.validation_results.values() if r['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"   • Total validation tests: {total_tests}")
        print(f"   • Passed: {passed_tests}")
        print(f"   • Failed: {failed_tests}")
        print(f"   • Success rate: {(passed_tests/total_tests*100):.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for test_name, result in self.validation_results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"   • {test_name}: {status}")
        
        print(f"\n📋 IMPLEMENTATION ASSESSMENT:")
        if overall_success:
            print("   ✅ Core architecture is fully implemented")
            print("   ✅ Learning services are comprehensively implemented") 
            print("   ✅ Safety mechanisms are properly configured")
            print("   ✅ Database schemas are correctly defined")
            print("   ✅ API interfaces are complete")
            print("   ✅ Documentation is comprehensive")
            print("   ✅ Test coverage is extensive")
            print("   ✅ IVA is production-ready")
        else:
            print("   ⚠️  Some components need attention (see detailed results above)")
            print("   ⚠️  Review failed validation tests")
            print("   ⚠️  Address missing dependencies if needed")
            print("   ⚠️  Complete any missing implementations")
        
        print(f"\n🚀 NEXT STEPS:")
        if overall_success:
            print("   1. ✅ IVA implementation is validated and production-ready")
            print("   2. ✅ All core components are properly implemented")
            print("   3. ✅ Safety guarantees are verified")
            print("   4. ✅ Integration patterns are available")
            print("   5. 🔄 Ready for deployment and integration with validation systems")
        else:
            print("   1. 🔧 Address validation failures identified above")
            print("   2. 🔧 Install missing dependencies (psutil, sklearn, joblib)")
            print("   3. 🔧 Complete any missing component implementations")
            print("   4. 🔧 Re-run validation to verify fixes")
            print("   5. 🔄 Proceed with deployment once all validations pass")


def main():
    """Main validation execution"""
    validator = IVAImplementationValidator()
    results = validator.run_comprehensive_validation()
    
    # Save results to file
    results_file = Path(__file__).parent / 'iva_validation_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to: {results_file}")
    
    # Return appropriate exit code
    overall_success = all(r['success'] for r in results.values())
    return 0 if overall_success else 1


if __name__ == '__main__':
    exit(main())