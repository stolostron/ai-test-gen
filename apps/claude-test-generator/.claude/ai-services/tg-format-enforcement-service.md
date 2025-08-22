# Test Generator Format Enforcement Service

## 🚨 **CRITICAL: MANDATORY FORMAT ENFORCEMENT**

**Purpose**: Real-time format validation service that enforces user-specified requirements for test case format, complete report structure, and content standards with BLOCKING authority.

**Service Status**: V1.0 - Production Ready with Zero-Tolerance Enforcement
**Integration Level**: Core Quality Service - MANDATORY for all output generation
**Authority**: BLOCKING - Can halt framework execution for format violations

## 🔒 **ZERO-TOLERANCE ENFORCEMENT RULES**

### **1. HTML TAG PREVENTION (ABSOLUTE)**

**REQUIREMENT**: Test cases and reports must contain ZERO HTML tags - markdown-only formatting

**BLOCKING PATTERNS:**
```regex
HTML_Tags_BLOCKED:
  - '<br>'                     # Line break tags
  - '<br/>'                    # Self-closing line breaks
  - '<br\s*>'                  # Line breaks with spaces
  - '<[^>]+>'                  # Any HTML tags
  - '&lt;'                     # HTML entities
  - '&gt;'                     # HTML entities
  - '&amp;'                    # HTML entities
```

**ENFORCEMENT ACTION:**
- **Real-time scanning** during content generation
- **IMMEDIATE REPLACEMENT** of HTML tags with markdown equivalents
- **AUTOMATIC CONVERSION** of `<br>` to proper line breaks
- **FRAMEWORK HALT** if HTML cannot be cleanly converted

### **2. CITATION-FREE TEST CASES (ABSOLUTE)**

**REQUIREMENT**: Test cases file must contain ZERO citations, sources, or references

**BLOCKING PATTERNS:**
```regex
Citation_Patterns_BLOCKED:
  - '\[Source:.*?\]'           # [Source: anything]
  - '\*\[Source:.*?\]\*'       # *[Source: anything]*
  - '\(Source:.*?\)'           # (Source: anything)
  - '\[.*?:.*?:.*?\]'          # [Type:reference:metadata]
  - '\[Code:.*?\]'             # [Code: references]
  - '\[GitHub:.*?\]'           # [GitHub: references]
  - '\[JIRA:.*?\]'             # [JIRA: references]
  - '\[Docs:.*?\]'             # [Docs: references]
  - 'Source:.*'                # Any "Source:" patterns
  - '\*\[.*?\]\*'              # Any bracketed references
```

**ENFORCEMENT ACTION:**
- **Real-time scanning** during test case generation
- **IMMEDIATE BLOCKING** when citation patterns detected
- **AUTOMATIC REMOVAL** of all citation content
- **FRAMEWORK HALT** if citations cannot be cleanly removed

### **3. MANDATORY DUAL-METHOD COVERAGE**

**REQUIREMENT**: Every test step must include both UI and CLI methods

**MANDATORY FORMAT:**
```markdown
| Step | UI Method | CLI Method | Expected Results |
|------|-----------|------------|------------------|
| 1 | **UI Navigation**: [Clear console navigation] | **CLI Command**: [Complete executable command] | **Output**: [Specific realistic results] |
```

**BLOCKING CONDITIONS:**
- ❌ **BLOCK**: Steps missing UI Method column
- ❌ **BLOCK**: Steps missing CLI Method column  
- ❌ **BLOCK**: Generic CLI descriptions without actual commands
- ❌ **BLOCK**: UI methods without clear navigation paths

### **4. COMPLETE CLI COMMANDS + FULL YAML**

**REQUIREMENT**: All CLI commands must be complete and executable

**MANDATORY CLI FORMAT:**
```bash
oc apply -f - <<EOF
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: [specific-name]
  namespace: [actual-namespace]
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"
spec:
  desiredCuration: upgrade
  cluster: [target-cluster-name]
  upgrade:
    desiredUpdate: "[specific-version-or-digest]"
    channel: stable-4.16
EOF
```

**BLOCKING CONDITIONS:**
- ❌ **BLOCK**: Truncated commands like "oc apply -f - with..."
- ❌ **BLOCK**: Incomplete YAML with "..." or "etc."
- ❌ **BLOCK**: Generic placeholders without specific values
- ❌ **BLOCK**: Commands that cannot be copy-pasted and executed

## 🎯 **MANDATORY COMPLETE REPORT STRUCTURE**

### **EXACT SECTION ORDER (NO DEVIATIONS):**

```markdown
## Summary
**Feature**: [Full JIRA ticket title as clickable link to JIRA]
**Customer Impact**: [Business impact description]
**Implementation Status**: [Clickable PR link with status]
**Test Environment**: [Clickable environment link with details]
**Feature Validation**: ✅/❌ [CLEAR STATUS] - [Explanation of validation capability]

## 1. JIRA Analysis Summary
**Ticket Details**: [Clickable JIRA link with full title]
[Requirements, customer context, business value]

## 2. Environment Assessment
**Test Environment Health**: [Score/Status]
**Cluster Details**: [Clickable environment link]
[Infrastructure readiness, connectivity, real data collected]

## 3. Implementation Analysis
**Primary Implementation**: [Clickable GitHub PR link]
[Code changes, technical details, integration points]

## 4. Test Scenarios Analysis
**Testing Strategy**: [Description of test approach]
### Test Case 1: [Scenario Title]
**Scenario**: [Brief description]
**Purpose**: [What this validates and why]
**Critical Validation**: [Key validation points]
**Customer Value**: [Business relevance]
[Repeat for each test case]
**Comprehensive Coverage Rationale**: [Why these scenarios provide complete coverage]
```

**MANDATORY REQUIREMENTS:**
- ❌ **BLOCK**: Use of "Executive" in any section heading
- ❌ **BLOCK**: Non-clickable JIRA or PR references
- ❌ **BLOCK**: Missing full JIRA ticket title
- ❌ **BLOCK**: Unclear feature validation status
- ❌ **BLOCK**: Sections 4-7 from old structure (Documentation, QE Intelligence, Feature Deployment, Business Impact)
- ✅ **REQUIRED**: Clickable links for JIRA, PRs, and environment
- ✅ **REQUIRED**: Clear feature validation status in Summary
- ✅ **REQUIRED**: Test scenarios discussion based on generated test cases
- ✅ **REQUIRED**: Exactly 4 main sections after Summary

**BLOCKING CONDITIONS:**
- ❌ **BLOCK**: Missing any required section
- ❌ **BLOCK**: Including removed sections (Documentation Analysis, QE Intelligence Assessment, etc.)
- ❌ **BLOCK**: Non-clickable links in Summary
- ❌ **BLOCK**: Unclear feature validation status

## 🔧 **ENHANCED EXPECTED RESULTS REQUIREMENTS**

### **REALISTIC SAMPLE INTEGRATION:**

**MANDATORY FORMAT:**
```markdown
| Action | Expected Results |
|--------|------------------|
| [Action description] | **Status**: [Specific status indicator]
**Output**: 
```yaml
status:
  conditions:
  - type: "Ready"
    status: "True"
    reason: "Successful"
```
**Controller Logs**: `Processing digest upgrade request`, `Digest resolved successfully`
**Resource State**: ClusterCurator shows `spec.desiredCuration: upgrade` with active curator job |
```

**REQUIREMENT DETAILS:**
- **Specific Values**: Use actual cluster names, namespaces from environment
- **YAML Samples**: Include relevant YAML portions from real resources
- **Command Outputs**: Show realistic command output samples
- **Controller Logs**: Include meaningful log messages
- **Status Indicators**: Use specific status conditions and states

## 🚨 **REAL-TIME ENFORCEMENT MECHANISMS**

### **HTML Tag Prevention Engine:**
```python
def enforce_html_tag_prevention(content):
    """
    CRITICAL: Real-time HTML tag detection and BLOCKING (not just conversion)
    """
    html_patterns = [
        r'<br\s*/?>',                # All <br> variants
        r'<[^>]+>',                  # Any HTML tags
        r'&lt;',                     # HTML entities
        r'&gt;',                     # HTML entities
        r'&amp;'                     # HTML entities
    ]
    
    violations = []
    for pattern in html_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            violations.extend(matches)
    
    if violations:
        return {
            "status": "CRITICAL_BLOCK",
            "violations": violations,
            "action": "BLOCK_HTML_CONTENT",
            "message": "HTML tags detected - must use markdown-only formatting",
            "required_fix": "Convert all HTML to proper markdown formatting",
            "blocking_priority": "ABSOLUTE"
        }
    
    return {"status": "APPROVED", "content": content}

def enforce_yaml_block_html_prevention(yaml_content):
    """
    CRITICAL: Detect and BLOCK HTML tags specifically within YAML blocks
    """
    # Detect HTML tags within YAML content (the critical issue reported)
    html_in_yaml_patterns = [
        r'yaml<br>',                    # Critical: yaml<br> pattern
        r'yaml.*<br>.*apiVersion',      # YAML block with <br> tags
        r'<br>\s*apiVersion',           # <br> before apiVersion
        r'<br>\s*kind:',                # <br> before kind
        r'<br>\s*metadata:',            # <br> before metadata
        r'<br>\s*spec:',                # <br> before spec
        r'with:\s*yaml<br>'             # "with: yaml<br>" pattern
    ]
    
    violations = []
    for pattern in html_in_yaml_patterns:
        matches = re.findall(pattern, yaml_content, re.IGNORECASE | re.MULTILINE)
        if matches:
            violations.extend(matches)
    
    if violations:
        return {
            "status": "CRITICAL_BLOCK",
            "violations": violations,
            "action": "CONVERT_TO_PROPER_YAML_BLOCKS",
            "message": "HTML tags detected in YAML content - must use proper ```yaml blocks",
            "required_format": "```yaml\napiVersion: cluster.open-cluster-management.io/v1beta1\nkind: ClusterCurator\n```",
            "blocking_priority": "ABSOLUTE"
        }
    
    return {"status": "APPROVED", "yaml_format": "valid"}
```

### **Citation Detection Engine:**
```python
def enforce_citation_free_test_cases(test_case_content):
    """
    Real-time citation pattern detection and blocking
    """
    citation_patterns = [
        r'\[Source:.*?\]',           # [Source: anything]
        r'\*\[Source:.*?\]\*',       # *[Source: anything]*
        r'\(Source:.*?\)',           # (Source: anything)
        r'\[.*?:.*?:.*?\]',          # [Type:reference:metadata]
        r'Source:.*',                # Any "Source:" patterns
        r'\*\[.*?\]\*'               # Any bracketed references
    ]
    
    violations = []
    for pattern in citation_patterns:
        matches = re.findall(pattern, test_case_content)
        if matches:
            violations.extend(matches)
    
    if violations:
        return {
            "status": "BLOCKED",
            "violations": violations,
            "action": "REMOVE_ALL_CITATIONS",
            "message": "Test cases file must be citation-free"
        }
    
    return {"status": "APPROVED", "violations": []}
```

### **YAML Escape Sequence Detection Engine:**
```python
def enforce_yaml_block_formatting(test_content):
    """
    Critical: Detect and block escape sequence YAML formatting in CLI commands
    """
    # Detect escape sequence patterns in YAML
    escape_sequence_patterns = [
        r'`[^`]*\\n[^`]*`',                    # YAML with \n escape sequences in backticks
        r'"[^"]*\\n[^"]*"',                    # YAML with \n escape sequences in quotes
        r"'[^']*\\n[^']*'",                    # YAML with \n escape sequences in single quotes
        r'add:\s*`[^`]*apiVersion[^`]*\\n',    # Specific pattern: add: `apiVersion...\n
        r'and add:\s*`[^`]*apiVersion[^`]*\\n' # Specific pattern: and add: `apiVersion...\n
    ]
    
    violations = []
    for pattern in escape_sequence_patterns:
        matches = re.findall(pattern, test_content, re.MULTILINE | re.DOTALL)
        if matches:
            violations.extend(matches)
    
    if violations:
        return {
            "status": "CRITICAL_BLOCK",
            "violations": violations,
            "action": "CONVERT_TO_YAML_BLOCKS",
            "message": "YAML with escape sequences detected - must use proper indented blocks",
            "required_format": "```yaml\\napiVersion: v1\\nkind: Resource\\n```",
            "blocking_priority": "ABSOLUTE"
        }
    
    return {"status": "APPROVED", "yaml_format": "valid"}
```

### **Enhanced CLI Command Validation Engine:**
```python
def enforce_executable_cli_commands(test_table_content):
    """
    Validate that every CLI command is copy-paste executable
    """
    required_columns = ["UI Method", "CLI Method", "Expected Results"]
    missing_requirements = []
    
    # Check for console login CLI method requirement
    console_login_patterns = [
        r'Log into.*Console|Login.*ACM.*Console|Access.*Console',
        r'Navigate to.*console-openshift-console\.apps'
    ]
    
    has_console_login_step = False
    for pattern in console_login_patterns:
        if re.search(pattern, test_table_content, re.IGNORECASE):
            has_console_login_step = True
            break
    
    # If console login step exists, must have oc login CLI method
    if has_console_login_step:
        oc_login_pattern = r'oc login.*https://api\.|oc login.*--token'
        if not re.search(oc_login_pattern, test_table_content):
            missing_requirements.append("CRITICAL: Console login step missing oc login CLI command")
    
    # Check for executable CLI command patterns
    executable_patterns = [
        r'oc apply -f - <<EOF.*?EOF',          # Heredoc pattern
        r'```yaml.*?```',                       # YAML block pattern
        r'touch.*?\.yaml.*?```yaml.*?```',      # Touch file + YAML block pattern
        r'oc login.*https://api\.',             # oc login commands
        r'oc login.*--token'                    # Token-based login
    ]
    
    has_executable_format = False
    for pattern in executable_patterns:
        if re.search(pattern, test_table_content, re.DOTALL):
            has_executable_format = True
            break
    
    if not has_executable_format:
        missing_requirements.append("Executable CLI commands with proper YAML blocks")
    
    # Check for UI navigation patterns
    ui_pattern = r'\*\*UI.*?\*\*:|Console.*?→|Navigate to|Click'
    if not re.search(ui_pattern, test_table_content):
        missing_requirements.append("Clear UI navigation methods")
    
    # Block escape sequence YAML
    if re.search(r'\\n|\\t', test_table_content):
        missing_requirements.append("CRITICAL: Escape sequence YAML detected - use proper blocks")
    
    if missing_requirements:
        return {
            "status": "BLOCKED",
            "missing": missing_requirements,
            "action": "FIX_CLI_METHODS",
            "message": "All CLI methods must be copy-paste executable"
        }
    
    return {"status": "APPROVED", "missing": []}
```

### **Dual-Method Validation Engine:**
```python
def enforce_dual_method_coverage(test_table_content):
    """
    Validate that every step includes both UI and CLI methods
    """
    # Use enhanced CLI command validation
    cli_validation = enforce_executable_cli_commands(test_table_content)
    yaml_validation = enforce_yaml_block_formatting(test_table_content)
    
    if cli_validation["status"] == "BLOCKED":
        return cli_validation
    
    if yaml_validation["status"] == "CRITICAL_BLOCK":
        return yaml_validation
    
    return {"status": "APPROVED", "methods": "dual_coverage_validated"}
```

### **Complete Report Structure Validation:**
```python
def enforce_complete_report_structure(report_content):
    """
    Validate exact section order and content requirements for new structure
    """
    mandatory_sections = [
        "Summary",
        "1. JIRA Analysis Summary",
        "2. Environment Assessment", 
        "3. Implementation Analysis",
        "4. Test Scenarios Analysis"
    ]
    
    # Blocked sections from old structure
    blocked_sections = [
        "Documentation Analysis",
        "QE Intelligence Assessment", 
        "Feature Deployment Status",
        "Business Impact Assessment",
        "Executive Summary"
    ]
    
    section_validation = []
    
    # Check for mandatory sections
    for section in mandatory_sections:
        if section not in report_content:
            section_validation.append(f"Missing mandatory section: {section}")
    
    # Check for blocked sections
    for blocked_section in blocked_sections:
        if blocked_section in report_content:
            section_validation.append(f"Blocked section found: {blocked_section}")
    
    # Check for clickable links in Summary
    if "Feature Validation:" not in report_content:
        section_validation.append("Missing Feature Validation status in Summary")
    
    # Check for full JIRA title link
    if not re.search(r'\[.*?\]\(https://issues\.redhat\.com/browse/.*?\)', report_content):
        section_validation.append("Missing clickable JIRA link with full title")
    
    # Check for "Executive" usage
    if "Executive" in report_content:
        section_validation.append("Blocked word 'Executive' found in report")
    
    if section_validation:
        return {
            "status": "BLOCKED",
            "violations": section_validation,
            "action": "FIX_STRUCTURE",
            "message": "Complete report must follow new mandatory structure"
        }
    
    return {"status": "APPROVED", "structure_compliance": True}
```

## 🎯 **INTEGRATION WITH EXISTING AI SERVICES**

### **Framework Enforcement Integration:**
- **Real-time Validation**: Continuous monitoring during generation
- **Blocking Authority**: Can halt framework execution for violations
- **Automatic Correction**: Attempt to fix violations when possible
- **Quality Gates**: Final validation before output delivery

### **Service Coordination:**
- **Pattern Extension Service**: Validate generated patterns follow format requirements
- **Regression Prevention Service**: Integrate with existing quality enforcement
- **Universal Data Integration**: Ensure real data integration follows format standards
- **Configuration Automation**: Auto-update enforcement rules based on template changes

## 🚨 **COMPREHENSIVE ENFORCEMENT EXECUTION ENGINE**

### **Real-Time Format Validation Pipeline:**
```python
def comprehensive_format_enforcement(content, content_type):
    """
    Comprehensive real-time format enforcement for all content types
    """
    validation_results = []
    
    # 1. CRITICAL: HTML Tag Prevention (ALL content)
    html_validation = enforce_html_tag_prevention(content)
    if html_validation["status"] == "CRITICAL_BLOCK":
        return html_validation  # Immediate block
    
    # 2. CRITICAL: YAML HTML Prevention (CLI methods)
    if "yaml" in content.lower() or "oc apply" in content:
        yaml_html_validation = enforce_yaml_block_html_prevention(content)
        if yaml_html_validation["status"] == "CRITICAL_BLOCK":
            return yaml_html_validation  # Immediate block
    
    # 3. Content-specific validations
    if content_type == "test_cases":
        # Citation-free enforcement for test cases
        citation_validation = enforce_citation_free_test_cases(content)
        if citation_validation["status"] == "BLOCKED":
            return citation_validation
        
        # Dual-method coverage enforcement
        dual_method_validation = enforce_dual_method_coverage(content)
        if dual_method_validation["status"] == "BLOCKED":
            return dual_method_validation
    
    elif content_type == "complete_report":
        # Complete report structure enforcement
        structure_validation = enforce_complete_report_structure(content)
        if structure_validation["status"] == "BLOCKED":
            return structure_validation
    
    return {"status": "APPROVED", "content_validated": True}
```

### **Mandatory Integration Points:**
```python
def integrate_with_framework_generation():
    """
    Integration points with framework content generation
    """
    integration_checkpoints = {
        "test_step_generation": "validate_dual_method_coverage_and_cli_completeness",
        "yaml_content_creation": "enforce_html_free_yaml_blocks", 
        "cli_command_generation": "validate_executable_commands_and_console_login",
        "report_section_creation": "enforce_structure_and_citation_compliance",
        "final_output_delivery": "comprehensive_validation_all_requirements"
    }
    
    return integration_checkpoints
```

## 📊 **ENFORCEMENT METRICS**

### **Compliance Targets:**
- **HTML Tag Prevention**: 100% compliance (zero HTML tags, markdown-only)
- **Citation-Free Test Cases**: 100% compliance (zero tolerance)
- **Dual-Method Coverage**: 100% (every step must have both UI and CLI)
- **Complete CLI Commands**: 100% (no truncated or incomplete commands)
- **New Report Structure**: 100% (mandatory 4-section structure only)
- **Clickable Links**: 100% (all JIRA, PR, and environment links must be clickable)
- **Feature Validation Status**: 100% (clear validation status required in Summary)

### **Blocked Content Enforcement:**
- **"Executive" Usage**: 0% tolerance (blocked word in all content)
- **Old Report Sections**: 0% tolerance (Documentation, QE Intelligence, Business Impact, Feature Deployment sections blocked)
- **Non-Clickable References**: 0% tolerance (all links must be clickable)
- **HTML Tags**: 0% tolerance (automatic conversion to markdown)

### **Quality Improvements Expected:**
- **Tester Clarity**: 95% improvement in step execution clarity
- **Copy-Paste Readiness**: 100% CLI commands ready for immediate execution
- **Professional Presentation**: Clean test cases without HTML clutter or citations
- **Streamlined Analysis**: Focused 4-section reports with test scenarios focus
- **Link Accessibility**: 100% clickable links for immediate access to sources

This Format Enforcement Service ensures all user requirements are met with zero tolerance for deviations, providing professional-quality outputs with mandatory HTML tag prevention, clickable links, clear feature validation status, and streamlined report structure focused on test scenarios analysis.
