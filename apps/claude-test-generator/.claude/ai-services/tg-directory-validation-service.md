# Test Generator Directory Validation Service

## 🔍 **CRITICAL: CONTINUOUS DIRECTORY STRUCTURE VALIDATION**

**Purpose**: Real-time validation service that monitors directory structure compliance and prevents violations through continuous monitoring and immediate intervention.

**Service Status**: V1.0 - Production Ready with Continuous Monitoring
**Integration Level**: Core Framework Service - MANDATORY for all operations
**Authority**: BLOCKING - Can halt operations for structure violations

## 🔒 **CONTINUOUS VALIDATION RULES**

### **1. SINGLE DIRECTORY STRUCTURE VALIDATION**

**REQUIREMENT**: Maintain single consolidated run directory structure

**MONITORED STRUCTURE:**
```
✅ COMPLIANT STRUCTURE:
apps/claude-test-generator/
├── runs/
│   └── ACM-22079-20250820-140028/     # Single main run directory
│       ├── Test-Cases-Report.md       # Final deliverable
│       ├── Complete-Analysis-Report.md # Final deliverable
│       └── run-metadata.json          # Final deliverable
└── [no intermediate files in root]

❌ VIOLATION EXAMPLES:
├── runs/
│   ├── ACM-22079-20250820-140028/     # Main directory
│   └── ACM-22079-QE-Intelligence-*/   # VIOLATION: Separate agent directory
├── ACM-22079-Documentation-*.md       # VIOLATION: Root intermediate file
└── agent-analysis-results.md          # VIOLATION: Root agent file
```

**VALIDATION ALGORITHM:**
```python
def validate_directory_structure(base_directory, jira_id):
    """
    Continuous validation of directory structure compliance
    """
    violations = []
    
    # Check for single run directory
    runs_dir = os.path.join(base_directory, 'runs')
    if os.path.exists(runs_dir):
        run_directories = [d for d in os.listdir(runs_dir) 
                          if os.path.isdir(os.path.join(runs_dir, d))]
        
        # Find main run directory
        main_run_dirs = [d for d in run_directories if jira_id in d and not any(
            pattern in d for pattern in ['-QE-Intelligence-', '-Analysis-', '-Investigation-']
        )]
        
        # Check for multiple main directories
        if len(main_run_dirs) > 1:
            violations.append({
                "type": "multiple_main_directories",
                "directories": main_run_dirs,
                "severity": "CRITICAL",
                "action": "CONSOLIDATE_DIRECTORIES"
            })
        
        # Check for separate agent directories
        agent_dirs = [d for d in run_directories if any(
            pattern in d for pattern in ['-QE-Intelligence-', '-Analysis-', '-Investigation-']
        )]
        
        if agent_dirs:
            violations.append({
                "type": "separate_agent_directories",
                "directories": agent_dirs,
                "severity": "CRITICAL", 
                "action": "CONSOLIDATE_AND_REMOVE"
            })
    
    # Check for root directory violations
    root_violations = check_root_directory_violations(base_directory, jira_id)
    violations.extend(root_violations)
    
    return {
        "status": "VIOLATIONS_DETECTED" if violations else "COMPLIANT",
        "violations": violations,
        "timestamp": datetime.now().isoformat()
    }
```

### **2. FILE COUNT VALIDATION**

**REQUIREMENT**: Monitor file count compliance in run directory

**VALIDATION STATES:**
```python
VALIDATION_STATES = {
    "INITIAL": {
        "max_files": 50,  # Allow intermediate files during processing
        "monitoring": "PERMISSIVE"
    },
    "PROCESSING": {
        "max_files": 100, # Allow temporary files during agent execution
        "monitoring": "ACTIVE"
    },
    "PRE_COMPLETION": {
        "max_files": 10,  # Begin cleanup phase
        "monitoring": "STRICT"
    },
    "COMPLETION": {
        "exact_files": 3, # Exactly 3 final deliverables
        "monitoring": "ZERO_TOLERANCE"
    }
}
```

**FILE COUNT MONITORING:**
```python
def validate_file_count(run_directory, validation_state):
    """
    Monitor file count based on current validation state
    """
    if not os.path.exists(run_directory):
        return {"status": "NO_DIRECTORY", "action": "CREATE_DIRECTORY"}
    
    files = [f for f in os.listdir(run_directory) 
            if os.path.isfile(os.path.join(run_directory, f))]
    file_count = len(files)
    
    state_config = VALIDATION_STATES[validation_state]
    
    if validation_state == "COMPLETION":
        # Zero tolerance for completion state
        if file_count != state_config["exact_files"]:
            return {
                "status": "VIOLATION",
                "violation_type": "incorrect_final_file_count",
                "expected": state_config["exact_files"],
                "actual": file_count,
                "files": files,
                "action": "TRIGGER_CLEANUP" if file_count > 3 else "REGENERATE_MISSING"
            }
    else:
        # Check maximum limits for other states
        if file_count > state_config["max_files"]:
            return {
                "status": "WARNING",
                "violation_type": "excessive_file_count",
                "max_allowed": state_config["max_files"],
                "actual": file_count,
                "action": "MONITOR_CLOSELY"
            }
    
    return {
        "status": "COMPLIANT",
        "file_count": file_count,
        "validation_state": validation_state
    }
```

### **3. ROOT DIRECTORY PROTECTION**

**REQUIREMENT**: Prevent intermediate file creation in root directory

**PROTECTED ROOT STRUCTURE:**
```
✅ ALLOWED IN ROOT:
├── .claude/                    # Configuration directory
├── runs/                       # Run results directory
├── docs/                       # Documentation
├── CLAUDE.md                   # Configuration file
├── README.md                   # Project documentation
└── [standard project files]

❌ BLOCKED IN ROOT:
├── ACM-*-Intelligence-Report.md    # Agent reports
├── ACM-*-Analysis.md               # Analysis files
├── agent-*-results.md              # Agent results
├── *-investigation.md              # Investigation files
└── [any intermediate files]
```

**ROOT PROTECTION ALGORITHM:**
```python
def validate_root_directory_protection(base_directory, jira_id):
    """
    Validate root directory protection against intermediate files
    """
    violations = []
    
    # Define allowed patterns in root
    allowed_patterns = [
        ".claude/*",
        "runs/*", 
        "docs/*",
        "CLAUDE.md",
        "README.md",
        "*.py",
        "*.json",
        ".git*"
    ]
    
    # Define blocked patterns
    blocked_patterns = [
        f"{jira_id}-*-Intelligence-Report.md",
        f"{jira_id}-*-Analysis.md",
        f"{jira_id}-*-Investigation.md", 
        "agent-*-results.md",
        "*-analysis.md",
        "*-investigation.md"
    ]
    
    for item in os.listdir(base_directory):
        item_path = os.path.join(base_directory, item)
        
        if os.path.isfile(item_path):
            # Check if file matches blocked patterns
            for pattern in blocked_patterns:
                if fnmatch.fnmatch(item, pattern):
                    violations.append({
                        "type": "root_intermediate_file",
                        "file": item,
                        "pattern_matched": pattern,
                        "severity": "CRITICAL",
                        "action": "IMMEDIATE_REMOVAL"
                    })
                    break
    
    return violations
```

## 🔧 **REAL-TIME MONITORING SYSTEM**

### **Continuous Monitoring Engine**
```python
class DirectoryValidationMonitor:
    def __init__(self, base_directory, jira_id):
        self.base_directory = base_directory
        self.jira_id = jira_id
        self.validation_state = "INITIAL"
        self.monitoring_active = True
        self.violation_log = []
    
    def start_monitoring(self):
        """
        Start continuous directory structure monitoring
        """
        while self.monitoring_active:
            # Validate directory structure
            structure_result = validate_directory_structure(
                self.base_directory, self.jira_id
            )
            
            # Validate file count
            run_dir = self.find_main_run_directory()
            if run_dir:
                count_result = validate_file_count(run_dir, self.validation_state)
            else:
                count_result = {"status": "NO_DIRECTORY"}
            
            # Validate root protection
            root_violations = validate_root_directory_protection(
                self.base_directory, self.jira_id
            )
            
            # Process violations
            if structure_result["violations"] or root_violations or count_result["status"] == "VIOLATION":
                self.handle_violations(structure_result, count_result, root_violations)
            
            time.sleep(1)  # Check every second during active processing
    
    def handle_violations(self, structure_result, count_result, root_violations):
        """
        Handle detected violations with appropriate actions
        """
        all_violations = structure_result["violations"] + root_violations
        
        if count_result["status"] == "VIOLATION":
            all_violations.append({
                "type": "file_count_violation",
                "details": count_result,
                "severity": "CRITICAL"
            })
        
        # Process by severity
        critical_violations = [v for v in all_violations if v["severity"] == "CRITICAL"]
        
        if critical_violations:
            self.trigger_immediate_intervention(critical_violations)
        
        # Log all violations
        self.violation_log.extend(all_violations)
```

### **Immediate Intervention System**
```python
def trigger_immediate_intervention(violations):
    """
    Take immediate action for critical violations
    """
    interventions = []
    
    for violation in violations:
        if violation["type"] == "separate_agent_directories":
            # Trigger consolidation
            result = consolidate_agent_directories(violation["directories"])
            interventions.append({
                "violation": violation,
                "action": "consolidation",
                "result": result
            })
        
        elif violation["type"] == "root_intermediate_file":
            # Remove root intermediate file
            file_path = os.path.join(base_directory, violation["file"])
            os.remove(file_path)
            interventions.append({
                "violation": violation,
                "action": "file_removal",
                "file": violation["file"]
            })
        
        elif violation["type"] == "incorrect_final_file_count":
            # Trigger cleanup
            result = trigger_cleanup_automation(violation["details"])
            interventions.append({
                "violation": violation, 
                "action": "cleanup_trigger",
                "result": result
            })
    
    return interventions
```

## 🎯 **VALIDATION CHECKPOINTS**

### **Framework Phase Integration**
```python
def execute_validation_checkpoint(phase, run_directory, jira_id):
    """
    Execute validation checkpoints at specific framework phases
    """
    checkpoints = {
        "pre_execution": validate_clean_initial_state,
        "post_phase_1": validate_initial_agent_outputs,
        "post_phase_2": validate_investigation_outputs,
        "post_phase_2_5": validate_qe_analysis_outputs,
        "pre_completion": validate_pre_completion_state,
        "post_completion": validate_final_deliverable_state
    }
    
    if phase in checkpoints:
        validation_function = checkpoints[phase]
        result = validation_function(run_directory, jira_id)
        
        # Update validation state based on phase
        update_validation_state(phase)
        
        return result
    
    return {"status": "CHECKPOINT_NOT_FOUND", "phase": phase}
```

### **State Transition Management**
```python
def update_validation_state(current_phase):
    """
    Update validation state based on current framework phase
    """
    state_mapping = {
        "pre_execution": "INITIAL",
        "post_phase_1": "PROCESSING", 
        "post_phase_2": "PROCESSING",
        "post_phase_2_5": "PROCESSING",
        "pre_completion": "PRE_COMPLETION",
        "post_completion": "COMPLETION"
    }
    
    new_state = state_mapping.get(current_phase, "INITIAL")
    
    # Log state transition
    log_state_transition(current_phase, new_state)
    
    return new_state
```

## 📊 **VALIDATION REPORTING AND METRICS**

### **Compliance Monitoring Dashboard**
```json
{
  "validation_metrics": {
    "directory_structure_compliance": "percentage",
    "file_count_compliance": "percentage", 
    "root_protection_compliance": "percentage",
    "violations_detected_per_run": "count",
    "violations_resolved_automatically": "count",
    "critical_violations_requiring_halt": "count"
  },
  "performance_targets": {
    "structure_compliance": "100%",
    "file_count_accuracy": "100%",
    "root_protection": "100%",
    "automatic_resolution_rate": "95%",
    "detection_latency": "<1_second"
  }
}
```

### **Violation Report Generation**
```python
def generate_validation_report(validation_log, jira_id):
    """
    Generate comprehensive validation report
    """
    report = {
        "jira_id": jira_id,
        "validation_summary": {
            "total_violations": len(validation_log),
            "critical_violations": len([v for v in validation_log if v["severity"] == "CRITICAL"]),
            "resolved_violations": len([v for v in validation_log if v.get("resolved", False)]),
            "final_compliance_status": "COMPLIANT" if all(v.get("resolved", False) for v in validation_log) else "NON_COMPLIANT"
        },
        "violation_breakdown": categorize_violations(validation_log),
        "resolution_actions": extract_resolution_actions(validation_log),
        "compliance_timeline": generate_compliance_timeline(validation_log)
    }
    
    return report
```

## 🚨 **MANDATORY INTEGRATION REQUIREMENTS**

### **Framework Integration** (CRITICAL)
- ❌ **BLOCKED**: Framework execution without validation service activation
- ❌ **BLOCKED**: Agent operations without structure monitoring
- ❌ **BLOCKED**: Framework completion without final validation
- ✅ **REQUIRED**: Continuous monitoring throughout all phases
- ✅ **REQUIRED**: Real-time violation detection and intervention
- ✅ **MANDATORY**: Compliance validation before completion

### **Service Integration Standards**
- **Real-Time Monitoring**: Continuous validation during execution
- **Immediate Intervention**: Automatic correction of violations
- **Comprehensive Reporting**: Detailed violation tracking and resolution
- **Zero-Tolerance Completion**: Framework cannot complete with violations

This Directory Validation Service ensures continuous compliance with directory structure requirements and provides immediate intervention for violations, maintaining the integrity of the single consolidated directory architecture throughout framework execution.