#!/usr/bin/env python3
"""
Comprehensive Unit Tests for AI-Powered Input Parsing

Tests every conceivable way a user might request test plan generation:
- Command line variations (positional, named, mixed)
- Natural language variations (formal, casual, complex)
- JIRA ID formats (ACM-22079, 22079, acm22079, etc.)
- Environment specifications (mist10, "using qe6", etc.)
- Edge cases, error conditions, and robustness scenarios

Ensures the framework intelligently understands ANY user input correctly.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from typing import List, Tuple, Dict, Any

# Add the ai-services directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '.claude', 'ai-services'))

from ai_powered_input_parser import (
    AIPoweredInputParser, 
    ParsedInput, 
    parse_user_input_ai, 
    validate_ai_parsed_input
)

class TestAIPoweredInputParser(unittest.TestCase):
    """Comprehensive tests for AI-powered input parsing"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = AIPoweredInputParser()
        
    def _assert_parsed_correctly(self, input_text: str, expected_jira: str, 
                                expected_env: str = None, min_confidence: float = 0.4):
        """Helper to assert parsing results"""
        try:
            result = self.parser.parse_with_ai_reasoning(input_text)
            is_valid, message = validate_ai_parsed_input(result)
            
            self.assertTrue(is_valid, f"Parsing failed for '{input_text}': {message}")
            self.assertEqual(result.jira_id, expected_jira, 
                           f"Wrong JIRA ID for '{input_text}': got {result.jira_id}, expected {expected_jira}")
            
            if expected_env:
                self.assertIsNotNone(result.environment, f"Environment not extracted from '{input_text}'")
                self.assertIn(expected_env.lower(), result.environment.lower(), 
                            f"Wrong environment for '{input_text}': got {result.environment}, expected {expected_env}")
            
            self.assertGreaterEqual(result.confidence, min_confidence, 
                                  f"Confidence too low for '{input_text}': {result.confidence}")
            
            return result
            
        except Exception as e:
            self.fail(f"Parsing failed for '{input_text}' with exception: {e}")

class TestJiraIdVariations(TestAIPoweredInputParser):
    """Test all possible JIRA ID format variations"""
    
    def test_standard_jira_formats(self):
        """Test standard ACM-XXXXX formats"""
        test_cases = [
            ("ACM-22079", "ACM-22079"),
            ("ACM-1234", "ACM-1234"),
            ("ACM-99999", "ACM-99999"),
            ("ACM-12345", "ACM-12345"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected, min_confidence=0.9)
    
    def test_no_hyphen_formats(self):
        """Test ACM formats without hyphens"""
        test_cases = [
            ("ACM22079", "ACM-22079"),
            ("ACM1234", "ACM-1234"),
            ("ACM99999", "ACM-99999"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected, min_confidence=0.8)
    
    def test_lowercase_formats(self):
        """Test lowercase variations"""
        test_cases = [
            ("acm-22079", "ACM-22079"),
            ("acm22079", "ACM-22079"),
            ("acm-1234", "ACM-1234"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected, min_confidence=0.7)
    
    def test_context_based_jira_extraction(self):
        """Test JIRA ID extraction with context keywords"""
        test_cases = [
            ("ticket 22079", "ACM-22079"),
            ("issue 22079", "ACM-22079"),
            ("story ACM-22079", "ACM-22079"),
            ("bug 1234", "ACM-1234"),
            ("ticket ACM-22079", "ACM-22079"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected, min_confidence=0.6)
    
    def test_rhacm4k_formats(self):
        """Test RHACM4K format conversion"""
        test_cases = [
            ("RHACM4K-58948", "ACM-58948"),
            ("RHACM4K58948", "ACM-58948"),
            ("rhacm4k-12345", "ACM-12345"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected, min_confidence=0.8)
    
    def test_numbers_only_with_context(self):
        """Test standalone numbers with JIRA context"""
        test_cases = [
            ("Generate test plan for 22079", "ACM-22079"),
            ("I need tests for 1234", "ACM-1234"),
            ("Create test cases for issue 99999", "ACM-99999"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected, min_confidence=0.5)

class TestEnvironmentVariations(TestAIPoweredInputParser):
    """Test all possible environment specification variations"""
    
    def test_simple_environment_names(self):
        """Test simple environment names"""
        test_cases = [
            ("ACM-22079 mist10", "ACM-22079", "mist10"),
            ("ACM-22079 qe6", "ACM-22079", "qe6"),
            ("ACM-22079 test-cluster", "ACM-22079", "test-cluster"),
            ("ACM-22079 local-cluster", "ACM-22079", "local-cluster"),
        ]
        
        for input_text, expected_jira, expected_env in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected_jira, expected_env, min_confidence=0.8)
    
    def test_environment_with_keywords(self):
        """Test environment extraction with keywords"""
        test_cases = [
            ("ACM-22079 using mist10", "ACM-22079", "mist10"),
            ("ACM-22079 with qe6", "ACM-22079", "qe6"),
            ("ACM-22079 on cluster mist10", "ACM-22079", "mist10"),
            ("ACM-22079 environment qe6", "ACM-22079", "qe6"),
        ]
        
        for input_text, expected_jira, expected_env in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected_jira, expected_env, min_confidence=0.7)
    
    def test_environment_with_separators(self):
        """Test environment with various separators"""
        test_cases = [
            ("ACM-22079 env=mist10", "ACM-22079", "mist10"),
            ("ACM-22079 env: qe6", "ACM-22079", "qe6"),
            ("ACM-22079 cluster=mist10", "ACM-22079", "mist10"),
            ("ACM-22079 host: qe6", "ACM-22079", "qe6"),
        ]
        
        for input_text, expected_jira, expected_env in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected_jira, expected_env, min_confidence=0.6)
    
    def test_complex_environment_descriptions(self):
        """Test complex environment descriptions"""
        test_cases = [
            ("ACM-22079 mist10 test environment", "ACM-22079", "mist10"),
            ("ACM-22079 qe6 cluster environment", "ACM-22079", "qe6"),
            ("ACM-22079 using the mist10 test cluster", "ACM-22079", "mist10"),
        ]
        
        for input_text, expected_jira, expected_env in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected_jira, expected_env, min_confidence=0.5)

class TestNaturalLanguageVariations(TestAIPoweredInputParser):
    """Test natural language input variations"""
    
    def test_formal_requests(self):
        """Test formal request patterns"""
        test_cases = [
            ("Generate test plan for ACM-22079", "ACM-22079"),
            ("Create test cases for ACM-1234", "ACM-1234"),
            ("Please generate comprehensive tests for ACM-99999", "ACM-99999"),
            ("I need a test plan for ticket ACM-22079", "ACM-22079"),
        ]
        
        for input_text, expected_jira in test_cases:
            with self.subTest(input_text=input_text):
                result = self._assert_parsed_correctly(input_text, expected_jira, min_confidence=0.8)
                self.assertEqual(result.extracted_intent, "test_generation")
    
    def test_casual_requests(self):
        """Test casual/informal request patterns"""
        test_cases = [
            ("I need test cases for 22079", "ACM-22079"),
            ("Can you help with tests for ACM-1234?", "ACM-1234"),
            ("Test plan for 99999 please", "ACM-99999"),
            ("Help me with ACM-22079 testing", "ACM-22079"),
        ]
        
        for input_text, expected_jira in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected_jira, min_confidence=0.6)
    
    def test_complex_natural_language(self):
        """Test complex natural language descriptions"""
        test_cases = [
            ("Can you create comprehensive test scenarios for ACM-22079 ClusterCurator digest upgrades?", "ACM-22079"),
            ("I need detailed test cases for ACM-1234 covering all edge cases and scenarios", "ACM-1234"),
            ("Please generate a complete test plan for ticket 22079 including setup and validation", "ACM-22079"),
        ]
        
        for input_text, expected_jira in test_cases:
            with self.subTest(input_text=input_text):
                result = self._assert_parsed_correctly(input_text, expected_jira, min_confidence=0.5)
                self.assertEqual(result.parsing_method, "ai_powered")
    
    def test_natural_language_with_environment(self):
        """Test natural language with environment specifications"""
        test_cases = [
            ("Generate test plan for ACM-22079 using mist10", "ACM-22079", "mist10"),
            ("I need test cases for 1234 on qe6 cluster", "ACM-1234", "qe6"),
            ("Create tests for ACM-99999 with environment mist10", "ACM-99999", "mist10"),
            ("Test plan for 22079 using the qe6 test environment", "ACM-22079", "qe6"),
        ]
        
        for input_text, expected_jira, expected_env in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected_jira, expected_env, min_confidence=0.6)

class TestCommandLineVariations(TestAIPoweredInputParser):
    """Test command line argument variations"""
    
    def test_positional_arguments(self):
        """Test positional command line arguments"""
        test_cases = [
            (["script.py", "ACM-22079", "mist10"], "ACM-22079", "mist10"),
            (["script.py", "ACM-1234", "qe6"], "ACM-1234", "qe6"),
            (["script.py", "22079", "test-cluster"], "ACM-22079", "test-cluster"),
            (["script.py", "ACM22079"], "ACM-22079", None),
        ]
        
        for input_args, expected_jira, expected_env in test_cases:
            with self.subTest(input_args=input_args):
                result = self.parser.parse_with_ai_reasoning(input_args)
                is_valid, message = validate_ai_parsed_input(result)
                
                self.assertTrue(is_valid, f"Failed to parse {input_args}: {message}")
                self.assertEqual(result.jira_id, expected_jira)
                if expected_env:
                    self.assertIsNotNone(result.environment)
    
    def test_named_arguments(self):
        """Test named command line arguments"""
        # Note: These test the parsing logic, actual argparse would be tested differently
        test_cases = [
            ("--jira-id ACM-22079 --env-name mist10", "ACM-22079", "mist10"),
            ("--ticket ACM-1234 --environment qe6", "ACM-1234", "qe6"),
            ("--id 22079 --env test-cluster", "ACM-22079", "test-cluster"),
        ]
        
        for input_text, expected_jira, expected_env in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected_jira, expected_env, min_confidence=0.7)
    
    def test_mixed_arguments(self):
        """Test mixed positional and named arguments"""
        test_cases = [
            ("ACM-22079 --env mist10", "ACM-22079", "mist10"),
            ("22079 --environment qe6", "ACM-22079", "qe6"),
            ("--jira-id ACM-1234 test-cluster", "ACM-1234", "test-cluster"),
        ]
        
        for input_text, expected_jira, expected_env in test_cases:
            with self.subTest(input_text=input_text):
                self._assert_parsed_correctly(input_text, expected_jira, expected_env, min_confidence=0.6)

class TestEdgeCasesAndRobustness(TestAIPoweredInputParser):
    """Test edge cases, error conditions, and robustness"""
    
    def test_malformed_inputs(self):
        """Test handling of malformed inputs"""
        malformed_inputs = [
            "",
            "   ",
            "ACM",
            "ACM-",
            "ACM-abc",
            "22079-ACM",
            "###@@@ ACM-22079 $$$",
        ]
        
        for input_text in malformed_inputs:
            with self.subTest(input_text=repr(input_text)):
                try:
                    result = self.parser.parse_with_ai_reasoning(input_text)
                    is_valid, message = validate_ai_parsed_input(result)
                    
                    # Should either parse successfully or fail gracefully
                    if is_valid:
                        self.assertIsNotNone(result.jira_id)
                        self.assertGreater(len(result.jira_id), 0)
                    else:
                        self.assertIn("confidence", message.lower())
                        
                except ValueError as e:
                    # Expected for some malformed inputs
                    self.assertIn("Could not extract JIRA ID", str(e))
    
    def test_ambiguous_inputs(self):
        """Test handling of ambiguous inputs"""
        ambiguous_inputs = [
            "ACM-22079 ACM-1234",  # Multiple JIRA IDs
            "22079 1234 test plan",  # Multiple numbers
            "mist10 qe6 environment",  # Multiple environments
            "Generate test plan for something",  # No JIRA ID
        ]
        
        for input_text in ambiguous_inputs:
            with self.subTest(input_text=input_text):
                try:
                    result = self.parser.parse_with_ai_reasoning(input_text)
                    
                    # Should pick the first/best option
                    if result.jira_id:
                        self.assertTrue(result.jira_id.startswith("ACM-"))
                        
                    # Should have alternatives for ambiguous cases
                    if result.confidence < 0.8:
                        self.assertGreater(len(result.alternatives), 0)
                        
                except ValueError:
                    # Acceptable for truly ambiguous inputs
                    pass
    
    def test_unicode_and_special_characters(self):
        """Test handling of unicode and special characters"""
        special_inputs = [
            "ACM-22079 mist10 🚀",
            "Générer plan de test pour ACM-22079",
            "ACM-22079 тест план",
            "ACM-22079 with special chars: !@#$%",
        ]
        
        for input_text in special_inputs:
            with self.subTest(input_text=input_text):
                try:
                    result = self.parser.parse_with_ai_reasoning(input_text)
                    
                    # Should still extract basic info
                    if result.jira_id:
                        self.assertTrue(result.jira_id.startswith("ACM-"))
                        
                except Exception as e:
                    # Should not crash completely
                    self.assertIsInstance(e, (ValueError, UnicodeError))
    
    def test_very_long_inputs(self):
        """Test handling of very long inputs"""
        long_input = "Generate comprehensive test plan for ACM-22079 " + "very " * 100 + "long description using mist10"
        
        try:
            result = self.parser.parse_with_ai_reasoning(long_input)
            self.assertEqual(result.jira_id, "ACM-22079")
            # Should still work despite length
            
        except Exception as e:
            # Should fail gracefully if at all
            self.assertIsInstance(e, (ValueError, MemoryError))
    
    def test_confidence_scoring_accuracy(self):
        """Test confidence scoring accuracy"""
        high_confidence_cases = [
            ("ACM-22079 mist10", 0.9),
            ("Generate test plan for ACM-22079", 0.8),
            ("--jira-id ACM-22079 --env mist10", 0.9),
        ]
        
        low_confidence_cases = [
            ("maybe test something for 22079", 0.6),
            ("ACM test environment", 0.4),
            ("generate tests", 0.3),
        ]
        
        for input_text, min_confidence in high_confidence_cases:
            with self.subTest(input_text=input_text, expected="high"):
                try:
                    result = self.parser.parse_with_ai_reasoning(input_text)
                    self.assertGreaterEqual(result.confidence, min_confidence,
                                          f"Confidence too low for '{input_text}': {result.confidence}")
                except ValueError:
                    pass  # Acceptable for some edge cases
        
        for input_text, max_confidence in low_confidence_cases:
            with self.subTest(input_text=input_text, expected="low"):
                try:
                    result = self.parser.parse_with_ai_reasoning(input_text)
                    if result.jira_id:  # Only check if parsing succeeded
                        self.assertLessEqual(result.confidence, max_confidence,
                                           f"Confidence too high for '{input_text}': {result.confidence}")
                except ValueError:
                    pass  # Expected for low confidence inputs

class TestConvenienceFunctions(TestAIPoweredInputParser):
    """Test convenience functions and integration points"""
    
    def test_parse_user_input_ai_function(self):
        """Test the parse_user_input_ai convenience function"""
        test_cases = [
            ("ACM-22079", "ACM-22079"),
            ("Generate test plan for ACM-1234", "ACM-1234"),
            (["script.py", "ACM-99999", "mist10"], "ACM-99999"),
        ]
        
        for input_data, expected_jira in test_cases:
            with self.subTest(input_data=input_data):
                result = parse_user_input_ai(input_data)
                self.assertEqual(result.jira_id, expected_jira)
    
    def test_validate_ai_parsed_input_function(self):
        """Test the validate_ai_parsed_input function"""
        # Valid input
        valid_result = ParsedInput(
            jira_id="ACM-22079",
            environment="mist10",
            confidence=0.8,
            raw_input="ACM-22079 mist10"
        )
        is_valid, message = validate_ai_parsed_input(valid_result)
        self.assertTrue(is_valid)
        self.assertIn("Successfully parsed", message)
        
        # Invalid JIRA ID
        invalid_result = ParsedInput(
            jira_id="INVALID",
            confidence=0.8,
            raw_input="invalid input"
        )
        is_valid, message = validate_ai_parsed_input(invalid_result)
        self.assertFalse(is_valid)
        self.assertIn("Invalid JIRA ID format", message)
        
        # Low confidence
        low_confidence_result = ParsedInput(
            jira_id="ACM-22079",
            confidence=0.2,
            raw_input="ambiguous input",
            alternatives=["Try ACM-1234"]
        )
        is_valid, message = validate_ai_parsed_input(low_confidence_result)
        self.assertFalse(is_valid)
        self.assertIn("Low confidence", message)
        self.assertIn("alternatives", message)

class TestIntegrationWithFramework(unittest.TestCase):
    """Test integration with the main framework"""
    
    @patch('ai_powered_input_parser.AIPoweredInputParser.parse_with_ai_reasoning')
    def test_framework_integration_mock(self, mock_parse):
        """Test framework integration with mocked parser"""
        # Mock successful parsing
        mock_parse.return_value = ParsedInput(
            jira_id="ACM-22079",
            environment="mist10",
            confidence=0.9,
            parsing_method="ai_powered",
            ai_reasoning="Test reasoning",
            extracted_intent="test_generation"
        )
        
        result = parse_user_input_ai("test input")
        self.assertEqual(result.jira_id, "ACM-22079")
        self.assertEqual(result.environment, "mist10")
        self.assertGreaterEqual(result.confidence, 0.9)
    
    def test_sys_argv_simulation(self):
        """Test parsing sys.argv-style inputs"""
        argv_styles = [
            ["script.py", "ACM-22079"],
            ["script.py", "ACM-22079", "mist10"],
            ["script.py", "--jira-id", "ACM-22079"],
            ["script.py", "generate", "test", "plan", "for", "ACM-22079"],
        ]
        
        for argv_input in argv_styles:
            with self.subTest(argv_input=argv_input):
                try:
                    result = parse_user_input_ai(argv_input)
                    is_valid, message = validate_ai_parsed_input(result)
                    
                    if is_valid:
                        self.assertTrue(result.jira_id.startswith("ACM-"))
                        self.assertGreater(len(result.ai_reasoning), 0)
                    else:
                        # Should provide helpful feedback
                        self.assertIn("confidence", message.lower())
                        
                except ValueError as e:
                    # Should provide clear error message
                    self.assertIn("Could not extract JIRA ID", str(e))

def run_comprehensive_tests():
    """Run all comprehensive tests and provide detailed results"""
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestJiraIdVariations,
        TestEnvironmentVariations,
        TestNaturalLanguageVariations,
        TestCommandLineVariations,
        TestEdgeCasesAndRobustness,
        TestConvenienceFunctions,
        TestIntegrationWithFramework,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"COMPREHENSIVE INPUT PARSING TEST RESULTS")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split(chr(10))[-2]}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split(chr(10))[-2]}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)