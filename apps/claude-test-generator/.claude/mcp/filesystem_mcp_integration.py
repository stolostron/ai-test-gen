#!/usr/bin/env python3
"""
File System MCP Integration Service for claude-test-generator

Provides MCP-style file system operations with semantic search capabilities.
Enhances QE Intelligence Service and Pattern Extension Service with advanced
file discovery and pattern analysis beyond basic grep/find commands.

This leverages existing file system permissions while adding intelligence.
"""

import os
import sys
import json
import re
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional, Any, Generator
from datetime import datetime
import subprocess
import fnmatch

class FileSystemMCPIntegration:
    """File System MCP-style integration with semantic search capabilities"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path).resolve()
        self.cache = {}
        self.last_scan_time = None
        
    def search_files(self, pattern: str = "*", 
                    semantic_search: bool = False,
                    file_types: List[str] = None,
                    max_results: int = 1000,
                    include_content: bool = False) -> Dict:
        """Advanced file search with semantic capabilities"""
        try:
            results = []
            search_paths = []
            
            # Use glob pattern matching
            if semantic_search:
                # Semantic search - interpret patterns intelligently
                search_patterns = self._generate_semantic_patterns(pattern)
            else:
                search_patterns = [pattern]
            
            for search_pattern in search_patterns:
                for file_path in self.base_path.rglob(search_pattern):
                    if file_path.is_file():
                        # Filter by file types if specified
                        if file_types and not any(file_path.suffix.lower() in [f'.{ft.lower()}' for ft in file_types]):
                            continue
                        
                        file_info = self._get_file_info(file_path, include_content)
                        results.append(file_info)
                        
                        if len(results) >= max_results:
                            break
            
            return {
                "files_found": len(results),
                "results": results,
                "patterns_used": search_patterns,
                "base_path": str(self.base_path),
                "meta": {
                    "searched_at": datetime.now().isoformat(),
                    "semantic_search": semantic_search,
                    "file_types_filter": file_types
                }
            }
            
        except Exception as e:
            return {"error": str(e), "fallback_to_find": True}
    
    def grep_with_context(self, pattern: str, 
                         file_pattern: str = "*",
                         context_lines: int = 3,
                         case_sensitive: bool = False,
                         regex_mode: bool = True) -> Dict:
        """Enhanced grep with intelligent context and pattern matching"""
        try:
            results = []
            flags = re.IGNORECASE if not case_sensitive else 0
            
            if regex_mode:
                compiled_pattern = re.compile(pattern, flags)
            else:
                compiled_pattern = re.compile(re.escape(pattern), flags)
            
            # Find files matching file pattern
            file_search = self.search_files(file_pattern, max_results=500)
            
            for file_info in file_search.get("results", []):
                file_path = Path(file_info["path"])
                
                # Skip binary files
                if not self._is_text_file(file_path):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    
                    matches = []
                    for line_num, line in enumerate(lines, 1):
                        if compiled_pattern.search(line):
                            # Extract context
                            start_line = max(0, line_num - context_lines - 1)
                            end_line = min(len(lines), line_num + context_lines)
                            
                            context = {
                                "line_number": line_num,
                                "matched_line": line.strip(),
                                "context_before": [lines[i].strip() for i in range(start_line, line_num - 1)],
                                "context_after": [lines[i].strip() for i in range(line_num, end_line)]
                            }
                            matches.append(context)
                    
                    if matches:
                        results.append({
                            "file": str(file_path.relative_to(self.base_path)),
                            "matches_count": len(matches),
                            "matches": matches
                        })
                
                except Exception as file_error:
                    continue  # Skip files that can't be read
            
            return {
                "files_with_matches": len(results),
                "total_matches": sum(r["matches_count"] for r in results),
                "results": results,
                "pattern": pattern,
                "meta": {
                    "searched_at": datetime.now().isoformat(),
                    "context_lines": context_lines,
                    "case_sensitive": case_sensitive,
                    "regex_mode": regex_mode
                }
            }
            
        except Exception as e:
            return {"error": str(e), "fallback_to_grep": True}
    
    def analyze_directory_structure(self, path: str = ".", 
                                  max_depth: int = 3,
                                  include_stats: bool = True) -> Dict:
        """Analyze directory structure for pattern recognition"""
        try:
            target_path = Path(path) if path != "." else self.base_path
            structure = self._build_directory_tree(target_path, max_depth, include_stats)
            
            # Analysis insights
            insights = self._analyze_project_structure(structure)
            
            return {
                "directory_tree": structure,
                "insights": insights,
                "meta": {
                    "analyzed_at": datetime.now().isoformat(),
                    "base_path": str(target_path),
                    "max_depth": max_depth
                }
            }
            
        except Exception as e:
            return {"error": str(e), "fallback_to_find": True}
    
    def find_test_patterns(self, 
                          test_dirs: List[str] = None,
                          test_patterns: List[str] = None) -> Dict:
        """Specialized method for QE Intelligence - find test file patterns"""
        try:
            if test_dirs is None:
                test_dirs = ["test", "tests", "spec", "cypress", "e2e", "__tests__"]
            
            if test_patterns is None:
                test_patterns = ["*.test.*", "*.spec.*", "*.cy.*", "*_test.*", "test_*.py"]
            
            test_files = []
            patterns_found = {}
            
            # Search in likely test directories
            for test_dir in test_dirs:
                test_dir_path = self.base_path / test_dir
                if test_dir_path.exists() and test_dir_path.is_dir():
                    for pattern in test_patterns:
                        files = list(test_dir_path.rglob(pattern))
                        for file_path in files:
                            if file_path.is_file():
                                test_info = self._analyze_test_file(file_path)
                                test_files.append(test_info)
                                
                                # Track patterns
                                pattern_key = f"{test_dir}/{pattern}"
                                patterns_found[pattern_key] = patterns_found.get(pattern_key, 0) + 1
            
            # Also search root directory for test files
            for pattern in test_patterns:
                for file_path in self.base_path.rglob(pattern):
                    if file_path.is_file():
                        # Avoid duplicates from test directories
                        relative_path = file_path.relative_to(self.base_path)
                        if not any(part in test_dirs for part in relative_path.parts):
                            test_info = self._analyze_test_file(file_path)
                            test_files.append(test_info)
            
            return {
                "test_files_found": len(test_files),
                "test_files": test_files,
                "patterns_found": patterns_found,
                "insights": self._generate_test_insights(test_files),
                "meta": {
                    "analyzed_at": datetime.now().isoformat(),
                    "search_directories": test_dirs,
                    "search_patterns": test_patterns
                }
            }
            
        except Exception as e:
            return {"error": str(e), "fallback_to_find": True}
    
    def cache_file_content(self, file_paths: List[str], 
                          content_type: str = "pattern_analysis") -> Dict:
        """Intelligent file content caching for repeated pattern analysis"""
        try:
            cached_content = {}
            cache_stats = {"hits": 0, "misses": 0, "errors": 0}
            
            for file_path_str in file_paths:
                file_path = Path(file_path_str)
                cache_key = f"{content_type}:{file_path}:{file_path.stat().st_mtime}"
                
                if cache_key in self.cache:
                    cached_content[file_path_str] = self.cache[cache_key]
                    cache_stats["hits"] += 1
                else:
                    try:
                        content = self._extract_file_content(file_path, content_type)
                        self.cache[cache_key] = content
                        cached_content[file_path_str] = content
                        cache_stats["misses"] += 1
                    except Exception:
                        cache_stats["errors"] += 1
            
            return {
                "cached_files": len(cached_content),
                "content": cached_content,
                "cache_stats": cache_stats,
                "meta": {
                    "cached_at": datetime.now().isoformat(),
                    "content_type": content_type
                }
            }
            
        except Exception as e:
            return {"error": str(e), "fallback_available": True}
    
    def _generate_semantic_patterns(self, pattern: str) -> List[str]:
        """Generate intelligent search patterns from semantic input"""
        patterns = [pattern]  # Start with original
        
        # Common semantic mappings
        semantic_map = {
            "test": ["*test*", "*spec*", "*.test.*", "*.spec.*"],
            "config": ["*config*", "*.conf", "*.ini", "*.yaml", "*.yml", "*.json"],
            "source": ["*.py", "*.js", "*.go", "*.java", "*.cpp", "*.c"],
            "documentation": ["*.md", "*.rst", "*.txt", "*README*", "*CHANGELOG*"],
            "cypress": ["*.cy.*", "*cypress*", "cypress/**/*"],
            "yaml": ["*.yaml", "*.yml"],
            "javascript": ["*.js", "*.jsx", "*.ts", "*.tsx"],
            "python": ["*.py", "*__pycache__*"],
            "go": ["*.go", "go.mod", "go.sum"]
        }
        
        pattern_lower = pattern.lower()
        for key, file_patterns in semantic_map.items():
            if key in pattern_lower:
                patterns.extend(file_patterns)
        
        return list(set(patterns))  # Remove duplicates
    
    def _get_file_info(self, file_path: Path, include_content: bool = False) -> Dict:
        """Get comprehensive file information"""
        try:
            stat = file_path.stat()
            info = {
                "path": str(file_path),
                "relative_path": str(file_path.relative_to(self.base_path)),
                "name": file_path.name,
                "extension": file_path.suffix,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "is_text": self._is_text_file(file_path)
            }
            
            if include_content and info["is_text"] and stat.st_size < 1024 * 1024:  # < 1MB
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        info["content"] = f.read()
                except:
                    info["content"] = None
            
            return info
        except Exception:
            return {"path": str(file_path), "error": "Could not read file info"}
    
    def _is_text_file(self, file_path: Path) -> bool:
        """Determine if file is text-based"""
        if file_path.suffix.lower() in ['.py', '.js', '.go', '.java', '.cpp', '.c', '.h', 
                                       '.yaml', '.yml', '.json', '.md', '.txt', '.rst',
                                       '.sh', '.bash', '.zsh', '.ps1', '.html', '.css',
                                       '.xml', '.csv', '.sql', '.conf', '.ini', '.toml']:
            return True
        
        try:
            mime_type, _ = mimetypes.guess_type(str(file_path))
            return mime_type and mime_type.startswith('text/')
        except:
            return False
    
    def _build_directory_tree(self, path: Path, max_depth: int, include_stats: bool, current_depth: int = 0) -> Dict:
        """Build directory tree structure"""
        if current_depth >= max_depth:
            return {"truncated": True}
        
        tree = {
            "name": path.name,
            "path": str(path.relative_to(self.base_path)),
            "type": "directory",
            "children": []
        }
        
        if include_stats:
            try:
                items = list(path.iterdir())
                tree["file_count"] = len([i for i in items if i.is_file()])
                tree["dir_count"] = len([i for i in items if i.is_dir()])
            except:
                tree["file_count"] = 0
                tree["dir_count"] = 0
        
        try:
            for item in sorted(path.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    child_tree = self._build_directory_tree(item, max_depth, include_stats, current_depth + 1)
                    tree["children"].append(child_tree)
                elif item.is_file() and current_depth < 2:  # Only show files in shallow directories
                    tree["children"].append({
                        "name": item.name,
                        "path": str(item.relative_to(self.base_path)),
                        "type": "file",
                        "extension": item.suffix
                    })
        except PermissionError:
            tree["error"] = "Permission denied"
        
        return tree
    
    def _analyze_project_structure(self, structure: Dict) -> Dict:
        """Analyze project structure for insights"""
        insights = {
            "project_type": "unknown",
            "test_directories": [],
            "config_files": [],
            "languages_detected": [],
            "framework_indicators": []
        }
        
        def traverse(node):
            if node.get("type") == "directory":
                name = node.get("name", "").lower()
                # Detect test directories
                if any(test_word in name for test_word in ["test", "spec", "cypress", "e2e"]):
                    insights["test_directories"].append(node.get("path"))
                
                # Recurse into children
                for child in node.get("children", []):
                    traverse(child)
            
            elif node.get("type") == "file":
                name = node.get("name", "").lower()
                ext = node.get("extension", "").lower()
                
                # Detect languages
                lang_map = {
                    ".py": "python", ".js": "javascript", ".ts": "typescript",
                    ".go": "go", ".java": "java", ".cpp": "cpp", ".c": "c"
                }
                if ext in lang_map:
                    lang = lang_map[ext]
                    if lang not in insights["languages_detected"]:
                        insights["languages_detected"].append(lang)
                
                # Detect config files
                if any(config_word in name for config_word in ["config", "package.json", "go.mod", "requirements.txt"]):
                    insights["config_files"].append(node.get("path"))
                
                # Detect frameworks
                if "package.json" in name:
                    insights["framework_indicators"].append("node.js")
                elif "go.mod" in name:
                    insights["framework_indicators"].append("go_modules")
                elif "requirements.txt" in name or "setup.py" in name:
                    insights["framework_indicators"].append("python")
        
        traverse(structure)
        
        # Determine primary project type
        if "node.js" in insights["framework_indicators"]:
            insights["project_type"] = "node.js"
        elif "go_modules" in insights["framework_indicators"]:
            insights["project_type"] = "go"
        elif "python" in insights["framework_indicators"]:
            insights["project_type"] = "python"
        elif insights["languages_detected"]:
            insights["project_type"] = insights["languages_detected"][0]
        
        return insights
    
    def _analyze_test_file(self, file_path: Path) -> Dict:
        """Analyze individual test file for patterns"""
        info = {
            "path": str(file_path.relative_to(self.base_path)),
            "name": file_path.name,
            "type": "unknown",
            "framework": "unknown",
            "test_count_estimate": 0,
            "patterns": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Detect test framework
            if '.cy.' in file_path.name or 'cypress' in str(file_path):
                info["framework"] = "cypress"
                info["type"] = "e2e"
            elif '.spec.' in file_path.name:
                info["framework"] = "spec"
                info["type"] = "unit_or_integration"
            elif '.test.' in file_path.name:
                info["framework"] = "test"
                info["type"] = "unit_or_integration"
            
            # Count test patterns
            test_patterns = [
                r'test\s*\(',
                r'it\s*\(',
                r'describe\s*\(',
                r'def\s+test_',
                r'func\s+Test\w+'
            ]
            
            for pattern in test_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                info["test_count_estimate"] += len(matches)
                if matches:
                    info["patterns"].append(pattern)
            
            # Extract some test names
            test_names = re.findall(r'(?:test|it|describe)\s*\(\s*[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
            info["sample_test_names"] = test_names[:5]  # First 5 test names
            
        except Exception:
            info["error"] = "Could not analyze file content"
        
        return info
    
    def _generate_test_insights(self, test_files: List[Dict]) -> Dict:
        """Generate insights from test file analysis"""
        insights = {
            "total_files": len(test_files),
            "frameworks_used": {},
            "test_types": {},
            "estimated_total_tests": 0,
            "file_naming_patterns": [],
            "common_test_names": []
        }
        
        all_test_names = []
        
        for test_file in test_files:
            # Count frameworks
            framework = test_file.get("framework", "unknown")
            insights["frameworks_used"][framework] = insights["frameworks_used"].get(framework, 0) + 1
            
            # Count test types
            test_type = test_file.get("type", "unknown")
            insights["test_types"][test_type] = insights["test_types"].get(test_type, 0) + 1
            
            # Sum estimated tests
            insights["estimated_total_tests"] += test_file.get("test_count_estimate", 0)
            
            # Collect test names
            all_test_names.extend(test_file.get("sample_test_names", []))
            
            # Analyze naming patterns
            name = test_file.get("name", "")
            if ".cy." in name:
                insights["file_naming_patterns"].append("cypress")
            elif ".spec." in name:
                insights["file_naming_patterns"].append("spec")
            elif ".test." in name:
                insights["file_naming_patterns"].append("test")
        
        # Find common test name patterns
        test_name_words = []
        for name in all_test_names:
            words = re.findall(r'\w+', name.lower())
            test_name_words.extend(words)
        
        # Count word frequency
        word_count = {}
        for word in test_name_words:
            if len(word) > 3:  # Skip short words
                word_count[word] = word_count.get(word, 0) + 1
        
        # Get most common words
        insights["common_test_names"] = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Remove duplicates from patterns
        insights["file_naming_patterns"] = list(set(insights["file_naming_patterns"]))
        
        return insights
    
    def _extract_file_content(self, file_path: Path, content_type: str) -> Dict:
        """Extract and process file content based on type"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if content_type == "pattern_analysis":
                # Extract key patterns for pattern analysis
                return {
                    "imports": re.findall(r'^(?:import|from|#include)\s+(.+)', content, re.MULTILINE),
                    "functions": re.findall(r'(?:def|function|func)\s+(\w+)', content),
                    "classes": re.findall(r'(?:class|type)\s+(\w+)', content),
                    "comments": re.findall(r'//\s*(.+)|#\s*(.+)', content),
                    "line_count": len(content.splitlines())
                }
            else:
                return {"content": content}
                
        except Exception as e:
            return {"error": str(e)}
    
    def test_connection(self) -> Dict:
        """Test file system access and permissions"""
        try:
            # Test basic operations
            test_results = {
                "base_path_readable": os.access(self.base_path, os.R_OK),
                "base_path_writable": os.access(self.base_path, os.W_OK),
                "current_directory": str(self.base_path),
                "total_files": 0,
                "total_directories": 0
            }
            
            # Quick count
            for item in self.base_path.rglob("*"):
                if item.is_file():
                    test_results["total_files"] += 1
                elif item.is_dir():
                    test_results["total_directories"] += 1
                
                # Limit counting to avoid long operations
                if test_results["total_files"] + test_results["total_directories"] > 1000:
                    test_results["count_limited"] = True
                    break
            
            return {
                "status": "connected",
                "capabilities": ["search", "grep", "analyze", "cache"],
                "test_results": test_results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "fallback_available": True
            }

def main():
    """CLI interface for testing File System MCP integration"""
    if len(sys.argv) < 2:
        print("Usage: python filesystem_mcp_integration.py <command> [args...]")
        print("Commands: test, search <pattern>, grep <pattern> [file_pattern], tests")
        return
    
    fs = FileSystemMCPIntegration()
    command = sys.argv[1]
    
    if command == "test":
        result = fs.test_connection()
        print(json.dumps(result, indent=2))
    
    elif command == "search" and len(sys.argv) >= 3:
        pattern = sys.argv[2]
        semantic = len(sys.argv) > 3 and sys.argv[3] == "--semantic"
        result = fs.search_files(pattern, semantic_search=semantic)
        print(json.dumps(result, indent=2, default=str))
    
    elif command == "grep" and len(sys.argv) >= 3:
        pattern = sys.argv[2]
        file_pattern = sys.argv[3] if len(sys.argv) > 3 else "*"
        result = fs.grep_with_context(pattern, file_pattern)
        print(json.dumps(result, indent=2, default=str))
    
    elif command == "tests":
        result = fs.find_test_patterns()
        print(json.dumps(result, indent=2, default=str))
    
    else:
        print("Invalid command or arguments")

if __name__ == "__main__":
    main()