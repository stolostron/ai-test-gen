#!/usr/bin/env python3
"""
Simple MCP Server for Claude Code Registration Test
"""

from mcp.server.fastmcp import FastMCP

# Create MCP server
server = FastMCP("test-demo")

@server.tool()
def hello() -> str:
    """Say hello via MCP"""
    return "Hello from MCP server!"

@server.tool()  
def add_numbers(a: int, b: int) -> int:
    """Add two numbers via MCP"""
    return a + b

if __name__ == "__main__":
    server.run()