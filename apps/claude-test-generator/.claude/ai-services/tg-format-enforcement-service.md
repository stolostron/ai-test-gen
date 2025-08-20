# Test Generator Format Enforcement Service

## 🚨 **CRITICAL: MANDATORY FORMAT ENFORCEMENT**

**Purpose**: Real-time format validation service that enforces user-specified requirements for test case format, complete report structure, and content standards with BLOCKING authority.

**Service Status**: V1.0 - Production Ready with Zero-Tolerance Enforcement
**Integration Level**: Core Quality Service - MANDATORY for all output generation
**Authority**: BLOCKING - Can halt framework execution for format violations

## 🔒 **ZERO-TOLERANCE ENFORCEMENT RULES**

### **1. CITATION-FREE TEST CASES (ABSOLUTE)**

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

### **2. MANDATORY DUAL-METHOD COVERAGE**

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

### **3. COMPLETE CLI COMMANDS + FULL YAML**

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
## 1. Feature Deployment Status
### **Feature Availability: [DEPLOYED/NOT_DEPLOYED/PARTIALLY_DEPLOYED]**
[Supporting data and evidence]

## 2A. Feature Validation Results (IF DEPLOYED)
### **Validation Status: [PASSED/FAILED/PARTIAL]**
[Validation tests and results]

## 2B. Feature Validation Limitation (IF NOT DEPLOYED)  
### **Validation Status: NOT POSSIBLE**
[Clear explanation of limitation]

## 3. Test Environment Status
### **Environment Summary:**
[Cluster details and capabilities]

## 4. Feature Implementation Analysis
### **Implementation Overview:**
[Verbal conceptual explanations with exact code portions]

## 5. Main Test Scenarios
### **Test Case 1: [Title]**
[Purpose, logic, and coverage explanation]

## 6. Business Impact
### **Customer Value:**
[Customer impact and business value]

## 7. Quality Metrics
### **Implementation Quality:**
[Quality assessment and metrics]

## 8. Conclusion
### **Summary Assessment:**
[Final summary and recommendations]
```

**BLOCKING CONDITIONS:**
- ❌ **BLOCK**: Missing any required section
- ❌ **BLOCK**: Sections in wrong order
- ❌ **BLOCK**: Modified section headings
- ❌ **BLOCK**: Missing mandatory subsections

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

### **Dual-Method Validation Engine:**
```python
def enforce_dual_method_coverage(test_table_content):
    """
    Validate that every step includes both UI and CLI methods
    """
    required_columns = ["UI Method", "CLI Method", "Expected Results"]
    missing_requirements = []
    
    # Check for complete CLI commands
    cli_command_pattern = r'oc apply -f - <<EOF.*?EOF'
    if not re.search(cli_command_pattern, test_table_content, re.DOTALL):
        missing_requirements.append("Complete CLI commands with full YAML")
    
    # Check for UI navigation patterns
    ui_pattern = r'\*\*UI.*?\*\*:|Console.*?→'
    if not re.search(ui_pattern, test_table_content):
        missing_requirements.append("Clear UI navigation methods")
    
    if missing_requirements:
        return {
            "status": "BLOCKED",
            "missing": missing_requirements,
            "action": "ADD_MISSING_METHODS",
            "message": "All steps must include both UI and CLI methods"
        }
    
    return {"status": "APPROVED", "missing": []}
```

### **Complete Report Structure Validation:**
```python
def enforce_complete_report_structure(report_content):
    """
    Validate exact section order and content requirements
    """
    mandatory_sections = [
        "Feature Deployment Status",
        "Test Environment Status", 
        "Feature Implementation Analysis",
        "Main Test Scenarios",
        "Business Impact",
        "Quality Metrics",
        "Conclusion"
    ]
    
    section_validation = []
    for i, section in enumerate(mandatory_sections):
        if section not in report_content:
            section_validation.append(f"Missing section: {section}")
        # Add order validation logic
    
    # Check for deployment status format
    if "Feature Availability:" not in report_content:
        section_validation.append("Missing explicit deployment status declaration")
    
    if section_validation:
        return {
            "status": "BLOCKED",
            "violations": section_validation,
            "action": "FIX_STRUCTURE",
            "message": "Complete report must follow exact template structure"
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

## 📊 **ENFORCEMENT METRICS**

### **Compliance Targets:**
- **Citation-Free Test Cases**: 100% compliance (zero tolerance)
- **Dual-Method Coverage**: 100% (every step must have both UI and CLI)
- **Complete CLI Commands**: 100% (no truncated or incomplete commands)
- **Fixed Report Structure**: 100% (exact template compliance required)

### **Quality Improvements Expected:**
- **Tester Clarity**: 95% improvement in step execution clarity
- **Copy-Paste Readiness**: 100% CLI commands ready for immediate execution
- **Professional Presentation**: Clean test cases without technical clutter
- **Comprehensive Analysis**: Complete reports with consistent structure and content

This Format Enforcement Service ensures all user requirements are met with zero tolerance for deviations, providing professional-quality outputs with clear separation between clean test cases and comprehensive analysis reports.
