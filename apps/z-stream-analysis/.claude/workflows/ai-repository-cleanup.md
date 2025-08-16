# AI Repository Cleanup Workflow

This workflow ensures proper cleanup of temporary repositories and analysis artifacts after completing real repository analysis.

## Overview

**Purpose:** Automatically clean up temporary repositories and files created during analysis to maintain a clean working environment and prevent storage bloat.

**Key Features:**
- **Automatic Cleanup**: Remove cloned repositories after analysis completion
- **Selective Preservation**: Keep analysis results while removing source repositories
- **Storage Management**: Prevent temp directory growth and storage issues
- **Security**: Remove potentially sensitive repository content after analysis

## Cleanup Framework

### 1. Post-Analysis Cleanup
**Purpose:** Remove temporary repositories after successful analysis completion
**Trigger:** Automatically after analysis report generation
**Scope:** Remove cloned repositories while preserving analysis results

```markdown
## AI Task: Execute Post-Analysis Cleanup

Clean up temporary repositories after completing analysis:

**Cleanup Requirements:**

### PHASE 1: ANALYSIS COMPLETION VERIFICATION
1. **Verify Analysis Complete:**
   - Confirm Detailed-Analysis.md has been generated
   - Verify analysis-metadata.json exists
   - Check jenkins-metadata.json is present
   - Ensure all required analysis artifacts are saved

2. **Identify Cleanup Targets:**
   - Locate temp-repos/ directory
   - Identify cloned repository directories
   - Verify no critical analysis data is in temp directories

### PHASE 2: SELECTIVE CLEANUP
1. **Preserve Analysis Results:**
   - Keep all files in runs/ directory
   - Preserve analysis-results/ if exists
   - Maintain all .md, .json analysis files

2. **Remove Temporary Repositories:**
   ```bash
   # Remove cloned repositories
   rm -rf temp-repos/[repository-name]
   
   # Clean up any git artifacts
   find temp-repos/ -name ".git" -type d -exec rm -rf {} + 2>/dev/null || true
   
   # Remove empty temp-repos directory if no analysis results
   if [ -z "$(ls -A temp-repos/ 2>/dev/null)" ]; then
     rmdir temp-repos/ 2>/dev/null || true
   fi
   ```

### PHASE 3: CLEANUP VERIFICATION
1. **Verify Cleanup Success:**
   - Confirm repository directories removed
   - Verify analysis results preserved
   - Check storage space reclaimed

2. **Log Cleanup Actions:**
   - Record what was cleaned up
   - Note any cleanup failures
   - Document preserved artifacts

**AI-Powered Cleanup Commands:**
Natural language commands that trigger intelligent cleanup:

```markdown
# Primary cleanup commands
"Clean up temporary repositories after analysis"
"Remove cloned repositories while preserving analysis results"
"Execute post-analysis cleanup"

# Advanced cleanup commands  
"Perform comprehensive repository cleanup"
"Clean temp directories and preserve analysis data"
"Emergency cleanup of all temporary files"

# Verification commands
"Verify cleanup completed successfully"
"Check for remaining temporary repositories"
"Confirm analysis results are preserved"
```

**AI Cleanup Process:**
The AI service will intelligently:
1. Identify temp-repos directories and cloned repositories
2. Verify analysis results are safely preserved in runs/ directory
3. Remove only temporary repository files while keeping analysis data
4. Provide cleanup confirmation and storage savings report
5. Log all cleanup actions for audit purposes
```

### 2. Scheduled Cleanup
**Purpose:** Regular cleanup of old temporary files and directories
**Trigger:** Can be run periodically or on-demand
**Scope:** Clean up forgotten temp files and old analysis artifacts

```markdown
## AI Task: Execute Scheduled Cleanup

Perform comprehensive cleanup of temporary files and old artifacts:

**Scheduled Cleanup Requirements:**

### PHASE 1: COMPREHENSIVE SCAN
1. **Identify Cleanup Targets:**
   - Find any remaining temp-repos/ directories
   - Locate old git repositories in workspace
   - Identify oversized analysis directories

2. **AI-Powered Age-Based Cleanup:**
   Natural language commands for scheduled maintenance:
   
   ```markdown
   "Clean up old temporary repositories older than 7 days"
   "Remove stray git directories from previous analysis"
   "Clean empty temp directories and optimize storage"
   "Perform weekly maintenance cleanup"
   ```

### PHASE 2: ANALYSIS ARCHIVE MANAGEMENT
1. **Archive Old Analysis:**
   - Compress analysis runs older than 30 days
   - Remove analysis runs older than 90 days (configurable)
   - Preserve metadata for historical tracking

2. **AI-Powered Storage Optimization:**
   Natural language commands for archive management:
   
   ```markdown
   "Archive old analysis runs older than 30 days"
   "Compress and optimize storage for historical analysis"
   "Remove analysis archives older than 90 days"
   "Optimize storage while preserving critical analysis data"
   ```

**AI Cleanup Verification:**
Natural language commands for verification:

```markdown
"Verify cleanup completed successfully"
"Report storage savings from cleanup"
"Check for any remaining temporary repositories"
"Confirm all analysis results are preserved"
"Generate cleanup summary report"
```
```

### 3. Emergency Cleanup
**Purpose:** Force cleanup when automatic cleanup fails
**Trigger:** Manual execution when temp directories are detected
**Scope:** Aggressive cleanup with safety checks

```markdown
## AI Task: Execute Emergency Cleanup

Force cleanup of all temporary repositories and files:

**Emergency Cleanup Requirements:**

### PHASE 1: SAFETY VERIFICATION
1. **Verify Analysis Preservation:**
   - Confirm all runs/ directories are intact
   - Check critical analysis files exist
   - Backup important analysis data if needed

2. **Identify All Temp Content:**
   ```bash
   # Find all temp-repos directories
   find . -name "temp-repos" -type d
   
   # Find all git repositories (excluding main repo)
   find . -name ".git" -type d | grep -v "^\./\.git$"
   
   # Check disk usage
   du -sh temp-repos/ 2>/dev/null || echo "No temp-repos found"
   ```

### PHASE 2: AGGRESSIVE CLEANUP
1. **Force Remove All Temp Repositories:**
   ```bash
   # Remove all temp-repos directories
   find . -name "temp-repos" -type d -exec rm -rf {} + 2>/dev/null || true
   
   # Remove stray git repositories (NOT the main repo)
   find . -name ".git" -type d | grep -v "^\./\.git$" | xargs rm -rf 2>/dev/null || true
   
   # Clean up any node_modules in temp areas
   find . -path "*/temp-*" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
   ```

2. **Verify Complete Cleanup:**
   ```bash
   # Confirm no temp repositories remain
   if [ -z "$(find . -name "temp-repos" -type d 2>/dev/null)" ]; then
     echo "✅ All temp-repos directories removed"
   else
     echo "⚠️  Some temp-repos directories remain"
     find . -name "temp-repos" -type d
   fi
   
   # Confirm analysis data preserved
   if [ -d "runs" ] && [ "$(ls -A runs/ 2>/dev/null)" ]; then
     echo "✅ Analysis results preserved"
     ls -la runs/
   else
     echo "⚠️  Analysis results may be missing"
   fi
   ```

**Final Verification:**
```bash
# Report final status
echo "=== CLEANUP SUMMARY ==="
echo "Temp repositories: $(find . -name "temp-repos" -type d | wc -l)"
echo "Analysis runs preserved: $(ls runs/ 2>/dev/null | wc -l)"
echo "Storage freed: $(du -sh . 2>/dev/null)"
```
```

## Integration with Analysis Framework

### Enhanced Workflow with Automatic Cleanup
```markdown
# Complete AI Analysis Workflow with Cleanup (V3.1)
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

### Cleanup Trigger Points
```markdown
**Automatic Cleanup Triggers:**
- After successful analysis report generation
- After metadata files creation
- Before analysis framework exit
- On analysis failure (cleanup partial work)

**Manual Cleanup Commands:**
- "Clean up temporary repositories"
- "Execute post-analysis cleanup"
- "Remove cloned repositories"
- "Emergency cleanup all temp files"
```

## Cleanup Configuration

### Cleanup Settings
```markdown
**Default Cleanup Behavior:**
- Remove cloned repositories after analysis completion
- Preserve all analysis results and metadata
- Keep analysis-results/ directory if it contains findings
- Log all cleanup actions for audit trail

**Configurable Options:**
- CLEANUP_ENABLED=true (default)
- PRESERVE_REPOS=false (default)
- CLEANUP_AGE_DAYS=7 (for scheduled cleanup)
- ARCHIVE_AGE_DAYS=30 (for analysis archiving)
```

### Safety Measures
```markdown
**Cleanup Safety Features:**
- Never remove main repository (.git in root)
- Always preserve runs/ directory and contents
- Verify analysis completion before cleanup
- Provide cleanup logs and verification
- Allow manual override of cleanup behavior
```

---

## AI Cleanup Service Implementation

### Natural Language Cleanup Commands

Users can trigger cleanup using simple natural language:

```markdown
# Primary cleanup commands
"Clean up temporary repositories after analysis"
"Remove cloned repositories while preserving analysis results" 
"Execute post-analysis cleanup"

# Advanced cleanup
"Perform comprehensive repository cleanup"
"Emergency cleanup of all temporary files"
"Optimize storage and clean temp directories"

# Verification
"Verify cleanup completed successfully"
"Check for remaining temporary repositories"
"Generate cleanup summary report"
```

### AI Service Benefits

**Advantages over Shell Scripts:**
- **Intelligent Decision Making**: AI can analyze what's safe to remove vs preserve
- **Context Awareness**: Understands analysis state and completion status
- **Error Handling**: Robust error recovery and fallback procedures
- **User-Friendly**: Natural language interface instead of complex commands
- **Cross-Platform**: Works regardless of operating system or shell
- **Safe Operations**: Built-in safety checks and verification
- **Audit Trail**: Comprehensive logging of all cleanup actions

**Implementation Status:** Enhanced AI service framework deployed  
**Focus:** Intelligent cleanup through natural language interface  
**Benefits:** Safe automation, user-friendly operation, robust error handling