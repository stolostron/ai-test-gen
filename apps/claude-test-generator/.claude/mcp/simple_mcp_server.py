#!/usr/bin/env python3
"""
Simple MCP Server - Claude Code Compatible Implementation
========================================================

A basic MCP server implementation that's compatible with Claude Code's MCP client.
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
    from optimized_filesystem_mcp_integration import OptimizedFileSystemMCPIntegration
except ImportError:
    print("❌ Could not import OptimizedFileSystemMCPIntegration", file=sys.stderr)
    sys.exit(1)

class SimpleMCPServer:
    """Simple MCP server implementation compatible with Claude Code"""
    
    def __init__(self, name: str):
        self.name = name
        self.initialized = False
        self.tools = {}
        self.resources = {}
        self.filesystem_client = OptimizedFileSystemMCPIntegration()
        
        # Register tools
        self._register_tools()
    
    def _register_tools(self):
        """Register available tools"""
        self.tools = {
            "search_files": {
                "name": "search_files", 
                "description": "Search for files in the filesystem",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern": {"type": "string", "description": "Glob pattern to search for"},
                        "max_results": {"type": "integer", "description": "Maximum number of results", "default": 100}
                    }
                }
            },
            "get_file_content": {
                "name": "get_file_content",
                "description": "Get content of a specific file", 
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to the file"},
                        "max_lines": {"type": "integer", "description": "Maximum lines to read", "default": 100}
                    },
                    "required": ["file_path"]
                }
            },
            "health_check": {
                "name": "health_check",
                "description": "Check server health status",
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
            if tool_name == "search_files":
                result = self._tool_search_files(arguments)
            elif tool_name == "get_file_content":
                result = self._tool_get_file_content(arguments)
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
    
    def _tool_search_files(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute search_files tool"""
        pattern = args.get("pattern", "*")
        max_results = args.get("max_results", 100)
        
        result = self.filesystem_client.search_files(
            pattern=pattern,
            minimal_metadata=True,
            max_results=max_results
        )
        
        return {
            "status": "success",
            "pattern": pattern,
            "max_results": max_results,
            "files_found": len(result.get("results", [])),
            "results": result
        }
    
    def _tool_get_file_content(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute get_file_content tool"""
        file_path = args.get("file_path")
        max_lines = args.get("max_lines", 100)
        
        if not file_path:
            return {"error": "file_path is required"}
        
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": f"File not found: {file_path}"}
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            content_lines = lines[:max_lines] if max_lines > 0 else lines
            content = ''.join(content_lines)
            
            return {
                "status": "success",
                "file_path": file_path,
                "total_lines": len(lines),
                "returned_lines": len(content_lines),
                "truncated": len(lines) > max_lines if max_lines > 0 else False,
                "content": content
            }
            
        except Exception as e:
            return {"error": f"Failed to read file: {str(e)}"}
    
    def _tool_health_check(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute health_check tool"""
        try:
            # Test filesystem access
            test_result = self.filesystem_client.search_files("*.py", max_results=1)
            
            return {
                "status": "healthy",
                "server_name": self.name,
                "initialized": self.initialized,
                "filesystem_access": "working",
                "tools_available": len(self.tools),
                "test_search": "success" if test_result else "failed"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def run(self):
        """Run the MCP server (listen on stdin)"""
        print(f"🚀 Simple MCP Server '{self.name}' starting...", file=sys.stderr)
        print(f"📍 Base path: {self.filesystem_client.base_path}", file=sys.stderr)
        print(f"🔧 Tools: {len(self.tools)} available", file=sys.stderr)
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
            print("📴 Server stopped", file=sys.stderr)
        except Exception as e:
            print(f"❌ Server error: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

def main():
    """Main entry point"""
    server = SimpleMCPServer("test-generator-filesystem-simple")
    server.run()

if __name__ == "__main__":
    main()