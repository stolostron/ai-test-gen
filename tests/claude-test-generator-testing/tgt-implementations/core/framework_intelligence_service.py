#!/usr/bin/env python3
"""
Framework Intelligence Service - Working within Isolation Constraints
Git-based intelligence gathering with real evidence collection
"""

import subprocess
import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class FrameworkIntelligenceService:
    """
    Real implementation for gathering framework intelligence
    Works within isolation constraints using git commands
    """
    
    def __init__(self):
        self.repo_root = Path("../../../../")
        self.main_framework_path = "apps/claude-test-generator"
        self.evidence = {}
        
    def run_git_command(self, cmd: List[str], cwd: str = ".") -> Dict[str, Any]:
        """Execute git command and collect evidence"""
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=cwd,
                timeout=30
            )
            
            return {
                'exit_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': ' '.join(cmd),
                'timestamp': datetime.now().isoformat(),
                'success': result.returncode == 0
            }
        except Exception as e:
            return {
                'exit_code': -1,
                'error': str(e),
                'command': ' '.join(cmd),
                'timestamp': datetime.now().isoformat(),
                'success': False
            }
    
    def discover_main_framework_services(self) -> Dict[str, Any]:
        """Discover main framework AI services using git"""
        print("🔍 Discovering main framework AI services...")
        
        # Use git to list service files - use the full correct path
        git_result = self.run_git_command([
            'git', 'ls-files', '../../../../apps/claude-test-generator/.claude/ai-services/*.md'
        ])
        
        services = []
        service_count = 0
        
        if git_result['success'] and git_result['stdout'].strip():
            service_files = [f for f in git_result['stdout'].strip().split('\n') if f]
            service_count = len(service_files)
            
            for service_file in service_files:
                service_name = Path(service_file).stem
                services.append({
                    'name': service_name,
                    'file_path': service_file,
                    'prefix': service_name.split('-')[0] if '-' in service_name else 'unknown'
                })
        
        # Analyze service patterns
        prefixes = {}
        for service in services:
            prefix = service['prefix']
            if prefix not in prefixes:
                prefixes[prefix] = []
            prefixes[prefix].append(service['name'])
        
        evidence = {
            'total_services': service_count,
            'services': services,
            'prefixes': prefixes,
            'git_command_result': git_result,
            'discovery_timestamp': datetime.now().isoformat()
        }
        
        print(f"📊 Discovered {service_count} AI services in main framework")
        
        return evidence
    
    def discover_testing_framework_services(self) -> Dict[str, Any]:
        """Discover current testing framework services"""
        print("🔍 Discovering testing framework AI services...")
        
        services_dir = Path("../../.claude/ai-services")
        services = []
        
        if services_dir.exists():
            for service_file in services_dir.glob("*.md"):
                service_name = service_file.stem
                services.append({
                    'name': service_name,
                    'file_path': str(service_file),
                    'prefix': service_name.split('-')[0] if '-' in service_name else 'unknown'
                })
        
        # Analyze service patterns
        prefixes = {}
        for service in services:
            prefix = service['prefix']
            if prefix not in prefixes:
                prefixes[prefix] = []
            prefixes[prefix].append(service['name'])
        
        evidence = {
            'total_services': len(services),
            'services': services,
            'prefixes': prefixes,
            'services_directory_exists': services_dir.exists(),
            'discovery_timestamp': datetime.now().isoformat()
        }
        
        print(f"📊 Discovered {len(services)} AI services in testing framework")
        
        return evidence
    
    def analyze_service_gap(self) -> Dict[str, Any]:
        """Analyze the gap between main framework and testing framework services"""
        print("📈 Analyzing service architecture gap...")
        
        main_services = self.discover_main_framework_services()
        testing_services = self.discover_testing_framework_services()
        
        # Calculate gaps
        main_count = main_services['total_services']
        testing_count = testing_services['total_services']
        gap = main_count - testing_count
        coverage = (testing_count / main_count * 100) if main_count > 0 else 0
        
        # Find missing service patterns
        main_prefixes = set(main_services['prefixes'].keys())
        testing_prefixes = set(testing_services['prefixes'].keys())
        missing_prefixes = main_prefixes - testing_prefixes
        
        # Create mapping recommendations
        recommendations = []
        for service in main_services['services']:
            main_name = service['name']
            # Convert tg- prefix to tgt- for testing
            if main_name.startswith('tg-'):
                testing_equivalent = main_name.replace('tg-', 'tgt-')
                testing_exists = any(s['name'] == testing_equivalent for s in testing_services['services'])
                
                if not testing_exists:
                    recommendations.append({
                        'main_service': main_name,
                        'recommended_testing_service': testing_equivalent,
                        'status': 'missing'
                    })
        
        gap_analysis = {
            'main_framework': main_services,
            'testing_framework': testing_services,
            'gap_analysis': {
                'main_service_count': main_count,
                'testing_service_count': testing_count,
                'service_gap': gap,
                'coverage_percentage': coverage,
                'missing_prefixes': list(missing_prefixes),
                'missing_services_count': len(recommendations)
            },
            'recommendations': recommendations,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        print(f"📊 Service Gap Analysis:")
        print(f"   Main Framework: {main_count} services")
        print(f"   Testing Framework: {testing_count} services")
        print(f"   Gap: {gap} services ({coverage:.1f}% coverage)")
        print(f"   Missing service mappings: {len(recommendations)}")
        
        return gap_analysis
    
    def analyze_framework_structure(self) -> Dict[str, Any]:
        """Analyze main framework structure using git"""
        print("🏗️ Analyzing framework structure...")
        
        # Get framework directory structure
        structure_result = self.run_git_command([
            'git', 'ls-files', f'{self.main_framework_path}/.claude/'
        ])
        
        directories = set()
        file_types = {}
        
        if structure_result['success']:
            files = structure_result['stdout'].strip().split('\n')
            
            for file_path in files:
                if not file_path:
                    continue
                    
                # Extract directory structure
                path_parts = Path(file_path).parts
                for i in range(len(path_parts)):
                    dir_path = '/'.join(path_parts[:i+1])
                    directories.add(dir_path)
                
                # Analyze file types
                extension = Path(file_path).suffix
                if extension not in file_types:
                    file_types[extension] = 0
                file_types[extension] += 1
        
        structure_analysis = {
            'directories': sorted(list(directories)),
            'file_types': file_types,
            'total_files': len(structure_result['stdout'].strip().split('\n')) if structure_result['success'] else 0,
            'git_result': structure_result,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        print(f"📁 Framework structure: {len(directories)} directories, {structure_analysis['total_files']} files")
        
        return structure_analysis
    
    def check_recent_changes(self) -> Dict[str, Any]:
        """Check recent changes in main framework"""
        print("🔄 Checking recent framework changes...")
        
        # Get recent commits affecting main framework
        recent_commits = self.run_git_command([
            'git', 'log', '--oneline', '-10', '--', f'{self.main_framework_path}/'
        ])
        
        # Get current status
        status_result = self.run_git_command([
            'git', 'status', '--porcelain', f'{self.main_framework_path}/'
        ])
        
        changes_analysis = {
            'recent_commits': recent_commits,
            'current_status': status_result,
            'changes_detected': bool(status_result['stdout'].strip()) if status_result['success'] else False,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        change_count = len(status_result['stdout'].strip().split('\n')) if status_result['success'] and status_result['stdout'].strip() else 0
        print(f"🔄 Recent changes detected: {change_count} modified files")
        
        return changes_analysis
    
    def run_comprehensive_intelligence_gathering(self) -> Dict[str, Any]:
        """Run comprehensive intelligence gathering"""
        print("🧠 Framework Intelligence Gathering")
        print("=" * 50)
        
        intelligence = {
            'intelligence_gathering': {
                'start_time': datetime.now().isoformat(),
                'isolation_compliant': True,
                'method': 'git_based_analysis'
            }
        }
        
        # Gather all intelligence
        intelligence['service_gap_analysis'] = self.analyze_service_gap()
        intelligence['framework_structure'] = self.analyze_framework_structure() 
        intelligence['recent_changes'] = self.check_recent_changes()
        
        # Generate summary
        service_gap = intelligence['service_gap_analysis']['gap_analysis']
        
        intelligence['summary'] = {
            'main_framework_services': service_gap['main_service_count'],
            'testing_framework_services': service_gap['testing_service_count'],
            'service_coverage': f"{service_gap['coverage_percentage']:.1f}%",
            'missing_services': service_gap['missing_services_count'],
            'intelligence_quality': 'high' if service_gap['main_service_count'] > 0 else 'limited',
            'end_time': datetime.now().isoformat()
        }
        
        print("\n" + "=" * 50)
        print("🎯 Intelligence Summary:")
        print(f"📊 Main Framework Services: {intelligence['summary']['main_framework_services']}")
        print(f"📉 Testing Framework Services: {intelligence['summary']['testing_framework_services']}")
        print(f"📈 Coverage: {intelligence['summary']['service_coverage']}")
        print(f"🔧 Missing Services: {intelligence['summary']['missing_services']}")
        
        return intelligence


def main():
    """Main execution function"""
    print("🧠 Framework Intelligence Service")
    print("Working within isolation constraints")
    print("-" * 40)
    
    service = FrameworkIntelligenceService()
    intelligence = service.run_comprehensive_intelligence_gathering()
    
    # Save intelligence data
    output_file = Path("tgt-implementations/evidence/framework_intelligence.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(intelligence, f, indent=2, default=str)
    
    print(f"\n📄 Intelligence saved to: {output_file}")
    
    return 0


if __name__ == "__main__":
    exit(main())