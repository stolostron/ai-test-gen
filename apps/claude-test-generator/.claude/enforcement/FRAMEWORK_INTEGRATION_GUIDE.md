# Framework Write Enforcement Integration Guide

## MANDATORY INTEGRATION

All framework execution MUST use validated Write operations.

### Step 1: Import Enforcement
```python
# Add at the start of framework execution
import sys
sys.path.append('.claude/enforcement')
from mandatory_write_enforcement import Write
```

### Step 2: Replace Write Tool Usage
```python
# OLD (bypasses validation):
# Write(file_path, content)

# NEW (enforced validation):
Write(file_path, content)  # Now automatically validated
```

### Step 3: Finalize Enforcement
```python
# At end of framework execution
from mandatory_write_enforcement import finalize_write_enforcement
finalize_write_enforcement(run_directory)
```

## Integration Status

✅ **ACTIVE**: All Write operations automatically validated
🛡️  **ENFORCEMENT**: Format violations automatically blocked
📋 **AUDIT**: Complete enforcement audit trail generated

## Validation Rules

- **Test Cases**: Must use Description/Setup/Table format
- **Dual Methods**: Must include UI Method and CLI Method columns  
- **YAML Integration**: Must be within table, not separate sections
- **HTML Prevention**: All HTML tags automatically blocked

## Compliance Guarantee

100% enforcement - no Write operations can bypass validation when
this module is properly integrated into framework execution.
