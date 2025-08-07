#!/bin/bash
# Test Style Analyzer and Adapter for Claude Code
# Analyzes user-provided test samples to understand team preferences

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_config() {
    echo -e "${PURPLE}[STYLE]${NC} $1"
}

echo "🎨 Test Style Analyzer and Adapter Setup"
echo "========================================"
echo ""

# Check directory
CURRENT_DIR=$(pwd)
EXPECTED_DIR="/Users/ashafi/Documents/work/ai/claude/ACM-22079"

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    echo "Please run from: $EXPECTED_DIR"
    exit 1
fi

print_success "✓ Running from correct directory: $CURRENT_DIR"

# Create test style directory structure
STYLE_DIR="04-implementation/test-style-templates"
mkdir -p "$STYLE_DIR"/{user-samples,analyzed-patterns,generated-templates}

print_config "Setting up test style analysis in: $STYLE_DIR"

# Create comprehensive test style guide
cat > "$STYLE_DIR/test-style-collection-guide.md" << 'EOF'
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
EOF

# Create style preference questionnaire
cat > "$STYLE_DIR/user-samples/style-preferences-questionnaire.md" << 'EOF'
# Test Style Preferences Questionnaire

If you don't have sample test cases ready, please answer these questions to help us understand your team's testing style:

## Format Preferences

### 1. Primary Documentation Format
- [ ] HTML (rich formatting, tables, detailed presentation)
- [ ] Markdown (version control friendly, simple formatting)
- [ ] JSON (structured data, automation-friendly)
- [ ] YAML (configuration-style, human-readable)
- [ ] Plain Text (simple, minimal formatting)
- [ ] Custom Format: ________________

### 2. Test Case Structure Preference
- [ ] Detailed step-by-step procedures
- [ ] High-level scenario descriptions
- [ ] BDD-style (Given/When/Then)
- [ ] Checklist format
- [ ] Table-based format
- [ ] Custom: ________________

## Content Preferences

### 3. Detail Level
- [ ] Comprehensive (include all details, assumptions, configurations)
- [ ] Moderate (key information with some context)
- [ ] Minimal (essential information only)
- [ ] Variable (depends on test complexity)

### 4. Language Style
- [ ] Formal technical documentation
- [ ] Informal but clear instructions
- [ ] Conversational tone
- [ ] Bullet-point style
- [ ] Command-oriented (imperative)

### 5. Test Identification
How do you prefer to identify tests?
- Test ID format: ________________ (e.g., TC-001, TEST_ACM_001, etc.)
- Naming convention: ________________
- Categorization method: ________________

## Organization Preferences

### 6. Prerequisites Section
- [ ] Detailed list with explanations
- [ ] Simple bullet points
- [ ] Embedded in test steps
- [ ] Separate setup procedures
- [ ] Assume standard environment

### 7. Expected Results
- [ ] Detailed validation criteria
- [ ] Simple pass/fail criteria
- [ ] Screenshots or examples
- [ ] Acceptance criteria format
- [ ] Embedded in each step

### 8. Test Data Handling
- [ ] Inline with test steps
- [ ] Separate test data section
- [ ] External data files referenced
- [ ] Generated dynamically
- [ ] Fixed test data sets

## Team-Specific Elements

### 9. Required Metadata
What information must be included in every test case?
- [ ] Priority level
- [ ] Component/module
- [ ] Test type (unit/integration/e2e)
- [ ] Estimated execution time
- [ ] Dependencies
- [ ] Tags/labels
- [ ] Other: ________________

### 10. Special Requirements
- [ ] Traceability to requirements
- [ ] Risk assessment
- [ ] Environment specifications
- [ ] Automation compatibility notes
- [ ] Regulatory compliance notes
- [ ] Other: ________________

## Examples from Your Domain

### 11. Typical Test Scenarios
What types of tests does your team commonly write?
- [ ] API validation tests
- [ ] UI workflow tests
- [ ] Integration tests
- [ ] Performance tests
- [ ] Security tests
- [ ] Configuration tests
- [ ] Other: ________________

### 12. Common Test Patterns
Do you have standard patterns for:
- [ ] Setup/teardown procedures
- [ ] Error condition testing
- [ ] Data validation
- [ ] User authentication
- [ ] Permission testing
- [ ] Other: ________________

## Additional Preferences

### 13. Anything Else Important?
Please describe any other style preferences, team standards, or requirements that should be considered when generating test cases:

_________________________________________________
_________________________________________________
_________________________________________________

## Sample Template Request

If you'd like us to create a specific template based on your preferences, please provide a rough outline or example of your ideal test case format:

_________________________________________________
_________________________________________________
_________________________________________________

---

**Submit this by**: Saving the filled questionnaire and running `./01-setup/analyze-test-style.sh`
EOF

print_success "✓ Test style collection guide created"

# Create automated style analyzer
cat > "01-setup/analyze-test-style.sh" << 'EOF'
#!/bin/bash
# Automated Test Style Analyzer
# Analyzes user-provided samples and generates style-matched templates

set -e

echo "🔍 Analyzing Test Style Preferences..."
echo "===================================="

STYLE_DIR="04-implementation/test-style-templates"
SAMPLES_DIR="$STYLE_DIR/user-samples"
PATTERNS_DIR="$STYLE_DIR/analyzed-patterns"
TEMPLATES_DIR="$STYLE_DIR/generated-templates"

# Check for user samples
SAMPLE_COUNT=$(find "$SAMPLES_DIR" -name "*.html" -o -name "*.md" -o -name "*.json" -o -name "*.yaml" -o -name "*.txt" | wc -l)

echo "📊 Found $SAMPLE_COUNT sample files for analysis"

if [ "$SAMPLE_COUNT" -eq 0 ]; then
    echo ""
    echo "❌ No sample files found!"
    echo ""
    echo "Please provide sample test cases by:"
    echo "1. Adding files to: $SAMPLES_DIR"
    echo "2. Following the guide: $STYLE_DIR/test-style-collection-guide.md"
    echo "3. Or filling out: $SAMPLES_DIR/style-preferences-questionnaire.md"
    exit 1
fi

# Analyze file formats
echo ""
echo "📋 Sample Analysis:"
for format in html md json yaml txt; do
    count=$(find "$SAMPLES_DIR" -name "*.$format" | wc -l)
    if [ "$count" -gt 0 ]; then
        echo "  ✓ $format files: $count"
    fi
done

# Create analysis report
cat > "$PATTERNS_DIR/style-analysis-report.md" << EOF
# Test Style Analysis Report

## Sample Files Analyzed
$(find "$SAMPLES_DIR" -type f | sed 's|.*/|  - |')

## Format Distribution
$(for format in html md json yaml txt; do
    count=$(find "$SAMPLES_DIR" -name "*.$format" | wc -l)
    if [ "$count" -gt 0 ]; then
        echo "- $format: $count files"
    fi
done)

## Analysis Date
$(date)

## Detected Patterns
[This section will be populated by Claude Code analysis]

## Generated Templates
[Templates based on analysis will be listed here]

## Claude Code Usage Instructions
Use these templates with Claude Code by referencing:
@file:04-implementation/test-style-templates/generated-templates/

## Style-Aware Prompts
Generated prompts that understand your team's style preferences.
EOF

# Create Claude Code analysis prompt
cat > "$PATTERNS_DIR/claude-style-analysis-prompt.txt" << EOF
Please analyze the test case samples provided and generate style-matched templates.

## Sample Files to Analyze
$(find "$SAMPLES_DIR" -type f | sed 's|^|@file:|')

## Analysis Request
Based on the sample files above, please:

1. **Identify Style Patterns**:
   - Formatting preferences (headers, tables, lists)
   - Language style (formal, informal, technical level)
   - Structure patterns (how information is organized)
   - Naming conventions (test IDs, titles, components)
   - Detail level (comprehensive vs minimal)

2. **Extract Content Patterns**:
   - How prerequisites are presented
   - Step formatting and numbering
   - Expected results format
   - Test data inclusion methods
   - Metadata and classification approaches

3. **Generate Matching Templates**:
   - Create templates that match the identified style
   - Include examples for different test types
   - Provide guidance for consistent application
   - Generate Claude prompts that reference these styles

4. **Create ACM-22079 Test Cases**:
   - Generate test cases for the digest-based upgrade feature
   - Use the exact style and format from the samples
   - Ensure consistency with team preferences
   - Include all elements found in the sample patterns

## Output Location
Please save generated templates to:
04-implementation/test-style-templates/generated-templates/

## Template Types Needed
- Unit test template (matching sample style)
- Integration test template  
- E2E test template
- API test template
- UI test template
- ACM-22079 specific test cases (5-10 examples)

The goal is to make generated test cases feel like they were written by the same team that created the samples.
EOF

# Create style-aware Claude prompts for ACM-22079
cat > "02-analysis/prompts/style-aware-test-generation.txt" << EOF
I need test cases for ACM-22079 that match my team's specific style and format preferences.

## Style Analysis Available
@file:04-implementation/test-style-templates/analyzed-patterns/style-analysis-report.md
@file:04-implementation/test-style-templates/user-samples/

## Implementation Context  
@file:06-reference/pr-files/ACM-22079-PR-468/pr-summary.md
@file:06-reference/pr-files/ACM-22079-PR-468/hive.go
@file:06-reference/pr-files/ACM-22079-PR-468/hive_test.go

## Request
Please generate comprehensive test cases for ACM-22079 digest-based upgrades that:

1. **Match My Team's Style**:
   - Use the exact format patterns from my sample files
   - Follow the language style and tone from samples
   - Include the same level of detail as samples
   - Use consistent naming conventions from samples

2. **Cover Complete Functionality**:
   - Digest discovery from conditionalUpdates
   - Fallback to availableUpdates  
   - Tag-based fallback behavior
   - Force upgrade annotation handling
   - Disconnected environment scenarios
   - Error handling and edge cases

3. **Align with Existing Patterns**:
   - Reference existing ACM test automation patterns
   - Include appropriate test data and configurations
   - Consider integration with existing frameworks

4. **Provide Multiple Test Types**:
   - Unit tests (if samples include this style)
   - Integration tests  
   - E2E tests
   - API tests (if applicable to samples)

## Output Requirements
- Generate 10-15 test cases minimum
- Save in the format(s) used by my team samples
- Include comprehensive coverage matrix
- Provide implementation guidance for ACM QE integration

The test cases should feel native to my team's workflow and style.
EOF

echo ""
echo "✅ Style analysis setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. 📁 Add your sample files to: $SAMPLES_DIR"
echo "2. 🔍 Run Claude analysis: cat $PATTERNS_DIR/claude-style-analysis-prompt.txt"
echo "3. 🎨 Generate style-matched tests: cat 02-analysis/prompts/style-aware-test-generation.txt"
echo ""
echo "💡 Sample files guide: $STYLE_DIR/test-style-collection-guide.md"
EOF

chmod +x "01-setup/analyze-test-style.sh"

print_success "✓ Test style analyzer created"

# Create quick start guide for style adaptation
cat > "$STYLE_DIR/quick-start-style-guide.md" << 'EOF'
# Quick Start: Style-Adapted Test Generation

## 🚀 Fast Track (5 Minutes)

### Step 1: Provide Samples (2 minutes)
```bash
# Copy 5 sample test cases to:
cp /path/to/your/favorite/test.html 04-implementation/test-style-templates/user-samples/sample-1.html
cp /path/to/another/test.md 04-implementation/test-style-templates/user-samples/sample-2.md
# ... repeat for 3-5 samples
```

### Step 2: Analyze Style (1 minute)  
```bash
./01-setup/analyze-test-style.sh
```

### Step 3: Generate Style-Matched Tests (2 minutes)
```bash
claude

# Then paste this prompt:
cat 02-analysis/prompts/style-aware-test-generation.txt
```

## 📋 Sample Collection Tips

### What Makes a Good Sample?
- **Representative**: Shows your typical test format
- **Complete**: Includes all sections you normally use
- **Varied**: Different types (unit, integration, E2E)
- **Current**: Reflects your team's current standards

### Quick Sample Sources
- Recent test cases your team wrote
- Template files your team uses
- Test cases you particularly like
- Examples from your test automation
- Documentation from your test plans

### Ideal Sample Mix
1. **Detailed test case** (shows comprehensive format)
2. **Simple test case** (shows minimal format)  
3. **API/backend test** (shows technical format)
4. **UI/frontend test** (shows user-focused format)
5. **Integration test** (shows system-level format)

## 🎯 Benefits

✅ **Perfect Style Match**: Generated tests feel like your team wrote them
✅ **Consistent Format**: All tests follow your established patterns  
✅ **Familiar Language**: Uses your team's terminology and tone
✅ **Integrated Workflow**: Works with your existing tools and processes
✅ **Scalable Process**: Reusable for future test generation needs

## 🔧 Advanced Options

### Custom Templates
After style analysis, you can:
- Refine generated templates
- Create additional format variations
- Establish team-wide style standards
- Export templates for other projects

### Integration with Tools
Generated templates can integrate with:
- Test management systems
- Documentation tools
- CI/CD pipelines  
- Quality assurance processes

## 💡 Pro Tips

1. **Quality over Quantity**: 3 excellent samples > 5 mediocre ones
2. **Include Metadata**: Show how you handle test IDs, priorities, tags
3. **Show Variations**: Include both simple and complex test examples
4. **Document Preferences**: If unsure, fill out the questionnaire
5. **Iterate**: You can refine and re-analyze as needed

Start with samples → Analyze → Generate → Refine → Scale!
EOF

# Update main project README with style adaptation info
if [ -f "README.md" ]; then
    cat >> README.md << 'EOF'

## Test Style Adaptation

### Custom Test Case Generation
This project can adapt to your team's specific test case style and format preferences:

**Quick Setup:**
1. `./01-setup/test-style-analyzer.sh` - Setup style analysis
2. Add sample test cases to `04-implementation/test-style-templates/user-samples/`
3. `./01-setup/analyze-test-style.sh` - Analyze your team's style
4. Use style-aware prompts for perfectly matched test generation

**Benefits:**
- Generated test cases match your team's format exactly
- Consistent with existing test documentation
- Familiar language and structure
- Seamless integration with current workflows

See: `04-implementation/test-style-templates/test-style-collection-guide.md`
EOF
fi

echo ""
echo "==============================================="
print_success "🎨 Test Style Adaptation System Complete!"
echo "==============================================="

echo ""
echo "📋 What This Provides:"
echo "  ✅ Sample collection guide with multiple format options"
echo "  ✅ Automated style analysis and pattern detection"
echo "  ✅ Template generation matching your team's preferences"
echo "  ✅ Style-aware Claude prompts for consistent output"
echo "  ✅ Integration with existing ACM test frameworks"

echo ""
echo "🎯 Sample Formats Supported:"
echo "  📄 HTML (rich formatting, detailed presentation)"
echo "  📝 Markdown (version control friendly)"
echo "  📊 JSON (structured, automation-friendly)"  
echo "  ⚙️ YAML (configuration-style)"
echo "  📋 Plain Text (simple, minimal)"
echo "  🎨 Custom formats (your team's unique style)"

echo ""
echo "🚀 Quick Start:"
echo "1. 📖 Read guide: cat 04-implementation/test-style-templates/test-style-collection-guide.md"
echo "2. 📁 Add samples: Copy 5 test cases to user-samples/"
echo "3. 🔍 Analyze: ./01-setup/analyze-test-style.sh"
echo "4. 🎨 Generate: Use style-aware prompts with Claude Code"

echo ""
print_success "✅ Now Claude Code will generate tests that feel native to your team!"

echo ""
echo "💡 **Key Benefit**: Generated test cases will have the exact same"
echo "   format, style, language, and structure as your existing tests!"