# Test Style Adaptation System - Complete Workflow

## 🎯 **What This System Solves**

You mentioned that different teams have different testing styles and preferences, and you'd like Claude Code to ask users for samples and then match their exact format and style. **This system does exactly that!**

## 🎨 **How It Works**

### **Step 1: User Provides Style Samples**
The system asks for **5 sample test cases** in any format:
- ✅ **HTML** (for rich formatting)
- ✅ **Markdown** (for documentation)  
- ✅ **JSON** (for structured data)
- ✅ **YAML** (for configuration-style)
- ✅ **Custom formats** (whatever your team uses)

### **Step 2: Automated Style Analysis**
Claude Code analyzes the samples to understand:
- **Format patterns** (tables, headers, sections)
- **Language style** (formal, informal, technical level)  
- **Content structure** (how information is organized)
- **Team-specific elements** (unique requirements, conventions)

### **Step 3: Style-Matched Test Generation**
Generated test cases **perfectly match** your team's style:
- Same format and visual appearance
- Same language tone and terminology
- Same level of detail and organization
- Same metadata and structure patterns

## 📁 **Current Demo Setup**

I've created a demonstration with sample test cases:

### **Sample 1: HTML Unit Test** 
```
04-implementation/test-style-templates/user-samples/sample-1-unit-test.html
```
- Rich HTML formatting with CSS styling
- Color-coded priorities and status indicators  
- Detailed tables for metadata and validation
- Comprehensive structure with emojis and visual elements

### **Sample 2: Markdown Integration Test**
```
04-implementation/test-style-templates/user-samples/sample-2-integration-test.md
```
- Professional Markdown documentation style
- Clear section organization with headers
- Table-based metadata and validation criteria
- Technical detail with code examples

## 🚀 **Complete Workflow**

### **For Your Team to Use:**

#### **1. Provide Your Style Samples (5 minutes)**
```bash
# Add your team's actual test cases to:
cp /path/to/your/test1.html 04-implementation/test-style-templates/user-samples/
cp /path/to/your/test2.md 04-implementation/test-style-templates/user-samples/
cp /path/to/your/test3.json 04-implementation/test-style-templates/user-samples/
# ... add 5 total samples
```

#### **2. Analyze Style Patterns (1 minute)**
```bash
./01-setup/analyze-test-style.sh
```

#### **3. Generate Style-Matched Tests (2 minutes)**
```bash
claude

# Then use this prompt:
cat 02-analysis/prompts/style-aware-test-generation.txt
```

## 🎯 **What You Get**

### **Before (Generic Tests)**
```
Test Case: TC-001
Verify cluster upgrade functionality
Steps:
1. Create cluster
2. Initiate upgrade  
3. Verify completion
Expected: Upgrade succeeds
```

### **After (Your Team's Style)**
**If your team uses HTML format:**
```html
<h1 class="test-id">Test Case ID: ACM-CLC-001</h1>
<table>
    <tr><td>Priority</td><td class="priority-high">High</td></tr>
    <tr><td>Component</td><td>ClusterCurator - Upgrade Module</td></tr>
</table>
<h2>🧪 Test Data</h2>
[Exact format matching your samples]
```

**If your team uses Markdown format:**
```markdown
# Test Case: ACM-CLC-INT-002 - ClusterCurator Digest-Based Upgrade

## 📝 Test Metadata
| Field | Value |
|-------|-------|
| **Priority** | **HIGH** |

### Phase 1: Setup and Validation
[Exact structure matching your samples]
```

## 🔧 **Supported Style Elements**

### **Format Adaptations**
- ✅ **HTML**: Rich formatting, CSS styling, color coding
- ✅ **Markdown**: Professional documentation, tables, code blocks
- ✅ **JSON**: Structured data, automation-friendly
- ✅ **YAML**: Configuration-style, hierarchical
- ✅ **Plain Text**: Simple, minimal formatting
- ✅ **Custom**: Whatever format your team prefers

### **Content Adaptations**
- ✅ **Metadata**: Test IDs, priorities, components (your format)
- ✅ **Prerequisites**: Simple lists vs detailed explanations
- ✅ **Test Steps**: Numbered, bulleted, or phase-based
- ✅ **Expected Results**: Brief vs comprehensive validation
- ✅ **Error Handling**: Team-specific error scenarios
- ✅ **Cleanup**: Your team's cleanup and teardown patterns

### **Language Adaptations**
- ✅ **Tone**: Formal technical vs informal conversational
- ✅ **Detail Level**: Comprehensive vs minimal descriptions
- ✅ **Terminology**: Your team's specific terms and conventions
- ✅ **Structure**: How your team organizes information

## 📊 **Benefits Demonstrated**

### **Style Consistency**
- Generated tests **look identical** to your existing tests
- Same visual formatting and organization
- Same language style and terminology
- Same level of technical detail

### **Team Integration**  
- Tests fit naturally into your existing documentation
- No training needed - familiar format for team members
- Seamless integration with your current tools and processes
- Maintains your established quality standards

### **Comprehensive Coverage**
- All ACM-22079 functionality covered
- Multiple test types in your preferred formats
- Complete integration with ACM test automation
- Aligned with your team's testing methodology

## 🔄 **Continuous Improvement**

### **Style Refinement**
- Analyze additional samples to improve accuracy
- Refine templates based on team feedback
- Update style patterns as team preferences evolve
- Create team-wide style standards

### **Template Reuse**
- Generated templates work for future test creation
- Style patterns applicable to other features
- Consistent approach across all team projects
- Scalable process for growing teams

## 💡 **Key Advantages**

✅ **Perfect Style Match**: Tests feel native to your team's workflow  
✅ **Zero Learning Curve**: Familiar format requires no additional training  
✅ **Comprehensive Coverage**: All technical requirements included  
✅ **Quality Consistency**: Maintains your team's documentation standards  
✅ **Scalable Process**: Reusable for any future test generation needs  

## 🎯 **Next Steps**

1. **Replace demo samples** with your team's actual test cases
2. **Run the analysis** to understand your team's patterns  
3. **Generate ACM-22079 tests** in your exact style
4. **Refine and iterate** based on team feedback
5. **Scale the process** for other features and projects

**Result**: Claude Code becomes an extension of your team, generating test cases that are indistinguishable from your team's own work while providing comprehensive technical coverage!

---

## 📁 **File Locations**

- **Style Guide**: `04-implementation/test-style-templates/test-style-collection-guide.md`
- **Sample Directory**: `04-implementation/test-style-templates/user-samples/`
- **Analysis Script**: `./01-setup/analyze-test-style.sh`
- **Style-Aware Prompt**: `02-analysis/prompts/style-aware-test-generation.txt`
- **Demo Samples**: Already provided in user-samples directory

This system transforms Claude Code from a generic test generator into a tool that perfectly matches your team's unique style and preferences!