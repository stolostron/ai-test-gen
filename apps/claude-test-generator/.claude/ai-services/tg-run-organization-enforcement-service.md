# Test Generator Run Organization Enforcement Service

## 🚨 **CRITICAL: ZERO-TOLERANCE RUN ORGANIZATION ENFORCEMENT**

**Purpose**: Real-time enforcement service that prevents run organization violations with ABSOLUTE blocking authority. Ensures ONLY 3 final deliverable files exist after framework completion.

**Service Status**: V1.0 - Production Ready with Zero-Tolerance Enforcement
**Integration Level**: Core Framework Service - MANDATORY for all runs
**Authority**: BLOCKING - Can halt framework execution for organization violations

## 🔒 **ABSOLUTE ENFORCEMENT RULES**

### **1. SINGLE DIRECTORY GUARANTEE (CRITICAL)**

**REQUIREMENT**: Only ONE final run directory per execution

**BLOCKING CONDITIONS:**
```
BLOCKED_BEHAVIORS:
- Creating separate agent directories (runs/ACM-22079-QE-Intelligence-*)
- Creating multiple run directories for same ticket
- Leaving empty agent directories after consolidation
- Any subdirectory creation within run directory
```

**ENFORCEMENT ACTION:**
- **Real-time monitoring** of directory creation attempts
- **IMMEDIATE BLOCKING** when separate directories detected
- **AUTOMATIC CONSOLIDATION** of any separated content
- **FRAMEWORK HALT** if consolidation fails

### **2. FINAL DELIVERABLES ONLY (ABSOLUTE)**

**REQUIREMENT**: Exactly 3 files in final run directory

**MANDATORY FINAL STATE:**
```
runs/ACM-22079-20250820-140028/
├── Test-Cases-Report.md           # REQUIRED
├── Complete-Analysis-Report.md    # REQUIRED  
└── run-metadata.json             # REQUIRED
```

**BLOCKED FILE PATTERNS:**
```regex
INTERMEDIATE_FILES_BLOCKED:
- agent-*-results.md              # Agent analysis files
- *-analysis.md                   # Analysis intermediates
- *-investigation.md              # Investigation files
- *-intelligence-*.md             # Intelligence reports
- feature_availability_analysis.md # Specific agent files
- github_investigation_results.md  # GitHub analysis
- documentation_intelligence_summary.md # Doc analysis
- qe_automation_analysis.md       # QE analysis
```

### **3. ROOT DIRECTORY PROTECTION (ZERO-TOLERANCE)**

**REQUIREMENT**: NO intermediate files in root directory

**BLOCKED ROOT PATTERNS:**
```regex
ROOT_VIOLATIONS_BLOCKED:
- {JIRA_ID}-*-Intelligence-Report.md  # Documentation reports
- {JIRA_ID}-*-Analysis.md             # Analysis files
- {JIRA_ID}-*-Investigation.md        # Investigation files
- Any file not in proper run directory
```

**ENFORCEMENT ACTION:**
- **Prevention** of root directory intermediate file creation
- **IMMEDIATE REMOVAL** if files detected in root
- **BLOCKING AUTHORITY** to halt framework execution

## 🔧 **REAL-TIME ENFORCEMENT MECHANISMS**

### **Directory Creation Monitor**
```python
def enforce_single_directory_policy(action_type, target_path, jira_id):
    """
    Real-time monitoring and enforcement of directory creation
    """
    if action_type == "create_directory":
        # Check if attempting to create separate agent directory
        if re.match(r"runs/.*-(Intelligence|Analysis|Investigation)-.*", target_path):
            return {
                "status": "BLOCKED",
                "violation": "separate_agent_directory",
                "action": "PREVENT_CREATION",
                "message": f"Separate agent directories forbidden. Use main run directory only."
            }
        
        # Check if attempting subdirectory in run directory
        if target_path.count('/') > 1 and 'runs/' in target_path:
            return {
                "status": "BLOCKED", 
                "violation": "subdirectory_creation",
                "action": "PREVENT_CREATION",
                "message": "No subdirectories allowed in run directory"
            }
    
    return {"status": "APPROVED"}
```

### **File Creation Monitor**
```python
def enforce_file_creation_policy(file_path, content, jira_id):
    """
    Real-time monitoring of file creation attempts
    """
    # Check for root directory violations
    if not file_path.startswith('runs/'):
        for pattern in [f"{jira_id}-*-Intelligence-Report.md", 
                       f"{jira_id}-*-Analysis.md",
                       f"{jira_id}-*-Investigation.md"]:
            if fnmatch.fnmatch(file_path, pattern):
                return {
                    "status": "BLOCKED",
                    "violation": "root_directory_intermediate",
                    "action": "PREVENT_CREATION",
                    "message": f"Intermediate files forbidden in root directory. Use run directory: runs/{jira_id}-*/"
                }
    
    # Check for blocked intermediate file patterns
    filename = os.path.basename(file_path)
    blocked_patterns = [
        "agent-*-results.md",
        "*-analysis.md", 
        "*-investigation.md",
        "*-intelligence-*.md"
    ]
    
    for pattern in blocked_patterns:
        if fnmatch.fnmatch(filename, pattern) and 'runs/' in file_path:
            return {
                "status": "BLOCKED",
                "violation": "intermediate_file_creation",
                "action": "PREVENT_CREATION", 
                "message": f"Intermediate file {filename} blocked. Include content in final deliverables only."
            }
    
    return {"status": "APPROVED"}
```

### **Framework Completion Monitor**
```python
def enforce_final_state_validation(run_directory):
    """
    Validate final state before framework completion
    """
    required_files = [
        "Test-Cases-Report.md",
        "Complete-Analysis-Report.md", 
        "run-metadata.json"
    ]
    
    # Get actual files in directory
    actual_files = [f for f in os.listdir(run_directory) 
                   if os.path.isfile(os.path.join(run_directory, f))]
    
    # Check exact file count
    if len(actual_files) != 3:
        return {
            "status": "BLOCKED",
            "violation": "incorrect_file_count",
            "expected": 3,
            "actual": len(actual_files),
            "files_found": actual_files,
            "action": "HALT_FRAMEWORK",
            "message": f"Must have exactly 3 files, found {len(actual_files)}: {actual_files}"
        }
    
    # Check required files present
    missing_files = [f for f in required_files if f not in actual_files]
    if missing_files:
        return {
            "status": "BLOCKED",
            "violation": "missing_required_files",
            "missing": missing_files,
            "action": "HALT_FRAMEWORK", 
            "message": f"Missing required files: {missing_files}"
        }
    
    # Check no extra files
    extra_files = [f for f in actual_files if f not in required_files]
    if extra_files:
        return {
            "status": "BLOCKED",
            "violation": "extra_files_present",
            "extra": extra_files,
            "action": "TRIGGER_CLEANUP",
            "message": f"Extra files must be removed: {extra_files}"
        }
    
    return {
        "status": "APPROVED",
        "validation": "final_state_correct",
        "message": "Run organization compliant - exactly 3 required files present"
    }
```

## 🎯 **INTEGRATION WITH FRAMEWORK PHASES**

### **Phase 0: Pre-Execution Validation**
```python
def pre_execution_validation(jira_id, requested_environment):
    """
    Validate run organization setup before framework execution
    """
    # Ensure clean starting state
    check_for_existing_violations(jira_id)
    
    # Set up monitoring for new run
    initialize_run_directory_monitoring(jira_id)
    
    # Configure enforcement rules
    configure_real_time_enforcement(jira_id)
    
    return "READY_FOR_EXECUTION"
```

### **Phase 1-2.5: Real-Time Monitoring**
```python
def monitor_agent_execution(agent_name, action, target, jira_id):
    """
    Real-time monitoring during agent execution phases
    """
    # Monitor directory creation attempts
    if action == "create_directory":
        return enforce_single_directory_policy(action, target, jira_id)
    
    # Monitor file creation attempts  
    if action == "create_file":
        return enforce_file_creation_policy(target, None, jira_id)
    
    # Log approved actions for cleanup tracking
    log_approved_action(agent_name, action, target, jira_id)
    
    return {"status": "MONITORING_ACTIVE"}
```

### **Phase 4: Pre-Completion Enforcement**
```python
def pre_completion_enforcement(run_directory):
    """
    Final enforcement before framework completion
    """
    # Trigger automatic cleanup
    cleanup_result = trigger_automatic_cleanup(run_directory)
    
    if cleanup_result["status"] != "SUCCESS":
        return {
            "status": "BLOCKED",
            "violation": "cleanup_failure",
            "details": cleanup_result,
            "action": "HALT_FRAMEWORK"
        }
    
    # Validate final state
    validation_result = enforce_final_state_validation(run_directory)
    
    if validation_result["status"] != "APPROVED":
        return {
            "status": "BLOCKED",
            "violation": "final_state_invalid", 
            "details": validation_result,
            "action": "HALT_FRAMEWORK"
        }
    
    return {
        "status": "APPROVED",
        "final_state": "COMPLIANT",
        "message": "Run organization enforcement successful"
    }
```

## 🔍 **VIOLATION DETECTION ALGORITHMS**

### **QE Intelligence Violation Detection**
```python
def detect_qe_intelligence_violations(base_directory):
    """
    Detect specific QE Intelligence service violations
    """
    violations = []
    
    # Check for separate QE Intelligence directories
    pattern = "runs/*-QE-Intelligence-*"
    qe_dirs = glob.glob(pattern)
    
    if qe_dirs:
        violations.append({
            "type": "separate_qe_directory",
            "directories": qe_dirs,
            "action": "CONSOLIDATE_AND_REMOVE"
        })
    
    return violations
```

### **Documentation Intelligence Violation Detection**
```python
def detect_documentation_violations(base_directory):
    """
    Detect Documentation Intelligence root directory violations
    """
    violations = []
    
    # Check for root directory documentation reports
    pattern = "*-Documentation-Intelligence-Report.md"
    doc_files = glob.glob(pattern)
    
    if doc_files:
        violations.append({
            "type": "root_documentation_files",
            "files": doc_files,
            "action": "REMOVE_AND_CONSOLIDATE"
        })
    
    return violations
```

## 📊 **ENFORCEMENT METRICS AND MONITORING**

### **Compliance Tracking**
```json
{
  "enforcement_metrics": {
    "directory_violations_prevented": "count_per_run",
    "file_violations_blocked": "count_per_run", 
    "cleanup_operations_performed": "count_per_run",
    "final_state_compliance_rate": "percentage",
    "framework_halts_triggered": "count_per_run"
  },
  "performance_targets": {
    "directory_compliance": "100%",
    "file_compliance": "100%", 
    "cleanup_success_rate": "100%",
    "final_state_accuracy": "100%"
  }
}
```

### **Quality Assurance Integration**
- **Zero-Tolerance Policy**: No violations allowed to proceed
- **Automatic Recovery**: Attempt cleanup and consolidation before halting
- **Comprehensive Logging**: Track all enforcement actions for audit
- **Performance Monitoring**: Ensure enforcement doesn't impact execution speed

## 🚨 **MANDATORY INTEGRATION REQUIREMENTS**

### **Framework Integration** (CRITICAL)
- ❌ **BLOCKED**: Framework execution without enforcement service activation
- ❌ **BLOCKED**: Agent operations without real-time monitoring
- ❌ **BLOCKED**: Framework completion without final state validation
- ✅ **REQUIRED**: Enforcement integration with all agent execution phases
- ✅ **REQUIRED**: Real-time violation detection and blocking
- ✅ **MANDATORY**: Final state validation before completion

### **Service Integration Standards**
- **Blocking Authority**: Can halt any framework operation for violations
- **Real-Time Operation**: Continuous monitoring throughout execution
- **Automatic Recovery**: Attempt to fix violations before blocking
- **Zero-False-Positives**: Accurate detection with minimal performance impact

This Run Organization Enforcement Service ensures absolute compliance with the 3-file final deliverable requirement and prevents all forms of directory organization violations through real-time monitoring and blocking authority.