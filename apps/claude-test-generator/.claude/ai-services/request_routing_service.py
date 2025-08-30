#!/usr/bin/env python3
"""
Request Routing Service for Claude Test Generator
===============================================

Automatically interprets natural language requests and routes them to proper framework execution.
Prevents direct AI simulation for framework-level requests.

CRITICAL FUNCTION: Bridge between natural language and Task tool orchestrator execution.
"""

import re
import logging
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class RequestType(Enum):
    """Classification of request types"""
    FRAMEWORK_EXECUTION = "framework_execution"      # Requires orchestrator
    DIRECT_AI_QUERY = "direct_ai_query"              # Can be answered directly
    FRAMEWORK_DEBUG = "framework_debug"              # Framework analysis/debugging
    INVALID_REQUEST = "invalid_request"              # Cannot be processed

@dataclass
class RoutingDecision:
    """Decision made by request router"""
    request_type: RequestType
    should_use_orchestrator: bool
    task_tool_config: Optional[Dict[str, Any]] = None
    confidence: float = 0.0
    reasoning: str = ""
    fallback_action: str = ""

class RequestRoutingService:
    """
    Service that automatically routes user requests to appropriate execution path
    """
    
    def __init__(self):
        self.framework_execution_patterns = [
            # Test generation requests
            r"generate.*test.*plan.*for.*([A-Z]+-\d+)",
            r"create.*test.*cases.*for.*([A-Z]+-\d+)", 
            r"test.*plan.*([A-Z]+-\d+)",
            r"comprehensive.*test.*cases.*([A-Z]+-\d+)",
            
            # Analysis requests requiring framework
            r"analyze.*([A-Z]+-\d+)",
            r"test.*([A-Z]+-\d+).*on.*([a-zA-Z0-9\-\.]+)",
            
            # Direct command patterns
            r"/generate\s+([A-Z]+-\d+)",
            r"/analyze\s+([A-Z]+-\d+)",
        ]
        
        self.direct_ai_patterns = [
            # Questions about code/framework
            r"what.*does.*code.*do",
            r"how.*does.*framework.*work",
            r"explain.*implementation",
            r"why.*did.*this.*happen",
            
            # Investigation requests
            r"investigate.*why",
            r"find.*root.*cause",
            r"ultrathink.*and.*figure.*out",
        ]
        
        self.framework_debug_patterns = [
            # Framework analysis
            r"analyze.*framework.*execution",
            r"investigate.*orchestrator",
            r"why.*phase.*\d+.*failed",
            r"what.*changed.*in.*routing",
        ]
    
    def classify_request(self, user_request: str) -> RoutingDecision:
        """
        Classify user request and determine routing decision
        """
        request_lower = user_request.lower()
        
        # Check for framework execution patterns
        for pattern in self.framework_execution_patterns:
            match = re.search(pattern, request_lower)
            if match:
                jira_id = match.group(1) if match.groups() else None
                environment = match.group(2) if len(match.groups()) > 1 else None
                
                return RoutingDecision(
                    request_type=RequestType.FRAMEWORK_EXECUTION,
                    should_use_orchestrator=True,
                    task_tool_config={
                        "subagent_type": "general-purpose",
                        "description": f"Execute full framework orchestrator for {jira_id}",
                        "prompt": self._create_orchestrator_prompt(jira_id, environment, user_request)
                    },
                    confidence=0.9,
                    reasoning=f"Detected framework execution request for {jira_id}",
                    fallback_action="manual_task_tool_execution"
                )
        
        # Check for direct AI query patterns
        for pattern in self.direct_ai_patterns:
            if re.search(pattern, request_lower):
                return RoutingDecision(
                    request_type=RequestType.DIRECT_AI_QUERY,
                    should_use_orchestrator=False,
                    confidence=0.8,
                    reasoning="Detected direct AI query - can be answered without orchestrator",
                    fallback_action="direct_ai_response"
                )
        
        # Check for framework debug patterns
        for pattern in self.framework_debug_patterns:
            if re.search(pattern, request_lower):
                return RoutingDecision(
                    request_type=RequestType.FRAMEWORK_DEBUG,
                    should_use_orchestrator=False,
                    confidence=0.7,
                    reasoning="Detected framework debugging request - requires analysis not execution",
                    fallback_action="framework_analysis_mode"
                )
        
        # Default: Assume framework execution if JIRA ID detected
        jira_match = re.search(r'([A-Z]+-\d+)', user_request)
        if jira_match:
            jira_id = jira_match.group(1)
            return RoutingDecision(
                request_type=RequestType.FRAMEWORK_EXECUTION,
                should_use_orchestrator=True,
                task_tool_config={
                    "subagent_type": "general-purpose", 
                    "description": f"Execute framework for {jira_id}",
                    "prompt": self._create_orchestrator_prompt(jira_id, None, user_request)
                },
                confidence=0.6,
                reasoning=f"JIRA ID detected ({jira_id}) - assuming framework execution needed",
                fallback_action="manual_task_tool_execution"
            )
        
        # No clear pattern detected
        return RoutingDecision(
            request_type=RequestType.DIRECT_AI_QUERY,
            should_use_orchestrator=False,
            confidence=0.3,
            reasoning="No clear framework execution pattern detected",
            fallback_action="direct_ai_response_with_framework_suggestion"
        )
    
    def _create_orchestrator_prompt(self, jira_id: str, environment: Optional[str], original_request: str) -> str:
        """Create orchestrator execution prompt"""
        base_prompt = f"""You are the main framework orchestrator for the claude-test-generator application. 

Execute the complete 6-phase framework for {jira_id}"""
        
        if environment:
            base_prompt += f" on {environment} environment"
        
        base_prompt += f""".

**ORIGINAL USER REQUEST**: {original_request}

**CRITICAL**: You must use the proper orchestrator execution pattern:

1. Import and execute: `from ai_agent_orchestrator import HybridAIAgentExecutor`
2. Execute: `await orchestrator.execute_full_framework("{jira_id}", "{environment or 'auto-detect'}")`
3. Generate proper run-metadata.json with complete execution statistics
4. Create deliverable files in runs/{jira_id}/{jira_id}-{{timestamp}}/

**Expected Output**: Complete orchestrator execution with:
- Phase 0: Framework initialization cleanup
- Phase 1: Parallel foundation analysis (Agent A + Agent D)
- Phase 2: Parallel deep investigation (Agent B + Agent C)  
- Phase 3: Enhanced AI cross-agent analysis
- Phase 4: Template-driven generation & validation
- Phase 5: Comprehensive temporary data cleanup

Execute the full framework orchestrator now and return the execution results."""
        
        return base_prompt
    
    def should_auto_route(self, routing_decision: RoutingDecision) -> bool:
        """
        Determine if request should be automatically routed to orchestrator
        """
        return (
            routing_decision.should_use_orchestrator and 
            routing_decision.confidence >= 0.7 and
            routing_decision.task_tool_config is not None
        )
    
    def get_routing_explanation(self, routing_decision: RoutingDecision) -> str:
        """
        Generate explanation of routing decision
        """
        explanation = f"**Request Classification**: {routing_decision.request_type.value}\n"
        explanation += f"**Should Use Orchestrator**: {routing_decision.should_use_orchestrator}\n"
        explanation += f"**Confidence**: {routing_decision.confidence:.1%}\n"
        explanation += f"**Reasoning**: {routing_decision.reasoning}\n"
        
        if routing_decision.should_use_orchestrator:
            explanation += f"**Action**: Routing to Task tool with orchestrator agent\n"
        else:
            explanation += f"**Action**: {routing_decision.fallback_action}\n"
        
        return explanation

# Convenience function for immediate use
def route_user_request(user_request: str) -> RoutingDecision:
    """Route user request and return routing decision"""
    router = RequestRoutingService()
    return router.classify_request(user_request)

if __name__ == "__main__":
    # Test the routing service
    test_requests = [
        "Generate test plan for ACM-22079",
        "Generate comprehensive test cases for ACM-22079 on mist10",
        "What does this code do?", 
        "Investigate why phase 0 failed",
        "Analyze ACM-12345 using staging environment"
    ]
    
    router = RequestRoutingService()
    print("🧠 REQUEST ROUTING SERVICE TEST")
    print("=" * 50)
    
    for request in test_requests:
        print(f"\n**Request**: {request}")
        decision = router.classify_request(request)
        print(router.get_routing_explanation(decision))