#!/usr/bin/env python3
"""
Test Script for AI-Powered Credential Scanner
=============================================

Demonstrates the improved accuracy of the AI-powered scanner
vs the original regex-based approach.
"""

import os
import tempfile
from ai_powered_credential_scanner import AICredentialScanner

def test_false_positive_cases():
    """Test cases that should NOT be flagged as security violations."""
    
    scanner = AICredentialScanner()
    
    test_cases = [
        # Case 1: Token counter variable (legitimate code)
        {
            'content': 'self.token_counter = TokenCounter(model="claude-4-sonnet-200k")',
            'description': 'Token counter variable assignment',
            'should_flag': False
        },
        
        # Case 2: JSON object key (legitimate data structure)
        {
            'content': '{"key": "ACM-20640", "title": "RBAC Implementation"}',
            'description': 'JSON object with key property',
            'should_flag': False
        },
        
        # Case 3: Lambda function parameter (legitimate code)
        {
            'content': 'sorted_items = sorted(items, key=lambda k: data[k]["count"])',
            'description': 'Lambda function with key parameter',
            'should_flag': False
        },
        
        # Case 4: Template placeholder (safe pattern)
        {
            'content': 'oc login <CLUSTER_CONSOLE_URL> -u <ADMIN_USER> -p <ADMIN_PASSWORD>',
            'description': 'Template with placeholders',
            'should_flag': False
        },
        
        # Case 5: Real credential (should be flagged)
        {
            'content': 'oc login https://api.real-cluster.com -u admin -p RealPassword123!',
            'description': 'Actual hardcoded credentials',
            'should_flag': True
        },
    ]
    
    print("🧪 Testing AI-Powered Scanner Against False Positive Cases")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['description']}")
        print(f"Content: {test_case['content']}")
        
        # Create temporary file for testing
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_case['content'])
            temp_file = f.name
        
        try:
            result = scanner.scan_file(temp_file)
            violations = result['violations']
            
            print(f"Violations found: {len(violations)}")
            print(f"Security status: {result['security_status']}")
            print(f"Confidence score: {result['confidence_score']:.2f}")
            
            # Check if result matches expectation
            has_violations = len(violations) > 0
            if has_violations == test_case['should_flag']:
                print("✅ CORRECT: Scanner behaved as expected")
            else:
                print("❌ INCORRECT: Scanner behavior doesn't match expectation")
                if violations:
                    for v in violations:
                        print(f"   - {v.description} (confidence: {v.confidence:.2f})")
        
        finally:
            os.unlink(temp_file)
    
    print("\n" + "=" * 60)
    print("🎯 AI Scanner Test Complete")

if __name__ == '__main__':
    test_false_positive_cases()
