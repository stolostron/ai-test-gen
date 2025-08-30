#!/usr/bin/env python3
"""
Real Filesystem MCP Server - Thin Wrapper Implementation
========================================================

This is a REAL MCP server that wraps our existing optimized filesystem implementation,
providing actual MCP protocol compliance while preserving all performance benefits.

Features:
- Real JSON-RPC MCP protocol
- Delegates to existing OptimizedFileSystemMCPIntegration
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
from optimized_filesystem_mcp_integration import OptimizedFileSystemMCPIntegration

# Create the MCP server
filesystem_mcp_server = FastMCP("test-generator-filesystem")

# Initialize our existing optimized implementation
filesystem_client = OptimizedFileSystemMCPIntegration()

# MCP Tool Implementations (thin wrappers around existing optimizations)

@filesystem_mcp_server.tool()
def search_files(pattern: str = "*", semantic_search: bool = False, 
                minimal_metadata: bool = True, max_results: int = 100) -> Dict[str, Any]:
    """
    Search files in the filesystem via MCP protocol
    
    Args:
        pattern: Glob pattern to search for (default: "*")
        semantic_search: Enable semantic pattern expansion (default: False)
        minimal_metadata: Return minimal metadata for speed (default: True)
        max_results: Maximum number of results (default: 100)
        
    Returns:
        File search results with metadata
    """
    try:
        # Delegate to existing optimized implementation
        result = filesystem_client.search_files(
            pattern=pattern,
            semantic_search=semantic_search,
            minimal_metadata=minimal_metadata,
            max_results=max_results
        )
        
        return {
            "status": "success",
            "data": result,
            "pattern": pattern,
            "semantic_search": semantic_search,
            "minimal_metadata": minimal_metadata,
            "max_results": max_results,
            "file_count": len(result.get("results", [])),
            "source": "optimized_filesystem_api"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "pattern": pattern
        }

@filesystem_mcp_server.tool()
def find_python_files(directory: str = ".", include_tests: bool = True, 
                     max_results: int = 200) -> Dict[str, Any]:
    """
    Find Python files in directory via MCP protocol
    
    Args:
        directory: Directory to search (default: ".")
        include_tests: Include test files (default: True)
        max_results: Maximum number of results (default: 200)
        
    Returns:
        Python file search results
    """
    try:
        # Use optimized search with Python-specific patterns
        if include_tests:
            patterns = ["**/*.py"]
        else:
            patterns = ["**/*.py"]  # Could add exclusion logic
            
        all_results = []
        for pattern in patterns:
            result = filesystem_client.search_files(
                pattern=pattern,
                semantic_search=False,
                minimal_metadata=False,
                max_results=max_results
            )
            all_results.extend(result.get("results", []))
        
        # Filter out tests if requested
        if not include_tests:
            all_results = [f for f in all_results if not any(test in f.get("path", "") 
                          for test in ["test_", "_test.py", "/tests/", "/test/"])]
        
        return {
            "status": "success", 
            "data": {"files": all_results[:max_results]},
            "directory": directory,
            "include_tests": include_tests,
            "file_count": len(all_results[:max_results])
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "directory": directory
        }

@filesystem_mcp_server.tool()
def analyze_directory_structure(directory: str = ".", max_depth: int = 3) -> Dict[str, Any]:
    """
    Analyze directory structure via MCP protocol
    
    Args:
        directory: Directory to analyze (default: ".")
        max_depth: Maximum depth to analyze (default: 3)
        
    Returns:
        Directory structure analysis
    """
    try:
        # Use existing optimized implementation with structure analysis
        base_path = Path(directory).resolve()
        
        structure = {
            "directories": [],
            "files_by_type": {},
            "total_files": 0,
            "total_directories": 0
        }
        
        # Get all files with metadata
        all_files_result = filesystem_client.search_files(
            pattern="**/*",
            semantic_search=False,
            minimal_metadata=False,
            max_results=1000
        )
        
        all_files = all_files_result.get("results", [])
        
        for file_info in all_files:
            file_path = Path(file_info.get("path", ""))
            
            # Skip if too deep
            try:
                relative_path = file_path.relative_to(base_path)
                if len(relative_path.parts) > max_depth:
                    continue
            except ValueError:
                continue
                
            if file_path.is_file():
                structure["total_files"] += 1
                ext = file_path.suffix.lower() or "no_extension"
                structure["files_by_type"][ext] = structure["files_by_type"].get(ext, 0) + 1
            elif file_path.is_dir():
                structure["total_directories"] += 1
                structure["directories"].append(str(relative_path))
        
        return {
            "status": "success",
            "data": structure,
            "directory": directory,
            "max_depth": max_depth
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "directory": directory
        }

@filesystem_mcp_server.tool()
def get_file_content(file_path: str, max_lines: int = 100) -> Dict[str, Any]:
    """
    Get file content via MCP protocol
    
    Args:
        file_path: Path to file to read
        max_lines: Maximum lines to read (default: 100)
        
    Returns:
        File content and metadata
    """
    try:
        path = Path(file_path)
        
        if not path.exists():
            return {
                "status": "error",
                "error": "File not found",
                "file_path": file_path
            }
        
        if not path.is_file():
            return {
                "status": "error", 
                "error": "Path is not a file",
                "file_path": file_path
            }
        
        # Read file content
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Limit lines if requested
        content_lines = lines[:max_lines] if max_lines > 0 else lines
        content = ''.join(content_lines)
        
        return {
            "status": "success",
            "data": {
                "content": content,
                "total_lines": len(lines),
                "returned_lines": len(content_lines),
                "truncated": len(lines) > max_lines if max_lines > 0 else False,
                "file_size": path.stat().st_size,
                "file_path": str(path)
            },
            "file_path": file_path,
            "max_lines": max_lines
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "file_path": file_path
        }

# MCP Resource Implementations (read-only access patterns)

@filesystem_mcp_server.resource("files://{pattern}")
def get_files_resource(pattern: str) -> str:
    """
    Get file listing as a resource (read-only)
    
    Args:
        pattern: Glob pattern to search
        
    Returns:
        Formatted file listing
    """
    try:
        result = filesystem_client.search_files(
            pattern=pattern,
            minimal_metadata=True,
            max_results=50
        )
        
        files = result.get("results", [])
        if not files:
            return f"No files found matching pattern: {pattern}"
        
        file_list = []
        for file_info in files[:20]:  # Limit for resource display
            path = file_info.get("path", "unknown")
            name = file_info.get("name", Path(path).name)
            file_list.append(f"  - {name} ({path})")
        
        total = len(files)
        showing = len(file_list)
        
        result_text = f"Files matching '{pattern}' ({showing}/{total}):\n"
        result_text += "\n".join(file_list)
        
        if total > showing:
            result_text += f"\n... and {total - showing} more files"
            
        return result_text
    except Exception as e:
        return f"Error searching files with pattern '{pattern}': {e}"

@filesystem_mcp_server.resource("directory://{path}")
def get_directory_resource(path: str) -> str:
    """
    Get directory contents as a resource (read-only)
    
    Args:
        path: Directory path
        
    Returns:
        Formatted directory listing
    """
    try:
        dir_path = Path(path)
        
        if not dir_path.exists():
            return f"Directory not found: {path}"
        
        if not dir_path.is_dir():
            return f"Path is not a directory: {path}"
        
        # Get directory contents
        contents = list(dir_path.iterdir())
        contents.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
        
        result_lines = [f"Directory: {path}"]
        
        dirs = [item for item in contents if item.is_dir()]
        files = [item for item in contents if item.is_file()]
        
        if dirs:
            result_lines.append(f"\nDirectories ({len(dirs)}):")
            for d in dirs[:10]:  # Limit display
                result_lines.append(f"  📁 {d.name}/")
            if len(dirs) > 10:
                result_lines.append(f"  ... and {len(dirs) - 10} more directories")
        
        if files:
            result_lines.append(f"\nFiles ({len(files)}):")
            for f in files[:15]:  # Limit display
                size = f.stat().st_size
                result_lines.append(f"  📄 {f.name} ({size} bytes)")
            if len(files) > 15:
                result_lines.append(f"  ... and {len(files) - 15} more files")
        
        return "\n".join(result_lines)
    except Exception as e:
        return f"Error accessing directory '{path}': {e}"

# Performance monitoring and diagnostics

@filesystem_mcp_server.tool()
def get_performance_stats() -> Dict[str, Any]:
    """
    Get filesystem MCP server performance statistics
    
    Returns:
        Performance and caching statistics
    """
    try:
        stats = {
            "server_name": "test-generator-filesystem",
            "implementation": "thin_mcp_wrapper", 
            "optimized_backend": "OptimizedFileSystemMCPIntegration",
            "base_path": str(filesystem_client.base_path),
            "cache_available": hasattr(filesystem_client, 'cache'),
            "working_directory": str(Path.cwd())
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

@filesystem_mcp_server.tool()
def health_check() -> Dict[str, Any]:
    """
    Filesystem MCP server health check
    
    Returns:
        Health status and filesystem access information
    """
    try:
        # Test filesystem access
        base_path = filesystem_client.base_path
        
        # Test basic file operations
        test_result = filesystem_client.search_files("*.py", max_results=1)
        
        # Check permissions
        readable = base_path.exists() and base_path.is_dir()
        
        return {
            "status": "healthy",
            "filesystem_access": "working" if readable else "limited",
            "base_path": str(base_path),
            "base_path_exists": base_path.exists(),
            "test_search": "success" if test_result else "failed",
            "server_name": "test-generator-filesystem"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "error_type": type(e).__name__,
            "server_name": "test-generator-filesystem"
        }

# Server lifecycle management

def main():
    """Main entry point for MCP server"""
    try:
        print("🚀 Starting Filesystem MCP Server...")
        print("Server: test-generator-filesystem")
        print("Backend: OptimizedFileSystemMCPIntegration")
        print("Protocol: MCP JSON-RPC")
        print(f"Base path: {filesystem_client.base_path}")
        print("\nTools available:")
        print("  - search_files")
        print("  - find_python_files")
        print("  - analyze_directory_structure")
        print("  - get_file_content")
        print("  - get_performance_stats")
        print("  - health_check")
        print("\nResources available:")
        print("  - files://{pattern}")
        print("  - directory://{path}")
        print("\n🔍 Debug: About to start MCP protocol server...")
        
        # Add debugging for server startup
        import sys
        print(f"🔍 Debug: Python version: {sys.version}")
        print(f"🔍 Debug: FastMCP module: {filesystem_mcp_server.__class__.__module__}")
        print(f"🔍 Debug: Server instance: {filesystem_mcp_server}")
        print(f"🔍 Debug: stdin isatty: {sys.stdin.isatty()}")
        print(f"🔍 Debug: stdout isatty: {sys.stdout.isatty()}")
        
        # Force flush before server run
        sys.stdout.flush()
        sys.stderr.flush()
        
        print("🔍 Debug: Calling filesystem_mcp_server.run()...")
        
        # Run the MCP server - this will block until connection closes
        filesystem_mcp_server.run()
        
        # Note: prints after run() may fail if stdout is closed by MCP protocol
        
    except KeyboardInterrupt:
        # May not print if stdout is closed
        try:
            print("\n✅ Filesystem MCP Server stopped (KeyboardInterrupt)")
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