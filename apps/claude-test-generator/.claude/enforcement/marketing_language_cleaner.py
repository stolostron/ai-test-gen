#!/usr/bin/env python3
"""
Marketing Language Cleaner

Systematically removes marketing language from enforcement system and documentation.
Replaces marketing terms with appropriate technical terminology.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

class MarketingLanguageCleaner:
    """Removes marketing language and replaces with technical terms"""
    
    def __init__(self):
        self.marketing_replacements = {
            # Primary marketing terms
            "enforcement": "enforcement",
            "enforcementS": "enforcements", 
            "enforcementD": "enforced",
            "strict": "strict",
            "comprehensive": "comprehensive",
            "high-quality": "high-quality",
            "enhanced": "enhanced",
            "improved": "improved",
            "enhancement": "enhancement",
            "enhancement": "enhancement",
            
            # Context-specific replacements
            "strict enforcement": "strict enforcement",
            "comprehensive enforcement": "comprehensive enforcement",
            "PROTECTION enforcement": "protection enforcement",
            "QUALITY enforcement": "quality enforcement",
            "RELIABILITY enforcement": "reliability enhancement",
            "SECURITY enforcement": "security enforcement",
            "COMPREHENSIVE enforcement": "comprehensive enforcement",
            
            # Certificate/ID terminology
            "IMPLEMENTATION ID": "IMPLEMENTATION ID",
            "enforcement CERTIFICATE": "ENFORCEMENT IMPLEMENTATION",
            "PROTECTION LEVEL": "PROTECTION LEVEL",  # Keep this as is
            
            # Technical accuracy improvements
            "ensures comprehensive": "enforces comprehensive",
            "provides comprehensive": "provides comprehensive", 
            "comprehensive protection": "comprehensive protection",
            "comprehensive coverage": "comprehensive coverage",
            "comprehensive compliance": "comprehensive compliance",
            "comprehensive prevention": "comprehensive prevention",
            
            # Scoring language fixes
            "high compliance": "high compliance",
            "full compliance": "full compliance",
            "high compliance": "high compliance",
            "target compliance": "target compliance"
        }
        
        self.files_processed = []
        self.changes_made = []
        
    def clean_file(self, file_path: Path) -> Tuple[bool, List[str]]:
        """Clean marketing language from a single file"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_in_file = []
            
            # Apply replacements
            for marketing_term, technical_term in self.marketing_replacements.items():
                if marketing_term in content:
                    old_count = content.count(marketing_term)
                    content = content.replace(marketing_term, technical_term)
                    new_count = content.count(marketing_term)
                    if old_count != new_count:
                        changes_in_file.append(f"Replaced '{marketing_term}' with '{technical_term}' ({old_count} instances)")
            
            # Write back if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.files_processed.append(str(file_path))
                self.changes_made.extend([f"{file_path}: {change}" for change in changes_in_file])
                return True, changes_in_file
            
            return False, []
            
        except Exception as e:
            return False, [f"Error processing {file_path}: {e}"]
    
    def clean_directory(self, directory_path: Path, file_patterns: List[str] = None) -> Dict:
        """Clean marketing language from all files in directory"""
        
        if file_patterns is None:
            file_patterns = ["*.py", "*.md", "*.json"]
        
        results = {
            "files_processed": 0,
            "files_changed": 0,
            "total_changes": 0,
            "errors": [],
            "changes_by_file": {}
        }
        
        # Find all matching files
        all_files = []
        for pattern in file_patterns:
            all_files.extend(directory_path.rglob(pattern))
        
        # Process each file
        for file_path in all_files:
            try:
                results["files_processed"] += 1
                
                changed, changes = self.clean_file(file_path)
                
                if changed:
                    results["files_changed"] += 1
                    results["total_changes"] += len(changes)
                    results["changes_by_file"][str(file_path)] = changes
                    
            except Exception as e:
                results["errors"].append(f"Error processing {file_path}: {e}")
        
        return results
    
    def generate_report(self, results: Dict, output_file: Path = None) -> str:
        """Generate comprehensive cleaning report"""
        
        report = f"""# Marketing Language Cleaning Report

**Timestamp**: {Path(__file__).stat().st_mtime}
**Scope**: Enforcement system and documentation files

## Summary

- **Files Processed**: {results['files_processed']}
- **Files Changed**: {results['files_changed']}
- **Total Changes**: {results['total_changes']}
- **Errors**: {len(results['errors'])}

## Changes by File

"""
        
        if results["changes_by_file"]:
            for file_path, changes in results["changes_by_file"].items():
                report += f"### {file_path}\n\n"
                for change in changes:
                    report += f"- {change}\n"
                report += "\n"
        else:
            report += "No changes were necessary - all files already use appropriate technical terminology.\n\n"
        
        # Error reporting
        if results["errors"]:
            report += "## Errors\n\n"
            for error in results["errors"]:
                report += f"- {error}\n"
            report += "\n"
        
        # Validation recommendations
        report += """## Technical Terminology Guidelines

**Preferred Technical Terms**:
- ✅ `enforcement` instead of `guarantee`
- ✅ `strict` instead of `absolute`
- ✅ `comprehensive` instead of `comprehensive`
- ✅ `high-quality` instead of `perfect`
- ✅ `enhancement` instead of `breakthrough`

**Reasoning**: Technical systems can have bugs, edge cases, or failures. Marketing language implies infallibility which is inappropriate for engineering documentation.

## Validation

After cleaning, verify that:
1. All functionality still works correctly
2. Configuration files parse properly
3. Enforcement systems operate as expected
4. Documentation remains clear and accurate

## Next Steps

1. Test all enforcement systems to ensure they still function
2. Validate configuration files parse correctly
3. Run framework tests to ensure no functionality is broken
4. Update any remaining references in generated content
"""
        
        # Save report if output file specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
        
        return report


def clean_marketing_language(target_directory: str = None) -> Dict:
    """Main function to clean marketing language from system"""
    
    if target_directory is None:
        target_directory = Path(__file__).parent
    else:
        target_directory = Path(target_directory)
    
    cleaner = MarketingLanguageCleaner()
    
    # Clean enforcement directory
    results = cleaner.clean_directory(target_directory)
    
    # Also clean parent CLAUDE.md files if we're in enforcement directory
    if target_directory.name == "enforcement":
        claude_files = target_directory.parent.parent.rglob("CLAUDE*.md")
        for claude_file in claude_files:
            try:
                changed, changes = cleaner.clean_file(claude_file)
                if changed:
                    results["files_changed"] += 1
                    results["total_changes"] += len(changes)
                    results["changes_by_file"][str(claude_file)] = changes
                results["files_processed"] += 1
            except Exception as e:
                results["errors"].append(f"Error processing {claude_file}: {e}")
    
    return results


if __name__ == "__main__":
    import sys
    
    # Allow target directory to be specified
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("🧹 **MARKETING LANGUAGE CLEANER**")
    print("Removing marketing terms and replacing with technical language...")
    print()
    
    # Clean the system
    results = clean_marketing_language(target_dir)
    
    # Generate and display report
    cleaner = MarketingLanguageCleaner()
    report = cleaner.generate_report(results)
    
    print(report)
    
    # Save report
    report_file = Path("marketing_language_cleaning_report.md")
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"📋 **Report saved**: {report_file}")
    
    # Exit with appropriate code
    if results["errors"]:
        print("⚠️ **Warnings**: Some errors occurred during processing")
        sys.exit(1)
    elif results["files_changed"] > 0:
        print("✅ **Success**: Marketing language cleaned successfully")
        sys.exit(0)
    else:
        print("ℹ️ **Info**: No marketing language found - files already clean")
        sys.exit(0)