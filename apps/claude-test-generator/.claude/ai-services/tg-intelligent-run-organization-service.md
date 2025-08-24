# Intelligent Run Organization Service

**Service ID**: `tg_intelligent_run_organization_service`  
**Service Type**: Run management and intelligent folder organization  
**Authority Level**: Directory creation and organization with cleanup authority  
**Integration Points**: Run generation, metadata management, framework completion

## 🎯 Mission Statement

Provide intelligent folder organization for multiple test runs of the same JIRA ticket, creating ticket-based grouping with chronological run organization while maintaining backward compatibility with existing single-run structure.

## 🏗️ Core Capabilities

### **Intelligent Folder Structure**
```
runs/
├── ACM-22079/                          # Ticket-based grouping (multiple runs)
│   ├── ACM-22079-20250823-114500/      # Individual run directories
│   │   ├── ACM-22079-Test-Cases.md
│   │   ├── ACM-22079-Complete-Analysis.md
│   │   └── run-metadata.json
│   ├── ACM-22079-20250823-122400/      # Second run
│   │   ├── ACM-22079-Test-Cases.md
│   │   ├── ACM-22079-Complete-Analysis.md
│   │   └── run-metadata.json
│   └── latest-run-metadata.json        # Quick access to latest run info
├── ACM-15207-20250822-030156/          # Single run - maintains current format
│   ├── ACM-15207-Test-Cases.md
│   ├── ACM-15207-Complete-Analysis.md
│   └── run-metadata.json
└── ACM-13644-20250822-004533/          # Single run - maintains current format
    ├── ACM-13644-Test-Cases.md
    ├── ACM-13644-Complete-Analysis.md
    └── run-metadata.json
```

### **Organization Logic**
1. **First Run**: Creates standard format `ACM-XXXXX-YYYYMMDD-HHMMSS/`
2. **Subsequent Runs**: 
   - Detects existing ticket runs
   - Creates ticket-based parent directory `ACM-XXXXX/`
   - Moves existing run into parent directory
   - Creates new run directory within parent
   - Updates latest-run-metadata.json for quick access

### **Migration Strategy**
- **Backward Compatibility**: Existing single runs remain unchanged
- **Progressive Enhancement**: Only reorganizes when second run detected
- **Preservation**: All existing data and structure maintained
- **Intelligent Detection**: Scans for ticket patterns and multiple runs

## 🔧 Implementation Architecture

### **Core Service Functions**

#### **1. Run Detection and Analysis**
```python
def detect_existing_runs(jira_ticket: str) -> List[str]:
    """
    Scan runs directory for existing instances of same ticket
    Returns list of existing run directories for the ticket
    """
    
def analyze_run_organization(jira_ticket: str) -> dict:
    """
    Analyze current organization state for ticket
    Returns: {
        'existing_runs': [],
        'needs_reorganization': bool,
        'parent_exists': bool,
        'recommended_action': str
    }
    """
```

#### **2. Intelligent Organization**
```python
def organize_ticket_runs(jira_ticket: str, new_run_id: str) -> str:
    """
    Intelligently organize runs for ticket
    - Creates ticket parent directory if needed
    - Migrates existing runs if necessary  
    - Returns final run directory path
    """

def migrate_existing_runs(jira_ticket: str, existing_runs: List[str]) -> bool:
    """
    Safely migrate existing runs into ticket-based organization
    Preserves all data and updates metadata references
    """
```

#### **3. Metadata Management**
```python
def create_latest_run_metadata(jira_ticket: str, run_metadata: dict) -> None:
    """
    Creates/updates latest-run-metadata.json in ticket parent directory
    Provides quick access to most recent run information
    """

def update_run_references(old_path: str, new_path: str) -> None:
    """
    Updates any internal references when migrating runs
    Ensures framework consistency after reorganization
    """
```

### **Service Integration Points**

#### **Framework Phase Integration**
- **Phase 0-Pre**: Environment selection with intelligent path determination
- **Phase 4**: Test generation with organized output directory
- **Phase 5**: Cleanup and finalization with organization validation

#### **Run Management Integration**
```yaml
run_organization_workflow:
  initialization:
    - detect_existing_runs()
    - analyze_run_organization()
    - determine_target_directory()
  
  execution:
    - create_organized_structure()
    - migrate_existing_runs_if_needed()
    - generate_run_content()
  
  finalization:
    - create_latest_run_metadata()
    - validate_organization_compliance()
    - cleanup_temporary_structures()
```

## 📊 Organization Examples

### **Example 1: First Run**
```
Input: ACM-22079 (no existing runs)
Output: runs/ACM-22079-20250823-114500/
Action: Standard single-run format
```

### **Example 2: Second Run (Triggers Reorganization)**
```
Input: ACM-22079 (existing: ACM-22079-20250823-114500/)
Actions:
1. Create: runs/ACM-22079/
2. Move: ACM-22079-20250823-114500/ → ACM-22079/ACM-22079-20250823-114500/
3. Create: ACM-22079/ACM-22079-20250823-122400/
4. Generate: ACM-22079/latest-run-metadata.json
```

### **Example 3: Third Run (Uses Existing Organization)**
```
Input: ACM-22079 (existing: ACM-22079/ directory with 2 runs)
Actions:
1. Create: ACM-22079/ACM-22079-20250823-130000/
2. Update: ACM-22079/latest-run-metadata.json
```

## 🔒 Quality Assurance

### **Data Preservation Guarantees**
- **Zero Data Loss**: All existing run data preserved during migration
- **Structure Integrity**: All file contents and metadata maintained
- **Reference Consistency**: Internal links and references updated appropriately
- **Rollback Capability**: Migration can be reversed if needed

### **Validation Requirements**
- **Organization Compliance**: Verify ticket-based structure correctness
- **Metadata Consistency**: Ensure all metadata files updated properly
- **Path Resolution**: Validate all file paths resolve correctly
- **Framework Integration**: Confirm framework services locate runs properly

### **Error Handling**
- **Migration Failures**: Rollback to original structure on error
- **Directory Conflicts**: Handle existing directory name conflicts
- **Permission Issues**: Graceful handling of filesystem permission errors
- **Partial Migrations**: Recovery from interrupted reorganization

## 🚀 Performance Considerations

### **Efficiency Optimizations**
- **Lazy Migration**: Only reorganize when second run detected
- **Minimal File Operations**: Efficient directory moves vs copies
- **Metadata Caching**: Cache organization analysis for performance
- **Batch Operations**: Group filesystem operations for efficiency

### **Resource Management**
- **Disk Usage**: Minimal overhead for organization structure
- **Memory Usage**: Efficient processing of large run collections
- **CPU Impact**: Fast pattern detection and organization logic
- **I/O Optimization**: Minimize filesystem operations

## 📋 Configuration Options

### **Service Configuration**
```json
{
  "intelligent_run_organization": {
    "enabled": true,
    "auto_migrate_threshold": 2,
    "preserve_single_runs": true,
    "latest_metadata_enabled": true,
    "backup_before_migration": true,
    "organization_validation": true
  }
}
```

### **Customization Options**
- **Migration Threshold**: Number of runs before reorganization
- **Naming Patterns**: Customizable directory naming schemes
- **Metadata Options**: Configurable latest-run metadata content
- **Validation Levels**: Different levels of organization validation
- **Backup Strategy**: Optional backup before major reorganizations

## 🎯 Integration Requirements

### **Framework Services Integration**
- **Run Management Service**: Enhanced with intelligent organization
- **Metadata Generation Service**: Updated for ticket-based structure
- **Cleanup Automation Service**: Extended for organized structure validation
- **Directory Validation Service**: Enhanced for ticket-based compliance

### **Observability Integration**
- **Real-time Monitoring**: Track organization operations
- **Business Intelligence**: Report on run organization efficiency
- **Performance Metrics**: Monitor migration and organization speed
- **Quality Tracking**: Validate organization compliance rates

This service provides intelligent, efficient, and safe run organization that scales naturally from single runs to multiple runs per ticket while maintaining complete backward compatibility and data preservation.