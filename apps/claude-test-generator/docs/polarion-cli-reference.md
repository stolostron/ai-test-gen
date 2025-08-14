# Polarion CLI Reference Guide

## 🎯 Complete Command Line Interface Reference

This guide provides comprehensive documentation for all Polarion CLI commands, replacing the need to execute scripts to understand functionality.

## 📋 Table of Contents
- [Quick Reference](#quick-reference)
- [Setup Commands](#setup-commands)
- [Learning Commands](#learning-commands)
- [Posting Commands](#posting-commands)
- [Utility Commands](#utility-commands)
- [Advanced Usage](#advanced-usage)
- [Error Handling](#error-handling)

## 🚀 Quick Reference

### Most Common Commands
```bash
# Setup and configuration
python3 -m polarion.cli setup-config
python3 -m polarion.cli setup-credentials
python3 -m polarion.cli test-connection

# Credential management
python3 -m polarion.cli credential-status
python3 -m polarion.cli remove-credentials

# Learning from existing test cases
python3 -m polarion.cli fetch-learning --search-terms "ACM" "upgrade" --limit 50

# Posting new test cases
python3 -m polarion.cli post-test-cases Test-Cases.md --project-id ACM_PROJECT

# Search existing test cases
python3 -m polarion.cli search --search-terms "cluster" "import" --limit 10
```

### Command Structure
```bash
python3 -m polarion.cli [COMMAND] [OPTIONS] [ARGUMENTS]
```

## ⚙️ Setup Commands

### `setup-config` - Initialize Configuration

**Purpose:** Creates sample configuration file with default settings

**Usage:**
```bash
python3 -m polarion.cli setup-config
```

**What it does:**
1. Creates `polarion_config.json` with default settings
2. Provides next steps for configuration
3. Shows required environment variables

**Output Example:**
```
✅ Created sample configuration: polarion_config.json

📋 Next steps:
1. Edit the configuration file with your Polarion details
2. Set environment variables for sensitive data:
   export POLARION_PAT_TOKEN='your-token-here'
   export POLARION_URL='https://polarion.your-company.com'
   export POLARION_PROJECT_ID='YOUR_PROJECT'
3. Test connection with: python -m polarion.cli test-connection
```

**No Options Available**

---

## 🔐 Credential Management Commands

### `setup-credentials` - Interactive Credential Setup

**Purpose:** Securely store Polarion credentials locally within the framework

**Usage:**
```bash
python3 -m polarion.cli setup-credentials
```

**What it does:**
1. Prompts for Polarion URL, project ID, and PAT token
2. Stores credentials in `.polarion/credentials.json` with secure permissions
3. Adds credential directory to `.gitignore` automatically
4. Tests connection to verify credentials work

**Interactive Prompts:**
```
🔐 Polarion Credential Setup
========================================
Polarion URL (e.g., https://polarion.company.com): [enter URL]
Default Project ID: [enter project]
Username (optional, press Enter to skip): [enter username]

🔑 Personal Access Token:
   Generate one in Polarion: User Menu → Access Tokens
PAT Token (input hidden): [enter token]

⚙️ Additional Configuration (optional):
API Timeout in seconds (default: 30): [enter or skip]
Verify SSL certificates? (y/N): [y/n or skip]
```

**Success Output:**
```
✅ Credentials stored successfully!
📁 Location: /path/to/.polarion/credentials.json
🔒 File secured with owner-only permissions

🧪 Test connection with: python3 -m polarion.cli test-connection
```

**Security Features:**
- Files stored with 600 permissions (owner read/write only)
- Directory secured with 700 permissions (owner access only)
- Automatically excluded from git via `.gitignore`
- PAT tokens stored locally, never in environment or config files

**No Options Available**

---

### `credential-status` - Show Credential Storage Status

**Purpose:** Display detailed information about stored credentials and security status

**Usage:**
```bash
python3 -m polarion.cli credential-status
```

**Output Example:**
```
📊 Polarion Credential Status
==============================
Credentials Stored: ✅ Yes (secure)
📁 Credentials File: /path/to/.polarion/credentials.json
📁 Config File: /path/to/.polarion/config.local.json
Directory Secure: 🔒 Yes
Url: https://polarion.company.com
Project Id: ACM_PROJECT
Username: user@company.com
Has Pat Token: ✅ Yes (secure)
Version: 1.0
```

**Status Indicators:**
- ✅ **Yes (secure)** - Credentials properly stored and secured
- ❌ **No** - Credentials not found or not set
- ⚠️ **No (check permissions)** - Directory permissions need fixing
- 🔒 **Yes** - Security permissions correctly configured

**No Options Available**

---

### `remove-credentials` - Remove Stored Credentials

**Purpose:** Safely remove all stored credentials and local configuration

**Usage:**
```bash
python3 -m polarion.cli remove-credentials [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--force` | Skip confirmation prompt | False |

**Examples:**
```bash
# Remove with confirmation prompt
python3 -m polarion.cli remove-credentials

# Force removal without confirmation
python3 -m polarion.cli remove-credentials --force
```

**Interactive Confirmation:**
```
⚠️ Remove stored credentials? This cannot be undone. (yes/no): yes
✅ Stored credentials removed
✅ Local configuration removed
```

**What it removes:**
- `.polarion/credentials.json` - Stored credentials
- `.polarion/config.local.json` - Local configuration overrides
- Leaves global configuration file intact

---

### `test-connection` - Validate API Connection

**Purpose:** Tests Polarion API connectivity and project access

**Usage:**
```bash
python3 -m polarion.cli test-connection [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--config`, `-c` | Configuration file path | `polarion_config.json` |

**What it does:**
1. Validates configuration file
2. Tests API authentication
3. Verifies project access
4. Reports connection status

**Success Output:**
```
✅ Configuration validation passed
✅ Polarion API connection successful
✅ Project access confirmed: Advanced Cluster Management
```

**Failure Output:**
```
❌ Configuration validation failed:
   - POLARION_PAT_TOKEN not set
   - Invalid project ID
❌ Polarion API connection failed
```

## 🔍 Learning Commands

### `fetch-learning` - Fetch Test Cases for Learning

**Purpose:** Downloads existing test cases to learn patterns and best practices

**Usage:**
```bash
python3 -m polarion.cli fetch-learning [OPTIONS]
```

**Options:**
| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--project-id`, `-p` | Project ID to search | From config | `ACM_PROJECT` |
| `--search-terms`, `-s` | Search terms (space-separated) | None | `"ACM" "upgrade"` |
| `--search-file` | File with search terms (one per line) | None | `search_terms.txt` |
| `--limit`, `-l` | Maximum test cases to fetch | 100 | `50` |
| `--output`, `-o` | Output file for learning data | Auto-generated | `learning_data.json` |

**Examples:**
```bash
# Basic learning fetch
python3 -m polarion.cli fetch-learning \
    --search-terms "ACM" "cluster" \
    --limit 50

# Using search terms from file
echo -e "ACM\nupgrade\ncluster\nRBAC" > search_terms.txt
python3 -m polarion.cli fetch-learning \
    --search-file search_terms.txt \
    --output acm_learning.json

# Project-specific learning
python3 -m polarion.cli fetch-learning \
    --project-id CUSTOM_PROJECT \
    --search-terms "security" "authentication" \
    --limit 25
```

**Output Example:**
```
🔍 Fetching learning samples from project: ACM_PROJECT
📋 Search terms: ACM, cluster, upgrade
✅ Learning data saved to: polarion_learning_2025-01-14T15-30-00.json

📊 Summary:
   - Test cases analyzed: 50
   - Average steps per test: 6.2
   - Top validation approaches: ['resource_verification', 'log_verification', 'api_verification']
   - Technologies covered: ['ACM', 'OpenShift', 'Kubernetes']
```

**Learning Data Structure:**
```json
{
  "project_id": "ACM_PROJECT",
  "search_terms": ["ACM", "cluster"],
  "fetch_timestamp": "2025-01-14T15:30:00",
  "statistics": {
    "total_count": 50,
    "avg_step_count": 6.2,
    "success_rate": 100.0
  },
  "patterns": {
    "common_validation_approaches": {
      "resource_verification": 25,
      "log_verification": 18,
      "api_verification": 12
    }
  },
  "learning_insights": {
    "validation_best_practices": ["resource_verification", "log_verification"],
    "setup_recommendations": ["cluster_access", "namespace_creation"]
  }
}
```

---

### `search` - Search Specific Test Cases

**Purpose:** Search for specific test cases and optionally save detailed results

**Usage:**
```bash
python3 -m polarion.cli search [OPTIONS]
```

**Options:**
| Option | Description | Required | Example |
|--------|-------------|----------|---------|
| `--project-id`, `-p` | Project ID to search | No | `ACM_PROJECT` |
| `--search-terms`, `-s` | Search terms | **Yes** | `"RBAC" "security"` |
| `--limit`, `-l` | Maximum results to show | No (default: 10) | `20` |
| `--output`, `-o` | Save detailed results to file | No | `rbac_cases.json` |

**Examples:**
```bash
# Basic search
python3 -m polarion.cli search \
    --search-terms "RBAC" "security" \
    --limit 5

# Search with detailed output
python3 -m polarion.cli search \
    --search-terms "cluster" "import" "export" \
    --limit 15 \
    --output cluster_management_cases.json

# Project-specific search
python3 -m polarion.cli search \
    --project-id SECURITY_PROJECT \
    --search-terms "authentication" "authorization" \
    --output security_test_cases.json
```

**Output Example:**
```
🔍 Searching test cases in project: ACM_PROJECT
📋 Search terms: RBAC, security
✅ Found 12 test cases:
   - ACM-TC-001: RBAC Policy Validation
   - ACM-TC-002: Security Context Testing
   - ACM-TC-003: User Permission Verification
   - ACM-TC-004: Role Binding Configuration
   - ACM-TC-005: Cluster Role Management
   ... and 7 more
📁 Detailed results saved to: rbac_cases.json
```

## 📤 Posting Commands

### `post-test-cases` - Post Test Cases to Polarion

**Purpose:** Uploads test cases from markdown files to Polarion

**Usage:**
```bash
python3 -m polarion.cli post-test-cases MARKDOWN_FILE [OPTIONS]
```

**Arguments:**
| Argument | Description | Required | Example |
|----------|-------------|----------|---------|
| `MARKDOWN_FILE` | Path to markdown file with test cases | **Yes** | `Test-Cases.md` |

**Options:**
| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--project-id`, `-p` | Project ID for posting | From config | `ACM_PROJECT` |
| `--metadata-file` | JSON file with additional metadata | None | `metadata.json` |
| `--status` | Test case status | From config | `draft` |
| `--priority` | Test case priority | From config | `normal` |
| `--severity` | Test case severity | From config | `normal` |
| `--report`, `-r` | Generate posting report to file | None | `posting_report.md` |

**Examples:**
```bash
# Basic posting
python3 -m polarion.cli post-test-cases Test-Cases.md

# Posting with custom status
python3 -m polarion.cli post-test-cases \
    Test-Cases.md \
    --project-id ACM_PROJECT \
    --status "approved" \
    --priority "high" \
    --report posting_report.md

# Posting with metadata file
python3 -m polarion.cli post-test-cases \
    Test-Cases.md \
    --metadata-file custom_metadata.json \
    --report detailed_posting_report.md
```

**Markdown Format Requirements:**
```markdown
## Test Case 1: Cluster Import Validation

**Description:** Validates the complete cluster import workflow

**Setup:** Access to ACM hub cluster and cluster ready for import

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into ACM hub** - Access hub cluster: `oc login https://api.cluster.com:6443 -u admin -p password` | Login successful with access confirmed |
| **Step 2: Create import configuration** - Apply YAML: `oc apply -f import.yaml` | Import configuration created successfully |
```

**Metadata File Example:**
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

**Success Output:**
```
📤 Posting test cases to project: ACM_PROJECT
📁 Source file: Test-Cases.md
✅ Successfully posted 3 test cases:
   - ACM-TC-123
   - ACM-TC-124  
   - ACM-TC-125
📋 Report saved to: posting_report.md
```

**Posting Report Example:**
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

## Links
- [ACM-TC-123](https://polarion.company.com/polarion/#/project/ACM_PROJECT/workitem?id=ACM-TC-123)
- [ACM-TC-124](https://polarion.company.com/polarion/#/project/ACM_PROJECT/workitem?id=ACM-TC-124)
- [ACM-TC-125](https://polarion.company.com/polarion/#/project/ACM_PROJECT/workitem?id=ACM-TC-125)
```

## 🔧 Utility Commands

### `list-projects` - List Available Projects

**Purpose:** Shows accessible Polarion projects

**Usage:**
```bash
python3 -m polarion.cli list-projects [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--limit`, `-l` | Maximum projects to show | 20 |

**Example:**
```bash
python3 -m polarion.cli list-projects --limit 10
```

**Output:**
```
📁 Available projects (15):
   - ACM_PROJECT: Advanced Cluster Management
   - OPENSHIFT_PROJECT: OpenShift Container Platform
   - SECURITY_PROJECT: Security Testing Framework
   - UI_PROJECT: User Interface Testing
   - API_PROJECT: API Testing Suite
   ... and 10 more
```

## 🎯 Advanced Usage

### Global Options

These options work with all commands:

| Option | Description | Default |
|--------|-------------|---------|
| `--config`, `-c` | Configuration file path | `polarion_config.json` |
| `--verbose`, `-v` | Enable verbose logging | False |

### Environment Variables

All commands respect these environment variables:

```bash
# Authentication
export POLARION_PAT_TOKEN='your-token'
export POLARION_URL='https://polarion.company.com'
export POLARION_PROJECT_ID='DEFAULT_PROJECT'

# Optional
export POLARION_USERNAME='username'
export POLARION_PASSWORD='password'
export POLARION_TIMEOUT='30'
export POLARION_VERIFY_SSL='true'
```

### Batch Operations

**Multiple Search Terms:**
```bash
# From command line
python3 -m polarion.cli fetch-learning \
    --search-terms "ACM" "OpenShift" "Kubernetes" "upgrade" "security"

# From file (one term per line)
echo -e "ACM\nOpenShift\nupgrade\nsecurity\nRBAC\nconsole" > search_terms.txt
python3 -m polarion.cli fetch-learning --search-file search_terms.txt
```

**Multiple Project Analysis:**
```bash
# Analyze multiple projects
for project in ACM_PROJECT OPENSHIFT_PROJECT SECURITY_PROJECT; do
    python3 -m polarion.cli fetch-learning \
        --project-id $project \
        --search-terms "upgrade" "security" \
        --output "learning_${project}.json"
done
```

### Integration with Framework

**Enhanced Analysis Workflow:**
```bash
# 1. Fetch learning data for ticket context
python3 -m polarion.cli fetch-learning \
    --search-terms "cluster" "import" "ACM" \
    --output learning_data.json

# 2. Run enhanced analysis (hypothetical integration)
analyze_ticket_enhanced ACM-12345 --learning-data learning_data.json

# 3. Post generated test cases
python3 -m polarion.cli post-test-cases \
    runs/ACM-12345/latest/Test-Cases.md \
    --report runs/ACM-12345/latest/Polarion-Report.md
```

## 🚨 Error Handling

### Common Error Messages and Solutions

#### Authentication Errors
```
❌ 401 Unauthorized: Invalid credentials
```
**Solution:**
```bash
# Check PAT token
echo "Token: $POLARION_PAT_TOKEN"
# Regenerate token in Polarion if needed
export POLARION_PAT_TOKEN='new_valid_token'
```

#### Connection Errors
```
❌ Connection timeout: Unable to reach Polarion server
```
**Solution:**
```bash
# Test basic connectivity
curl -k "$POLARION_URL/polarion/rest/v1/projects"
# Increase timeout
export POLARION_TIMEOUT='60'
```

#### Configuration Errors
```
❌ Configuration validation failed: Missing required fields
```
**Solution:**
```bash
# Regenerate configuration
python3 -m polarion.cli setup-config
# Edit with correct values
```

#### Project Access Errors
```
❌ Project 'PROJECT_ID' not accessible
```
**Solution:**
```bash
# List available projects
python3 -m polarion.cli list-projects
# Use correct project ID
```

#### SSL/TLS Errors
```
❌ SSL certificate verification failed
```
**Solution:**
```bash
# Disable SSL verification (not recommended for production)
export POLARION_VERIFY_SSL='false'
```

### Debugging with Verbose Mode

```bash
# Enable detailed logging for any command
python3 -m polarion.cli --verbose test-connection
python3 -m polarion.cli --verbose fetch-learning --search-terms "ACM"
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error (configuration, connection, etc.) |

## 📚 Examples by Use Case

### Learning from Existing Test Cases
```bash
# Comprehensive learning for ACM features
python3 -m polarion.cli fetch-learning \
    --search-terms "ACM" "Advanced Cluster Management" "cluster" "upgrade" \
    --limit 100 \
    --output comprehensive_acm_learning.json

# Security-focused learning
python3 -m polarion.cli fetch-learning \
    --search-terms "RBAC" "security" "authentication" "authorization" \
    --limit 50 \
    --output security_learning.json
```

### Research and Analysis
```bash
# Find upgrade-related test cases
python3 -m polarion.cli search \
    --search-terms "upgrade" "version" "migration" \
    --limit 20 \
    --output upgrade_test_cases.json

# Analyze UI testing patterns
python3 -m polarion.cli search \
    --search-terms "console" "UI" "interface" "frontend" \
    --output ui_test_patterns.json
```

### Production Test Case Posting
```bash
# Post with full metadata and reporting
python3 -m polarion.cli post-test-cases \
    production_test_cases.md \
    --project-id PRODUCTION_PROJECT \
    --metadata-file production_metadata.json \
    --status "approved" \
    --priority "high" \
    --report production_posting_report.md
```

## 🔄 Workflow Integration

This CLI is designed to integrate with the main Claude Test Generator framework:

1. **Pre-Analysis**: Fetch learning data before generating test cases
2. **Post-Generation**: Automatically post generated test cases to Polarion
3. **Continuous Learning**: Use posted test cases to improve future generations

See [Polarion Integration Workflow](.claude/workflows/polarion-integration.md) for complete integration documentation.

---

This reference guide provides complete documentation for all Polarion CLI functionality, eliminating the need to execute scripts to understand commands and options.