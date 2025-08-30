#!/usr/bin/env python3
"""
Minimal MCP GitHub Server - Direct JSON-RPC Implementation
===========================================================

A minimal MCP server implementation for GitHub operations that follows the
official MCP specification exactly, using direct JSON-RPC over stdio for
maximum Claude Code compatibility.

No external dependencies beyond Python standard library.
"""

import sys
import json
import subprocess
import os
from typing import Dict, List, Any, Optional

class MinimalMCPGitHubServer:
    """Minimal MCP server for GitHub operations"""
    
    def __init__(self):
        self.name = "test-generator-github"
        self.version = "1.0.0"
        
    def log_debug(self, message: str):
        """Log debug message to stderr"""
        print(f"[{self.name}] {message}", file=sys.stderr, flush=True)
        
    def send_response(self, response: Dict[str, Any]):
        """Send JSON-RPC response to stdout"""
        json_str = json.dumps(response)
        print(json_str, flush=True)
        
    def send_error(self, request_id: Any, code: int, message: str, data: Any = None):
        """Send JSON-RPC error response"""
        error_response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
        if data is not None:
            error_response["error"]["data"] = data
        self.send_response(error_response)
        
    def handle_initialize(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": False
                    },
                    "resources": {
                        "subscribe": False,
                        "listChanged": False
                    }
                },
                "serverInfo": {
                    "name": self.name,
                    "version": self.version
                }
            }
        }
        
    def handle_tools_list(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/list request"""
        tools = [
            {
                "name": "search_repositories",
                "description": "Search GitHub repositories using gh CLI",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for repositories"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return",
                            "default": 10
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_repository_info",
                "description": "Get information about a specific GitHub repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo": {
                            "type": "string",
                            "description": "Repository in format 'owner/repo'"
                        }
                    },
                    "required": ["repo"]
                }
            },
            {
                "name": "search_code",
                "description": "Search for code in GitHub repositories",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Code search query"
                        },
                        "repo": {
                            "type": "string",
                            "description": "Limit search to specific repository (owner/repo)",
                            "default": ""
                        },
                        "limit": {
                            "type": "integer", 
                            "description": "Maximum number of results to return",
                            "default": 10
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_pull_request",
                "description": "Get information about a specific pull request",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "repo": {
                            "type": "string",
                            "description": "Repository in format 'owner/repo'"
                        },
                        "pr_number": {
                            "type": "integer",
                            "description": "Pull request number"
                        }
                    },
                    "required": ["repo", "pr_number"]
                }
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools
            }
        }
        
    def handle_tools_call(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "search_repositories":
                result = self.tool_search_repositories(arguments)
            elif tool_name == "get_repository_info":
                result = self.tool_get_repository_info(arguments)
            elif tool_name == "search_code":
                result = self.tool_search_code(arguments)
            elif tool_name == "get_pull_request":
                result = self.tool_get_pull_request(arguments)
            else:
                return self.error_response(request_id, -32601, f"Unknown tool: {tool_name}")
                
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
            
        except Exception as e:
            return self.error_response(request_id, -32603, f"Tool execution failed: {str(e)}")
            
    def error_response(self, request_id: Any, code: int, message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
        
    def run_gh_command(self, cmd: List[str]) -> Dict[str, Any]:
        """Run gh CLI command and return result"""
        try:
            result = subprocess.run(
                ["gh"] + cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            else:
                return {
                    "status": "error",
                    "error": f"gh command failed (code {result.returncode})",
                    "stderr": result.stderr,
                    "stdout": result.stdout
                }
                
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "error": "Command timed out"
            }
        except FileNotFoundError:
            return {
                "status": "error",
                "error": "gh CLI not found - please install GitHub CLI"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
            
    def tool_search_repositories(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search GitHub repositories"""
        query = args.get("query")
        limit = args.get("limit", 10)
        
        if not query:
            return {"status": "error", "error": "query is required"}
            
        cmd = ["search", "repos", query, "--limit", str(limit), "--json", 
               "name,owner,description,url,stars,language,updatedAt"]
        
        result = self.run_gh_command(cmd)
        
        if result["status"] == "success":
            try:
                repos = json.loads(result["stdout"]) if result["stdout"].strip() else []
                return {
                    "status": "success",
                    "query": query,
                    "found": len(repos),
                    "repositories": repos
                }
            except json.JSONDecodeError:
                return {
                    "status": "error",
                    "error": "Failed to parse gh command output"
                }
        else:
            return result
            
    def tool_get_repository_info(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get repository information"""
        repo = args.get("repo")
        
        if not repo:
            return {"status": "error", "error": "repo is required"}
            
        cmd = ["repo", "view", repo, "--json", 
               "name,owner,description,url,stars,forks,language,topics,createdAt,updatedAt"]
        
        result = self.run_gh_command(cmd)
        
        if result["status"] == "success":
            try:
                repo_info = json.loads(result["stdout"]) if result["stdout"].strip() else {}
                return {
                    "status": "success",
                    "repository": repo,
                    "info": repo_info
                }
            except json.JSONDecodeError:
                return {
                    "status": "error",
                    "error": "Failed to parse gh command output"
                }
        else:
            return result
            
    def tool_search_code(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search code in GitHub repositories"""
        query = args.get("query")
        repo = args.get("repo", "")
        limit = args.get("limit", 10)
        
        if not query:
            return {"status": "error", "error": "query is required"}
            
        # Build search query
        full_query = query
        if repo:
            full_query = f"{query} repo:{repo}"
            
        cmd = ["search", "code", full_query, "--limit", str(limit), "--json",
               "repository,path,url,htmlUrl"]
        
        result = self.run_gh_command(cmd)
        
        if result["status"] == "success":
            try:
                code_results = json.loads(result["stdout"]) if result["stdout"].strip() else []
                return {
                    "status": "success",
                    "query": query,
                    "repo_filter": repo,
                    "found": len(code_results),
                    "results": code_results
                }
            except json.JSONDecodeError:
                return {
                    "status": "error",
                    "error": "Failed to parse gh command output"
                }
        else:
            return result
            
    def tool_get_pull_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get pull request information"""
        repo = args.get("repo")
        pr_number = args.get("pr_number")
        
        if not repo:
            return {"status": "error", "error": "repo is required"}
        if not pr_number:
            return {"status": "error", "error": "pr_number is required"}
            
        cmd = ["pr", "view", str(pr_number), "--repo", repo, "--json",
               "title,body,author,state,url,createdAt,updatedAt,mergeable,labels"]
        
        result = self.run_gh_command(cmd)
        
        if result["status"] == "success":
            try:
                pr_info = json.loads(result["stdout"]) if result["stdout"].strip() else {}
                return {
                    "status": "success",
                    "repository": repo,
                    "pr_number": pr_number,
                    "pull_request": pr_info
                }
            except json.JSONDecodeError:
                return {
                    "status": "error",
                    "error": "Failed to parse gh command output"
                }
        else:
            return result
    
    def run(self):
        """Main server loop"""
        self.log_debug("Starting minimal MCP GitHub server")
        
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    request = json.loads(line)
                    self.log_debug(f"Received: {request.get('method', 'unknown')}")
                    
                    method = request.get("method")
                    request_id = request.get("id")
                    params = request.get("params", {})
                    
                    if method == "initialize":
                        response = self.handle_initialize(request_id, params)
                    elif method == "tools/list":
                        response = self.handle_tools_list(request_id, params)
                    elif method == "tools/call":
                        response = self.handle_tools_call(request_id, params)
                    elif method == "notifications/initialized":
                        # Acknowledgment - no response needed
                        continue
                    else:
                        response = self.error_response(request_id, -32601, f"Unknown method: {method}")
                        
                    self.send_response(response)
                    
                except json.JSONDecodeError as e:
                    self.log_debug(f"JSON decode error: {e}")
                    self.send_error(None, -32700, "Parse error")
                except Exception as e:
                    self.log_debug(f"Request handling error: {e}")
                    self.send_error(None, -32603, "Internal error")
                    
        except KeyboardInterrupt:
            self.log_debug("Server interrupted")
        except Exception as e:
            self.log_debug(f"Server error: {e}")

if __name__ == "__main__":
    server = MinimalMCPGitHubServer()
    server.run()