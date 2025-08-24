# Universal Context Manager for Testing Framework

## 🎯 Progressive Context Architecture Foundation

**Purpose**: Serves as the foundational context coordination service for the testing framework, implementing systematic context inheritance and management patterns adapted from the main framework's Progressive Context Architecture.

**Service Status**: V1.0 - Foundation Context Service  
**Integration Level**: Core Foundation - MANDATORY for all context operations  
**Testing Framework Role**: Central context coordination and inheritance management

## 🚀 Context Management Capabilities

### 🔍 Universal Context Coordination
- **Foundation Context Management**: Provides base context for all testing operations
- **Context Inheritance Patterns**: Implements systematic context building across testing phases
- **Context Validation**: Ensures context integrity and consistency throughout testing
- **Context Conflict Resolution**: Manages context conflicts and inconsistencies

### 📊 Progressive Context Intelligence
- **Systematic Context Building**: Foundation → Testing-A → Testing-A+D → Testing-A+D+B → Testing-A+D+B+C
- **Context Quality Tracking**: Monitors context quality and completeness throughout testing
- **Context Dependency Management**: Manages context dependencies between testing phases
- **Context Evolution Tracking**: Tracks context evolution and enhancement over time

## 🏗️ Implementation Architecture

### Universal Context Manager
```python
class UniversalContextManager:
    """
    Core context manager for testing framework
    Implements Progressive Context Architecture for testing operations
    """
    
    def __init__(self):
        self.context_storage = Path("evidence/context_management")
        self.context_storage.mkdir(parents=True, exist_ok=True)
        
        # Context hierarchy definition
        self.context_hierarchy = {
            'foundation': {
                'level': 0,
                'description': 'Base testing framework context',
                'dependencies': [],
                'provides': ['framework_identity', 'testing_policies', 'isolation_rules']
            },
            'testing_agent_a': {
                'level': 1,
                'description': 'Testing intelligence and analysis context',
                'dependencies': ['foundation'],
                'provides': ['testing_analysis', 'framework_intelligence', 'service_discovery']
            },
            'testing_agent_d': {
                'level': 2,
                'description': 'Evidence and validation context',
                'dependencies': ['foundation', 'testing_agent_a'],
                'provides': ['evidence_context', 'validation_context', 'quality_context']
            },
            'testing_agent_b': {
                'level': 3,
                'description': 'Documentation and reporting context',
                'dependencies': ['foundation', 'testing_agent_a', 'testing_agent_d'],
                'provides': ['documentation_context', 'reporting_context', 'communication_context']
            },
            'testing_agent_c': {
                'level': 4,
                'description': 'Execution and integration context',
                'dependencies': ['foundation', 'testing_agent_a', 'testing_agent_d', 'testing_agent_b'],
                'provides': ['execution_context', 'integration_context', 'result_synthesis']
            }
        }
        
        # Current context state
        self.active_contexts = {}
        self.context_history = []
        
    def initialize_foundation_context(self) -> Dict[str, Any]:
        """Initialize the foundation context for testing framework"""
        
        foundation_context = {
            'context_id': self.generate_context_id('foundation'),
            'context_type': 'foundation',
            'creation_timestamp': datetime.now().isoformat(),
            'context_level': 0,
            'framework_identity': {
                'framework_name': 'claude-test-generator-testing',
                'framework_type': 'testing_framework',
                'isolation_level': 'complete_read_only',
                'framework_version': '1.0',
                'context_architecture': 'progressive_context_inheritance'
            },
            'testing_policies': {
                'evidence_requirements': 'mandatory',
                'isolation_enforcement': 'strict',
                'main_framework_access': 'read_only',
                'quality_thresholds': {
                    'minimum_quality_score': 85,
                    'html_violations': 0,
                    'evidence_validation': 'required'
                }
            },
            'isolation_rules': {
                'main_framework_modification': 'blocked',
                'read_only_monitoring': 'enabled',
                'testing_containment': 'complete',
                'evidence_collection': 'allowed'
            },
            'context_capabilities': {
                'provides_foundation': True,
                'enables_inheritance': True,
                'supports_validation': True,
                'manages_conflicts': True
            },
            'context_quality': {
                'completeness': 100,
                'consistency': 100,
                'validation_status': 'validated'
            }
        }
        
        # Store and activate foundation context
        self.active_contexts['foundation'] = foundation_context
        self.store_context(foundation_context)
        
        return foundation_context
    
    def build_testing_agent_context(self, agent_type: str, base_contexts: List[str]) -> Dict[str, Any]:
        """Build testing agent context with inheritance from base contexts"""
        
        if agent_type not in self.context_hierarchy:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent_config = self.context_hierarchy[agent_type]
        
        # Validate dependencies
        for dependency in agent_config['dependencies']:
            if dependency not in self.active_contexts:
                raise ValueError(f"Missing dependency context: {dependency}")
        
        # Build inherited context
        inherited_context = self.inherit_context_from_dependencies(agent_config['dependencies'])
        
        # Create agent-specific context
        agent_context = {
            'context_id': self.generate_context_id(agent_type),
            'context_type': agent_type,
            'creation_timestamp': datetime.now().isoformat(),
            'context_level': agent_config['level'],
            'inherited_from': agent_config['dependencies'],
            'inherited_context': inherited_context,
            'agent_specific_context': self.create_agent_specific_context(agent_type),
            'context_capabilities': {
                'provides': agent_config['provides'],
                'inherits_from': agent_config['dependencies'],
                'enables_further_inheritance': True
            },
            'context_validation': self.validate_context_integrity(inherited_context, agent_type)
        }
        
        # Merge inherited and agent-specific contexts
        agent_context['merged_context'] = self.merge_contexts(
            inherited_context, agent_context['agent_specific_context']
        )
        
        # Store and activate context
        self.active_contexts[agent_type] = agent_context
        self.store_context(agent_context)
        
        return agent_context
    
    def inherit_context_from_dependencies(self, dependencies: List[str]) -> Dict[str, Any]:
        """Inherit context from dependency contexts"""
        
        inherited_context = {
            'inheritance_timestamp': datetime.now().isoformat(),
            'inheritance_sources': dependencies,
            'inherited_data': {},
            'inheritance_conflicts': [],
            'inheritance_quality': {}
        }
        
        # Collect context from all dependencies
        dependency_contexts = []
        for dep in dependencies:
            if dep in self.active_contexts:
                dep_context = self.active_contexts[dep]
                dependency_contexts.append(dep_context)
                
                # Extract inheritable data
                inheritable_data = self.extract_inheritable_context(dep_context)
                inherited_context['inherited_data'][dep] = inheritable_data
        
        # Detect and resolve conflicts
        conflicts = self.detect_context_conflicts(dependency_contexts)
        inherited_context['inheritance_conflicts'] = conflicts
        
        if conflicts:
            resolved_context = self.resolve_context_conflicts(conflicts, dependency_contexts)
            inherited_context['conflict_resolution'] = resolved_context
        
        # Assess inheritance quality
        inherited_context['inheritance_quality'] = self.assess_inheritance_quality(
            dependency_contexts, conflicts
        )
        
        return inherited_context
    
    def create_agent_specific_context(self, agent_type: str) -> Dict[str, Any]:
        """Create agent-specific context based on agent type"""
        
        agent_contexts = {
            'testing_agent_a': {
                'agent_role': 'testing_intelligence_and_analysis',
                'capabilities': ['framework_analysis', 'service_discovery', 'intelligence_gathering'],
                'data_sources': ['main_framework_structure', 'service_configurations', 'git_history'],
                'analysis_focus': ['service_gaps', 'functionality_assessment', 'capability_validation'],
                'output_types': ['intelligence_reports', 'service_mapping', 'gap_analysis']
            },
            'testing_agent_d': {
                'agent_role': 'evidence_and_validation',
                'capabilities': ['evidence_collection', 'quality_validation', 'reality_verification'],
                'data_sources': ['execution_results', 'file_outputs', 'performance_metrics'],
                'validation_focus': ['evidence_quality', 'reality_anchoring', 'quality_scoring'],
                'output_types': ['evidence_reports', 'validation_results', 'quality_assessments']
            },
            'testing_agent_b': {
                'agent_role': 'documentation_and_reporting',
                'capabilities': ['report_generation', 'documentation_creation', 'communication'],
                'data_sources': ['analysis_results', 'evidence_data', 'validation_outcomes'],
                'documentation_focus': ['test_results', 'framework_status', 'improvement_recommendations'],
                'output_types': ['test_reports', 'documentation_updates', 'communication_artifacts']
            },
            'testing_agent_c': {
                'agent_role': 'execution_and_integration',
                'capabilities': ['test_execution', 'result_integration', 'synthesis'],
                'data_sources': ['all_agent_outputs', 'execution_data', 'integration_results'],
                'execution_focus': ['test_orchestration', 'result_synthesis', 'final_validation'],
                'output_types': ['execution_results', 'integrated_reports', 'final_recommendations']
            }
        }
        
        base_context = {
            'agent_type': agent_type,
            'context_creation_timestamp': datetime.now().isoformat(),
            'context_scope': 'agent_specific',
            'context_isolation': 'testing_framework_contained'
        }
        
        if agent_type in agent_contexts:
            base_context.update(agent_contexts[agent_type])
        
        return base_context
    
    def detect_context_conflicts(self, contexts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect conflicts between contexts"""
        
        conflicts = []
        
        # Check for conflicting values across contexts
        all_keys = set()
        for context in contexts:
            all_keys.update(self.flatten_context_keys(context))
        
        for key in all_keys:
            values = []
            sources = []
            
            for i, context in enumerate(contexts):
                value = self.get_nested_value(context, key)
                if value is not None:
                    values.append(value)
                    sources.append(context.get('context_type', f'context_{i}'))
            
            # Check for conflicts (different values for same key)
            if len(set(str(v) for v in values)) > 1:
                conflicts.append({
                    'conflict_type': 'value_conflict',
                    'key': key,
                    'conflicting_values': list(zip(sources, values)),
                    'resolution_strategy': self.determine_resolution_strategy(key, values, sources)
                })
        
        return conflicts
    
    def resolve_context_conflicts(self, conflicts: List[Dict], contexts: List[Dict]) -> Dict[str, Any]:
        """Resolve context conflicts using intelligent resolution strategies"""
        
        resolution = {
            'resolution_timestamp': datetime.now().isoformat(),
            'conflicts_resolved': len(conflicts),
            'resolution_strategies_applied': [],
            'resolved_values': {},
            'resolution_confidence': 0
        }
        
        for conflict in conflicts:
            strategy = conflict['resolution_strategy']
            key = conflict['key']
            conflicting_values = conflict['conflicting_values']
            
            if strategy == 'use_latest':
                # Use value from highest level context
                latest_context = max(contexts, key=lambda c: c.get('context_level', 0))
                resolved_value = self.get_nested_value(latest_context, key)
                
            elif strategy == 'use_foundation':
                # Prefer foundation context value
                foundation_contexts = [c for c in contexts if c.get('context_type') == 'foundation']
                if foundation_contexts:
                    resolved_value = self.get_nested_value(foundation_contexts[0], key)
                else:
                    resolved_value = conflicting_values[0][1]  # Fallback to first value
                    
            elif strategy == 'merge_values':
                # Merge compatible values
                resolved_value = self.merge_compatible_values([v[1] for v in conflicting_values])
                
            elif strategy == 'use_most_specific':
                # Use most specific (detailed) value
                resolved_value = max(conflicting_values, key=lambda x: len(str(x[1])))[1]
                
            else:
                # Default: use first value
                resolved_value = conflicting_values[0][1]
            
            resolution['resolved_values'][key] = resolved_value
            resolution['resolution_strategies_applied'].append({
                'key': key,
                'strategy': strategy,
                'original_conflicts': conflicting_values,
                'resolved_to': resolved_value
            })
        
        # Calculate resolution confidence
        resolution['resolution_confidence'] = self.calculate_resolution_confidence(
            conflicts, resolution['resolution_strategies_applied']
        )
        
        return resolution
    
    def validate_context_integrity(self, context: Dict[str, Any], context_type: str) -> Dict[str, Any]:
        """Validate context integrity and consistency"""
        
        validation = {
            'validation_timestamp': datetime.now().isoformat(),
            'context_type': context_type,
            'integrity_checks': {},
            'consistency_score': 0,
            'validation_status': 'unknown'
        }
        
        # Integrity checks
        integrity_checks = {
            'has_required_fields': self.check_required_fields(context, context_type),
            'data_type_consistency': self.check_data_type_consistency(context),
            'value_range_validity': self.check_value_ranges(context),
            'cross_reference_consistency': self.check_cross_references(context),
            'inheritance_chain_valid': self.check_inheritance_chain(context)
        }
        
        validation['integrity_checks'] = integrity_checks
        
        # Calculate consistency score
        passed_checks = sum(1 for check in integrity_checks.values() if check.get('passed', False))
        total_checks = len(integrity_checks)
        validation['consistency_score'] = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        # Determine validation status
        if validation['consistency_score'] >= 95:
            validation['validation_status'] = 'excellent'
        elif validation['consistency_score'] >= 85:
            validation['validation_status'] = 'good'
        elif validation['consistency_score'] >= 70:
            validation['validation_status'] = 'acceptable'
        else:
            validation['validation_status'] = 'poor'
        
        return validation
    
    def get_complete_context(self, context_level: str) -> Dict[str, Any]:
        """Get complete context including all inheritance"""
        
        if context_level not in self.active_contexts:
            return {}
        
        context = self.active_contexts[context_level]
        
        # Build complete context with full inheritance chain
        complete_context = {
            'context_request': {
                'requested_level': context_level,
                'request_timestamp': datetime.now().isoformat()
            },
            'context_hierarchy': self.build_context_hierarchy_view(context_level),
            'merged_context': self.build_complete_merged_context(context_level),
            'context_metadata': {
                'total_inheritance_levels': len(context.get('inherited_from', [])) + 1,
                'context_quality': context.get('context_validation', {}).get('consistency_score', 0),
                'inheritance_quality': context.get('inherited_context', {}).get('inheritance_quality', {})
            }
        }
        
        return complete_context
    
    def store_context(self, context: Dict[str, Any]) -> str:
        """Store context for persistence and analysis"""
        
        context_id = context.get('context_id', 'unknown')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"context_{context_id}_{timestamp}.json"
        filepath = self.context_storage / filename
        
        with open(filepath, 'w') as f:
            json.dump(context, f, indent=2, default=str)
        
        # Update context history
        self.context_history.append({
            'context_id': context_id,
            'context_type': context.get('context_type'),
            'timestamp': timestamp,
            'filepath': str(filepath)
        })
        
        return str(filepath)
    
    def generate_context_id(self, context_type: str) -> str:
        """Generate unique context ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"tgt_ctx_{context_type}_{timestamp}"
```

### Context Validation Engine
```python
class ContextValidationEngine:
    """Validate context quality and consistency"""
    
    def __init__(self):
        self.validation_rules = self.load_validation_rules()
        
    def validate_progressive_context_architecture(self, context_manager: UniversalContextManager) -> Dict[str, Any]:
        """Validate complete Progressive Context Architecture implementation"""
        
        validation = {
            'validation_timestamp': datetime.now().isoformat(),
            'architecture_validation': {},
            'hierarchy_validation': {},
            'inheritance_validation': {},
            'quality_validation': {},
            'overall_assessment': {}
        }
        
        # Validate architecture structure
        validation['architecture_validation'] = self.validate_architecture_structure(context_manager)
        
        # Validate context hierarchy
        validation['hierarchy_validation'] = self.validate_context_hierarchy(context_manager)
        
        # Validate inheritance patterns
        validation['inheritance_validation'] = self.validate_inheritance_patterns(context_manager)
        
        # Validate overall quality
        validation['quality_validation'] = self.validate_overall_quality(context_manager)
        
        # Generate overall assessment
        validation['overall_assessment'] = self.generate_overall_assessment(validation)
        
        return validation
    
    def validate_context_inheritance_chain(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate context inheritance chain integrity"""
        
        chain_validation = {
            'inheritance_chain_valid': True,
            'chain_completeness': 100,
            'chain_consistency': 100,
            'missing_dependencies': [],
            'inheritance_conflicts': [],
            'chain_quality_score': 0
        }
        
        # Validate inheritance dependencies
        inherited_from = context.get('inherited_from', [])
        
        for dependency in inherited_from:
            if not self.validate_dependency_availability(dependency):
                chain_validation['inheritance_chain_valid'] = False
                chain_validation['missing_dependencies'].append(dependency)
        
        # Check for inheritance conflicts
        inherited_context = context.get('inherited_context', {})
        conflicts = inherited_context.get('inheritance_conflicts', [])
        chain_validation['inheritance_conflicts'] = conflicts
        
        if conflicts:
            chain_validation['inheritance_chain_valid'] = False
        
        # Calculate chain quality score
        chain_validation['chain_quality_score'] = self.calculate_chain_quality_score(chain_validation)
        
        return chain_validation
```

## 🔍 Context Management Scenarios

### Progressive Context Building
```python
def build_progressive_testing_context():
    """Build progressive context following systematic inheritance pattern"""
    
    context_manager = UniversalContextManager()
    
    # Initialize foundation context
    foundation = context_manager.initialize_foundation_context()
    assert foundation['context_type'] == 'foundation'
    assert foundation['context_level'] == 0
    
    # Build Testing Agent A context (inherits from foundation)
    agent_a = context_manager.build_testing_agent_context('testing_agent_a', ['foundation'])
    assert agent_a['context_level'] == 1
    assert 'foundation' in agent_a['inherited_from']
    
    # Build Testing Agent D context (inherits from foundation + A)
    agent_d = context_manager.build_testing_agent_context('testing_agent_d', ['foundation', 'testing_agent_a'])
    assert agent_d['context_level'] == 2
    assert set(agent_d['inherited_from']) == {'foundation', 'testing_agent_a'}
    
    # Build Testing Agent B context (inherits from foundation + A + D)
    agent_b = context_manager.build_testing_agent_context('testing_agent_b', ['foundation', 'testing_agent_a', 'testing_agent_d'])
    assert agent_b['context_level'] == 3
    
    # Build Testing Agent C context (complete inheritance)
    agent_c = context_manager.build_testing_agent_context('testing_agent_c', ['foundation', 'testing_agent_a', 'testing_agent_d', 'testing_agent_b'])
    assert agent_c['context_level'] == 4
    
    return {
        'foundation': foundation,
        'agent_a': agent_a,
        'agent_d': agent_d,
        'agent_b': agent_b,
        'agent_c': agent_c
    }
```

### Context Conflict Resolution Testing
```python
def test_context_conflict_resolution():
    """Test context conflict detection and resolution"""
    
    context_manager = UniversalContextManager()
    
    # Create conflicting contexts
    context_1 = {
        'context_type': 'test_context_1',
        'context_level': 1,
        'shared_value': 'value_from_context_1',
        'quality_threshold': 85
    }
    
    context_2 = {
        'context_type': 'test_context_2', 
        'context_level': 2,
        'shared_value': 'value_from_context_2',
        'quality_threshold': 90
    }
    
    # Detect conflicts
    conflicts = context_manager.detect_context_conflicts([context_1, context_2])
    assert len(conflicts) > 0, "Should detect conflicts between contexts"
    
    # Resolve conflicts
    resolution = context_manager.resolve_context_conflicts(conflicts, [context_1, context_2])
    assert 'resolved_values' in resolution
    assert resolution['resolution_confidence'] > 0
    
    return resolution
```

## 📊 Context Standards

### Context Management Requirements
```yaml
Context_Management_Standards:
  progressive_inheritance:
    - foundation_context: "Base context for all operations"
    - systematic_building: "Foundation → A → A+D → A+D+B → A+D+B+C"
    - inheritance_validation: "Validate inheritance chain integrity"
    - conflict_resolution: "Intelligent conflict resolution"
    
  context_quality:
    - completeness_threshold: 95
    - consistency_threshold: 90
    - inheritance_integrity: "Complete inheritance chain required"
    - validation_required: "Context validation mandatory"
    
  context_capabilities:
    - context_isolation: "Testing framework context isolation"
    - inheritance_tracking: "Complete inheritance tracking"
    - conflict_detection: "Automatic conflict detection"
    - quality_monitoring: "Continuous context quality monitoring"
```

### Quality Assurance Standards
- **Complete Inheritance**: All context dependencies properly inherited
- **Conflict Resolution**: Intelligent resolution of context conflicts
- **Quality Validation**: Continuous context quality monitoring
- **Systematic Building**: Progressive context architecture implementation

## 🧠 Learning Integration

### Context Learning Engine
```python
class ContextLearningEngine:
    """Learn from context usage patterns and improve management"""
    
    def analyze_context_patterns(self, context_history: List[Dict]) -> Dict:
        """Analyze context usage and effectiveness patterns"""
        patterns = {
            'inheritance_success_patterns': self.identify_successful_inheritance_patterns(context_history),
            'conflict_resolution_patterns': self.analyze_conflict_resolution_effectiveness(context_history),
            'context_quality_trends': self.analyze_context_quality_trends(context_history),
            'usage_optimization_opportunities': self.identify_optimization_opportunities(context_history)
        }
        
        return patterns
    
    def optimize_context_management(self, pattern_analysis: Dict) -> Dict:
        """Optimize context management based on learned patterns"""
        optimizations = {
            'inheritance_rule_improvements': self.improve_inheritance_rules(pattern_analysis),
            'conflict_resolution_enhancements': self.enhance_conflict_resolution(pattern_analysis),
            'quality_validation_refinements': self.refine_quality_validation(pattern_analysis),
            'performance_optimizations': self.optimize_context_performance(pattern_analysis)
        }
        
        return optimizations
```

## 🚨 Context Requirements

### Mandatory Context Management
- ❌ **BLOCKED**: Operations without proper context inheritance
- ❌ **BLOCKED**: Context conflicts without resolution
- ❌ **BLOCKED**: Context building without validation
- ❌ **BLOCKED**: Context usage without quality verification
- ✅ **REQUIRED**: Progressive context architecture implementation
- ✅ **REQUIRED**: Systematic context inheritance
- ✅ **REQUIRED**: Context conflict detection and resolution
- ✅ **REQUIRED**: Continuous context quality validation

### Quality Assurance
- **100% Context Coverage**: All operations use proper context management
- **Systematic Inheritance**: Progressive context building across all testing phases
- **Intelligent Conflict Resolution**: Automatic detection and resolution of context conflicts
- **Continuous Quality Monitoring**: Ongoing context quality validation and improvement

## 🎯 Expected Outcomes

- **Systematic Context Architecture**: Progressive context inheritance across all testing operations
- **Intelligent Context Management**: Automatic conflict detection and resolution
- **High-Quality Context Operations**: Continuous context quality validation and improvement
- **Scalable Context Framework**: Context architecture that scales with testing framework growth
- **Reliable Context Foundation**: Solid foundation for all testing framework context operations