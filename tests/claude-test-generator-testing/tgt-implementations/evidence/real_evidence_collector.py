#!/usr/bin/env python3
"""
Real Evidence Collection Engine - Implementation First Approach
Working implementation following main framework patterns
"""

import subprocess
import json
import time
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib

class RealEvidenceCollector:
    """
    Real implementation for evidence collection
    Following main framework enforcement patterns with actual data gathering
    """
    
    def __init__(self):
        self.evidence_storage = Path("../evidence")
        self.evidence_storage.mkdir(exist_ok=True)
        self.collection_session_id = self.generate_session_id()
        
    def generate_session_id(self) -> str:
        """Generate unique session ID for evidence collection"""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:8]
    
    def collect_framework_execution_evidence(self, command: str, timeout: int = 300) -> Dict[str, Any]:
        """Collect REAL evidence from framework execution"""
        collection_start = time.time()
        
        evidence = {
            'collection_info': {
                'session_id': self.collection_session_id,
                'command': command,
                'start_time': datetime.now().isoformat(),
                'timeout': timeout
            }
        }
        
        try:
            # Execute command and collect real evidence
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.get_framework_directory()
            )
            
            execution_time = time.time() - collection_start
            
            # Collect execution evidence
            evidence['execution_evidence'] = {
                'exit_code': result.returncode,
                'execution_time': execution_time,
                'command_success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'stdout_line_count': len(result.stdout.split('\n')),
                'stderr_line_count': len(result.stderr.split('\n'))
            }
            
            # Collect file evidence
            evidence['file_evidence'] = self.collect_file_generation_evidence()
            
            # Collect quality evidence
            evidence['quality_evidence'] = self.collect_quality_evidence(result)
            
            # Collect behavioral evidence
            evidence['behavioral_evidence'] = self.collect_behavioral_evidence(result)
            
            evidence['collection_status'] = 'SUCCESS'
            evidence['collection_duration'] = time.time() - collection_start
            
        except subprocess.TimeoutExpired:
            evidence['collection_status'] = 'TIMEOUT'
            evidence['error'] = f'Command timed out after {timeout} seconds'
            evidence['collection_duration'] = time.time() - collection_start
            
        except Exception as e:
            evidence['collection_status'] = 'ERROR'
            evidence['error'] = str(e)
            evidence['collection_duration'] = time.time() - collection_start
        
        # Store evidence
        self.store_evidence(evidence)
        
        return evidence
    
    def get_framework_directory(self) -> str:
        """Get main framework directory path"""
        return "../../../../apps/claude-test-generator"
    
    def collect_file_generation_evidence(self) -> Dict[str, Any]:
        """Collect evidence about file generation"""
        framework_dir = Path(self.get_framework_directory())
        runs_dir = framework_dir / "runs"
        
        file_evidence = {
            'runs_directory_exists': runs_dir.exists(),
            'total_run_directories': 0,
            'recent_runs': [],
            'total_files_generated': 0,
            'file_details': []
        }
        
        if runs_dir.exists():
            # Count run directories
            run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
            file_evidence['total_run_directories'] = len(run_dirs)
            
            # Get recent runs (last 5)
            recent_runs = sorted(run_dirs, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
            
            for run_dir in recent_runs:
                run_files = list(run_dir.glob("*"))
                file_evidence['recent_runs'].append({
                    'run_directory': run_dir.name,
                    'files_count': len(run_files),
                    'files': [f.name for f in run_files if f.is_file()],
                    'modified_time': run_dir.stat().st_mtime,
                    'size_bytes': sum(f.stat().st_size for f in run_files if f.is_file())
                })
                
                file_evidence['total_files_generated'] += len([f for f in run_files if f.is_file()])
                
                # Collect detailed file evidence
                for file_path in run_files:
                    if file_path.is_file():
                        file_evidence['file_details'].append({
                            'name': file_path.name,
                            'path': str(file_path),
                            'size': file_path.stat().st_size,
                            'modified': file_path.stat().st_mtime,
                            'run_directory': run_dir.name
                        })
        
        return file_evidence
    
    def collect_quality_evidence(self, execution_result) -> Dict[str, Any]:
        """Collect quality evidence from execution"""
        quality_evidence = {
            'html_violation_analysis': self.analyze_html_violations(execution_result.stdout + execution_result.stderr),
            'citation_analysis': self.analyze_citations(execution_result.stdout),
            'error_pattern_analysis': self.analyze_error_patterns(execution_result.stderr),
            'output_structure_analysis': self.analyze_output_structure(execution_result.stdout)
        }
        
        # Calculate quality score
        quality_evidence['calculated_quality_score'] = self.calculate_quality_score(quality_evidence)
        
        return quality_evidence
    
    def analyze_html_violations(self, content: str) -> Dict[str, Any]:
        """Analyze HTML violations in output"""
        html_patterns = [
            r'<br\s*/?>', r'<div[^>]*>', r'</div>', r'<p[^>]*>', r'</p>',
            r'<span[^>]*>', r'</span>', r'<code[^>]*>', r'</code>',
            r'&nbsp;', r'&lt;', r'&gt;', r'&amp;', r'&quot;'
        ]
        
        violations = []
        total_violations = 0
        
        for pattern in html_patterns:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                violations.append({
                    'pattern': pattern,
                    'count': len(matches),
                    'examples': [match.group() for match in matches[:3]]  # First 3 examples
                })
                total_violations += len(matches)
        
        return {
            'total_violations': total_violations,
            'violation_patterns': violations,
            'html_clean': total_violations == 0,
            'violation_density': total_violations / len(content) if content else 0
        }
    
    def analyze_citations(self, content: str) -> Dict[str, Any]:
        """Analyze citation patterns in output"""
        citation_patterns = {
            'jira_references': r'ACM-\d+',
            'file_references': r'\w+\.\w+:\d+',
            'method_references': r'\w+\(\)',
            'url_references': r'https?://[^\s]+',
            'configuration_references': r'config\[\w+\]'
        }
        
        citation_analysis = {}
        total_citations = 0
        
        for pattern_name, pattern in citation_patterns.items():
            matches = re.findall(pattern, content)
            citation_analysis[pattern_name] = {
                'count': len(matches),
                'examples': matches[:5]  # First 5 examples
            }
            total_citations += len(matches)
        
        citation_analysis['total_citations'] = total_citations
        citation_analysis['citation_density'] = total_citations / len(content) if content else 0
        
        return citation_analysis
    
    def analyze_error_patterns(self, stderr_content: str) -> Dict[str, Any]:
        """Analyze error patterns in stderr"""
        error_indicators = {
            'critical_errors': r'ERROR|CRITICAL|FATAL',
            'warnings': r'WARNING|WARN',
            'exceptions': r'Exception|Error:',
            'stack_traces': r'Traceback|at \w+\.\w+',
            'timeout_indicators': r'timeout|timed out'
        }
        
        error_analysis = {}
        total_issues = 0
        
        for indicator_name, pattern in error_indicators.items():
            matches = re.findall(pattern, stderr_content, re.IGNORECASE)
            error_analysis[indicator_name] = {
                'count': len(matches),
                'examples': matches[:3]  # First 3 examples
            }
            total_issues += len(matches)
        
        error_analysis['total_error_indicators'] = total_issues
        error_analysis['error_free'] = total_issues == 0
        
        return error_analysis
    
    def analyze_output_structure(self, stdout_content: str) -> Dict[str, Any]:
        """Analyze output structure patterns"""
        structure_indicators = {
            'phase_indicators': r'Phase \d+|PHASE \d+',
            'agent_indicators': r'Agent [A-D]|AGENT [A-D]',
            'completion_indicators': r'completed|finished|done|SUCCESS',
            'progress_indicators': r'progress|processing|working'
        }
        
        structure_analysis = {}
        
        for indicator_name, pattern in structure_indicators.items():
            matches = re.findall(pattern, stdout_content, re.IGNORECASE)
            structure_analysis[indicator_name] = {
                'count': len(matches),
                'examples': matches[:3]
            }
        
        # Analyze overall structure quality
        structure_analysis['structure_quality'] = self.assess_structure_quality(structure_analysis)
        
        return structure_analysis
    
    def assess_structure_quality(self, structure_analysis: Dict) -> Dict[str, Any]:
        """Assess overall structure quality"""
        quality_indicators = {
            'has_phase_progression': structure_analysis.get('phase_indicators', {}).get('count', 0) > 0,
            'has_agent_activity': structure_analysis.get('agent_indicators', {}).get('count', 0) > 0,
            'has_completion_signals': structure_analysis.get('completion_indicators', {}).get('count', 0) > 0,
            'has_progress_tracking': structure_analysis.get('progress_indicators', {}).get('count', 0) > 0
        }
        
        quality_score = sum(quality_indicators.values()) / len(quality_indicators) * 100
        
        return {
            'quality_indicators': quality_indicators,
            'structure_quality_score': quality_score,
            'well_structured': quality_score >= 75
        }
    
    def calculate_quality_score(self, quality_evidence: Dict) -> float:
        """Calculate overall quality score"""
        weights = {
            'html_compliance': 0.3,  # 30% weight
            'citation_quality': 0.2,  # 20% weight
            'error_absence': 0.3,     # 30% weight
            'structure_quality': 0.2   # 20% weight
        }
        
        scores = {
            'html_compliance': 100 if quality_evidence['html_violation_analysis']['html_clean'] else 0,
            'citation_quality': min(100, quality_evidence['citation_analysis']['total_citations'] * 10),
            'error_absence': 100 if quality_evidence['error_pattern_analysis']['error_free'] else 0,
            'structure_quality': quality_evidence['output_structure_analysis']['structure_quality']['structure_quality_score']
        }
        
        overall_score = sum(scores[component] * weights[component] for component in weights)
        return round(overall_score, 2)
    
    def collect_behavioral_evidence(self, execution_result) -> Dict[str, Any]:
        """Collect behavioral evidence from execution"""
        behavioral_evidence = {
            'execution_behavior': {
                'clean_exit': execution_result.returncode == 0,
                'produced_output': bool(execution_result.stdout.strip()),
                'minimal_errors': len(execution_result.stderr.strip()) < 1000
            },
            'output_patterns': self.analyze_output_patterns(execution_result.stdout),
            'interaction_patterns': self.analyze_interaction_patterns(execution_result.stdout)
        }
        
        return behavioral_evidence
    
    def analyze_output_patterns(self, stdout_content: str) -> Dict[str, Any]:
        """Analyze patterns in output"""
        patterns = {
            'markdown_generation': bool(re.search(r'#+ \w+', stdout_content)),
            'code_block_generation': bool(re.search(r'```\w*', stdout_content)),
            'list_generation': bool(re.search(r'^[-*+] ', stdout_content, re.MULTILINE)),
            'structured_sections': bool(re.search(r'## \w+', stdout_content))
        }
        
        pattern_score = sum(patterns.values()) / len(patterns) * 100
        
        return {
            'patterns_detected': patterns,
            'pattern_score': pattern_score,
            'well_formatted_output': pattern_score >= 50
        }
    
    def analyze_interaction_patterns(self, stdout_content: str) -> Dict[str, Any]:
        """Analyze interaction patterns"""
        interaction_indicators = {
            'service_calls': len(re.findall(r'service|Service', stdout_content)),
            'agent_interactions': len(re.findall(r'agent|Agent', stdout_content)),
            'context_sharing': len(re.findall(r'context|Context', stdout_content)),
            'validation_steps': len(re.findall(r'validat|Validat', stdout_content))
        }
        
        total_interactions = sum(interaction_indicators.values())
        
        return {
            'interaction_indicators': interaction_indicators,
            'total_interaction_signals': total_interactions,
            'interaction_rich': total_interactions > 10
        }
    
    def store_evidence(self, evidence: Dict[str, Any]) -> str:
        """Store evidence to file system"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"evidence_{self.collection_session_id}_{timestamp}.json"
        filepath = self.evidence_storage / filename
        
        with open(filepath, 'w') as f:
            json.dump(evidence, f, indent=2, default=str)
        
        return str(filepath)
    
    def validate_evidence_quality(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the quality of collected evidence"""
        validation = {
            'evidence_completeness': {
                'has_execution_evidence': 'execution_evidence' in evidence,
                'has_file_evidence': 'file_evidence' in evidence,
                'has_quality_evidence': 'quality_evidence' in evidence,
                'has_behavioral_evidence': 'behavioral_evidence' in evidence
            },
            'evidence_quality': {
                'collection_successful': evidence.get('collection_status') == 'SUCCESS',
                'execution_completed': evidence.get('execution_evidence', {}).get('command_success', False),
                'measurable_results': self.has_measurable_results(evidence),
                'comprehensive_coverage': self.has_comprehensive_coverage(evidence)
            }
        }
        
        # Calculate validation score
        all_checks = []
        for category in validation.values():
            all_checks.extend(category.values())
        
        validation_score = sum(all_checks) / len(all_checks) * 100
        validation['validation_score'] = validation_score
        validation['evidence_valid'] = validation_score >= 80
        
        return validation
    
    def has_measurable_results(self, evidence: Dict[str, Any]) -> bool:
        """Check if evidence contains measurable results"""
        measurable_indicators = [
            evidence.get('execution_evidence', {}).get('execution_time', 0) > 0,
            evidence.get('file_evidence', {}).get('total_files_generated', 0) > 0,
            evidence.get('quality_evidence', {}).get('calculated_quality_score', 0) > 0,
            evidence.get('collection_duration', 0) > 0
        ]
        
        return sum(measurable_indicators) >= 3
    
    def has_comprehensive_coverage(self, evidence: Dict[str, Any]) -> bool:
        """Check if evidence provides comprehensive coverage"""
        coverage_indicators = [
            bool(evidence.get('execution_evidence', {}).get('stdout')),
            bool(evidence.get('file_evidence', {}).get('file_details')),
            bool(evidence.get('quality_evidence', {}).get('html_violation_analysis')),
            bool(evidence.get('behavioral_evidence', {}).get('execution_behavior'))
        ]
        
        return sum(coverage_indicators) >= 3


def main():
    """Test the evidence collection engine"""
    print("🧪 Real Evidence Collection Engine Test")
    print("-" * 40)
    
    collector = RealEvidenceCollector()
    
    # Test evidence collection with a simple command
    test_command = "echo 'Framework execution test' && ls -la"
    
    print(f"🔍 Collecting evidence for command: {test_command}")
    evidence = collector.collect_framework_execution_evidence(test_command, timeout=30)
    
    # Validate evidence quality
    validation = collector.validate_evidence_quality(evidence)
    
    print(f"\n📊 Evidence Collection Results:")
    print(f"   Status: {evidence.get('collection_status', 'UNKNOWN')}")
    print(f"   Duration: {evidence.get('collection_duration', 0):.2f}s")
    print(f"   Quality Score: {evidence.get('quality_evidence', {}).get('calculated_quality_score', 0)}")
    print(f"   Validation Score: {validation.get('validation_score', 0):.1f}%")
    print(f"   Evidence Valid: {validation.get('evidence_valid', False)}")
    
    # Store evidence
    evidence_file = collector.store_evidence(evidence)
    print(f"\n📄 Evidence stored: {evidence_file}")
    
    return evidence


if __name__ == "__main__":
    main()