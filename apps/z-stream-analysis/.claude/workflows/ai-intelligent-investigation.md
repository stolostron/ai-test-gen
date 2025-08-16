# AI-Powered Intelligent Investigation Framework

This workflow provides systematic AI-powered investigation of pipeline failures to deliver definitive verdicts on whether failures are product bugs, automation bugs, or automation gaps.

## Overview

**Purpose:** Enhance the Z-Stream Analysis Engine with intelligent product vs automation bug classification that provides:
- **Definitive Verdicts:** Clear categorization with supporting evidence
- **Code Analysis:** Deep investigation of automation repository code
- **Environment Analysis:** Systematic environment and product state assessment  
- **Robust Fixes:** Specific automation fixes with implementation guidance
- **Product Bug Detection:** Systematic identification of actual product issues

## Investigation Framework

### 1. AI Systematic Investigation Workflow
**Purpose:** Conduct comprehensive investigation to determine failure root cause category  
**Output:** Definitive verdict with supporting evidence

```markdown
## AI Task: Systematic Pipeline Failure Investigation

Conduct comprehensive investigation to determine the definitive cause category:

**Jenkins Data:**
- Build Metadata: [jenkins_metadata]
- Console Logs: [console_output]
- Test Results: [test_results]
- Environment: [environment_details]

**Investigation Framework:**

### PHASE 1: INITIAL EVIDENCE GATHERING
1. **Extract Key Failure Indicators:**
   - Primary error messages and stack traces
   - Test failure details and assertions
   - Environment configuration and state
   - Product version and component information

2. **Identify Failure Patterns:**
   - Error message analysis for known patterns
   - Stack trace analysis for code vs product issues
   - Environment dependency failures
   - Configuration or setup issues

### PHASE 2: SYSTEMATIC CATEGORIZATION ANALYSIS

#### A. PRODUCT BUG INVESTIGATION
**Criteria for Product Bug Classification:**
- Application functionality not working as designed
- API responses indicating product errors
- UI behavior inconsistent with expected product operation  
- Backend service failures or errors
- Database or data inconsistencies
- Product configuration or deployment issues

**Evidence to Collect:**
- Error messages indicating product malfunction
- API response codes suggesting backend issues
- UI screenshots showing incorrect product behavior
- Service logs indicating product component failures
- Product-specific error patterns

#### B. AUTOMATION BUG INVESTIGATION  
**Criteria for Automation Bug Classification:**
- Test code logic errors or incorrect assertions
- Test framework configuration issues
- Incorrect test data or test setup
- Test execution environment problems
- Automation tool or library bugs

**Evidence to Collect:**
- Test code analysis revealing logic errors
- Incorrect selectors or element interactions
- Test configuration problems
- Test data issues or hardcoded values
- Test framework or tool compatibility issues

#### C. AUTOMATION GAP INVESTIGATION
**Criteria for Automation Gap Classification:**
- Product features changed but tests not updated
- New product functionality not covered by tests
- Environmental changes not reflected in tests
- Test coverage missing for edge cases
- Product workflow changes not automated

**Evidence to Collect:**
- Recent product changes not reflected in tests
- New features lacking test coverage
- Environment updates not handled by automation
- Product workflow modifications without test updates

### PHASE 3: DEFINITIVE VERDICT DETERMINATION

Based on systematic analysis, provide:

**Required Output Format:**
```json
{
  "investigation_verdict": {
    "primary_classification": "product_bug|automation_bug|automation_gap",
    "confidence_level": "high|medium|low",
    "verdict_rationale": "detailed_explanation_of_classification_decision",
    "supporting_evidence": [
      {
        "evidence_type": "error_message|stack_trace|ui_behavior|api_response|configuration",
        "source": "console_log|test_result|screenshot|api_response",
        "content": "specific_evidence_content",
        "significance": "critical|high|medium|low"
      }
    ]
  },
  "detailed_analysis": {
    "product_indicators": [
      "evidence_pointing_to_product_issues"
    ],
    "automation_indicators": [
      "evidence_pointing_to_automation_issues"  
    ],
    "gap_indicators": [
      "evidence_pointing_to_automation_gaps"
    ],
    "environment_factors": [
      "environmental_considerations"
    ]
  },
  "investigation_confidence": {
    "data_completeness": "complete|partial|limited",
    "evidence_quality": "strong|moderate|weak",
    "verdict_certainty": "definitive|probable|uncertain"
  }
}
```
```

### 2. AI Code Repository Analysis
**Purpose:** Analyze automation repository code to understand test implementation  
**Output:** Code analysis with specific areas for investigation and improvement

```markdown
## AI Task: Automation Repository Code Analysis

Analyze the automation repository code to understand test implementation and identify issues:

**Repository Context:**
- Repository: stolostron/clc-ui-e2e
- Branch: release-2.12
- Failed Test: [specific_test_file_and_function]
- Test Framework: Cypress

**Code Analysis Requirements:**

### PHASE 1: TEST CODE EXAMINATION
1. **Locate and Analyze Failed Test:**
   - Find the specific test file and function that failed
   - Analyze test logic, assertions, and expectations
   - Review test data, selectors, and interactions
   - Examine test setup and teardown procedures

2. **Test Implementation Quality Assessment:**
   - Evaluate test assertion accuracy and appropriateness
   - Check for hardcoded values or brittle selectors
   - Assess error handling and retry logic
   - Review test data management and cleanup

### PHASE 2: FRAMEWORK AND CONFIGURATION ANALYSIS
1. **Test Framework Configuration:**
   - Review Cypress configuration and setup
   - Analyze test environment configuration
   - Check for framework version compatibility issues
   - Examine custom commands and utilities

2. **Test Support Infrastructure:**
   - Review helper functions and page objects
   - Analyze test data management approaches
   - Check environment-specific configurations
   - Examine CI/CD integration points

### PHASE 3: REPOSITORY CONTEXT ANALYSIS
1. **Recent Changes Analysis:**
   - Review recent commits affecting failed test areas
   - Analyze product changes that might impact tests
   - Check for dependency updates or configuration changes
   - Examine environment or infrastructure modifications

2. **Test Coverage and Maintenance:**
   - Assess test coverage for affected functionality
   - Review test maintenance patterns and practices
   - Check for technical debt or known issues
   - Analyze test stability and flakiness patterns

**Required Output Format:**
```json
{
  "code_analysis": {
    "failed_test_details": {
      "file_path": "path_to_test_file",
      "test_function": "specific_test_name",
      "test_logic_assessment": "detailed_analysis_of_test_implementation",
      "assertion_analysis": "evaluation_of_test_assertions",
      "code_quality_issues": ["list_of_identified_issues"]
    },
    "framework_assessment": {
      "configuration_issues": ["cypress_config_problems"],
      "framework_compatibility": "assessment_of_framework_issues",
      "test_infrastructure": "evaluation_of_support_code"
    },
    "repository_context": {
      "recent_changes_impact": "analysis_of_recent_commits",
      "test_maintenance_issues": ["maintenance_and_debt_issues"],
      "coverage_gaps": ["areas_lacking_coverage"]
    },
    "automation_verdict": {
      "primary_issue_category": "test_logic|test_data|test_configuration|framework_issue|coverage_gap",
      "issue_description": "specific_problem_identified",
      "fix_complexity": "simple|moderate|complex",
      "fix_confidence": "high|medium|low"
    }
  }
}
```
```

### 3. AI Product State Analysis
**Purpose:** Analyze product behavior and state to identify potential product issues  
**Output:** Product analysis with definitive assessment of product functionality

```markdown
## AI Task: Product State and Behavior Analysis

Analyze product behavior and state to determine if issues are product-related:

**Product Context:**
- Product: Advanced Cluster Management (ACM) 2.12
- Component: Cluster Lifecycle (CLC) - AKS cluster import
- Environment: [environment_details]
- Expected Behavior: [expected_product_functionality]

**Product Analysis Requirements:**

### PHASE 1: PRODUCT FUNCTIONALITY ASSESSMENT
1. **Core Functionality Analysis:**
   - Analyze expected product behavior for the failed scenario
   - Review product documentation and specifications
   - Compare actual behavior with documented functionality
   - Assess API responses and data consistency

2. **Product State Validation:**
   - Examine product logs and error messages
   - Analyze backend service responses
   - Check database state and data integrity
   - Review product configuration and setup

### PHASE 2: PRODUCT CHANGE IMPACT ANALYSIS
1. **Recent Product Changes:**
   - Review product release notes and change logs
   - Analyze recent product updates affecting tested functionality
   - Check for known product issues or regressions
   - Examine product configuration or behavior changes

2. **Environment-Product Interaction:**
   - Assess product behavior in test environment
   - Check for environment-specific product issues
   - Analyze product dependencies and integrations
   - Review product version compatibility

### PHASE 3: PRODUCT VS AUTOMATION DISTINCTION
1. **Product Issue Indicators:**
   - Product error messages or service failures
   - Incorrect product responses or behavior
   - Backend service or API problems
   - Product configuration or deployment issues

2. **Automation Issue Indicators:**
   - Product functioning correctly but test expectations wrong
   - Product behavior changed but tests not updated
   - Test implementation issues or incorrect assertions
   - Test environment or configuration problems

**Required Output Format:**
```json
{
  "product_analysis": {
    "functionality_assessment": {
      "expected_behavior": "documented_product_functionality",
      "actual_behavior": "observed_product_behavior", 
      "behavior_consistency": "consistent|inconsistent|unclear",
      "product_error_indicators": ["specific_product_errors"]
    },
    "product_change_impact": {
      "recent_changes": ["relevant_product_changes"],
      "change_impact_on_tests": "analysis_of_change_impact",
      "known_issues": ["documented_product_issues"],
      "regression_indicators": ["signs_of_product_regression"]
    },
    "product_verdict": {
      "product_functioning_correctly": "yes|no|unclear",
      "product_issue_probability": "high|medium|low|none",
      "product_issue_description": "specific_product_problem_if_any",
      "product_vs_automation_conclusion": "detailed_analysis"
    }
  }
}
```
```

## Investigation Integration Workflow

### Complete Investigation Process
```markdown
# Comprehensive AI Investigation Workflow
1. ai_systematic_investigation()        # Systematic failure categorization
2. ai_code_repository_analysis()       # Deep automation code analysis  
3. ai_product_state_analysis()         # Product functionality assessment
4. ai_cross_reference_findings()       # Correlate all investigation results
5. ai_generate_definitive_verdict()    # Final classification with evidence
6. ai_create_robust_fix_plan()         # Specific fixes for automation issues
```

### Evidence Cross-Referencing
```markdown
## AI Task: Cross-Reference Investigation Findings

Correlate findings from all investigation phases to reach definitive verdict:

**Investigation Results:**
- Systematic Investigation: [systematic_investigation_results]
- Code Analysis: [code_analysis_results] 
- Product Analysis: [product_analysis_results]

**Cross-Reference Requirements:**
1. **Evidence Consistency:** Ensure all evidence points to same conclusion
2. **Conflict Resolution:** Address any conflicting evidence or indicators
3. **Confidence Assessment:** Evaluate overall confidence in verdict
4. **Supporting Data:** Compile strongest evidence for final verdict

**Output:** Definitive classification with comprehensive supporting evidence
```

## Enhanced Report Structure

### New Report Format with Upfront Verdict
```markdown
# Pipeline Failure Analysis Report

## 🎯 DEFINITIVE VERDICT
**Classification:** [PRODUCT BUG | AUTOMATION BUG | AUTOMATION GAP]  
**Confidence Level:** [HIGH | MEDIUM | LOW]  
**Verdict Summary:** [One-sentence definitive statement]

## 📊 SUPPORTING EVIDENCE
### Primary Evidence
[Most compelling evidence supporting the verdict]

### Supporting Analysis  
[Additional evidence and analysis details]

### Investigation Confidence
- Data Completeness: [assessment]
- Evidence Quality: [assessment]  
- Verdict Certainty: [assessment]

## [Rest of analysis continues with traditional structure]
```

---

**Implementation Status:** Framework ready for deployment  
**Enhancement Focus:** Intelligent investigation with definitive verdicts  
**Benefits:** Clear product vs automation distinction with robust evidence