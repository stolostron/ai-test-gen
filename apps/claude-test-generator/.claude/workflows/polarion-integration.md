# Polarion Integration Workflow

## 🎯 Overview

This workflow integrates Polarion test case management with the Claude Test Generator framework, enabling:

1. **Learning from existing test cases** - Fetch and analyze patterns from Polarion
2. **Direct test case posting** - Post generated test cases directly to Polarion instead of just markdown

## 📋 Setup Process

> **Complete Setup Guide**: See [Polarion Setup Guide](../../docs/polarion-setup-guide.md)
> **CLI Command Reference**: See [Polarion CLI Reference](../../docs/polarion-cli-reference.md)

### 1. Install Dependencies

```bash
# Navigate to claude-test-generator directory
cd ai/ai_systems/apps/claude-test-generator

# Install Python dependencies (create requirements.txt if needed)
pip install requests python-dotenv
```

### 2. Configure Polarion Connection

```bash
# Set up configuration
python -m polarion.cli setup-config

# Set environment variables for sensitive data
export POLARION_PAT_TOKEN='your-pat-token-here'
export POLARION_URL='https://polarion.your-company.com'
export POLARION_PROJECT_ID='ACM_PROJECT'

# Test connection
python -m polarion.cli test-connection
```

### 3. Edit Configuration File

Edit `polarion_config.json`:

```json
{
  "base_url": "https://polarion.your-company.com",
  "default_project_id": "ACM_PROJECT",
  "test_case_type": "testcase",
  "timeout": 30,
  "verify_ssl": true,
  "max_test_cases_fetch": 1000,
  "learning_search_terms": [
    "ACM", "Advanced Cluster Management", "OpenShift",
    "cluster", "upgrade", "import", "export", "RBAC",
    "console", "UI", "API", "security"
  ],
  "posting_defaults": {
    "type": "testcase",
    "status": "draft",
    "severity": "normal",
    "priority": "normal"
  }
}
```

## 🔍 Learning from Existing Test Cases

### Fetch Learning Samples

```bash
# Fetch test cases for learning patterns
python -m polarion.cli fetch-learning \
    --search-terms "ACM" "upgrade" "cluster" \
    --limit 100 \
    --output learning_data.json

# Search for specific patterns
python -m polarion.cli search \
    --search-terms "RBAC" "security" \
    --limit 20 \
    --output rbac_test_cases.json
```

### Analyze Learning Data

The learning system automatically analyzes:

- **Title patterns** - Common naming conventions
- **Description patterns** - Setup and validation approaches
- **Step patterns** - Common command sequences and workflows
- **Validation approaches** - How different features are tested
- **Setup requirements** - Prerequisites and environment needs
- **Technologies** - Component and technology coverage

### Integration with AI Analysis

```python
# Example: Use learning data in AI analysis
from polarion import TestCaseFetcher, PolarionConfig

def enhance_analysis_with_learning(ticket_id: str):
    """Enhance ticket analysis with Polarion learning data"""
    
    # Fetch relevant learning samples
    config = PolarionConfig()
    fetcher = TestCaseFetcher(config)
    
    # Search for related test cases
    search_terms = extract_search_terms_from_ticket(ticket_id)
    learning_data = fetcher.fetch_learning_samples(
        search_terms=search_terms,
        limit=50
    )
    
    # Extract patterns for AI analysis
    patterns = learning_data.get('patterns', {})
    insights = learning_data.get('learning_insights', {})
    
    return {
        'validation_approaches': patterns.get('common_validation_approaches', {}),
        'setup_patterns': patterns.get('common_setup_requirements', {}),
        'naming_conventions': insights.get('naming_suggestions', []),
        'best_practices': insights.get('validation_best_practices', [])
    }
```

## 📤 Posting Test Cases to Polarion

### Enhanced Workflow Integration

Update the main analysis workflow to include Polarion posting:

```python
# Example workflow integration
def enhanced_test_generation_workflow(ticket_id: str):
    """Enhanced workflow with Polarion integration"""
    
    # 1. Fetch learning data
    learning_data = fetch_relevant_learning_data(ticket_id)
    
    # 2. Run existing AI analysis with learning enhancement
    analysis_result = run_ai_analysis_with_learning(ticket_id, learning_data)
    
    # 3. Generate test cases (existing workflow)
    test_cases_md = generate_test_cases_markdown(analysis_result)
    
    # 4. Post to Polarion
    posting_result = post_to_polarion(test_cases_md, ticket_id)
    
    # 5. Generate enhanced report
    generate_enhanced_report(analysis_result, posting_result)
    
    return {
        'markdown_files': test_cases_md,
        'polarion_ids': posting_result.get('successful', []),
        'learning_insights': learning_data.get('learning_insights', {})
    }
```

### Direct Posting from Generated Markdown

```bash
# Post test cases from generated markdown
python -m polarion.cli post-test-cases \
    runs/ACM-12345/run-001-20250114-1530/Test-Cases.md \
    --project-id ACM_PROJECT \
    --status "draft" \
    --priority "normal" \
    --report posting_report.md

# Batch posting with metadata
python -m polarion.cli post-test-cases \
    Test-Cases.md \
    --metadata-file metadata.json \
    --report detailed_report.md
```

### Metadata File Example

Create `metadata.json` for enhanced test case information:

```json
{
  "custom_fields": {
    "jira_ticket": "ACM-12345",
    "component": "cluster_management",
    "test_type": "integration",
    "automation_status": "not_automated",
    "technologies": "ACM,OpenShift"
  },
  "status": "draft",
  "priority": "normal",
  "severity": "normal"
}
```

## 🔧 Enhanced Claude Analysis with Polarion

### Learning-Enhanced AI Prompts

```markdown
**Enhanced AI Analysis Prompt with Polarion Learning:**

You are analyzing JIRA ticket {TICKET_ID} with enhanced learning from existing Polarion test cases.

**Learning Data Available:**
- {learning_insights.validation_best_practices} are the most common validation approaches
- {learning_insights.setup_recommendations} are typical setup requirements
- {patterns.common_technologies} are covered technologies
- {patterns.naming_conventions} show common naming patterns

**Generate test cases that:**
1. Follow proven validation patterns from existing test cases
2. Use established naming conventions
3. Include common setup requirements
4. Apply validated testing approaches for this technology stack

**Output Requirements:**
- Generate both markdown (for backup) and Polarion-ready format
- Include metadata for automatic posting
- Reference learning patterns in test case design
```

### Integration Points in Existing Framework

1. **Pre-Analysis Learning** - Fetch relevant patterns before JIRA analysis
2. **AI-Enhanced Generation** - Use learning data to improve test case quality
3. **Dual Output Generation** - Create both markdown and Polarion-ready formats
4. **Automatic Posting** - Post to Polarion with metadata
5. **Learning Loop** - Use posted test cases to improve future generations

## 📊 Enhanced Reporting

### Comprehensive Analysis Report

The enhanced workflow generates reports that include:

```markdown
# Enhanced Analysis Report with Polarion Integration

## 🎯 Learning-Enhanced Analysis
**Learning Sources:** {learning_data.total_test_cases} existing test cases analyzed
**Pattern Confidence:** {pattern_confidence}%
**Validation Approaches:** {top_validation_methods}

## 📤 Polarion Integration Results
**Posted Test Cases:** {successful_posts}
**Polarion URLs:** {polarion_links}
**Posting Success Rate:** {success_rate}%

## 🔍 Learning Insights Applied
- **Naming Convention:** Based on {naming_pattern_source}
- **Validation Approach:** Following {validation_pattern}
- **Setup Requirements:** Aligned with {setup_pattern}

## 📋 Generated Test Cases
[Existing test case content]

## 🔗 Polarion References
- **Project:** {project_id}
- **Test Case IDs:** {posted_test_case_ids}
- **Direct Links:** {polarion_test_case_urls}
```

## 🔄 Workflow Commands

### Complete Enhanced Workflow

```bash
# 1. Fetch learning data for ticket context
python -m polarion.cli fetch-learning \
    --search-terms $(extract_terms_from_ticket ACM-12345) \
    --output learning_$(date +%Y%m%d).json

# 2. Run enhanced analysis (existing framework with learning)
analyze_ticket_enhanced ACM-12345 --learning-data learning_$(date +%Y%m%d).json

# 3. Post generated test cases
python -m polarion.cli post-test-cases \
    runs/ACM-12345/latest/Test-Cases.md \
    --report runs/ACM-12345/latest/Polarion-Report.md

# 4. Update learning database with new patterns
update_learning_patterns runs/ACM-12345/latest/
```

### Automated Integration Workflow

Create `enhanced_analyze_with_polarion.sh` using the CLI commands documented in [Polarion CLI Reference](../../docs/polarion-cli-reference.md):

```bash
#!/bin/bash
# enhanced_analyze_with_polarion.sh

TICKET_ID=$1
PROJECT_ID=${2:-ACM_PROJECT}

echo "🔍 Enhanced analysis with Polarion integration for $TICKET_ID"

# 1. Fetch learning data
echo "📚 Fetching learning data..."
python -m polarion.cli fetch-learning \
    --search-terms "ACM" "cluster" "upgrade" \
    --limit 50 \
    --output "learning_${TICKET_ID}.json"

# 2. Run enhanced analysis
echo "🤖 Running AI analysis with learning enhancement..."
analyze_ticket_enhanced $TICKET_ID \
    --learning-data "learning_${TICKET_ID}.json" \
    --polarion-integration

# 3. Post to Polarion
echo "📤 Posting test cases to Polarion..."
python -m polarion.cli post-test-cases \
    "runs/$TICKET_ID/latest/Test-Cases.md" \
    --project-id $PROJECT_ID \
    --metadata-file "runs/$TICKET_ID/latest/metadata.json" \
    --report "runs/$TICKET_ID/latest/Polarion-Report.md"

echo "✅ Enhanced analysis complete with Polarion integration"
```

## 🎯 Benefits of Integration

1. **Improved Test Quality** - Learn from proven patterns in existing test cases
2. **Consistency** - Follow established conventions and approaches
3. **Efficiency** - Direct posting eliminates manual copy-paste workflow
4. **Traceability** - Maintain links between JIRA tickets and Polarion test cases
5. **Continuous Learning** - Each generation improves based on existing knowledge
6. **Collaboration** - Test cases immediately available to team in Polarion

This integration transforms the framework from a markdown-only generator to a complete test case management solution that learns from existing knowledge and integrates seamlessly with enterprise workflows.
