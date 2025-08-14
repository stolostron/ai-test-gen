# Polarion Integration Setup Guide

## 🚀 Complete Setup Guide for Polarion Integration

This guide provides step-by-step instructions for setting up Polarion integration with the Claude Test Generator framework.

## 📋 Prerequisites

### System Requirements
- **Python 3.8+** (Check with: `python3 --version`)
- **pip3** package manager
- **Internet access** to Polarion server
- **Valid Polarion credentials** (PAT token or username/password)

### Required Access
- Polarion server access
- Project permissions for test case reading/writing
- Network connectivity to Polarion REST API

## 🔧 Step 1: Install Dependencies

### Navigate to Framework Directory
```bash
cd apps/claude-test-generator
```

### Install Python Dependencies
```bash
# Install required packages
pip3 install -r requirements.txt

# If requirements.txt doesn't exist, install manually:
pip3 install requests python-dotenv
```

### Verify Installation
```bash
python3 -c "import requests; print('✅ Dependencies installed successfully')"
```

## ⚙️ Step 2: Configure Credentials

### Option A: Secure Local Storage (Recommended)

**Interactive Setup:**
```bash
# Set up credentials interactively with secure storage
python3 -m polarion.cli setup-credentials
```

This will:
- Prompt for Polarion URL, project ID, and PAT token
- Store credentials securely in `.polarion/credentials.json` (owner-only access)
- Automatically add the directory to `.gitignore`
- Test the connection

**Check Status:**
```bash
# View credential storage status
python3 -m polarion.cli credential-status
```

**Benefits of Local Storage:**
- 🔒 **Secure**: Files stored with owner-only permissions (600)
- 🚫 **Git-ignored**: Credentials never committed to version control
- 🎯 **Framework-local**: Stored within framework directory
- 🔄 **Persistent**: No need to set environment variables each session

### Option B: Environment Variables (Alternative)

If you prefer environment variables, set these in your shell profile:

```bash
# Required for authentication
export POLARION_PAT_TOKEN='your-personal-access-token-here'
export POLARION_URL='https://polarion.your-company.com'
export POLARION_PROJECT_ID='YOUR_PROJECT_ID'

# Optional configuration
export POLARION_USERNAME='username'           # Alternative to PAT
export POLARION_PASSWORD='password'           # Alternative to PAT  
export POLARION_TEST_CASE_TYPE='testcase'    # Default test case type
export POLARION_TIMEOUT='30'                 # API timeout in seconds
export POLARION_VERIFY_SSL='true'            # SSL verification
```

**Apply Environment Variables:**
```bash
# Reload your shell profile
source ~/.bashrc  # or ~/.zshrc

# Verify variables are set
echo "Polarion URL: $POLARION_URL"
echo "Project ID: $POLARION_PROJECT_ID"
```

### Priority Order
The framework loads credentials in this order (later sources override earlier ones):
1. Configuration file (`polarion_config.json`)
2. **Secure local storage** (`.polarion/credentials.json`)
3. Environment variables (highest priority)

## 📄 Step 3: Create Configuration File

### Generate Sample Configuration
```bash
python3 -m polarion.cli setup-config
```

This creates `polarion_config.json` with default settings.

### Customize Configuration
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

### Configuration Validation
```bash
python3 -m polarion.cli test-connection
```

## 🔍 Step 4: Test Connection

### Basic Connection Test
```bash
# Test API connectivity
python3 -m polarion.cli test-connection
```

**Expected Output:**
```
✅ Configuration validation passed
✅ Polarion API connection successful
✅ Project access confirmed: Advanced Cluster Management
```

### Credential Management Commands

**Check Credential Status:**
```bash
# View detailed credential status
python3 -m polarion.cli credential-status
```

**Update Credentials:**
```bash
# Re-run setup to update stored credentials
python3 -m polarion.cli setup-credentials
```

**Remove Credentials:**
```bash
# Remove stored credentials (with confirmation)
python3 -m polarion.cli remove-credentials

# Force removal without confirmation
python3 -m polarion.cli remove-credentials --force
```

### Troubleshooting Connection Issues

#### SSL Certificate Issues
```bash
# Disable SSL verification if needed
export POLARION_VERIFY_SSL='false'
python3 -m polarion.cli test-connection
```

#### Authentication Issues
```bash
# Verify PAT token format
echo "PAT Token length: ${#POLARION_PAT_TOKEN}"

# Test with username/password if PAT fails
export POLARION_USERNAME='your_username'
export POLARION_PASSWORD='your_password'
unset POLARION_PAT_TOKEN
```

#### Network Connectivity
```bash
# Test basic HTTP connectivity
curl -k "$POLARION_URL/polarion/rest/v1/projects"

# Check firewall/proxy settings
ping polarion.your-company.com
```

## 📚 Step 5: Verify Learning Capabilities

### Test Learning Data Fetch
```bash
# Fetch sample learning data
python3 -m polarion.cli fetch-learning \
    --search-terms "ACM" "upgrade" \
    --limit 10 \
    --output test_learning.json
```

**Expected Output:**
```
🔍 Fetching learning samples from project: ACM_PROJECT
📋 Search terms: ACM, upgrade
✅ Learning data saved to: test_learning.json

📊 Summary:
   - Test cases analyzed: 10
   - Average steps per test: 6.2
   - Top validation approaches: ['resource_verification', 'log_verification', 'api_verification']
   - Technologies covered: ['ACM', 'OpenShift', 'Kubernetes']
```

### Verify Learning Data Structure
```bash
# Check learning data format
python3 -c "
import json
with open('test_learning.json', 'r') as f:
    data = json.load(f)
    print(f\"✅ Learning data contains {len(data.get('test_cases', []))} test cases\")
    print(f\"✅ Patterns discovered: {len(data.get('patterns', {}))} categories\")
"
```

## 📤 Step 6: Test Posting Capabilities

### Create Test Markdown File
Create `test_cases_sample.md`:

```markdown
## Test Case 1: Sample Connection Test

**Description:** Validates Polarion integration is working correctly

**Setup:** Access to ACM hub cluster

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster.com:6443 --username=admin --password=<password> --insecure-skip-tls-verify=true` | Login successful with access confirmed |
| **Step 2: Verify cluster status** - Check cluster health: `oc get nodes` | All nodes in Ready state |
```

### Test Posting (Dry Run)
```bash
# Test posting without actually creating test cases
python3 -m polarion.cli post-test-cases \
    test_cases_sample.md \
    --project-id $POLARION_PROJECT_ID \
    --status "draft" \
    --report test_posting_report.md
```

## 🔧 Step 7: Advanced Configuration

### Configure Learning Search Terms
Edit the `learning_search_terms` in your config file based on your domain:

```json
{
  "learning_search_terms": [
    "your_product_name",
    "specific_features",
    "technology_stack",
    "common_test_scenarios"
  ]
}
```

### Set Up Custom Metadata Templates
Create `metadata_template.json`:

```json
{
  "custom_fields": {
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

## ✅ Verification Checklist

Before using Polarion integration in production, verify:

- [ ] **Python 3.8+** installed and accessible
- [ ] **Dependencies** installed successfully
- [ ] **Environment variables** set and verified
- [ ] **Configuration file** created and customized
- [ ] **Connection test** passes successfully
- [ ] **Project access** confirmed
- [ ] **Learning fetch** works with sample data
- [ ] **Test posting** verified (dry run)
- [ ] **SSL/TLS** configuration appropriate for your environment
- [ ] **Firewall/proxy** settings allow Polarion access

## 🚨 Common Issues and Solutions

### Issue: "Module not found" errors
**Solution:**
```bash
# Ensure you're in the correct directory
cd apps/claude-test-generator

# Reinstall dependencies
pip3 install -r requirements.txt
```

### Issue: "401 Unauthorized" errors
**Solution:**
```bash
# Check PAT token validity
# Regenerate token in Polarion if needed
export POLARION_PAT_TOKEN='new_valid_token'
```

### Issue: "Connection timeout" errors
**Solution:**
```bash
# Increase timeout
export POLARION_TIMEOUT='60'

# Check network connectivity
ping polarion.your-company.com
```

### Issue: "SSL certificate verification failed"
**Solution:**
```bash
# Disable SSL verification (not recommended for production)
export POLARION_VERIFY_SSL='false'

# Or install proper certificates
```

## 🎯 Next Steps

After successful setup:

1. **Integration with Framework**: See `.claude/workflows/polarion-integration.md`
2. **Learning Enhancement**: Use learning data to improve test generation
3. **Automated Workflows**: Set up automated posting from CI/CD
4. **Team Training**: Share configuration with team members

## 📚 Additional Resources

- **[Polarion Integration Workflow](.claude/workflows/polarion-integration.md)** - Complete workflow guide
- **[CLI Reference](polarion/README.md)** - Detailed CLI documentation  
- **[Usage Examples](examples/polarion_usage_example.py)** - Python integration examples
- **[Framework Documentation](CLAUDE.md)** - Main framework documentation

---

## 🔒 Security Notes

### Credential Storage Security
- **Secure Local Storage**: Credentials stored in `.polarion/` directory with owner-only permissions
- **File Permissions**: 600 (owner read/write only) for credential files, 700 for directory
- **Git Protection**: `.polarion/` directory automatically added to `.gitignore`
- **No Version Control**: Credentials never committed to git repositories
- **Framework Isolation**: Credentials stored within framework directory, not globally

### Best Practices
- **Regular Rotation**: Regularly rotate PAT tokens in Polarion
- **SSL Validation**: Always validate SSL certificates in production environments
- **Network Security**: Restrict network access to Polarion server as appropriate
- **Access Control**: Use PAT tokens instead of username/password when possible
- **Monitoring**: Monitor credential usage through Polarion's access token management

### Migration from Environment Variables
If you previously used environment variables, you can:
1. Run `python3 -m polarion.cli setup-credentials` to store them securely
2. Remove environment variables from shell profile
3. Use `python3 -m polarion.cli credential-status` to verify secure storage

### Credential Lifecycle
```bash
# Initial setup
python3 -m polarion.cli setup-credentials

# Regular checks
python3 -m polarion.cli credential-status

# Update when tokens change
python3 -m polarion.cli setup-credentials  # Overwrites existing

# Remove when no longer needed
python3 -m polarion.cli remove-credentials
```

This setup guide replaces the `setup_polarion.sh` script with comprehensive documentation that includes secure credential management through local storage rather than environment variables.