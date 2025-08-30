#!/usr/bin/env python3
"""
Context Budget Monitor - Real-time Context Budget Tracking
=========================================================

Real-time monitoring and alerting system for context window budget management.
Provides early warnings, automatic triggers, and budget optimization recommendations.

Key Features:
- Real-time budget utilization tracking
- Early warning system for approaching limits
- Automatic compression triggers
- Budget allocation optimization
- Performance impact monitoring
"""

import os
import json
import logging
import time
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
import threading
from collections import deque

from context_manager import ContextManager, ContextItemType, ContextMetrics
from context_compressor import AdvancedContextCompressor, CompressionStrategy

logger = logging.getLogger(__name__)

class BudgetAlertLevel(str, Enum):
    """Budget alert severity levels"""
    INFO = "info"           # 0-60% utilization
    WARNING = "warning"     # 60-80% utilization
    CRITICAL = "critical"   # 80-95% utilization
    EMERGENCY = "emergency" # 95%+ utilization

class BudgetAction(str, Enum):
    """Actions that can be taken when budget limits are approached"""
    LOG_WARNING = "log_warning"
    COMPRESS_LOW_PRIORITY = "compress_low_priority"
    COMPRESS_AGGRESSIVE = "compress_aggressive"
    BLOCK_NEW_CONTENT = "block_new_content"
    EMERGENCY_CLEANUP = "emergency_cleanup"

@dataclass
class BudgetAlert:
    """Budget alert message"""
    level: BudgetAlertLevel
    message: str
    utilization: float
    tokens_used: int
    tokens_available: int
    recommended_actions: List[BudgetAction]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class BudgetThreshold:
    """Budget threshold configuration"""
    utilization_threshold: float    # 0.0 to 1.0
    alert_level: BudgetAlertLevel
    actions: List[BudgetAction]
    cooldown_seconds: int = 60     # Minimum time between same alerts

@dataclass
class BudgetOptimization:
    """Budget optimization recommendation"""
    current_allocation: Dict[str, int]
    recommended_allocation: Dict[str, int]
    expected_improvement: Dict[str, float]
    rationale: str

class BudgetMonitor:
    """
    Real-time context budget monitoring and management system
    """
    
    def __init__(self, 
                 context_manager: ContextManager,
                 monitoring_interval: float = 5.0,
                 enable_auto_actions: bool = True):
        """
        Initialize budget monitor
        
        Args:
            context_manager: Context manager instance to monitor
            monitoring_interval: Monitoring check interval in seconds
            enable_auto_actions: Whether to automatically execute budget actions
        """
        self.context_manager = context_manager
        self.monitoring_interval = monitoring_interval
        self.enable_auto_actions = enable_auto_actions
        
        # Monitoring state
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Alert system
        self.alert_handlers: List[Callable[[BudgetAlert], None]] = []
        self.recent_alerts = deque(maxlen=100)
        self.last_alert_times: Dict[BudgetAlertLevel, datetime] = {}
        
        # Budget thresholds
        self.thresholds = self._create_default_thresholds()
        
        # Metrics tracking
        self.metrics_history = deque(maxlen=1000)
        self.optimization_history = []
        
        # Compression system
        self.compressor = AdvancedContextCompressor()
        
        logger.info("Budget Monitor initialized")
    
    def _create_default_thresholds(self) -> List[BudgetThreshold]:
        """Create default budget threshold configuration"""
        return [
            BudgetThreshold(
                utilization_threshold=0.60,
                alert_level=BudgetAlertLevel.WARNING,
                actions=[BudgetAction.LOG_WARNING],
                cooldown_seconds=300
            ),
            BudgetThreshold(
                utilization_threshold=0.80,
                alert_level=BudgetAlertLevel.CRITICAL,
                actions=[BudgetAction.LOG_WARNING, BudgetAction.COMPRESS_LOW_PRIORITY],
                cooldown_seconds=120
            ),
            BudgetThreshold(
                utilization_threshold=0.95,
                alert_level=BudgetAlertLevel.EMERGENCY,
                actions=[
                    BudgetAction.LOG_WARNING,
                    BudgetAction.COMPRESS_AGGRESSIVE,
                    BudgetAction.BLOCK_NEW_CONTENT
                ],
                cooldown_seconds=60
            )
        ]
    
    def start_monitoring(self):
        """Start real-time budget monitoring"""
        if self.monitoring_active:
            logger.warning("Budget monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info(f"Budget monitoring started (interval: {self.monitoring_interval}s)")
    
    def stop_monitoring(self):
        """Stop real-time budget monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        
        logger.info("Budget monitoring stopped")
    
    def add_alert_handler(self, handler: Callable[[BudgetAlert], None]):
        """Add custom alert handler function"""
        self.alert_handlers.append(handler)
        logger.debug(f"Added alert handler: {handler.__name__}")
    
    def check_budget_status(self) -> Tuple[BudgetAlertLevel, Optional[BudgetAlert]]:
        """
        Check current budget status and return alert if needed
        
        Returns:
            Tuple of (alert_level, alert_object or None)
        """
        metrics = self.context_manager.get_context_summary()
        utilization = metrics.budget_utilization
        
        # Record metrics
        self.metrics_history.append({
            "timestamp": datetime.now(),
            "utilization": utilization,
            "total_tokens": metrics.total_tokens,
            "compression_savings": metrics.compression_savings,
            "items_count": metrics.total_items
        })
        
        # Determine alert level
        alert_level = BudgetAlertLevel.INFO
        triggered_threshold = None
        
        for threshold in sorted(self.thresholds, key=lambda x: x.utilization_threshold, reverse=True):
            if utilization >= threshold.utilization_threshold:
                alert_level = threshold.alert_level
                triggered_threshold = threshold
                break
        
        # Check if we should issue an alert
        if triggered_threshold and self._should_issue_alert(alert_level):
            alert = BudgetAlert(
                level=alert_level,
                message=self._generate_alert_message(metrics, triggered_threshold),
                utilization=utilization,
                tokens_used=metrics.total_tokens,
                tokens_available=self.context_manager.max_tokens - metrics.total_tokens,
                recommended_actions=triggered_threshold.actions
            )
            
            self.recent_alerts.append(alert)
            self.last_alert_times[alert_level] = datetime.now()
            
            # Execute alert actions
            if self.enable_auto_actions:
                self._execute_alert_actions(alert, triggered_threshold)
            
            # Notify handlers
            for handler in self.alert_handlers:
                try:
                    handler(alert)
                except Exception as e:
                    logger.error(f"Alert handler error: {e}")
            
            return alert_level, alert
        
        return alert_level, None
    
    def _should_issue_alert(self, alert_level: BudgetAlertLevel) -> bool:
        """Check if alert should be issued based on cooldown"""
        if alert_level not in self.last_alert_times:
            return True
        
        threshold = next(t for t in self.thresholds if t.alert_level == alert_level)
        last_alert = self.last_alert_times[alert_level]
        time_since_last = datetime.now() - last_alert
        
        return time_since_last.total_seconds() >= threshold.cooldown_seconds
    
    def _generate_alert_message(self, metrics: ContextMetrics, threshold: BudgetThreshold) -> str:
        """Generate human-readable alert message"""
        return (
            f"Context budget {threshold.alert_level.value.upper()}: "
            f"{metrics.budget_utilization:.1%} utilization "
            f"({metrics.total_tokens:,}/{self.context_manager.max_tokens:,} tokens). "
            f"Actions recommended: {', '.join(action.value for action in threshold.actions)}"
        )
    
    def _execute_alert_actions(self, alert: BudgetAlert, threshold: BudgetThreshold):
        """Execute automatic actions for budget alert"""
        for action in threshold.actions:
            try:
                if action == BudgetAction.LOG_WARNING:
                    logger.warning(alert.message)
                
                elif action == BudgetAction.COMPRESS_LOW_PRIORITY:
                    self._compress_low_priority_content()
                
                elif action == BudgetAction.COMPRESS_AGGRESSIVE:
                    self._compress_aggressive()
                
                elif action == BudgetAction.BLOCK_NEW_CONTENT:
                    self._enable_content_blocking()
                
                elif action == BudgetAction.EMERGENCY_CLEANUP:
                    self._emergency_cleanup()
                
            except Exception as e:
                logger.error(f"Failed to execute budget action {action.value}: {e}")
    
    def _compress_low_priority_content(self):
        """Compress low-priority context items"""
        logger.info("Executing low-priority compression")
        
        # Get compression recommendations for low-priority items
        low_priority_items = [
            item for item in self.context_manager.context_items
            if item.importance < 0.7 and not item.compressed
        ]
        
        if not low_priority_items:
            logger.info("No low-priority items to compress")
            return
        
        # Compress items
        tokens_saved = 0
        items_compressed = 0
        
        for item in low_priority_items[:5]:  # Limit to 5 items per action
            try:
                result = self.compressor.compress_context_item(item, target_ratio=0.6)
                
                if result.compressed_tokens < item.token_count:
                    # Update item in context manager
                    old_tokens = item.token_count
                    item.content = result.content_preserved
                    item.token_count = result.compressed_tokens
                    item.compressed = True
                    item.compression_ratio = result.compression_ratio
                    
                    # Update context manager token count
                    self.context_manager.current_token_count -= old_tokens - result.compressed_tokens
                    
                    tokens_saved += old_tokens - result.compressed_tokens
                    items_compressed += 1
                    
            except Exception as e:
                logger.error(f"Failed to compress item from {item.source}: {e}")
        
        logger.info(f"Low-priority compression complete: {items_compressed} items, {tokens_saved:,} tokens saved")
    
    def _compress_aggressive(self):
        """Aggressive compression of all compressible content"""
        logger.warning("Executing aggressive compression")
        
        # Get all compressible items
        compressible_items = [
            item for item in self.context_manager.context_items
            if item.importance < 0.9 and item.item_type != ContextItemType.FOUNDATION
        ]
        
        recommendations = self.compressor.get_compression_recommendations(
            compressible_items, target_reduction=0.3
        )
        
        tokens_saved = 0
        items_compressed = 0
        
        for item, strategy, ratio in recommendations:
            try:
                result = self.compressor.compress_context_item(item, target_ratio=ratio, strategy=strategy)
                
                if result.compressed_tokens < item.token_count:
                    # Update item
                    old_tokens = item.token_count
                    item.content = result.content_preserved
                    item.token_count = result.compressed_tokens
                    item.compressed = True
                    item.compression_ratio = result.compression_ratio
                    
                    # Update context manager
                    self.context_manager.current_token_count -= old_tokens - result.compressed_tokens
                    
                    tokens_saved += old_tokens - result.compressed_tokens
                    items_compressed += 1
                    
            except Exception as e:
                logger.error(f"Failed to aggressively compress item from {item.source}: {e}")
        
        logger.warning(f"Aggressive compression complete: {items_compressed} items, {tokens_saved:,} tokens saved")
    
    def _enable_content_blocking(self):
        """Enable blocking of new low-importance content"""
        logger.critical("Enabling content blocking for new low-importance content")
        # This would integrate with context manager to reject new content below certain importance
        # For now, just log the action
    
    def _emergency_cleanup(self):
        """Emergency cleanup of temporary and debug content"""
        logger.critical("Executing emergency cleanup")
        
        # Remove all temporary and debug items
        items_to_remove = [
            item for item in self.context_manager.context_items
            if item.item_type in [ContextItemType.TEMPORARY, ContextItemType.DEBUG]
        ]
        
        tokens_freed = 0
        for item in items_to_remove:
            self.context_manager.context_items.remove(item)
            self.context_manager.current_token_count -= item.token_count
            tokens_freed += item.token_count
        
        logger.critical(f"Emergency cleanup complete: {len(items_to_remove)} items removed, {tokens_freed:,} tokens freed")
    
    def _monitoring_loop(self):
        """Main monitoring loop (runs in separate thread)"""
        logger.debug("Budget monitoring loop started")
        
        while self.monitoring_active:
            try:
                alert_level, alert = self.check_budget_status()
                
                if alert:
                    logger.debug(f"Budget alert issued: {alert_level.value}")
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Budget monitoring error: {e}")
                time.sleep(self.monitoring_interval)
    
    def get_budget_optimization_recommendations(self) -> BudgetOptimization:
        """Get budget allocation optimization recommendations"""
        current_metrics = self.context_manager.get_context_summary()
        current_allocation = {}
        
        # Calculate current allocation by type
        for item_type in ContextItemType:
            current_allocation[item_type.value] = current_metrics.tokens_by_type.get(item_type, 0)
        
        # Analyze usage patterns
        total_tokens = sum(current_allocation.values())
        if total_tokens == 0:
            return BudgetOptimization(
                current_allocation=current_allocation,
                recommended_allocation=current_allocation,
                expected_improvement={},
                rationale="No content to analyze"
            )
        
        # Generate recommendations based on current usage
        recommended_allocation = current_allocation.copy()
        improvements = {}
        
        # Identify overused categories
        budget_percentages = {
            ContextItemType.FOUNDATION.value: 0.15,
            ContextItemType.AGENT_OUTPUT.value: 0.50,
            ContextItemType.TEMPLATE.value: 0.20,
            ContextItemType.METADATA.value: 0.10,
            ContextItemType.DEBUG.value: 0.03,
            ContextItemType.TEMPORARY.value: 0.02
        }
        
        rationale_parts = []
        
        for item_type, target_percentage in budget_percentages.items():
            current_percentage = current_allocation.get(item_type, 0) / total_tokens
            
            if current_percentage > target_percentage * 1.5:  # 50% over target
                reduction = current_allocation[item_type] * 0.3  # Reduce by 30%
                recommended_allocation[item_type] -= int(reduction)
                improvements[item_type] = -reduction
                rationale_parts.append(f"Reduce {item_type} usage by {reduction:,.0f} tokens")
            
            elif current_percentage < target_percentage * 0.5:  # 50% under target
                increase = (target_percentage * total_tokens - current_allocation[item_type]) * 0.5
                recommended_allocation[item_type] += int(increase)
                improvements[item_type] = increase
                rationale_parts.append(f"Increase {item_type} allocation by {increase:,.0f} tokens")
        
        rationale = "; ".join(rationale_parts) if rationale_parts else "Current allocation is well-balanced"
        
        return BudgetOptimization(
            current_allocation=current_allocation,
            recommended_allocation=recommended_allocation,
            expected_improvement=improvements,
            rationale=rationale
        )
    
    def get_monitoring_statistics(self) -> Dict[str, Any]:
        """Get comprehensive monitoring statistics"""
        if not self.metrics_history:
            return {"status": "no_data"}
        
        recent_metrics = list(self.metrics_history)[-100:]  # Last 100 measurements
        
        utilizations = [m["utilization"] for m in recent_metrics]
        token_counts = [m["total_tokens"] for m in recent_metrics]
        
        return {
            "monitoring_status": "active" if self.monitoring_active else "inactive",
            "total_measurements": len(self.metrics_history),
            "recent_measurements": len(recent_metrics),
            "average_utilization": sum(utilizations) / len(utilizations),
            "peak_utilization": max(utilizations),
            "current_utilization": utilizations[-1] if utilizations else 0.0,
            "average_tokens": sum(token_counts) / len(token_counts),
            "peak_tokens": max(token_counts),
            "current_tokens": token_counts[-1] if token_counts else 0,
            "total_alerts": len(self.recent_alerts),
            "alert_breakdown": {
                level.value: sum(1 for alert in self.recent_alerts if alert.level == level)
                for level in BudgetAlertLevel
            },
            "last_alert": asdict(self.recent_alerts[-1]) if self.recent_alerts else None
        }

# Convenience functions
def create_budget_monitor(context_manager: ContextManager, 
                         enable_monitoring: bool = True) -> BudgetMonitor:
    """Create budget monitor for framework integration"""
    monitor = BudgetMonitor(context_manager, enable_auto_actions=True)
    
    if enable_monitoring:
        monitor.start_monitoring()
    
    return monitor

def setup_console_alert_handler(monitor: BudgetMonitor):
    """Setup console logging alert handler"""
    def console_handler(alert: BudgetAlert):
        level_symbols = {
            BudgetAlertLevel.INFO: "ℹ️",
            BudgetAlertLevel.WARNING: "⚠️",
            BudgetAlertLevel.CRITICAL: "🚨",
            BudgetAlertLevel.EMERGENCY: "🔥"
        }
        
        symbol = level_symbols.get(alert.level, "❓")
        print(f"{symbol} BUDGET ALERT: {alert.message}")
        
        if alert.recommended_actions:
            print(f"   Recommended actions: {', '.join(action.value for action in alert.recommended_actions)}")
    
    monitor.add_alert_handler(console_handler)

if __name__ == "__main__":
    # Test the budget monitor
    from context_manager import create_framework_context_manager, ContextItemType
    
    print("📊 BUDGET MONITOR TEST")
    print("=" * 50)
    
    # Create context manager with small budget for testing
    cm = create_framework_context_manager(max_tokens=1000)
    monitor = create_budget_monitor(cm, enable_monitoring=False)
    setup_console_alert_handler(monitor)
    
    # Add content to trigger alerts
    test_content = "This is test content for budget monitoring. " * 20
    
    for i in range(5):
        cm.add_context(
            content=f"{test_content} Item {i}",
            importance=0.5,
            item_type=ContextItemType.AGENT_OUTPUT,
            source=f"test_source_{i}"
        )
        
        alert_level, alert = monitor.check_budget_status()
        metrics = cm.get_context_summary()
        
        print(f"Step {i+1}: {metrics.total_tokens:,} tokens ({metrics.budget_utilization:.1%}) - {alert_level.value}")
        
        if alert:
            print(f"  Alert: {alert.message}")
    
    # Get optimization recommendations
    optimization = monitor.get_budget_optimization_recommendations()
    print(f"\nOptimization: {optimization.rationale}")
    
    print("\n✅ Budget monitor test completed")