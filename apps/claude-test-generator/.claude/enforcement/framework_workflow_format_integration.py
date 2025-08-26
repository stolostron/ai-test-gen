#!/usr/bin/env python3
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
Target Score: target compliances
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
