# Polarion Integration for Claude Test Generator

🎯 **Complete Polarion integration for fetching existing test cases (learning) and posting generated test cases directly to Polarion.**

## 🚀 Quick Start

### 1. Setup

Follow the comprehensive setup guide: **[Polarion Setup Guide](../docs/polarion-setup-guide.md)**

Quick setup commands:
```bash
# Install dependencies
pip3 install -r requirements.txt

# Set environment variables
export POLARION_PAT_TOKEN='your-pat-token-here'
export POLARION_URL='https://polarion.your-company.com'
export POLARION_PROJECT_ID='ACM_PROJECT'

# Create and test configuration
python3 -m polarion.cli setup-config
python3 -m polarion.cli test-connection
```

### 2. Fetch Learning Data

```bash
# Fetch test cases for learning patterns
python3 -m polarion.cli fetch-learning \
    --search-terms "ACM" "upgrade" "cluster" \
    --limit 100 \
    --output learning_data.json
```

### 3. Post Test Cases

```bash
# Post generated test cases to Polarion
python3 -m polarion.cli post-test-cases \
    Test-Cases.md \
    --project-id ACM_PROJECT \
    --status "draft" \
    --report posting_report.md
```

## 📚 Components

### 🔧 Core Modules

| Module | Purpose | Key Features |
|--------|---------|--------------|
| **`api_client.py`** | Polarion REST API client | Authentication, CRUD operations |
| **`config.py`** | Configuration management | Environment variables, defaults |
| **`test_case_fetcher.py`** | Learning from existing test cases | Pattern analysis, insights |
| **`test_case_poster.py`** | Posting new test cases | Markdown parsing, batch posting |
| **`cli.py`** | Command-line interface | Complete CLI operations |

### 🎯 Key Features

#### Learning Capabilities
- **Pattern Recognition** - Analyzes existing test cases for common patterns
- **Validation Approaches** - Identifies proven testing methods
- **Setup Requirements** - Learns standard prerequisites
- **Naming Conventions** - Extracts consistent naming patterns
- **Technology Mapping** - Maps features to technology stacks

#### Posting Capabilities
- **Markdown Parsing** - Converts generated markdown to Polarion format
- **Batch Operations** - Post multiple test cases efficiently
- **Metadata Enhancement** - Automatically adds relevant metadata
- **Error Handling** - Comprehensive error reporting
- **Report Generation** - Detailed posting reports

## 🔧 Configuration

### Environment Variables

```bash
# Required
export POLARION_PAT_TOKEN='your-personal-access-token'
export POLARION_URL='https://polarion.your-company.com'
export POLARION_PROJECT_ID='YOUR_PROJECT_ID'

# Optional
export POLARION_USERNAME='username'           # Alternative to PAT
export POLARION_PASSWORD='password'           # Alternative to PAT
export POLARION_TEST_CASE_TYPE='testcase'    # Default test case type
export POLARION_TIMEOUT='30'                 # API timeout in seconds
export POLARION_VERIFY_SSL='true'            # SSL verification
```

### Configuration File

Create `polarion_config.json`:

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
    "cluster", "upgrade", "import", "export", "RBAC"
  ],
  "posting_defaults": {
    "type": "testcase",
    "status": "draft",
    "severity": "normal",
    "priority": "normal"
  }
}
```

## 📋 CLI Commands

### Setup and Testing

```bash
# Create sample configuration
python3 -m polarion.cli setup-config

# Test API connection
python3 -m polarion.cli test-connection

# List available projects
python3 -m polarion.cli list-projects --limit 10
```

### Learning Operations

```bash
# Fetch learning samples with specific search terms
python3 -m polarion.cli fetch-learning \
    --search-terms "ACM" "cluster" "upgrade" \
    --limit 50 \
    --output learning_data.json

# Search for specific test cases
python3 -m polarion.cli search \
    --search-terms "RBAC" "security" \
    --limit 20 \
    --output rbac_cases.json
```

### Posting Operations

```bash
# Post test cases from markdown
python3 -m polarion.cli post-test-cases \
    Test-Cases.md \
    --project-id ACM_PROJECT \
    --status "draft" \
    --priority "normal" \
    --report posting_report.md

# Post with custom metadata
python3 -m polarion.cli post-test-cases \
    Test-Cases.md \
    --metadata-file metadata.json \
    --report detailed_report.md
```

## 🔍 Learning Data Analysis

### Fetched Learning Data Structure

```json
{
  "project_id": "ACM_PROJECT",
  "search_terms": ["ACM", "cluster"],
  "fetch_timestamp": "2025-01-14T10:30:00",
  "test_cases": [
    {
      "id": "ACM-TC-001",
      "title": "Cluster Import Validation",
      "description": "Validates cluster import process",
      "test_steps": [...],
      "analysis": {
        "title_patterns": ["import_export_testing"],
        "validation_approaches": ["resource_verification"],
        "setup_requirements": ["cluster_access"],
        "technologies": ["ACM"]
      }
    }
  ],
  "patterns": {
    "common_validation_approaches": {
      "resource_verification": 25,
      "log_verification": 18,
      "api_verification": 12
    },
    "common_setup_requirements": {
      "cluster_access": 40,
      "namespace_creation": 22,
      "resource_configuration": 15
    }
  },
  "learning_insights": {
    "validation_best_practices": ["resource_verification", "log_verification"],
    "setup_recommendations": ["cluster_access", "namespace_creation"],
    "naming_suggestions": ["cluster", "import", "validation"]
  }
}
```

### Using Learning Data

```python
from polarion import TestCaseFetcher, PolarionConfig

# Fetch learning data
config = PolarionConfig()
fetcher = TestCaseFetcher(config)

learning_data = fetcher.fetch_learning_samples(
    search_terms=['ACM', 'upgrade'],
    limit=100
)

# Extract insights
insights = learning_data.get('learning_insights', {})
best_practices = insights.get('validation_best_practices', [])
setup_recommendations = insights.get('setup_recommendations', [])

print(f"Best practices: {best_practices}")
print(f"Setup recommendations: {setup_recommendations}")
```

## 📤 Posting Test Cases

### Markdown Format Requirements

Your generated markdown must follow this structure:

```markdown
## Test Case 1: Cluster Import Validation

**Description:** Validates the complete cluster import workflow

**Setup:** Access to ACM hub cluster and cluster ready for import

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster-url.com:6443 -u admin -p password --insecure-skip-tls-verify` | Login successful with access confirmed |
| **Step 2: Create import configuration** - Apply import YAML: `oc apply -f import.yaml` | Import configuration created successfully |
```

### Metadata Enhancement

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

### Programmatic Posting

```python
from polarion import TestCasePoster, PolarionConfig

# Initialize poster
config = PolarionConfig()
poster = TestCasePoster(config)

# Post from markdown file
created_ids = poster.post_test_cases_from_markdown(
    markdown_file="Test-Cases.md",
    project_id="ACM_PROJECT",
    metadata={
        "status": "draft",
        "priority": "normal"
    }
)

print(f"Created test cases: {created_ids}")
```

## 🔗 Integration with Claude Test Generator

### Enhanced Workflow

1. **Pre-Analysis Learning** - Fetch relevant patterns before generating test cases
2. **AI-Enhanced Generation** - Use learning data to improve test case quality
3. **Dual Output** - Generate both markdown and Polarion-ready formats
4. **Direct Posting** - Post to Polarion with metadata
5. **Learning Loop** - Use posted test cases for future improvements

### Workflow Commands

```bash
# Complete enhanced workflow
./enhanced_analyze_with_polarion.sh ACM-12345 ACM_PROJECT

# Manual step-by-step
python3 -m polarion.cli fetch-learning --search-terms "upgrade" --output learning.json
analyze_ticket_enhanced ACM-12345 --learning-data learning.json
python3 -m polarion.cli post-test-cases runs/ACM-12345/latest/Test-Cases.md
```

## 🔧 Error Handling

### Common Issues and Solutions

#### Authentication Issues
```bash
# PAT token invalid
export POLARION_PAT_TOKEN='new-valid-token'
python3 -m polarion.cli test-connection

# SSL certificate issues
export POLARION_VERIFY_SSL='false'
```

#### Connection Issues
```bash
# Check URL format
export POLARION_URL='https://polarion.company.com'  # Include https://

# Test basic connectivity
curl -k $POLARION_URL/polarion/rest/v1/projects
```

#### Posting Issues
```bash
# Check project permissions
python3 -m polarion.cli list-projects

# Validate markdown format
python3 -m polarion.cli post-test-cases Test-Cases.md --dry-run
```

## 📊 Reporting

### Learning Report Example

```markdown
# Learning Analysis Report

## 📊 Summary
- **Test Cases Analyzed:** 85
- **Average Steps per Test:** 6.2
- **Success Rate:** 100%

## 🔍 Patterns Discovered
- **Top Validation Approaches:** resource_verification (25), log_verification (18)
- **Common Setup Requirements:** cluster_access (40), namespace_creation (22)
- **Technologies Covered:** ACM (35), OpenShift (28), Kubernetes (15)

## 💡 Insights
- Most tests follow 3-phase pattern: setup, execution, validation
- Resource verification is the most reliable validation method
- Cluster access is a universal requirement
```

### Posting Report Example

```markdown
# Polarion Posting Report

## Summary
- **Total Attempted:** 3
- **Successful:** 3
- **Failed:** 0
- **Success Rate:** 100.0%

## Successfully Created Test Cases
- **ACM-TC-123:** Cluster Import Validation
- **ACM-TC-124:** Upgrade Process Verification
- **ACM-TC-125:** RBAC Configuration Testing
```

## 🎯 Benefits

✅ **Improved Quality** - Learn from proven patterns  
✅ **Consistency** - Follow established conventions  
✅ **Efficiency** - Direct posting eliminates manual work  
✅ **Traceability** - Maintain JIRA ↔ Polarion links  
✅ **Learning** - Continuous improvement from existing knowledge  
✅ **Collaboration** - Immediate team access in Polarion  

## 📚 Additional Resources

- **[Workflow Integration Guide](.claude/workflows/polarion-integration.md)** - Complete integration documentation
- **[Usage Example](examples/polarion_usage_example.py)** - Python example script
- **[Setup Guide](../docs/polarion-setup-guide.md)** - Complete setup documentation
- **[CLI Reference](../docs/polarion-cli-reference.md)** - Comprehensive CLI command reference

For more details, see the complete workflow documentation in `.claude/workflows/polarion-integration.md`.
