#!/usr/bin/env python3
"""
Z-Stream Analysis Real-Time Monitor
Live monitoring and dashboard for active pipeline analysis runs
"""

import json
import time
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
import threading
import os


class ZStreamRealtimeMonitor:
    """
    Real-time monitoring for z-stream-analysis logging system
    """
    
    def __init__(self, base_logging_dir: str = ".claude/logging"):
        self.base_dir = Path(base_logging_dir)
        self.current_run_file = self.base_dir / "current_run_monitor.json"
        self.refresh_interval = 2.0
        self.running = False
        
        if not self.base_dir.exists():
            raise ValueError(f"Logging directory does not exist: {base_logging_dir}")
    
    def get_current_run_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the currently active run"""
        if not self.current_run_file.exists():
            return None
        
        try:
            with open(self.current_run_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def get_run_status(self, run_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed status of a specific run"""
        run_dir = Path(run_info['log_directory'])
        master_log = run_dir / "master_log.jsonl"
        
        status = {
            "run_id": run_info['run_id'],
            "jenkins_url": run_info.get('jenkins_url'),
            "start_time": run_info['start_time'],
            "status": run_info['status'],
            "current_time": datetime.now(timezone.utc).isoformat(),
            "total_entries": 0,
            "latest_entries": [],
            "active_components": set(),
            "current_stage": "unknown",
            "errors": 0,
            "performance": {
                "entries_per_minute": 0,
                "avg_tool_duration_ms": 0,
                "active_tools": []
            }
        }
        
        if not master_log.exists():
            status["error"] = "Master log not found"
            return status
        
        # Read recent entries
        entries = []
        try:
            with open(master_log, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        entries.append(entry)
                    except:
                        continue
        except:
            status["error"] = "Could not read master log"
            return status
        
        status["total_entries"] = len(entries)
        
        # Get latest 10 entries
        status["latest_entries"] = entries[-10:] if len(entries) >= 10 else entries
        
        # Analyze recent activity
        recent_entries = entries[-50:] if len(entries) >= 50 else entries
        
        for entry in recent_entries:
            # Track active components
            component = entry.get('component')
            if component:
                status["active_components"].add(component)
            
            # Track current stage
            stage = entry.get('stage')
            if stage:
                status["current_stage"] = stage
            
            # Count errors
            if entry.get('log_level') in ['ERROR', 'CRITICAL']:
                status["errors"] += 1
        
        status["active_components"] = list(status["active_components"])
        
        # Calculate performance metrics
        if entries:
            start_time = datetime.fromisoformat(run_info['start_time'].replace('Z', '+00:00'))
            current_time = datetime.now(timezone.utc)
            duration_minutes = (current_time - start_time).total_seconds() / 60
            
            if duration_minutes > 0:
                status["performance"]["entries_per_minute"] = len(entries) / duration_minutes
        
        # Calculate average tool duration
        tool_durations = []
        active_tools = set()
        
        for entry in recent_entries:
            duration = entry.get('duration_ms')
            if duration:
                tool_durations.append(duration)
            
            tool = entry.get('tool')
            if tool:
                active_tools.add(tool)
        
        if tool_durations:
            status["performance"]["avg_tool_duration_ms"] = sum(tool_durations) / len(tool_durations)
        
        status["performance"]["active_tools"] = list(active_tools)
        
        return status
    
    def print_dashboard(self, status: Dict[str, Any]):
        """Print a real-time dashboard"""
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("=" * 80)
        print("🔍 Z-STREAM ANALYSIS REAL-TIME MONITOR")
        print("=" * 80)
        print()
        
        if "error" in status:
            print(f"❌ Error: {status['error']}")
            return
        
        # Run Information
        print(f"📋 Run ID: {status['run_id']}")
        print(f"🔗 Jenkins URL: {status.get('jenkins_url', 'N/A')}")
        print(f"⏰ Start Time: {status['start_time']}")
        print(f"📊 Status: {status['status'].upper()}")
        print()
        
        # Current Activity
        print("🚀 CURRENT ACTIVITY")
        print("-" * 40)
        print(f"Current Stage: {status['current_stage']}")
        print(f"Total Log Entries: {status['total_entries']}")
        print(f"Error Count: {status['errors']}")
        print()
        
        # Active Components
        print("🔧 ACTIVE COMPONENTS")
        print("-" * 40)
        for component in status["active_components"]:
            print(f"  • {component}")
        print()
        
        # Performance Metrics
        perf = status["performance"]
        print("📈 PERFORMANCE METRICS")
        print("-" * 40)
        print(f"Log Entries/Minute: {perf['entries_per_minute']:.1f}")
        print(f"Avg Tool Duration: {perf['avg_tool_duration_ms']:.1f}ms")
        print(f"Active Tools: {', '.join(perf['active_tools'])}")
        print()
        
        # Latest Activity
        print("📝 LATEST ACTIVITY (Last 5 entries)")
        print("-" * 40)
        latest = status["latest_entries"][-5:] if len(status["latest_entries"]) >= 5 else status["latest_entries"]
        
        for entry in latest:
            timestamp = entry.get('timestamp', '')[:19]  # Remove microseconds
            component = entry.get('component', 'UNKNOWN')[:20]  # Truncate long component names
            action = entry.get('action', 'unknown')[:30]  # Truncate long actions
            level = entry.get('log_level', 'INFO')
            
            level_icon = {
                'INFO': '✅',
                'WARN': '⚠️ ',
                'WARNING': '⚠️ ',
                'ERROR': '❌',
                'CRITICAL': '🚨'
            }.get(level, '📝')
            
            print(f"  {level_icon} {timestamp} | {component:<20} | {action}")
        
        print()
        print(f"🔄 Last Updated: {datetime.now().strftime('%H:%M:%S')}")
        print("Press Ctrl+C to stop monitoring")
    
    def monitor_current_run(self, dashboard: bool = True):
        """Monitor the currently active run"""
        self.running = True
        
        try:
            while self.running:
                run_info = self.get_current_run_info()
                
                if not run_info:
                    if dashboard:
                        os.system('clear' if os.name == 'posix' else 'cls')
                        print("=" * 80)
                        print("🔍 Z-STREAM ANALYSIS REAL-TIME MONITOR")
                        print("=" * 80)
                        print()
                        print("⏳ No active run detected. Waiting for analysis to start...")
                        print()
                        print(f"🔄 Last Checked: {datetime.now().strftime('%H:%M:%S')}")
                        print("Press Ctrl+C to stop monitoring")
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] No active run")
                else:
                    status = self.get_run_status(run_info)
                    
                    if dashboard:
                        self.print_dashboard(status)
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] {status['run_id']}: "
                             f"{status['total_entries']} entries, stage: {status['current_stage']}, "
                             f"errors: {status['errors']}")
                
                time.sleep(self.refresh_interval)
        
        except KeyboardInterrupt:
            print("\\n\\n🛑 Monitoring stopped by user")
            self.running = False
    
    def get_run_list(self) -> List[Dict[str, Any]]:
        """Get list of all available runs"""
        runs_dir = self.base_dir / "runs"
        if not runs_dir.exists():
            return []
        
        runs = []
        for run_dir in runs_dir.iterdir():
            if run_dir.is_dir():
                master_log = run_dir / "master_log.jsonl"
                summary_file = run_dir / "execution_summary.json"
                
                run_info = {
                    "run_id": run_dir.name,
                    "directory": str(run_dir),
                    "has_master_log": master_log.exists(),
                    "has_summary": summary_file.exists(),
                    "created": datetime.fromtimestamp(run_dir.stat().st_ctime).isoformat()
                }
                
                # Try to get basic info from master log
                if master_log.exists():
                    try:
                        with open(master_log, 'r') as f:
                            first_line = f.readline()
                            if first_line:
                                first_entry = json.loads(first_line.strip())
                                run_info["jenkins_url"] = first_entry.get('jenkins_url')
                                run_info["start_time"] = first_entry.get('timestamp')
                        
                        # Count total entries
                        with open(master_log, 'r') as f:
                            run_info["total_entries"] = sum(1 for _ in f)
                    except:
                        run_info["total_entries"] = 0
                
                runs.append(run_info)
        
        # Sort by creation time (newest first)
        runs.sort(key=lambda x: x["created"], reverse=True)
        return runs
    
    def export_current_status(self, output_file: str):
        """Export current status to file"""
        run_info = self.get_current_run_info()
        
        if not run_info:
            status = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "active_run": None,
                "message": "No active run detected"
            }
        else:
            status = self.get_run_status(run_info)
            status["timestamp"] = datetime.now(timezone.utc).isoformat()
        
        with open(output_file, 'w') as f:
            json.dump(status, f, indent=2)
        
        print(f"Status exported to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Z-Stream Analysis Real-Time Monitor")
    parser.add_argument("--base-dir", default=".claude/logging", 
                       help="Base logging directory")
    parser.add_argument("--dashboard", action="store_true", 
                       help="Show interactive dashboard")
    parser.add_argument("--current", action="store_true", 
                       help="Monitor current active run")
    parser.add_argument("--list", action="store_true", 
                       help="List all available runs")
    parser.add_argument("--export", help="Export current status to file")
    parser.add_argument("--refresh", type=float, default=2.0, 
                       help="Refresh interval in seconds")
    
    args = parser.parse_args()
    
    try:
        monitor = ZStreamRealtimeMonitor(args.base_dir)
        monitor.refresh_interval = args.refresh
        
        if args.list:
            runs = monitor.get_run_list()
            print("📋 Available Analysis Runs:")
            print("-" * 60)
            
            for run in runs:
                print(f"🔍 {run['run_id']}")
                print(f"   📅 Created: {run['created']}")
                print(f"   📊 Entries: {run.get('total_entries', 'N/A')}")
                if run.get('jenkins_url'):
                    print(f"   🔗 Jenkins: {run['jenkins_url']}")
                print(f"   📁 Directory: {run['directory']}")
                print()
        
        elif args.export:
            monitor.export_current_status(args.export)
        
        elif args.current or args.dashboard:
            print("🚀 Starting real-time monitoring...")
            print(f"⏱️  Refresh interval: {args.refresh} seconds")
            print("Press Ctrl+C to stop")
            print()
            time.sleep(2)
            
            monitor.monitor_current_run(dashboard=args.dashboard)
        
        else:
            # Default: show current status once
            run_info = monitor.get_current_run_info()
            
            if not run_info:
                print("No active run detected")
            else:
                status = monitor.get_run_status(run_info)
                print(json.dumps(status, indent=2))
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()