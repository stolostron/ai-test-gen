
# JIRA API Script: Setup and Usage Guide

## 🚀 Overview

This guide explains how to set up your environment and use a command-line script to interact with a JIRA ticket via its REST API. The focus is on secure configuration and common usage patterns.

***

## 📋 Prerequisites

1. **JIRA Account**: Access to a JIRA instance (e.g., Atlassian Cloud, a company-hosted server).  
2. **API Token**: A Personal Access Token (PAT) for secure, password-less authentication.  
3. **Required Tools**: `curl` and `jq` must be installed on your system.

***

## 🔑 Step 1: Generate Your JIRA API Token

An API token is the recommended way to authenticate with the JIRA API.

1. **Navigate** to the Personal Access Tokens (PAT) section in your JIRA profile. The URL is often similar to:  
   `https://your-jira-instance.com/secure/ViewProfile.jspa`

2. Click **"Create token"**.

3. **Configure the token**:  
   - **Name**: Give it a memorable name like `CLI-Script-Access`.  
   - **Expiry Date**: Set an expiration date for security.  

4. **Copy the generated token immediately**. You will not be able to see it again. Store it securely.

***

## 🔧 Step 2: Configure Environment Variables

Use environment variables to store your credentials securely, preventing them from being exposed in your command history or script files.

```bash
# The base URL of your JIRA instance
export JIRA_BASE_URL="https://your-jira-instance.com"

# The email address for your JIRA account
export JIRA_USERNAME="your.email@example.com"

# The API token you just generated
export JIRA_API_TOKEN="your_generated_api_token_here"

# The default ticket ID for the script to target (e.g., "PROJ-1234")
export JIRA_TICKET_ID="PROJ-1234"
```

💡 *Pro Tip*: Add these `export` commands to your shell's startup file (e.g., `~/.zshrc` or `~/.bashrc`) and run `source ~/.zshrc` to make them permanent for all future sessions.

***

## ▶️ Step 3: Typical Use Cases

Here are the most common ways to use the script (`./update-jira.sh`) from your terminal.

### Use Case 1: Check Ticket Info (Read-Only)
Verify your connection and get the current status, summary, and assignee of the ticket without making any changes.

```bash
./update-jira.sh --info
```

### Use Case 2: Add a Simple Comment
Post a quick update or note to the ticket's comment section.

```bash
./update-jira.sh --comment "Quick update: Staging deployment was successful."
```

### Use Case 3: Update Description from a File
For longer, formatted descriptions, write the content in a local file and use the script to apply it. This is ideal for detailed progress reports.

```bash
# Assumes 'report.md' contains the new description text
./update-jira.sh --description-file report.md
```

### Use Case 4: Target a Different Ticket
Temporarily override the default `JIRA_TICKET_ID` for a one-off operation on another ticket.

```bash
JIRA_TICKET_ID="PROJ-5678" ./update-jira.sh --info
```

### Use Case 5: Show Help
Display all available commands and flags for the script.

```bash
./update-jira.sh --help
```

***

## ⚠️ Troubleshooting

- **401 Unauthorized**: This error indicates your credentials are wrong. Double-check that `$JIRA_USERNAME` and `$JIRA_API_TOKEN` are set correctly and the token has not expired.  
- **403 Forbidden**: You are authenticated, but your account lacks the necessary permissions to view or edit the target ticket.  
- **Connection Errors**: Ensure `$JIRA_BASE_URL` is correct and that you have network access to your JIRA instance. You can test connectivity with:

```bash
curl --fail -u "$JIRA_USERNAME:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/2/serverInfo"
```

