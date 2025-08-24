#!/usr/bin/env python3
"""
Real-Time Framework Monitor

Purpose: Provide real-time monitoring of framework execution with live updates,
alerts, and dashboard-style interface for debugging and investigation.

Author: AI Systems Suite
Version: 1.0.0
"""

import json
import time
import threading
import queue
import curses
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import defaultdict, deque
import subprocess
import os

class RealTimeFrameworkMonitor:
    """
    Real-time framework monitoring with live dashboard interface
    
    Features:
    - Live log streaming and parsing
    - Real-time execution status
    - Agent coordination tracking
    - Performance metrics display
    - Error alerting
    - Interactive dashboard
    - Export capabilities
    """
    
    def __init__(self, log_directory: str, refresh_interval: float = 1.0):
        self.log_dir = Path(log_directory)
        self.refresh_interval = refresh_interval
        
        # State tracking
        self.current_state = {
            'run_id': None,
            'start_time': None,
            'current_phase': None,
            'active_agents': set(),
            'completed_agents': set(),
            'validation_status': {},
            'error_count': 0,
            'total_events': 0,
            'last_activity': None
        }
        
        # Real-time data
        self.recent_events = deque(maxlen=100)  # Last 100 events
        self.phase_timeline = []
        self.agent_status = {}
        self.tool_usage = defaultdict(int)
        self.performance_metrics = {}
        self.error_log = deque(maxlen=20)  # Last 20 errors
        
        # Monitoring state
        self.monitoring_active = False
        self.last_file_positions = {}
        self.alert_conditions = {
            'error_threshold': 5,
            'phase_timeout': 300,  # 5 minutes
            'agent_timeout': 180   # 3 minutes
        }
        
        # Threading
        self.log_queue = queue.Queue()
        self.monitor_thread = None
        self.update_thread = None
        self._stop_event = threading.Event()
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        if self.monitoring_active:
            print("⚠️  Monitoring already active")
            return
        
        print(f"🔍 Starting real-time monitoring of: {self.log_dir}")
        self.monitoring_active = True
        self._stop_event.clear()
        
        # Start log monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_logs, daemon=True)
        self.monitor_thread.start()
        
        # Start update processing thread
        self.update_thread = threading.Thread(target=self._process_updates, daemon=True)
        self.update_thread.start()
        
        print("✅ Real-time monitoring started")
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        if not self.monitoring_active:
            return
        
        print("🛑 Stopping real-time monitoring...")
        self.monitoring_active = False
        self._stop_event.set()
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        if self.update_thread:
            self.update_thread.join(timeout=2)
        
        print("✅ Real-time monitoring stopped")
    
    def _monitor_logs(self):
        """Monitor log files for changes"""
        while self.monitoring_active and not self._stop_event.is_set():
            try:
                # Check for new or updated log files
                self._scan_log_files()
                time.sleep(self.refresh_interval)
                
            except Exception as e:
                print(f"❌ Log monitoring error: {e}")
                time.sleep(self.refresh_interval)
    
    def _scan_log_files(self):
        """Scan log directory for new content"""
        if not self.log_dir.exists():
            return
        
        # Check master log file
        master_log = self.log_dir / 'framework_debug_master.jsonl'
        if master_log.exists():
            self._tail_log_file(master_log, 'master')
        
        # Check summary file
        summary_file = self.log_dir / 'execution_summary.json'
        if summary_file.exists():
            self._check_summary_file(summary_file)
        
        # Check component-specific logs
        for component_dir in ['phases', 'agents', 'tools', 'context', 'validation', 'environment']:
            comp_path = self.log_dir / component_dir
            if comp_path.exists():
                for log_file in comp_path.glob("*.jsonl"):
                    self._tail_log_file(log_file, f"{component_dir}_{log_file.stem}")
    
    def _tail_log_file(self, log_file: Path, file_key: str):
        """Tail a log file for new content"""
        try:
            current_size = log_file.stat().st_size
            last_position = self.last_file_positions.get(file_key, 0)
            
            if current_size > last_position:
                with open(log_file, 'r') as f:
                    f.seek(last_position)
                    new_lines = f.readlines()
                    self.last_file_positions[file_key] = f.tell()
                
                # Process new lines
                for line in new_lines:
                    line = line.strip()
                    if line:
                        try:
                            log_entry = json.loads(line)
                            self.log_queue.put(('log_entry', log_entry))
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            # File might be being written to, ignore errors
            pass
    
    def _check_summary_file(self, summary_file: Path):
        """Check summary file for updates"""
        try:
            with open(summary_file, 'r') as f:
                summary = json.load(f)
            
            self.log_queue.put(('summary_update', summary))
            
        except Exception as e:
            pass
    
    def _process_updates(self):
        """Process log updates and maintain state"""
        while self.monitoring_active and not self._stop_event.is_set():
            try:
                # Process queued updates
                while not self.log_queue.empty():
                    update_type, data = self.log_queue.get_nowait()
                    
                    if update_type == 'log_entry':
                        self._process_log_entry(data)
                    elif update_type == 'summary_update':
                        self._process_summary_update(data)
                
                # Check for alerts
                self._check_alerts()
                
                time.sleep(0.1)  # Fast processing loop
                
            except queue.Empty:
                time.sleep(0.1)
            except Exception as e:
                print(f"❌ Update processing error: {e}")
                time.sleep(1)
    
    def _process_log_entry(self, log_entry: Dict[str, Any]):
        """Process a new log entry"""
        self.current_state['total_events'] += 1
        self.current_state['last_activity'] = log_entry.get('timestamp')
        
        # Add to recent events
        self.recent_events.append({
            'timestamp': log_entry.get('timestamp'),
            'component': log_entry.get('component'),
            'action': log_entry.get('action'),
            'phase': log_entry.get('phase'),
            'agent': log_entry.get('agent'),
            'log_level': log_entry.get('log_level')
        })
        
        # Process by component
        component = log_entry.get('component')
        
        if component == 'PHASE':
            self._process_phase_event(log_entry)
        elif component == 'AGENT':
            self._process_agent_event(log_entry)
        elif component == 'TOOL':
            self._process_tool_event(log_entry)
        elif component == 'VALIDATION':
            self._process_validation_event(log_entry)
        
        # Process errors
        if log_entry.get('log_level') in ['ERROR', 'CRITICAL']:
            self._process_error_event(log_entry)
        
        # Process performance metrics
        if log_entry.get('performance_metrics'):
            self._process_performance_event(log_entry)
    
    def _process_phase_event(self, log_entry: Dict[str, Any]):
        """Process phase-related event"""
        phase = log_entry.get('phase')
        action = log_entry.get('action', '')
        
        if phase:
            if 'start' in action.lower():
                self.current_state['current_phase'] = phase
                self.phase_timeline.append({
                    'phase': phase,
                    'start_time': log_entry.get('timestamp'),
                    'status': 'in_progress'
                })
            elif 'complete' in action.lower():
                # Update timeline
                for phase_entry in reversed(self.phase_timeline):
                    if phase_entry['phase'] == phase and phase_entry['status'] == 'in_progress':
                        phase_entry['end_time'] = log_entry.get('timestamp')
                        phase_entry['status'] = 'completed'
                        break
    
    def _process_agent_event(self, log_entry: Dict[str, Any]):
        """Process agent-related event"""
        agent = log_entry.get('agent')
        action = log_entry.get('action', '')
        
        if agent:
            if 'spawn' in action.lower() or 'start' in action.lower():
                self.current_state['active_agents'].add(agent)
                self.agent_status[agent] = {
                    'status': 'active',
                    'start_time': log_entry.get('timestamp'),
                    'last_activity': log_entry.get('timestamp')
                }
            elif 'complete' in action.lower():
                self.current_state['active_agents'].discard(agent)
                self.current_state['completed_agents'].add(agent)
                if agent in self.agent_status:
                    self.agent_status[agent]['status'] = 'completed'
                    self.agent_status[agent]['end_time'] = log_entry.get('timestamp')
            else:
                # Update last activity
                if agent in self.agent_status:
                    self.agent_status[agent]['last_activity'] = log_entry.get('timestamp')
    
    def _process_tool_event(self, log_entry: Dict[str, Any]):
        """Process tool-related event"""
        details = log_entry.get('details', {})
        tool_name = details.get('tool_name', 'unknown')
        
        self.tool_usage[tool_name] += 1
    
    def _process_validation_event(self, log_entry: Dict[str, Any]):
        """Process validation-related event"""
        details = log_entry.get('details', {})
        validation_type = details.get('validation_type', 'unknown')
        result = details.get('result', 'unknown')
        confidence = details.get('confidence')
        
        self.current_state['validation_status'][validation_type] = {
            'result': result,
            'confidence': confidence,
            'timestamp': log_entry.get('timestamp')
        }
    
    def _process_error_event(self, log_entry: Dict[str, Any]):
        """Process error event"""
        self.current_state['error_count'] += 1
        
        self.error_log.append({
            'timestamp': log_entry.get('timestamp'),
            'component': log_entry.get('component'),
            'action': log_entry.get('action'),
            'details': log_entry.get('details', {}),
            'phase': log_entry.get('phase'),
            'agent': log_entry.get('agent')
        })
    
    def _process_performance_event(self, log_entry: Dict[str, Any]):
        """Process performance metrics"""
        metrics = log_entry.get('performance_metrics', {})
        component = log_entry.get('component')
        
        if component not in self.performance_metrics:
            self.performance_metrics[component] = {}
        
        for metric_name, value in metrics.items():
            if metric_name not in self.performance_metrics[component]:
                self.performance_metrics[component][metric_name] = []
            
            self.performance_metrics[component][metric_name].append({
                'value': value,
                'timestamp': log_entry.get('timestamp')
            })
    
    def _process_summary_update(self, summary: Dict[str, Any]):
        """Process summary file update"""
        run_metadata = summary.get('run_metadata', {})
        
        if run_metadata:
            self.current_state['run_id'] = run_metadata.get('run_id')
            self.current_state['start_time'] = run_metadata.get('start_time')
    
    def _check_alerts(self):
        """Check for alert conditions"""
        current_time = datetime.now()
        
        # Check error threshold
        if self.current_state['error_count'] > self.alert_conditions['error_threshold']:
            self._trigger_alert(f"High error count: {self.current_state['error_count']} errors")
        
        # Check phase timeout
        if self.phase_timeline:
            last_phase = self.phase_timeline[-1]
            if last_phase['status'] == 'in_progress':
                try:
                    start_time = datetime.fromisoformat(last_phase['start_time'].replace('Z', '+00:00'))
                    if (current_time - start_time.replace(tzinfo=None)).total_seconds() > self.alert_conditions['phase_timeout']:
                        self._trigger_alert(f"Phase timeout: {last_phase['phase']} running for too long")
                except ValueError:
                    pass
        
        # Check agent timeout
        for agent, status in self.agent_status.items():
            if status['status'] == 'active':
                try:
                    start_time = datetime.fromisoformat(status['start_time'].replace('Z', '+00:00'))
                    if (current_time - start_time.replace(tzinfo=None)).total_seconds() > self.alert_conditions['agent_timeout']:
                        self._trigger_alert(f"Agent timeout: {agent} running for too long")
                except ValueError:
                    pass
    
    def _trigger_alert(self, message: str):
        """Trigger an alert"""
        print(f"🚨 ALERT: {message}")
        # Could add more alert mechanisms here (email, webhook, etc.)
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        return {
            'current_state': dict(self.current_state),
            'recent_events': list(self.recent_events),
            'phase_timeline': self.phase_timeline,
            'agent_status': dict(self.agent_status),
            'tool_usage': dict(self.tool_usage),
            'error_count': len(self.error_log),
            'recent_errors': list(self.error_log),
            'monitoring_active': self.monitoring_active
        }
    
    def print_status_summary(self):
        """Print current status summary"""
        status = self.get_current_status()
        current_state = status['current_state']
        
        print("\n📊 REAL-TIME FRAMEWORK STATUS")
        print("=" * 50)
        print(f"Run ID: {current_state.get('run_id', 'N/A')}")
        print(f"Current Phase: {current_state.get('current_phase', 'N/A')}")
        print(f"Active Agents: {len(current_state.get('active_agents', []))}")
        print(f"Completed Agents: {len(current_state.get('completed_agents', []))}")
        print(f"Total Events: {current_state.get('total_events', 0)}")
        print(f"Error Count: {current_state.get('error_count', 0)}")
        print(f"Last Activity: {current_state.get('last_activity', 'N/A')}")
        
        # Show active agents
        if current_state.get('active_agents'):
            print(f"\n🤖 Active Agents:")
            for agent in current_state['active_agents']:
                agent_info = status['agent_status'].get(agent, {})
                start_time = agent_info.get('start_time', 'N/A')
                print(f"   {agent:15} (started: {start_time[:19] if start_time != 'N/A' else 'N/A'})")
        
        # Show recent events
        if status['recent_events']:
            print(f"\n📋 Recent Events (Last 5):")
            for event in list(status['recent_events'])[-5:]:
                timestamp = event.get('timestamp', 'N/A')[:19]
                component = event.get('component', 'N/A')
                action = event.get('action', 'N/A')[:30]
                print(f"   {timestamp} {component:10} {action}")
        
        # Show recent errors
        if status['recent_errors']:
            print(f"\n❌ Recent Errors:")
            for error in list(status['recent_errors'])[-3:]:
                timestamp = error.get('timestamp', 'N/A')[:19]
                component = error.get('component', 'N/A')
                action = error.get('action', 'N/A')[:30]
                print(f"   {timestamp} {component:10} {action}")
    
    def start_dashboard(self):
        """Start interactive curses dashboard"""
        try:
            curses.wrapper(self._dashboard_main)
        except KeyboardInterrupt:
            print("\nDashboard interrupted")
        except Exception as e:
            print(f"Dashboard error: {e}")
    
    def _dashboard_main(self, stdscr):
        """Main dashboard display using curses"""
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(1)   # Non-blocking input
        stdscr.timeout(1000)  # 1 second timeout
        
        # Color pairs
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Success
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Error
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Warning
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Info
        
        while self.monitoring_active:
            try:
                stdscr.clear()
                height, width = stdscr.getmaxyx()
                
                # Title
                title = f"Framework Real-Time Monitor - {self.log_dir.name}"
                stdscr.addstr(0, max(0, (width - len(title)) // 2), title, 
                            curses.color_pair(4) | curses.A_BOLD)
                
                # Current status
                status = self.get_current_status()
                current_state = status['current_state']
                
                row = 2
                stdscr.addstr(row, 2, f"Run ID: {current_state.get('run_id', 'N/A')}")
                row += 1
                stdscr.addstr(row, 2, f"Phase: {current_state.get('current_phase', 'N/A')}")
                row += 1
                stdscr.addstr(row, 2, f"Active Agents: {len(current_state.get('active_agents', []))}")
                row += 1
                stdscr.addstr(row, 2, f"Total Events: {current_state.get('total_events', 0)}")
                row += 1
                
                # Error count with color
                error_count = current_state.get('error_count', 0)
                error_color = curses.color_pair(2) if error_count > 0 else curses.color_pair(1)
                stdscr.addstr(row, 2, f"Errors: {error_count}", error_color)
                row += 2
                
                # Recent events
                stdscr.addstr(row, 2, "Recent Events:", curses.A_BOLD)
                row += 1
                
                for event in list(status['recent_events'])[-10:]:
                    if row >= height - 2:
                        break
                    
                    timestamp = event.get('timestamp', 'N/A')[:19]
                    component = event.get('component', 'N/A')[:8]
                    action = event.get('action', 'N/A')[:40]
                    
                    event_color = curses.A_NORMAL
                    if event.get('log_level') == 'ERROR':
                        event_color = curses.color_pair(2)
                    elif event.get('log_level') == 'WARN':
                        event_color = curses.color_pair(3)
                    
                    event_line = f"{timestamp} {component:8} {action}"
                    if len(event_line) > width - 4:
                        event_line = event_line[:width-7] + "..."
                    
                    stdscr.addstr(row, 4, event_line, event_color)
                    row += 1
                
                # Footer
                footer = "Press 'q' to quit, 'r' to refresh"
                stdscr.addstr(height-1, 2, footer)
                
                stdscr.refresh()
                
                # Handle input
                key = stdscr.getch()
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    continue  # Force refresh
                
            except Exception as e:
                # If there's an error, show it and continue
                try:
                    stdscr.addstr(height-2, 2, f"Display error: {str(e)[:width-10]}", curses.color_pair(2))
                    stdscr.refresh()
                    time.sleep(1)
                except:
                    break
    
    def export_status(self, output_file: str):
        """Export current status to file"""
        status = self.get_current_status()
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(status, f, indent=2, default=str)
        
        print(f"📄 Status exported to: {output_path}")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Real-Time Framework Monitor")
    parser.add_argument('log_directory', help='Path to log directory to monitor')
    parser.add_argument('--interval', type=float, default=1.0, help='Refresh interval in seconds')
    parser.add_argument('--dashboard', action='store_true', help='Start interactive dashboard')
    parser.add_argument('--status', action='store_true', help='Show current status and exit')
    parser.add_argument('--export', help='Export status to file and exit')
    parser.add_argument('--error-threshold', type=int, default=5, help='Error count alert threshold')
    parser.add_argument('--phase-timeout', type=int, default=300, help='Phase timeout in seconds')
    parser.add_argument('--agent-timeout', type=int, default=180, help='Agent timeout in seconds')
    
    args = parser.parse_args()
    
    try:
        monitor = RealTimeFrameworkMonitor(args.log_directory, args.interval)
        
        # Set alert conditions
        monitor.alert_conditions['error_threshold'] = args.error_threshold
        monitor.alert_conditions['phase_timeout'] = args.phase_timeout
        monitor.alert_conditions['agent_timeout'] = args.agent_timeout
        
        if args.status:
            # Just show current status
            monitor.start_monitoring()
            time.sleep(2)  # Give it time to read logs
            monitor.print_status_summary()
            monitor.stop_monitoring()
            
        elif args.export:
            # Export status and exit
            monitor.start_monitoring()
            time.sleep(2)  # Give it time to read logs
            monitor.export_status(args.export)
            monitor.stop_monitoring()
            
        elif args.dashboard:
            # Start interactive dashboard
            monitor.start_monitoring()
            print("Starting interactive dashboard...")
            time.sleep(1)  # Brief pause before dashboard
            monitor.start_dashboard()
            monitor.stop_monitoring()
            
        else:
            # Continuous monitoring with periodic status
            monitor.start_monitoring()
            
            try:
                while True:
                    time.sleep(10)  # Update every 10 seconds
                    os.system('clear' if os.name == 'posix' else 'cls')
                    monitor.print_status_summary()
                    
            except KeyboardInterrupt:
                print("\nStopping monitor...")
                monitor.stop_monitoring()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())