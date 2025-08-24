"""
Agent Learning Framework Package

Comprehensive learning infrastructure for continuous agent improvement
"""

from .agent_learning_framework import AgentLearningFramework
from .pattern_database import PatternDatabase
from .performance_tracker import PerformanceTracker, MetricType, PerformanceMetric
from .async_executor import AsyncExecutor, LearningEvent, EventPriority

# Version info
__version__ = "1.0.0"
__author__ = "AI Systems Suite"

# Export main classes
__all__ = [
    'AgentLearningFramework',
    'PatternDatabase',
    'PerformanceTracker',
    'AsyncExecutor',
    'LearningEvent',
    'EventPriority',
    'MetricType',
    'PerformanceMetric'
]

# Module level logger
import logging
logger = logging.getLogger(__name__)

# Initialize framework on import (singleton pattern)
_framework_instance = None

def get_learning_framework():
    """Get the singleton learning framework instance"""
    global _framework_instance
    if _framework_instance is None:
        _framework_instance = AgentLearningFramework()
    return _framework_instance

# Log initialization
logger.info(f"Agent Learning Framework v{__version__} loaded")
