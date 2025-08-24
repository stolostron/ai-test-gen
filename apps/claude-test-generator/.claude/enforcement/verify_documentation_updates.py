#!/usr/bin/env python3
"""
Documentation Consistency Verification
Verify that Agent C HTML sanitization enhancement is properly documented across all CLAUDE.md files
"""

import sys
from pathlib import Path

def check_file_contains(file_path, search_terms, description):
    """Check if file contains all required search terms"""
    try:
        content = Path(file_path).read_text()
        
        print(f"\n📋 Checking {description}:")
        print(f"   File: {file_path}")
        
        found_terms = []
        missing_terms = []
        
        for term in search_terms:
            if term.lower() in content.lower():
                found_terms.append(term)
                print(f"   ✅ Found: {term}")
            else:
                missing_terms.append(term)
                print(f"   ❌ Missing: {term}")
        
        success_rate = len(found_terms) / len(search_terms) * 100
        print(f"   📊 Coverage: {success_rate:.1f}% ({len(found_terms)}/{len(search_terms)} terms)")
        
        return len(missing_terms) == 0, missing_terms
        
    except FileNotFoundError:
        print(f"   ❌ File not found: {file_path}")
        return False, search_terms
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")
        return False, search_terms

def main():
    print("🔍 Agent C HTML Sanitization Documentation Verification")
    print("=" * 60)
    
    base_path = Path("/Users/ashafi/Documents/work/ai/ai_systems/apps/claude-test-generator")
    
    # Files to check and their required content
    checks = [
        {
            "file": base_path / "CLAUDE.md",
            "terms": ["Agent C HTML sanitization", "cascade failure prevention"],
            "description": "Main CLAUDE.md summary"
        },
        {
            "file": base_path / "CLAUDE.features.md", 
            "terms": ["Agent C with complete context inheritance and HTML sanitization", "Phase 2**: Parallel deep investigation (Documentation + GitHub with HTML sanitization", "html_contamination_prevention"],
            "description": "Framework features documentation"
        },
        {
            "file": base_path / "CLAUDE.policies.md",
            "terms": ["Agent C source sanitization", "Technical HTML tag prevention"],
            "description": "Policy enforcement documentation"
        },
        {
            "file": base_path / ".claude/ai-services/tg-enhanced-github-investigation-service.md",
            "terms": ["sanitize_collected_data", "html_sanitization_capabilities", "Stage 3.5"],
            "description": "Agent C service implementation"
        },
        {
            "file": base_path / ".claude/enforcement/AGENT_C_HTML_SANITIZATION_ENHANCEMENT.md",
            "terms": ["Proactive HTML sanitization", "WebFetch retrieves raw GitHub HTML", "dual-layer protection"],
            "description": "Enhancement documentation"
        }
    ]
    
    # Run all checks
    all_passed = True
    total_missing = []
    
    for check in checks:
        passed, missing = check_file_contains(
            check["file"],
            check["terms"],
            check["description"]
        )
        
        if not passed:
            all_passed = False
            total_missing.extend(missing)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Documentation Verification Summary:")
    
    if all_passed:
        print("✅ ALL DOCUMENTATION CHECKS PASSED")
        print("✅ Agent C HTML sanitization properly documented across all files")
        print("✅ Framework documentation is consistent and up-to-date")
        
        # Verify key integration points
        print("\n🔧 Key Integration Points Verified:")
        print("   ✅ Main CLAUDE.md references HTML sanitization")
        print("   ✅ Features documentation includes Phase 2 enhancement") 
        print("   ✅ Policies documentation includes mandatory enforcement")
        print("   ✅ Service implementation includes sanitization method")
        print("   ✅ Enhancement documentation provides complete details")
        
        return True
        
    else:
        print("❌ SOME DOCUMENTATION CHECKS FAILED")
        print(f"❌ Missing terms found: {len(total_missing)}")
        print("❌ Review and update documentation before deployment")
        
        if total_missing:
            print("\n📋 Missing Terms Summary:")
            for term in set(total_missing):
                print(f"   - {term}")
        
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 DOCUMENTATION VERIFICATION COMPLETE")
        print("All CLAUDE.md files properly document Agent C HTML sanitization enhancement!")
        sys.exit(0)
    else:
        print("\n⚠️ DOCUMENTATION VERIFICATION FAILED") 
        print("Update missing documentation before proceeding.")
        sys.exit(1)