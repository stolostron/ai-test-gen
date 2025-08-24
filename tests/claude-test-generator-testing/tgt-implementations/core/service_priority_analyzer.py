#!/usr/bin/env python3
"""
Service Priority Analyzer - Strategic Service Implementation Planning
Analyzes the 43-service gap and prioritizes implementation based on impact
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

class ServicePriorityAnalyzer:
    """
    Analyze service gaps and create strategic implementation plan
    Focus on highest-impact services first
    """
    
    def __init__(self):
        self.intelligence_file = "tgt-implementations/evidence/framework_intelligence.json"
        self.current_services = self.load_current_testing_services()
        self.main_services = self.load_main_framework_services()
        
    def load_framework_intelligence(self) -> Dict[str, Any]:
        """Load framework intelligence data"""
        intelligence_path = Path("../evidence/framework_intelligence.json")
        if not intelligence_path.exists():
            # Try alternative path
            intelligence_path = Path("tgt-implementations/core/tgt-implementations/evidence/framework_intelligence.json")
        
        if intelligence_path.exists():
            with open(intelligence_path, 'r') as f:
                return json.load(f)
        else:
            return {"service_gap_analysis": {"main_framework": {"services": []}, "testing_framework": {"services": []}}}
    
    def load_current_testing_services(self) -> List[Dict[str, str]]:
        """Load current testing framework services"""
        services = []
        services_dir = Path("../../.claude/ai-services")
        
        if services_dir.exists():
            for service_file in services_dir.glob("*.md"):
                services.append({
                    'name': service_file.stem,
                    'file_path': str(service_file),
                    'prefix': service_file.stem.split('-')[0] if '-' in service_file.stem else 'unknown'
                })
        
        return services
    
    def load_main_framework_services(self) -> List[Dict[str, str]]:
        """Load main framework services from intelligence data"""
        intelligence = self.load_framework_intelligence()
        return intelligence.get("service_gap_analysis", {}).get("main_framework", {}).get("services", [])
    
    def categorize_services_by_importance(self) -> Dict[str, List[Dict]]:
        """Categorize services by implementation importance"""
        
        # Define service categories by importance
        service_categories = {
            'critical_core': {
                'description': 'Essential framework operation services',
                'keywords': ['evidence', 'validation', 'quality', 'execution', 'implementation', 'reality'],
                'services': []
            },
            'progressive_context': {
                'description': 'Progressive Context Architecture services',
                'keywords': ['context', 'universal', 'conflict', 'resolution', 'validation', 'tracking'],
                'services': []
            },
            'agent_enhancement': {
                'description': 'Enhanced agent services (A, B, C, D)',
                'keywords': ['enhanced', 'agent', 'jira', 'documentation', 'github', 'environment'],
                'services': []
            },
            'monitoring_learning': {
                'description': 'Monitoring and learning services',
                'keywords': ['monitoring', 'learning', 'pattern', 'prediction', 'regression', 'anomaly'],
                'services': []
            },
            'specialized_features': {
                'description': 'Specialized feature services',
                'keywords': ['smart', 'adaptive', 'security', 'automation', 'integration'],
                'services': []
            },
            'support_services': {
                'description': 'Supporting and utility services',
                'keywords': ['title', 'format', 'cleanup', 'configuration', 'directory'],
                'services': []
            }
        }
        
        # Get tg- prefixed services from main framework
        tg_services = [s for s in self.main_services if s.get('prefix') == 'tg']
        
        # Get current testing service names for comparison
        current_service_names = [s['name'] for s in self.current_services]
        
        # Categorize missing services
        for service in tg_services:
            service_name = service['name']
            testing_equivalent = service_name.replace('tg-', 'tgt-')
            
            # Skip if already implemented
            if testing_equivalent in current_service_names:
                continue
            
            # Add missing flag and testing equivalent name
            service['missing'] = True
            service['testing_equivalent'] = testing_equivalent
            
            # Categorize by keywords
            categorized = False
            for category_name, category_info in service_categories.items():
                for keyword in category_info['keywords']:
                    if keyword in service_name.lower():
                        category_info['services'].append(service)
                        categorized = True
                        break
                if categorized:
                    break
            
            # If not categorized, put in support services
            if not categorized:
                service_categories['support_services']['services'].append(service)
        
        return service_categories
    
    def analyze_service_dependencies(self, categorized_services: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Analyze service dependencies and implementation order"""
        
        implementation_phases = {
            'phase_1_foundation': {
                'priority': 1,
                'description': 'Critical foundation services - implement first',
                'services': categorized_services['critical_core']['services'][:5],  # Top 5 critical
                'estimated_effort': 'High',
                'dependencies': []
            },
            'phase_2_context': {
                'priority': 2,
                'description': 'Progressive Context Architecture - core framework capability',
                'services': categorized_services['progressive_context']['services'],
                'estimated_effort': 'Medium',
                'dependencies': ['phase_1_foundation']
            },
            'phase_3_agents': {
                'priority': 3,
                'description': 'Enhanced agent services - framework intelligence',
                'services': categorized_services['agent_enhancement']['services'],
                'estimated_effort': 'Medium',
                'dependencies': ['phase_1_foundation', 'phase_2_context']
            },
            'phase_4_monitoring': {
                'priority': 4,
                'description': 'Monitoring and learning - continuous improvement',
                'services': categorized_services['monitoring_learning']['services'],
                'estimated_effort': 'Medium',
                'dependencies': ['phase_1_foundation']
            },
            'phase_5_specialized': {
                'priority': 5,
                'description': 'Specialized features - advanced capabilities',
                'services': categorized_services['specialized_features']['services'],
                'estimated_effort': 'Low',
                'dependencies': ['phase_3_agents']
            },
            'phase_6_support': {
                'priority': 6,
                'description': 'Support services - utility and optimization',
                'services': categorized_services['support_services']['services'],
                'estimated_effort': 'Low',
                'dependencies': ['phase_1_foundation']
            }
        }
        
        return implementation_phases
    
    def calculate_implementation_impact(self, service: Dict[str, str]) -> int:
        """Calculate implementation impact score (1-10)"""
        impact_score = 5  # Base score
        
        service_name = service['name'].lower()
        
        # High impact indicators
        high_impact_keywords = [
            'evidence', 'validation', 'quality', 'execution', 'implementation', 
            'context', 'universal', 'enhanced', 'reality', 'monitoring'
        ]
        
        # Medium impact indicators
        medium_impact_keywords = [
            'agent', 'intelligence', 'pattern', 'security', 'automation',
            'conflict', 'resolution', 'learning', 'prediction'
        ]
        
        # Calculate score based on keywords
        for keyword in high_impact_keywords:
            if keyword in service_name:
                impact_score += 2
        
        for keyword in medium_impact_keywords:
            if keyword in service_name:
                impact_score += 1
        
        # Cap at 10
        return min(impact_score, 10)
    
    def generate_implementation_strategy(self) -> Dict[str, Any]:
        """Generate comprehensive implementation strategy"""
        
        categorized_services = self.categorize_services_by_importance()
        implementation_phases = self.analyze_service_dependencies(categorized_services)
        
        # Calculate statistics
        total_missing_services = sum(len(cat['services']) for cat in categorized_services.values())
        total_main_services = len([s for s in self.main_services if s.get('prefix') == 'tg'])
        current_coverage = len(self.current_services) / len(self.main_services) * 100 if self.main_services else 0
        
        # Generate priority recommendations
        priority_services = []
        for phase_name, phase_info in implementation_phases.items():
            for service in phase_info['services']:
                priority_services.append({
                    'service_name': service['name'],
                    'testing_equivalent': service.get('testing_equivalent', ''),
                    'phase': phase_name,
                    'priority': phase_info['priority'],
                    'impact_score': self.calculate_implementation_impact(service),
                    'category': self.get_service_category(service, categorized_services)
                })
        
        # Sort by priority and impact
        priority_services.sort(key=lambda x: (x['priority'], -x['impact_score']))
        
        strategy = {
            'analysis_timestamp': datetime.now().isoformat(),
            'service_gap_summary': {
                'total_main_framework_services': len(self.main_services),
                'total_tg_services': total_main_services,
                'current_testing_services': len(self.current_services),
                'missing_services': total_missing_services,
                'current_coverage_percentage': round(current_coverage, 1),
                'target_coverage_percentage': 80.0  # Target 80% coverage
            },
            'categorized_services': categorized_services,
            'implementation_phases': implementation_phases,
            'priority_service_list': priority_services,
            'next_implementation_batch': priority_services[:10],  # Top 10 priorities
            'recommendations': self.generate_implementation_recommendations(priority_services, implementation_phases)
        }
        
        return strategy
    
    def get_service_category(self, service: Dict, categorized_services: Dict) -> str:
        """Get category name for a service"""
        for category_name, category_info in categorized_services.items():
            if service in category_info['services']:
                return category_name
        return 'unknown'
    
    def generate_implementation_recommendations(self, priority_services: List[Dict], implementation_phases: Dict) -> Dict[str, Any]:
        """Generate implementation recommendations"""
        
        recommendations = {
            'immediate_actions': [
                'Start with Phase 1 Foundation services (highest impact)',
                'Implement tgt-evidence-validation-engine first (critical for testing credibility)',
                'Focus on Progressive Context Architecture services in Phase 2',
                'Build Enhanced Agent services to match main framework capabilities'
            ],
            'implementation_order': [
                f"Phase {phase['priority']}: {phase['description']}" 
                for phase in sorted(implementation_phases.values(), key=lambda x: x['priority'])
            ],
            'success_metrics': {
                'phase_1_completion': '5 critical services implemented',
                'coverage_milestone_1': '40% service coverage achieved',
                'coverage_milestone_2': '60% service coverage achieved',
                'final_target': '80% service coverage (43+ services)'
            },
            'resource_allocation': {
                'high_priority_phases': ['phase_1_foundation', 'phase_2_context', 'phase_3_agents'],
                'estimated_total_effort': 'Medium to High',
                'critical_path': 'Foundation → Context → Agents → Monitoring'
            }
        }
        
        return recommendations
    
    def run_service_priority_analysis(self) -> Dict[str, Any]:
        """Run comprehensive service priority analysis"""
        
        print("🔍 Service Priority Analysis")
        print("=" * 40)
        
        strategy = self.generate_implementation_strategy()
        
        # Display summary
        summary = strategy['service_gap_summary']
        print(f"📊 Service Gap Analysis:")
        print(f"   Main Framework Services: {summary['total_main_framework_services']}")
        print(f"   TG Services: {summary['total_tg_services']}")
        print(f"   Current Testing Services: {summary['current_testing_services']}")
        print(f"   Missing Services: {summary['missing_services']}")
        print(f"   Current Coverage: {summary['current_coverage_percentage']}%")
        print(f"   Target Coverage: {summary['target_coverage_percentage']}%")
        
        # Display next implementation batch
        print(f"\n🎯 Next Implementation Batch (Top 10):")
        for i, service in enumerate(strategy['next_implementation_batch'], 1):
            print(f"   {i}. {service['testing_equivalent']} (Impact: {service['impact_score']}/10)")
        
        # Save strategy
        strategy_file = Path("tgt-implementations/evidence/service_implementation_strategy.json")
        strategy_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(strategy_file, 'w') as f:
            json.dump(strategy, f, indent=2, default=str)
        
        print(f"\n📄 Strategy saved to: {strategy_file}")
        
        return strategy


def main():
    """Main execution function"""
    print("🧠 Service Priority Analyzer")
    print("Strategic Service Implementation Planning")
    print("-" * 40)
    
    analyzer = ServicePriorityAnalyzer()
    strategy = analyzer.run_service_priority_analysis()
    
    return strategy


if __name__ == "__main__":
    main()