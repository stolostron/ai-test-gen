# Test Scenario Template

## Test Identification
**Test ID**: TST-{CATEGORY}-{NUMBER}
**Test Name**: {Descriptive test name}
**Category**: {Policy Compliance | AI Service Integration | Quality Validation | Regression}
**Priority**: {Critical | High | Medium | Low}
**Framework Version**: {Target framework version}

## Test Objective
**Purpose**: {Clear description of what this test validates}
**Policy Reference**: {Link to CLAUDE.md policy or requirement}
**Risk Mitigation**: {What risks this test addresses}

## Test Setup
**Prerequisites**:
- {List all required conditions}
- {Framework state requirements}
- {Data requirements}

**Test Data**:
```yaml
test_input:
  jira_ticket: "{JIRA-ID}"
  environment: "{test-environment}"
  parameters: {additional parameters}
```

## Test Execution Steps
1. **Step Name**: {Action description}
   - Command: `{exact command}`
   - Expected Behavior: {what should happen}
   - Evidence Collection: {what data to collect}

2. **Step Name**: {Action description}
   - Command: `{exact command}`
   - Expected Behavior: {what should happen}
   - Evidence Collection: {what data to collect}

## Validation Criteria
### Success Criteria
- [ ] {Specific measurable success criterion}
- [ ] {Quality metric threshold}
- [ ] {Performance requirement}

### Evidence Requirements
- **Execution Evidence**: {Required execution data}
- **Output Evidence**: {Required output artifacts}
- **Quality Evidence**: {Required quality metrics}
- **Behavioral Evidence**: {Required behavioral validation}

## Expected Results
### Positive Validation
- {Expected successful outcome}
- {Quality score range}
- {Performance metrics}

### Negative Validation
- {Known failure modes to test}
- {Error handling verification}
- {Recovery mechanism validation}

## Evidence Collection
```yaml
evidence_manifest:
  execution_data:
    - start_time
    - end_time
    - exit_code
    - resource_usage
  
  output_data:
    - generated_files: ["Test-Cases-Report.md", "Complete-Analysis-Report.md"]
    - quality_scores
    - format_compliance
  
  behavioral_data:
    - service_interactions
    - cascade_prevention
    - error_handling
```

## Risk Assessment
**Failure Impact**: {Impact if this test fails}
**Regression Risk**: {Likelihood of regression in this area}
**Mitigation Strategy**: {How to handle test failures}

## Learning Integration
**Pattern Recognition**: {Patterns to track from this test}
**Success Indicators**: {What indicates good framework behavior}
**Failure Indicators**: {What indicates problems}
**Improvement Opportunities**: {How this test can be enhanced}

## Notes
- {Any special considerations}
- {Known limitations}
- {Future enhancements}
