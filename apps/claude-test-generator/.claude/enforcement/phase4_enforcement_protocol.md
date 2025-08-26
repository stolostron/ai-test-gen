# Phase 4 Technical Enforcement Protocol

## 🚨 MANDATORY TECHNICAL ENFORCEMENT DURING PHASE 4

**Purpose**: Bridge the gap between semantic framework specifications and technical enforcement to prevent HTML tag violations and other format breaches during content generation.

**Status**: CRITICAL ENFORCEMENT - Must be followed without exception during Phase 4

## 🔒 PRE-WRITE VALIDATION REQUIREMENT

### **MANDATORY VALIDATION BEFORE ANY WRITE TOOL USAGE**

Before using the Write tool during Phase 4, the following technical validation MUST be performed:

```bash
# MANDATORY: Run validation before Write tool
python .claude/enforcement/pre_write_validator.py "<file_path>" "<content>"

# Validation returns:
# - Exit code 0: Content approved, proceed with Write
# - Exit code 1: Content BLOCKED, fix violations before proceeding
```

### **BLOCKING AUTHORITY**

The validation service has **strict BLOCKING AUTHORITY**:
- ❌ **BLOCKED**: Write tool usage if validation fails
- ❌ **BLOCKED**: Content generation with HTML tags 
- ❌ **BLOCKED**: Test cases with citations
- ❌ **BLOCKED**: Missing dual method coverage
- ✅ **APPROVED**: Only when all validations pass

## 🎯 PHASE 4 EXECUTION PROTOCOL

### **STEP 1: Content Preparation**
1. Prepare content for test cases or analysis report
2. Ensure content follows documented format requirements
3. Review for HTML tags, citations, and format compliance

### **STEP 2: MANDATORY VALIDATION**
```bash
# For test cases file
python .claude/enforcement/pre_write_validator.py "runs/ACM-XXXXX/Test-Cases.md" "$CONTENT"

# For complete analysis file  
python .claude/enforcement/pre_write_validator.py "runs/ACM-XXXXX/Complete-Analysis.md" "$CONTENT"
```

### **STEP 3: CONDITIONAL WRITE**
- **IF validation passes**: Proceed with Write tool
- **IF validation fails**: Fix violations and re-validate

### **STEP 4: POST-WRITE VERIFICATION**
1. Verify file was created successfully
2. Confirm content matches approved version
3. Document validation in run metadata

## 🔧 TECHNICAL VALIDATION PATTERNS

### **HTML Tag Detection (CRITICAL)**
```python
# Patterns that trigger CRITICAL_BLOCK
html_patterns = [
    r'<br\s*/?>', 
    r'<[^>]+>',
    r'&lt;',
    r'&gt;',
    r'&amp;'
]
```

### **YAML Block HTML Prevention (CRITICAL)**
```python
# Patterns that trigger CRITICAL_BLOCK in YAML content
yaml_html_patterns = [
    r'yaml<br>',
    r'yaml.*<br>.*apiVersion',
    r'<br>\s*apiVersion',
    r'<br>\s*kind:',
    r'<br>\s*metadata:',
    r'<br>\s*spec:'
]
```

### **Citation Detection in Test Cases (BLOCKED)**
```python
# Patterns that trigger BLOCKED for test cases
citation_patterns = [
    r'\[Source:.*?\]',
    r'\*\[Source:.*?\]\*',
    r'\(Source:.*?\)',
    r'\[.*?:.*?:.*?\]',
    r'\[Code:.*?\]',
    r'\[GitHub:.*?\]',
    r'\[JIRA:.*?\]',
    r'\[Docs:.*?\]'
]
```

## 🚨 ENFORCEMENT EXAMPLES

### **Example 1: HTML Tag Violation BLOCKED**
```bash
$ python .claude/enforcement/pre_write_validator.py "test-cases.md" "Create YAML:<br/>```yaml<br/>apiVersion:"

🚨 WRITE BLOCKED: test-cases.md
📋 Reason: HTML tags detected in YAML content - must use proper ```yaml blocks
🔧 Required Action: CONVERT_TO_PROPER_YAML_BLOCKS
⚠️  Specific Violations:
   - <br/>
   - <br/>
✅ Required Fix: ```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
```

❌ CONTENT GENERATION BLOCKED - Fix violations before proceeding
```

### **Example 2: Validation Success**
```bash
$ python .claude/enforcement/pre_write_validator.py "test-cases.md" "Create YAML file:
```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
```"

✅ VALIDATION PASSED: test-cases.md - Content approved for writing
```

## 🔄 INTEGRATION WITH FRAMEWORK WORKFLOW

### **Framework Modification Required**
During Phase 4 execution, the following process MUST be followed:

1. **Content Generation**: Prepare content following semantic specifications
2. **MANDATORY VALIDATION**: Execute technical validation using enforcement scripts
3. **Conditional Proceed**: Only use Write tool if validation passes
4. **Error Handling**: Fix violations and re-validate if blocked
5. **Success Path**: Continue with file creation only after validation approval

### **No More Semantic-Only Enforcement**
- ❌ **ELIMINATED**: Relying solely on semantic compliance
- ❌ **ELIMINATED**: Bypassing format requirements during generation
- ✅ **IMPLEMENTED**: Technical validation with blocking authority
- ✅ **IMPLEMENTED**: Executable enforcement preventing violations

## 📊 AUDIT AND LOGGING

### **Validation Logging**
All validation attempts are logged for audit purposes:
```json
{
  "file_path": "runs/ACM-22079/Test-Cases.md",
  "content_type": "test_cases", 
  "result": {
    "status": "CRITICAL_BLOCK",
    "violations": ["<br/>", "<br/>"],
    "message": "HTML tags detected in YAML content"
  },
  "timestamp": "2025-08-21T18:45:00Z"
}
```

### **Success Metrics**
- **HTML Tag Prevention**: comprehensive blocking of HTML tag violations
- **Format Compliance**: comprehensive adherence to documented requirements
- **Technical Enforcement**: comprehensive validation before Write tool usage
- **Audit Trail**: Complete logging of all validation attempts

## 🎯 IMPLEMENTATION enforcement

**strict ENFORCEMENT PROMISE**:
- ✅ Technical validation replaces semantic-only enforcement
- ✅ Blocking authority prevents HTML tag violations
- ✅ Executable code validates content before Write tool usage
- ✅ Framework reliability through technical rather than semantic compliance

This protocol ensures that the documented format enforcement specifications are technically implemented and cannot be bypassed during Phase 4 content generation.