#!/usr/bin/env python3
"""
GitHub MCP Integration Service for claude-test-generator

Provides MCP-style GitHub API access using existing GitHub CLI authentication.
Enhances Agent C (GitHub Investigation) with direct API capabilities while 
maintaining fallback to CLI+WebFetch pattern.

This is a lightweight MCP-style wrapper that leverages existing auth.
"""

import json
import subprocess
import requests
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import time

class GitHubMCPIntegration:
    """GitHub MCP-style integration using existing CLI auth"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.auth_token = self._get_github_token()
        self.headers = {
            "Authorization": f"token {self.auth_token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = time.time() + 3600
        
    def _get_github_token(self) -> str:
        """Extract GitHub token from CLI auth"""
        try:
            result = subprocess.run(['gh', 'auth', 'token'], 
                                  capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            raise Exception("GitHub CLI not authenticated. Run 'gh auth login' first.")
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make authenticated GitHub API request with rate limiting"""
        if self.rate_limit_remaining < 10:
            if time.time() < self.rate_limit_reset:
                wait_time = self.rate_limit_reset - time.time()
                print(f"Rate limit approaching, waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=self.headers, params=params or {})
        
        # Update rate limit info
        self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 5000))
        self.rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600))
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "Not found", "status": 404}
        else:
            response.raise_for_status()
    
    def get_pull_request(self, repo: str, pr_number: int) -> Dict:
        """Get detailed PR information"""
        try:
            endpoint = f"/repos/{repo}/pulls/{pr_number}"
            pr_data = self._make_request(endpoint)
            
            if "error" in pr_data:
                return pr_data
            
            # Enhance with commits and file changes
            commits = self._make_request(f"{endpoint}/commits")
            files = self._make_request(f"{endpoint}/files")
            
            return {
                "pr_info": pr_data,
                "commits": commits if not isinstance(commits, dict) or "error" not in commits else [],
                "files_changed": files if not isinstance(files, dict) or "error" not in files else [],
                "meta": {
                    "retrieved_at": datetime.now().isoformat(),
                    "rate_limit_remaining": self.rate_limit_remaining
                }
            }
        except Exception as e:
            return {"error": str(e), "fallback_to_cli": True}
    
    def search_pull_requests(self, repo: str, query: str = "", state: str = "all", limit: int = 100) -> List[Dict]:
        """Search PRs in repository with advanced filtering"""
        try:
            # Use GitHub search API for more powerful queries
            search_query = f"repo:{repo} type:pr {query}"
            if state != "all":
                search_query += f" state:{state}"
            
            endpoint = "/search/issues"
            params = {
                "q": search_query,
                "sort": "updated",
                "order": "desc",
                "per_page": min(limit, 100)
            }
            
            results = self._make_request(endpoint, params)
            
            if "error" in results:
                return results
            
            return {
                "pull_requests": results.get("items", []),
                "total_count": results.get("total_count", 0),
                "meta": {
                    "query": search_query,
                    "retrieved_at": datetime.now().isoformat(),
                    "rate_limit_remaining": self.rate_limit_remaining
                }
            }
        except Exception as e:
            return {"error": str(e), "fallback_to_cli": True}
    
    def get_repository_info(self, repo: str) -> Dict:
        """Get comprehensive repository information"""
        try:
            repo_data = self._make_request(f"/repos/{repo}")
            
            if "error" in repo_data:
                return repo_data
            
            # Get recent commits for timeline analysis
            commits = self._make_request(f"/repos/{repo}/commits", {"per_page": 50})
            
            # Get repository structure for pattern analysis
            contents = self._make_request(f"/repos/{repo}/contents")
            
            return {
                "repository": repo_data,
                "recent_commits": commits if not isinstance(commits, dict) or "error" not in commits else [],
                "root_contents": contents if not isinstance(contents, dict) or "error" not in contents else [],
                "meta": {
                    "retrieved_at": datetime.now().isoformat(),
                    "rate_limit_remaining": self.rate_limit_remaining
                }
            }
        except Exception as e:
            return {"error": str(e), "fallback_to_cli": True}
    
    def get_file_content(self, repo: str, path: str, ref: str = "main") -> Dict:
        """Get specific file content for pattern analysis"""
        try:
            endpoint = f"/repos/{repo}/contents/{path}"
            params = {"ref": ref}
            
            content_data = self._make_request(endpoint, params)
            
            if "error" in content_data:
                return content_data
            
            # Decode base64 content if it's a file
            if content_data.get("type") == "file" and "content" in content_data:
                import base64
                decoded_content = base64.b64decode(content_data["content"]).decode('utf-8', errors='ignore')
                content_data["decoded_content"] = decoded_content
            
            return content_data
            
        except Exception as e:
            return {"error": str(e), "fallback_to_cli": True}
    
    def analyze_pr_timeline(self, repo: str, pr_numbers: List[int]) -> Dict:
        """Analyze multiple PRs for timeline and correlation patterns"""
        try:
            prs_data = []
            
            for pr_num in pr_numbers[:10]:  # Limit to 10 PRs to avoid rate limits
                pr_data = self.get_pull_request(repo, pr_num)
                if "error" not in pr_data:
                    prs_data.append(pr_data)
            
            # Analyze patterns
            timeline_analysis = self._analyze_pr_patterns(prs_data)
            
            return {
                "prs_analyzed": len(prs_data),
                "timeline_analysis": timeline_analysis,
                "meta": {
                    "analyzed_at": datetime.now().isoformat(),
                    "rate_limit_remaining": self.rate_limit_remaining
                }
            }
            
        except Exception as e:
            return {"error": str(e), "fallback_to_cli": True}
    
    def _analyze_pr_patterns(self, prs_data: List[Dict]) -> Dict:
        """Internal method to analyze PR patterns for Agent C"""
        if not prs_data:
            return {}
        
        patterns = {
            "merge_patterns": [],
            "file_change_patterns": [],
            "commit_patterns": [],
            "timeline_insights": {}
        }
        
        for pr_data in prs_data:
            pr_info = pr_data.get("pr_info", {})
            
            # Merge pattern analysis
            if pr_info.get("merged_at"):
                patterns["merge_patterns"].append({
                    "pr_number": pr_info.get("number"),
                    "merged_at": pr_info.get("merged_at"),
                    "time_to_merge": self._calculate_merge_time(pr_info)
                })
            
            # File change pattern analysis
            files_changed = pr_data.get("files_changed", [])
            if files_changed:
                patterns["file_change_patterns"].append({
                    "pr_number": pr_info.get("number"),
                    "files_count": len(files_changed),
                    "file_types": self._analyze_file_types(files_changed)
                })
        
        return patterns
    
    def _calculate_merge_time(self, pr_info: Dict) -> Optional[str]:
        """Calculate time from creation to merge"""
        try:
            created = datetime.fromisoformat(pr_info["created_at"].replace('Z', '+00:00'))
            merged = datetime.fromisoformat(pr_info["merged_at"].replace('Z', '+00:00'))
            delta = merged - created
            return str(delta)
        except:
            return None
    
    def _analyze_file_types(self, files_changed: List[Dict]) -> Dict:
        """Analyze file types in PR changes"""
        file_types = {}
        for file_info in files_changed:
            filename = file_info.get("filename", "")
            extension = Path(filename).suffix
            file_types[extension] = file_types.get(extension, 0) + 1
        return file_types
    
    def test_connection(self) -> Dict:
        """Test GitHub API connection and authentication"""
        try:
            user_info = self._make_request("/user")
            return {
                "status": "connected",
                "user": user_info.get("login", "unknown"),
                "rate_limit_remaining": self.rate_limit_remaining,
                "authentication": "github_cli_token"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "fallback_available": True
            }

def main():
    """CLI interface for testing GitHub MCP integration"""
    if len(sys.argv) < 2:
        print("Usage: python github_mcp_integration.py <command> [args...]")
        print("Commands: test, pr <repo> <number>, search <repo> [query]")
        return
    
    github = GitHubMCPIntegration()
    command = sys.argv[1]
    
    if command == "test":
        result = github.test_connection()
        print(json.dumps(result, indent=2))
    
    elif command == "pr" and len(sys.argv) >= 4:
        repo = sys.argv[2]
        pr_number = int(sys.argv[3])
        result = github.get_pull_request(repo, pr_number)
        print(json.dumps(result, indent=2, default=str))
    
    elif command == "search" and len(sys.argv) >= 3:
        repo = sys.argv[2]
        query = sys.argv[3] if len(sys.argv) > 3 else ""
        result = github.search_pull_requests(repo, query)
        print(json.dumps(result, indent=2, default=str))
    
    else:
        print("Invalid command or arguments")

if __name__ == "__main__":
    main()