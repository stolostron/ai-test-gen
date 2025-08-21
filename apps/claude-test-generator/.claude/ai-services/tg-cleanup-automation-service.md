# Test Generator Cleanup Automation Service

## 🧹 **CRITICAL: AUTOMATIC CLEANUP ENFORCEMENT**

**Purpose**: Automated cleanup service that removes all intermediate files and consolidates content to ensure EXACTLY 3 final deliverable files remain in run directory.

**Service Status**: V1.0 - Production Ready with Zero-Tolerance Cleanup
**Integration Level**: Core Framework Service - MANDATORY for completion
**Authority**: BLOCKING - Framework cannot complete without successful cleanup

## 🔒 **AUTOMATIC CLEANUP PROCEDURES**

### **1. INTERMEDIATE FILE REMOVAL (MANDATORY)**

**PROCEDURE**: Remove all intermediate agent files from run directory

**TARGET PATTERNS:**
```regex
INTERMEDIATE_FILES_TO_REMOVE:
- agent-*-results.md              # Agent analysis files
- *-analysis.md                   # Analysis intermediates  
- *-investigation.md              # Investigation files
- *-intelligence-*.md             # Intelligence reports
- feature_availability_analysis.md # Feature analysis
- github_investigation_results.md  # GitHub analysis
- documentation_intelligence_summary.md # Doc analysis
- qe_automation_analysis.md       # QE analysis
- *-summary.md                    # Summary files
- *-report.md (except final deliverables) # Intermediate reports
```

**CLEANUP ALGORITHM:**
```python
def remove_intermediate_files(run_directory):
    """
    Remove all intermediate files while preserving final deliverables
    """
    # Protected files that must NOT be removed
    protected_files = [
        "Test-Cases-Report.md",
        "Complete-Analysis-Report.md", 
        "run-metadata.json"
    ]
    
    # Patterns of files to remove
    removal_patterns = [
        "agent-*-results.md",
        "*-analysis.md", 
        "*-investigation.md",
        "*-intelligence-*.md",
        "feature_availability_analysis.md",
        "github_investigation_results.md",
        "documentation_intelligence_summary.md",
        "qe_automation_analysis.md"
    ]
    
    removed_files = []
    
    for file in os.listdir(run_directory):
        if file in protected_files:
            continue  # Skip final deliverables
            
        file_path = os.path.join(run_directory, file)
        if os.path.isfile(file_path):
            # Check if file matches removal patterns
            for pattern in removal_patterns:
                if fnmatch.fnmatch(file, pattern):
                    os.remove(file_path)
                    removed_files.append(file)
                    break
    
    return {
        "status": "SUCCESS",
        "removed_files": removed_files,
        "remaining_files": [f for f in os.listdir(run_directory) 
                           if os.path.isfile(os.path.join(run_directory, f))]
    }
```

### **2. SEPARATE DIRECTORY CONSOLIDATION (CRITICAL)**

**PROCEDURE**: Consolidate any separate agent directories and remove them

**TARGET DIRECTORY PATTERNS:**
```regex
DIRECTORIES_TO_CONSOLIDATE:
- runs/*-QE-Intelligence-*        # QE Intelligence directories
- runs/*-Analysis-*               # Analysis directories  
- runs/*-Investigation-*          # Investigation directories
- runs/agent-*                    # Agent-specific directories
- Any subdirectory within run directory
```

**CONSOLIDATION ALGORITHM:**
```python
def consolidate_separate_directories(base_runs_directory, main_run_directory):
    """
    Find separate agent directories and consolidate useful content
    """
    consolidated_content = []
    removed_directories = []
    
    # Find all directories in runs folder
    for item in os.listdir(base_runs_directory):
        item_path = os.path.join(base_runs_directory, item)
        
        if os.path.isdir(item_path) and item_path != main_run_directory:
            # Check if it's a separate agent directory
            if any(pattern in item for pattern in ['-QE-Intelligence-', '-Analysis-', '-Investigation-']):
                
                # Extract any useful content for consolidation
                useful_content = extract_useful_content(item_path)
                
                if useful_content:
                    # Consolidate into main run directory final deliverables
                    consolidate_into_final_deliverables(useful_content, main_run_directory)
                    consolidated_content.append({
                        "source_directory": item,
                        "content_consolidated": useful_content
                    })
                
                # Remove the separate directory
                shutil.rmtree(item_path)
                removed_directories.append(item)
    
    return {
        "status": "SUCCESS",
        "consolidated_content": consolidated_content,
        "removed_directories": removed_directories
    }
```

### **3. ROOT DIRECTORY CLEANUP (ZERO-TOLERANCE)**

**PROCEDURE**: Remove any intermediate files created in root directory

**TARGET ROOT PATTERNS:**
```regex
ROOT_FILES_TO_REMOVE:
- {JIRA_ID}-*-Intelligence-Report.md  # Documentation reports
- {JIRA_ID}-*-Analysis.md             # Analysis files
- {JIRA_ID}-*-Investigation.md        # Investigation files
- *-summary.md                        # Summary files
- Any intermediate file outside run directory
```

**ROOT CLEANUP ALGORITHM:**
```python
def cleanup_root_directory(root_directory, jira_id):
    """
    Remove any intermediate files from root directory
    """
    removed_files = []
    
    # Patterns to remove from root
    removal_patterns = [
        f"{jira_id}-*-Intelligence-Report.md",
        f"{jira_id}-*-Analysis.md", 
        f"{jira_id}-*-Investigation.md",
        "*-summary.md",
        "agent-*-results.md"
    ]
    
    for file in os.listdir(root_directory):
        if file.startswith('runs/'):
            continue  # Skip runs directory
            
        file_path = os.path.join(root_directory, file)
        if os.path.isfile(file_path):
            # Check if file matches removal patterns
            for pattern in removal_patterns:
                if fnmatch.fnmatch(file, pattern):
                    os.remove(file_path)
                    removed_files.append(file)
                    break
    
    return {
        "status": "SUCCESS", 
        "removed_root_files": removed_files
    }
```

## 🔧 **CONTENT CONSOLIDATION STRATEGIES**

### **Useful Content Extraction**
```python
def extract_useful_content(separate_directory):
    """
    Extract content that should be preserved during consolidation
    """
    useful_content = {}
    
    for file in os.listdir(separate_directory):
        file_path = os.path.join(separate_directory, file)
        
        if os.path.isfile(file_path) and file.endswith('.md'):
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Extract key insights for consolidation
            if 'QE Intelligence' in file or 'qe' in file.lower():
                useful_content['qe_insights'] = extract_qe_insights(content)
            elif 'Documentation' in file or 'doc' in file.lower():
                useful_content['doc_insights'] = extract_documentation_insights(content)
            elif 'GitHub' in file or 'github' in file.lower():
                useful_content['github_insights'] = extract_github_insights(content)
    
    return useful_content
```

### **Final Deliverable Integration**
```python
def consolidate_into_final_deliverables(useful_content, main_run_directory):
    """
    Integrate useful content into final deliverable files
    """
    complete_analysis_path = os.path.join(main_run_directory, "Complete-Analysis-Report.md")
    
    if os.path.exists(complete_analysis_path):
        with open(complete_analysis_path, 'r') as f:
            current_content = f.read()
        
        # Enhance existing sections with consolidated insights
        enhanced_content = enhance_analysis_with_insights(current_content, useful_content)
        
        with open(complete_analysis_path, 'w') as f:
            f.write(enhanced_content)
        
        return {"status": "CONSOLIDATED", "target": "Complete-Analysis-Report.md"}
    
    return {"status": "NO_TARGET_FILE"}
```

## 🎯 **CLEANUP EXECUTION PIPELINE**

### **Phase 1: Pre-Cleanup Assessment**
```python
def assess_cleanup_requirements(base_directory, jira_id):
    """
    Assess what needs to be cleaned up before starting
    """
    assessment = {
        "intermediate_files": [],
        "separate_directories": [],
        "root_violations": [],
        "current_file_count": 0
    }
    
    # Find main run directory
    main_run_dir = find_main_run_directory(base_directory, jira_id)
    
    if main_run_dir:
        # Count current files in main directory
        files = [f for f in os.listdir(main_run_dir) 
                if os.path.isfile(os.path.join(main_run_dir, f))]
        assessment["current_file_count"] = len(files)
        
        # Identify intermediate files
        for file in files:
            if not file in ["Test-Cases-Report.md", "Complete-Analysis-Report.md", "run-metadata.json"]:
                assessment["intermediate_files"].append(file)
    
    # Find separate directories
    for item in os.listdir(base_directory + '/runs'):
        if item != os.path.basename(main_run_dir) and os.path.isdir(base_directory + '/runs/' + item):
            assessment["separate_directories"].append(item)
    
    # Check root directory
    for file in os.listdir(base_directory):
        if any(pattern in file for pattern in [f"{jira_id}-", "Intelligence-Report", "Analysis.md"]):
            assessment["root_violations"].append(file)
    
    return assessment
```

### **Phase 2: Execute Cleanup Operations**
```python
def execute_comprehensive_cleanup(base_directory, jira_id):
    """
    Execute all cleanup operations in correct order
    """
    cleanup_log = {
        "phase_1_assessment": None,
        "phase_2_intermediate_removal": None,
        "phase_3_directory_consolidation": None, 
        "phase_4_root_cleanup": None,
        "phase_5_final_validation": None
    }
    
    # Phase 1: Assessment
    cleanup_log["phase_1_assessment"] = assess_cleanup_requirements(base_directory, jira_id)
    
    # Phase 2: Remove intermediate files
    main_run_dir = find_main_run_directory(base_directory, jira_id)
    if main_run_dir:
        cleanup_log["phase_2_intermediate_removal"] = remove_intermediate_files(main_run_dir)
    
    # Phase 3: Consolidate separate directories
    runs_dir = os.path.join(base_directory, 'runs')
    cleanup_log["phase_3_directory_consolidation"] = consolidate_separate_directories(runs_dir, main_run_dir)
    
    # Phase 4: Clean root directory
    cleanup_log["phase_4_root_cleanup"] = cleanup_root_directory(base_directory, jira_id)
    
    # Phase 5: Final validation
    cleanup_log["phase_5_final_validation"] = validate_final_state(main_run_dir)
    
    return cleanup_log
```

### **Phase 3: Final State Validation**
```python
def validate_final_state(main_run_directory):
    """
    Validate that cleanup achieved the required final state
    """
    if not os.path.exists(main_run_directory):
        return {
            "status": "FAILED",
            "error": "Main run directory not found",
            "action": "HALT_FRAMEWORK"
        }
    
    # Check file count
    files = [f for f in os.listdir(main_run_directory) 
            if os.path.isfile(os.path.join(main_run_directory, f))]
    
    if len(files) != 3:
        return {
            "status": "FAILED",
            "error": f"Expected 3 files, found {len(files)}: {files}",
            "action": "REPEAT_CLEANUP"
        }
    
    # Check required files
    required_files = ["Test-Cases-Report.md", "Complete-Analysis-Report.md", "run-metadata.json"]
    missing_files = [f for f in required_files if f not in files]
    
    if missing_files:
        return {
            "status": "FAILED",
            "error": f"Missing required files: {missing_files}",
            "action": "REGENERATE_MISSING"
        }
    
    return {
        "status": "SUCCESS",
        "final_files": files,
        "validation": "COMPLIANT"
    }
```

## 📊 **CLEANUP MONITORING AND REPORTING**

### **Cleanup Metrics Tracking**
```json
{
  "cleanup_metrics": {
    "files_removed_per_run": "count",
    "directories_consolidated_per_run": "count",
    "root_violations_cleaned": "count", 
    "cleanup_execution_time": "seconds",
    "final_state_compliance_rate": "percentage"
  },
  "performance_targets": {
    "cleanup_success_rate": "100%",
    "final_file_count_accuracy": "100%",
    "execution_time": "<5_seconds",
    "content_preservation": "100%"
  }
}
```

### **Error Recovery Procedures**
```python
def handle_cleanup_failures(cleanup_log, main_run_directory):
    """
    Handle cleanup failures with recovery procedures
    """
    if cleanup_log["phase_5_final_validation"]["status"] != "SUCCESS":
        # Attempt recovery based on failure type
        failure_type = cleanup_log["phase_5_final_validation"]["action"]
        
        if failure_type == "REPEAT_CLEANUP":
            # Retry cleanup with more aggressive settings
            return execute_aggressive_cleanup(main_run_directory)
        
        elif failure_type == "REGENERATE_MISSING":
            # Trigger regeneration of missing final deliverables
            return trigger_deliverable_regeneration(main_run_directory)
        
        else:
            # Critical failure - halt framework
            return {
                "status": "CRITICAL_FAILURE",
                "action": "HALT_FRAMEWORK",
                "message": "Cleanup cannot be completed - manual intervention required"
            }
    
    return {"status": "NO_RECOVERY_NEEDED"}
```

## 🚨 **MANDATORY INTEGRATION REQUIREMENTS**

### **Framework Integration** (CRITICAL)
- ❌ **BLOCKED**: Framework completion without cleanup execution
- ❌ **BLOCKED**: Cleanup bypass or override capabilities
- ❌ **BLOCKED**: Manual cleanup processes
- ✅ **REQUIRED**: Automatic cleanup trigger before completion
- ✅ **REQUIRED**: Cleanup validation with blocking authority
- ✅ **MANDATORY**: Content preservation during consolidation

### **Service Integration Standards**
- **Automatic Execution**: No manual intervention required
- **Content Preservation**: Useful content consolidated into final deliverables
- **Zero Data Loss**: Important insights preserved during cleanup
- **Complete Cleanup**: Zero intermediate files remain after execution

This Cleanup Automation Service ensures that every framework execution ends with exactly 3 files in the run directory while preserving all valuable content through intelligent consolidation.