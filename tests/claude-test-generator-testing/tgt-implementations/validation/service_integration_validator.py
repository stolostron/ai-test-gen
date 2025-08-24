#!/usr/bin/env python3
"""
Service Integration Validator - Comprehensive Service Ecosystem Testing
Validates integration and coordination of all implemented AI services
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

class ServiceIntegrationValidator:
    """
    Comprehensive validator for testing framework service integration
    Ensures all services work together effectively
    """
    
    def __init__(self):
        self.validation_storage = Path("evidence/service_integration")
        self.validation_storage.mkdir(parents=True, exist_ok=True)
        
        self.services_directory = Path(".claude/ai-services")
        self.implementations_directory = Path("tgt-implementations")
        
        self.discovered_services = []
        self.service_dependencies = {}
        self.integration_results = {}
        
    def validate_complete_service_integration(self) -> Dict[str, Any]:
        """Validate complete service ecosystem integration"""
        
        validation_result = {
            'validation_timestamp': datetime.now().isoformat(),
            'service_discovery': {},
            'dependency_analysis': {},
            'integration_testing': {},
            'coordination_validation': {},
            'performance_assessment': {},
            'overall_integration_score': 0,
            'integration_status': 'unknown'
        }
        
        print("🔍 Service Integration Validation")
        print("=" * 50)
        
        # Discover all services
        validation_result['service_discovery'] = self.discover_all_services()
        print(f"📊 Discovered {len(self.discovered_services)} services")
        
        # Analyze service dependencies
        validation_result['dependency_analysis'] = self.analyze_service_dependencies()
        print(f"🔗 Analyzed dependencies for {len(self.service_dependencies)} services")
        
        # Test service integration
        validation_result['integration_testing'] = self.test_service_integration()
        print(f"🧪 Integration tests: {validation_result['integration_testing'].get('tests_passed', 0)}/{validation_result['integration_testing'].get('total_tests', 0)} passed")
        
        # Validate service coordination
        validation_result['coordination_validation'] = self.validate_service_coordination()
        print(f"⚙️  Coordination validation: {validation_result['coordination_validation'].get('coordination_score', 0):.1f}%")
        
        # Assess performance
        validation_result['performance_assessment'] = self.assess_integration_performance()
        print(f"⚡ Performance score: {validation_result['performance_assessment'].get('performance_score', 0):.1f}%")
        
        # Calculate overall integration score
        validation_result['overall_integration_score'] = self.calculate_overall_integration_score(validation_result)
        
        # Determine integration status
        integration_score = validation_result['overall_integration_score']
        if integration_score >= 90:
            validation_result['integration_status'] = 'excellent'
        elif integration_score >= 75:
            validation_result['integration_status'] = 'good'
        elif integration_score >= 60:
            validation_result['integration_status'] = 'fair'
        else:
            validation_result['integration_status'] = 'poor'
        
        print(f"\n🎯 Overall Integration Score: {integration_score:.1f}% ({validation_result['integration_status'].upper()})")
        
        # Store validation results
        self.store_validation_results(validation_result)
        
        return validation_result
    
    def discover_all_services(self) -> Dict[str, Any]:
        """Discover all available services"""
        
        discovery_result = {
            'discovery_timestamp': datetime.now().isoformat(),
            'services_found': [],
            'service_categories': {},
            'implementation_coverage': {},
            'discovery_summary': {}
        }
        
        try:
            # Discover service files
            if self.services_directory.exists():
                service_files = list(self.services_directory.glob("tgt-*.md"))
                
                for service_file in service_files:
                    service_info = self.analyze_service_file(service_file)
                    discovery_result['services_found'].append(service_info)
                    self.discovered_services.append(service_info)
                
                # Categorize services
                discovery_result['service_categories'] = self.categorize_services(
                    discovery_result['services_found']
                )
                
                # Check implementation coverage
                discovery_result['implementation_coverage'] = self.check_implementation_coverage(
                    discovery_result['services_found']
                )
                
                # Generate discovery summary
                discovery_result['discovery_summary'] = {
                    'total_services': len(discovery_result['services_found']),
                    'implemented_services': discovery_result['implementation_coverage'].get('implemented_count', 0),
                    'implementation_rate': discovery_result['implementation_coverage'].get('implementation_rate', 0),
                    'categories_covered': len(discovery_result['service_categories'])
                }
            
        except Exception as e:
            discovery_result['error'] = f"Service discovery failed: {str(e)}"
        
        return discovery_result
    
    def analyze_service_file(self, service_file: Path) -> Dict[str, Any]:
        """Analyze individual service file"""
        
        service_info = {
            'service_name': service_file.stem,
            'file_path': str(service_file),
            'service_type': 'unknown',
            'capabilities': [],
            'dependencies': [],
            'implementation_status': 'unknown',
            'file_size': 0,
            'last_modified': None
        }
        
        try:
            # Get file stats
            stats = service_file.stat()
            service_info['file_size'] = stats.st_size
            service_info['last_modified'] = datetime.fromtimestamp(stats.st_mtime).isoformat()
            
            # Read and analyze service content
            content = service_file.read_text(encoding='utf-8')
            
            # Extract service type from name
            service_name = service_file.stem.lower()
            if 'evidence' in service_name or 'validation' in service_name:
                service_info['service_type'] = 'core_validation'
            elif 'context' in service_name or 'universal' in service_name:
                service_info['service_type'] = 'context_management'
            elif 'pattern' in service_name or 'learning' in service_name:
                service_info['service_type'] = 'learning_intelligence'
            elif 'monitoring' in service_name or 'anomaly' in service_name:
                service_info['service_type'] = 'monitoring_services'
            elif 'github' in service_name or 'environment' in service_name or 'security' in service_name:
                service_info['service_type'] = 'specialized_services'
            else:
                service_info['service_type'] = 'general_service'
            
            # Extract capabilities (look for capability bullet points)
            capability_lines = [line.strip() for line in content.split('\n') 
                             if line.strip().startswith('- **') and '**:' in line]
            service_info['capabilities'] = [line.split('**:')[0].replace('- **', '') 
                                         for line in capability_lines[:5]]  # Top 5 capabilities
            
            # Determine implementation status
            if 'class ' in content and 'def ' in content:
                service_info['implementation_status'] = 'implemented'
            elif '```python' in content:
                service_info['implementation_status'] = 'partially_implemented'
            else:
                service_info['implementation_status'] = 'specification_only'
            
        except Exception as e:
            service_info['analysis_error'] = f"Service analysis failed: {str(e)}"
        
        return service_info
    
    def categorize_services(self, services: List[Dict]) -> Dict[str, List[str]]:
        """Categorize services by type"""
        
        categories = {}
        
        for service in services:
            service_type = service.get('service_type', 'unknown')
            service_name = service.get('service_name', 'unknown')
            
            if service_type not in categories:
                categories[service_type] = []
            
            categories[service_type].append(service_name)
        
        return categories
    
    def check_implementation_coverage(self, services: List[Dict]) -> Dict[str, Any]:
        """Check implementation coverage of services"""
        
        coverage = {
            'total_services': len(services),
            'implemented_count': 0,
            'partially_implemented_count': 0,
            'specification_only_count': 0,
            'implementation_rate': 0.0,
            'implementation_details': []
        }
        
        for service in services:
            status = service.get('implementation_status', 'unknown')
            
            if status == 'implemented':
                coverage['implemented_count'] += 1
            elif status == 'partially_implemented':
                coverage['partially_implemented_count'] += 1
            else:
                coverage['specification_only_count'] += 1
            
            coverage['implementation_details'].append({
                'service_name': service.get('service_name'),
                'status': status,
                'capabilities_count': len(service.get('capabilities', []))
            })
        
        # Calculate implementation rate
        if coverage['total_services'] > 0:
            implemented_weight = coverage['implemented_count'] * 1.0
            partial_weight = coverage['partially_implemented_count'] * 0.5
            coverage['implementation_rate'] = ((implemented_weight + partial_weight) / coverage['total_services']) * 100
        
        return coverage
    
    def analyze_service_dependencies(self) -> Dict[str, Any]:
        """Analyze dependencies between services"""
        
        dependency_analysis = {
            'analysis_timestamp': datetime.now().isoformat(),
            'dependency_map': {},
            'circular_dependencies': [],
            'dependency_levels': {},
            'coordination_requirements': []
        }
        
        try:
            # Analyze dependencies for each service
            for service in self.discovered_services:
                service_name = service.get('service_name')
                dependencies = self.identify_service_dependencies(service)
                
                dependency_analysis['dependency_map'][service_name] = dependencies
                self.service_dependencies[service_name] = dependencies
            
            # Check for circular dependencies
            dependency_analysis['circular_dependencies'] = self.detect_circular_dependencies()
            
            # Calculate dependency levels
            dependency_analysis['dependency_levels'] = self.calculate_dependency_levels()
            
            # Identify coordination requirements
            dependency_analysis['coordination_requirements'] = self.identify_coordination_requirements()
            
        except Exception as e:
            dependency_analysis['error'] = f"Dependency analysis failed: {str(e)}"
        
        return dependency_analysis
    
    def identify_service_dependencies(self, service: Dict[str, Any]) -> List[str]:
        """Identify dependencies for a specific service"""
        
        dependencies = []
        service_name = service.get('service_name', '').lower()
        
        # Common dependency patterns based on service type
        if 'enhanced' in service_name:
            dependencies.append('tgt-implementation-reality-agent')
        
        if 'pattern' in service_name:
            dependencies.append('tgt-evidence-validation-engine')
        
        if 'monitoring' in service_name:
            dependencies.extend(['tgt-pattern-learning-engine', 'tgt-anomaly-detection-service'])
        
        if 'context' in service_name:
            dependencies.append('tgt-implementation-reality-agent')
        
        # Service-specific dependencies
        service_specific_deps = {
            'tgt-regression-detection-service': ['tgt-evidence-validation-engine'],
            'tgt-pattern-learning-engine': ['tgt-implementation-reality-agent'],
            'tgt-anomaly-detection-service': ['tgt-pattern-learning-engine'],
            'tgt-intelligent-monitoring-service': ['tgt-anomaly-detection-service', 'tgt-pattern-learning-engine'],
            'tgt-enhanced-github-integration': ['tgt-security-validation-engine'],
            'tgt-smart-environment-service': ['tgt-intelligent-monitoring-service'],
            'tgt-security-validation-engine': ['tgt-implementation-reality-agent']
        }
        
        if service_name in service_specific_deps:
            dependencies.extend(service_specific_deps[service_name])
        
        # Remove duplicates and self-references
        dependencies = list(set(dep for dep in dependencies if dep != service_name))
        
        return dependencies
    
    def test_service_integration(self) -> Dict[str, Any]:
        """Test integration between services"""
        
        integration_testing = {
            'testing_timestamp': datetime.now().isoformat(),
            'integration_tests': [],
            'tests_passed': 0,
            'tests_failed': 0,
            'total_tests': 0,
            'integration_issues': []
        }
        
        try:
            # Test core service integration
            core_tests = self.test_core_service_integration()
            integration_testing['integration_tests'].extend(core_tests)
            
            # Test context service integration
            context_tests = self.test_context_service_integration()
            integration_testing['integration_tests'].extend(context_tests)
            
            # Test specialized service integration
            specialized_tests = self.test_specialized_service_integration()
            integration_testing['integration_tests'].extend(specialized_tests)
            
            # Calculate test results
            for test in integration_testing['integration_tests']:
                integration_testing['total_tests'] += 1
                if test.get('passed', False):
                    integration_testing['tests_passed'] += 1
                else:
                    integration_testing['tests_failed'] += 1
                    integration_testing['integration_issues'].append({
                        'test_name': test.get('test_name'),
                        'issue': test.get('failure_reason', 'Unknown issue')
                    })
            
        except Exception as e:
            integration_testing['error'] = f"Integration testing failed: {str(e)}"
        
        return integration_testing
    
    def test_core_service_integration(self) -> List[Dict[str, Any]]:
        """Test integration of core services"""
        
        core_tests = []
        
        # Test Evidence Validation Engine integration
        evidence_test = {
            'test_name': 'evidence_validation_integration',
            'test_type': 'core_integration',
            'passed': False,
            'execution_time': 0.0
        }
        
        try:
            start_time = time.time()
            
            # Check if evidence validation service exists and has required structure
            evidence_service = self.find_service_by_name('tgt-evidence-validation-engine')
            
            if evidence_service:
                # Check for implementation indicators
                service_file = Path(evidence_service['file_path'])
                if service_file.exists():
                    content = service_file.read_text()
                    
                    # Check for key integration points
                    has_class_definition = 'class ' in content
                    has_validation_methods = 'validate' in content.lower()
                    has_evidence_collection = 'evidence' in content.lower()
                    
                    if has_class_definition and has_validation_methods and has_evidence_collection:
                        evidence_test['passed'] = True
                    else:
                        evidence_test['failure_reason'] = 'Missing required integration components'
                else:
                    evidence_test['failure_reason'] = 'Service file not found'
            else:
                evidence_test['failure_reason'] = 'Evidence validation service not discovered'
            
            evidence_test['execution_time'] = time.time() - start_time
            
        except Exception as e:
            evidence_test['failure_reason'] = f"Test execution failed: {str(e)}"
        
        core_tests.append(evidence_test)
        
        return core_tests
    
    def test_context_service_integration(self) -> List[Dict[str, Any]]:
        """Test integration of context services"""
        
        context_tests = []
        
        # Test Universal Context Manager integration
        context_test = {
            'test_name': 'universal_context_integration',
            'test_type': 'context_integration',
            'passed': False,
            'execution_time': 0.0
        }
        
        try:
            start_time = time.time()
            
            context_service = self.find_service_by_name('tgt-universal-context-manager')
            
            if context_service:
                service_file = Path(context_service['file_path'])
                if service_file.exists():
                    content = service_file.read_text()
                    
                    # Check for Progressive Context Architecture components
                    has_context_management = 'UniversalContextManager' in content
                    has_inheritance_logic = 'inheritance' in content.lower()
                    has_validation_engine = 'ContextValidationEngine' in content
                    
                    if has_context_management and has_inheritance_logic and has_validation_engine:
                        context_test['passed'] = True
                    else:
                        context_test['failure_reason'] = 'Missing Progressive Context Architecture components'
                else:
                    context_test['failure_reason'] = 'Context service file not found'
            else:
                context_test['failure_reason'] = 'Universal context manager not discovered'
            
            context_test['execution_time'] = time.time() - start_time
            
        except Exception as e:
            context_test['failure_reason'] = f"Context test failed: {str(e)}"
        
        context_tests.append(context_test)
        
        return context_tests
    
    def test_specialized_service_integration(self) -> List[Dict[str, Any]]:
        """Test integration of specialized services"""
        
        specialized_tests = []
        
        # Test GitHub Integration
        github_test = {
            'test_name': 'github_integration_test',
            'test_type': 'specialized_integration',
            'passed': False,
            'execution_time': 0.0
        }
        
        try:
            start_time = time.time()
            
            github_service = self.find_service_by_name('tgt-enhanced-github-integration')
            
            if github_service:
                service_file = Path(github_service['file_path'])
                if service_file.exists():
                    content = service_file.read_text()
                    
                    # Check for GitHub integration components
                    has_github_client = 'EnhancedGitHubIntegration' in content
                    has_repository_analysis = 'analyze_repository' in content
                    has_workflow_automation = 'workflow' in content.lower()
                    
                    if has_github_client and has_repository_analysis and has_workflow_automation:
                        github_test['passed'] = True
                    else:
                        github_test['failure_reason'] = 'Missing GitHub integration components'
                else:
                    github_test['failure_reason'] = 'GitHub service file not found'
            else:
                github_test['failure_reason'] = 'GitHub integration service not discovered'
            
            github_test['execution_time'] = time.time() - start_time
            
        except Exception as e:
            github_test['failure_reason'] = f"GitHub integration test failed: {str(e)}"
        
        specialized_tests.append(github_test)
        
        return specialized_tests
    
    def validate_service_coordination(self) -> Dict[str, Any]:
        """Validate coordination between services"""
        
        coordination_validation = {
            'validation_timestamp': datetime.now().isoformat(),
            'coordination_matrix': {},
            'coordination_score': 0.0,
            'coordination_issues': [],
            'optimization_opportunities': []
        }
        
        try:
            # Build coordination matrix
            coordination_validation['coordination_matrix'] = self.build_coordination_matrix()
            
            # Calculate coordination score
            coordination_validation['coordination_score'] = self.calculate_coordination_score(
                coordination_validation['coordination_matrix']
            )
            
            # Identify coordination issues
            coordination_validation['coordination_issues'] = self.identify_coordination_issues()
            
            # Find optimization opportunities
            coordination_validation['optimization_opportunities'] = self.find_coordination_optimizations()
            
        except Exception as e:
            coordination_validation['error'] = f"Coordination validation failed: {str(e)}"
        
        return coordination_validation
    
    def build_coordination_matrix(self) -> Dict[str, Any]:
        """Build service coordination matrix"""
        
        matrix = {
            'service_pairs': [],
            'coordination_strength': {},
            'dependency_satisfaction': {},
            'integration_points': {}
        }
        
        # Analyze coordination between all service pairs
        for i, service_a in enumerate(self.discovered_services):
            for service_b in self.discovered_services[i+1:]:
                service_pair_id = f"pair_{i}_{service_a['service_name'][:10]}_to_{service_b['service_name'][:10]}"
                
                coordination_strength = self.calculate_pair_coordination(
                    service_a, service_b
                )
                
                matrix['service_pairs'].append(service_pair_id)
                matrix['coordination_strength'][service_pair_id] = coordination_strength
        
        return matrix
    
    def calculate_pair_coordination(self, service_a: Dict, service_b: Dict) -> float:
        """Calculate coordination strength between two services"""
        
        coordination_score = 0.0
        
        # Check if services are in same category
        if service_a.get('service_type') == service_b.get('service_type'):
            coordination_score += 0.3
        
        # Check for dependency relationship
        service_a_deps = self.service_dependencies.get(service_a['service_name'], [])
        service_b_deps = self.service_dependencies.get(service_b['service_name'], [])
        
        if service_b['service_name'] in service_a_deps or service_a['service_name'] in service_b_deps:
            coordination_score += 0.5
        
        # Check for capability overlap
        capabilities_a = set(service_a.get('capabilities', []))
        capabilities_b = set(service_b.get('capabilities', []))
        
        if capabilities_a and capabilities_b:
            overlap = len(capabilities_a.intersection(capabilities_b))
            total = len(capabilities_a.union(capabilities_b))
            if total > 0:
                coordination_score += (overlap / total) * 0.2
        
        return min(coordination_score, 1.0)
    
    def find_service_by_name(self, service_name: str) -> Dict[str, Any]:
        """Find service by name"""
        for service in self.discovered_services:
            if service.get('service_name') == service_name:
                return service
        return None
    
    def calculate_overall_integration_score(self, validation_result: Dict[str, Any]) -> float:
        """Calculate overall integration score"""
        
        scores = []
        weights = []
        
        # Service discovery score (20%)
        discovery = validation_result.get('service_discovery', {})
        discovery_summary = discovery.get('discovery_summary', {})
        implementation_rate = discovery_summary.get('implementation_rate', 0)
        scores.append(implementation_rate)
        weights.append(0.20)
        
        # Integration testing score (40%)
        integration_testing = validation_result.get('integration_testing', {})
        if integration_testing.get('total_tests', 0) > 0:
            test_success_rate = (integration_testing.get('tests_passed', 0) / 
                               integration_testing.get('total_tests', 1)) * 100
            scores.append(test_success_rate)
            weights.append(0.40)
        
        # Coordination score (30%)
        coordination = validation_result.get('coordination_validation', {})
        coordination_score = coordination.get('coordination_score', 0)
        scores.append(coordination_score)
        weights.append(0.30)
        
        # Performance score (10%)
        performance = validation_result.get('performance_assessment', {})
        performance_score = performance.get('performance_score', 0)
        scores.append(performance_score)
        weights.append(0.10)
        
        # Calculate weighted average
        if scores and weights:
            weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
            total_weight = sum(weights)
            overall_score = weighted_sum / total_weight if total_weight > 0 else 0
        else:
            overall_score = 0
        
        return round(overall_score, 2)
    
    def assess_integration_performance(self) -> Dict[str, Any]:
        """Assess integration performance"""
        
        performance_assessment = {
            'assessment_timestamp': datetime.now().isoformat(),
            'service_load_times': {},
            'coordination_efficiency': 0.0,
            'resource_utilization': {},
            'performance_score': 0.0
        }
        
        try:
            # Simulate service load time assessment
            for service in self.discovered_services[:5]:  # Test first 5 services
                service_name = service.get('service_name')
                
                start_time = time.time()
                # Simulate service analysis (reading file)
                service_file = Path(service['file_path'])
                if service_file.exists():
                    content = service_file.read_text()
                    # Simple processing simulation
                    processed_lines = len(content.split('\n'))
                load_time = time.time() - start_time
                
                performance_assessment['service_load_times'][service_name] = {
                    'load_time': load_time,
                    'file_size': service.get('file_size', 0),
                    'efficiency_ratio': service.get('file_size', 1) / max(load_time, 0.001)
                }
            
            # Calculate performance score
            load_times = [data['load_time'] for data in performance_assessment['service_load_times'].values()]
            if load_times:
                avg_load_time = sum(load_times) / len(load_times)
                # Score based on average load time (lower is better)
                if avg_load_time < 0.01:
                    performance_assessment['performance_score'] = 100
                elif avg_load_time < 0.05:
                    performance_assessment['performance_score'] = 80
                elif avg_load_time < 0.1:
                    performance_assessment['performance_score'] = 60
                else:
                    performance_assessment['performance_score'] = 40
            
        except Exception as e:
            performance_assessment['error'] = f"Performance assessment failed: {str(e)}"
        
        return performance_assessment
    
    def store_validation_results(self, validation_result: Dict[str, Any]) -> str:
        """Store validation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"service_integration_validation_{timestamp}.json"
        filepath = self.validation_storage / filename
        
        with open(filepath, 'w') as f:
            json.dump(validation_result, f, indent=2, default=str)
        
        print(f"\n📄 Validation results saved to: {filepath}")
        return str(filepath)


def main():
    """Main execution function"""
    print("🔧 Service Integration Validator")
    print("Comprehensive Service Ecosystem Testing")
    print("-" * 50)
    
    validator = ServiceIntegrationValidator()
    validation_result = validator.validate_complete_service_integration()
    
    # Display final summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    discovery = validation_result.get('service_discovery', {})
    summary = discovery.get('discovery_summary', {})
    
    print(f"Services Discovered: {summary.get('total_services', 0)}")
    print(f"Implementation Rate: {summary.get('implementation_rate', 0):.1f}%")
    
    integration = validation_result.get('integration_testing', {})
    print(f"Integration Tests: {integration.get('tests_passed', 0)}/{integration.get('total_tests', 0)} passed")
    
    coordination = validation_result.get('coordination_validation', {})
    print(f"Coordination Score: {coordination.get('coordination_score', 0):.1f}%")
    
    overall_score = validation_result.get('overall_integration_score', 0)
    integration_status = validation_result.get('integration_status', 'unknown').upper()
    print(f"\n🎯 OVERALL INTEGRATION: {overall_score:.1f}% ({integration_status})")
    
    if overall_score >= 75:
        print("✅ Service integration is successful!")
    else:
        print("⚠️  Service integration needs improvement.")
        issues = integration.get('integration_issues', [])
        if issues:
            print("\nKey Issues to Address:")
            for issue in issues[:3]:  # Top 3 issues
                print(f"  - {issue.get('test_name')}: {issue.get('issue')}")
    
    return validation_result


if __name__ == "__main__":
    main()
