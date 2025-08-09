#!/bin/bash

# ssh-github-validator.sh - SSH GitHub Access Validation and Setup
# Validates and helps configure SSH access to stolostron repositories

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_header() {
    echo
    echo "========================================"
    echo -e "${BLUE}🔐 SSH GitHub Access Validator${NC}"
    echo "========================================"
    echo "Validating access to stolostron repositories"
    echo
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Test SSH key availability
test_ssh_key() {
    print_step "1. Checking SSH key availability..."
    
    if [ -f ~/.ssh/id_rsa ] || [ -f ~/.ssh/id_ed25519 ] || [ -f ~/.ssh/id_ecdsa ]; then
        print_success "SSH key found"
        
        # Show available keys
        echo "Available SSH keys:"
        ls -la ~/.ssh/id_* 2>/dev/null | grep -v '.pub' || echo "  No private keys found"
        
        return 0
    else
        print_error "No SSH keys found in ~/.ssh/"
        return 1
    fi
}

# Test SSH agent
test_ssh_agent() {
    print_step "2. Checking SSH agent..."
    
    if [ -n "$SSH_AUTH_SOCK" ] && ssh-add -l >/dev/null 2>&1; then
        print_success "SSH agent is running with loaded keys"
        ssh-add -l
        return 0
    else
        print_warning "SSH agent not running or no keys loaded"
        return 1
    fi
}

# Test GitHub SSH connectivity
test_github_connectivity() {
    print_step "3. Testing GitHub SSH connectivity..."
    
    if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        print_success "GitHub SSH authentication successful"
        return 0
    else
        print_error "GitHub SSH authentication failed"
        return 1
    fi
}

# Test stolostron repository access
test_stolostron_access() {
    print_step "4. Testing stolostron repository access..."
    
    # Test access to a known public stolostron repository
    local test_repo="cluster-curator-controller"
    
    print_info "Testing access to stolostron/$test_repo..."
    
    # Create temporary directory for testing
    local temp_dir=$(mktemp -d)
    cd "$temp_dir"
    
    if git clone --depth=1 git@github.com:stolostron/$test_repo.git >/dev/null 2>&1; then
        print_success "Successfully accessed stolostron/$test_repo"
        
        # Test fetching a specific PR
        cd "$test_repo"
        if git fetch origin pull/468/head:test-pr >/dev/null 2>&1; then
            print_success "Successfully fetched PR #468 (digest upgrade feature)"
        else
            print_warning "Could not fetch specific PR (may be normal)"
        fi
        
        cd ..
        rm -rf "$temp_dir"
        return 0
    else
        print_error "Failed to access stolostron/$test_repo"
        rm -rf "$temp_dir"
        return 1
    fi
}

# Test Claude Code GitHub integration
test_claude_github_integration() {
    print_step "5. Testing Claude Code GitHub integration..."
    
    if command -v claude >/dev/null 2>&1; then
        print_info "Testing Claude Code's GitHub API access..."
        
        # Test if Claude can access GitHub repositories
        local test_response=$(claude --print "Can you access the file pkg/jobs/hive/hive.go from stolostron/cluster-curator-controller? Just respond with YES or NO." 2>/dev/null | grep -i "yes\|no" | head -1)
        
        if echo "$test_response" | grep -qi "yes"; then
            print_success "Claude Code can access GitHub repositories directly"
            return 0
        else
            print_warning "Claude Code GitHub access uncertain (may still work)"
            return 1
        fi
    else
        print_error "Claude Code CLI not available"
        return 1
    fi
}

# Generate SSH setup guide
generate_ssh_setup_guide() {
    local guide_file="SSH_GITHUB_SETUP_GUIDE.md"
    
    cat > "$guide_file" << 'EOF'
# 🔐 SSH GitHub Setup Guide for stolostron Access

## Quick Setup for Red Hat Developers

### 1. Generate SSH Key (if needed)
```bash
# Generate Ed25519 key (recommended)
ssh-keygen -t ed25519 -C "your.email@redhat.com"

# Or generate RSA key (alternative)
ssh-keygen -t rsa -b 4096 -C "your.email@redhat.com"
```

### 2. Add Key to SSH Agent
```bash
# Start SSH agent
eval "$(ssh-agent -s)"

# Add your SSH key
ssh-add ~/.ssh/id_ed25519  # or ~/.ssh/id_rsa
```

### 3. Add SSH Key to GitHub
```bash
# Copy public key to clipboard
cat ~/.ssh/id_ed25519.pub | pbcopy  # macOS
# or
cat ~/.ssh/id_ed25519.pub           # Linux - copy manually
```

Then:
1. Go to GitHub.com → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Paste your public key
4. Give it a descriptive title (e.g., "Red Hat MacBook Pro")

### 4. Test Connection
```bash
ssh -T git@github.com
# Should see: "Hi username! You've successfully authenticated..."
```

### 5. Configure Git (if needed)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@redhat.com"
```

### 6. Test stolostron Access
```bash
git clone git@github.com:stolostron/cluster-curator-controller.git
```

## Troubleshooting

### Permission Denied (publickey)
- Ensure SSH key is added to SSH agent: `ssh-add -l`
- Verify public key is added to GitHub
- Check SSH key permissions: `chmod 600 ~/.ssh/id_ed25519`

### Wrong Repository
- Use `git@github.com:stolostron/repo.git` format
- NOT `https://github.com/stolostron/repo.git`

### Corporate Network Issues
- Check if SSH port 22 is blocked
- Try GitHub's SSH over HTTPS: `ssh -T -p 443 git@ssh.github.com`
- Configure SSH config if needed:
```
Host github.com
  Hostname ssh.github.com
  Port 443
```

### Multiple SSH Keys
Create `~/.ssh/config`:
```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
```
EOF

    print_success "SSH setup guide created: $guide_file"
}

# Auto-fix common SSH issues
auto_fix_ssh_issues() {
    print_step "6. Attempting to auto-fix common SSH issues..."
    
    # Start SSH agent if not running
    if [ -z "$SSH_AUTH_SOCK" ]; then
        print_info "Starting SSH agent..."
        eval "$(ssh-agent -s)"
    fi
    
    # Add SSH keys to agent if available
    for key in ~/.ssh/id_rsa ~/.ssh/id_ed25519 ~/.ssh/id_ecdsa; do
        if [ -f "$key" ]; then
            print_info "Adding $key to SSH agent..."
            ssh-add "$key" 2>/dev/null || true
        fi
    done
    
    # Set proper permissions on SSH directory
    if [ -d ~/.ssh ]; then
        print_info "Setting proper SSH directory permissions..."
        chmod 700 ~/.ssh
        chmod 600 ~/.ssh/id_* 2>/dev/null || true
        chmod 644 ~/.ssh/*.pub 2>/dev/null || true
    fi
}

# Main validation function
main() {
    print_header
    
    local all_tests_passed=true
    
    # Run all tests
    test_ssh_key || all_tests_passed=false
    test_ssh_agent || { auto_fix_ssh_issues; test_ssh_agent || all_tests_passed=false; }
    test_github_connectivity || all_tests_passed=false
    test_stolostron_access || all_tests_passed=false
    test_claude_github_integration || all_tests_passed=false
    
    echo
    echo "========================================"
    if [ "$all_tests_passed" = true ]; then
        print_success "🎉 All SSH GitHub validations passed!"
        print_info "Your setup is ready for stolostron repository access"
        echo
        print_info "Framework capabilities enabled:"
        echo "  ✅ Direct GitHub repository access"
        echo "  ✅ Real-time PR and commit analysis"
        echo "  ✅ Cross-repository pattern discovery"
        echo "  ✅ Dynamic code fetching for Claude Code"
        echo
    else
        print_warning "⚠️  Some SSH validations failed"
        print_info "Generating setup guide to help resolve issues..."
        generate_ssh_setup_guide
        echo
        print_info "Please follow the generated SSH_GITHUB_SETUP_GUIDE.md"
        print_info "Then run this script again to validate"
    fi
    echo "========================================"
    
    return $([ "$all_tests_passed" = true ] && echo 0 || echo 1)
}

# Execute main function
main "$@"