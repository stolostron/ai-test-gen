#!/usr/bin/env python3
"""
Example: Thin MCP Wrapper Implementation
========================================

This demonstrates how to create real MCP servers that wrap your existing
optimized implementations, providing MCP protocol compliance without
losing performance benefits.
"""

import asyncio
import sys
from pathlib import Path

# Add your existing modules
sys.path.insert(0, str(Path(__file__).parent / ".claude" / "mcp"))
from optimized_github_mcp_integration import OptimizedGitHubMCPIntegration
from optimized_filesystem_mcp_integration import OptimizedFileSystemMCPIntegration

# Real MCP server implementation
try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    print("MCP not installed. Run: pip install mcp")
    MCP_AVAILABLE = False


def create_github_mcp_server():
    """Create real MCP server wrapping existing GitHub optimizations"""
    if not MCP_AVAILABLE:
        return None
    
    # Create MCP server
    mcp_server = FastMCP("test-generator-github")
    
    # Reuse your existing optimized implementation
    github_client = OptimizedGitHubMCPIntegration()
    
    @mcp_server.tool()
    def get_pull_request(repo: str, pr_number: int) -> dict:
        """Get GitHub PR information via MCP protocol"""
        # Delegate to existing optimized code - keeps all performance benefits
        try:
            result = github_client.get_pr_details(repo, pr_number)
            return {
                "status": "success",
                "data": result,
                "cached": github_client.cache_hit if hasattr(github_client, 'cache_hit') else False
            }
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e)
            }
    
    @mcp_server.tool()
    def search_repositories(query: str, max_results: int = 10) -> dict:
        """Search GitHub repositories via MCP protocol"""
        # Another example of wrapping existing functionality
        try:
            result = github_client.search_repositories(query, max_results)
            return {
                "status": "success",
                "data": result,
                "query": query
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    @mcp_server.resource("github://pr/{repo}/{pr_number}")
    def get_pr_resource(repo: str, pr_number: str) -> str:
        """Get PR as a resource (read-only access)"""
        try:
            result = github_client.get_pr_details(repo, int(pr_number))
            return f"PR #{pr_number} in {repo}: {result.get('title', 'Unknown')}"
        except Exception as e:
            return f"Error: {e}"
    
    return mcp_server


def create_filesystem_mcp_server():
    """Create real MCP server wrapping existing filesystem optimizations"""
    if not MCP_AVAILABLE:
        return None
    
    # Create MCP server
    mcp_server = FastMCP("test-generator-filesystem")
    
    # Reuse your existing optimized implementation
    fs_client = OptimizedFileSystemMCPIntegration()
    
    @mcp_server.tool()
    def search_files(pattern: str, semantic_search: bool = False, max_results: int = 100) -> dict:
        """Search files via MCP protocol"""
        try:
            result = fs_client.search_files(
                pattern=pattern,
                semantic_search=semantic_search,
                max_results=max_results
            )
            return {
                "status": "success",
                "data": result,
                "pattern": pattern,
                "semantic": semantic_search
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    @mcp_server.tool()
    def analyze_file_patterns(directory: str = ".") -> dict:
        """Analyze file patterns in directory via MCP protocol"""
        try:
            result = fs_client.analyze_patterns(directory)
            return {
                "status": "success",
                "data": result,
                "directory": directory
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    @mcp_server.resource("files://{pattern}")
    def get_files_resource(pattern: str) -> str:
        """Get file listing as resource"""
        try:
            result = fs_client.search_files(pattern, minimal_metadata=True)
            files = [f["path"] for f in result.get("files", [])]
            return f"Files matching '{pattern}':\n" + "\n".join(files[:20])
        except Exception as e:
            return f"Error: {e}"
    
    return mcp_server


async def main():
    """Run both MCP servers"""
    if not MCP_AVAILABLE:
        print("❌ MCP not available. Install with: pip install mcp")
        return
    
    print("🚀 Starting Thin MCP Wrapper Servers...")
    
    # Create servers
    github_server = create_github_mcp_server()
    filesystem_server = create_filesystem_mcp_server()
    
    if github_server and filesystem_server:
        print("✅ GitHub MCP Server: test-generator-github")
        print("✅ Filesystem MCP Server: test-generator-filesystem")
        print("\nTo register with Claude Code:")
        print("claude mcp add test-generator-github 'python example_thin_mcp_wrapper.py --server github'")
        print("claude mcp add test-generator-filesystem 'python example_thin_mcp_wrapper.py --server filesystem'")
        
        # Run servers (in real implementation, you'd run them separately)
        print("\n🔄 Servers ready for MCP protocol communication...")
        print("Press Ctrl+C to stop")
        
        try:
            await asyncio.sleep(3600)  # Keep running
        except KeyboardInterrupt:
            print("\n✅ Servers stopped")


if __name__ == "__main__":
    if "--server" in sys.argv:
        server_type = sys.argv[sys.argv.index("--server") + 1]
        if server_type == "github":
            github_server = create_github_mcp_server()
            if github_server:
                # Run GitHub server
                asyncio.run(github_server.run())
        elif server_type == "filesystem":
            filesystem_server = create_filesystem_mcp_server()
            if filesystem_server:
                # Run filesystem server
                asyncio.run(filesystem_server.run())
    else:
        # Demo mode
        asyncio.run(main())