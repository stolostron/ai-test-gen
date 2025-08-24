"""
Pattern Database for Agent Learning Framework

Stores and retrieves learned patterns for each agent with efficient caching
and fast retrieval mechanisms.
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict, deque
from typing import Dict, List, Optional, Any
import hashlib
import pickle
import aiofiles
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class PatternDatabase:
    """
    Efficient pattern storage and retrieval system for agent learning
    """
    
    def __init__(self, storage_path: str = ".claude/learning-data/patterns"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # In-memory caches for fast access
        self.pattern_cache = defaultdict(list)  # agent_id -> patterns
        self.relevance_cache = {}  # (agent_id, context_hash) -> patterns
        self.cache_ttl = 3600  # 1 hour cache TTL
        self.cache_timestamps = {}
        
        # Pattern statistics
        self.pattern_stats = defaultdict(lambda: {
            'usage_count': 0,
            'success_rate': 0.0,
            'last_used': None
        })
        
        # Load existing patterns
        self._load_patterns()
    
    def _load_patterns(self):
        """Load patterns from disk into memory cache"""
        try:
            for agent_file in self.storage_path.glob("*_patterns.json"):
                agent_id = agent_file.stem.replace("_patterns", "")
                
                with open(agent_file, 'r') as f:
                    data = json.load(f)
                    self.pattern_cache[agent_id] = data.get('patterns', [])
                    
                    # Load stats
                    stats_data = data.get('stats', {})
                    for pattern_id, stats in stats_data.items():
                        self.pattern_stats[pattern_id] = stats
                        
            logger.info(f"Loaded patterns for {len(self.pattern_cache)} agents")
            
        except Exception as e:
            logger.warning(f"Could not load existing patterns: {e}")
    
    async def store_patterns(self, agent_id: str, patterns: List[Dict]):
        """
        Store new patterns for an agent
        
        Args:
            agent_id: Agent identifier (agent_a, agent_b, etc.)
            patterns: List of pattern dictionaries
        """
        try:
            # Add patterns to cache
            self.pattern_cache[agent_id].extend(patterns)
            
            # Update pattern statistics
            for pattern in patterns:
                pattern_id = self._generate_pattern_id(pattern)
                self.pattern_stats[pattern_id]['usage_count'] += 1
                self.pattern_stats[pattern_id]['last_used'] = datetime.utcnow().isoformat()
                
                # Update success rate (moving average)
                success_rate = pattern.get('success_rate', 0.0)
                current_rate = self.pattern_stats[pattern_id]['success_rate']
                count = self.pattern_stats[pattern_id]['usage_count']
                
                # Weighted average
                new_rate = ((current_rate * (count - 1)) + success_rate) / count
                self.pattern_stats[pattern_id]['success_rate'] = new_rate
            
            # Persist to disk asynchronously
            await self._persist_patterns(agent_id)
            
            # Clear relevance cache for this agent
            self._clear_relevance_cache(agent_id)
            
            logger.debug(f"Stored {len(patterns)} patterns for {agent_id}")
            
        except Exception as e:
            logger.error(f"Failed to store patterns: {e}")
    
    async def get_relevant_patterns(self, agent_id: str, context: Dict, 
                                  max_latency_ms: int = 50) -> Optional[List[Dict]]:
        """
        Get relevant patterns for given context with latency constraint
        
        Args:
            agent_id: Agent identifier
            context: Current execution context
            max_latency_ms: Maximum allowed latency
            
        Returns:
            List of relevant patterns or None if timeout
        """
        start_time = time.time()
        
        try:
            # Check relevance cache first
            context_hash = self._hash_context(context)
            cache_key = (agent_id, context_hash)
            
            if cache_key in self.relevance_cache:
                cache_time = self.cache_timestamps.get(cache_key, 0)
                if time.time() - cache_time < self.cache_ttl:
                    return self.relevance_cache[cache_key]
            
            # Get all patterns for agent
            agent_patterns = self.pattern_cache.get(agent_id, [])
            
            if not agent_patterns:
                return None
            
            # Score patterns by relevance (with timeout)
            relevant_patterns = []
            
            for pattern in agent_patterns:
                # Check timeout
                if (time.time() - start_time) * 1000 > max_latency_ms * 0.8:
                    # Use what we have so far
                    break
                
                relevance_score = self._calculate_relevance(pattern, context)
                if relevance_score > 0.7:  # Relevance threshold
                    relevant_patterns.append({
                        **pattern,
                        'relevance_score': relevance_score,
                        'stats': self.pattern_stats.get(
                            self._generate_pattern_id(pattern), {}
                        )
                    })
            
            # Sort by relevance and success rate
            relevant_patterns.sort(
                key=lambda p: (
                    p['relevance_score'] * 0.6 + 
                    p.get('stats', {}).get('success_rate', 0) * 0.4
                ),
                reverse=True
            )
            
            # Take top patterns
            top_patterns = relevant_patterns[:5]
            
            # Cache result
            self.relevance_cache[cache_key] = top_patterns
            self.cache_timestamps[cache_key] = time.time()
            
            return top_patterns
            
        except Exception as e:
            logger.debug(f"Pattern retrieval error: {e}")
            return None
    
    def get_cached_patterns(self, agent_id: str, context: Dict) -> Optional[List[Dict]]:
        """
        Get patterns from cache only (no computation)
        Used for synchronous fast access
        """
        context_hash = self._hash_context(context)
        cache_key = (agent_id, context_hash)
        
        if cache_key in self.relevance_cache:
            cache_time = self.cache_timestamps.get(cache_key, 0)
            if time.time() - cache_time < self.cache_ttl:
                return self.relevance_cache[cache_key]
        
        # Return most successful patterns as fallback
        agent_patterns = self.pattern_cache.get(agent_id, [])
        if agent_patterns:
            # Return top 3 by success rate
            sorted_patterns = sorted(
                agent_patterns,
                key=lambda p: self.pattern_stats.get(
                    self._generate_pattern_id(p), {}
                ).get('success_rate', 0),
                reverse=True
            )
            return sorted_patterns[:3]
        
        return None
    
    def _calculate_relevance(self, pattern: Dict, context: Dict) -> float:
        """Calculate relevance score between pattern and context"""
        score = 0.0
        
        # Type matching
        pattern_type = pattern.get('type', '')
        context_type = context.get('type', '')
        
        if pattern_type and context_type and pattern_type == context_type:
            score += 0.3
        
        # Keyword matching
        pattern_keywords = set(pattern.get('pattern', {}).get('keywords', []))
        context_keywords = set(context.get('keywords', []))
        
        if pattern_keywords and context_keywords:
            overlap = len(pattern_keywords & context_keywords)
            total = len(pattern_keywords | context_keywords)
            if total > 0:
                score += 0.4 * (overlap / total)
        
        # Component matching (for JIRA patterns)
        pattern_components = set(pattern.get('pattern', {}).get('components', []))
        context_components = set(context.get('components', []))
        
        if pattern_components and context_components:
            overlap = len(pattern_components & context_components)
            if overlap > 0:
                score += 0.3
        
        return min(score, 1.0)
    
    def _generate_pattern_id(self, pattern: Dict) -> str:
        """Generate unique ID for pattern"""
        pattern_str = json.dumps(pattern.get('pattern', {}), sort_keys=True)
        return hashlib.md5(pattern_str.encode()).hexdigest()[:12]
    
    def _hash_context(self, context: Dict) -> str:
        """Generate hash for context (for caching)"""
        # Extract key fields only to avoid over-specific hashing
        key_fields = {
            'type': context.get('type'),
            'agent_id': context.get('agent_id'),
            'keywords': sorted(context.get('keywords', [])),
            'components': sorted(context.get('components', []))
        }
        context_str = json.dumps(key_fields, sort_keys=True)
        return hashlib.md5(context_str.encode()).hexdigest()[:16]
    
    async def _persist_patterns(self, agent_id: str):
        """Persist patterns to disk"""
        try:
            file_path = self.storage_path / f"{agent_id}_patterns.json"
            
            # Prepare data
            data = {
                'agent_id': agent_id,
                'patterns': self.pattern_cache[agent_id][-1000:],  # Keep last 1000
                'stats': {},
                'last_updated': datetime.utcnow().isoformat()
            }
            
            # Add stats for patterns
            for pattern in data['patterns']:
                pattern_id = self._generate_pattern_id(pattern)
                data['stats'][pattern_id] = self.pattern_stats[pattern_id]
            
            # Write atomically
            temp_file = file_path.with_suffix('.tmp')
            async with aiofiles.open(temp_file, 'w') as f:
                await f.write(json.dumps(data, indent=2))
            
            # Atomic rename
            temp_file.rename(file_path)
            
        except Exception as e:
            logger.error(f"Failed to persist patterns: {e}")
    
    def _clear_relevance_cache(self, agent_id: str):
        """Clear relevance cache for an agent"""
        keys_to_remove = [
            key for key in self.relevance_cache.keys()
            if key[0] == agent_id
        ]
        for key in keys_to_remove:
            del self.relevance_cache[key]
            self.cache_timestamps.pop(key, None)
    
    async def cleanup_old_patterns(self, days: int = 30):
        """Remove patterns older than specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        for agent_id, patterns in self.pattern_cache.items():
            # Filter patterns
            kept_patterns = []
            for pattern in patterns:
                pattern_id = self._generate_pattern_id(pattern)
                stats = self.pattern_stats.get(pattern_id, {})
                
                last_used_str = stats.get('last_used')
                if last_used_str:
                    last_used = datetime.fromisoformat(last_used_str)
                    if last_used > cutoff_date or stats.get('success_rate', 0) > 0.8:
                        kept_patterns.append(pattern)
                else:
                    kept_patterns.append(pattern)
            
            # Update cache
            self.pattern_cache[agent_id] = kept_patterns
            
            # Persist cleaned data
            await self._persist_patterns(agent_id)
        
        logger.info(f"Cleaned up patterns older than {days} days")
