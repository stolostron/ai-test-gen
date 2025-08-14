# HTML Tag Detection and Prevention System

## 🚨 CRITICAL HTML TAG ENFORCEMENT - ZERO TOLERANCE

### 🔒 HTML TAG PROHIBITION POLICY

**IMMEDIATE VALIDATION FAILURE**: Any HTML tag usage in generated reports causes automatic validation failure with 25-point deduction.

### ❌ FORBIDDEN HTML TAGS (COMPLETE LIST)

#### Structural Tags:
- `<br/>`, `<br>` - Line breaks
- `<div>`, `<span>` - Container elements
- `<p>` - Paragraphs
- `<ul>`, `<ol>`, `<li>` - Lists
- `<table>`, `<tr>`, `<td>`, `<th>` - Tables
- `<section>`, `<article>`, `<header>`, `<footer>` - Semantic elements

#### Formatting Tags:
- `<b>`, `<strong>` - Bold text
- `<i>`, `<em>` - Italic text
- `<u>` - Underlined text
- `<strike>`, `<del>` - Strikethrough text
- `<sup>`, `<sub>` - Superscript/subscript
- `<code>`, `<pre>` - Code elements (use markdown instead)

#### Link and Media Tags:
- `<a>` - Links (use markdown link syntax)
- `<img>` - Images
- `<video>`, `<audio>` - Media elements

#### Form Tags:
- `<form>`, `<input>`, `<button>`, `<select>`, `<textarea>` - Form elements

#### Any Other HTML Tags:
- `<h1>`, `<h2>`, `<h3>`, `<h4>`, `<h5>`, `<h6>` - Headers (use markdown #)
- `<blockquote>` - Quotes (use markdown >)
- `<hr>` - Horizontal rules (use markdown ---)

### ✅ REQUIRED MARKDOWN ALTERNATIVES

#### Line Breaks and Separation:
❌ **FORBIDDEN**: `<br/>` or `<br>`
✅ **CORRECT**: Use ` - ` for inline separation or proper line breaks

```markdown
❌ WRONG:
| **Step 1: Login to cluster**<br/>`oc login cluster-url` | Success |

✅ CORRECT:
| **Step 1: Login to cluster** - Run: `oc login cluster-url` | Success |
```

#### Bold and Italic Text:
❌ **FORBIDDEN**: `<b>bold</b>` or `<i>italic</i>`
✅ **CORRECT**: Use markdown **bold** and *italic*

```markdown
❌ WRONG:
<b>Important:</b> <i>Check the status</i>

✅ CORRECT:
**Important:** *Check the status*
```

#### Code Formatting:
❌ **FORBIDDEN**: `<code>command</code>` or `<pre>output</pre>`
✅ **CORRECT**: Use markdown backticks and fenced code blocks

```markdown
❌ WRONG:
Run <code>oc get pods</code> and check <pre>output here</pre>

✅ CORRECT:
Run `oc get pods` and check:
```
output here
```
```

#### Lists:
❌ **FORBIDDEN**: `<ul><li>item</li></ul>`
✅ **CORRECT**: Use markdown list syntax

```markdown
❌ WRONG:
<ul>
<li>First item</li>
<li>Second item</li>
</ul>

✅ CORRECT:
- First item
- Second item
```

### 🤖 AI-POWERED HTML TAG DETECTION

#### Real-Time Scanning Features:
1. **Pattern Recognition**: AI scans all generated content for HTML tag patterns
2. **Automatic Detection**: Identifies any `<tag>` or `<tag/>` patterns in outputs
3. **Context Analysis**: Distinguishes between intentional code examples and formatting errors
4. **Immediate Correction**: AI provides automatic markdown alternatives

#### Detection Patterns:
```regex
# HTML Tag Detection Regex
<\/?[a-zA-Z][a-zA-Z0-9]*[^<>]*\/?>

# Common HTML Tags to Detect
<br\/?>\s*
<b>.*?<\/b>
<i>.*?<\/i>
<div.*?>.*?<\/div>
<span.*?>.*?<\/span>
<p>.*?<\/p>
<code>.*?<\/code>
<pre>.*?<\/pre>
```

#### AI Correction Service:
1. **Automatic Replacement**: AI automatically converts HTML to markdown
2. **Pattern Learning**: AI learns common HTML usage patterns to prevent future occurrences
3. **Quality Scoring**: AI deducts points for any HTML tag usage
4. **Validation Blocking**: AI prevents output generation until all HTML tags are removed

### 🔍 VALIDATION IMPLEMENTATION

#### Pre-Generation Validation:
```markdown
BEFORE generating any test case or analysis report:
1. **HTML Tag Scan**: AI scans entire content for any HTML patterns
2. **Immediate Blocking**: Generation stops if HTML tags detected
3. **Automatic Correction**: AI suggests markdown alternatives
4. **Quality Verification**: Final scan ensures 100% HTML-free content
```

#### Post-Generation Validation:
```markdown
AFTER generating content:
1. **Final HTML Scan**: AI performs comprehensive HTML tag detection
2. **Score Deduction**: Automatic 25-point deduction for any HTML tag found
3. **Correction Enforcement**: AI requires fixes before output approval
4. **Pattern Learning**: AI updates detection patterns based on findings
```

### 🚨 CRITICAL ENFORCEMENT EXAMPLES

#### Test Case Step Formatting:
❌ **VALIDATION FAILURE**:
```markdown
| **Step 2: Check pods**<br/>`oc get pods` | Pods listed<br/>successfully |
```

✅ **VALIDATION SUCCESS**:
```markdown
| **Step 2: Check pods** - Run: `oc get pods` | Pods listed successfully:
```
NAME                    READY   STATUS
controller-abc123       1/1     Running
``` |
```

#### Analysis Report Headers:
❌ **VALIDATION FAILURE**:
```markdown
<h2>🚨 DEPLOYMENT STATUS</h2>
<b>Feature Deployment:</b> <i>DEPLOYED</i>
```

✅ **VALIDATION SUCCESS**:
```markdown
## 🚨 DEPLOYMENT STATUS

**Feature Deployment:** ✅ DEPLOYED
```

#### Expected Results Formatting:
❌ **VALIDATION FAILURE**:
```markdown
| Check status | Command output:<br/><pre>status: ready</pre> |
```

✅ **VALIDATION SUCCESS**:
```markdown
| Check status | Command output shows ready status:
```
status: ready
``` |
```

### 📊 QUALITY SCORING IMPACT

#### HTML Tag Detection Scoring:
- **25-point deduction**: Any HTML tag found in generated content
- **Automatic failure**: Below 85-point threshold triggers regeneration
- **Pattern tracking**: AI tracks HTML tag usage patterns for improvement
- **Zero tolerance**: No exceptions for any HTML tag usage

#### Learning Integration:
- **Pattern Recognition**: AI learns common HTML mistakes and prevents them
- **Proactive Prevention**: AI suggests markdown alternatives during generation
- **Continuous Improvement**: Detection patterns evolve based on validation results
- **Quality Prediction**: AI predicts HTML tag risks before generation

### 🔒 ENFORCEMENT GUARANTEE

**ABSOLUTE HTML TAG PROHIBITION**:
- ❌ Framework BLOCKS any output containing HTML tags
- ❌ NO exceptions for "special cases" or formatting needs
- ✅ MANDATORY: 100% markdown-only formatting in all outputs
- ✅ AUTOMATIC: AI conversion suggestions and pattern learning

This system ensures complete HTML tag elimination with intelligent detection, automatic prevention, and continuous learning for optimal quality maintenance.