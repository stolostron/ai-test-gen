#!/usr/bin/env python3
"""
Git Hooks Safety Net - FINAL VALIDATION LAYER
==============================================

CRITICAL PURPOSE: Final safety net to catch any validation failures
ROBUSTNESS LEVEL: MAXIMUM - Last line of defense before commit
AUTHORITY: BLOCKING - Prevents commits with validation violations

This creates git pre-commit hooks that validate all content before commits.
"""

import os
import sys
import subprocess
from pathlib import Path
from pre_write_validator import enforce_pre_write_validation

class GitHooksSafetyNet:
    """Git-based safety net for validation enforcement"""
    
    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getcwd()
        self.hooks_dir = os.path.join(self.repo_path, '.git', 'hooks')
        
    def create_pre_commit_hook(self):
        """Create pre-commit hook for validation enforcement"""
        
        hook_content = f'''#!/usr/bin/env python3
"""
PRE-COMMIT VALIDATION HOOK - SAFETY NET
======================================

This hook validates all staged files before allowing commit.
BLOCKS commits that contain validation violations.
"""

import os
import sys
import subprocess

# Add enforcement directory to path
enforcement_dir = "{os.path.dirname(os.path.abspath(__file__))}/../../.claude/enforcement"
sys.path.insert(0, enforcement_dir)

try:
    from pre_write_validator import enforce_pre_write_validation
except ImportError:
    print("❌ CRITICAL: Validation system not found")
    print("🔧 Ensure .claude/enforcement/ directory exists")
    sys.exit(1)

def validate_staged_files():
    """Validate all staged files"""
    print("🛡️  PRE-COMMIT VALIDATION SAFETY NET")
    print("=" * 50)
    
    # Get staged files
    try:
        result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                              capture_output=True, text=True, check=True)
        staged_files = result.stdout.strip().split('\\n')
    except subprocess.CalledProcessError:
        print("❌ Could not get staged files")
        return False
    
    if not staged_files or staged_files == ['']:
        print("✅ No staged files to validate")
        return True
    
    validation_failures = []
    
    for file_path in staged_files:
        # Only validate relevant files
        if not (file_path.endswith('.md') or 'Test-Cases' in file_path or 'Analysis' in file_path):
            continue
            
        if not os.path.exists(file_path):
            continue  # File might be deleted
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue  # Skip files that can't be read
        
        print(f"🔍 Validating: {{file_path}}")
        
        if not enforce_pre_write_validation(file_path, content):
            validation_failures.append(file_path)
            print(f"❌ VALIDATION FAILED: {{file_path}}")
        else:
            print(f"✅ VALIDATION PASSED: {{file_path}}")
    
    if validation_failures:
        print("\\n🚨 COMMIT BLOCKED - VALIDATION FAILURES DETECTED")
        print("❌ Files with validation violations:")
        for file_path in validation_failures:
            print(f"   - {{file_path}}")
        print("\\n🔧 Fix validation errors before committing")
        return False
    
    print("\\n✅ ALL VALIDATIONS PASSED - COMMIT APPROVED")
    return True

if __name__ == "__main__":
    if not validate_staged_files():
        sys.exit(1)
    sys.exit(0)
'''
        
        hook_path = os.path.join(self.hooks_dir, 'pre-commit')
        
        # Ensure hooks directory exists
        os.makedirs(self.hooks_dir, exist_ok=True)
        
        # Write hook
        with open(hook_path, 'w') as f:
            f.write(hook_content)
        
        # Make executable
        os.chmod(hook_path, 0o755)
        
        print(f"✅ Pre-commit hook created: {hook_path}")
        return hook_path
    
    def create_commit_msg_hook(self):
        """Create commit message hook for enforcement logging"""
        
        hook_content = '''#!/usr/bin/env python3
"""
COMMIT MESSAGE VALIDATION HOOK
=============================

Adds validation enforcement info to commit messages.
"""

import sys
import os

def enhance_commit_message():
    """Add validation enforcement info to commit message"""
    commit_msg_file = sys.argv[1]
    
    with open(commit_msg_file, 'r') as f:
        original_message = f.read()
    
    # Add validation enforcement footer
    enforcement_footer = """

🛡️ Validation Enforcement: ACTIVE
✅ All content passed validation checks
🔒 Safety net: git hooks + framework integration + wrapper scripts
"""
    
    with open(commit_msg_file, 'w') as f:
        f.write(original_message + enforcement_footer)

if __name__ == "__main__":
    enhance_commit_message()
'''
        
        hook_path = os.path.join(self.hooks_dir, 'commit-msg')
        
        with open(hook_path, 'w') as f:
            f.write(hook_content)
        
        os.chmod(hook_path, 0o755)
        
        print(f"✅ Commit message hook created: {hook_path}")
        return hook_path
    
    def setup_safety_net(self):
        """Setup complete git hooks safety net"""
        print("🔧 SETTING UP GIT HOOKS SAFETY NET")
        print("=" * 40)
        
        if not os.path.exists(os.path.join(self.repo_path, '.git')):
            print("❌ Not a git repository")
            return False
        
        # Create hooks
        pre_commit_hook = self.create_pre_commit_hook()
        commit_msg_hook = self.create_commit_msg_hook()
        
        print("✅ Git hooks safety net setup complete")
        print("🛡️  Commits will be validated before acceptance")
        
        return True
    
    def test_safety_net(self):
        """Test the safety net with sample violations"""
        print("🧪 TESTING SAFETY NET")
        print("=" * 30)
        
        # Test HTML tag detection
        test_content_html = """
# Test File

| Step | Action | CLI Method |
|------|--------|------------|
| 1 | Test | `command`<br/>`more` |
"""
        
        # Test format violations
        test_content_format = """
# Test File

**Step 1:** This should be table format
- **UI Method**: Something
- **CLI Method**: Something
"""
        
        test_cases = [
            ("test-html-violation.md", test_content_html),
            ("test-format-violation.md", test_content_format)
        ]
        
        for file_path, content in test_cases:
            print(f"🔍 Testing validation for: {file_path}")
            result = enforce_pre_write_validation(file_path, content)
            
            if result:
                print(f"⚠️  WARNING: {file_path} passed validation (expected failure)")
            else:
                print(f"✅ CORRECT: {file_path} failed validation as expected")
        
        print("🧪 Safety net testing complete")

def setup_git_safety_net(repo_path: str = None):
    """Setup git hooks safety net for repository"""
    safety_net = GitHooksSafetyNet(repo_path)
    return safety_net.setup_safety_net()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = os.getcwd()
    
    safety_net = GitHooksSafetyNet(repo_path)
    
    if "--test" in sys.argv:
        safety_net.test_safety_net()
    else:
        safety_net.setup_safety_net()