# AI Service: Intelligent Run Organizer Service

## Service Identity
**Service Name**: `tg-intelligent-run-organizer-service`  
**Purpose**: Automatic enforcement of ticket-based run organization for all framework executions  
**Integration**: Framework startup, run creation, and continuous validation  
**Priority**: Critical - Framework dependency  

## Service Overview

**Intelligent Run Organization Service** provides automatic enforcement of proper ticket-based folder structure for all framework runs, ensuring consistent organization without manual intervention.

**Structure Enforced**:
```
runs/
├── ACM-XXXXX/
│   ├── ACM-XXXXX-20250823-170246/
│   ├── ACM-XXXXX-20250824-091502/
│   └── latest -> ACM-XXXXX-20250824-091502
```

## Core Capabilities

### Automatic Organization
- **Ticket Extraction**: Intelligent detection of JIRA tickets from various input formats
- **Structure Creation**: Automatic creation of proper ticket-based folder hierarchy
- **Latest Symlinks**: Automatic creation and updating of 'latest' symlinks
- **Metadata Generation**: Comprehensive run metadata with organization details
- **Legacy Migration**: Automatic migration of existing runs to proper structure

### Framework Integration
- **Startup Validation**: Validates and organizes existing runs during framework startup
- **Run Creation**: Automatically organizes new runs with proper structure
- **Continuous Monitoring**: Ensures organization compliance throughout execution
- **Cleanup Integration**: Works with cleanup services to maintain structure integrity

### Ticket Intelligence
- **Universal Pattern Support**: Supports ACM, OCPBUGS, RHEL, JIRA, and generic patterns
- **Smart Extraction**: Multiple extraction patterns for various input formats
- **Fallback Handling**: Graceful handling when ticket extraction fails
- **Case Normalization**: Automatic normalization of ticket IDs

## Framework Integration Points

### Integration Requirements
```python
# Framework Startup Integration
from .run_organization.intelligent_run_organizer import IntelligentRunOrganizer

def framework_startup():
    organizer = IntelligentRunOrganizer()
    # Validate existing structure
    # Migrate legacy runs if needed
    # Prepare for new run creation

# Run Creation Integration  
def create_new_run(ticket_input):
    organizer = IntelligentRunOrganizer()
    run_info = organizer.organize_ticket_runs(ticket_input)
    return run_info["run_directory"]
```

### Automatic Triggers
- **Framework Startup**: Validates and organizes existing runs
- **Run Creation**: Automatically organizes new runs with proper structure
- **Agent Execution**: Ensures outputs go to correctly organized directories
- **Framework Completion**: Validates final organization compliance

## Service Configuration

### Enforcement Rules
- **Ticket-Based Organization**: All runs must be organized by ticket ID
- **Latest Symlink**: Each ticket must have 'latest' symlink to most recent run
- **Metadata Compliance**: All runs must include proper metadata files
- **Structure Validation**: Continuous validation of organization compliance

### Supported Patterns
- `ACM-\d+`: Advanced Cluster Management tickets
- `OCPBUGS-\d+`: OpenShift bug tickets  
- `RHEL-\d+`: Red Hat Enterprise Linux tickets
- `JIRA-\d+`: Generic JIRA tickets
- `[A-Z]+-\d+`: Universal pattern for any project

### Fallback Behavior
- **No Ticket Found**: Creates "GENERIC" folder with warning
- **Extraction Failed**: Prompts user for ticket ID if interactive
- **Organization Error**: Continues with warning and error logging

## Implementation Integration

### Service Dependencies
- **Run Organization Config**: `.claude/config/run-organization-config.json`
- **Intelligent Organizer**: `.claude/run-organization/intelligent_run_organizer.py`
- **Framework Integration**: Automatic integration with all framework components

### Execution Flow
1. **Framework Startup**: Validate existing structure, migrate if needed
2. **Ticket Input**: Extract ticket ID from user input or PR analysis
3. **Structure Creation**: Create proper ticket-based folder hierarchy
4. **Run Directory**: Return properly organized run directory path
5. **Latest Update**: Update latest symlink to point to new run
6. **Metadata**: Generate comprehensive run metadata
7. **Validation**: Continuous validation throughout execution

## Quality Assurance

### Validation Metrics
- **Structure Compliance**: 100% compliance with ticket-based organization
- **Latest Symlink Accuracy**: All latest symlinks point to most recent runs
- **Metadata Completeness**: All runs include complete metadata
- **Migration Success**: 100% successful migration of legacy runs

### Error Handling
- **Graceful Degradation**: Framework continues even if organization partially fails
- **Comprehensive Logging**: Detailed logging of all organization activities
- **User Communication**: Clear communication of organization actions and issues
- **Validation Reporting**: Comprehensive reporting of organization status

## Service Outputs

### Organization Results
- **Run Directory Path**: Path to properly organized run directory
- **Ticket Information**: Extracted and normalized ticket ID
- **Symlink Status**: Latest symlink creation and update status
- **Metadata Files**: Generated metadata with organization details

### Validation Reports
- **Structure Summary**: Overview of all tickets and their organization
- **Compliance Status**: Detailed compliance reporting for each ticket
- **Issue Detection**: Identification and reporting of organization issues
- **Migration Reports**: Results of any legacy run migrations

## Integration Commands

### Framework Usage
```python
# Create organized run (automatic integration)
run_dir = create_organized_run("ACM-22079", {"phase": "analysis"})

# Get latest run for ticket
latest_run = get_latest_run_directory("ACM-22079")

# Validate framework organization
is_valid = validate_framework_organization()
```

### Manual Operations
```bash
# Validate current organization
python .claude/run-organization/intelligent_run_organizer.py --validate

# Show organization summary  
python .claude/run-organization/intelligent_run_organizer.py --summary

# Test organization for ticket
python .claude/run-organization/intelligent_run_organizer.py --ticket "ACM-22079"
```

## Service Status

**Status**: ✅ Production Ready  
**Integration**: ✅ Framework Integrated  
**Validation**: ✅ Comprehensive Testing  
**Documentation**: ✅ Complete  

**Deployment**: Automatic enforcement active for all framework executions with complete backward compatibility and zero operational risk.