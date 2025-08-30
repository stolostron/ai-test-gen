#!/usr/bin/env python3
"""
Z-Stream Analysis Log Analyzer
Comprehensive analysis and investigation tools for logged pipeline analysis runs
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from collections import defaultdict, Counter
import re


class ZStreamLogAnalyzer:
    """
    Comprehensive log analysis for z-stream-analysis framework
    """
    
    def __init__(self, run_directory: str):
        self.run_dir = Path(run_directory)
        self.master_log = self.run_dir / "master_log.jsonl"
        self.summary_file = self.run_dir / "execution_summary.json"
        
        if not self.run_dir.exists():
            raise ValueError(f"Run directory does not exist: {run_directory}")
        
        if not self.master_log.exists():
            raise ValueError(f"Master log not found: {self.master_log}")
    
    def load_all_entries(self) -> List[Dict[str, Any]]:
        """Load all log entries from master log"""
        entries = []
        
        try:
            with open(self.master_log, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        entry = json.loads(line.strip())
                        entries.append(entry)
                    except json.JSONDecodeError as e:
                        print(f"Warning: Invalid JSON on line {line_num}: {e}")
                        continue
        except Exception as e:
            print(f"Error reading master log: {e}")
            return []
        
        return entries
    
    def analyze_timeline(self) -> Dict[str, Any]:
        """Analyze execution timeline"""
        entries = self.load_all_entries()
        if not entries:
            return {"error": "No entries found"}
        
        timeline = {
            "total_entries": len(entries),
            "start_time": None,
            "end_time": None,
            "duration_seconds": 0,
            "phases": {},
            "services": {},
            "tools": {},
            "stage_timeline": []
        }
        
        start_time = None
        end_time = None
        
        for entry in entries:
            timestamp = entry.get('timestamp')
            if timestamp:
                if not start_time:
                    start_time = timestamp
                end_time = timestamp
            
            # Track phases
            stage = entry.get('stage', 'unknown')
            if stage not in timeline['phases']:
                timeline['phases'][stage] = {
                    "first_seen": timestamp,
                    "last_seen": timestamp,
                    "entry_count": 0,
                    "errors": 0
                }
            
            timeline['phases'][stage]['entry_count'] += 1
            timeline['phases'][stage]['last_seen'] = timestamp
            
            if entry.get('log_level') in ['ERROR', 'CRITICAL']:
                timeline['phases'][stage]['errors'] += 1
            
            # Track services
            component = entry.get('component', 'unknown')
            if component not in timeline['services']:
                timeline['services'][component] = {
                    "first_seen": timestamp,
                    "last_seen": timestamp,
                    "entry_count": 0,
                    "actions": Counter()
                }
            
            timeline['services'][component]['entry_count'] += 1
            timeline['services'][component]['last_seen'] = timestamp
            
            action = entry.get('action', 'unknown')
            timeline['services'][component]['actions'][action] += 1
            
            # Track tools
            tool = entry.get('tool')
            if tool:
                if tool not in timeline['tools']:
                    timeline['tools'][tool] = {
                        "usage_count": 0,
                        "total_duration_ms": 0,
                        "avg_duration_ms": 0,
                        "errors": 0
                    }
                
                timeline['tools'][tool]['usage_count'] += 1
                
                duration = entry.get('duration_ms', 0)
                if duration:
                    timeline['tools'][tool]['total_duration_ms'] += duration
                    timeline['tools'][tool]['avg_duration_ms'] = (
                        timeline['tools'][tool]['total_duration_ms'] / 
                        timeline['tools'][tool]['usage_count']
                    )
                
                if not entry.get('success', True):
                    timeline['tools'][tool]['errors'] += 1
        
        # Calculate overall duration
        timeline['start_time'] = start_time
        timeline['end_time'] = end_time
        
        if start_time and end_time:
            try:
                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                timeline['duration_seconds'] = (end_dt - start_dt).total_seconds()
            except:
                timeline['duration_seconds'] = 0
        
        return timeline
    
    def analyze_services(self) -> Dict[str, Any]:
        """Analyze service coordination and performance"""
        entries = self.load_all_entries()
        
        services_analysis = {
            "service_summary": {},
            "coordination_flow": [],
            "service_performance": {},
            "context_inheritance": []
        }
        
        service_entries = defaultdict(list)
        
        for entry in entries:
            component = entry.get('component', 'unknown')
            if 'service' in component.lower() or 'intelligence' in component.lower():
                service_entries[component].append(entry)
        
        # Analyze each service
        for service, entries_list in service_entries.items():
            analysis = {
                "total_operations": len(entries_list),
                "start_time": entries_list[0].get('timestamp') if entries_list else None,
                "end_time": entries_list[-1].get('timestamp') if entries_list else None,
                "stages": Counter(),
                "actions": Counter(),
                "errors": 0,
                "success_rate": 0
            }
            
            successful_ops = 0
            for entry in entries_list:
                stage = entry.get('stage', 'unknown')
                action = entry.get('action', 'unknown')
                
                analysis['stages'][stage] += 1
                analysis['actions'][action] += 1
                
                if entry.get('log_level') in ['ERROR', 'CRITICAL']:
                    analysis['errors'] += 1
                elif entry.get('success', True):
                    successful_ops += 1
            
            if analysis['total_operations'] > 0:
                analysis['success_rate'] = successful_ops / analysis['total_operations']
            
            services_analysis['service_summary'][service] = analysis
        
        return services_analysis
    
    def analyze_tools(self) -> Dict[str, Any]:
        """Analyze tool usage and performance"""
        entries = self.load_all_entries()
        
        tools_analysis = {
            "tool_summary": {},
            "command_patterns": Counter(),
            "performance_metrics": {},
            "security_events": []
        }
        
        tool_entries = defaultdict(list)
        
        for entry in entries:
            tool = entry.get('tool')
            if tool:
                tool_entries[tool].append(entry)
                
                # Track command patterns
                command = entry.get('command', '')
                if command:
                    # Extract command type
                    cmd_type = command.split()[0] if command.split() else 'unknown'
                    tools_analysis['command_patterns'][cmd_type] += 1
                
                # Track security events
                security = entry.get('security', {})
                if security.get('credentials_masked') or security.get('sensitive_data_detected'):
                    tools_analysis['security_events'].append({
                        "timestamp": entry.get('timestamp'),
                        "tool": tool,
                        "command": command[:50] + "..." if len(command) > 50 else command,
                        "security_action": "credential_masking" if security.get('credentials_masked') else "sensitive_data_detection"
                    })
        
        # Analyze each tool
        for tool, entries_list in tool_entries.items():
            durations = []
            errors = 0
            total_ops = len(entries_list)
            
            for entry in entries_list:
                duration = entry.get('duration_ms')
                if duration:
                    durations.append(duration)
                
                if not entry.get('success', True) or entry.get('log_level') in ['ERROR', 'CRITICAL']:
                    errors += 1
            
            analysis = {
                "total_executions": total_ops,
                "error_count": errors,
                "success_rate": (total_ops - errors) / total_ops if total_ops > 0 else 0,
                "avg_duration_ms": sum(durations) / len(durations) if durations else 0,
                "max_duration_ms": max(durations) if durations else 0,
                "min_duration_ms": min(durations) if durations else 0
            }
            
            tools_analysis['tool_summary'][tool] = analysis
        
        return tools_analysis
    
    def analyze_errors(self) -> Dict[str, Any]:
        """Analyze errors and issues"""
        entries = self.load_all_entries()
        
        error_analysis = {
            "total_errors": 0,
            "error_types": Counter(),
            "error_timeline": [],
            "affected_components": Counter(),
            "error_patterns": [],
            "critical_errors": []
        }
        
        for entry in entries:
            log_level = entry.get('log_level', 'INFO')
            
            if log_level in ['ERROR', 'CRITICAL', 'WARNING']:
                error_analysis['total_errors'] += 1
                error_analysis['error_types'][log_level] += 1
                
                component = entry.get('component', 'unknown')
                error_analysis['affected_components'][component] += 1
                
                error_event = {
                    "timestamp": entry.get('timestamp'),
                    "level": log_level,
                    "component": component,
                    "stage": entry.get('stage'),
                    "action": entry.get('action'),
                    "message": entry.get('message', ''),
                    "tool": entry.get('tool'),
                    "command": entry.get('command', '')[:100] + "..." if len(entry.get('command', '')) > 100 else entry.get('command', '')
                }
                
                error_analysis['error_timeline'].append(error_event)
                
                if log_level == 'CRITICAL':
                    error_analysis['critical_errors'].append(error_event)
        
        return error_analysis
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate comprehensive summary report"""
        timeline = self.analyze_timeline()
        services = self.analyze_services()
        tools = self.analyze_tools()
        errors = self.analyze_errors()
        
        summary = {
            "run_id": self.run_dir.name,
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
            "overview": {
                "total_log_entries": timeline.get('total_entries', 0),
                "execution_duration_seconds": timeline.get('duration_seconds', 0),
                "start_time": timeline.get('start_time'),
                "end_time": timeline.get('end_time'),
                "total_errors": errors.get('total_errors', 0),
                "services_involved": len(services.get('service_summary', {})),
                "tools_used": len(tools.get('tool_summary', {})),
                "stages_completed": len(timeline.get('phases', {}))
            },
            "performance": {
                "most_used_tool": max(tools.get('tool_summary', {}).items(), 
                                   key=lambda x: x[1]['total_executions'], 
                                   default=("none", {"total_executions": 0}))[0],
                "slowest_tool": max(tools.get('tool_summary', {}).items(), 
                                  key=lambda x: x[1]['avg_duration_ms'], 
                                  default=("none", {"avg_duration_ms": 0}))[0],
                "tool_success_rates": {tool: data['success_rate'] 
                                     for tool, data in tools.get('tool_summary', {}).items()}
            },
            "service_coordination": {
                "service_success_rates": {service: data['success_rate'] 
                                        for service, data in services.get('service_summary', {}).items()},
                "most_active_service": max(services.get('service_summary', {}).items(), 
                                         key=lambda x: x[1]['total_operations'], 
                                         default=("none", {"total_operations": 0}))[0]
            },
            "quality": {
                "error_rate": errors.get('total_errors', 0) / timeline.get('total_entries', 1),
                "critical_errors": len(errors.get('critical_errors', [])),
                "security_events": len(tools.get('security_events', [])),
                "most_problematic_component": max(errors.get('affected_components', {}).items(), 
                                                key=lambda x: x[1], 
                                                default=("none", 0))[0]
            }
        }
        
        return summary
    
    def export_analysis(self, output_file: str, analysis_type: str = "all"):
        """Export analysis to file"""
        output_path = Path(output_file)
        
        if analysis_type == "all":
            data = {
                "timeline": self.analyze_timeline(),
                "services": self.analyze_services(),
                "tools": self.analyze_tools(),
                "errors": self.analyze_errors(),
                "summary": self.generate_summary_report()
            }
        elif analysis_type == "timeline":
            data = self.analyze_timeline()
        elif analysis_type == "services":
            data = self.analyze_services()
        elif analysis_type == "tools":
            data = self.analyze_tools()
        elif analysis_type == "errors":
            data = self.analyze_errors()
        elif analysis_type == "summary":
            data = self.generate_summary_report()
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Analysis exported to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Z-Stream Analysis Log Analyzer")
    parser.add_argument("run_directory", help="Path to the run directory to analyze")
    parser.add_argument("--analysis", choices=["all", "timeline", "services", "tools", "errors", "summary"], 
                       default="summary", help="Type of analysis to perform")
    parser.add_argument("--export", help="Export analysis to file")
    parser.add_argument("--interactive", action="store_true", help="Start interactive analysis session")
    
    args = parser.parse_args()
    
    try:
        analyzer = ZStreamLogAnalyzer(args.run_directory)
        
        if args.interactive:
            print("=== Z-Stream Analysis Interactive Mode ===")
            print("Available commands: timeline, services, tools, errors, summary, export, quit")
            
            while True:
                command = input("\\nanalyzer> ").strip().lower()
                
                if command == "quit":
                    break
                elif command == "timeline":
                    result = analyzer.analyze_timeline()
                    print(json.dumps(result, indent=2))
                elif command == "services":
                    result = analyzer.analyze_services()
                    print(json.dumps(result, indent=2))
                elif command == "tools":
                    result = analyzer.analyze_tools()
                    print(json.dumps(result, indent=2))
                elif command == "errors":
                    result = analyzer.analyze_errors()
                    print(json.dumps(result, indent=2))
                elif command == "summary":
                    result = analyzer.generate_summary_report()
                    print(json.dumps(result, indent=2))
                elif command.startswith("export "):
                    filename = command.split(" ", 1)[1]
                    analyzer.export_analysis(filename, "all")
                else:
                    print("Unknown command. Available: timeline, services, tools, errors, summary, export <file>, quit")
        
        else:
            # Non-interactive mode
            if args.analysis == "timeline":
                result = analyzer.analyze_timeline()
            elif args.analysis == "services":
                result = analyzer.analyze_services()
            elif args.analysis == "tools":
                result = analyzer.analyze_tools()
            elif args.analysis == "errors":
                result = analyzer.analyze_errors()
            elif args.analysis == "summary":
                result = analyzer.generate_summary_report()
            elif args.analysis == "all":
                result = {
                    "timeline": analyzer.analyze_timeline(),
                    "services": analyzer.analyze_services(),
                    "tools": analyzer.analyze_tools(),
                    "errors": analyzer.analyze_errors(),
                    "summary": analyzer.generate_summary_report()
                }
            
            if args.export:
                analyzer.export_analysis(args.export, args.analysis)
            else:
                print(json.dumps(result, indent=2))
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()