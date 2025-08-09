# Example Versioning System Guide

The AI Test Generation Framework includes an intelligent versioning system that automatically creates separate directories for multiple runs of the same JIRA ticket, ensuring no previous work is lost.

## 🎯 **Overview**

When you run the framework multiple times against the same JIRA ticket (e.g., ACM-22079), instead of overwriting previous results, the system automatically creates versioned directories:

```
examples/
├── ACM-22079/           # First run (Version 1)
├── ACM-22079-2/         # Second run (Version 2)  
├── ACM-22079-3/         # Third run (Version 3)
└── ACM-22079-N/         # Nth run (Version N)
```

## 🔄 **How It Works**

### **Automatic Versioning**
1. **First Run**: Creates `examples/ACM-22079/`
2. **Subsequent Runs**: Creates `examples/ACM-22079-2/`, `ACM-22079-3/`, etc.
3. **Preserved History**: All previous runs remain intact and accessible

### **Run Tracking**
Each versioned directory contains:
- **`run-metadata.json`**: Version info, timestamps, and status
- **`README.md`**: Human-readable summary of the run
- **Complete artifacts**: All generated files from that specific run

## 📋 **Usage Examples**

### **Basic Usage** (Integrated into main workflow)
```bash
# First run - creates examples/ACM-22079/
./create-test-case.sh ACM-22079 --test-plan-only

# Second run - creates examples/ACM-22079-2/  
./create-test-case.sh ACM-22079 --test-plan-only

# Third run - creates examples/ACM-22079-3/
./create-test-case.sh ACM-22079
```

### **Manual Versioning Commands**
```bash
# Set up versioned environment (standalone)
./01-setup/example-versioning.sh setup ACM-22079

# List all versions for a ticket
./01-setup/example-versioning.sh list ACM-22079

# Mark a run as completed (usually automatic)
./01-setup/example-versioning.sh complete examples/ACM-22079-3
```

## 📁 **Directory Structure**

Each versioned example contains:

```
ACM-22079-2/                           # Version 2 example
├── 01-setup/                          # Environment scripts
├── 02-analysis/                       # AI analysis results
│   ├── prompts/                      # Prompt templates used
│   └── sessions/                     # Analysis session logs
├── 02-test-planning/                 # Generated test plans
├── 03-implementation/                # Framework-specific tests
├── 04-quality/                       # Quality validation reports
├── 05-documentation/                 # Generated documentation
├── 06-reference/                     # Research materials
├── run-metadata.json                 # Run tracking info
└── README.md                         # Version-specific guide
```

## 🔍 **Run Metadata**

The `run-metadata.json` file tracks:

```json
{
  "jira_ticket": "ACM-22079",
  "version": 2,
  "created_at": "2025-01-08T13:18:19-04:00",
  "framework_version": "2.0",
  "status": "completed",
  "example_dir": "examples/ACM-22079-2",
  "completed_at": "2025-01-08T15:22:45-04:00",
  "archived_artifacts": ["02-test-planning/test-plan.md"]
}
```

## 📊 **Status Tracking**

### **Run Statuses**
- **`in_progress`**: Currently running
- **`completed`**: Successfully finished
- **`failed`**: Encountered errors
- **`incomplete`**: Interrupted or partially complete

### **Automatic Cleanup**
- **Failed runs**: Cleaned up automatically after 24 hours
- **Completed runs**: Preserved permanently
- **In-progress runs**: Protected from cleanup during active development

## 🔄 **Version Comparison**

### **Compare Versions**
```bash
# Compare test plans across versions
diff examples/ACM-22079/02-test-planning/test-plan.md \
     examples/ACM-22079-2/02-test-planning/test-plan.md

# Review version history
./01-setup/example-versioning.sh list ACM-22079
```

### **Access Specific Versions**
```bash
# Reference version 1 artifacts
cat examples/ACM-22079/02-test-planning/test-plan.md

# Copy configuration from version 2
cp examples/ACM-22079-2/team-config.yaml ./

# Review version 3 implementation
ls examples/ACM-22079-3/03-implementation/
```

## 🎯 **Best Practices**

### **When to Use Versioning**
1. **Iterating on test plans**: Refining requirements and approaches
2. **Testing different configurations**: Comparing framework settings
3. **Debugging and troubleshooting**: Preserving working states
4. **Historical reference**: Maintaining audit trails
5. **Team collaboration**: Sharing specific run results

### **Version Management**
```bash
# Create meaningful runs with different configurations
./create-test-case.sh ACM-22079 --config cypress-config.yaml
./create-test-case.sh ACM-22079 --config selenium-config.yaml
./create-test-case.sh ACM-22079 --config go-config.yaml

# Document version purposes in run metadata
echo "Testing cypress-specific implementation" > examples/ACM-22079-2/PURPOSE.md
```

## 🛠️ **Advanced Features**

### **Artifact Archiving**
The system automatically archives artifacts from the working directory:
- Preserves incomplete work when starting new runs
- Maintains workflow continuity
- Prevents data loss during iterations

### **Intelligent Cleanup**
- **Conservative approach**: Only removes explicitly failed runs
- **Time-based cleanup**: Removes runs older than 24 hours if failed
- **Status preservation**: Completed and in-progress runs are protected

### **Cross-Version Analysis**
```bash
# Generate comparison report across versions
for version in examples/ACM-22079*; do
  echo "=== $(basename $version) ==="
  if [ -f "$version/run-metadata.json" ]; then
    echo "Status: $(jq -r '.status' $version/run-metadata.json)"
    echo "Created: $(jq -r '.created_at' $version/run-metadata.json)"
    echo "Framework: $(jq -r '.framework_version' $version/run-metadata.json)"
  fi
  echo ""
done
```

## 🔗 **Integration with Main Framework**

The versioning system is fully integrated with the main workflow:

1. **Automatic Setup**: Called during `create-test-case.sh` execution
2. **Environment Variables**: Sets `CURRENT_EXAMPLE_DIR` for other scripts
3. **Completion Tracking**: Automatically marks runs as completed
4. **Status Reporting**: Shows version info in workflow summaries

## 📈 **Benefits**

### **Development Workflow**
- **No lost work**: Previous runs are always preserved
- **Easy comparison**: Compare results across iterations
- **Audit trail**: Full history of testing approaches
- **Team sharing**: Share specific version results

### **Quality Assurance**
- **Incremental improvement**: Build on previous work
- **Regression testing**: Verify improvements don't break existing functionality
- **Historical analysis**: Track framework evolution and effectiveness

---

## 🚀 **Quick Reference**

```bash
# Automatic versioning (recommended)
./create-test-case.sh ACM-22079              # Creates next version automatically

# Manual versioning
./01-setup/example-versioning.sh setup ACM-22079    # Set up new version
./01-setup/example-versioning.sh list ACM-22079     # List all versions
./01-setup/example-versioning.sh complete DIR       # Mark as completed

# Access versions
ls examples/ACM-22079*/                              # List all versions
cat examples/ACM-22079-2/run-metadata.json         # Check version info
```

**The versioning system ensures your iterative testing work is preserved and organized, enabling efficient development and collaboration while maintaining complete historical context.**