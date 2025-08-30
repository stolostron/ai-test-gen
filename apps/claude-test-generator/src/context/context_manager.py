#!/usr/bin/env python3
"""
Context Manager - Factor 3: Own Your Context Window
=================================================

Intelligent context window management with token counting, budget allocation,
and compression strategies. Prevents token overflow failures and maintains
critical information through importance scoring.

Key Features:
- Accurate token counting (Claude-specific tokenization)
- Budget allocation across framework phases
- Importance-based content prioritization
- Smart compression when approaching limits
- Real-time context monitoring and alerts
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import time
from datetime import datetime
from pathlib import Path

# For Claude tokenization - fallback to tiktoken if not available
try:
    import anthropic
    CLAUDE_TOKENIZER_AVAILABLE = True
except ImportError:
    CLAUDE_TOKENIZER_AVAILABLE = False

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

logger = logging.getLogger(__name__)

class ContextItemType(str, Enum):
    """Types of context items for importance scoring"""
    FOUNDATION = "foundation"           # Foundation context (highest importance)
    AGENT_OUTPUT = "agent_output"       # Agent analysis results
    TEMPLATE = "template"               # Templates and prompts
    METADATA = "metadata"               # Execution metadata
    DEBUG = "debug"                     # Debug information
    TEMPORARY = "temporary"             # Temporary data (lowest importance)

class CompressionStrategy(str, Enum):
    """Context compression strategies"""
    IMPORTANCE_BASED = "importance"     # Remove by importance score
    TEMPORAL = "temporal"               # Remove oldest content
    SUMMARIZATION = "summarization"     # Compress into summaries
    HYBRID = "hybrid"                   # Combine multiple strategies

@dataclass
class ContextItem:
    """Individual context item with metadata"""
    content: str
    importance: float                   # 0.0 to 1.0 (1.0 = critical)
    item_type: ContextItemType
    source: str                        # Source component/agent
    timestamp: float
    token_count: int
    compressed: bool = False
    original_size: Optional[int] = None # Original token count before compression
    compression_ratio: Optional[float] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class ContextBudget:
    """Context budget allocation across framework phases"""
    max_tokens: int
    foundation_budget: int              # Tokens for foundation context
    agent_outputs_budget: int           # Tokens for agent results
    templates_budget: int               # Tokens for templates/prompts
    buffer_budget: int                  # Safety buffer
    used_tokens: int = 0
    allocated_tokens: Dict[str, int] = None
    
    def __post_init__(self):
        if self.allocated_tokens is None:
            self.allocated_tokens = {}

@dataclass
class ContextMetrics:
    """Context usage metrics and statistics"""
    total_items: int
    total_tokens: int
    budget_utilization: float           # 0.0 to 1.0
    compression_savings: int           # Tokens saved through compression
    items_by_type: Dict[ContextItemType, int]
    tokens_by_type: Dict[ContextItemType, int]
    average_importance: float
    oldest_item_age: float             # Seconds since oldest item
    compression_ratio: float           # Overall compression ratio
    
class TokenCounter:
    """Token counting utility with Claude and fallback support"""
    
    def __init__(self, model: str = "claude-4-sonnet-20241022"):
        self.model = model
        self._setup_tokenizer()
    
    def _setup_tokenizer(self):
        """Setup appropriate tokenizer based on availability"""
        if CLAUDE_TOKENIZER_AVAILABLE:
            try:
                # Try to setup Anthropic client for token counting
                self.client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
                self.tokenizer_type = "claude"
                logger.info("Using Claude native tokenization")
            except Exception as e:
                logger.warning(f"Claude tokenizer setup failed: {e}, falling back to tiktoken")
                self._setup_tiktoken_fallback()
        else:
            self._setup_tiktoken_fallback()
    
    def _setup_tiktoken_fallback(self):
        """Setup tiktoken as fallback tokenizer"""
        if TIKTOKEN_AVAILABLE:
            try:
                # Use GPT-4 tokenizer as approximation for Claude
                self.encoding = tiktoken.encoding_for_model("gpt-4")
                self.tokenizer_type = "tiktoken"
                logger.info("Using tiktoken fallback for token counting")
            except Exception as e:
                logger.warning(f"Tiktoken setup failed: {e}, using character estimation")
                self.tokenizer_type = "estimation"
        else:
            logger.warning("No tokenizer available, using character-based estimation")
            self.tokenizer_type = "estimation"
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using best available method"""
        if not text:
            return 0
        
        try:
            if self.tokenizer_type == "claude":
                # Use Claude's native token counting if available
                return self._count_claude_tokens(text)
            elif self.tokenizer_type == "tiktoken":
                # Use tiktoken for approximation
                return len(self.encoding.encode(text))
            else:
                # Fallback to character estimation (rough approximation)
                return self._estimate_tokens_from_chars(text)
        except Exception as e:
            logger.warning(f"Token counting failed: {e}, using estimation")
            return self._estimate_tokens_from_chars(text)
    
    def _count_claude_tokens(self, text: str) -> int:
        """Count tokens using Claude's API (when available)"""
        try:
            # This would use Anthropic's token counting API when available
            # For now, fall back to tiktoken
            if hasattr(self, 'encoding'):
                return len(self.encoding.encode(text))
            else:
                return self._estimate_tokens_from_chars(text)
        except Exception as e:
            logger.debug(f"Claude token counting failed: {e}")
            return self._estimate_tokens_from_chars(text)
    
    def _estimate_tokens_from_chars(self, text: str) -> int:
        """Estimate tokens from character count (rough approximation)"""
        # Rough estimation: ~4 characters per token for English text
        # This is conservative to avoid underestimating
        return max(1, len(text) // 3)  # Conservative estimate

class ContextManager:
    """
    Intelligent context window management for Claude Test Generator
    
    Manages token budgets, importance scoring, and compression to prevent
    context overflow while preserving critical information.
    """
    
    def __init__(self, 
                 max_tokens: int = 200000,
                 model: str = "claude-4-sonnet-20241022",
                 compression_threshold: float = 0.85,
                 framework_root: str = None):
        """
        Initialize context manager
        
        Args:
            max_tokens: Maximum context window size
            model: Model name for tokenization
            compression_threshold: Trigger compression at this utilization
            framework_root: Framework root directory
        """
        self.max_tokens = max_tokens
        self.model = model
        self.compression_threshold = compression_threshold
        self.framework_root = framework_root or os.getcwd()
        
        # Initialize tokenizer
        self.token_counter = TokenCounter(model)
        
        # Context storage
        self.context_items: List[ContextItem] = []
        self.current_token_count = 0
        
        # Budget allocation (based on 12-factor recommendation)
        self.budget = ContextBudget(
            max_tokens=max_tokens,
            foundation_budget=int(max_tokens * 0.15),     # 15% for foundation
            agent_outputs_budget=int(max_tokens * 0.50),  # 50% for agent outputs
            templates_budget=int(max_tokens * 0.20),      # 20% for templates
            buffer_budget=int(max_tokens * 0.15)          # 15% safety buffer
        )
        
        # Context state
        self.compression_stats = {
            "compressions_performed": 0,
            "tokens_saved": 0,
            "items_compressed": 0,
            "items_removed": 0
        }
        
        logger.info(f"Context Manager initialized: {max_tokens:,} token budget, {self.token_counter.tokenizer_type} tokenizer")
    
    def add_context(self, 
                   content: str, 
                   importance: float,
                   item_type: ContextItemType,
                   source: str,
                   metadata: Dict[str, Any] = None) -> bool:
        """
        Add content to context window with intelligent budget management
        
        Args:
            content: Text content to add
            importance: Importance score (0.0 to 1.0)
            item_type: Type of context item
            source: Source component/agent
            metadata: Additional metadata
            
        Returns:
            True if content was added, False if rejected
        """
        if not content or not content.strip():
            return False
        
        # Count tokens in new content
        token_count = self.token_counter.count_tokens(content)
        
        # Check if we need compression
        if self.current_token_count + token_count > self.max_tokens * self.compression_threshold:
            logger.info(f"Context approaching limit ({self.current_token_count + token_count:,} tokens), triggering compression")
            self._compress_context_intelligent(token_count)
        
        # Create context item
        context_item = ContextItem(
            content=content,
            importance=importance,
            item_type=item_type,
            source=source,
            timestamp=time.time(),
            token_count=token_count,
            metadata=metadata or {}
        )
        
        # Check budget allocation for this type
        type_budget = self._get_budget_for_type(item_type)
        type_usage = self._get_current_usage_for_type(item_type)
        
        if type_usage + token_count > type_budget:
            logger.warning(f"Budget exceeded for {item_type.value}: {type_usage + token_count:,} > {type_budget:,}")
            # Try to compress items of this type
            self._compress_items_by_type(item_type, token_count)
        
        # Add item if we have space
        if self.current_token_count + token_count <= self.max_tokens:
            self.context_items.append(context_item)
            self.current_token_count += token_count
            self.budget.used_tokens = self.current_token_count
            
            logger.debug(f"Added context: {token_count:,} tokens from {source} ({item_type.value})")
            return True
        else:
            logger.error(f"Cannot add context: would exceed maximum tokens ({self.current_token_count + token_count:,} > {self.max_tokens:,})")
            return False
    
    def get_context_summary(self) -> ContextMetrics:
        """Get comprehensive context usage metrics"""
        if not self.context_items:
            return ContextMetrics(
                total_items=0,
                total_tokens=0,
                budget_utilization=0.0,
                compression_savings=0,
                items_by_type={},
                tokens_by_type={},
                average_importance=0.0,
                oldest_item_age=0.0,
                compression_ratio=1.0
            )
        
        # Calculate metrics
        items_by_type = {}
        tokens_by_type = {}
        total_importance = 0.0
        oldest_timestamp = min(item.timestamp for item in self.context_items)
        total_original_tokens = sum(item.original_size or item.token_count for item in self.context_items)
        
        for item in self.context_items:
            # Count by type
            items_by_type[item.item_type] = items_by_type.get(item.item_type, 0) + 1
            tokens_by_type[item.item_type] = tokens_by_type.get(item.item_type, 0) + item.token_count
            total_importance += item.importance
        
        return ContextMetrics(
            total_items=len(self.context_items),
            total_tokens=self.current_token_count,
            budget_utilization=self.current_token_count / self.max_tokens,
            compression_savings=self.compression_stats["tokens_saved"],
            items_by_type=items_by_type,
            tokens_by_type=tokens_by_type,
            average_importance=total_importance / len(self.context_items),
            oldest_item_age=time.time() - oldest_timestamp,
            compression_ratio=self.current_token_count / total_original_tokens if total_original_tokens > 0 else 1.0
        )
    
    def get_context_for_phase(self, phase: str, include_types: List[ContextItemType] = None) -> str:
        """Get context content optimized for specific framework phase"""
        if include_types is None:
            include_types = [ContextItemType.FOUNDATION, ContextItemType.AGENT_OUTPUT, ContextItemType.TEMPLATE]
        
        relevant_items = [
            item for item in self.context_items 
            if item.item_type in include_types
        ]
        
        # Sort by importance (descending)
        relevant_items.sort(key=lambda x: x.importance, reverse=True)
        
        # Build context string
        context_parts = []
        for item in relevant_items:
            context_parts.append(f"[{item.source}] {item.content}")
        
        return "\n\n".join(context_parts)
    
    def compress_context_manual(self, target_reduction: float = 0.3) -> Dict[str, Any]:
        """Manually trigger context compression"""
        logger.info(f"Manual compression triggered: target reduction {target_reduction:.1%}")
        return self._compress_context_intelligent(target_tokens=int(self.current_token_count * target_reduction))
    
    def _compress_context_intelligent(self, needed_tokens: int) -> Dict[str, Any]:
        """Intelligent context compression using multiple strategies"""
        original_count = self.current_token_count
        original_items = len(self.context_items)
        
        logger.info(f"Starting intelligent compression: need {needed_tokens:,} tokens, have {original_count:,}")
        
        compression_result = {
            "strategy_used": "hybrid",
            "original_tokens": original_count,
            "original_items": original_items,
            "tokens_freed": 0,
            "items_removed": 0,
            "items_compressed": 0
        }
        
        # Strategy 1: Remove temporary/debug items first
        self._remove_low_importance_items(ContextItemType.TEMPORARY, needed_tokens * 0.3)
        self._remove_low_importance_items(ContextItemType.DEBUG, needed_tokens * 0.3)
        
        # Strategy 2: Compress agent outputs if still need space
        if self.current_token_count + needed_tokens > self.max_tokens:
            self._compress_items_by_type(ContextItemType.AGENT_OUTPUT, needed_tokens * 0.4)
        
        # Strategy 3: Remove oldest metadata if still need space
        if self.current_token_count + needed_tokens > self.max_tokens:
            self._remove_oldest_items(ContextItemType.METADATA, needed_tokens * 0.2)
        
        # Update compression stats
        compression_result["tokens_freed"] = original_count - self.current_token_count
        compression_result["items_removed"] = original_items - len(self.context_items)
        compression_result["final_tokens"] = self.current_token_count
        compression_result["final_items"] = len(self.context_items)
        
        self.compression_stats["compressions_performed"] += 1
        self.compression_stats["tokens_saved"] += compression_result["tokens_freed"]
        
        logger.info(f"Compression complete: freed {compression_result['tokens_freed']:,} tokens, removed {compression_result['items_removed']} items")
        
        return compression_result
    
    def _remove_low_importance_items(self, item_type: ContextItemType, target_tokens: int):
        """Remove low-importance items of specific type"""
        items_of_type = [item for item in self.context_items if item.item_type == item_type]
        items_of_type.sort(key=lambda x: x.importance)  # Ascending order (lowest first)
        
        tokens_freed = 0
        items_to_remove = []
        
        for item in items_of_type:
            if tokens_freed >= target_tokens:
                break
            items_to_remove.append(item)
            tokens_freed += item.token_count
        
        # Remove items
        for item in items_to_remove:
            self.context_items.remove(item)
            self.current_token_count -= item.token_count
            
        if items_to_remove:
            logger.debug(f"Removed {len(items_to_remove)} low-importance {item_type.value} items, freed {tokens_freed:,} tokens")
    
    def _compress_items_by_type(self, item_type: ContextItemType, target_tokens: int):
        """Compress items of specific type using summarization"""
        items_of_type = [item for item in self.context_items if item.item_type == item_type and not item.compressed]
        
        if not items_of_type:
            return
        
        # Sort by importance (keep highest importance items uncompressed)
        items_of_type.sort(key=lambda x: x.importance)
        
        tokens_saved = 0
        for item in items_of_type:
            if tokens_saved >= target_tokens:
                break
            
            # Simple compression: keep first 50% of content
            original_content = item.content
            original_tokens = item.token_count
            
            compressed_content = self._compress_content_simple(original_content)
            new_token_count = self.token_counter.count_tokens(compressed_content)
            
            if new_token_count < original_tokens:
                item.content = compressed_content
                item.original_size = original_tokens
                item.token_count = new_token_count
                item.compressed = True
                item.compression_ratio = new_token_count / original_tokens
                
                tokens_saved += original_tokens - new_token_count
                self.current_token_count -= original_tokens - new_token_count
                self.compression_stats["items_compressed"] += 1
        
        if tokens_saved > 0:
            logger.debug(f"Compressed {item_type.value} items, saved {tokens_saved:,} tokens")
    
    def _remove_oldest_items(self, item_type: ContextItemType, target_tokens: int):
        """Remove oldest items of specific type"""
        items_of_type = [item for item in self.context_items if item.item_type == item_type]
        items_of_type.sort(key=lambda x: x.timestamp)  # Ascending order (oldest first)
        
        tokens_freed = 0
        items_to_remove = []
        
        for item in items_of_type:
            if tokens_freed >= target_tokens:
                break
            items_to_remove.append(item)
            tokens_freed += item.token_count
        
        # Remove items
        for item in items_to_remove:
            self.context_items.remove(item)
            self.current_token_count -= item.token_count
            
        if items_to_remove:
            logger.debug(f"Removed {len(items_to_remove)} oldest {item_type.value} items, freed {tokens_freed:,} tokens")
    
    def _compress_content_simple(self, content: str) -> str:
        """Simple content compression strategy"""
        lines = content.split('\n')
        
        # Keep first and last 25% of lines, add summary in middle
        if len(lines) > 10:
            keep_start = max(1, len(lines) // 4)
            keep_end = max(1, len(lines) // 4)
            
            start_lines = lines[:keep_start]
            end_lines = lines[-keep_end:]
            
            summary_line = f"[COMPRESSED: {len(lines) - keep_start - keep_end} lines omitted]"
            
            return '\n'.join(start_lines + [summary_line] + end_lines)
        else:
            # If content is short, just truncate to 70%
            return content[:int(len(content) * 0.7)] + " [TRUNCATED]"
    
    def _get_budget_for_type(self, item_type: ContextItemType) -> int:
        """Get budget allocation for specific context item type"""
        budget_mapping = {
            ContextItemType.FOUNDATION: self.budget.foundation_budget,
            ContextItemType.AGENT_OUTPUT: self.budget.agent_outputs_budget,
            ContextItemType.TEMPLATE: self.budget.templates_budget,
            ContextItemType.METADATA: self.budget.buffer_budget // 2,
            ContextItemType.DEBUG: self.budget.buffer_budget // 4,
            ContextItemType.TEMPORARY: self.budget.buffer_budget // 4
        }
        return budget_mapping.get(item_type, self.budget.buffer_budget // 4)
    
    def _get_current_usage_for_type(self, item_type: ContextItemType) -> int:
        """Get current token usage for specific context item type"""
        return sum(item.token_count for item in self.context_items if item.item_type == item_type)
    
    def save_context_state(self, run_dir: str = None) -> str:
        """Save current context state to file"""
        if run_dir:
            state_file = Path(run_dir) / "context_state.json"
        else:
            state_file = Path(self.framework_root) / ".claude" / "context" / f"context_state_{int(time.time())}.json"
        
        state_file.parent.mkdir(parents=True, exist_ok=True)
        
        state_data = {
            "timestamp": datetime.now().isoformat(),
            "max_tokens": self.max_tokens,
            "current_token_count": self.current_token_count,
            "budget": asdict(self.budget),
            "compression_stats": self.compression_stats,
            "context_items": [asdict(item) for item in self.context_items],
            "metrics": asdict(self.get_context_summary())
        }
        
        with open(state_file, 'w') as f:
            json.dump(state_data, f, indent=2, default=str)
        
        logger.info(f"Context state saved to {state_file}")
        return str(state_file)
    
    def load_context_state(self, state_file: str) -> bool:
        """Load context state from file"""
        try:
            with open(state_file, 'r') as f:
                state_data = json.load(f)
            
            self.max_tokens = state_data["max_tokens"]
            self.current_token_count = state_data["current_token_count"]
            self.compression_stats = state_data["compression_stats"]
            
            # Reconstruct context items
            self.context_items = []
            for item_data in state_data["context_items"]:
                item = ContextItem(**item_data)
                self.context_items.append(item)
            
            logger.info(f"Context state loaded from {state_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to load context state: {e}")
            return False

# Convenience functions for framework integration
def create_framework_context_manager(max_tokens: int = 200000) -> ContextManager:
    """Create context manager optimized for Claude Test Generator framework"""
    return ContextManager(
        max_tokens=max_tokens,
        model="claude-4-sonnet-20241022",
        compression_threshold=0.85
    )

def get_importance_score(content_type: str, source: str, phase: str = None) -> float:
    """Get recommended importance score for content"""
    importance_mapping = {
        "foundation_context": 0.95,      # Critical foundation data
        "jira_analysis": 0.90,           # Primary requirements
        "environment_data": 0.85,        # Environment specifics
        "github_analysis": 0.80,         # Code insights
        "documentation": 0.75,           # Supporting documentation
        "qe_intelligence": 0.70,         # QE insights
        "template": 0.65,                # Templates and prompts
        "metadata": 0.50,                # Execution metadata
        "debug": 0.30,                   # Debug information
        "temporary": 0.20                # Temporary data
    }
    
    return importance_mapping.get(content_type, 0.50)

if __name__ == "__main__":
    # Test the context manager
    cm = create_framework_context_manager(100000)
    
    # Add some test content
    cm.add_context(
        "This is foundation context for ACM-22079: ClusterCurator digest-based upgrades",
        importance=0.95,
        item_type=ContextItemType.FOUNDATION,
        source="foundation_context"
    )
    
    cm.add_context(
        "Agent A analysis: ClusterCurator requires digest-based upgrade functionality for disconnected environments. This feature enables reliable upgrades using image digests instead of tags.",
        importance=0.90,
        item_type=ContextItemType.AGENT_OUTPUT,
        source="agent_a_jira_intelligence"
    )
    
    # Test metrics
    metrics = cm.get_context_summary()
    print(f"Context Manager Test:")
    print(f"  Total tokens: {metrics.total_tokens:,}")
    print(f"  Budget utilization: {metrics.budget_utilization:.1%}")
    print(f"  Items by type: {metrics.items_by_type}")
    print(f"  Average importance: {metrics.average_importance:.2f}")