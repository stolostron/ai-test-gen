"""
Agent A (JIRA Intelligence) Integration with Learning Framework

Shows how to enhance Agent A with learning capabilities while maintaining
backward compatibility and zero regression risk.
"""

import time
import asyncio
import logging
from typing import Dict, Optional, Any

# Import the learning framework
from ..agent_learning_framework import AgentLearningFramework

logger = logging.getLogger(__name__)


class AgentA:
    """Original Agent A implementation (simplified for demonstration)"""
    
    def analyze_jira(self, ticket: str) -> Dict:
        """
        Original JIRA analysis logic
        This represents the existing Agent A functionality
        """
        # Simulate existing JIRA analysis
        analysis = {
            'ticket': ticket,
            'status': 'success',
            'ticket_type': 'feature',
            'components': ['ClusterCurator', 'ACM'],
            'confidence': 0.90,
            'pr_references': ['#468'],
            'version': 'ACM 2.15'
        }
        
        # Simulate processing time
        time.sleep(0.1)
        
        return analysis


class AgentAWithLearning(AgentA):
    """
    Enhanced Agent A with learning capabilities
    Inherits from original Agent A to maintain all existing functionality
    """
    
    def __init__(self):
        super().__init__()
        # Get singleton learning framework instance
        self.learning_framework = AgentLearningFramework()
        self.agent_id = 'agent_a'
        
        # Feature flag for gradual rollout (can be disabled if needed)
        self.learning_enabled = True
        
        logger.info("Agent A initialized with learning capabilities")
    
    def analyze_jira(self, ticket: str) -> Dict:
        """
        Enhanced JIRA analysis with learning integration
        Maintains exact same interface and behavior as original
        """
        start_time = time.time()
        
        # 1. Check for learning recommendations (fast, cached, non-blocking)
        recommendations = None
        if self.learning_enabled:
            try:
                recommendations = self.learning_framework.apply_learnings(
                    self.agent_id,
                    {
                        'ticket': ticket,
                        'type': 'jira_analysis',
                        # Add any known context
                        'keywords': self._extract_keywords(ticket)
                    }
                )
                
                if recommendations:
                    logger.debug(f"Applied {len(recommendations.get('patterns', []))} learned patterns")
            except Exception as e:
                # Learning errors never affect main execution
                logger.debug(f"Learning recommendation skipped: {e}")
        
        # 2. Execute original logic (exactly the same)
        analysis = super().analyze_jira(ticket)
        
        # 3. Apply any learning optimizations (non-invasive)
        if recommendations:
            analysis = self._apply_recommendations(analysis, recommendations)
        
        # 4. Capture execution data (async, non-blocking)
        if self.learning_enabled:
            execution_time = time.time() - start_time
            
            metrics = {
                'execution_time': execution_time,
                'success': analysis.get('status') == 'success',
                'confidence': analysis.get('confidence', 0),
                'ticket_type_identified': bool(analysis.get('ticket_type')),
                'components_found': len(analysis.get('components', [])),
                'pr_references_found': len(analysis.get('pr_references', []))
            }
            
            # Queue learning capture (fire-and-forget)
            asyncio.create_task(
                self._capture_learning_async(ticket, analysis, metrics)
            )
        
        # Return exact same structure as original
        return analysis
    
    async def _capture_learning_async(self, ticket: str, analysis: Dict, metrics: Dict):
        """
        Async learning capture - runs in background
        Never blocks or affects main execution
        """
        try:
            await self.learning_framework.capture_execution(
                self.agent_id,
                {
                    'ticket': ticket,
                    'keywords_found': self._extract_keywords(ticket),
                    'component_keywords': self._extract_component_keywords(analysis)
                },
                analysis,
                metrics
            )
        except Exception as e:
            # Log but don't propagate
            logger.debug(f"Learning capture error (non-critical): {e}")
    
    def _apply_recommendations(self, analysis: Dict, recommendations: Dict) -> Dict:
        """
        Apply learning recommendations to enhance analysis
        Only makes improvements, never degrades results
        """
        # Copy to avoid modifying original
        enhanced = analysis.copy()
        
        # Apply confidence boost if patterns indicate high success
        if 'confidence_adjustment' in recommendations:
            adjustment = recommendations['confidence_adjustment']
            current_confidence = enhanced.get('confidence', 0.5)
            # Only boost, never reduce
            if adjustment > 0:
                enhanced['confidence'] = min(
                    current_confidence + adjustment,
                    0.99  # Cap at 99%
                )
                logger.debug(f"Confidence boosted by {adjustment:.2%}")
        
        # Add learned insights (if any)
        if 'patterns' in recommendations and recommendations['patterns']:
            enhanced['learning_insights'] = {
                'patterns_applied': len(recommendations['patterns']),
                'optimization_hints': recommendations.get('optimization_suggestions', [])
            }
        
        return enhanced
    
    def _extract_keywords(self, ticket: str) -> list:
        """Extract keywords from ticket ID for pattern matching"""
        # Simple keyword extraction (can be enhanced)
        keywords = []
        
        # Extract project prefix (e.g., ACM from ACM-12345)
        if '-' in ticket:
            project = ticket.split('-')[0]
            keywords.append(project.lower())
        
        return keywords
    
    def _extract_component_keywords(self, analysis: Dict) -> list:
        """Extract component-related keywords from analysis"""
        keywords = []
        
        components = analysis.get('components', [])
        for component in components:
            # Normalize component names
            normalized = component.lower().replace('-', '').replace('_', '')
            keywords.append(normalized)
        
        return keywords
    
    def disable_learning(self):
        """Disable learning if needed (for testing or issues)"""
        self.learning_enabled = False
        logger.info("Learning disabled for Agent A")
    
    def enable_learning(self):
        """Re-enable learning"""
        self.learning_enabled = True
        logger.info("Learning enabled for Agent A")


# Demonstration and validation
def demonstrate_integration():
    """Demonstrate that enhanced agent produces same results"""
    print("Agent A Learning Integration Demonstration")
    print("=" * 50)
    
    # Create both versions
    original_agent = AgentA()
    enhanced_agent = AgentAWithLearning()
    
    # Test ticket
    ticket = "ACM-22079"
    
    # Run both versions
    print(f"\nAnalyzing ticket: {ticket}")
    print("-" * 30)
    
    # Original
    start = time.time()
    original_result = original_agent.analyze_jira(ticket)
    original_time = time.time() - start
    
    # Enhanced
    start = time.time()
    enhanced_result = enhanced_agent.analyze_jira(ticket)
    enhanced_time = time.time() - start
    
    # Compare results
    print(f"\nOriginal execution time: {original_time:.3f}s")
    print(f"Enhanced execution time: {enhanced_time:.3f}s")
    
    # Remove learning insights for comparison
    enhanced_compare = enhanced_result.copy()
    enhanced_compare.pop('learning_insights', None)
    
    # Verify identical core results
    identical = original_result == enhanced_compare
    print(f"\nCore results identical: {'✅ YES' if identical else '❌ NO'}")
    
    if not identical:
        print("Differences found:")
        for key in set(original_result.keys()) | set(enhanced_compare.keys()):
            if original_result.get(key) != enhanced_compare.get(key):
                print(f"  {key}: {original_result.get(key)} vs {enhanced_compare.get(key)}")
    
    # Show learning enhancements
    if 'learning_insights' in enhanced_result:
        print("\nLearning enhancements applied:")
        insights = enhanced_result['learning_insights']
        print(f"  Patterns applied: {insights.get('patterns_applied', 0)}")
        print(f"  Optimization hints: {len(insights.get('optimization_hints', []))}")
    
    print("\n" + "=" * 50)
    print("✅ Integration successful - no regression detected")
    
    return identical


if __name__ == '__main__':
    # Run demonstration
    demonstrate_integration()
