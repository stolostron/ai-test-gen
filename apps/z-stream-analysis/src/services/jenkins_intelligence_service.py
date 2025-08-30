#!/usr/bin/env python3
"""
Jenkins Intelligence Service
Core service for extracting intelligence from Jenkins pipeline failures
"""

import json
import logging
import re
import subprocess
import time
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse


@dataclass
class JenkinsMetadata:
    """Jenkins build metadata structure"""
    build_url: str
    job_name: str
    build_number: int
    build_result: str
    timestamp: str
    parameters: Dict[str, Any]
    console_log_snippet: str
    artifacts: List[str]
    branch: Optional[str] = None
    commit_sha: Optional[str] = None


@dataclass
class JenkinsIntelligence:
    """Complete Jenkins intelligence analysis result"""
    metadata: JenkinsMetadata
    failure_analysis: Dict[str, Any]
    environment_info: Dict[str, Any]
    evidence_sources: List[str]
    confidence_score: float


class JenkinsIntelligenceService:
    """
    Jenkins Intelligence Service
    Extracts comprehensive intelligence from Jenkins pipeline failures
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def analyze_jenkins_url(self, jenkins_url: str) -> JenkinsIntelligence:
        """
        Main method to analyze Jenkins pipeline failure
        
        Args:
            jenkins_url: Jenkins build URL
            
        Returns:
            JenkinsIntelligence: Complete analysis result
        """
        self.logger.info(f"Starting Jenkins intelligence analysis for: {jenkins_url}")
        
        # Extract metadata
        metadata = self._extract_jenkins_metadata(jenkins_url)
        
        # Analyze failure patterns
        failure_analysis = self._analyze_failure_patterns(metadata.console_log_snippet)
        
        # Extract environment information
        environment_info = self._extract_environment_info(metadata.parameters)
        
        # Build evidence sources
        evidence_sources = self._build_evidence_sources(metadata)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(metadata, failure_analysis)
        
        return JenkinsIntelligence(
            metadata=metadata,
            failure_analysis=failure_analysis,
            environment_info=environment_info,
            evidence_sources=evidence_sources,
            confidence_score=confidence_score
        )
    
    def _extract_jenkins_metadata(self, jenkins_url: str) -> JenkinsMetadata:
        """Extract basic metadata from Jenkins build"""
        parsed_url = urlparse(jenkins_url)
        
        # Parse job name and build number from URL
        path_parts = parsed_url.path.strip('/').split('/')
        
        if 'job' in path_parts:
            job_index = path_parts.index('job')
            job_name = path_parts[job_index + 1] if job_index + 1 < len(path_parts) else "unknown"
        else:
            job_name = "unknown"
            
        # Extract build number
        build_number = self._extract_build_number(jenkins_url)
        
        # Get console log and build info
        console_log = self._fetch_console_log(jenkins_url)
        build_info = self._fetch_build_info(jenkins_url)
        
        return JenkinsMetadata(
            build_url=jenkins_url,
            job_name=job_name,
            build_number=build_number,
            build_result=build_info.get('result', 'UNKNOWN'),
            timestamp=build_info.get('timestamp', ''),
            parameters=build_info.get('parameters', {}),
            console_log_snippet=console_log[:2000],  # First 2KB for analysis
            artifacts=build_info.get('artifacts', []),
            branch=self._extract_branch_from_parameters(build_info.get('parameters', {})),
            commit_sha=self._extract_commit_from_console(console_log)
        )
    
    def _extract_build_number(self, jenkins_url: str) -> int:
        """Extract build number from Jenkins URL"""
        # Match patterns like /123/ or /123 at end of URL
        match = re.search(r'/(\d+)/?$', jenkins_url)
        if match:
            return int(match.group(1))
        return 0
    
    def _fetch_console_log(self, jenkins_url: str) -> str:
        """Fetch console log using curl"""
        console_url = f"{jenkins_url.rstrip('/')}/consoleText"
        
        try:
            result = subprocess.run(
                ['curl', '-k', '-s', '--max-time', '30', console_url],
                capture_output=True,
                text=True,
                timeout=35
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                self.logger.warning(f"Failed to fetch console log: {result.stderr}")
                return ""
                
        except subprocess.TimeoutExpired:
            self.logger.warning("Console log fetch timed out")
            return ""
        except Exception as e:
            self.logger.error(f"Error fetching console log: {str(e)}")
            return ""
    
    def _fetch_build_info(self, jenkins_url: str) -> Dict[str, Any]:
        """Fetch build information using Jenkins API"""
        api_url = f"{jenkins_url.rstrip('/')}/api/json"
        
        try:
            result = subprocess.run(
                ['curl', '-k', '-s', '--max-time', '30', api_url],
                capture_output=True,
                text=True,
                timeout=35
            )
            
            if result.returncode == 0 and result.stdout:
                return json.loads(result.stdout)
            else:
                self.logger.warning("Failed to fetch build info via API")
                return {}
                
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            self.logger.warning(f"Error fetching build info: {str(e)}")
            return {}
        except Exception as e:
            self.logger.error(f"Unexpected error fetching build info: {str(e)}")
            return {}
    
    def _analyze_failure_patterns(self, console_log: str) -> Dict[str, Any]:
        """Analyze console log for failure patterns"""
        failure_patterns = {
            'timeout_errors': [],
            'element_not_found': [],
            'network_errors': [],
            'assertion_failures': [],
            'build_failures': [],
            'environment_issues': []
        }
        
        # Timeout patterns
        timeout_patterns = [
            r'timeout.*waiting.*for.*element',
            r'TimeoutError',
            r'timed out after \d+',
            r'cypress.*timed.*out'
        ]
        
        for pattern in timeout_patterns:
            matches = re.findall(pattern, console_log, re.IGNORECASE)
            failure_patterns['timeout_errors'].extend(matches)
        
        # Element not found patterns
        element_patterns = [
            r'element.*not.*found',
            r'selector.*not.*found',
            r'NoSuchElementException',
            r'ElementNotInteractableException'
        ]
        
        for pattern in element_patterns:
            matches = re.findall(pattern, console_log, re.IGNORECASE)
            failure_patterns['element_not_found'].extend(matches)
        
        # Network error patterns
        network_patterns = [
            r'connection.*refused',
            r'network.*error',
            r'failed.*to.*connect',
            r'DNS.*resolution.*failed'
        ]
        
        for pattern in network_patterns:
            matches = re.findall(pattern, console_log, re.IGNORECASE)
            failure_patterns['network_errors'].extend(matches)
        
        # Count total failures
        total_failures = sum(len(errors) for errors in failure_patterns.values())
        
        return {
            'patterns': failure_patterns,
            'total_failures': total_failures,
            'primary_failure_type': self._determine_primary_failure_type(failure_patterns)
        }
    
    def _determine_primary_failure_type(self, patterns: Dict[str, List]) -> str:
        """Determine the primary type of failure"""
        failure_counts = {key: len(values) for key, values in patterns.items()}
        
        if not any(failure_counts.values()):
            return 'unknown'
            
        return max(failure_counts, key=failure_counts.get)
    
    def _extract_environment_info(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Extract environment information from build parameters"""
        env_info = {
            'cluster_name': None,
            'environment_type': None,
            'target_branch': None,
            'test_suite': None
        }
        
        # Common parameter names for cluster information
        cluster_params = ['CLUSTER_NAME', 'cluster', 'environment', 'ENVIRONMENT']
        for param in cluster_params:
            if param in parameters:
                env_info['cluster_name'] = parameters[param]
                break
        
        # Branch information
        branch_params = ['BRANCH', 'branch', 'GIT_BRANCH', 'git_branch']
        for param in branch_params:
            if param in parameters:
                env_info['target_branch'] = parameters[param]
                break
        
        # Test suite information
        suite_params = ['TEST_SUITE', 'test_suite', 'SUITE']
        for param in suite_params:
            if param in parameters:
                env_info['test_suite'] = parameters[param]
                break
        
        return env_info
    
    def _extract_branch_from_parameters(self, parameters: Dict[str, Any]) -> Optional[str]:
        """Extract branch name from build parameters"""
        branch_params = ['BRANCH', 'branch', 'GIT_BRANCH', 'git_branch']
        
        for param in branch_params:
            if param in parameters:
                branch = parameters[param]
                # Clean up branch name (remove origin/ prefix if present)
                if isinstance(branch, str):
                    return branch.replace('origin/', '').strip()
        
        return None
    
    def _extract_commit_from_console(self, console_log: str) -> Optional[str]:
        """Extract commit SHA from console log"""
        # Look for git commit patterns
        commit_patterns = [
            r'commit\s+([a-f0-9]{7,40})',
            r'Revision:\s+([a-f0-9]{7,40})',
            r'Checking out\s+([a-f0-9]{7,40})'
        ]
        
        for pattern in commit_patterns:
            match = re.search(pattern, console_log, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _build_evidence_sources(self, metadata: JenkinsMetadata) -> List[str]:
        """Build list of evidence sources for citations"""
        sources = []
        
        # Jenkins build source
        sources.append(f"[Jenkins:{metadata.job_name}:{metadata.build_number}:{metadata.build_result}:{metadata.timestamp}]({metadata.build_url})")
        
        # Console log source
        console_url = f"{metadata.build_url.rstrip('/')}/console"
        sources.append(f"[Console:{metadata.job_name}:{metadata.build_number}]({console_url})")
        
        # Repository source if commit is available
        if metadata.commit_sha and metadata.branch:
            sources.append(f"[Repo:{metadata.branch}:commit:{metadata.commit_sha}]")
        
        return sources
    
    def _calculate_confidence_score(self, metadata: JenkinsMetadata, failure_analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for the analysis"""
        score = 0.0
        
        # Base score for having metadata
        if metadata.build_result != 'UNKNOWN':
            score += 0.3
        
        # Score for having console log data
        if metadata.console_log_snippet:
            score += 0.2
        
        # Score for having failure analysis
        if failure_analysis['total_failures'] > 0:
            score += 0.3
        
        # Score for having build parameters
        if metadata.parameters:
            score += 0.1
        
        # Score for having branch and commit info
        if metadata.branch:
            score += 0.05
        if metadata.commit_sha:
            score += 0.05
        
        return min(score, 1.0)
    
    def to_dict(self, intelligence: JenkinsIntelligence) -> Dict[str, Any]:
        """Convert JenkinsIntelligence to dictionary for serialization"""
        return {
            'metadata': asdict(intelligence.metadata),
            'failure_analysis': intelligence.failure_analysis,
            'environment_info': intelligence.environment_info,
            'evidence_sources': intelligence.evidence_sources,
            'confidence_score': intelligence.confidence_score
        }