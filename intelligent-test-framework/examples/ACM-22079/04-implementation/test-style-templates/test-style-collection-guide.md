# Test Style Collection Guide

## What We Need from You

To generate test cases that match your team's style and preferences, please provide **5 sample test cases** in the formats you typically use.

## Recommended Sample Formats

### 1. **HTML Format** (Recommended for detailed test cases)
Save as `.html` files with rich formatting, tables, and sections.

**Example Structure:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Test Case: Feature Name</title>
</head>
<body>
    <h1>Test Case ID: TC-001</h1>
    <table>
        <tr><td>Test Title</td><td>Verify cluster upgrade functionality</td></tr>
        <tr><td>Priority</td><td>High</td></tr>
        <tr><td>Component</td><td>ClusterCurator</td></tr>
    </table>
    
    <h2>Prerequisites</h2>
    <ul>
        <li>Hub cluster deployed</li>
        <li>Managed cluster available</li>
    </ul>
    
    <h2>Test Steps</h2>
    <ol>
        <li>Navigate to cluster management page</li>
        <li>Select target cluster</li>
        <li>Click upgrade option</li>
    </ol>
    
    <h2>Expected Results</h2>
    <p>Upgrade completes successfully</p>
</body>
</html>
```

### 2. **Markdown Format** (Great for version control)
Save as `.md` files with clear structure and formatting.

**Example Structure:**
```markdown
# Test Case: TC-001 - Cluster Upgrade Verification

## Test Information
- **ID**: TC-001
- **Title**: Verify cluster upgrade functionality  
- **Priority**: High
- **Component**: ClusterCurator
- **Type**: Integration

## Prerequisites
- Hub cluster deployed and accessible
- Managed cluster in ready state
- Appropriate permissions configured

## Test Steps
1. **Setup**: Navigate to cluster management interface
2. **Action**: Select target cluster for upgrade
3. **Execute**: Initiate upgrade process
4. **Verify**: Monitor upgrade progress and completion

## Expected Results
- ✅ Upgrade initiates without errors
- ✅ Progress indicators show correctly  
- ✅ Upgrade completes within expected timeframe
- ✅ Cluster shows updated version

## Test Data
- Source Version: 4.5.8
- Target Version: 4.5.10
- Cluster Type: AWS
```

### 3. **JSON Format** (Structured for automation)
Save as `.json` files for structured test data.

**Example Structure:**
```json
{
  "testCase": {
    "id": "TC-001",
    "title": "Cluster Upgrade Verification",
    "metadata": {
      "priority": "High",
      "component": "ClusterCurator",
      "type": "Integration",
      "tags": ["upgrade", "cluster", "automation"]
    },
    "prerequisites": [
      "Hub cluster deployed and accessible",
      "Managed cluster in ready state",
      "Appropriate permissions configured"
    ],
    "steps": [
      {
        "step": 1,
        "action": "Navigate to cluster management interface",
        "expected": "Interface loads successfully"
      },
      {
        "step": 2,
        "action": "Select target cluster for upgrade",
        "expected": "Cluster details displayed"
      }
    ],
    "validation": {
      "success_criteria": [
        "Upgrade completes successfully",
        "No error messages displayed",
        "Cluster shows updated version"
      ]
    }
  }
}
```

### 4. **YAML Format** (Configuration-friendly)
Save as `.yaml` files for structured, readable test definitions.

**Example Structure:**
```yaml
testCase:
  id: TC-001
  title: "Cluster Upgrade Verification"
  metadata:
    priority: High
    component: ClusterCurator
    type: Integration
    tags:
      - upgrade
      - cluster
      - automation
  
  prerequisites:
    - "Hub cluster deployed and accessible"
    - "Managed cluster in ready state"
    - "Appropriate permissions configured"
  
  steps:
    - step: 1
      action: "Navigate to cluster management interface"
      expected: "Interface loads successfully"
    - step: 2
      action: "Select target cluster for upgrade"
      expected: "Cluster details displayed"
  
  validation:
    success_criteria:
      - "Upgrade completes successfully"
      - "No error messages displayed"
      - "Cluster shows updated version"
```

### 5. **Custom Team Format**
If your team uses a specific template or tool, provide examples in that format.

## What to Include in Your Samples

### Test Case Variety
Please provide samples that cover:
1. **Unit Test**: Component-level testing
2. **Integration Test**: Component interaction testing  
3. **E2E Test**: Complete workflow testing
4. **API Test**: Backend/service testing
5. **UI Test**: Frontend/interface testing

### Content Elements to Include
Make sure your samples show:
- **Test identification** (IDs, titles, metadata)
- **Prerequisites and setup** requirements
- **Step-by-step procedures** 
- **Expected results** and validation criteria
- **Test data** and configurations
- **Error handling** scenarios
- **Cleanup** procedures

### Style Elements to Capture
Include examples that demonstrate:
- **Formatting preferences** (tables, lists, sections)
- **Language style** (formal, informal, technical level)
- **Detail level** (brief vs comprehensive)
- **Organization patterns** (how you structure information)
- **Naming conventions** (how you name tests and components)

## How to Provide Your Samples

### Option 1: Direct File Placement
Save your 5 sample files in:
```
04-implementation/test-style-templates/user-samples/
├── sample-1-unit-test.html
├── sample-2-integration-test.md
├── sample-3-e2e-test.json
├── sample-4-api-test.yaml
└── sample-5-ui-test.html
```

### Option 2: Reference Existing Tests
If you have existing test repositories, provide paths:
```
# Add to user-samples/existing-test-references.txt
/Users/ashafi/Documents/work/automation/clc-ui/cypress/integration/my-favorite-test.spec.js
/path/to/your/test/repository/excellent-test-example.md
```

### Option 3: Describe Your Preferences
If you don't have samples ready, describe your preferences in:
```
04-implementation/test-style-templates/user-samples/style-preferences.md
```

## Analysis Benefits

Once you provide samples, the system will:
✅ **Analyze formatting patterns** and replicate your style
✅ **Extract language preferences** and match your tone
✅ **Understand detail level** and provide appropriate depth
✅ **Learn organization patterns** and structure tests accordingly
✅ **Adopt naming conventions** that fit your team standards
✅ **Generate templates** that feel native to your workflow

## Next Steps

1. **Provide samples** using any of the methods above
2. **Run analysis**: `./01-setup/analyze-test-style.sh`
3. **Review templates**: Generated templates will appear in `generated-templates/`
4. **Use with Claude**: Enhanced prompts will reference your style preferences

This ensures all generated test cases feel like they were written by your team!
