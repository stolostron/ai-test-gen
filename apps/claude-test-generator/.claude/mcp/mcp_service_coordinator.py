#!/usr/bin/env python3
"""
MCP Service Coordinator for claude-test-generator

Centralized coordinator for GitHub and File System MCP integrations.
Provides unified interface for all MCP operations with intelligent fallback
and performance optimization for the framework's AI services.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import importlib.util

class MCPServiceCoordinator:
    """Central coordinator for all MCP services"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.config_path = self.base_path / ".claude/config/mcp-integration-config.json"
        self.config = self._load_config()
        
        # Initialize MCP services
        self.github_mcp = None
        self.filesystem_mcp = None
        self._initialize_services()
        
        # Performance tracking
        self.performance_stats = {
            "github_calls": 0,
            "filesystem_calls": 0,
            "fallback_activations": 0,
            "cache_hits": 0,
            "total_time_saved": 0.0
        }
    
    def _load_config(self) -> Dict:
        """Load MCP integration configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception:
            return {"mcp_integration": {"enabled": False}}
    
    def _initialize_services(self):
        """Initialize available MCP services"""
        try:
            # Initialize GitHub MCP if enabled
            if self.config.get("mcp_integration", {}).get("github_mcp", {}).get("enabled", False):
                github_module_path = self.base_path / ".claude/mcp/github_mcp_integration.py"
                if github_module_path.exists():
                    spec = importlib.util.spec_from_file_location("github_mcp", github_module_path)
                    github_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(github_module)
                    self.github_mcp = github_module.GitHubMCPIntegration()
            
            # Initialize File System MCP if enabled
            if self.config.get("mcp_integration", {}).get("filesystem_mcp", {}).get("enabled", False):
                fs_module_path = self.base_path / ".claude/mcp/filesystem_mcp_integration.py"
                if fs_module_path.exists():
                    spec = importlib.util.spec_from_file_location("filesystem_mcp", fs_module_path)
                    fs_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(fs_module)
                    self.filesystem_mcp = fs_module.FileSystemMCPIntegration(str(self.base_path))
                    
        except Exception as e:
            print(f"Warning: MCP service initialization error: {e}")
    
    # GitHub MCP Operations
    def github_get_pull_request(self, repo: str, pr_number: int, use_fallback: bool = True) -> Dict:
        """Get PR information with MCP enhancement"""
        self.performance_stats["github_calls"] += 1
        
        if self.github_mcp:
            try:
                result = self.github_mcp.get_pull_request(repo, pr_number)
                if "error" in result and use_fallback:
                    return self._github_cli_fallback("pr", repo, pr_number)
                return result
            except Exception as e:
                if use_fallback:
                    self.performance_stats["fallback_activations"] += 1
                    return self._github_cli_fallback("pr", repo, pr_number)
                return {"error": str(e)}
        elif use_fallback:
            return self._github_cli_fallback("pr", repo, pr_number)
        else:
            return {"error": "GitHub MCP not available"}
    
    def github_search_pull_requests(self, repo: str, query: str = "", use_fallback: bool = True) -> Dict:
        """Search PRs with MCP enhancement"""
        self.performance_stats["github_calls"] += 1
        
        if self.github_mcp:
            try:
                result = self.github_mcp.search_pull_requests(repo, query)
                if "error" in result and use_fallback:
                    return self._github_cli_fallback("search", repo, query)
                return result
            except Exception as e:
                if use_fallback:
                    self.performance_stats["fallback_activations"] += 1
                    return self._github_cli_fallback("search", repo, query)
                return {"error": str(e)}
        elif use_fallback:
            return self._github_cli_fallback("search", repo, query)
        else:
            return {"error": "GitHub MCP not available"}
    
    def github_analyze_pr_timeline(self, repo: str, pr_numbers: List[int], use_fallback: bool = True) -> Dict:
        """Advanced PR timeline analysis (MCP-only feature)"""
        self.performance_stats["github_calls"] += 1
        
        if self.github_mcp:
            try:
                return self.github_mcp.analyze_pr_timeline(repo, pr_numbers)
            except Exception as e:
                return {"error": str(e), "fallback_available": False}
        else:
            return {"error": "GitHub MCP not available - advanced timeline analysis requires MCP"}
    
    # File System MCP Operations
    def filesystem_search_files(self, pattern: str, semantic_search: bool = False, 
                               file_types: List[str] = None, use_fallback: bool = True) -> Dict:
        """Enhanced file search with semantic capabilities"""
        self.performance_stats["filesystem_calls"] += 1
        
        if self.filesystem_mcp:
            try:
                return self.filesystem_mcp.search_files(pattern, semantic_search, file_types)
            except Exception as e:
                if use_fallback:
                    self.performance_stats["fallback_activations"] += 1
                    return self._filesystem_fallback("find", pattern)
                return {"error": str(e)}
        elif use_fallback:
            return self._filesystem_fallback("find", pattern)
        else:
            return {"error": "File System MCP not available"}
    
    def filesystem_grep_with_context(self, pattern: str, file_pattern: str = "*",
                                   context_lines: int = 3, use_fallback: bool = True) -> Dict:
        """Enhanced grep with context and intelligence"""
        self.performance_stats["filesystem_calls"] += 1
        
        if self.filesystem_mcp:
            try:
                return self.filesystem_mcp.grep_with_context(pattern, file_pattern, context_lines)
            except Exception as e:
                if use_fallback:
                    self.performance_stats["fallback_activations"] += 1
                    return self._filesystem_fallback("grep", pattern, file_pattern)
                return {"error": str(e)}
        elif use_fallback:
            return self._filesystem_fallback("grep", pattern, file_pattern)
        else:
            return {"error": "File System MCP not available"}
    
    def filesystem_find_test_patterns(self, test_dirs: List[str] = None, use_fallback: bool = True) -> Dict:
        """Specialized test pattern finding (MCP-enhanced feature)"""
        self.performance_stats["filesystem_calls"] += 1
        
        if self.filesystem_mcp:
            try:
                return self.filesystem_mcp.find_test_patterns(test_dirs)
            except Exception as e:
                if use_fallback:
                    self.performance_stats["fallback_activations"] += 1
                    return self._filesystem_fallback("test_search")
                return {"error": str(e)}
        elif use_fallback:
            return self._filesystem_fallback("test_search")
        else:
            return {"error": "File System MCP not available"}
    
    def filesystem_cache_content(self, file_paths: List[str], content_type: str = "pattern_analysis") -> Dict:
        """Intelligent content caching (MCP-only feature)"""
        self.performance_stats["filesystem_calls"] += 1
        
        if self.filesystem_mcp:
            try:
                result = self.filesystem_mcp.cache_file_content(file_paths, content_type)
                if result.get("cache_stats", {}).get("hits", 0) > 0:
                    self.performance_stats["cache_hits"] += result["cache_stats"]["hits"]
                return result
            except Exception as e:
                return {"error": str(e), "fallback_available": False}
        else:
            return {"error": "File System MCP not available - caching requires MCP"}
    
    # Fallback Methods
    def _github_cli_fallback(self, operation: str, *args) -> Dict:
        """Fallback to GitHub CLI operations"""
        import subprocess
        
        try:
            if operation == "pr":
                repo, pr_number = args
                result = subprocess.run(['gh', 'pr', 'view', str(pr_number), 
                                       '--repo', repo, '--json', 'title,body,state,url'],
                                      capture_output=True, text=True, check=True)
                data = json.loads(result.stdout)
                return {
                    "pr_info": data,
                    "source": "github_cli_fallback",
                    "fallback_reason": "mcp_unavailable_or_failed"
                }
            
            elif operation == "search":
                repo, query = args
                result = subprocess.run(['gh', 'search', 'prs', '--repo', repo, 
                                       '--limit', '20', '--json', 'title,url,state'],
                                      capture_output=True, text=True, check=True)
                data = json.loads(result.stdout)
                return {
                    "pull_requests": data,
                    "source": "github_cli_fallback",
                    "fallback_reason": "mcp_unavailable_or_failed"
                }
            
        except Exception as e:
            return {"error": f"GitHub CLI fallback failed: {e}"}
    
    def _filesystem_fallback(self, operation: str, *args) -> Dict:
        """Fallback to basic file system operations"""
        import subprocess
        import glob
        
        try:
            if operation == "find":
                pattern = args[0]
                files = glob.glob(f"**/{pattern}", recursive=True)
                return {
                    "files_found": len(files),
                    "results": [{"path": f, "source": "glob_fallback"} for f in files[:100]],
                    "source": "filesystem_fallback",
                    "fallback_reason": "mcp_unavailable_or_failed"
                }
            
            elif operation == "grep":
                pattern, file_pattern = args[0], args[1] if len(args) > 1 else "*"
                result = subprocess.run(['grep', '-r', '-n', pattern, '.', '--include', file_pattern],
                                      capture_output=True, text=True)
                matches = result.stdout.strip().split('\n') if result.stdout else []
                return {
                    "matches_found": len(matches),
                    "results": [{"match": m} for m in matches[:50]],
                    "source": "grep_fallback",
                    "fallback_reason": "mcp_unavailable_or_failed"
                }
            
            elif operation == "test_search":
                test_files = glob.glob("**/*test*", recursive=True) + \
                           glob.glob("**/*spec*", recursive=True)
                return {
                    "test_files_found": len(test_files),
                    "test_files": [{"path": f} for f in test_files[:20]],
                    "source": "glob_fallback",
                    "fallback_reason": "mcp_unavailable_or_failed"
                }
                
        except Exception as e:
            return {"error": f"File system fallback failed: {e}"}
    
    # Coordination Methods
    def get_service_status(self) -> Dict:
        """Get status of all MCP services"""
        return {
            "github_mcp": {
                "available": self.github_mcp is not None,
                "enabled": self.config.get("mcp_integration", {}).get("github_mcp", {}).get("enabled", False),
                "status": self.config.get("mcp_integration", {}).get("github_mcp", {}).get("status", "unknown")
            },
            "filesystem_mcp": {
                "available": self.filesystem_mcp is not None,
                "enabled": self.config.get("mcp_integration", {}).get("filesystem_mcp", {}).get("enabled", False),
                "status": self.config.get("mcp_integration", {}).get("filesystem_mcp", {}).get("status", "unknown")
            },
            "performance_stats": self.performance_stats,
            "coordinator_status": "operational"
        }
    
    def test_all_services(self) -> Dict:
        """Test all available MCP services"""
        results = {}
        
        # Test GitHub MCP
        if self.github_mcp:
            try:
                results["github_mcp"] = self.github_mcp.test_connection()
            except Exception as e:
                results["github_mcp"] = {"error": str(e)}
        else:
            results["github_mcp"] = {"status": "not_available"}
        
        # Test File System MCP
        if self.filesystem_mcp:
            try:
                results["filesystem_mcp"] = self.filesystem_mcp.test_connection()
            except Exception as e:
                results["filesystem_mcp"] = {"error": str(e)}
        else:
            results["filesystem_mcp"] = {"status": "not_available"}
        
        return {
            "test_results": results,
            "overall_status": "operational" if any(
                r.get("status") == "connected" for r in results.values()
            ) else "degraded",
            "tested_at": datetime.now().isoformat()
        }
    
    def optimize_for_agent(self, agent_name: str, operation_type: str) -> Dict:
        """Provide optimized MCP configuration for specific agents"""
        optimization_map = {
            "agent_c_github_investigation": {
                "preferred_operations": ["github_get_pull_request", "github_search_pull_requests", "github_analyze_pr_timeline"],
                "performance_mode": "accuracy_over_speed",
                "fallback_tolerance": "low"
            },
            "implementation_reality_agent": {
                "preferred_operations": ["filesystem_search_files", "filesystem_grep_with_context", "github_get_file_content"],
                "performance_mode": "speed_over_completeness",
                "fallback_tolerance": "medium"
            },
            "qe_intelligence_service": {
                "preferred_operations": ["filesystem_find_test_patterns", "filesystem_cache_content", "filesystem_search_files"],
                "performance_mode": "comprehensive_analysis",
                "fallback_tolerance": "high"
            },
            "pattern_extension_service": {
                "preferred_operations": ["filesystem_cache_content", "filesystem_grep_with_context", "github_analyze_pr_timeline"],
                "performance_mode": "pattern_focused",
                "fallback_tolerance": "low"
            }
        }
        
        config = optimization_map.get(agent_name, {
            "preferred_operations": ["filesystem_search_files", "github_get_pull_request"],
            "performance_mode": "balanced",
            "fallback_tolerance": "medium"
        })
        
        return {
            "agent": agent_name,
            "operation_type": operation_type,
            "optimization_config": config,
            "recommendations": self._generate_recommendations(agent_name, operation_type, config)
        }
    
    def _generate_recommendations(self, agent_name: str, operation_type: str, config: Dict) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        if "github" in operation_type and self.github_mcp:
            recommendations.append("Use GitHub MCP for enhanced PR analysis and timeline correlation")
        elif "github" in operation_type:
            recommendations.append("GitHub MCP unavailable - using CLI fallback with reduced capabilities")
        
        if "filesystem" in operation_type and self.filesystem_mcp:
            recommendations.append("Use File System MCP for semantic search and intelligent caching")
        elif "filesystem" in operation_type:
            recommendations.append("File System MCP unavailable - using basic grep/find fallback")
        
        if config.get("performance_mode") == "speed_over_completeness":
            recommendations.append("Enable aggressive caching for repeated operations")
        
        return recommendations

def main():
    """CLI interface for MCP Service Coordinator"""
    if len(sys.argv) < 2:
        print("Usage: python mcp_service_coordinator.py <command> [args...]")
        print("Commands: status, test, github-pr <repo> <number>, fs-search <pattern>")
        return
    
    coordinator = MCPServiceCoordinator()
    command = sys.argv[1]
    
    if command == "status":
        result = coordinator.get_service_status()
        print(json.dumps(result, indent=2))
    
    elif command == "test":
        result = coordinator.test_all_services()
        print(json.dumps(result, indent=2))
    
    elif command == "github-pr" and len(sys.argv) >= 4:
        repo = sys.argv[2]
        pr_number = int(sys.argv[3])
        result = coordinator.github_get_pull_request(repo, pr_number)
        print(json.dumps(result, indent=2, default=str))
    
    elif command == "fs-search" and len(sys.argv) >= 3:
        pattern = sys.argv[2]
        semantic = len(sys.argv) > 3 and sys.argv[3] == "--semantic"
        result = coordinator.filesystem_search_files(pattern, semantic_search=semantic)
        print(json.dumps(result, indent=2, default=str))
    
    else:
        print("Invalid command or arguments")

if __name__ == "__main__":
    main()