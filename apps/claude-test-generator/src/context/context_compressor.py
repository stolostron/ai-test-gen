#!/usr/bin/env python3
"""
Context Compressor - Smart Compression Engine
===========================================

Advanced context compression strategies with importance-based preservation,
semantic summarization, and adaptive compression based on content type.

Key Features:
- Importance-based compression (preserve critical information)
- Semantic summarization for agent outputs
- Content-type aware compression strategies
- Adaptive compression ratios based on context pressure
- Reversible compression with metadata preservation
"""

import os
import json
import logging
import re
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import time
from datetime import datetime
from pathlib import Path

# For advanced text processing
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

from context_manager import ContextItem, ContextItemType, CompressionStrategy

logger = logging.getLogger(__name__)

@dataclass
class CompressionResult:
    """Result of context compression operation"""
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    strategy_used: CompressionStrategy
    content_preserved: str
    content_removed: str
    metadata: Dict[str, Any]
    reversible: bool = False
    
    def __post_init__(self):
        if self.compression_ratio == 0.0 and self.original_tokens > 0:
            self.compression_ratio = self.compressed_tokens / self.original_tokens

@dataclass
class CompressionProfile:
    """Compression profile for different content types"""
    content_type: ContextItemType
    importance_threshold: float      # Don't compress if importance above this
    max_compression_ratio: float     # Maximum compression (0.0 = remove all, 1.0 = no compression)
    preferred_strategy: CompressionStrategy
    preserve_patterns: List[str]     # Regex patterns to always preserve
    remove_patterns: List[str]       # Patterns that can be removed first

class SemanticSummarizer:
    """Semantic text summarization for context compression"""
    
    def __init__(self):
        self.setup_complete = False
        self._setup_nlp()
    
    def _setup_nlp(self):
        """Setup NLP pipeline for summarization"""
        if SPACY_AVAILABLE:
            try:
                import spacy
                self.nlp = spacy.load("en_core_web_sm")
                self.setup_complete = True
                logger.info("Semantic summarizer initialized with spaCy")
            except OSError:
                logger.warning("spaCy model 'en_core_web_sm' not found, using rule-based summarization")
                self.setup_complete = False
        else:
            logger.info("spaCy not available, using rule-based summarization")
            self.setup_complete = False
    
    def summarize_text(self, text: str, target_ratio: float = 0.5) -> str:
        """
        Summarize text to target compression ratio
        
        Args:
            text: Input text to summarize
            target_ratio: Target ratio of output/input length
            
        Returns:
            Summarized text
        """
        if not text or not text.strip():
            return text
        
        if self.setup_complete:
            return self._semantic_summarize(text, target_ratio)
        else:
            return self._rule_based_summarize(text, target_ratio)
    
    def _semantic_summarize(self, text: str, target_ratio: float) -> str:
        """Semantic summarization using spaCy"""
        try:
            doc = self.nlp(text)
            sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
            
            if len(sentences) <= 2:
                return text  # Too short to summarize meaningfully
            
            # Score sentences by various criteria
            scored_sentences = []
            for i, sentence in enumerate(sentences):
                score = self._score_sentence(sentence, i, len(sentences))
                scored_sentences.append((score, sentence))
            
            # Sort by score and take top sentences
            scored_sentences.sort(reverse=True, key=lambda x: x[0])
            target_count = max(1, int(len(sentences) * target_ratio))
            
            selected_sentences = [sent for _, sent in scored_sentences[:target_count]]
            
            # Reorder sentences to maintain original flow
            ordered_summary = []
            for sentence in sentences:
                if sentence in selected_sentences:
                    ordered_summary.append(sentence)
            
            return ' '.join(ordered_summary)
            
        except Exception as e:
            logger.warning(f"Semantic summarization failed: {e}, falling back to rule-based")
            return self._rule_based_summarize(text, target_ratio)
    
    def _score_sentence(self, sentence: str, position: int, total_sentences: int) -> float:
        """Score sentence importance for summarization"""
        score = 0.0
        
        # Position scoring (first and last sentences often important)
        if position == 0 or position == total_sentences - 1:
            score += 0.3
        elif position < total_sentences * 0.2:  # Early sentences
            score += 0.2
        
        # Length scoring (avoid very short sentences)
        word_count = len(sentence.split())
        if 5 <= word_count <= 25:
            score += 0.2
        elif word_count < 5:
            score -= 0.2
        
        # Keyword scoring
        important_keywords = [
            'requirement', 'critical', 'important', 'must', 'required',
            'error', 'failure', 'issue', 'problem', 'solution',
            'test', 'validate', 'verify', 'confirm', 'ensure',
            'configuration', 'setup', 'deploy', 'install',
            'cluster', 'node', 'pod', 'namespace', 'service'
        ]
        
        sentence_lower = sentence.lower()
        keyword_count = sum(1 for keyword in important_keywords if keyword in sentence_lower)
        score += keyword_count * 0.1
        
        # Avoid sentences with just code/commands
        if re.match(r'^\s*[`$#]|^\s*\w+:\s*$', sentence):
            score -= 0.3
        
        return score
    
    def _rule_based_summarize(self, text: str, target_ratio: float) -> str:
        """Rule-based summarization fallback"""
        lines = text.split('\n')
        
        # Prioritize lines that contain important information
        important_lines = []
        regular_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Important patterns
            important_patterns = [
                r'error|failure|critical|important|required|must',
                r'test.*case|validation|verification',
                r'configuration|setup|deployment',
                r'jira|ticket|requirement',
                r'^\s*[A-Z][^.]*:',  # Headers/labels
                r'^\s*\d+\.',        # Numbered items
                r'^\s*[-*]',         # Bullet points
            ]
            
            is_important = any(re.search(pattern, line, re.IGNORECASE) for pattern in important_patterns)
            
            if is_important:
                important_lines.append(line)
            else:
                regular_lines.append(line)
        
        # Calculate how many lines to keep
        total_lines = len(important_lines) + len(regular_lines)
        target_lines = max(1, int(total_lines * target_ratio))
        
        # Always keep important lines, then add regular lines
        selected_lines = important_lines[:target_lines]
        remaining_slots = target_lines - len(selected_lines)
        
        if remaining_slots > 0:
            selected_lines.extend(regular_lines[:remaining_slots])
        
        return '\n'.join(selected_lines)

class AdvancedContextCompressor:
    """
    Advanced context compression engine with multiple strategies
    """
    
    def __init__(self):
        self.summarizer = SemanticSummarizer()
        self.compression_profiles = self._create_compression_profiles()
        self.compression_history = []
        
    def _create_compression_profiles(self) -> Dict[ContextItemType, CompressionProfile]:
        """Create compression profiles for different content types"""
        return {
            ContextItemType.FOUNDATION: CompressionProfile(
                content_type=ContextItemType.FOUNDATION,
                importance_threshold=0.95,  # Almost never compress foundation
                max_compression_ratio=0.9,
                preferred_strategy=CompressionStrategy.IMPORTANCE_BASED,
                preserve_patterns=[
                    r'jira.*id|ticket.*id',
                    r'version|release',
                    r'environment|cluster',
                    r'critical|important|required'
                ],
                remove_patterns=[
                    r'debug|trace|verbose',
                    r'timestamp|metadata',
                ]
            ),
            
            ContextItemType.AGENT_OUTPUT: CompressionProfile(
                content_type=ContextItemType.AGENT_OUTPUT,
                importance_threshold=0.80,
                max_compression_ratio=0.6,
                preferred_strategy=CompressionStrategy.SUMMARIZATION,
                preserve_patterns=[
                    r'requirement|specification',
                    r'test.*case|validation',
                    r'error|failure|issue',
                    r'configuration|setup'
                ],
                remove_patterns=[
                    r'example|sample|demo',
                    r'verbose.*log|debug.*info',
                    r'timestamp|execution.*time'
                ]
            ),
            
            ContextItemType.TEMPLATE: CompressionProfile(
                content_type=ContextItemType.TEMPLATE,
                importance_threshold=0.75,
                max_compression_ratio=0.7,
                preferred_strategy=CompressionStrategy.IMPORTANCE_BASED,
                preserve_patterns=[
                    r'mandatory|required',
                    r'template|format',
                    r'validation|enforcement'
                ],
                remove_patterns=[
                    r'example|sample',
                    r'comment|note'
                ]
            ),
            
            ContextItemType.METADATA: CompressionProfile(
                content_type=ContextItemType.METADATA,
                importance_threshold=0.60,
                max_compression_ratio=0.4,
                preferred_strategy=CompressionStrategy.TEMPORAL,
                preserve_patterns=[
                    r'version|release',
                    r'status|state'
                ],
                remove_patterns=[
                    r'timestamp|time',
                    r'debug|trace',
                    r'temporary|temp'
                ]
            ),
            
            ContextItemType.DEBUG: CompressionProfile(
                content_type=ContextItemType.DEBUG,
                importance_threshold=0.40,
                max_compression_ratio=0.2,
                preferred_strategy=CompressionStrategy.TEMPORAL,
                preserve_patterns=[
                    r'error|exception|failure'
                ],
                remove_patterns=[
                    r'trace|stack.*trace',
                    r'debug.*log|verbose',
                    r'timestamp|time'
                ]
            ),
            
            ContextItemType.TEMPORARY: CompressionProfile(
                content_type=ContextItemType.TEMPORARY,
                importance_threshold=0.30,
                max_compression_ratio=0.1,
                preferred_strategy=CompressionStrategy.TEMPORAL,
                preserve_patterns=[],
                remove_patterns=[
                    r'.*'  # Can remove almost everything
                ]
            )
        }
    
    def compress_context_item(self, 
                             item: ContextItem, 
                             target_ratio: float = None,
                             strategy: CompressionStrategy = None) -> CompressionResult:
        """
        Compress a single context item using optimal strategy
        
        Args:
            item: Context item to compress
            target_ratio: Target compression ratio (optional)
            strategy: Compression strategy to use (optional)
            
        Returns:
            CompressionResult with compressed content and metadata
        """
        # Get compression profile for this item type
        profile = self.compression_profiles.get(item.item_type, self.compression_profiles[ContextItemType.TEMPORARY])
        
        # Check if item should be compressed based on importance
        if item.importance > profile.importance_threshold:
            logger.debug(f"Skipping compression for high-importance {item.item_type.value} item (importance: {item.importance:.2f})")
            return CompressionResult(
                original_tokens=item.token_count,
                compressed_tokens=item.token_count,
                compression_ratio=1.0,
                strategy_used=CompressionStrategy.IMPORTANCE_BASED,
                content_preserved=item.content,
                content_removed="",
                metadata={"skipped": "high_importance"},
                reversible=True
            )
        
        # Determine compression strategy and target ratio
        compression_strategy = strategy or profile.preferred_strategy
        compression_ratio = target_ratio or profile.max_compression_ratio
        
        logger.debug(f"Compressing {item.item_type.value} item using {compression_strategy.value} strategy (target ratio: {compression_ratio:.2f})")
        
        # Apply compression based on strategy
        if compression_strategy == CompressionStrategy.IMPORTANCE_BASED:
            return self._compress_importance_based(item, compression_ratio, profile)
        elif compression_strategy == CompressionStrategy.SUMMARIZATION:
            return self._compress_summarization(item, compression_ratio, profile)
        elif compression_strategy == CompressionStrategy.TEMPORAL:
            return self._compress_temporal(item, compression_ratio, profile)
        elif compression_strategy == CompressionStrategy.HYBRID:
            return self._compress_hybrid(item, compression_ratio, profile)
        else:
            # Default to importance-based
            return self._compress_importance_based(item, compression_ratio, profile)
    
    def _compress_importance_based(self, 
                                  item: ContextItem, 
                                  target_ratio: float, 
                                  profile: CompressionProfile) -> CompressionResult:
        """Compress based on content importance patterns"""
        content = item.content
        lines = content.split('\n')
        
        # Score lines by importance
        scored_lines = []
        for i, line in enumerate(lines):
            score = self._score_line_importance(line, profile)
            scored_lines.append((score, line, i))
        
        # Sort by importance and keep top lines
        scored_lines.sort(reverse=True, key=lambda x: x[0])
        target_lines = max(1, int(len(lines) * target_ratio))
        
        preserved_lines = [(line, orig_idx) for _, line, orig_idx in scored_lines[:target_lines]]
        removed_lines = [line for _, line, _ in scored_lines[target_lines:]]
        
        # Maintain original order for preserved lines
        preserved_lines.sort(key=lambda x: x[1])
        compressed_content = '\n'.join([line for line, _ in preserved_lines])
        removed_content = '\n'.join(removed_lines)
        
        # Calculate token counts (approximate)
        compressed_tokens = int(item.token_count * len(compressed_content) / len(content)) if content else 0
        
        return CompressionResult(
            original_tokens=item.token_count,
            compressed_tokens=compressed_tokens,
            compression_ratio=compressed_tokens / item.token_count if item.token_count > 0 else 0.0,
            strategy_used=CompressionStrategy.IMPORTANCE_BASED,
            content_preserved=compressed_content,
            content_removed=removed_content,
            metadata={
                "lines_preserved": len(preserved_lines),
                "lines_removed": len(removed_lines),
                "importance_threshold": profile.importance_threshold
            },
            reversible=True
        )
    
    def _compress_summarization(self, 
                               item: ContextItem, 
                               target_ratio: float, 
                               profile: CompressionProfile) -> CompressionResult:
        """Compress using semantic summarization"""
        content = item.content
        
        # Apply semantic summarization
        summarized_content = self.summarizer.summarize_text(content, target_ratio)
        
        # Calculate token counts (approximate)
        compressed_tokens = int(item.token_count * len(summarized_content) / len(content)) if content else 0
        
        return CompressionResult(
            original_tokens=item.token_count,
            compressed_tokens=compressed_tokens,
            compression_ratio=compressed_tokens / item.token_count if item.token_count > 0 else 0.0,
            strategy_used=CompressionStrategy.SUMMARIZATION,
            content_preserved=summarized_content,
            content_removed="[SUMMARIZED CONTENT]",
            metadata={
                "summarization_ratio": target_ratio,
                "semantic_analysis": "applied"
            },
            reversible=False  # Summarization is not reversible
        )
    
    def _compress_temporal(self, 
                          item: ContextItem, 
                          target_ratio: float, 
                          profile: CompressionProfile) -> CompressionResult:
        """Compress based on temporal patterns (remove older content)"""
        content = item.content
        lines = content.split('\n')
        
        # For temporal compression, keep more recent content
        # Assume content is roughly chronological
        target_lines = max(1, int(len(lines) * target_ratio))
        
        # Keep the last N lines (most recent)
        preserved_lines = lines[-target_lines:]
        removed_lines = lines[:-target_lines] if target_lines < len(lines) else []
        
        compressed_content = '\n'.join(preserved_lines)
        removed_content = '\n'.join(removed_lines)
        
        # Add temporal marker
        if removed_lines:
            compressed_content = f"[OLDER CONTENT REMOVED: {len(removed_lines)} lines]\n{compressed_content}"
        
        # Calculate token counts (approximate)
        compressed_tokens = int(item.token_count * len(compressed_content) / len(content)) if content else 0
        
        return CompressionResult(
            original_tokens=item.token_count,
            compressed_tokens=compressed_tokens,
            compression_ratio=compressed_tokens / item.token_count if item.token_count > 0 else 0.0,
            strategy_used=CompressionStrategy.TEMPORAL,
            content_preserved=compressed_content,
            content_removed=removed_content,
            metadata={
                "lines_preserved": len(preserved_lines),
                "lines_removed": len(removed_lines),
                "temporal_strategy": "keep_recent"
            },
            reversible=True
        )
    
    def _compress_hybrid(self, 
                        item: ContextItem, 
                        target_ratio: float, 
                        profile: CompressionProfile) -> CompressionResult:
        """Hybrid compression using multiple strategies"""
        # First apply importance-based compression (50% of target)
        importance_result = self._compress_importance_based(item, min(1.0, target_ratio / 0.5), profile)
        
        # Then apply summarization to the result (remaining compression)
        if importance_result.compression_ratio > target_ratio:
            # Create temporary item for second compression
            temp_item = ContextItem(
                content=importance_result.content_preserved,
                importance=item.importance,
                item_type=item.item_type,
                source=item.source,
                timestamp=item.timestamp,
                token_count=importance_result.compressed_tokens
            )
            
            secondary_ratio = target_ratio / importance_result.compression_ratio
            summary_result = self._compress_summarization(temp_item, secondary_ratio, profile)
            
            return CompressionResult(
                original_tokens=item.token_count,
                compressed_tokens=summary_result.compressed_tokens,
                compression_ratio=summary_result.compressed_tokens / item.token_count if item.token_count > 0 else 0.0,
                strategy_used=CompressionStrategy.HYBRID,
                content_preserved=summary_result.content_preserved,
                content_removed=f"{importance_result.content_removed}\n[THEN SUMMARIZED]",
                metadata={
                    "hybrid_stages": ["importance_based", "summarization"],
                    "stage_1_ratio": importance_result.compression_ratio,
                    "stage_2_ratio": secondary_ratio
                },
                reversible=False  # Hybrid with summarization is not reversible
            )
        else:
            return importance_result
    
    def _score_line_importance(self, line: str, profile: CompressionProfile) -> float:
        """Score a line's importance for compression decisions"""
        score = 0.5  # Base score
        line_lower = line.lower().strip()
        
        if not line_lower:
            return 0.0  # Empty lines have no importance
        
        # Boost score for preserve patterns
        for pattern in profile.preserve_patterns:
            if re.search(pattern, line_lower, re.IGNORECASE):
                score += 0.3
        
        # Reduce score for remove patterns
        for pattern in profile.remove_patterns:
            if re.search(pattern, line_lower, re.IGNORECASE):
                score -= 0.4
        
        # Additional scoring based on content characteristics
        
        # Headers and structure (usually important)
        if re.match(r'^\s*#{1,6}\s+|^\s*[A-Z][^.]*:$', line):
            score += 0.2
        
        # Lists and numbered items (often important)
        if re.match(r'^\s*[-*•]\s+|^\s*\d+\.', line):
            score += 0.1
        
        # Code blocks or commands (context-dependent)
        if re.match(r'^\s*```|^\s*`|^\s*\$|^\s*#', line):
            score += 0.1
        
        # Very short lines (often less important)
        if len(line_lower) < 10:
            score -= 0.1
        
        # Lines with specific keywords
        important_keywords = ['error', 'critical', 'important', 'required', 'must', 'failure', 'issue']
        for keyword in important_keywords:
            if keyword in line_lower:
                score += 0.2
                break
        
        return max(0.0, min(1.0, score))  # Clamp to [0, 1]
    
    def get_compression_recommendations(self, 
                                      items: List[ContextItem], 
                                      target_reduction: float) -> List[Tuple[ContextItem, CompressionStrategy, float]]:
        """
        Get compression recommendations for a list of context items
        
        Args:
            items: List of context items to analyze
            target_reduction: Target token reduction (0.0 to 1.0)
            
        Returns:
            List of (item, strategy, ratio) recommendations
        """
        recommendations = []
        
        # Sort items by compressibility score (least important first)
        compressible_items = []
        for item in items:
            profile = self.compression_profiles.get(item.item_type, self.compression_profiles[ContextItemType.TEMPORARY])
            
            # Calculate compressibility score
            compressibility = self._calculate_compressibility(item, profile)
            compressible_items.append((compressibility, item))
        
        compressible_items.sort(reverse=True, key=lambda x: x[0])  # Most compressible first
        
        # Distribute compression across items
        total_tokens = sum(item.token_count for item in items)
        target_tokens_to_save = int(total_tokens * target_reduction)
        tokens_saved = 0
        
        for compressibility, item in compressible_items:
            if tokens_saved >= target_tokens_to_save:
                break
            
            profile = self.compression_profiles[item.item_type]
            
            # Calculate how much to compress this item
            remaining_tokens_needed = target_tokens_to_save - tokens_saved
            max_saveable = int(item.token_count * (1 - profile.max_compression_ratio))
            tokens_to_save = min(remaining_tokens_needed, max_saveable)
            
            if tokens_to_save > 0:
                compression_ratio = 1 - (tokens_to_save / item.token_count)
                recommendations.append((item, profile.preferred_strategy, compression_ratio))
                tokens_saved += tokens_to_save
        
        return recommendations
    
    def _calculate_compressibility(self, item: ContextItem, profile: CompressionProfile) -> float:
        """Calculate how compressible an item is (0.0 = not compressible, 1.0 = highly compressible)"""
        # Base compressibility on importance and content type
        base_score = 1.0 - item.importance
        
        # Adjust based on content type
        type_multipliers = {
            ContextItemType.FOUNDATION: 0.1,     # Very low compressibility
            ContextItemType.AGENT_OUTPUT: 0.7,   # Medium compressibility
            ContextItemType.TEMPLATE: 0.5,       # Medium-low compressibility
            ContextItemType.METADATA: 0.8,       # High compressibility
            ContextItemType.DEBUG: 0.9,          # Very high compressibility
            ContextItemType.TEMPORARY: 1.0       # Maximum compressibility
        }
        
        type_multiplier = type_multipliers.get(item.item_type, 0.5)
        
        # Consider content characteristics
        content_length = len(item.content)
        if content_length > 5000:  # Long content is more compressible
            length_bonus = 0.2
        elif content_length < 500:  # Short content less compressible
            length_bonus = -0.2
        else:
            length_bonus = 0.0
        
        final_score = base_score * type_multiplier + length_bonus
        return max(0.0, min(1.0, final_score))

# Factory function for easy integration
def create_context_compressor() -> AdvancedContextCompressor:
    """Create advanced context compressor for framework integration"""
    return AdvancedContextCompressor()

if __name__ == "__main__":
    # Test the context compressor
    from context_manager import ContextItem, ContextItemType, TokenCounter
    
    compressor = create_context_compressor()
    token_counter = TokenCounter()
    
    # Create test content
    test_content = """
    Agent A Analysis Results for ACM-22079:
    
    JIRA Intelligence Summary:
    - Ticket ID: ACM-22079
    - Component: ClusterCurator
    - Feature: Digest-based upgrades for disconnected environments
    - Priority: High
    - Customer: Amadeus
    
    Requirements Analysis:
    1. Support image digest references instead of tags
    2. Enable reliable upgrades in disconnected environments
    3. Maintain backwards compatibility with existing workflows
    4. Provide proper error handling and rollback capabilities
    
    Technical Implementation Details:
    The ClusterCurator must be enhanced to accept image digest references
    in addition to traditional tag references. This involves modifying the
    upgrade controller to handle both formats and implementing validation
    to ensure digest integrity before proceeding with upgrades.
    
    Debug Information:
    - Execution timestamp: 2025-08-29T04:30:00Z
    - Agent execution time: 2.34 seconds
    - Confidence score: 0.89
    - Context inheritance: successful
    - Validation checks: all passed
    """
    
    test_item = ContextItem(
        content=test_content,
        importance=0.70,  # Lower importance to trigger compression
        item_type=ContextItemType.AGENT_OUTPUT,
        source="agent_a_jira_intelligence",
        timestamp=time.time(),
        token_count=token_counter.count_tokens(test_content)
    )
    
    print("🗜️  CONTEXT COMPRESSOR TEST")
    print("=" * 50)
    print(f"Original content: {test_item.token_count} tokens")
    
    # Test different compression strategies
    strategies = [
        (CompressionStrategy.IMPORTANCE_BASED, 0.6),
        (CompressionStrategy.SUMMARIZATION, 0.5),
        (CompressionStrategy.TEMPORAL, 0.4),
        (CompressionStrategy.HYBRID, 0.3)
    ]
    
    for strategy, ratio in strategies:
        result = compressor.compress_context_item(test_item, ratio, strategy)
        print(f"\n{strategy.value.upper()} (target: {ratio:.1%}):")
        print(f"  Compressed: {result.compressed_tokens} tokens ({result.compression_ratio:.1%})")
        print(f"  Savings: {result.original_tokens - result.compressed_tokens} tokens")
        print(f"  Reversible: {result.reversible}")
        
    print("\n✅ Context compressor test completed")