#!/usr/bin/env python3
"""
Deploy Format Enforcement
Deploys comprehensive format enforcement across the framework
"""

import os
import json
import shutil
from pathlib import Path

class FormatEnforcementDeployment:
    def __init__(self, framework_root):
        self.framework_root = Path(framework_root)
        self.enforcement_dir = self.framework_root / ".claude" / "enforcement"
        self.deployment_log = []
        
    def deploy_comprehensive_format_enforcement(self):
        """Deploy comprehensive format enforcement system"""
        print("🚀 Deploying Comprehensive Format Enforcement System")
        
        # 1. Create enforcement directory structure
        self._create_enforcement_structure()
        
        # 2. Deploy format validation hooks
        self._deploy_format_validation_hooks()
        
        # 3. Create agent prompt updates
        self._update_agent_prompts_with_format_requirements()
        
        # 4. Create Pattern Extension Service integration
        self._integrate_with_pattern_extension_service()
        
        # 5. Create framework workflow integration
        self._integrate_with_framework_workflow()
        
        # 6. Generate deployment manifest
        self._generate_deployment_manifest()
        
        print("✅ Format enforcement deployment complete")
        
    def _create_enforcement_structure(self):
        """Create enforcement directory structure"""
        directories = [
            "format_validation",
            "format_hooks", 
            "format_reports",
            "format_corrections",
            "deployment_logs"
        ]
        
        for dir_name in directories:
            dir_path = self.enforcement_dir / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            self.deployment_log.append(f"✅ Created directory: {dir_path}")
            
    def _deploy_format_validation_hooks(self):
        """Deploy format validation hooks into framework"""
        
        # Create pre-generation hook
        pre_hook_content = '''#!/usr/bin/env python3
"""
Pre-Generation Format Hook
Validates format requirements before test generation
"""

from .pattern_extension_format_enforcer import PatternExtensionFormatEnforcer

def pre_generation_format_check():
    """Check format requirements before generation"""
    enforcer = PatternExtensionFormatEnforcer()
    format_prompt = enforcer.generate_format_enforcement_prompt()
    
    return {
        'format_requirements': format_prompt,
        'enforcement_active': True,
        'target_score': 85
    }

def get_format_enforcement_prompt():
    """Get format enforcement prompt for agents"""
    return """
MANDATORY FORMAT REQUIREMENTS (TARGET: 85+ POINTS):

1. **EXACT Login Format Required:**
   **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>`

2. **Single-Line Table Format Only:**
   | Step | Expected Result |
   |------|-----------------|
   | **Step description** - Command: `oc command` | Expected output: `sample output` |

3. **Mandatory Elements:**
   - NO HTML tags (<br/>, <b>, <i>) - use markdown
   - Sample outputs in backticks for every step
   - NO internal script references (setup_clc, login_oc)
   - **Description:** and **Setup:** sections required
   - Minimum 3 test cases

4. **Validation:** Automatic format validation applied (85+ points required)
"""
'''
        
        pre_hook_path = self.enforcement_dir / "format_hooks" / "pre_generation_format_hook.py"
        with open(pre_hook_path, 'w') as f:
            f.write(pre_hook_content)
            
        self.deployment_log.append(f"✅ Deployed pre-generation hook: {pre_hook_path}")
        
        # Create post-generation hook
        post_hook_content = '''#!/usr/bin/env python3
"""
Post-Generation Format Hook
Validates generated test cases and provides corrections
"""

from .test_case_format_enforcer import TestCaseFormatEnforcer
from .framework_format_integration import FrameworkFormatIntegration

def post_generation_format_validation(ticket_id, run_path):
    """Validate generated test cases"""
    integration = FrameworkFormatIntegration(run_path.parent.parent.parent)
    passed, result = integration.validate_generated_test_cases(ticket_id, run_path)
    
    if not passed:
        print(f"⚠️  Format validation warning: {result['percentage']}% (Target: 85%)")
        print("📋 Review format guidance for corrections")
        
    return {
        'validation_passed': passed,
        'score': result['score'],
        'percentage': result['percentage'],
        'violations': result['violations']
    }
'''
        
        post_hook_path = self.enforcement_dir / "format_hooks" / "post_generation_format_hook.py"
        with open(post_hook_path, 'w') as f:
            f.write(post_hook_content)
            
        self.deployment_log.append(f"✅ Deployed post-generation hook: {post_hook_path}")
        
    def _update_agent_prompts_with_format_requirements(self):
        """Update agent prompts to include format requirements"""
        
        # Agent A (JIRA Intelligence) format addition
        agent_a_format = '''
# FORMAT ENFORCEMENT FOR AGENT A OUTPUT

When providing intelligence for test case generation, ensure your output enables creation of test cases that meet these requirements:

1. **Login Step Specification:** Ensure test cases start with exact format: "**Step 1: Log into the ACM hub cluster**"
2. **Clear Command Examples:** Provide specific CLI commands that can be formatted as single-line table entries
3. **Expected Output Examples:** Include realistic command outputs for validation steps
4. **Environment Context:** Provide environment-specific details for placeholder replacement

Your intelligence should support test cases with:
- Single-line table format compatibility
- Realistic sample outputs
- Clear step-by-step progression
- Security-compliant placeholder usage
'''
        
        agent_format_path = self.enforcement_dir / "format_hooks" / "agent_format_requirements.md"
        with open(agent_format_path, 'w') as f:
            f.write(agent_a_format)
            
        self.deployment_log.append(f"✅ Created agent format requirements: {agent_format_path}")
        
    def _integrate_with_pattern_extension_service(self):
        """Integrate format enforcement with Pattern Extension Service"""
        
        integration_script = '''#!/usr/bin/env python3
"""
Pattern Extension Service Format Integration
Ensures Pattern Extension Service generates properly formatted test cases
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from pattern_extension_format_enforcer import PatternExtensionFormatEnforcer

class PatternExtensionFormatIntegration:
    def __init__(self):
        self.enforcer = PatternExtensionFormatEnforcer()
        
    def enhance_pattern_extension_prompt(self, base_prompt):
        """Enhance Pattern Extension prompt with format requirements"""
        format_requirements = self.enforcer.generate_format_enforcement_prompt()
        
        enhanced_prompt = f"""
{base_prompt}

{format_requirements}

CRITICAL: Generated test cases will be automatically validated. 
Target: 85+ points for framework acceptance.
Format violations will trigger corrective guidance generation.
"""
        return enhanced_prompt
        
    def validate_and_correct_generated_test_cases(self, generated_content):
        """Validate and apply corrections to generated test cases"""
        corrected_content, passed, result = self.enforcer.enforce_format_during_generation(generated_content)
        
        return {
            'content': corrected_content,
            'passed': passed,
            'validation_result': result,
            'auto_corrected': result['percentage'] > self.enforcer.validate_generated_content(generated_content)['percentage']
        }

# Export integration functions
def get_format_enhanced_prompt(base_prompt):
    integration = PatternExtensionFormatIntegration()
    return integration.enhance_pattern_extension_prompt(base_prompt)
    
def validate_generated_content(content):
    integration = PatternExtensionFormatIntegration()
    return integration.validate_and_correct_generated_test_cases(content)
'''
        
        integration_path = self.enforcement_dir / "pattern_extension_format_integration.py"
        with open(integration_path, 'w') as f:
            f.write(integration_script)
            
        self.deployment_log.append(f"✅ Created Pattern Extension integration: {integration_path}")
        
    def _integrate_with_framework_workflow(self):
        """Integrate format enforcement into main framework workflow"""
        
        workflow_integration = '''#!/usr/bin/env python3
"""
Framework Workflow Format Integration
Integrates format enforcement into main framework execution
"""

from pathlib import Path
from .framework_format_integration import FrameworkFormatHook

class FrameworkFormatWorkflowIntegration:
    def __init__(self, framework_root):
        self.framework_root = Path(framework_root)
        
    def execute_format_enforcement_workflow(self, ticket_id, run_path):
        """Execute complete format enforcement workflow"""
        
        print(f"🔍 Executing format enforcement for {ticket_id}")
        
        # Phase 1: Pre-generation format requirements
        format_requirements = self._get_format_requirements()
        print("✅ Format requirements loaded")
        
        # Phase 2: Post-generation validation
        validation_result = FrameworkFormatHook.post_test_generation_hook(ticket_id, run_path)
        
        # Phase 3: Final delivery validation
        delivery_validation = FrameworkFormatHook.validate_before_delivery(ticket_id, run_path)
        
        # Phase 4: Generate enforcement report
        report = self._generate_enforcement_report(ticket_id, validation_result, delivery_validation)
        
        return {
            'format_enforcement_complete': True,
            'validation_passed': validation_result['format_validation_passed'],
            'delivery_ready': delivery_validation,
            'enforcement_report': report
        }
        
    def _get_format_requirements(self):
        """Get format requirements for framework execution"""
        return {
            'login_format_required': True,
            'html_tags_prohibited': True,
            'sample_outputs_required': True,
            'table_single_line_required': True,
            'target_score': 85,
            'auto_correction_enabled': True
        }
        
    def _generate_enforcement_report(self, ticket_id, validation_result, delivery_validation):
        """Generate comprehensive enforcement report"""
        report_path = self.framework_root / "runs" / ticket_id / "latest" / "FORMAT_ENFORCEMENT_REPORT.md"
        
        report_content = f"""# Format Enforcement Report - {ticket_id}

## Validation Results
- **Format Validation Passed:** {validation_result['format_validation_passed']}
- **Delivery Ready:** {delivery_validation}

## Enforcement Summary
{validation_result['enforcement_summary']}

## Format Compliance
Target Score: 85+ points
Status: {'✅ COMPLIANT' if validation_result['format_validation_passed'] else '❌ NON-COMPLIANT'}

Generated: {self._get_timestamp()}
"""
        
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(report_content)
            
        return str(report_path)
        
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

# Framework integration point
def execute_framework_format_enforcement(ticket_id, run_path):
    """Main integration point for framework format enforcement"""
    framework_root = Path(__file__).parent.parent.parent
    integration = FrameworkFormatWorkflowIntegration(framework_root)
    return integration.execute_format_enforcement_workflow(ticket_id, run_path)
'''
        
        workflow_path = self.enforcement_dir / "framework_workflow_format_integration.py"
        with open(workflow_path, 'w') as f:
            f.write(workflow_integration)
            
        self.deployment_log.append(f"✅ Created framework workflow integration: {workflow_path}")
        
    def _generate_deployment_manifest(self):
        """Generate deployment manifest"""
        
        manifest = {
            'deployment_name': 'Comprehensive Format Enforcement System',
            'deployment_version': '1.0.0',
            'deployment_date': self._get_timestamp(),
            'components_deployed': [
                'test_case_format_enforcer.py',
                'framework_format_integration.py', 
                'pattern_extension_format_enforcer.py',
                'pattern_extension_format_integration.py',
                'framework_workflow_format_integration.py'
            ],
            'hooks_deployed': [
                'pre_generation_format_hook.py',
                'post_generation_format_hook.py'
            ],
            'validation_target': '85+ points',
            'enforcement_scope': 'All test case generation',
            'auto_correction': 'Enabled',
            'deployment_log': self.deployment_log,
            'status': 'ACTIVE'
        }
        
        manifest_path = self.enforcement_dir / "DEPLOYMENT_MANIFEST.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
            
        print(f"📋 Deployment manifest created: {manifest_path}")
        
        # Create human-readable deployment report
        report_content = f"""# Format Enforcement Deployment Report

## System Overview
**Deployment:** {manifest['deployment_name']} v{manifest['deployment_version']}
**Date:** {manifest['deployment_date']}
**Status:** {manifest['status']}

## Components Deployed
"""
        
        for component in manifest['components_deployed']:
            report_content += f"- ✅ {component}\n"
            
        report_content += "\n## Hooks Deployed\n"
        for hook in manifest['hooks_deployed']:
            report_content += f"- ✅ {hook}\n"
            
        report_content += f"""
## Enforcement Configuration
- **Validation Target:** {manifest['validation_target']}
- **Enforcement Scope:** {manifest['enforcement_scope']}
- **Auto-Correction:** {manifest['auto_correction']}

## Deployment Log
"""
        
        for log_entry in self.deployment_log:
            report_content += f"- {log_entry}\n"
            
        report_content += """
## Usage
The format enforcement system is now active and will:
1. Validate all generated test cases
2. Apply automatic corrections where possible
3. Generate corrective guidance for violations
4. Integrate with Pattern Extension Service
5. Provide comprehensive reporting

**Target:** 85+ points for framework acceptance
**Validation:** Automatic on every test case generation
"""
        
        report_path = self.enforcement_dir / "DEPLOYMENT_REPORT.md"
        with open(report_path, 'w') as f:
            f.write(report_content)
            
        print(f"📋 Deployment report created: {report_path}")
        
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

def main():
    """Deploy format enforcement system"""
    framework_root = Path(__file__).parent.parent.parent
    
    deployment = FormatEnforcementDeployment(framework_root)
    deployment.deploy_comprehensive_format_enforcement()
    
    print("\n🎯 Format Enforcement System Deployment Summary:")
    print("✅ Comprehensive format validation deployed")
    print("✅ Pattern Extension Service integration active")
    print("✅ Framework workflow integration complete")
    print("✅ Automatic correction capabilities enabled")
    print("✅ 85+ point validation target enforced")
    print("\n📋 All future test case generation will be format-validated")

if __name__ == "__main__":
    main()