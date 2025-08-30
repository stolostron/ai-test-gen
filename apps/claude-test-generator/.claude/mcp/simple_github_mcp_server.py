#!/usr/bin/env python3
"""
Simple GitHub MCP Server - Claude Code Compatible Implementation
===============================================================

A basic GitHub MCP server implementation that's compatible with Claude Code's MCP client.
Uses standard JSON-RPC over stdio without strict validation that might cause issues.
"""

import sys
import json
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from optimized_github_mcp_integration import OptimizedGitHubMCPIntegration
except ImportError:
    print("❌ Could not import OptimizedGitHubMCPIntegration", file=sys.stderr)
    sys.exit(1)

class SimpleGitHubMCPServer:
    """Simple GitHub MCP server implementation compatible with Claude Code"""
    
    def __init__(self, name: str):
        self.name = name
        self.initialized = False
        self.tools = {}
        self.resources = {}
        self.github_client = OptimizedGitHubMCPIntegration(lazy_init=True)
        
        # Register tools
        self._register_tools()
    
    def _register_tools(self):
        """Register available GitHub tools"""
        self.tools = {
            "get_pull_request": {
                "name": "get_pull_request",
                "description": "Get GitHub pull request information",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo": {"type": "string", "description": "Repository in format 'owner/repo'"},
                        "pr_number": {"type": "integer", "description": "Pull request number"}
                    },
                    "required": ["repo", "pr_number"]
                }
            },
            "search_repositories": {
                "name": "search_repositories",
                "description": "Search GitHub repositories",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query string"},
                        "max_results": {"type": "integer", "description": "Maximum number of results", "default": 10},
                        "sort": {"type": "string", "description": "Sort order (stars, forks, updated)", "default": "stars"}
                    },
                    "required": ["query"]
                }
            },
            "get_repository_info": {
                "name": "get_repository_info",
                "description": "Get GitHub repository information",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo": {"type": "string", "description": "Repository in format 'owner/repo'"}
                    },
                    "required": ["repo"]
                }
            },
            "get_pull_request_files": {
                "name": "get_pull_request_files", 
                "description": "Get files changed in a pull request",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo": {"type": "string", "description": "Repository in format 'owner/repo'"},
                        "pr_number": {"type": "integer", "description": "Pull request number"}
                    },
                    "required": ["repo", "pr_number"]
                }
            },
            "health_check": {
                "name": "health_check",
                "description": "Check GitHub server health status",
                "inputSchema": {"type": "object", "properties": {}}
            }
        }
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC request"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method == "initialize":
                return self._handle_initialize(request_id, params)
            elif method == "tools/list":
                return self._handle_list_tools(request_id)
            elif method == "tools/call":
                return self._handle_call_tool(request_id, params)
            elif method == "resources/list":
                return self._handle_list_resources(request_id)
            elif method == "ping":
                return {"jsonrpc": "2.0", "id": request_id, "result": {}}
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }
                
        except Exception as e:
            return {
                "jsonrpc": "2.0", 
                "id": request.get("id"),
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }
    
    def _handle_initialize(self, request_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request"""
        self.initialized = True
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": self.name,
                    "version": "1.0.0"
                }
            }
        }
    
    def _handle_list_tools(self, request_id: int) -> Dict[str, Any]:
        """Handle tools/list request"""
        if not self.initialized:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32002, "message": "Server not initialized"}
            }
        
        tools_list = list(self.tools.values())
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": tools_list}
        }
    
    def _handle_call_tool(self, request_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        if not self.initialized:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32002, "message": "Server not initialized"}
            }
        
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in self.tools:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32602, "message": f"Unknown tool: {tool_name}"}
            }
        
        try:
            if tool_name == "get_pull_request":
                result = self._tool_get_pull_request(arguments)
            elif tool_name == "search_repositories":
                result = self._tool_search_repositories(arguments)
            elif tool_name == "get_repository_info":
                result = self._tool_get_repository_info(arguments)
            elif tool_name == "get_pull_request_files":
                result = self._tool_get_pull_request_files(arguments)
            elif tool_name == "health_check":
                result = self._tool_health_check(arguments)
            else:
                result = {"error": f"Tool not implemented: {tool_name}"}
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            }
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Tool execution failed: {str(e)}"}
            }
    
    def _handle_list_resources(self, request_id: int) -> Dict[str, Any]:
        """Handle resources/list request"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"resources": []}
        }
    
    def _tool_get_pull_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute get_pull_request tool"""
        repo = args.get("repo")
        pr_number = args.get("pr_number")
        
        if not repo or not pr_number:
            return {"error": "repo and pr_number are required"}
        
        try:
            # Delegate to existing optimized implementation
            result = self.github_client.get_pr_details(repo, pr_number)
            
            return {
                "status": "success",
                "data": result,
                "repo": repo,
                "pr_number": pr_number,
                "cached": getattr(self.github_client, 'last_was_cached', False),
                "source": "optimized_github_api"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__,
                "repo": repo,
                "pr_number": pr_number
            }
    
    def _tool_search_repositories(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute search_repositories tool"""
        query = args.get("query")
        max_results = args.get("max_results", 10)
        sort = args.get("sort", "stars")
        
        if not query:
            return {"error": "query is required"}
        
        try:
            # Use optimized implementation if available, fallback to basic search
            if hasattr(self.github_client, 'search_repositories'):
                result = self.github_client.search_repositories(query, max_results, sort)
            else:
                # Basic implementation using existing patterns
                self.github_client._initialize()
                search_url = f"{self.github_client.base_url}/search/repositories"
                params = {
                    "q": query,
                    "sort": sort,
                    "per_page": min(max_results, 100)
                }
                
                response = self.github_client.session.get(search_url, params=params)
                response.raise_for_status()
                result = response.json()
            
            return {
                "status": "success",
                "data": result,
                "query": query,
                "max_results": max_results,
                "sort": sort,
                "cached": getattr(self.github_client, 'last_was_cached', False)
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__,
                "query": query
            }
    
    def _tool_get_repository_info(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute get_repository_info tool"""
        repo = args.get("repo")
        
        if not repo:
            return {"error": "repo is required"}
        
        try:
            # Initialize if needed
            self.github_client._initialize()
            
            # Get repository info using existing session
            repo_url = f"{self.github_client.base_url}/repos/{repo}"
            response = self.github_client.session.get(repo_url)
            response.raise_for_status()
            result = response.json()
            
            return {
                "status": "success",
                "data": result,
                "repo": repo,
                "cached": False  # Could add caching for this too
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__,
                "repo": repo
            }
    
    def _tool_get_pull_request_files(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute get_pull_request_files tool"""
        repo = args.get("repo")
        pr_number = args.get("pr_number")
        
        if not repo or not pr_number:
            return {"error": "repo and pr_number are required"}
        
        try:
            self.github_client._initialize()
            
            # Get PR files using existing session
            files_url = f"{self.github_client.base_url}/repos/{repo}/pulls/{pr_number}/files"
            response = self.github_client.session.get(files_url)
            response.raise_for_status()
            files = response.json()
            
            return {
                "status": "success",
                "data": files,
                "repo": repo,
                "pr_number": pr_number,
                "file_count": len(files)
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__,
                "repo": repo,
                "pr_number": pr_number
            }
    
    def _tool_health_check(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute health_check tool"""
        try:
            # Test GitHub API connectivity
            self.github_client._initialize()
            
            # Simple API test
            test_url = f"{self.github_client.base_url}/rate_limit"
            response = self.github_client.session.get(test_url)
            response.raise_for_status()
            rate_limit = response.json()
            
            return {
                "status": "healthy",
                "server_name": self.name,
                "initialized": self.initialized,
                "github_api": "connected",
                "rate_limit_remaining": rate_limit.get('rate', {}).get('remaining', 'unknown'),
                "auth_token": "present" if self.github_client.auth_token else "missing",
                "tools_available": len(self.tools)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "error_type": type(e).__name__,
                "server_name": self.name
            }
    
    def run(self):
        """Run the MCP server (listen on stdin)"""
        print(f"🚀 Simple GitHub MCP Server '{self.name}' starting...", file=sys.stderr)
        print(f"🔧 Tools: {len(self.tools)} available", file=sys.stderr)
        print(f"🔑 Auth: {'Present' if self.github_client.auth_token else 'Missing'}", file=sys.stderr)
        print("✅ Server ready for MCP requests", file=sys.stderr)
        
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    response = self.handle_request(request)
                    print(json.dumps(response), flush=True)
                except json.JSONDecodeError:
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32700, "message": "Parse error"}
                    }
                    print(json.dumps(error_response), flush=True)
                except Exception as e:
                    error_response = {
                        "jsonrpc": "2.0", 
                        "id": None,
                        "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
                    }
                    print(json.dumps(error_response), flush=True)
                    
        except KeyboardInterrupt:
            print("📴 GitHub Server stopped", file=sys.stderr)
        except Exception as e:
            print(f"❌ GitHub Server error: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

def main():
    """Main entry point"""
    server = SimpleGitHubMCPServer("test-generator-github-simple")
    server.run()

if __name__ == "__main__":
    main()