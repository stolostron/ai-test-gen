#!/usr/bin/env python3
"""
Z-Stream Analysis Comprehensive Logging Hook
Claude Code Native Hook System Integration

This hook automatically captures all tool executions and analysis operations
for complete observability of the z-stream-analysis pipeline failure analysis.
"""

import json
import os
import sys
import time
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List
import hashlib
import subprocess


class ZStreamLoggingHook:
    """
    Comprehensive logging hook for z-stream-analysis framework
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.runs_dir = self.base_dir / "runs"
        self.runs_dir.mkdir(exist_ok=True)
        
        # Current run tracking
        self.current_run_file = self.base_dir / "current_run_monitor.json"
        self.config_file = self.base_dir / "framework_config.json"
        
        # Load configuration
        self.config = self._load_config()
        
        # Sensitive data patterns for security
        self.sensitive_patterns = [
            r'token=[^&\s]+',
            r'password=[^&\s]+',
            r'Authorization:\s*Bearer\s+[^\s]+',
            r'oc login.*--token=[^\s]+',
            r'export.*TOKEN.*=.*',
            r'[A-Za-z0-9]{32,}',  # Potential API keys
            r'--token\s+[^\s]+',
            r'--password\s+[^\s]+',
        ]
        
    def _load_config(self) -> Dict[str, Any]:
        """Load logging configuration"""
        default_config = {
            "enabled": True,
            "log_level": "INFO",
            "auto_start": True,
            "real_time_monitoring": True,
            "security": {
                "mask_credentials": True,
                "audit_sensitive_data": True
            },
            "performance": {
                "track_timing": True,
                "track_memory": False,
                "async_logging": True
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except:
                pass
        
        # Create default config
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def _get_current_run_id(self) -> Optional[str]:
        """Get the current active run ID"""
        if self.current_run_file.exists():
            try:
                with open(self.current_run_file, 'r') as f:
                    data = json.load(f)
                    return data.get('run_id')
            except:
                pass
        return None
    
    def _generate_run_id(self, jenkins_url: Optional[str] = None) -> str:
        """Generate a new run ID based on context"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        
        if jenkins_url:
            # Extract pipeline info from Jenkins URL
            pipeline_id = self._extract_pipeline_id(jenkins_url)
            return f"{pipeline_id}_{timestamp}"
        else:
            # Fallback to generic run ID
            return f"zstream_analysis_{timestamp}"
    
    def _extract_pipeline_id(self, jenkins_url: str) -> str:
        """Extract pipeline identifier from Jenkins URL"""
        # Try to extract job name and build number
        patterns = [
            r'/job/([^/]+)/(\d+)/?$',  # Standard Jenkins pattern
            r'/job/([^/]+)/job/([^/]+)/(\d+)/?$',  # Nested job pattern
        ]
        
        for pattern in patterns:
            match = re.search(pattern, jenkins_url)
            if match:
                if len(match.groups()) == 2:
                    job, build = match.groups()
                    return f"{job}_{build}"
                elif len(match.groups()) == 3:
                    parent, job, build = match.groups()
                    return f"{parent}_{job}_{build}"
        
        # Fallback: use hash of URL
        url_hash = hashlib.md5(jenkins_url.encode()).hexdigest()[:8]
        return f"jenkins_{url_hash}"
    
    def _start_new_run(self, jenkins_url: Optional[str] = None) -> str:
        """Start a new logging run"""
        run_id = self._generate_run_id(jenkins_url)
        
        # Create run directory structure
        run_dir = self.runs_dir / run_id
        run_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        for subdir in ['services', 'stages', 'tools', 'context', 'security']:
            (run_dir / subdir).mkdir(exist_ok=True)
        
        # Initialize run tracking
        run_data = {
            "run_id": run_id,
            "jenkins_url": jenkins_url,
            "start_time": datetime.now(timezone.utc).isoformat(),
            "status": "active",
            "log_directory": str(run_dir)
        }
        
        with open(self.current_run_file, 'w') as f:
            json.dump(run_data, f, indent=2)
        
        # Initialize master log
        self._log_entry(run_dir, {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "run_id": run_id,
            "jenkins_url": jenkins_url,
            "log_level": "INFO",
            "component": "LOGGING_SYSTEM",
            "stage": "initialization",
            "action": "start_run",
            "message": f"Started new z-stream-analysis logging run: {run_id}",
            "data": run_data
        })
        
        return run_id
    
    def _mask_sensitive_data(self, text: str) -> tuple[str, bool]:
        """Mask sensitive data in text"""
        if not self.config.get('security', {}).get('mask_credentials', True):
            return text, False
        
        masked_text = text
        had_sensitive = False
        
        for pattern in self.sensitive_patterns:
            if re.search(pattern, masked_text, re.IGNORECASE):
                had_sensitive = True
                masked_text = re.sub(pattern, '[MASKED]', masked_text, flags=re.IGNORECASE)
        
        return masked_text, had_sensitive
    
    def _log_entry(self, run_dir: Path, entry: Dict[str, Any]):
        """Write log entry to appropriate files"""
        timestamp = entry.get('timestamp', datetime.now(timezone.utc).isoformat())
        
        # Mask sensitive data
        if 'command' in entry:
            entry['command'], had_sensitive = self._mask_sensitive_data(entry['command'])
            if had_sensitive:
                entry['security'] = entry.get('security', {})
                entry['security']['credentials_masked'] = True
        
        if 'output' in entry and entry['output']:
            entry['output'], had_sensitive = self._mask_sensitive_data(str(entry['output']))
            if had_sensitive:
                entry['security'] = entry.get('security', {})
                entry['security']['credentials_masked'] = True
        
        # Write to master log
        master_log = run_dir / "master_log.jsonl"
        with open(master_log, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        # Write to component-specific logs
        component = entry.get('component', 'general').lower()
        stage = entry.get('stage', 'general')
        
        # Service-specific logs
        if 'service' in component or 'intelligence' in component:
            service_log = run_dir / "services" / f"{component}.jsonl"
            with open(service_log, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        
        # Stage-specific logs
        if stage and stage != 'general':
            stage_log = run_dir / "stages" / f"stage_{stage}.jsonl"
            with open(stage_log, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        
        # Tool-specific logs
        if 'tool' in entry:
            tool = entry['tool']
            tool_log = run_dir / "tools" / f"{tool}_commands.jsonl"
            with open(tool_log, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        
        # Error log
        if entry.get('log_level') in ['ERROR', 'CRITICAL']:
            error_log = run_dir / "error_log.jsonl"
            with open(error_log, 'a') as f:
                f.write(json.dumps(entry) + '\n')
    
    def handle_tool_execution(self, stage: str, tool_data: Dict[str, Any]):
        """Handle tool execution logging"""
        if not self.config.get('enabled', True):
            return
        
        run_id = self._get_current_run_id()
        if not run_id:
            # Auto-start run if not already active
            jenkins_url = tool_data.get('jenkins_url')
            run_id = self._start_new_run(jenkins_url)
        
        run_dir = self.runs_dir / run_id
        if not run_dir.exists():
            return
        
        # Determine component from context
        component = "GENERAL"
        if 'jenkins' in str(tool_data.get('command', '')).lower():
            component = "JENKINS_INTELLIGENCE_SERVICE"
        elif 'curl' in str(tool_data.get('command', '')).lower():
            if 'jenkins' in str(tool_data.get('command', '')).lower():
                component = "JENKINS_INTELLIGENCE_SERVICE"
            else:
                component = "INVESTIGATION_INTELLIGENCE_SERVICE"
        
        # Create log entry
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "run_id": run_id,
            "log_level": "INFO",
            "component": component,
            "stage": stage,
            "action": "tool_execution",
            **tool_data
        }
        
        self._log_entry(run_dir, entry)
    
    def handle_analysis_event(self, event_type: str, event_data: Dict[str, Any]):
        """Handle analysis lifecycle events"""
        if not self.config.get('enabled', True):
            return
        
        run_id = self._get_current_run_id()
        
        if event_type == "analysis_start":
            # Start new run
            jenkins_url = event_data.get('jenkins_url')
            run_id = self._start_new_run(jenkins_url)
        
        if not run_id:
            return
        
        run_dir = self.runs_dir / run_id
        if not run_dir.exists():
            return
        
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "run_id": run_id,
            "log_level": "INFO",
            "component": "ANALYSIS_FRAMEWORK",
            "stage": event_type,
            "action": event_type,
            **event_data
        }
        
        self._log_entry(run_dir, entry)
        
        if event_type == "analysis_complete":
            # Finalize run
            self._finalize_run(run_id)
    
    def _finalize_run(self, run_id: str):
        """Finalize logging run"""
        run_dir = self.runs_dir / run_id
        
        # Update run status
        if self.current_run_file.exists():
            try:
                with open(self.current_run_file, 'r') as f:
                    data = json.load(f)
                
                data.update({
                    "status": "completed",
                    "end_time": datetime.now(timezone.utc).isoformat()
                })
                
                with open(self.current_run_file, 'w') as f:
                    json.dump(data, f, indent=2)
            except:
                pass
        
        # Generate execution summary
        self._generate_execution_summary(run_dir)
    
    def _generate_execution_summary(self, run_dir: Path):
        """Generate execution summary for completed run"""
        master_log = run_dir / "master_log.jsonl"
        if not master_log.exists():
            return
        
        summary = {
            "run_id": run_dir.name,
            "start_time": None,
            "end_time": None,
            "duration_seconds": 0,
            "total_entries": 0,
            "components": {},
            "tools_used": {},
            "stages": {},
            "errors": 0,
            "performance": {
                "avg_tool_duration_ms": 0,
                "total_tool_executions": 0
            }
        }
        
        entries = []
        start_time = None
        end_time = None
        tool_durations = []
        
        try:
            with open(master_log, 'r') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    entries.append(entry)
                    
                    timestamp = entry.get('timestamp')
                    if timestamp:
                        if not start_time:
                            start_time = timestamp
                        end_time = timestamp
                    
                    # Count components
                    component = entry.get('component', 'Unknown')
                    summary['components'][component] = summary['components'].get(component, 0) + 1
                    
                    # Count tools
                    tool = entry.get('tool')
                    if tool:
                        summary['tools_used'][tool] = summary['tools_used'].get(tool, 0) + 1
                        summary['performance']['total_tool_executions'] += 1
                        
                        duration = entry.get('duration_ms')
                        if duration:
                            tool_durations.append(duration)
                    
                    # Count stages
                    stage = entry.get('stage')
                    if stage:
                        summary['stages'][stage] = summary['stages'].get(stage, 0) + 1
                    
                    # Count errors
                    if entry.get('log_level') in ['ERROR', 'CRITICAL']:
                        summary['errors'] += 1
        
        except Exception as e:
            print(f"Error generating summary: {e}")
            return
        
        # Calculate summary statistics
        summary['total_entries'] = len(entries)
        summary['start_time'] = start_time
        summary['end_time'] = end_time
        
        if start_time and end_time:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            summary['duration_seconds'] = (end_dt - start_dt).total_seconds()
        
        if tool_durations:
            summary['performance']['avg_tool_duration_ms'] = sum(tool_durations) / len(tool_durations)
        
        # Write summary
        summary_file = run_dir / "execution_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)


def main():
    """Main hook entry point"""
    if len(sys.argv) < 3 or sys.argv[1] != '--stage':
        print("Usage: comprehensive_logging_hook.py --stage <stage_name> [additional_args]")
        sys.exit(1)
    
    stage = sys.argv[2]
    hook = ZStreamLoggingHook()
    
    # Parse additional arguments and environment variables
    tool_data = {}
    
    # Get data from environment variables (Claude Code provides these)
    tool_data['tool'] = os.environ.get('CLAUDE_TOOL_NAME', 'unknown')
    tool_data['command'] = os.environ.get('CLAUDE_COMMAND', '')
    tool_data['jenkins_url'] = os.environ.get('CLAUDE_JENKINS_URL', '')
    
    # Parse command line arguments for additional data
    if len(sys.argv) > 3:
        for arg in sys.argv[3:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                tool_data[key] = value
    
    # Handle different hook stages
    if stage in ['pre-tool', 'post-tool']:
        hook.handle_tool_execution(stage, tool_data)
    elif stage in ['analysis-start', 'analysis-complete', 'service-start', 'service-complete']:
        hook.handle_analysis_event(stage, tool_data)
    else:
        # Generic event handling
        hook.handle_tool_execution(stage, tool_data)


if __name__ == "__main__":
    main()