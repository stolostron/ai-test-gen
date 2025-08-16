# AI Cleanup Enforcement Service

This service enforces automatic cleanup of temporary repositories and files after analysis completion to maintain a clean working environment.

## Overview

**Purpose:** Ensure automatic and mandatory removal of temporary repositories while preserving all analysis results.

**Trigger:** Automatically executes after analysis completion or on-demand via user command.

**Scope:** Remove temp-repos/ directory and all cloned repositories while preserving runs/ directory.

## Service Implementation

### 1. Automatic Post-Analysis Cleanup

**Primary Function:** Remove temporary repositories immediately after analysis completion

```markdown
## AI Task: Execute Mandatory Post-Analysis Cleanup

**CRITICAL:** This cleanup is MANDATORY and automatically executes after ANY analysis completion.

**Cleanup Framework:**

### PHASE 1: VERIFY ANALYSIS COMPLETION
1. **Confirm Analysis Results Saved:**
   ```bash
   # Verify required analysis files exist
   if [ -d "runs" ] && [ "$(ls -A runs/ 2>/dev/null)" ]; then
     echo "✅ Analysis results preserved in runs/ directory"
   else
     echo "⚠️ WARNING: No analysis results found - cleanup may be premature"
   fi
   ```

2. **Identify Cleanup Targets:**
   ```bash
   # Check for temp-repos directory
   if [ -d "temp-repos" ]; then
     echo "🧹 Found temp-repos directory for cleanup"
     du -sh temp-repos/ 2>/dev/null || echo "Empty temp-repos"
   else
     echo "✅ No temp-repos directory found"
   fi
   ```

### PHASE 2: MANDATORY CLEANUP EXECUTION
1. **Remove Temporary Repositories:**
   ```bash
   # MANDATORY: Remove all temporary repositories
   if [ -d "temp-repos" ]; then
     echo "🧹 Removing temporary repositories..."
     rm -rf temp-repos/
     echo "✅ Temporary repositories removed"
   fi
   ```

2. **Clean Up Any Stray Git Repositories:**
   ```bash
   # Remove any stray cloned repositories (preserve main repo)
   find . -name ".git" -type d | grep -v "^\./\.git$" | while read repo; do
     if [ -n "$repo" ] && [ "$repo" != "./.git" ]; then
       echo "🧹 Removing stray repository: $repo"
       rm -rf "$(dirname "$repo")"
     fi
   done
   ```

### PHASE 3: CLEANUP VERIFICATION
1. **Verify Cleanup Success:**
   ```bash
   # Confirm temp-repos removed
   if [ ! -d "temp-repos" ]; then
     echo "✅ CLEANUP SUCCESS: temp-repos directory removed"
   else
     echo "❌ CLEANUP FAILED: temp-repos directory still exists"
   fi
   
   # Confirm analysis results preserved
   if [ -d "runs" ] && [ "$(ls -A runs/ 2>/dev/null)" ]; then
     echo "✅ VERIFICATION SUCCESS: Analysis results preserved"
     echo "📊 Analysis runs preserved: $(ls runs/ | wc -l)"
   else
     echo "⚠️ VERIFICATION WARNING: Analysis results may be missing"
   fi
   ```

2. **Report Cleanup Summary:**
   ```bash
   echo "=== CLEANUP SUMMARY ==="
   echo "Temporary repositories: $(find . -name "temp-repos" -type d | wc -l)"
   echo "Analysis runs preserved: $(ls runs/ 2>/dev/null | wc -l)"
   echo "Working directory size: $(du -sh . 2>/dev/null | cut -f1)"
   echo "Cleanup completed at: $(date)"
   ```
```

### 2. On-Demand Cleanup Commands

**Natural Language Interface:** Users can trigger cleanup using simple commands

```markdown
## AI Task: Execute On-Demand Cleanup

**User Commands:**
- "Clean up temporary repositories"
- "Remove temp-repos directory"
- "Execute cleanup"
- "Clean up cloned repositories"
- "Remove temporary files"

**Enhanced Commands:**
- "Emergency cleanup all temp files"
- "Force cleanup and verify results"
- "Clean up and report storage savings"
- "Comprehensive cleanup with verification"

**Verification Commands:**
- "Verify cleanup completed"
- "Check for temp repositories"
- "Confirm analysis results preserved"
- "Report cleanup status"
```

### 3. Emergency Cleanup Mode

**Purpose:** Force cleanup when automatic cleanup fails or when manual intervention is needed

```markdown
## AI Task: Execute Emergency Cleanup

**Emergency Cleanup Protocol:**

### PHASE 1: SAFETY BACKUP
1. **Verify Critical Analysis Data:**
   ```bash
   # Backup critical analysis if needed
   if [ -d "runs" ]; then
     echo "✅ Analysis results in runs/ directory - safe to proceed"
   else
     echo "⚠️ No runs directory found - creating safety backup"
     mkdir -p backup-analysis/
     cp -r . backup-analysis/ 2>/dev/null || true
   fi
   ```

### PHASE 2: AGGRESSIVE CLEANUP
1. **Force Remove All Temporary Content:**
   ```bash
   # Force removal of all temp content
   find . -name "temp-repos" -type d -exec rm -rf {} + 2>/dev/null || true
   find . -name "temp-*" -type d -exec rm -rf {} + 2>/dev/null || true
   find . -name "*.tmp" -exec rm -f {} + 2>/dev/null || true
   
   # Remove stray git repos (preserve main)
   find . -name ".git" -type d | grep -v "^\./\.git$" | xargs rm -rf 2>/dev/null || true
   ```

2. **Clean Up Node Modules in Temp Areas:**
   ```bash
   # Remove node_modules from cloned repos
   find . -path "*/clc-*" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
   ```

### PHASE 3: COMPREHENSIVE VERIFICATION
1. **Complete Verification Suite:**
   ```bash
   echo "=== EMERGENCY CLEANUP VERIFICATION ==="
   echo "Temp directories remaining: $(find . -name "temp-*" -type d | wc -l)"
   echo "Git repositories (excluding main): $(find . -name ".git" -type d | grep -v "^\./\.git$" | wc -l)"
   echo "Analysis runs preserved: $(ls runs/ 2>/dev/null | wc -l)"
   echo "Total directory size: $(du -sh . 2>/dev/null | cut -f1)"
   echo "Emergency cleanup completed: $(date)"
   ```
```

## Service Configuration

### Cleanup Settings
```markdown
**Default Behavior:**
- CLEANUP_ENABLED=true (always enabled)
- AUTO_CLEANUP=true (automatic after analysis)
- PRESERVE_ANALYSIS=true (always preserve runs/)
- VERIFY_CLEANUP=true (always verify success)

**Safety Features:**
- Never remove runs/ directory
- Never remove main repository (.git)
- Always verify analysis preservation
- Provide detailed cleanup logs
```

### Integration Points

```markdown
**Automatic Triggers:**
- After ai_generate_enhanced_reports() completion
- After analysis-metadata.json creation
- After jenkins-metadata.json creation
- Before analysis framework exit

**Manual Triggers:**
- User natural language commands
- Emergency cleanup requests
- Storage optimization requests
- Maintenance cleanup commands
```

## Success Metrics

### Cleanup Effectiveness
- **100% automatic cleanup execution** after analysis completion
- **Zero temp-repos persistence** after analysis
- **100% analysis preservation** in runs/ directory
- **Complete verification** of cleanup success

### Storage Optimization
- **Significant storage savings** through temp repository removal
- **Clean working environment** maintained
- **No storage bloat** from accumulated temp files
- **Efficient resource utilization**

---

**Implementation Status:** ✅ **Production Ready**  
**Service Type:** AI-Powered Cleanup Enforcement  
**Execution:** Automatic + On-Demand  
**Safety Level:** Maximum (preserves all analysis data)  
**Integration:** Complete with Analysis Framework V4.0