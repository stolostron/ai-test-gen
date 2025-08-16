# Real Repository Analysis Workflow

This workflow provides comprehensive analysis of actual automation repositories to identify real issues and generate precise fixes.

## Overview

**Purpose:** Analyze actual automation repositories to:
- **Clone Real Repositories:** Access actual codebases instead of making assumptions
- **Examine Real File Structure:** Understand actual organization and patterns
- **Identify Real Issues:** Find actual failing code and root causes
- **Generate Precise Fixes:** Create exact code changes based on real analysis
- **Verify Implementation:** Test fixes against actual repository structure

## Repository Analysis Framework

### 1. Repository Cloning and Setup
**Purpose:** Clone and prepare the actual automation repository for analysis
**Input:** Repository URL from Jenkins metadata
**Output:** Local repository copy ready for analysis

```markdown
## AI Task: Clone and Analyze Real Repository

Clone and analyze the actual automation repository:

**Repository Context:**
- Repository URL: [extracted_from_jenkins_metadata]
- Branch: [extracted_from_jenkins_parameters] 
- Commit: [extracted_from_jenkins_build_info]

**Cloning Strategy:**
1. **Create Analysis Directory:**
   ```bash
   mkdir -p temp-repos
   cd temp-repos
   ```

2. **Clone Repository:**
   ```bash
   git clone [repository_url]
   cd [repository_name]
   git checkout [specific_branch_or_commit]
   ```

3. **Verify Repository Structure:**
   ```bash
   find . -name "*.js" -o -name "*.json" -o -name "*.md" | head -20
   ls -la
   ```

4. **Automatic Post-Analysis Cleanup:**
   ```bash
   # After analysis completion, automatically remove temp repositories
   cd ../../
   rm -rf temp-repos/[repository_name]
   # Remove empty temp-repos directory if no other repos
   rmdir temp-repos 2>/dev/null || true
   ```

**Repository Analysis Requirements:**
- Confirm actual file structure matches Jenkins references
- Identify actual test framework and version
- Locate actual failing test files
- Examine actual support and configuration files
```

### 2. Real File Structure Analysis  
**Purpose:** Understand actual repository organization and patterns
**Input:** Cloned repository
**Output:** Comprehensive repository structure understanding

```markdown
## AI Task: Analyze Real File Structure

Analyze the actual repository structure:

**File Structure Analysis:**
1. **Framework Identification:**
   - Examine package.json for actual dependencies
   - Check configuration files (cypress.config.js, etc.)
   - Identify actual test framework version

2. **Test File Analysis:**
   - Locate actual failing test files mentioned in Jenkins logs
   - Examine actual test structure and patterns
   - Identify actual support files and utilities

3. **Support Code Analysis:**
   - Examine cypress/support/ directory structure
   - Analyze actual commands.js and other support files
   - Identify actual helper functions and utilities

**Required Analysis:**
```bash
# Framework analysis
cat package.json | grep -A5 -B5 "cypress\|dependencies"
ls -la cypress*/

# Failing test file analysis  
cat cypress/tests/credentials/addCredentials.spec.js
cat cypress/tests/clusters/managedClusters/create/createClusters.spec.js

# Support file analysis
ls -la cypress/support/
cat cypress/support/commands.js | head -50
cat cypress/support/e2e.js
```

**Output Format:**
```json
{
  "repository_analysis": {
    "framework": {
      "type": "cypress",
      "version": "actual_version_found",
      "configuration": "actual_config_details"
    },
    "file_structure": {
      "test_files": ["actual_failing_test_paths"],
      "support_files": ["actual_support_file_paths"],
      "configuration_files": ["actual_config_file_paths"]
    },
    "failing_tests": {
      "test_1": {
        "file_path": "exact_path_in_repository",
        "before_hooks": ["actual_before_hook_functions"],
        "test_methods": ["actual_test_method_calls"]
      }
    }
  }
}
```
```

### 3. Real Code Issue Identification
**Purpose:** Identify actual issues in real code  
**Input:** Repository analysis results
**Output:** Precise issue identification with exact line numbers

```markdown
## AI Task: Identify Real Code Issues

Analyze actual failing code to identify real issues:

**Issue Identification Requirements:**

1. **Examine Actual Before Hooks:**
   - Analyze actual before() functions in failing tests
   - Identify actual function calls being made
   - Trace actual function definitions in support files

2. **Analyze Real Function Implementations:**
   - Examine actual cy.loginViaAPI() implementation
   - Check actual authentication and session handling
   - Identify actual timeout configurations and retry logic

3. **Real Error Pattern Analysis:**
   - Match Jenkins error messages to actual code lines
   - Identify actual functions causing timeouts
   - Examine actual error handling patterns

**Analysis Commands:**
```bash
# Find actual function definitions
grep -rn "loginViaAPI" cypress/
grep -rn "before.*function" cypress/tests/

# Examine actual timeout configurations
grep -rn "timeout" cypress/
cat cypress.config.js | grep -A10 -B10 "timeout"

# Analyze actual authentication flow
cat cypress/support/commands.js | grep -A50 "loginViaAPI"
```

**Required Output:**
```json
{
  "real_issue_analysis": {
    "failing_function": {
      "name": "actual_function_name",
      "file_path": "exact_file_path",
      "line_numbers": "exact_line_range",
      "implementation": "actual_code_implementation"
    },
    "root_cause": {
      "issue_type": "timeout|authentication|configuration|network",
      "specific_problem": "detailed_problem_description",
      "error_location": "exact_file_and_line"
    },
    "dependencies": {
      "called_functions": ["actual_dependent_functions"],
      "configuration_dependencies": ["actual_config_dependencies"]
    }
  }
}
```
```

### 4. Precise Fix Generation
**Purpose:** Generate exact fixes based on real code analysis
**Input:** Real issue analysis  
**Output:** Precise code changes with exact file paths and line numbers

```markdown
## AI Task: Generate Precise Automation Fixes

Generate exact fixes based on real repository analysis:

**Fix Generation Requirements:**

1. **Exact File Modifications:**
   - Provide actual file paths from repository
   - Specify exact line numbers to modify
   - Show actual current code vs. proposed fixes

2. **Repository-Consistent Patterns:**
   - Follow actual coding patterns found in repository
   - Use actual utility functions available in repository
   - Match actual error handling patterns used

3. **Real Configuration Updates:**
   - Update actual configuration files if needed
   - Use actual timeout values appropriate for framework
   - Follow actual configuration patterns in repository

**Implementation Strategy:**
```bash
# Analyze actual patterns for timeouts
grep -rn "timeout.*[0-9]" cypress/
grep -rn "defaultCommandTimeout" cypress/

# Examine actual error handling patterns
grep -rn "catch\|try\|error" cypress/support/
grep -A10 -B10 "failOnNonZeroExit" cypress/support/commands.js

# Check actual retry patterns
grep -rn "retry\|repeat" cypress/
```

**Required Output:**
```json
{
  "precise_fixes": [
    {
      "file_path": "exact/repository/path/file.js",
      "line_numbers": "specific_lines_to_modify",
      "current_code": "actual_existing_code_from_repository",
      "fixed_code": "precise_replacement_code",
      "rationale": "why_this_specific_fix_solves_real_issue"
    }
  ],
  "configuration_changes": [
    {
      "file_path": "exact/config/file/path",
      "current_config": "actual_current_configuration",
      "updated_config": "precise_new_configuration",
      "change_reason": "specific_reason_for_change"
    }
  ],
  "verification_commands": [
    "exact_commands_to_test_fix_in_repository"
  ]
}
```
```

### 5. Repository Integration Validation
**Purpose:** Validate fixes work with actual repository structure
**Input:** Generated fixes
**Output:** Implementation and testing guidance

```markdown
## AI Task: Validate Repository Integration

Validate fixes work with actual repository:

**Validation Requirements:**

1. **File Path Verification:**
   ```bash
   # Verify all file paths exist in repository
   ls -la [each_file_path_from_fixes]
   
   # Check line numbers are valid
   wc -l [each_file_path_from_fixes]
   ```

2. **Pattern Consistency Check:**
   ```bash
   # Verify coding patterns match repository style
   grep -A5 -B5 "similar_pattern" cypress/
   
   # Check function naming conventions
   grep -rn "function.*(" cypress/ | head -10
   ```

3. **Framework Compatibility:**
   ```bash
   # Verify proposed changes work with actual framework version
   cat package.json | grep cypress
   
   # Check if proposed commands/methods exist
   grep -rn "proposed_method_name" node_modules/cypress/
   ```

**Implementation Steps:**
1. Apply fixes to local repository copy
2. Run actual tests to verify fixes work
3. Check for any syntax or compatibility issues
4. Validate no regression in other tests

**Success Criteria:**
- All file paths exist and are accessible
- Proposed changes follow repository patterns
- Fixes are compatible with actual framework version
- Implementation guidance is actionable
```

## Integration with Analysis Framework

### Enhanced Workflow with Real Repository Analysis
```markdown
# Complete AI Analysis Workflow with Real Repository Analysis
1. ai_systematic_investigation()           # Determine verdict: product vs automation
2. ai_clone_real_repository()              # Clone actual automation repository  
3. ai_analyze_real_file_structure()        # Understand actual repository organization
4. ai_identify_real_code_issues()          # Find actual issues in real code
5. ai_generate_precise_fixes()             # Create exact fixes based on real analysis
6. ai_validate_repository_integration()    # Ensure fixes work with actual repository
7. ai_product_state_analysis()             # Product functionality assessment  
8. ai_cross_reference_findings()           # Correlate investigation results
9. ai_generate_definitive_verdict()        # Final classification with evidence
10. ai_generate_enhanced_reports()         # Reports with precise fixes and real analysis
11. ai_execute_post_analysis_cleanup()     # AUTOMATIC CLEANUP of temporary repositories
```

## Repository Analysis Storage

### Analysis Results Structure
```
temp-repos/
├── [repository-name]/                     # Cloned actual repository
│   ├── [actual-repository-structure]     # Real files and directories
│   └── .git/                             # Git history and branch info
├── analysis-results/
│   ├── file-structure-analysis.json      # Real repository structure analysis
│   ├── issue-identification.json         # Real code issue analysis
│   ├── precise-fixes.json               # Exact fixes with real file paths
│   └── validation-results.json          # Repository integration validation
└── verification-scripts/
    ├── test-fixes.sh                     # Scripts to test fixes
    └── validate-patterns.sh             # Scripts to validate repository patterns
```

---

**Implementation Status:** Ready for immediate deployment  
**Focus:** Real repository analysis instead of assumptions  
**Benefits:** Precise, implementable fixes based on actual code analysis