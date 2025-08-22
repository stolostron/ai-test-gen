#!/usr/bin/env python3
"""
Optimized File System MCP Integration - Performance Enhanced Version

Provides fast file system operations with intelligent metadata collection.
Optimizes for speed while maintaining enhanced capabilities when needed.
"""

import os
import glob
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class OptimizedFileSystemMCPIntegration:
    """Performance-optimized File System MCP integration"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path).resolve()
        # Minimal initialization - no expensive setup
        
    def search_files(self, pattern: str = "*", 
                    semantic_search: bool = False,
                    minimal_metadata: bool = True,
                    max_results: int = 1000) -> Dict:
        """Optimized file search with optional metadata collection"""
        try:
            if semantic_search:
                search_patterns = self._generate_semantic_patterns_fast(pattern)
            else:
                search_patterns = [pattern]
            
            results = []
            
            if minimal_metadata:
                # Fast path: minimal metadata (like glob but with structure)
                for search_pattern in search_patterns:
                    # Use fast glob for basic patterns
                    if not ('**' in search_pattern or search_pattern.startswith('**/')):
                        # Simple pattern - use glob
                        files = glob.glob(str(self.base_path / search_pattern))
                        for file_path in files[:max_results]:
                            if os.path.isfile(file_path):
                                results.append({
                                    "path": file_path,
                                    "relative_path": os.path.relpath(file_path, self.base_path),
                                    "name": os.path.basename(file_path)
                                })
                    else:
                        # Complex pattern - use rglob
                        for file_path in self.base_path.rglob(search_pattern):
                            if file_path.is_file() and len(results) < max_results:
                                results.append({
                                    "path": str(file_path),
                                    "relative_path": str(file_path.relative_to(self.base_path)),
                                    "name": file_path.name
                                })
            else:
                # Full metadata path (slower but comprehensive)
                for search_pattern in search_patterns:
                    for file_path in self.base_path.rglob(search_pattern):
                        if file_path.is_file() and len(results) < max_results:
                            results.append(self._get_file_info_fast(file_path))
            
            return {
                "files_found": len(results),
                "results": results,
                "patterns_used": search_patterns,
                "base_path": str(self.base_path),
                "meta": {
                    "searched_at": datetime.now().isoformat(),
                    "semantic_search": semantic_search,
                    "minimal_metadata": minimal_metadata
                }
            }
            
        except Exception as e:
            return {"error": str(e), "fallback_to_find": True}
    
    def _generate_semantic_patterns_fast(self, pattern: str) -> List[str]:
        """Fast semantic pattern generation with reduced mappings"""
        patterns = [pattern]
        
        # Simplified semantic mappings for common cases
        if "test" in pattern.lower():
            patterns.extend(["*test*", "*spec*"])
        elif "config" in pattern.lower():
            patterns.extend(["*.json", "*.yaml", "*.yml"])
        elif pattern.startswith("tg_") or pattern.startswith("tg-"):
            patterns.append(pattern.replace("_", "-"))
            patterns.append(pattern.replace("-", "_"))
        
        return list(set(patterns))
    
    def _get_file_info_fast(self, file_path: Path) -> Dict:
        """Fast file info collection with minimal system calls"""
        try:
            # Single stat call for all needed info
            stat = file_path.stat()
            
            return {
                "path": str(file_path),
                "relative_path": str(file_path.relative_to(self.base_path)),
                "name": file_path.name,
                "extension": file_path.suffix,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                # Skip expensive text detection for speed
                "is_text": file_path.suffix.lower() in {
                    '.py', '.js', '.go', '.java', '.md', '.txt', '.json', 
                    '.yaml', '.yml', '.sh', '.html', '.css', '.xml'
                }
            }
        except:
            # Fallback to minimal info
            return {
                "path": str(file_path),
                "relative_path": str(file_path.relative_to(self.base_path)),
                "name": file_path.name
            }
    
    def grep_with_context(self, pattern: str, 
                         file_pattern: str = "*",
                         context_lines: int = 3,
                         fast_mode: bool = True) -> Dict:
        """Optimized grep with optional full context"""
        try:
            if fast_mode:
                # Use system grep for speed
                import subprocess
                cmd = ['grep', '-r', '-n', pattern, str(self.base_path), '--include', file_pattern]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                matches = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        matches.append({"match": line})
                
                return {
                    "matches_found": len(matches),
                    "results": matches[:100],  # Limit for performance
                    "method": "system_grep_fast"
                }
            else:
                # Full Python implementation for advanced features
                return self._grep_python_implementation(pattern, file_pattern, context_lines)
                
        except Exception as e:
            return {"error": str(e), "fallback_available": True}
    
    def _grep_python_implementation(self, pattern: str, file_pattern: str, context_lines: int) -> Dict:
        """Python grep implementation for advanced features"""
        # Simplified implementation focusing on speed
        results = []
        file_search = self.search_files(file_pattern, minimal_metadata=True, max_results=100)
        
        import re
        compiled_pattern = re.compile(pattern, re.IGNORECASE)
        
        for file_info in file_search.get("results", []):
            file_path = Path(file_info["path"])
            
            # Quick text file check
            if file_path.suffix.lower() not in {'.py', '.js', '.go', '.md', '.txt', '.json', '.yaml', '.yml'}:
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines):
                    if compiled_pattern.search(line):
                        results.append({
                            "file": str(file_path),
                            "line_number": line_num + 1,
                            "content": line.strip(),
                            "context": self._get_context_lines(lines, line_num, context_lines)
                        })
                        
                        if len(results) >= 50:  # Limit for performance
                            break
                            
            except Exception:
                continue  # Skip problematic files
                
        return {
            "matches_found": len(results),
            "results": results,
            "method": "python_grep_full"
        }
    
    def _get_context_lines(self, lines: List[str], line_num: int, context_lines: int) -> Dict:
        """Get context lines around match"""
        start = max(0, line_num - context_lines)
        end = min(len(lines), line_num + context_lines + 1)
        
        return {
            "before": [lines[i].strip() for i in range(start, line_num)],
            "after": [lines[i].strip() for i in range(line_num + 1, end)]
        }
    
    def find_test_patterns(self, test_dirs: List[str] = None, fast_mode: bool = True) -> Dict:
        """Fast test pattern finding"""
        try:
            if fast_mode:
                # Use glob for speed
                test_patterns = ['*test*', '*spec*', '*.test.*', '*.spec.*']
                test_files = []
                
                for pattern in test_patterns:
                    files = glob.glob(str(self.base_path / '**' / pattern), recursive=True)
                    for file_path in files:
                        if os.path.isfile(file_path):
                            test_files.append({
                                "path": file_path,
                                "type": self._detect_test_type_fast(file_path)
                            })
                
                return {
                    "test_files_found": len(test_files),
                    "test_files": test_files[:50],  # Limit for performance
                    "method": "glob_fast_scan"
                }
            else:
                # Full implementation with detailed analysis
                return self.search_files("*test*", semantic_search=True, minimal_metadata=False)
                
        except Exception as e:
            return {"error": str(e)}
    
    def _detect_test_type_fast(self, file_path: str) -> str:
        """Fast test type detection"""
        file_lower = file_path.lower()
        
        if 'cypress' in file_lower or '.cy.' in file_lower:
            return 'cypress'
        elif 'spec' in file_lower:
            return 'spec'
        elif 'test' in file_lower:
            return 'unit_test'
        else:
            return 'unknown'
    
    def test_connection(self) -> Dict:
        """Test connection and performance"""
        try:
            start_time = time.time()
            
            # Quick test
            result = self.search_files("*.md", minimal_metadata=True, max_results=10)
            
            test_time = (time.time() - start_time) * 1000
            
            return {
                "status": "connected",
                "performance": f"{test_time:.2f}ms",
                "files_found": result.get("files_found", 0),
                "optimization": "enabled"
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

# Performance testing function
def compare_performance():
    """Compare optimized vs original performance"""
    import time
    
    print("🏃 Performance Comparison Test")
    print("=" * 40)
    
    # Test original glob
    start = time.time()
    files = glob.glob(".claude/ai-services/*.md")
    glob_time = (time.time() - start) * 1000
    print(f"Glob baseline: {glob_time:.2f}ms ({len(files)} files)")
    
    # Test optimized MCP
    optimized = OptimizedFileSystemMCPIntegration(".")
    start = time.time()
    result = optimized.search_files("*.md", minimal_metadata=True)
    optimized_time = (time.time() - start) * 1000
    print(f"Optimized MCP: {optimized_time:.2f}ms ({result.get('files_found', 0)} files)")
    
    print(f"Performance ratio: {optimized_time/glob_time:.1f}x")
    
    if optimized_time < glob_time * 3:  # Within 3x is acceptable
        print("✅ Performance acceptable")
    else:
        print("⚠️ Performance needs improvement")

if __name__ == "__main__":
    compare_performance()