#!/usr/bin/env python3
"""
Minimal MCP Filesystem Server - Direct JSON-RPC Implementation
==============================================================

A minimal MCP server implementation that follows the official MCP specification
exactly, using direct JSON-RPC over stdio for maximum Claude Code compatibility.

No external dependencies beyond Python standard library.
"""

import sys
import json
import os
import glob
from pathlib import Path
from typing import Dict, List, Any, Optional

class MinimalMCPFilesystemServer:
    """Minimal MCP server for filesystem operations"""
    
    def __init__(self):
        self.name = "test-generator-filesystem"
        self.version = "1.0.0"
        self.base_path = Path.cwd()
        
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
                "name": "search_files",
                "description": "Search for files using glob patterns",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Glob pattern to search for (e.g., '*.py', '**/*.md')",
                            "default": "*"
                        },
                        "max_results": {
                            "type": "integer", 
                            "description": "Maximum number of results to return",
                            "default": 100
                        }
                    }
                }
            },
            {
                "name": "read_file",
                "description": "Read the contents of a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to read"
                        },
                        "max_lines": {
                            "type": "integer",
                            "description": "Maximum number of lines to read (0 for all)",
                            "default": 0
                        }
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "list_directory",
                "description": "List contents of a directory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "directory": {
                            "type": "string",
                            "description": "Directory path to list",
                            "default": "."
                        }
                    }
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
            if tool_name == "search_files":
                result = self.tool_search_files(arguments)
            elif tool_name == "read_file":
                result = self.tool_read_file(arguments)
            elif tool_name == "list_directory":
                result = self.tool_list_directory(arguments)
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
        
    def tool_search_files(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search for files using glob patterns"""
        pattern = args.get("pattern", "*")
        max_results = args.get("max_results", 100)
        
        try:
            # Handle both simple and recursive patterns
            if "**" in pattern:
                files = list(Path(".").rglob(pattern.replace("**/", "")))
            else:
                files = list(Path(".").glob(pattern))
                
            # Convert to relative paths and filter files only
            results = []
            for file_path in files[:max_results]:
                if file_path.is_file():
                    results.append({
                        "path": str(file_path),
                        "name": file_path.name,
                        "size": file_path.stat().st_size if file_path.exists() else 0,
                        "type": "file"
                    })
                    
            return {
                "status": "success",
                "pattern": pattern,
                "found": len(results),
                "files": results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
            
    def tool_read_file(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Read file contents"""
        file_path = args.get("file_path")
        max_lines = args.get("max_lines", 0)
        
        if not file_path:
            return {"status": "error", "error": "file_path is required"}
            
        try:
            path = Path(file_path)
            if not path.exists():
                return {"status": "error", "error": f"File not found: {file_path}"}
                
            if not path.is_file():
                return {"status": "error", "error": f"Not a file: {file_path}"}
                
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                if max_lines > 0:
                    lines = [f.readline() for _ in range(max_lines)]
                    content = ''.join(line for line in lines if line)
                else:
                    content = f.read()
                    
            return {
                "status": "success",
                "file_path": str(path),
                "content": content,
                "size": len(content)
            }
            
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e)
            }
            
    def tool_list_directory(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """List directory contents"""
        directory = args.get("directory", ".")
        
        try:
            path = Path(directory)
            if not path.exists():
                return {"status": "error", "error": f"Directory not found: {directory}"}
                
            if not path.is_dir():
                return {"status": "error", "error": f"Not a directory: {directory}"}
                
            items = []
            for item in path.iterdir():
                items.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else 0
                })
                
            # Sort: directories first, then files
            items.sort(key=lambda x: (x["type"] != "directory", x["name"].lower()))
            
            return {
                "status": "success",
                "directory": str(path),
                "items": items,
                "count": len(items)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def run(self):
        """Main server loop"""
        self.log_debug("Starting minimal MCP filesystem server")
        self.log_debug(f"Base path: {self.base_path}")
        
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
    server = MinimalMCPFilesystemServer()
    server.run()