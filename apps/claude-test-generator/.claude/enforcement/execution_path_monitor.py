#!/usr/bin/env python3
"""
Execution Path Monitor and Blocker

Monitors framework execution path in real-time and blocks any attempts to bypass
the mandatory 6-phase workflow. Prevents shortcuts, skipped phases, and quality
control circumvention.
"""

import json
import os
import sys
import threading
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Any

class ExecutionPathMonitor:
    """Monitors and enforces proper execution path"""
    
    def __init__(self):
        self.monitoring_active = False
        self.execution_violations = []
        self.current_execution_state = {
            "phase": None,
            "agents_active": set(),
            "tools_used": [],
            "files_created": [],
            "bypasses_detected": []
        }
        self.allowed_execution_patterns = self._define_allowed_patterns()
        self.blocked_patterns = self._define_blocked_patterns()
        self.monitoring_thread = None
        self.violation_threshold = 3
        
    def _define_allowed_patterns(self) -> Dict:
        """Define allowed execution patterns"""
        return {
            "mandatory_tool_sequence": [
                "TodoWrite",  # Phase tracking
                "Bash",       # Environment validation 
                "WebFetch",   # Information gathering
                "Read",       # File analysis
                "Write"       # Final deliverable creation
            ],
            "mandatory_phase_sequence": [
                "phase_0",    # JIRA and Environment
                "phase_1",    # Enhanced parallel (A+D)
                "phase_2",    # Context-aware parallel (B+C)
                "phase_2_5",  # QE Intelligence
                "phase_3",    # AI Strategic Analysis
                "phase_4",    # Pattern-based generation
                "phase_5"     # Cleanup and finalization
            ],
            "agent_coordination_patterns": {
                "phase_1": ["agent_a", "agent_d"],
                "phase_2": ["agent_b", "agent_c"]
            }
        }
    
    def _define_blocked_patterns(self) -> Dict:
        """Define blocked execution patterns"""
        return {
            "manual_file_creation": [
                "direct_write_without_framework",
                "root_directory_file_creation", 
                "bypass_run_directory_structure"
            ],
            "phase_skipping": [
                "skip_jira_analysis",
                "skip_environment_validation",
                "skip_agent_coordination",
                "skip_quality_checkpoints"
            ],
            "quality_bypasses": [
                "manual_html_tag_insertion",
                "bypass_format_enforcement",
                "skip_citation_validation",
                "bypass_pattern_validation"
            ],
            "framework_circumvention": [
                "direct_tool_calls_without_coordination",
                "bypass_observability_integration",
                "skip_metadata_generation",
                "manual_execution_without_framework"
            ]
        }
    
    def start_monitoring(self, execution_context: Dict) -> None:
        """Start execution path monitoring"""
        
        self.monitoring_active = True
        self.execution_context = execution_context
        
        print("🔍 **EXECUTION PATH MONITORING ACTIVE**")
        print("🛡️ Framework bypass prevention enabled")
        print("📊 Real-time execution validation started")
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop, 
            daemon=True
        )
        self.monitoring_thread.start()
        
    def _monitoring_loop(self) -> None:
        """Main monitoring loop"""
        
        while self.monitoring_active:
            try:
                # Check for execution violations
                self._check_execution_path()
                
                # Check for file system violations
                self._check_file_system_violations()
                
                # Check for quality bypasses
                self._check_quality_bypasses()
                
                # Check for framework circumvention
                self._check_framework_circumvention()
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                self._log_monitoring_error(e)
    
    def _check_execution_path(self) -> None:
        """Check execution path compliance"""
        
        # Detect manual file creation outside framework
        for item in Path(".").iterdir():
            if item.is_file() and item.suffix in [".md", ".json"]:
                if "ACM-" in item.name and item.name not in self.current_execution_state["files_created"]:
                    self._record_violation("unauthorized_file_creation", {
                        "file": str(item),
                        "location": "root_directory",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
        
        # Check for run directory violations
        runs_dir = Path("runs")
        if runs_dir.exists():
            for ticket_dir in runs_dir.iterdir():
                if ticket_dir.is_dir() and ticket_dir.name.startswith("ACM-"):
                    # Check for files created outside proper run structure
                    for item in ticket_dir.iterdir():
                        if item.is_file() and item.suffix in [".md", ".json"]:
                            self._record_violation("improper_run_structure", {
                                "file": str(item),
                                "should_be_in": "timestamped_run_directory",
                                "timestamp": datetime.now(timezone.utc).isoformat()
                            })
    
    def _check_file_system_violations(self) -> None:
        """Check for file system violations"""
        
        # Check for unauthorized directories
        unauthorized_dirs = []
        for item in Path(".").iterdir():
            if item.is_dir() and item.name.startswith("ACM-"):
                unauthorized_dirs.append(str(item))
        
        if unauthorized_dirs:
            self._record_violation("unauthorized_directory_creation", {
                "directories": unauthorized_dirs,
                "violation": "ticket_directories_in_root",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        
        # Check for files in wrong locations
        wrong_location_files = []
        for item in Path(".").iterdir():
            if item.is_file() and any(pattern in item.name.lower() for pattern in ["test", "analysis", "plan"]):
                wrong_location_files.append(str(item))
        
        if wrong_location_files:
            self._record_violation("files_in_wrong_location", {
                "files": wrong_location_files,
                "violation": "deliverables_outside_run_directory",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
    
    def _check_quality_bypasses(self) -> None:
        """Check for quality control bypasses"""
        
        # Check for HTML tag violations in recent files
        recent_files = self._get_recent_markdown_files()
        
        for file_path in recent_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Check for HTML tags
                if "<br>" in content or "</" in content:
                    self._record_violation("html_tag_violation", {
                        "file": str(file_path),
                        "violation": "html_tags_present",
                        "tags_found": self._extract_html_tags(content),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                
                # Check for improper structure
                if not self._validate_markdown_structure(content):
                    self._record_violation("structure_violation", {
                        "file": str(file_path),
                        "violation": "improper_test_case_structure",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                    
            except Exception as e:
                # File might be in use, skip for now
                pass
    
    def _check_framework_circumvention(self) -> None:
        """Check for framework circumvention attempts"""
        
        # Check if metadata files are missing (indicates framework bypass)
        runs_dir = Path("runs")
        if runs_dir.exists():
            for ticket_dir in runs_dir.iterdir():
                if ticket_dir.is_dir() and ticket_dir.name.startswith("ACM-"):
                    for run_dir in ticket_dir.iterdir():
                        if run_dir.is_dir() and "-" in run_dir.name:
                            metadata_file = run_dir / "run-metadata.json"
                            if not metadata_file.exists():
                                # Check if there are deliverable files without metadata
                                deliverable_files = list(run_dir.glob("*.md"))
                                if deliverable_files:
                                    self._record_violation("framework_bypass", {
                                        "run_directory": str(run_dir),
                                        "violation": "deliverables_without_metadata",
                                        "files": [str(f) for f in deliverable_files],
                                        "timestamp": datetime.now(timezone.utc).isoformat()
                                    })
    
    def _get_recent_markdown_files(self) -> List[Path]:
        """Get recently modified markdown files"""
        
        recent_files = []
        cutoff_time = time.time() - 300  # 5 minutes ago
        
        # Check runs directory
        runs_dir = Path("runs")
        if runs_dir.exists():
            for md_file in runs_dir.rglob("*.md"):
                if md_file.stat().st_mtime > cutoff_time:
                    recent_files.append(md_file)
        
        # Check root directory
        for md_file in Path(".").glob("*.md"):
            if md_file.stat().st_mtime > cutoff_time:
                recent_files.append(md_file)
        
        return recent_files
    
    def _extract_html_tags(self, content: str) -> List[str]:
        """Extract HTML tags from content"""
        
        import re
        html_pattern = r'<[^>]+>'
        tags = re.findall(html_pattern, content)
        return list(set(tags))  # Remove duplicates
    
    def _validate_markdown_structure(self, content: str) -> bool:
        """Validate markdown structure for test cases"""
        
        # Check for proper test case structure
        required_patterns = [
            "## Test Case",
            "### Description", 
            "### Setup",
            "### Test Table"
        ]
        
        # At least some structure should be present
        structure_count = sum(1 for pattern in required_patterns if pattern in content)
        return structure_count >= 2  # At least some structure
    
    def _record_violation(self, violation_type: str, details: Dict) -> None:
        """Record an execution violation"""
        
        violation = {
            "type": violation_type,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": self._assess_violation_severity(violation_type)
        }
        
        self.execution_violations.append(violation)
        self.current_execution_state["bypasses_detected"].append(violation_type)
        
        # Log violation
        print(f"🚨 **EXECUTION VIOLATION DETECTED**: {violation_type}")
        
        # Check if we should trigger emergency stop
        if violation["severity"] == "critical" or len(self.execution_violations) >= self.violation_threshold:
            self._trigger_emergency_stop(violation)
    
    def _assess_violation_severity(self, violation_type: str) -> str:
        """Assess violation severity"""
        
        critical_violations = [
            "framework_bypass",
            "unauthorized_file_creation",
            "phase_skipping",
            "quality_control_bypass"
        ]
        
        high_violations = [
            "html_tag_violation",
            "structure_violation", 
            "improper_run_structure"
        ]
        
        if violation_type in critical_violations:
            return "critical"
        elif violation_type in high_violations:
            return "high"
        else:
            return "medium"
    
    def _trigger_emergency_stop(self, violation: Dict) -> None:
        """Trigger emergency execution stop"""
        
        print("🚨 **EMERGENCY EXECUTION STOP**")
        print(f"🛑 Critical violation detected: {violation['type']}")
        print("🔒 Framework execution halted to prevent quality degradation")
        
        # Create emergency log
        emergency_log = {
            "event": "emergency_stop",
            "trigger_violation": violation,
            "all_violations": self.execution_violations,
            "execution_state": self.current_execution_state,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Write emergency log
        log_file = Path(".claude/logs/emergency-stop.json")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(log_file, 'w') as f:
                json.dump(emergency_log, f, indent=2)
        except Exception as e:
            print(f"Failed to write emergency log: {e}")
        
        # Stop monitoring
        self.monitoring_active = False
        
        # Raise exception to halt execution
        raise RuntimeError(f"Emergency stop triggered: {violation['type']}")
    
    def _log_monitoring_error(self, error: Exception) -> None:
        """Log monitoring error"""
        
        error_log = {
            "error": str(error),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Write to error log
        error_file = Path(".claude/logs/monitoring-errors.json")
        error_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            existing_errors = []
            if error_file.exists():
                with open(error_file, 'r') as f:
                    existing_errors = json.load(f)
            
            existing_errors.append(error_log)
            
            with open(error_file, 'w') as f:
                json.dump(existing_errors, f, indent=2)
                
        except Exception:
            pass  # Avoid infinite error loops
    
    def record_tool_usage(self, tool_name: str, parameters: Dict) -> None:
        """Record tool usage for monitoring"""
        
        tool_record = {
            "tool": tool_name,
            "parameters": parameters,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        self.current_execution_state["tools_used"].append(tool_record)
        
        # Check for suspicious tool usage patterns
        if tool_name == "Write" and not self._validate_write_operation(parameters):
            self._record_violation("unauthorized_write_operation", {
                "tool": tool_name,
                "parameters": parameters,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
    
    def _validate_write_operation(self, parameters: Dict) -> bool:
        """Validate write operation"""
        
        file_path = parameters.get("file_path", "")
        
        # Must be in runs directory
        if "runs/" not in file_path:
            return False
        
        # Must be in proper run structure
        if not any(pattern in file_path for pattern in ["Test-Cases.md", "Complete-Analysis.md", "run-metadata.json"]):
            return False
        
        return True
    
    def record_phase_transition(self, phase: str) -> None:
        """Record phase transition"""
        
        self.current_execution_state["phase"] = phase
        
        # Validate phase sequence
        allowed_phases = self.allowed_execution_patterns["mandatory_phase_sequence"]
        if phase not in allowed_phases:
            self._record_violation("invalid_phase", {
                "phase": phase,
                "allowed_phases": allowed_phases,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
    
    def stop_monitoring(self) -> Dict:
        """Stop monitoring and return report"""
        
        self.monitoring_active = False
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        report = {
            "monitoring_session": {
                "start_time": getattr(self, 'start_time', None),
                "end_time": datetime.now(timezone.utc).isoformat(),
                "violations_detected": len(self.execution_violations),
                "execution_state": self.current_execution_state
            },
            "violations": self.execution_violations,
            "compliance_status": "compliant" if not self.execution_violations else "violations_detected"
        }
        
        print("📊 **EXECUTION MONITORING COMPLETE**")
        print(f"🔍 Violations detected: {len(self.execution_violations)}")
        
        return report


# Global monitor instance
_execution_monitor = None

def get_execution_monitor() -> ExecutionPathMonitor:
    """Get global execution monitor"""
    global _execution_monitor
    
    if _execution_monitor is None:
        _execution_monitor = ExecutionPathMonitor()
    
    return _execution_monitor

def start_execution_monitoring(execution_context: Dict) -> None:
    """Start execution path monitoring"""
    monitor = get_execution_monitor()
    monitor.start_monitoring(execution_context)

def record_tool_usage(tool_name: str, parameters: Dict) -> None:
    """Record tool usage"""
    monitor = get_execution_monitor()
    monitor.record_tool_usage(tool_name, parameters)

def record_phase_transition(phase: str) -> None:
    """Record phase transition"""
    monitor = get_execution_monitor()
    monitor.record_phase_transition(phase)

def stop_execution_monitoring() -> Dict:
    """Stop monitoring and get report"""
    monitor = get_execution_monitor()
    return monitor.stop_monitoring()


if __name__ == "__main__":
    # Test monitoring system
    monitor = ExecutionPathMonitor()
    
    test_context = {
        "jira_ticket": "ACM-TEST-123",
        "start_time": datetime.now(timezone.utc).isoformat()
    }
    
    print("🧪 Testing execution path monitoring...")
    
    try:
        monitor.start_monitoring(test_context)
        
        # Simulate some operations
        monitor.record_tool_usage("TodoWrite", {"todos": []})
        monitor.record_phase_transition("phase_0")
        
        time.sleep(3)
        
        report = monitor.stop_monitoring()
        print(f"✅ Monitoring test completed")
        print(f"📊 Final report: {json.dumps(report, indent=2)}")
        
    except Exception as e:
        print(f"❌ Monitoring test failed: {e}")
        sys.exit(1)