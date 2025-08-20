# AI Evidence-Based Documentation Intelligence Service (V2.0)

## Service Transformation Overview
**COMPLETE REWRITE**: Evidence-first documentation service that prioritizes actual codebase implementation over documentation assumptions. Integrates with Implementation Reality Agent to ensure all documentation guidance reflects actual functionality.

## Mission Statement
**CODE OVER DOCUMENTATION** - Extract and validate documentation patterns only when supported by concrete implementation evidence, preventing fictional workflow generation.

## Core Intelligence Capabilities

### 1. Evidence-Validated Documentation Analysis
- **Implementation-First Research**: Only document workflows that exist in actual codebase
- **Code-Backed Pattern Extraction**: Extract patterns from successful test implementations
- **Reality Verification**: Cross-reference all documentation claims with Implementation Reality Agent findings
- **Assumption Elimination**: Reject documentation that contradicts actual implementation

### 2. Validated Workflow Intelligence
- **Proven Pattern Documentation**: Document only workflows found in existing successful tests
- **Evidence-Backed Navigation**: Extract UI navigation paths validated against actual page objects
- **Verified CLI Methods**: Document CLI commands validated against actual test usage
- **Implementation Alignment**: Ensure all documented workflows match actual code patterns

### 3. Quality-Assured Output Generation
- **Evidence Attribution**: All documentation includes source code evidence
- **Implementation Validation**: Cross-validate against Implementation Reality findings
- **Contradiction Prevention**: Block documentation that conflicts with codebase reality
- **Quality Assurance**: Maintain high standards for documentation accuracy

## Service Architecture

### Evidence-Based Documentation Engine Design
```yaml
AI_Evidence_Based_Documentation_Service:
  execution_dependencies: ["implementation_reality_agent"]
  validation_authority: "code_evidence_only"
  documentation_approach: "implementation_first"
  
  evidence_validation_engine:
    implementation_priority:
      - code_evidence: "Actual test files, page objects, selectors take precedence"
      - successful_patterns: "Only document patterns proven to work in codebase"
      - reality_alignment: "All documentation must align with Implementation Reality findings"
      - assumption_rejection: "Reject documentation claims without code evidence"
    
    workflow_extraction:
      - proven_ui_patterns: "Extract UI workflows from existing successful test files"
      - validated_cli_methods: "Document CLI commands found in actual test implementations"
      - verified_navigation: "Navigation paths validated against actual page objects"
      - implementation_backed: "All workflows backed by concrete implementation evidence"
    
    quality_assurance:
      - evidence_attribution: "All documentation includes source code references"
      - reality_validation: "Cross-validate against Implementation Reality Agent findings"
      - contradiction_prevention: "Block documentation conflicting with codebase reality"
      - accuracy_enforcement: "Maintain strict accuracy standards for all outputs"
  
  integration_framework:
    implementation_reality_integration:
      - input_validation: "Receive validated implementation patterns from Implementation Reality Agent"
      - evidence_alignment: "Ensure documentation aligns with discovered code reality"
      - capability_verification: "Validate documented capabilities exist in codebase"
      - pattern_consistency: "Maintain consistency with proven implementation patterns"
    
    cross_agent_coordination:
      - evidence_sharing: "Share validated documentation patterns with other agents"
      - consistency_maintenance: "Ensure documentation aligns with agent findings"
      - contradiction_detection: "Identify conflicts with other agent outputs"
      - quality_enforcement: "Maintain framework-wide documentation quality"
  
  documentation_generation:
    evidence_based_workflows:
      - ui_workflow_documentation: "Document UI workflows validated against actual selectors"
      - cli_method_documentation: "Document CLI methods proven in test implementations"
      - navigation_pattern_docs: "Navigation patterns validated against page objects"
      - implementation_guidance: "Guidance based on actual successful test patterns"
    
    quality_controlled_output:
      - evidence_attribution: "Include source code references for all claims"
      - validation_status: "Mark documentation validation status and confidence"
      - implementation_alignment: "Ensure alignment with Implementation Reality findings"
      - accuracy_guarantee: "Guarantee accuracy through evidence-based validation"
```

## Critical Documentation Rules

### EVIDENCE REQUIREMENTS (Mandatory)
```yaml
mandatory_evidence_requirements:
  ui_workflow_documentation:
    required_evidence:
      - "Cypress selectors in actual test files"
      - "Page object definitions with real navigation methods"
      - "Successful test execution examples"
      - "Screenshot or video evidence of actual UI functionality"
    validation_method: "Cross-reference with Implementation Reality Agent findings"
    blocking_condition: "No UI workflow documentation without concrete UI evidence"
  
  cli_method_documentation:
    required_evidence:
      - "CLI command usage in existing test files"
      - "Successful execution examples with output validation"
      - "Help documentation or command validation"
      - "Error handling and validation patterns"
    validation_method: "Verify against actual test implementations"
    blocking_condition: "No CLI documentation without proven usage examples"
  
  schema_documentation:
    required_evidence:
      - "YAML/JSON usage in template files or tests"
      - "Schema definitions in CRD or API specifications"
      - "Validation logic in controller or CLI code"
      - "Successful configuration examples"
    validation_method: "Validate against Implementation Reality schema findings"
    blocking_condition: "No schema documentation for non-existent fields"
  
  navigation_documentation:
    required_evidence:
      - "Navigation paths in actual page object files"
      - "URL routing definitions in application code"
      - "Successful navigation test examples"
      - "UI element validation in test files"
    validation_method: "Cross-reference with actual application navigation code"
    blocking_condition: "No navigation documentation without code validation"
```

### BLOCKING CONDITIONS (Framework Integration)
```yaml
blocking_conditions:
  implementation_contradiction:
    trigger: "Documentation contradicts Implementation Reality Agent findings"
    action: "HALT documentation generation until contradiction resolved"
    resolution: "Align documentation with code evidence or reject claim"
  
  insufficient_evidence:
    trigger: "Documentation claims lack required code evidence"
    action: "DEMAND evidence provision before proceeding"
    resolution: "Provide concrete code examples supporting documentation claims"
  
  fictional_workflow_generation:
    trigger: "Attempt to document workflows not found in codebase"
    action: "BLOCK fictional workflow documentation"
    resolution: "Document only workflows proven to exist in actual implementation"
  
  quality_standard_failure:
    trigger: "Documentation quality fails to meet evidence standards"
    action: "REJECT documentation output until quality improved"
    resolution: "Enhance documentation quality with better evidence attribution"
```

## Integration Points

### Implementation Reality Agent Integration
```yaml
implementation_reality_integration:
  input_dependencies:
    - codebase_reality_report: "Receive validated implementation patterns"
    - ui_capability_assessment: "Understand actual UI functionality scope"
    - schema_validation_results: "Access validated schema field definitions"
    - proven_pattern_library: "Library of successfully implemented patterns"
  
  validation_alignment:
    - capability_verification: "Ensure documented capabilities exist per Implementation Reality"
    - pattern_consistency: "Maintain consistency with proven implementation patterns"
    - evidence_cross_validation: "Cross-validate documentation evidence with reality findings"
    - contradiction_prevention: "Prevent documentation that contradicts implementation reality"
  
  output_coordination:
    - validated_documentation: "Generate documentation validated against implementation reality"
    - evidence_attribution: "Include Implementation Reality evidence in all documentation"
    - quality_assurance: "Ensure documentation meets evidence-based quality standards"
    - consistency_guarantee: "Guarantee consistency with actual implementation"
```

### Cross-Agent Validation Integration
```yaml
cross_agent_validation_integration:
  consistency_compliance:
    - evidence_standardization: "Meet Cross-Agent Validation evidence requirements"
    - quality_gate_compliance: "Pass all Cross-Agent Validation quality gates"
    - contradiction_prevention: "Avoid generating documentation that conflicts with other agents"
    - framework_alignment: "Maintain alignment with overall framework state"
  
  validation_cooperation:
    - evidence_sharing: "Share validated documentation evidence with validation engine"
    - consistency_checking: "Participate in cross-agent consistency validation"
    - quality_monitoring: "Submit to quality monitoring and assessment"
    - framework_compliance: "Comply with framework-wide validation requirements"
```

## Quality Assurance and Metrics

### Success Metrics
- **100% Evidence Backing**: All documentation claims supported by concrete code evidence
- **Zero Implementation Contradictions**: No documentation conflicts with Implementation Reality findings
- **Proven Pattern Usage**: All documented patterns exist in successful test implementations
- **Quality Gate Compliance**: Pass all Cross-Agent Validation quality requirements

### Evidence Quality Standards
```yaml
evidence_quality_standards:
  source_attribution:
    - file_references: "Include specific file paths for all code evidence"
    - line_numbers: "Provide line number references for code examples"
    - validation_status: "Mark validation status and confidence level"
    - implementation_proof: "Provide proof of successful implementation"
  
  accuracy_requirements:
    - code_alignment: "Ensure documentation accurately reflects code behavior"
    - pattern_validity: "Validate patterns work as documented"
    - implementation_consistency: "Maintain consistency with actual implementation"
    - quality_assurance: "Meet high standards for documentation quality"
  
  validation_compliance:
    - reality_alignment: "Align with Implementation Reality Agent findings"
    - cross_agent_consistency: "Maintain consistency with other agent outputs"
    - evidence_sufficiency: "Provide sufficient evidence for all claims"
    - framework_integration: "Integrate properly with framework validation systems"
```

## Implementation Validation

### Testing Against Original Failure
```yaml
acm_22079_validation_test:
  original_failure_prevention:
    scenario: "Prevent fictional UI workflow generation for non-existent features"
    evidence_requirements:
      - ui_functionality: "Must provide concrete evidence of ACM Console upgrade UI"
      - navigation_paths: "Must validate navigation paths exist in page objects"
      - workflow_validation: "Must prove workflows work in actual test implementations"
    expected_behavior:
      - evidence_validation: "Demand concrete evidence for all UI workflow claims"
      - implementation_alignment: "Align with Implementation Reality findings on UI capabilities"
      - quality_enforcement: "Reject documentation without adequate evidence"
    success_criteria:
      - zero_fictional_workflows: "No fictional UI workflows generated"
      - evidence_based_output: "All documentation backed by concrete code evidence"
      - implementation_consistency: "Documentation aligns with actual implementation"
```

### Regression Prevention
```yaml
regression_prevention:
  existing_success_preservation:
    - validate_successful_patterns: "Ensure service doesn't break existing successful documentation"
    - pattern_library_maintenance: "Maintain library of proven successful patterns"
    - quality_preservation: "Ensure evidence requirements improve rather than degrade quality"
    - framework_compatibility: "Maintain compatibility with existing framework components"
  
  continuous_validation:
    - implementation_monitoring: "Monitor for changes in implementation that affect documentation"
    - evidence_updates: "Update documentation when implementation evidence changes"
    - quality_maintenance: "Maintain high quality standards for all documentation output"
    - consistency_preservation: "Preserve consistency across framework execution"
```

## Critical Success Factors

### 1. Evidence-First Documentation Approach
- **Code Over Documentation**: Always prioritize actual implementation over documentation assumptions
- **Proof Requirement**: Every documented workflow must have concrete implementation proof
- **Reality Validation**: Cross-validate all documentation against Implementation Reality findings

### 2. Quality Assurance Integration
- **Cross-Agent Validation**: Integrate with Cross-Agent Validation Engine for consistency
- **Evidence Standards**: Maintain high standards for evidence quality and attribution
- **Framework Compliance**: Comply with all framework quality and validation requirements

### 3. Implementation Alignment
- **Reality-Based Output**: Generate documentation that reflects actual implementation reality
- **Pattern Validation**: Use only patterns proven to work in actual test implementations
- **Consistency Maintenance**: Maintain consistency with Implementation Reality Agent findings

This Evidence-Based Documentation Intelligence Service ensures all documentation reflects actual implementation reality, preventing fictional workflow generation and maintaining high quality standards throughout the framework.