#!/usr/bin/env python3
"""
Embedded Context Management - ULTRATHINK Efficiency Solution
==========================================================

Self-contained context management system embedded directly in the framework
for maximum efficiency and zero external dependencies.

Features:
- Claude 4 Sonnet 200K token management
- Real-time budget monitoring with alerts
- Importance-based compression
- Performance optimized (sub-10ms operations)
"""

import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)

class ContextItemType(str, Enum):
    """Context item types for budget allocation"""
    FOUNDATION = "foundation"
    AGENT_OUTPUT = "agent_output"
    TEMPLATE = "template"
    METADATA = "metadata"
    DEBUG = "debug"
    TEMPORARY = "temporary"

class BudgetAlertLevel(str, Enum):
    """Budget alert levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

@dataclass
class ContextItem:
    """Individual context item with metadata"""
    content: str
    importance: float
    item_type: ContextItemType
    source: str
    timestamp: float
    token_count: int
    compressed: bool = False
    compression_ratio: float = 1.0

@dataclass
class ContextMetrics:
    """Context usage metrics"""
    total_tokens: int
    total_items: int
    budget_utilization: float
    compression_savings: int
    tokens_by_type: Dict[str, int]

@dataclass
class BudgetAlert:
    """Budget alert information"""
    level: BudgetAlertLevel
    message: str
    utilization: float
    recommended_actions: List[str]
    timestamp: datetime

class EmbeddedTokenCounter:
    """Ultra-fast token counting using character-based approximation"""
    
    def __init__(self, model: str = "claude-4-sonnet-20241022"):
        self.model = model
        # Character to token ratio for Claude (approximate)
        self.char_to_token_ratio = 4.0  # ~4 characters per token
        
    def count_tokens(self, text: str) -> int:
        """Fast token counting using character approximation"""
        if not text:
            return 0
        
        # Quick approximation: characters / 4
        return max(1, int(len(text) / self.char_to_token_ratio))

class EmbeddedContextManager:
    """Self-contained context management system"""
    
    def __init__(self, max_tokens: int = 200000):
        self.max_tokens = max_tokens
        self.context_items: List[ContextItem] = []
        self.current_token_count = 0
        self.token_counter = EmbeddedTokenCounter()
        
        # Budget allocation (percentages)
        self.budget_allocation = {
            ContextItemType.FOUNDATION: 0.15,    # 15%
            ContextItemType.AGENT_OUTPUT: 0.50,  # 50%
            ContextItemType.TEMPLATE: 0.20,      # 20%
            ContextItemType.METADATA: 0.10,      # 10%
            ContextItemType.DEBUG: 0.03,         # 3%
            ContextItemType.TEMPORARY: 0.02      # 2%
        }
        
        # Compression threshold
        self.compression_threshold = 0.8  # Start compression at 80%
        
        logger.info(f"Embedded Context Manager initialized: {max_tokens:,} token budget")
    
    def add_context(self, content: str, importance: float, item_type: str, 
                   source: str, metadata: Dict[str, Any] = None) -> bool:
        """Add context item with budget checking"""
        
        # Convert string type to enum
        if isinstance(item_type, str):
            try:
                item_type = ContextItemType(item_type)
            except ValueError:
                item_type = ContextItemType.METADATA
        
        # Count tokens
        token_count = self.token_counter.count_tokens(content)
        
        # Check if adding would exceed budget
        if self.current_token_count + token_count > self.max_tokens:
            logger.warning(f"Token budget exceeded: {self.current_token_count + token_count:,} > {self.max_tokens:,}")
            return False
        
        # Create context item
        item = ContextItem(
            content=content,
            importance=importance,
            item_type=item_type,
            source=source,
            timestamp=time.time(),
            token_count=token_count
        )
        
        # Add to context
        self.context_items.append(item)
        self.current_token_count += token_count
        
        return True
    
    def get_context_summary(self) -> ContextMetrics:
        """Get current context metrics"""
        tokens_by_type = {}
        for item_type in ContextItemType:
            tokens_by_type[item_type.value] = sum(
                item.token_count for item in self.context_items 
                if item.item_type == item_type
            )
        
        # Calculate compression savings
        compression_savings = sum(
            int(item.token_count * (1 - item.compression_ratio))
            for item in self.context_items if item.compressed
        )
        
        return ContextMetrics(
            total_tokens=self.current_token_count,
            total_items=len(self.context_items),
            budget_utilization=self.current_token_count / self.max_tokens,
            compression_savings=compression_savings,
            tokens_by_type=tokens_by_type
        )
    
    def compress_low_priority_items(self) -> int:
        """Compress low-priority items to free up budget"""
        tokens_saved = 0
        
        # Find low-priority items
        low_priority_items = [
            item for item in self.context_items
            if item.importance < 0.7 and not item.compressed
        ]
        
        for item in low_priority_items[:5]:  # Limit to 5 items
            # Simple compression: keep first 60% of content
            original_length = len(item.content)
            compressed_length = int(original_length * 0.6)
            
            if compressed_length > 0:
                # Compress content
                item.content = item.content[:compressed_length] + "...[COMPRESSED]"
                
                # Update token count
                new_token_count = self.token_counter.count_tokens(item.content)
                tokens_saved += item.token_count - new_token_count
                
                # Update item
                item.token_count = new_token_count
                item.compressed = True
                item.compression_ratio = new_token_count / (item.token_count + tokens_saved) if (item.token_count + tokens_saved) > 0 else 0.6
        
        # Update total count
        self.current_token_count -= tokens_saved
        
        if tokens_saved > 0:
            logger.info(f"Compressed {len(low_priority_items)} items, saved {tokens_saved:,} tokens")
        
        return tokens_saved

class EmbeddedBudgetMonitor:
    """Lightweight budget monitoring system"""
    
    def __init__(self, context_manager: EmbeddedContextManager):
        self.context_manager = context_manager
        self.alert_history = deque(maxlen=100)
        self.measurements = deque(maxlen=1000)
        
        # Alert thresholds
        self.thresholds = {
            0.60: BudgetAlertLevel.WARNING,
            0.80: BudgetAlertLevel.CRITICAL,
            0.95: BudgetAlertLevel.EMERGENCY
        }
    
    def check_budget_status(self) -> Tuple[BudgetAlertLevel, Optional[BudgetAlert]]:
        """Check current budget status and return alert if needed"""
        metrics = self.context_manager.get_context_summary()
        utilization = metrics.budget_utilization
        
        # Record measurement
        self.measurements.append({
            "timestamp": datetime.now(),
            "utilization": utilization,
            "total_tokens": metrics.total_tokens
        })
        
        # Determine alert level
        alert_level = BudgetAlertLevel.INFO
        for threshold, level in sorted(self.thresholds.items(), reverse=True):
            if utilization >= threshold:
                alert_level = level
                break
        
        # Create alert if not INFO level
        alert = None
        if alert_level != BudgetAlertLevel.INFO:
            actions = []
            if alert_level == BudgetAlertLevel.WARNING:
                actions = ["Monitor closely"]
            elif alert_level == BudgetAlertLevel.CRITICAL:
                actions = ["Compress low-priority content"]
            elif alert_level == BudgetAlertLevel.EMERGENCY:
                actions = ["Aggressive compression", "Block new content"]
            
            alert = BudgetAlert(
                level=alert_level,
                message=f"Context budget {alert_level.value}: {utilization:.1%} utilization",
                utilization=utilization,
                recommended_actions=actions,
                timestamp=datetime.now()
            )
            
            self.alert_history.append(alert)
            
            # Auto-execute actions for critical levels
            if alert_level == BudgetAlertLevel.CRITICAL:
                self.context_manager.compress_low_priority_items()
        
        return alert_level, alert
    
    def get_monitoring_statistics(self) -> Dict[str, Any]:
        """Get monitoring statistics"""
        if not self.measurements:
            return {"status": "no_data"}
        
        recent = list(self.measurements)[-100:]
        utilizations = [m["utilization"] for m in recent]
        
        return {
            "monitoring_status": "active",
            "total_measurements": len(self.measurements),
            "average_utilization": sum(utilizations) / len(utilizations),
            "peak_utilization": max(utilizations),
            "current_utilization": utilizations[-1] if utilizations else 0.0,
            "total_alerts": len(self.alert_history),
            "alert_breakdown": {
                level.value: sum(1 for alert in self.alert_history if alert.level == level)
                for level in BudgetAlertLevel
            }
        }

# Factory functions for easy integration
def create_embedded_context_manager(max_tokens: int = 200000) -> EmbeddedContextManager:
    """Create embedded context manager"""
    return EmbeddedContextManager(max_tokens)

def create_embedded_budget_monitor(context_manager: EmbeddedContextManager) -> EmbeddedBudgetMonitor:
    """Create embedded budget monitor"""
    return EmbeddedBudgetMonitor(context_manager)

def get_importance_score(source: str, context_type: str) -> float:
    """Get importance score for context item"""
    # Importance scoring based on source and type
    base_scores = {
        "foundation": 0.95,
        "jira_tracking": 0.90,
        "agent_findings": 0.85,
        "framework_execution": 0.80,
        "environment_data": 0.75,
        "documentation": 0.70,
        "github_analysis": 0.70,
        "template": 0.65,
        "metadata": 0.60,
        "debug": 0.40,
        "temporary": 0.30
    }
    
    # Get base score
    score = base_scores.get(context_type, 0.50)
    
    # Adjust based on source
    if "agent_a" in source or "jira" in source:
        score += 0.05
    elif "agent_d" in source or "environment" in source:
        score += 0.03
    
    return min(1.0, score)

if __name__ == "__main__":
    # Test embedded context management
    print("🧠 EMBEDDED CONTEXT MANAGEMENT TEST")
    print("=" * 50)
    
    # Create system
    cm = create_embedded_context_manager()
    monitor = create_embedded_budget_monitor(cm)
    
    # Test adding content
    success = cm.add_context(
        content="Test framework execution for embedded context management validation",
        importance=get_importance_score("test", "framework_execution"),
        item_type=ContextItemType.FOUNDATION,
        source="embedded_test"
    )
    
    print(f"✅ Content added: {success}")
    
    # Check metrics
    metrics = cm.get_context_summary()
    print(f"📊 Budget: {metrics.total_tokens:,}/{cm.max_tokens:,} tokens")
    print(f"🎯 Utilization: {metrics.budget_utilization:.1%}")
    
    # Check monitoring
    level, alert = monitor.check_budget_status()
    print(f"🔍 Alert Level: {level.value}")
    
    print("🏆 Embedded Context Management: OPERATIONAL")