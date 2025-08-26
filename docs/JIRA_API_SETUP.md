# JIRA API Setup Guide for ACM-22620 Update

## 🚀 **Quick Start**

This script automatically updates JIRA ticket ACM-22620 with comprehensive progress information using the JIRA REST API.

## 📋 **Prerequisites**

1. **JIRA Account**: Red Hat JIRA access with edit permissions on ACM-22620
2. **API Token**: Personal Access Token from Red Hat JIRA
3. **Tools**: `curl` and `jq` (both already available on your system)

## 🔑 **Step 1: Get Your JIRA API Token**

1. **Navigate to**: [https://issues.redhat.com/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens](https://issues.redhat.com/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens)

2. **Click "Create token"**

3. **Enter token details**:
   - **Label**: `ACM-QE-API-Access` (or any descriptive name)
   - **Expires**: Set appropriate expiration (e.g., 90 days)

4. **Copy the generated token** (save it securely - you won't see it again!)

## 🔧 **Step 2: Set Environment Variables**

```bash
# Set your Red Hat email
export JIRA_USERNAME="your.email@redhat.com"

# Set your JIRA API token (replace with your actual token)
export JIRA_API_TOKEN="your_generated_api_token_here"
```

**💡 Tip**: Add these to your `~/.zshrc` or `~/.bashrc` for persistence:

```bash
echo 'export JIRA_USERNAME="your.email@redhat.com"' >> ~/.zshrc
echo 'export JIRA_API_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

## ▶️ **Step 3: Run the Update Script**

### **Option A: Full Update (Recommended)**
```bash
./update-jira-ticket.sh
```

This will:
- ✅ Update the ticket description with comprehensive progress
- ✅ Add a progress comment with key highlights
- ✅ Show confirmation before making changes

### **Option B: Check Ticket Info Only**
```bash
./update-jira-ticket.sh --info
```

This will:
- 📋 Show current ticket status, assignee, and summary
- 🔍 Verify your API access without making changes

### **Option C: Show Help**
```bash
./update-jira-ticket.sh --help
```

## 🎯 **What Gets Updated**

### **Ticket Description**
- Complete framework progress summary
- Workflow architecture diagram (text format)
- Key achievements and performance metrics
- Current implementation status (validated with ACM-22079 example)
- Next steps and roadmap
- All key links (GitHub repo, documentation, examples)

### **Progress Comment**
- High-level status update
- Key deliverables summary
- Links to framework and documentation

## 🔍 **Verification**

After running the script, verify the update:

1. **Visit**: [https://issues.redhat.com/browse/ACM-22620](https://issues.redhat.com/browse/ACM-22620)
2. **Check**: Updated description with comprehensive progress
3. **Review**: New comment with framework highlights
4. **Confirm**: All links are working (GitHub repo, documentation)

## ⚠️ **Troubleshooting**

### **Authentication Issues**
```bash
# Error: 401 Unauthorized
# Solution: Check your username and API token
echo "Username: $JIRA_USERNAME"
echo "Token set: $(if [[ -n "$JIRA_API_TOKEN" ]]; then echo "Yes"; else echo "No"; fi)"
```

### **Permission Issues**
```bash
# Error: 403 Forbidden
# Solution: Ensure you have edit permissions on ACM-22620
./update-jira-ticket.sh --info  # Test read access first
```

### **Network Issues**
```bash
# Test JIRA connectivity
curl -s -u "$JIRA_USERNAME:$JIRA_API_TOKEN" \
  "https://issues.redhat.com/rest/api/2/issue/ACM-22620" | jq .key
# Should return: "ACM-22620"
```

## 🛡️ **Security Notes**

- ✅ **API tokens are safer than passwords** - they can be revoked individually
- ✅ **Tokens have expiration dates** - set appropriate validity periods
- ✅ **Script uses HTTPS** - all communication is encrypted
- ⚠️ **Never commit tokens to git** - use environment variables only
- ⚠️ **Store tokens securely** - treat them like passwords

## 📊 **Expected Output**

```bash
[INFO] Starting JIRA ticket update for ACM-22620...
================================================================
[SUCCESS] JIRA credentials found
[INFO] Fetching current ticket information...
[SUCCESS] Successfully fetched ticket information
Current ticket info:
Summary: Investigate - Use Claude's agentic capabilities
Status: In Progress
Assignee: Atif Shafi
================================================================
[INFO] Creating update content...
[SUCCESS] Update content created
================================================================
[WARNING] About to update JIRA ticket ACM-22620 with comprehensive progress information
Do you want to proceed? (y/N): y
================================================================
[SUCCESS] ✅ Ticket description updated successfully
[SUCCESS] ✅ Progress comment added successfully
================================================================
[SUCCESS] JIRA ticket update completed!
[INFO] View the updated ticket: https://issues.redhat.com/browse/ACM-22620
[INFO] Cleanup completed
```

## 🎯 **Ready to Go!**

Your script is ready to update ACM-22620 with all the framework progress we've made. Just set your credentials and run it! 🚀