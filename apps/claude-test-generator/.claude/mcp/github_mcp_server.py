#!/usr/bin/env python3
"""
Real GitHub MCP Server - Thin Wrapper Implementation
====================================================

This is a REAL MCP server that wraps our existing optimized GitHub implementation,
providing actual MCP protocol compliance while preserving all performance benefits.

Features:
- Real JSON-RPC MCP protocol
- Delegates to existing OptimizedGitHubMCPIntegration
- Keeps all caching and performance optimizations
- Registers with Claude Code MCP system
- Future-proof for ecosystem integration
"""

import sys
import json
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from optimized_github_mcp_integration import OptimizedGitHubMCPIntegration

# Create the MCP server
github_mcp_server = FastMCP("test-generator-github")

# Initialize our existing optimized implementation
github_client = OptimizedGitHubMCPIntegration(lazy_init=True)

# MCP Tool Implementations (thin wrappers around existing optimizations)

@github_mcp_server.tool()
def get_pull_request(repo: str, pr_number: int) -> Dict[str, Any]:
    """
    Get GitHub pull request information via MCP protocol
    
    Args:
        repo: Repository in format "owner/repo"
        pr_number: Pull request number
        
    Returns:
        Pull request data with status and caching info
    """
    try:
        # Delegate to existing optimized implementation
        result = github_client.get_pr_details(repo, pr_number)
        
        return {
            "status": "success",
            "data": result,
            "repo": repo,
            "pr_number": pr_number,
            "cached": getattr(github_client, 'last_was_cached', False),
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

@github_mcp_server.tool()
def search_repositories(query: str, max_results: int = 10, sort: str = "stars") -> Dict[str, Any]:
    """
    Search GitHub repositories via MCP protocol
    
    Args:
        query: Search query string
        max_results: Maximum number of results (default: 10)
        sort: Sort order (stars, forks, updated, etc.)
        
    Returns:
        Repository search results
    """
    try:
        # Use optimized implementation if available, fallback to basic search
        if hasattr(github_client, 'search_repositories'):
            result = github_client.search_repositories(query, max_results, sort)
        else:
            # Basic implementation using existing patterns
            github_client._initialize()
            search_url = f"{github_client.base_url}/search/repositories"
            params = {
                "q": query,
                "sort": sort,
                "per_page": min(max_results, 100)
            }
            
            response = github_client.session.get(search_url, params=params)
            response.raise_for_status()
            result = response.json()
        
        return {
            "status": "success",
            "data": result,
            "query": query,
            "max_results": max_results,
            "sort": sort,
            "cached": getattr(github_client, 'last_was_cached', False)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "query": query
        }

@github_mcp_server.tool() 
def get_repository_info(repo: str) -> Dict[str, Any]:
    """
    Get GitHub repository information via MCP protocol
    
    Args:
        repo: Repository in format "owner/repo"
        
    Returns:
        Repository information
    """
    try:
        # Initialize if needed
        github_client._initialize()
        
        # Get repository info using existing session
        repo_url = f"{github_client.base_url}/repos/{repo}"
        response = github_client.session.get(repo_url)
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

@github_mcp_server.tool()
def get_pull_request_files(repo: str, pr_number: int) -> Dict[str, Any]:
    """
    Get files changed in a pull request via MCP protocol
    
    Args:
        repo: Repository in format "owner/repo"
        pr_number: Pull request number
        
    Returns:
        List of files changed in the PR
    """
    try:
        github_client._initialize()
        
        # Get PR files using existing session
        files_url = f"{github_client.base_url}/repos/{repo}/pulls/{pr_number}/files"
        response = github_client.session.get(files_url)
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

# MCP Resource Implementations (read-only access patterns)

@github_mcp_server.resource("github://pr/{repo}/{pr_number}")
def get_pr_resource(repo: str, pr_number: str) -> str:
    """
    Get pull request as a resource (read-only)
    
    Args:
        repo: Repository name
        pr_number: Pull request number as string
        
    Returns:
        Formatted pull request information
    """
    try:
        result = github_client.get_pr_details(repo, int(pr_number))
        if result:
            title = result.get('title', 'Unknown')
            state = result.get('state', 'unknown')
            user = result.get('user', {}).get('login', 'unknown')
            return f"PR #{pr_number} in {repo}: {title} ({state}) by {user}"
        else:
            return f"PR #{pr_number} in {repo}: Not found"
    except Exception as e:
        return f"Error accessing PR #{pr_number} in {repo}: {e}"

@github_mcp_server.resource("github://repo/{repo}")
def get_repo_resource(repo: str) -> str:
    """
    Get repository as a resource (read-only)
    
    Args:
        repo: Repository name
        
    Returns:
        Formatted repository information
    """
    try:
        github_client._initialize()
        repo_url = f"{github_client.base_url}/repos/{repo}"
        response = github_client.session.get(repo_url)
        response.raise_for_status()
        result = response.json()
        
        name = result.get('full_name', repo)
        description = result.get('description', 'No description')
        stars = result.get('stargazers_count', 0)
        language = result.get('language', 'Unknown')
        
        return f"{name}: {description} ({language}, {stars} stars)"
    except Exception as e:
        return f"Error accessing repository {repo}: {e}"

# Performance monitoring and diagnostics

@github_mcp_server.tool()
def get_performance_stats() -> Dict[str, Any]:
    """
    Get GitHub MCP server performance statistics
    
    Returns:
        Performance and caching statistics
    """
    try:
        # Get stats from optimized implementation
        stats = {
            "server_name": "test-generator-github",
            "implementation": "thin_mcp_wrapper",
            "optimized_backend": "OptimizedGitHubMCPIntegration",
            "auth_status": "authenticated" if github_client.auth_token else "not_authenticated",
            "cache_size": len(getattr(github_client, 'cache', {})),
            "session_active": github_client.session is not None
        }
        
        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }

@github_mcp_server.tool()
def health_check() -> Dict[str, Any]:
    """
    GitHub MCP server health check
    
    Returns:
        Health status and connectivity information
    """
    try:
        # Test GitHub API connectivity
        github_client._initialize()
        
        # Simple API test
        test_url = f"{github_client.base_url}/rate_limit"
        response = github_client.session.get(test_url)
        response.raise_for_status()
        rate_limit = response.json()
        
        return {
            "status": "healthy",
            "github_api": "connected",
            "rate_limit_remaining": rate_limit.get('rate', {}).get('remaining', 'unknown'),
            "auth_token": "present" if github_client.auth_token else "missing",
            "server_name": "test-generator-github"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "error_type": type(e).__name__,
            "server_name": "test-generator-github"
        }

# Server lifecycle management

def main():
    """Main entry point for MCP server"""
    try:
        print("🚀 Starting GitHub MCP Server...")
        print("Server: test-generator-github")
        print("Backend: OptimizedGitHubMCPIntegration")
        print("Protocol: MCP JSON-RPC")
        print("\nTools available:")
        print("  - get_pull_request")
        print("  - search_repositories") 
        print("  - get_repository_info")
        print("  - get_pull_request_files")
        print("  - get_performance_stats")
        print("  - health_check")
        print("\nResources available:")
        print("  - github://pr/{repo}/{pr_number}")
        print("  - github://repo/{repo}")
        print("\n🔍 Debug: About to start MCP protocol server...")
        
        # Add debugging for server startup
        import sys
        print(f"🔍 Debug: Python version: {sys.version}")
        print(f"🔍 Debug: FastMCP module: {github_mcp_server.__class__.__module__}")
        print(f"🔍 Debug: Server instance: {github_mcp_server}")
        print(f"🔍 Debug: stdin isatty: {sys.stdin.isatty()}")
        print(f"🔍 Debug: stdout isatty: {sys.stdout.isatty()}")
        
        # Force flush before server run
        sys.stdout.flush()
        sys.stderr.flush()
        
        print("🔍 Debug: Calling github_mcp_server.run()...")
        
        # Run the MCP server - this will block until connection closes
        github_mcp_server.run()
        
        # Note: prints after run() may fail if stdout is closed by MCP protocol
        
    except KeyboardInterrupt:
        # May not print if stdout is closed
        try:
            print("\n✅ GitHub MCP Server stopped (KeyboardInterrupt)")
        except:
            pass
    except Exception as e:
        # Handle the case where stdout might be closed
        try:
            print(f"❌ Server error: {e}")
            print(f"🔍 Debug: Exception type: {type(e)}")
            traceback.print_exc()
        except:
            # Write to stderr if stdout is closed
            import sys
            try:
                sys.stderr.write(f"❌ Server error: {e}\n")
                sys.stderr.flush()
            except:
                pass
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()