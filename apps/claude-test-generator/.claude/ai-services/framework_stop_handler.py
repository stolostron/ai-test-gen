#!/usr/bin/env python3
"""
Framework Stop Handler for insufficient information scenarios
Provides graceful stopping and user reporting when data is insufficient
"""

import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class StopReport:
    """Report generated when framework stops due to insufficient information"""
    jira_id: str
    score: float
    status: str
    timestamp: str
    missing_critical: List[str]
    missing_optional: List[str]
    recommendations: List[str]
    jira_update_suggestions: List[str]
    collected_data_summary: Dict[str, bool]
    can_force_proceed: bool
    
    def to_markdown(self) -> str:
        """Convert report to user-friendly markdown format"""
        md_lines = [
            "# 🚨 FRAMEWORK STOP: Insufficient Information",
            "",
            f"**JIRA Ticket**: {self.jira_id}",
            f"**Information Score**: {self.score:.2f} / 1.00 (Minimum required: 0.75)",
            f"**Timestamp**: {self.timestamp}",
            "",
            "## ❌ Missing Critical Information:",
            ""
        ]
        
        if self.missing_critical:
            for i, item in enumerate(self.missing_critical, 1):
                md_lines.append(f"{i}. **{item}**")
        else:
            md_lines.append("*No critical information missing*")
            
        md_lines.extend([
            "",
            "## ⚠️ Missing Optional Information:",
            ""
        ])
        
        if self.missing_optional:
            for item in self.missing_optional:
                md_lines.append(f"- {item}")
        else:
            md_lines.append("*No optional information missing*")
            
        md_lines.extend([
            "",
            "## 📝 Recommended Actions:",
            ""
        ])
        
        for i, rec in enumerate(self.recommendations, 1):
            md_lines.append(f"{i}. {rec}")
            
        md_lines.extend([
            "",
            "## 💡 Suggested JIRA Updates:",
            "",
            "```"
        ])
        
        for suggestion in self.jira_update_suggestions:
            md_lines.append(suggestion)
            
        md_lines.extend([
            "```",
            "",
            "## 📊 Information Collection Summary:",
            ""
        ])
        
        for category, present in self.collected_data_summary.items():
            status = "✅" if present else "❌"
            md_lines.append(f"- {status} {category.replace('_', ' ').title()}")
            
        if self.can_force_proceed:
            md_lines.extend([
                "",
                "## 🔧 Alternative Options:",
                "",
                "1. **Update JIRA ticket** with missing information and re-run",
                "2. **Force proceed** with `--force` flag (test coverage will be limited)",
                "3. **Provide additional context** via `--context-file` option"
            ])
            
        return "\n".join(md_lines)


class FrameworkStopHandler:
    """
    Handles framework stopping when information is insufficient
    Provides detailed reporting and recovery suggestions
    """
    
    def __init__(self, run_dir: Optional[str] = None):
        """Initialize the stop handler"""
        self.run_dir = run_dir or os.getcwd()
        self.reports_dir = os.path.join(self.run_dir, "insufficient_info_reports")
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def trigger_stop(self, jira_id: str, collected_data: Dict, 
                    score: float, missing_info: Dict) -> StopReport:
        """
        Trigger framework stop and generate comprehensive report
        
        Args:
            jira_id: JIRA ticket ID
            collected_data: All collected data
            score: Sufficiency score
            missing_info: Dict with 'critical' and 'optional' missing items
            
        Returns:
            StopReport with all details
        """
        logger.error(f"Triggering framework stop for {jira_id}: "
                    f"Insufficient information (score: {score:.2f})")
        
        # Analyze what was collected
        data_summary = self._analyze_collected_data(collected_data)
        
        # Generate JIRA update suggestions
        jira_suggestions = self._generate_jira_suggestions(
            missing_info.get('critical', []),
            missing_info.get('optional', []),
            collected_data
        )
        
        # Generate recommendations
        recommendations = self._generate_detailed_recommendations(
            missing_info, collected_data, score
        )
        
        # Create report
        report = StopReport(
            jira_id=jira_id,
            score=score,
            status="INSUFFICIENT_INFORMATION",
            timestamp=datetime.now().isoformat(),
            missing_critical=missing_info.get('critical', []),
            missing_optional=missing_info.get('optional', []),
            recommendations=recommendations,
            jira_update_suggestions=jira_suggestions,
            collected_data_summary=data_summary,
            can_force_proceed=(score >= 0.60)  # Can force if above fallback threshold
        )
        
        # Save report
        self._save_report(report)
        
        # Log summary
        logger.info(f"Stop report generated for {jira_id}: "
                   f"{len(report.missing_critical)} critical items missing")
        
        return report
    
    def _analyze_collected_data(self, data: Dict) -> Dict[str, bool]:
        """Analyze what information was successfully collected"""
        return {
            'jira_ticket_found': bool(data.get('jira_info')),
            'pr_references_found': bool(data.get('pr_references') or data.get('github_prs')),
            'subtasks_analyzed': bool(data.get('subtasks')),
            'linked_issues_analyzed': bool(data.get('linked_issues')),
            'comments_extracted': bool(data.get('comments')),
            'acceptance_criteria_found': bool(data.get('acceptance_criteria')),
            'technical_design_found': bool(data.get('technical_design')),
            'components_identified': bool(data.get('affected_components')),
            'environment_info_found': bool(data.get('environment_info')),
            'version_info_found': bool(data.get('target_version'))
        }
    
    def _generate_jira_suggestions(self, missing_critical: List[str], 
                                  missing_optional: List[str],
                                  collected_data: Dict) -> List[str]:
        """Generate specific JIRA ticket update suggestions"""
        suggestions = []
        
        # Header
        suggestions.extend([
            "## Suggested JIRA Ticket Updates",
            ""
        ])
        
        # Check for missing PRs
        if missing_critical and any('PR' in item or 'GitHub' in item for item in missing_critical):
            suggestions.extend([
                "## Implementation Details",
                "**GitHub PRs**:",
                "- PR #1234: [Brief description of changes]",
                "- PR #5678: [Additional changes]",
                "",
                "**Related Repositories**:",
                "- stolostron/console (UI changes)",
                "- stolostron/multicloud-operators-* (Backend changes)",
                ""
            ])
        
        # Check for missing acceptance criteria
        if missing_critical and any('acceptance' in item.lower() or 'criteria' in item.lower() 
               for item in missing_critical):
            suggestions.extend([
                "## Acceptance Criteria",
                "- [ ] Feature can perform [specific action]",
                "- [ ] User can [specific workflow]",
                "- [ ] Integration with [component] works correctly",
                "- [ ] Error handling for [scenario] displays appropriate message",
                ""
            ])
        
        # Check for missing technical design
        if missing_critical and any('design' in item.lower() or 'architecture' in item.lower() 
               for item in missing_critical):
            suggestions.extend([
                "## Technical Design",
                "**Architecture Overview**:",
                "[Brief description or link to design doc]",
                "",
                "**Key Components**:",
                "- Component A: [responsibility]",
                "- Component B: [responsibility]",
                "",
                "**API Changes**:",
                "- New endpoint: POST /api/v1/[resource]",
                "- Modified: GET /api/v1/[resource]/{id}",
                ""
            ])
        
        # Check for missing test scenarios
        if missing_optional and any('test' in item.lower() for item in missing_optional):
            suggestions.extend([
                "## Test Scenarios",
                "1. **Happy Path**: [Description]",
                "2. **Error Handling**: [Description]",
                "3. **Edge Cases**: [Description]",
                ""
            ])
        
        return suggestions
    
    def _generate_detailed_recommendations(self, missing_info: Dict,
                                         collected_data: Dict,
                                         score: float) -> List[str]:
        """Generate detailed recommendations for improving information"""
        recommendations = []
        
        # Primary recommendation based on score
        if score < 0.60:
            recommendations.append(
                "**Critical**: Information is severely insufficient. "
                "Major updates to JIRA ticket required before proceeding."
            )
        elif score < 0.75:
            recommendations.append(
                "**Important**: Additional information needed for comprehensive testing. "
                "Update JIRA ticket or provide supplementary documentation."
            )
        
        # PR-specific recommendations
        if not (collected_data.get('pr_references') or collected_data.get('github_prs')):
            recommendations.extend([
                "**Search for PRs**: Use `gh pr list --search \"ACM-XXXXX\"` in relevant repos",
                "**Check PR descriptions**: PRs often contain valuable implementation details",
                "**Link PRs to JIRA**: Add PR URLs to JIRA ticket description or comments"
            ])
        
        # Documentation recommendations
        if score < 0.75:
            recommendations.extend([
                "**Check documentation**: Search for feature in official docs",
                "**Review design documents**: Check for linked design docs or ADRs",
                "**Contact feature owner**: Reach out to assignee for clarification"
            ])
        
        # Alternative approaches
        recommendations.extend([
            "**Alternative**: Create initial test plan with placeholders for missing info",
            "**Alternative**: Focus on areas with sufficient information first"
        ])
        
        return recommendations
    
    def _save_report(self, report: StopReport):
        """Save stop report to file system"""
        # Save as JSON
        json_path = os.path.join(
            self.reports_dir, 
            f"{report.jira_id}_stop_report_{report.timestamp.replace(':', '-')}.json"
        )
        with open(json_path, 'w') as f:
            json.dump(asdict(report), f, indent=2)
        
        # Save as Markdown
        md_path = os.path.join(
            self.reports_dir,
            f"{report.jira_id}_stop_report_{report.timestamp.replace(':', '-')}.md"
        )
        with open(md_path, 'w') as f:
            f.write(report.to_markdown())
        
        # Save latest symlink
        latest_path = os.path.join(self.reports_dir, f"{report.jira_id}_latest.md")
        if os.path.exists(latest_path):
            os.remove(latest_path)
        os.symlink(os.path.basename(md_path), latest_path)
        
        logger.info(f"Stop report saved to: {md_path}")
    
    def get_latest_report(self, jira_id: str) -> Optional[StopReport]:
        """Retrieve the latest stop report for a JIRA ID"""
        latest_path = os.path.join(self.reports_dir, f"{jira_id}_latest.md")
        if not os.path.exists(latest_path):
            return None
            
        # Find the actual file
        actual_path = os.path.join(self.reports_dir, os.readlink(latest_path))
        json_path = actual_path.replace('.md', '.json')
        
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
                return StopReport(**data)
        
        return None


class InsufficientInformationError(Exception):
    """Exception raised when information is insufficient to proceed"""
    
    def __init__(self, report: StopReport):
        self.report = report
        super().__init__(f"Insufficient information for {report.jira_id}: "
                        f"Score {report.score:.2f} < 0.75 required")
