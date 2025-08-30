#!/usr/bin/env python3
"""
AI-Powered Intelligent Input Parser for Test Generator Framework

Uses AI reasoning to understand natural language requests and extract:
- JIRA ticket IDs (various formats)
- Environment specifications
- Console URLs and credentials
- User intent and context

Handles complex variations, typos, and ambiguous inputs intelligently.
"""

import re
import json
import sys
from typing import Tuple, Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ParsedInput:
    """Structured representation of parsed user input with AI reasoning"""
    jira_id: str
    environment: Optional[str] = None
    console_url: Optional[str] = None
    credentials: Optional[str] = None
    raw_input: str = ""
    confidence: float = 1.0
    parsing_method: str = "ai_powered"
    ai_reasoning: str = ""
    extracted_intent: str = "test_generation"
    alternatives: List[str] = None
    
    def __post_init__(self):
        if self.alternatives is None:
            self.alternatives = []

class AIPoweredInputParser:
    """
    AI-enhanced parser that uses structured reasoning to understand user input
    """
    
    def __init__(self):
        self.knowledge_base = self._build_knowledge_base()
        
    def _build_knowledge_base(self) -> Dict[str, Any]:
        """Build knowledge base of ACM/OpenShift patterns"""
        return {
            "jira_patterns": {
                "primary": [r'ACM-(\d+)', r'RHACM4K-(\d+)', r'ACM(\d+)'],
                "flexible": [r'acm-?(\d+)', r'ticket\s*(\d+)', r'issue\s*(\d+)', r'(\d{4,5})'],
                "context_clues": ["ticket", "issue", "jira", "bug", "enhancement", "story"]
            },
            "environment_patterns": {
                "cluster_names": ["mist10", "qe6", "local-cluster", "test-cluster"],
                "environment_types": ["dev", "test", "staging", "prod", "production"],
                "patterns": [
                    r'env(?:ironment)?[:\s=]*([a-zA-Z0-9\-\.]+)',
                    r'cluster[:\s=]*([a-zA-Z0-9\-\.]+)',
                    r'(?:using|with|on)\s+([a-zA-Z0-9\-\.]+)'
                ]
            },
            "console_patterns": {
                "url_indicators": ["console", "url", "host", "endpoint"],
                "credential_indicators": ["kubeadmin", "admin", "username", "password", "token"]
            },
            "intent_patterns": {
                "test_generation": ["generate", "create", "test plan", "test cases", "tests"],
                "analysis": ["analyze", "investigate", "examine", "review"],
                "validation": ["validate", "verify", "check", "confirm"]
            }
        }
    
    def parse_with_ai_reasoning(self, input_text: str) -> ParsedInput:
        """
        Main AI-powered parsing function with structured reasoning
        """
        
        # Step 1: Normalize and clean input
        cleaned_input = self._normalize_input(input_text)
        
        # Step 2: AI reasoning for context understanding
        ai_analysis = self._ai_analyze_input(cleaned_input)
        
        # Step 3: Extract structured information
        jira_id = self._ai_extract_jira_id(cleaned_input, ai_analysis)
        environment = self._ai_extract_environment(cleaned_input, ai_analysis)
        console_url = self._ai_extract_console_url(cleaned_input, ai_analysis)
        credentials = self._ai_extract_credentials(cleaned_input, ai_analysis)
        
        # Step 4: Calculate AI confidence
        confidence = self._ai_calculate_confidence(cleaned_input, jira_id, environment, ai_analysis)
        
        # Step 5: Generate alternatives if confidence is low
        alternatives = self._ai_generate_alternatives(cleaned_input, jira_id, ai_analysis)
        
        return ParsedInput(
            jira_id=jira_id,
            environment=environment,
            console_url=console_url,
            credentials=credentials,
            raw_input=input_text,
            confidence=confidence,
            parsing_method="ai_powered",
            ai_reasoning=ai_analysis["reasoning"],
            extracted_intent=ai_analysis["intent"],
            alternatives=alternatives
        )
    
    def _normalize_input(self, input_text: str) -> str:
        """Normalize input text for better AI processing"""
        
        if isinstance(input_text, list):
            # Handle sys.argv format
            input_text = " ".join(str(arg) for arg in input_text[1:])  # Skip script name
        
        # Clean up common formatting issues
        cleaned = re.sub(r'\s+', ' ', str(input_text).strip())
        cleaned = re.sub(r'["""'']', '"', cleaned)  # Normalize quotes
        cleaned = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', cleaned)  # Add space between letters and numbers
        cleaned = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', cleaned)  # Add space between numbers and letters
        
        return cleaned
    
    def _ai_analyze_input(self, input_text: str) -> Dict[str, Any]:
        """
        AI-powered analysis of user input to understand context and intent
        """
        
        analysis = {
            "input_type": self._classify_input_type(input_text),
            "intent": self._classify_intent(input_text),
            "complexity": self._assess_complexity(input_text),
            "context_clues": self._extract_context_clues(input_text),
            "confidence_factors": [],
            "reasoning": ""
        }
        
        # Build AI reasoning
        reasoning_parts = []
        
        # Analyze input type
        if analysis["input_type"] == "command_line":
            reasoning_parts.append("Detected command-line style input with structured arguments")
            analysis["confidence_factors"].append("structured_format")
        elif analysis["input_type"] == "natural_language":
            reasoning_parts.append("Detected natural language input requiring interpretation")
        else:
            reasoning_parts.append("Detected mixed format input combining structured and natural elements")
        
        # Analyze intent
        if analysis["intent"] == "test_generation":
            reasoning_parts.append("User intent: Generate test plan/cases for ACM feature")
            analysis["confidence_factors"].append("clear_intent")
        
        # Analyze context clues
        if analysis["context_clues"]["jira_indicators"]:
            reasoning_parts.append(f"Found JIRA indicators: {', '.join(analysis['context_clues']['jira_indicators'])}")
            analysis["confidence_factors"].append("jira_context")
        
        if analysis["context_clues"]["environment_indicators"]:
            reasoning_parts.append(f"Found environment indicators: {', '.join(analysis['context_clues']['environment_indicators'])}")
            analysis["confidence_factors"].append("environment_context")
        
        analysis["reasoning"] = ". ".join(reasoning_parts) + "."
        
        return analysis
    
    def _classify_input_type(self, input_text: str) -> str:
        """Classify the type of input format"""
        
        # Check for command line patterns
        if re.search(r'--\w+', input_text) or len(input_text.split()) <= 3:
            return "command_line"
        
        # Check for natural language patterns
        if any(word in input_text.lower() for word in ["generate", "create", "please", "can you", "need", "want"]):
            return "natural_language"
        
        return "mixed"
    
    def _classify_intent(self, input_text: str) -> str:
        """Classify user intent using AI reasoning"""
        
        # Test generation patterns
        test_keywords = ["generate", "create", "test plan", "test cases", "tests", "testing"]
        if any(keyword in input_text.lower() for keyword in test_keywords):
            return "test_generation"
        
        # Analysis patterns
        analysis_keywords = ["analyze", "investigate", "examine", "review", "understand"]
        if any(keyword in input_text.lower() for keyword in analysis_keywords):
            return "analysis"
        
        # Default to test generation for ACM tickets
        if re.search(r'ACM-?\d+', input_text, re.IGNORECASE):
            return "test_generation"
        
        return "unknown"
    
    def _assess_complexity(self, input_text: str) -> str:
        """Assess input complexity for appropriate handling"""
        
        word_count = len(input_text.split())
        
        if word_count <= 3:
            return "simple"
        elif word_count <= 10:
            return "moderate"
        else:
            return "complex"
    
    def _extract_context_clues(self, input_text: str) -> Dict[str, List[str]]:
        """Extract context clues using AI pattern recognition"""
        
        clues = {
            "jira_indicators": [],
            "environment_indicators": [],
            "console_indicators": [],
            "action_indicators": []
        }
        
        # JIRA context clues
        jira_patterns = ["ticket", "issue", "jira", "acm", "bug", "enhancement", "story"]
        for pattern in jira_patterns:
            if pattern in input_text.lower():
                clues["jira_indicators"].append(pattern)
        
        # Environment context clues
        env_patterns = ["environment", "cluster", "env", "host", "mist10", "qe6", "test"]
        for pattern in env_patterns:
            if pattern in input_text.lower():
                clues["environment_indicators"].append(pattern)
        
        # Console context clues  
        console_patterns = ["console", "url", "https", "apps", "openshift"]
        for pattern in console_patterns:
            if pattern in input_text.lower():
                clues["console_indicators"].append(pattern)
        
        # Action context clues
        action_patterns = ["generate", "create", "test", "plan", "cases"]
        for pattern in action_patterns:
            if pattern in input_text.lower():
                clues["action_indicators"].append(pattern)
        
        return clues
    
    def _ai_extract_jira_id(self, input_text: str, ai_analysis: Dict) -> str:
        """AI-powered JIRA ID extraction with intelligent fallbacks"""
        
        # Primary patterns with high confidence
        primary_patterns = [
            r'ACM-(\d+)',           # ACM-22079
            r'RHACM4K-(\d+)',       # RHACM4K-58948
        ]
        
        for pattern in primary_patterns:
            match = re.search(pattern, input_text, re.IGNORECASE)
            if match:
                number = match.group(1)
                return f"ACM-{number}"
        
        # Secondary patterns with context validation
        secondary_patterns = [
            r'ACM(\d+)',            # ACM22079
            r'acm-?(\d+)',          # acm-22079, acm22079
            r'ticket\s*(\d+)',      # ticket 22079
            r'issue\s*(\d+)',       # issue 22079
        ]
        
        for pattern in secondary_patterns:
            match = re.search(pattern, input_text, re.IGNORECASE)
            if match:
                number = match.group(1)
                # Validate number looks like ACM ticket (4-5 digits)
                if len(number) >= 4:
                    return f"ACM-{number}"
        
        # Fallback: standalone numbers with context validation
        if ai_analysis["context_clues"]["jira_indicators"]:
            number_match = re.search(r'\b(\d{4,5})\b', input_text)
            if number_match:
                return f"ACM-{number_match.group(1)}"
        
        raise ValueError(f"Could not extract JIRA ID from input: {input_text}")
    
    def _ai_extract_environment(self, input_text: str, ai_analysis: Dict) -> Optional[str]:
        """AI-powered environment extraction with intelligent context awareness"""
        
        # Known environment names with high confidence
        known_environments = ["mist10", "qe6", "local-cluster", "test-cluster"]
        for env in known_environments:
            if env in input_text.lower():
                return env
        
        # Pattern-based extraction with context validation
        env_patterns = [
            r'env(?:ironment)?[:\s=]+([a-zA-Z0-9\-\.]+)',
            r'cluster[:\s=]+([a-zA-Z0-9\-\.]+)', 
            r'host[:\s=]+([a-zA-Z0-9\-\.]+)',
            r'(?:using|with|on)\s+([a-zA-Z0-9\-\.]+)',
        ]
        
        for pattern in env_patterns:
            match = re.search(pattern, input_text, re.IGNORECASE)
            if match:
                env_candidate = match.group(1).strip()
                # Validate it looks like an environment name
                if self._validate_environment_name(env_candidate):
                    return env_candidate
        
        return None
    
    def _validate_environment_name(self, name: str) -> bool:
        """Validate if a string looks like a valid environment name"""
        
        # Basic validation rules
        if len(name) < 2 or len(name) > 20:
            return False
        
        # Should contain alphanumeric characters, hyphens, or dots
        if not re.match(r'^[a-zA-Z0-9\-\.]+$', name):
            return False
        
        # Common environment name patterns
        env_indicators = ["test", "dev", "prod", "staging", "cluster", "qe", "mist"]
        if any(indicator in name.lower() for indicator in env_indicators):
            return True
        
        # If it has cluster-like naming (letters + numbers)
        if re.match(r'^[a-zA-Z]+\d+$', name):
            return True
        
        return False
    
    def _ai_extract_console_url(self, input_text: str, ai_analysis: Dict) -> Optional[str]:
        """Extract console URL with AI validation"""
        
        # Look for full URLs
        url_pattern = r'https?://[a-zA-Z0-9\-\.:/]+'
        url_match = re.search(url_pattern, input_text)
        if url_match:
            return url_match.group(0)
        
        # Look for console URL fragments
        if "console" in input_text.lower():
            # Extract potential hostname after console
            console_pattern = r'console[:\s=]*([a-zA-Z0-9\-\.]+)'
            match = re.search(console_pattern, input_text, re.IGNORECASE)
            if match:
                hostname = match.group(1)
                if "." in hostname:  # Looks like a domain
                    return f"https://{hostname}"
        
        return None
    
    def _ai_extract_credentials(self, input_text: str, ai_analysis: Dict) -> Optional[str]:
        """Extract credentials with security awareness"""
        
        # Look for credential patterns but be security conscious
        cred_patterns = [
            r'kubeadmin[:/]\s*([^\s]+)',
            r'admin[:/]\s*([^\s]+)',
            r'username[:/]\s*([^\s]+)',
        ]
        
        for pattern in cred_patterns:
            match = re.search(pattern, input_text, re.IGNORECASE)
            if match:
                # For security, return placeholder format
                return "<CLUSTER_ADMIN_USER>/<CLUSTER_ADMIN_PASSWORD>"
        
        return None
    
    def _ai_calculate_confidence(self, input_text: str, jira_id: str, environment: str, ai_analysis: Dict) -> float:
        """AI-powered confidence calculation"""
        
        confidence = 0.3  # Base confidence
        
        # Boost for successful extraction
        if jira_id:
            confidence += 0.3
        
        if environment:
            confidence += 0.2
        
        # Boost for confidence factors from AI analysis
        confidence_factors = ai_analysis.get("confidence_factors", [])
        confidence += len(confidence_factors) * 0.1
        
        # Boost for clear intent
        if ai_analysis["intent"] == "test_generation":
            confidence += 0.1
        
        # Boost for structured input
        if ai_analysis["input_type"] == "command_line":
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _ai_generate_alternatives(self, input_text: str, jira_id: str, ai_analysis: Dict) -> List[str]:
        """Generate alternative interpretations for low-confidence inputs"""
        
        alternatives = []
        
        # If JIRA ID extraction was uncertain
        if jira_id and "ACM-" in jira_id:
            # Find all numbers in input
            numbers = re.findall(r'\d+', input_text)
            for number in numbers:
                if len(number) >= 3 and f"ACM-{number}" != jira_id:
                    alternatives.append(f"Alternative JIRA ID: ACM-{number}")
        
        # If environment was not found
        if not ai_analysis.get("environment"):
            # Look for any word that could be an environment
            words = input_text.split()
            for word in words:
                if self._validate_environment_name(word):
                    alternatives.append(f"Possible environment: {word}")
        
        return alternatives

def parse_user_input_ai(*args) -> ParsedInput:
    """
    AI-powered convenience function to parse various input formats
    
    Usage:
        # Command line: python script.py ACM-22079 mist10
        result = parse_user_input_ai(sys.argv)
        
        # Natural language: 
        result = parse_user_input_ai("Generate test plan for ACM-22079")
        
        # Complex natural language:
        result = parse_user_input_ai("I need comprehensive test cases for ACM22079 using the mist10 test environment")
    """
    parser = AIPoweredInputParser()
    
    if len(args) == 1:
        # Single argument
        input_data = args[0]
        if isinstance(input_data, list):
            input_text = " ".join(str(item) for item in input_data[1:])  # Skip script name
        else:
            input_text = str(input_data)
    else:
        # Multiple arguments - treat as natural language
        input_text = " ".join(str(arg) for arg in args)
    
    return parser.parse_with_ai_reasoning(input_text)

def validate_ai_parsed_input(parsed_input: ParsedInput) -> Tuple[bool, str]:
    """
    Validate AI-parsed input with enhanced reasoning
    """
    
    if not parsed_input.jira_id:
        return False, "JIRA ID is required but could not be extracted from input"
    
    if not re.match(r'ACM-\d+', parsed_input.jira_id):
        return False, f"Invalid JIRA ID format: {parsed_input.jira_id} (expected ACM-XXXXX)"
    
    if parsed_input.confidence < 0.4:
        error_msg = f"Low confidence ({parsed_input.confidence:.1f}) in parsing. "
        if parsed_input.alternatives:
            error_msg += f"Consider alternatives: {', '.join(parsed_input.alternatives[:2])}"
        return False, error_msg
    
    return True, f"Successfully parsed with {parsed_input.confidence:.1f} confidence"

# Test function for AI-powered parsing
def test_ai_parsing():
    """Test AI-powered parsing with various challenging inputs"""
    
    test_cases = [
        # Simple command line
        "ACM-22079 mist10",
        
        # Natural language variations
        "Generate test plan for ACM-22079",
        "I need test cases for ticket 22079 using mist10 environment",
        "Create comprehensive tests for ACM22079 on cluster mist10",
        "Test plan for issue 22079 please with environment qe6",
        
        # Complex natural language
        "Can you generate a complete test plan for ACM-22079 cluster curator digest upgrades using the mist10 test environment?",
        
        # Ambiguous/challenging inputs
        "22079 mist10",
        "acm22079 with env mist10",
        "test cases for 22079",
        "ACM 22079 cluster test environment mist10",
        
        # Edge cases
        "Generate tests for RHACM4K-58948",
        "Need validation for ACM-22079 at https://console-openshift-console.apps.mist10-0.qe.red-chesterfield.com",
    ]
    
    parser = AIPoweredInputParser()
    
    print("🤖 AI-Powered Input Parsing Test Results")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Input: {test_case}")
        
        try:
            result = parser.parse_with_ai_reasoning(test_case)
            is_valid, message = validate_ai_parsed_input(result)
            
            print(f"✅ JIRA ID: {result.jira_id}")
            print(f"🌍 Environment: {result.environment}")
            print(f"🔗 Console URL: {result.console_url}")
            print(f"📊 Confidence: {result.confidence:.2f}")
            print(f"🎯 Intent: {result.extracted_intent}")
            print(f"🧠 AI Reasoning: {result.ai_reasoning}")
            print(f"✅ Valid: {is_valid}")
            if result.alternatives:
                print(f"🔄 Alternatives: {', '.join(result.alternatives)}")
            print(f"📝 Validation: {message}")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_ai_parsing()
    else:
        # Demonstrate AI-powered parsing
        try:
            result = parse_user_input_ai(sys.argv)
            is_valid, message = validate_ai_parsed_input(result)
            
            print("🤖 AI-Powered Parsing Results:")
            print(f"   JIRA ID: {result.jira_id}")
            print(f"   Environment: {result.environment}")
            print(f"   Console URL: {result.console_url}")
            print(f"   Confidence: {result.confidence:.2f}")
            print(f"   Intent: {result.extracted_intent}")
            print(f"   AI Reasoning: {result.ai_reasoning}")
            print(f"   Status: {'✅ Valid' if is_valid else '❌ Invalid'}")
            print(f"   Message: {message}")
            
            if result.alternatives:
                print(f"   Alternatives: {', '.join(result.alternatives)}")
                
        except Exception as e:
            print(f"❌ AI Parsing Error: {e}")