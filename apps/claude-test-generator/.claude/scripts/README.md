# Utility Scripts

This directory contains utility scripts for development and maintenance.

## Scripts

### MCP Setup
- `setup_mcp_servers.sh` - Sets up real MCP servers for Claude Code integration

### Performance & Debugging  
- `benchmark_mcp_performance.py` - Performance benchmarking for MCP integration
- `debug_orchestrator_loading.py` - Debug script for AI orchestrator loading issues

## Usage

Scripts can be run from the root directory:
```bash
# Setup MCP servers
./.claude/scripts/setup_mcp_servers.sh

# Run performance benchmark
python3 ./.claude/scripts/benchmark_mcp_performance.py
```
