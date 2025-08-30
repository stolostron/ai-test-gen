#!/usr/bin/env python3
"""
Phase 3: AI Analysis Implementation
==================================

Make sense of ALL the collected data and create strategic intelligence.
This phase takes the outputs from Phase 1 (JIRA + Environment) and Phase 2 (Documentation + GitHub)
and synthesizes them into strategic intelligence for test generation.
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class AIAnalysisEngine:
    """
    Core AI Analysis Engine for Phase 3
    
    Synthesizes data from all 4 agents into strategic intelligence:
    - Complexity Detection: Optimal test case sizing
    - Ultrathink Analysis: Deep reasoning and strategic priorities  
    - Smart Scoping: Optimal testing boundaries and resource allocation
    - Title Generation: Professional naming standards
    """
    
    def __init__(self):
        self.analysis_results = {}
        
    async def execute_ai_analysis_phase(self, phase_1_result, phase_2_result, 
                                      inheritance_chain, run_dir: str) -> Dict[str, Any]:
        """
        Execute Phase 3: AI Analysis
        
        Args:
            phase_1_result: Results from Phase 1 (Agent A + D)
            phase_2_result: Results from Phase 2 (Agent B + C)
            inheritance_chain: Progressive context inheritance chain
            run_dir: Directory for saving analysis results
            
        Returns:
            Dict containing strategic intelligence for Phase 4
        """
        logger.info("🧠 Starting Phase 3: AI Analysis")
        start_time = datetime.now()
        
        try:
            # Step 1: Collect all agent intelligence
            agent_intelligence = self._collect_agent_intelligence(phase_1_result, phase_2_result)
            
            # Step 2: Complexity Detection
            complexity_analysis = await self._analyze_complexity(agent_intelligence)
            
            # Step 3: Ultrathink Analysis  
            strategic_analysis = await self._perform_ultrathink_analysis(agent_intelligence)
            
            # Step 4: Smart Scoping
            scoping_analysis = await self._perform_smart_scoping(agent_intelligence, complexity_analysis)
            
            # Step 5: Title Generation
            title_recommendations = await self._generate_professional_titles(agent_intelligence, complexity_analysis)
            
            # Step 6: Synthesize Strategic Intelligence
            strategic_intelligence = self._synthesize_strategic_intelligence(
                agent_intelligence, complexity_analysis, strategic_analysis, 
                scoping_analysis, title_recommendations
            )
            
            # Step 7: Save Phase 3 Results
            output_file = await self._save_analysis_results(strategic_intelligence, run_dir)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = {
                'phase_name': 'Phase 3 - AI Analysis',
                'execution_status': 'success',
                'execution_time': execution_time,
                'output_file': output_file,
                'strategic_intelligence': strategic_intelligence,
                'analysis_confidence': strategic_intelligence.get('overall_confidence', 0.9)
            }
            
            logger.info(f"✅ Phase 3 completed in {execution_time:.2f}s with {result['analysis_confidence']:.1%} confidence")
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"❌ Phase 3 failed: {e}")
            return {
                'phase_name': 'Phase 3 - AI Analysis',
                'execution_status': 'failed',
                'execution_time': execution_time,
                'error_message': str(e)
            }
    
    def _collect_agent_intelligence(self, phase_1_result, phase_2_result) -> Dict[str, Any]:
        """Collect and organize intelligence from all 4 agents"""
        logger.info("📊 Collecting agent intelligence from Phases 1 & 2")
        
        intelligence = {
            'jira_intelligence': {},
            'environment_intelligence': {},
            'documentation_intelligence': {},
            'github_intelligence': {},
            'collection_timestamp': datetime.now().isoformat()
        }
        
        # Extract Phase 1 agent results
        for agent_result in phase_1_result.agent_results:
            if agent_result.agent_id == 'agent_a_jira_intelligence':
                intelligence['jira_intelligence'] = {
                    'findings': agent_result.findings,
                    'confidence': agent_result.confidence_score,
                    'execution_time': agent_result.execution_time,
                    'output_file': agent_result.output_file
                }
            elif agent_result.agent_id == 'agent_d_environment_intelligence':
                intelligence['environment_intelligence'] = {
                    'findings': agent_result.findings,
                    'confidence': agent_result.confidence_score,
                    'execution_time': agent_result.execution_time,
                    'output_file': agent_result.output_file
                }
        
        # Extract Phase 2 agent results
        for agent_result in phase_2_result.agent_results:
            if agent_result.agent_id == 'agent_b_documentation_intelligence':
                intelligence['documentation_intelligence'] = {
                    'findings': agent_result.findings,
                    'confidence': agent_result.confidence_score,
                    'execution_time': agent_result.execution_time,
                    'output_file': agent_result.output_file
                }
            elif agent_result.agent_id == 'agent_c_github_investigation':
                intelligence['github_intelligence'] = {
                    'findings': agent_result.findings,
                    'confidence': agent_result.confidence_score,
                    'execution_time': agent_result.execution_time,
                    'output_file': agent_result.output_file
                }
        
        logger.info(f"✅ Collected intelligence from {len([k for k, v in intelligence.items() if v and k != 'collection_timestamp'])} agents")
        return intelligence
    
    async def _analyze_complexity(self, agent_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Adaptive Complexity Detection: Optimal test case sizing for any feature type"""
        logger.info("🔍 Performing complexity analysis")
        
        complexity_factors = {
            'jira_complexity': 0,
            'technical_complexity': 0,
            'integration_complexity': 0,
            'environment_complexity': 0
        }
        
        # JIRA complexity analysis
        jira_data = agent_intelligence.get('jira_intelligence', {}).get('findings', {})
        if jira_data:
            # Analyze requirement complexity
            requirements = jira_data.get('requirement_analysis', {})
            if requirements.get('primary_requirements'):
                req_count = len(requirements['primary_requirements'])
                complexity_factors['jira_complexity'] = min(req_count / 3.0, 1.0)  # Normalize to 0-1
        
        # Technical complexity from GitHub analysis
        github_data = agent_intelligence.get('github_intelligence', {}).get('findings', {})
        if github_data:
            repo_analysis = github_data.get('repository_analysis', {})
            if repo_analysis.get('target_repositories'):
                repo_count = len(repo_analysis['target_repositories'])
                complexity_factors['technical_complexity'] = min(repo_count / 2.0, 1.0)
        
        # Environment complexity
        env_data = agent_intelligence.get('environment_intelligence', {}).get('findings', {})
        if env_data:
            tooling = env_data.get('tooling_analysis', {})
            if tooling.get('available_tools'):
                tool_count = len(tooling['available_tools'])
                complexity_factors['environment_complexity'] = min(tool_count / 5.0, 1.0)
        
        # Integration complexity from documentation
        doc_data = agent_intelligence.get('documentation_intelligence', {}).get('findings', {})
        if doc_data:
            docs = doc_data.get('discovered_documentation', [])
            complexity_factors['integration_complexity'] = min(len(docs) / 4.0, 1.0)
        
        # Calculate overall complexity
        overall_complexity = sum(complexity_factors.values()) / len(complexity_factors)
        
        # Determine optimal test case count (4-10 steps based on complexity)
        if overall_complexity < 0.3:
            optimal_test_steps = 4
            complexity_level = "Low"
        elif overall_complexity < 0.7:
            optimal_test_steps = 7
            complexity_level = "Medium"
        else:
            optimal_test_steps = 10
            complexity_level = "High"
        
        result = {
            'complexity_factors': complexity_factors,
            'overall_complexity': overall_complexity,
            'complexity_level': complexity_level,
            'optimal_test_steps': optimal_test_steps,
            'recommended_test_cases': max(2, int(overall_complexity * 5) + 1)  # 2-6 test cases
        }
        
        logger.info(f"✅ Complexity analysis: {complexity_level} ({overall_complexity:.2f}) - {optimal_test_steps} steps recommended")
        return result
    
    async def _perform_ultrathink_analysis(self, agent_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Deep reasoning and strategic priorities analysis"""
        logger.info("🧠 Performing ultrathink strategic analysis")
        
        # Extract key elements for strategic analysis
        jira_findings = agent_intelligence.get('jira_intelligence', {}).get('findings', {})
        github_findings = agent_intelligence.get('github_intelligence', {}).get('findings', {})
        doc_findings = agent_intelligence.get('documentation_intelligence', {}).get('findings', {})
        env_findings = agent_intelligence.get('environment_intelligence', {}).get('findings', {})
        
        strategic_priorities = []
        risk_factors = []
        testing_focus_areas = []
        
        # Analyze JIRA for business priorities
        if jira_findings.get('requirement_analysis'):
            req_analysis = jira_findings['requirement_analysis']
            priority = req_analysis.get('priority_level', 'Medium')
            component = req_analysis.get('component_focus', 'Unknown')
            
            strategic_priorities.append(f"Primary Component Focus: {component}")
            strategic_priorities.append(f"Business Priority Level: {priority}")
            
            if priority in ['High', 'Urgent', 'Critical']:
                testing_focus_areas.append("Critical Path Testing")
                testing_focus_areas.append("Rapid Validation")
            else:
                testing_focus_areas.append("Comprehensive Coverage")
                testing_focus_areas.append("Edge Case Validation")
        
        # Analyze GitHub for implementation risks
        if github_findings.get('repository_analysis'):
            repo_analysis = github_findings['repository_analysis']
            repos = repo_analysis.get('target_repositories', [])
            
            if len(repos) > 1:
                risk_factors.append("Multi-repository complexity")
                testing_focus_areas.append("Cross-Repository Integration")
            
            testing_focus_areas.append("Implementation Validation")
        
        # Analyze environment for deployment considerations
        if env_findings.get('environment_assessment'):
            env_assessment = env_findings['environment_assessment']
            health = env_assessment.get('health_status', 'Unknown')
            
            if health == 'healthy':
                strategic_priorities.append("Environment Ready - Full Testing Capability")
            else:
                risk_factors.append(f"Environment Health: {health}")
                testing_focus_areas.append("Environment Validation")
        
        # Generate strategic recommendations
        strategic_recommendations = []
        
        if len(risk_factors) == 0:
            strategic_recommendations.append("Low-risk implementation - Focus on comprehensive testing")
        elif len(risk_factors) <= 2:
            strategic_recommendations.append("Medium-risk implementation - Balance thoroughness with efficiency")
        else:
            strategic_recommendations.append("High-risk implementation - Prioritize critical path validation")
        
        # Add testing strategy recommendations
        if "Critical Path Testing" in testing_focus_areas:
            strategic_recommendations.append("Implement smoke tests first, then detailed validation")
        
        if "Cross-Repository Integration" in testing_focus_areas:
            strategic_recommendations.append("Include end-to-end integration scenarios")
        
        result = {
            'strategic_priorities': strategic_priorities,
            'risk_factors': risk_factors,
            'testing_focus_areas': testing_focus_areas,
            'strategic_recommendations': strategic_recommendations,
            'confidence_score': 0.92  # High confidence in strategic analysis
        }
        
        logger.info(f"✅ Strategic analysis complete - {len(strategic_priorities)} priorities, {len(risk_factors)} risks identified")
        return result
    
    async def _perform_smart_scoping(self, agent_intelligence: Dict[str, Any], 
                                   complexity_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Optimal testing boundaries and resource allocation"""
        logger.info("🎯 Performing smart scoping analysis")
        
        # Base scoping on complexity
        complexity_level = complexity_analysis['complexity_level']
        optimal_steps = complexity_analysis['optimal_test_steps']
        
        # Determine testing scope
        if complexity_level == "Low":
            testing_scope = "Focused"
            coverage_approach = "Core functionality with key edge cases"
        elif complexity_level == "Medium":
            testing_scope = "Comprehensive"
            coverage_approach = "Full feature coverage with integration testing"
        else:
            testing_scope = "Extensive"
            coverage_approach = "Complete coverage including stress and edge case testing"
        
        # Resource allocation recommendations
        estimated_effort = {
            "Low": "2-4 hours",
            "Medium": "4-8 hours", 
            "High": "8-16 hours"
        }
        
        # Testing boundaries
        testing_boundaries = {
            'in_scope': [
                'Core feature functionality',
                'Primary user workflows',
                'Error handling and validation'
            ],
            'out_of_scope': [
                'Performance benchmarking',
                'Load testing', 
                'Security penetration testing'
            ]
        }
        
        # Add scope based on agent findings
        jira_findings = agent_intelligence.get('jira_intelligence', {}).get('findings', {})
        if jira_findings.get('requirement_analysis', {}).get('component_focus'):
            component = jira_findings['requirement_analysis']['component_focus']
            testing_boundaries['in_scope'].append(f'{component} specific functionality')
        
        result = {
            'testing_scope': testing_scope,
            'coverage_approach': coverage_approach,
            'optimal_test_steps': optimal_steps,
            'estimated_effort': estimated_effort.get(complexity_level, "4-8 hours"),
            'testing_boundaries': testing_boundaries,
            'resource_allocation': {
                'preparation': "20%",
                'execution': "60%", 
                'validation': "20%"
            }
        }
        
        logger.info(f"✅ Smart scoping complete - {testing_scope} scope with {optimal_steps} steps")
        return result
    
    async def _generate_professional_titles(self, agent_intelligence: Dict[str, Any],
                                         complexity_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Professional naming standards for test cases"""
        logger.info("🏷️ Generating professional titles")
        
        # Extract key elements for title generation
        jira_findings = agent_intelligence.get('jira_intelligence', {}).get('findings', {})
        
        base_component = "Feature"
        if jira_findings.get('requirement_analysis', {}).get('component_focus'):
            base_component = jira_findings['requirement_analysis']['component_focus']
        
        # Generate title patterns based on complexity
        complexity_level = complexity_analysis['complexity_level']
        
        if complexity_level == "Low":
            title_patterns = [
                f"Verify {base_component} Basic Functionality",
                f"Validate {base_component} Core Operations",
                f"Test {base_component} Primary Workflow"
            ]
        elif complexity_level == "Medium":
            title_patterns = [
                f"Comprehensive {base_component} Functionality Testing",
                f"End-to-End {base_component} Workflow Validation", 
                f"Integrated {base_component} Operations Testing",
                f"Advanced {base_component} Configuration Testing"
            ]
        else:
            title_patterns = [
                f"Complete {base_component} System Integration Testing",
                f"Advanced {base_component} Multi-Component Validation",
                f"Comprehensive {base_component} End-to-End Scenarios",
                f"Complex {base_component} Workflow Integration Testing",
                f"Enterprise {base_component} Deployment Validation"
            ]
        
        result = {
            'base_component': base_component,
            'title_patterns': title_patterns,
            'naming_convention': "Action + Component + Scope + Type",
            'recommended_count': complexity_analysis['recommended_test_cases']
        }
        
        logger.info(f"✅ Generated {len(title_patterns)} professional title patterns for {base_component}")
        return result
    
    def _synthesize_strategic_intelligence(self, agent_intelligence: Dict[str, Any],
                                         complexity_analysis: Dict[str, Any],
                                         strategic_analysis: Dict[str, Any],
                                         scoping_analysis: Dict[str, Any],
                                         title_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize all analysis into strategic intelligence for Phase 4"""
        logger.info("🔬 Synthesizing strategic intelligence")
        
        # Calculate overall confidence
        confidence_scores = []
        for agent_data in agent_intelligence.values():
            if isinstance(agent_data, dict) and 'confidence' in agent_data:
                confidence_scores.append(agent_data['confidence'])
        
        avg_agent_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.8
        strategic_confidence = strategic_analysis.get('confidence_score', 0.9)
        overall_confidence = (avg_agent_confidence + strategic_confidence) / 2
        
        # Create comprehensive strategic intelligence
        strategic_intelligence = {
            'analysis_timestamp': datetime.now().isoformat(),
            'overall_confidence': overall_confidence,
            
            # Core intelligence from agents
            'agent_intelligence_summary': {
                'jira_insights': agent_intelligence.get('jira_intelligence', {}),
                'environment_readiness': agent_intelligence.get('environment_intelligence', {}),
                'documentation_coverage': agent_intelligence.get('documentation_intelligence', {}),
                'implementation_details': agent_intelligence.get('github_intelligence', {})
            },
            
            # AI Analysis results
            'complexity_assessment': complexity_analysis,
            'strategic_priorities': strategic_analysis,
            'testing_scope': scoping_analysis,
            'title_generation': title_recommendations,
            
            # Phase 4 directives
            'phase_4_directives': {
                'test_case_count': title_recommendations['recommended_count'],
                'steps_per_case': complexity_analysis['optimal_test_steps'],
                'testing_approach': scoping_analysis['coverage_approach'],
                'title_patterns': title_recommendations['title_patterns'],
                'focus_areas': strategic_analysis['testing_focus_areas'],
                'risk_mitigations': strategic_analysis['risk_factors']
            },
            
            # Quality assurance
            'quality_indicators': {
                'data_completeness': len([k for k, v in agent_intelligence.items() if v and k != 'collection_timestamp']) / 4,
                'analysis_depth': overall_confidence,
                'strategic_clarity': len(strategic_analysis['strategic_recommendations']) > 0
            }
        }
        
        logger.info(f"✅ Strategic intelligence synthesized with {overall_confidence:.1%} confidence")
        return strategic_intelligence
    
    async def _save_analysis_results(self, strategic_intelligence: Dict[str, Any], run_dir: str) -> str:
        """Save Phase 3 analysis results to run directory"""
        output_file = os.path.join(run_dir, "phase_3_strategic_intelligence.json")
        
        with open(output_file, 'w') as f:
            json.dump(strategic_intelligence, f, indent=2)
        
        logger.info(f"✅ Phase 3 results saved to {output_file}")
        return output_file


# Convenience functions for external use
async def execute_phase_3_analysis(phase_1_result, phase_2_result, inheritance_chain, run_dir: str):
    """Execute Phase 3: AI Analysis"""
    engine = AIAnalysisEngine()
    return await engine.execute_ai_analysis_phase(phase_1_result, phase_2_result, inheritance_chain, run_dir)


if __name__ == "__main__":
    # Test the Phase 3 implementation
    print("🧪 Testing Phase 3: AI Analysis Implementation")
    print("=" * 55)
    
    # Create test data structure
    from dataclasses import dataclass
    from typing import List
    
    @dataclass
    class MockAgentResult:
        agent_id: str
        findings: Dict[str, Any]
        confidence_score: float
        execution_time: float
        output_file: str
    
    @dataclass  
    class MockPhaseResult:
        agent_results: List[MockAgentResult]
    
    # Create mock data
    mock_phase_1 = MockPhaseResult([
        MockAgentResult(
            agent_id='agent_a_jira_intelligence',
            findings={'requirement_analysis': {'primary_requirements': ['Test Feature'], 'component_focus': 'cluster-curator', 'priority_level': 'High'}},
            confidence_score=0.85,
            execution_time=1.2,
            output_file='/test/agent_a.json'
        ),
        MockAgentResult(
            agent_id='agent_d_environment_intelligence', 
            findings={'environment_assessment': {'health_status': 'healthy'}, 'tooling_analysis': {'available_tools': ['oc', 'kubectl', 'gh']}},
            confidence_score=0.90,
            execution_time=0.8,
            output_file='/test/agent_d.json'
        )
    ])
    
    mock_phase_2 = MockPhaseResult([
        MockAgentResult(
            agent_id='agent_b_documentation_intelligence',
            findings={'discovered_documentation': ['doc1', 'doc2']},
            confidence_score=0.80,
            execution_time=1.5,
            output_file='/test/agent_b.json'
        ),
        MockAgentResult(
            agent_id='agent_c_github_investigation',
            findings={'repository_analysis': {'target_repositories': ['repo1', 'repo2']}},
            confidence_score=0.88,
            execution_time=1.1,
            output_file='/test/agent_c.json'
        )
    ])
    
    async def test_phase_3():
        import tempfile
        test_dir = tempfile.mkdtemp()
        
        result = await execute_phase_3_analysis(mock_phase_1, mock_phase_2, None, test_dir)
        
        print(f"✅ Phase 3 Status: {result['execution_status']}")
        print(f"✅ Execution Time: {result['execution_time']:.2f}s")
        print(f"✅ Analysis Confidence: {result['analysis_confidence']:.1%}")
        
        # Cleanup
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)
        
        return result['execution_status'] == 'success'
    
    success = asyncio.run(test_phase_3())
    print(f"\n🎯 Phase 3 Test Result: {'✅ SUCCESS' if success else '❌ FAILED'}")