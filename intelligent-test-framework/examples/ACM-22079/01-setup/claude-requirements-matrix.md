# Claude Code Requirements Detection & Auto-Configuration Matrix

## What Our Detection System Covers

### ✅ **Automatic Detection & Configuration**

| Component | Detection | Auto-Configuration | Manual Steps Required |
|-----------|-----------|-------------------|----------------------|
| **Claude Code CLI** | ✅ Detects installation & version | ✅ Auto-installs via npm if missing | None (if npm available) |
| **Environment Variables** | ✅ Validates all required vars | ✅ Auto-adds to shell config | Reload shell config |
| **Google Cloud CLI** | ✅ Checks installation & config | ✅ Auto-sets project | Authentication commands |
| **Node.js & NPM** | ✅ Detects versions | ✅ Configures npm global prefix | Install if missing |
| **Network Connectivity** | ✅ Tests internet & API endpoints | ❌ Reports issues only | Fix network/firewall |
| **Permissions** | ✅ Validates file/directory access | ❌ Reports issues only | Fix permissions manually |
| **Authentication** | ✅ Checks Google Cloud auth status | ❌ Provides commands to run | Run auth commands |

### 🔧 **What Gets Auto-Configured**

#### Environment Variables
```bash
# These are automatically added to your shell config:
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=itpc-gcp-hcm-pe-eng-claude
export ANTHROPIC_MODEL='claude-sonnet-4@20250514'
export ANTHROPIC_SMALL_FAST_MODEL='claude-sonnet-4@20250514'
```

#### NPM Configuration
```bash
# Auto-configured:
npm config set prefix '~/.npm-global'
# PATH updated in shell config:
export PATH=$HOME/.npm-global/bin:$PATH
```

#### Google Cloud Project
```bash
# Auto-configured:
gcloud config set project itpc-gcp-hcm-pe-eng-claude
```

#### Directory Structure
```bash
# Auto-created:
~/.config/claude-code/          # Claude config directory
~/.npm-global/                  # NPM global directory
```

### ⚠️ **Manual Steps Still Required**

#### 1. Initial Software Installation (if missing)
```bash
# macOS
brew install node                           # For Node.js/NPM
brew install --cask google-cloud-sdk       # For Google Cloud CLI

# Linux
sudo apt-get install nodejs npm            # For Node.js/NPM
# Follow Google Cloud installation guide
```

#### 2. Google Cloud Authentication
```bash
# These commands must be run manually:
gcloud auth login                                                           # Authenticate with Google
gcloud auth application-default login                                      # Set application credentials
gcloud auth application-default set-quota-project cloudability-it-gemini   # Set quota project
```

#### 3. Shell Configuration Reload
```bash
# After auto-configuration, reload shell:
source ~/.zshrc     # macOS (zsh)
source ~/.bashrc    # Linux (bash)
```

### 🎯 **Detection Results Interpretation**

#### ✅ All Green - Ready to Go
```
[SUCCESS] ✓ Claude Code CLI found: 1.0.64 (Claude Code)
[SUCCESS] ✓ Environment Variables: All configured
[SUCCESS] ✓ Google Cloud: Configured and authenticated
[SUCCESS] ✓ API Connection: Successfully tested
```
**Action**: Proceed with analysis immediately

#### ⚠️ Warnings - Minor Issues
```
[WARNING] ⚠ Google Cloud project: wrong-project (expected: itpc-gcp-hcm-pe-eng-claude)
[WARNING] ⚠ ANTHROPIC_MODEL: old-model (expected: claude-sonnet-4@20250514)
```
**Action**: Script auto-fixes these, reload shell and re-run

#### ❌ Errors - Manual Action Required
```
[ERROR] ✗ Claude Code CLI not found
[ERROR] ✗ Not authenticated with Google Cloud
[ERROR] ✗ Node.js not found
```
**Action**: Follow provided installation/authentication commands

### 🔄 **Auto-Recovery Process**

Our detection system follows this flow:

1. **Detect Issue** → 2. **Attempt Auto-Fix** → 3. **Provide Manual Instructions** → 4. **Re-validate**

#### Example Auto-Recovery Flow:
```
[WARNING] ✗ Environment variable CLAUDE_CODE_USE_VERTEX is not set
[CONFIG] Auto-configuring missing environment variables...
[CONFIG] Using shell config: /Users/ashafi/.zshrc
[CONFIG] Adding Claude Code environment variables to /Users/ashafi/.zshrc
[SUCCESS] ✓ Environment variables added to /Users/ashafi/.zshrc
[SUCCESS] ✓ Configuration reloaded
```

### 🛠️ **Advanced Configuration Detection**

#### Permissions and Security
- ✅ Checks write permissions in project directory
- ✅ Validates home directory access
- ✅ Detects if running as root (warns about potential issues)
- ✅ Verifies appropriate user context

#### Network and Connectivity
- ✅ Tests internet connectivity (ping google.com)
- ✅ Validates Google Cloud AI Platform endpoint access
- ✅ Checks for proxy/firewall issues
- ✅ Verifies DNS resolution

#### Claude Code Specific
- ✅ Creates Claude configuration directory if missing
- ✅ Validates project context setup
- ✅ Tests actual API connectivity with timeout
- ✅ Verifies response quality and content

### 🚨 **Common Issues and Auto-Fixes**

#### Issue: "claude: command not found"
**Auto-Fix**: 
- Installs via npm if npm is available
- Configures PATH correctly
- Clears shell command cache

#### Issue: Wrong environment variables
**Auto-Fix**:
- Detects existing config
- Updates or adds missing variables
- Reloads configuration automatically

#### Issue: Wrong Google Cloud project
**Auto-Fix**:
- Sets correct project automatically
- Validates change was successful
- Continues with authentication check

#### Issue: NPM global directory not configured
**Auto-Fix**:
- Creates ~/.npm-global directory
- Sets npm prefix configuration
- Updates PATH in shell config

### 🔍 **Manual Verification Commands**

After auto-configuration, you can manually verify:

```bash
# Check Claude Code
claude --version
which claude

# Check environment variables
echo $CLAUDE_CODE_USE_VERTEX
echo $ANTHROPIC_VERTEX_PROJECT_ID

# Check Google Cloud
gcloud config list
gcloud auth list

# Test Claude Code connection
claude --print "Hello, test message"
```

### 📋 **Setup Validation Checklist**

Our comprehensive check validates:
- [ ] Claude Code CLI installed and in PATH
- [ ] All 5 required environment variables set correctly
- [ ] Google Cloud CLI installed and configured
- [ ] Correct Google Cloud project selected
- [ ] Google Cloud authentication active
- [ ] Node.js and NPM installed and configured
- [ ] NPM global directory configured correctly
- [ ] Appropriate file and directory permissions
- [ ] Internet connectivity available
- [ ] Google Cloud AI Platform accessible
- [ ] Claude Code configuration directory exists
- [ ] Actual Claude Code API connection working

### 🎯 **Expected Outcomes**

**Success Scenario** (Most Common):
```
🎯 Comprehensive setup check PASSED!
🚀 Ready to proceed with ACM-22079 analysis!
```

**Partial Success** (Some Auto-Fixes Applied):
```
⚠ Setup check identified issues that need attention
📋 Required actions: [specific steps provided]
🔧 Common solutions: [specific commands provided]
```

**Manual Intervention Required** (Missing Core Components):
```
✗ Critical components missing
📋 Required installations: [specific software to install]
🔧 Run after installing: [specific commands to run]
```

## Summary

✅ **Our detection system handles 80-90% of setup issues automatically**  
⚠️ **Manual steps only required for core software installation and authentication**  
🔄 **Re-running the script after manual steps validates all fixes**  
🎯 **Result: Reliable, working Claude Code setup for ACM-22079 analysis**