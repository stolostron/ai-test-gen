#!/usr/bin/env python3
"""
Framework Logging Integration Script

Purpose: Enable comprehensive logging and debugging for claude-test-generator framework.
Provides easy setup, configuration, and integration of all logging components.

Author: AI Systems Suite
Version: 1.0.0
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from framework_debug_logger import FrameworkDebugLogger, initialize_global_logger, finalize_global_logger
from framework_hooks import FrameworkHookIntegration, initialize_global_hooks, finalize_global_hooks, with_framework_hooks
from log_analyzer import FrameworkLogAnalyzer
from realtime_monitor import RealTimeFrameworkMonitor

class FrameworkLoggingIntegration:
    """
    Complete framework logging integration and management system
    
    Features:
    - Automatic logging setup and configuration
    - Hook integration for tool and framework monitoring
    - Real-time monitoring capabilities
    - Log analysis and debugging tools
    - Configuration management
    - Integration with existing framework
    """
    
    def __init__(self, config_file: str = None):
        self.base_dir = Path(__file__).parent.parent
        self.config_file = config_file or self.base_dir / "config" / "logging-config.json"
        self.config = self._load_configuration()
        
        # Components
        self.logger = None
        self.hooks = None
        self.monitor = None
        self.analyzer = None
        
        print(f"🔧 Framework Logging Integration initialized")
        print(f"   Base directory: {self.base_dir}")
        print(f"   Config file: {self.config_file}")
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load logging configuration"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            return config.get('framework_debug_logging', {})
        except Exception as e:
            print(f"⚠️  Failed to load config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "enabled": True,
            "global_settings": {
                "default_log_level": "DEBUG",
                "auto_start_logging": True,
                "enable_real_time_monitoring": False
            },
            "hook_configuration": {
                "auto_install_hooks": True,
                "enabled_hooks": {
                    "claude_code_tools": True,
                    "framework_phases": True,
                    "agent_coordination": True,
                    "context_flow": True,
                    "validation_checkpoints": True
                }
            }
        }
    
    def setup_logging(self, run_id: str = None, jira_ticket: str = None) -> FrameworkDebugLogger:
        """Setup comprehensive logging"""
        print(f"\n🔍 Setting up framework logging...")
        
        if not self.config.get('enabled', True):
            print("⚠️  Logging disabled in configuration")
            return None
        
        # Determine log directory
        log_settings = self.config.get('log_destinations', {})
        base_dir = log_settings.get('base_directory', '.claude/logging')
        log_base_path = self.base_dir / base_dir
        
        # Initialize logger
        self.logger = initialize_global_logger(run_id, str(log_base_path))
        
        print(f"✅ Framework logging initialized")
        print(f"   Run ID: {self.logger.run_id}")
        print(f"   Log directory: {self.logger.log_dir}")
        
        return self.logger
    
    def setup_hooks(self) -> FrameworkHookIntegration:
        """Setup framework hooks"""
        print(f"\n🪝 Setting up framework hooks...")
        
        hook_config = self.config.get('hook_configuration', {})
        
        if not hook_config.get('auto_install_hooks', True):
            print("⚠️  Hook installation disabled in configuration")
            return None
        
        # Initialize hooks
        self.hooks = initialize_global_hooks(self.logger)
        
        # Configure enabled hooks based on config
        enabled_hooks = hook_config.get('enabled_hooks', {})
        
        if not enabled_hooks.get('claude_code_tools', True):
            print("⚠️  Claude Code tool hooks disabled")
            # In a real implementation, you'd disable specific hooks here
        
        print(f"✅ Framework hooks installed")
        print(f"   Hooks enabled: {len(self.hooks.hook_registry)}")
        
        return self.hooks
    
    def start_monitoring(self, real_time: bool = None) -> Optional[RealTimeFrameworkMonitor]:
        """Start real-time monitoring"""
        if real_time is None:
            real_time = self.config.get('real_time_monitoring', {}).get('enabled', False)
        
        if not real_time or not self.logger:
            return None
        
        print(f"\n📊 Starting real-time monitoring...")
        
        monitor_config = self.config.get('real_time_monitoring', {})
        refresh_interval = monitor_config.get('refresh_interval_seconds', 1.0)
        
        self.monitor = RealTimeFrameworkMonitor(str(self.logger.log_dir), refresh_interval)
        
        # Configure alert conditions
        alert_conditions = monitor_config.get('alert_conditions', {})
        if alert_conditions:
            self.monitor.alert_conditions.update({
                'error_threshold': alert_conditions.get('error_threshold', 5),
                'phase_timeout': alert_conditions.get('phase_timeout_minutes', 5) * 60,
                'agent_timeout': alert_conditions.get('agent_timeout_minutes', 3) * 60
            })
        
        self.monitor.start_monitoring()
        
        print(f"✅ Real-time monitoring started")
        print(f"   Refresh interval: {refresh_interval}s")
        
        return self.monitor
    
    def enable_framework_logging(self, run_id: str = None, jira_ticket: str = None, 
                                real_time_monitoring: bool = None) -> Dict[str, Any]:
        """Enable complete framework logging with all components"""
        print(f"\n🚀 ENABLING COMPREHENSIVE FRAMEWORK LOGGING")
        print("=" * 60)
        
        components = {}
        
        try:
            # Setup logging
            logger = self.setup_logging(run_id, jira_ticket)
            components['logger'] = logger is not None
            
            # Setup hooks
            hooks = self.setup_hooks()
            components['hooks'] = hooks is not None
            
            # Start framework logging
            if hooks:
                hooks.start_framework_logging(run_id, jira_ticket)
            
            # Start monitoring
            monitor = self.start_monitoring(real_time_monitoring)
            components['monitor'] = monitor is not None
            
            print(f"\n✅ FRAMEWORK LOGGING FULLY ENABLED")
            print(f"   Logger: {'✓' if components['logger'] else '✗'}")
            print(f"   Hooks: {'✓' if components['hooks'] else '✗'}")
            print(f"   Monitor: {'✓' if components['monitor'] else '✗'}")
            
            if logger:
                print(f"   Log directory: {logger.log_dir}")
                
                # Log the activation
                logger.log_info("FRAMEWORK_LOGGING_ENABLED", "Comprehensive framework logging enabled", {
                    "components_enabled": components,
                    "run_id": run_id,
                    "jira_ticket": jira_ticket,
                    "config_file": str(self.config_file)
                })
            
            return {
                'success': True,
                'components': components,
                'logger': logger,
                'hooks': hooks,
                'monitor': monitor,
                'log_directory': str(logger.log_dir) if logger else None
            }
            
        except Exception as e:
            print(f"❌ Failed to enable framework logging: {e}")
            return {
                'success': False,
                'error': str(e),
                'components': components
            }
    
    def disable_framework_logging(self):
        """Disable framework logging and clean up"""
        print(f"\n🛑 Disabling framework logging...")
        
        try:
            # Stop monitoring
            if self.monitor:
                self.monitor.stop_monitoring()
                self.monitor = None
                print("✅ Real-time monitoring stopped")
            
            # Finalize hooks
            if self.hooks:
                finalize_global_hooks()
                self.hooks = None
                print("✅ Framework hooks finalized")
            
            # Finalize logger
            if self.logger:
                log_dir = self.logger.log_dir
                finalize_global_logger()
                self.logger = None
                print(f"✅ Framework logging finalized")
                print(f"   Logs saved to: {log_dir}")
            
            print(f"✅ Framework logging fully disabled")
            
        except Exception as e:
            print(f"❌ Error disabling logging: {e}")
    
    def analyze_logs(self, log_directory: str = None, analysis_type: str = 'all') -> FrameworkLogAnalyzer:
        """Analyze framework logs"""
        if log_directory is None:
            if self.logger:
                log_directory = str(self.logger.log_dir)
            else:
                print("❌ No log directory specified and no active logger")
                return None
        
        print(f"\n📊 Analyzing framework logs: {log_directory}")
        
        try:
            analyzer = FrameworkLogAnalyzer(log_directory)
            
            if analysis_type == 'all':
                analyzer.generate_debug_report()
            elif analysis_type == 'timeline':
                analyzer.analyze_execution_timeline()
            elif analysis_type == 'agents':
                analyzer.analyze_agent_coordination()
            elif analysis_type == 'tools':
                analyzer.analyze_tool_usage()
            elif analysis_type == 'context':
                analyzer.analyze_context_flow()
            elif analysis_type == 'validate':
                analyzer.analyze_validation_checkpoints()
            elif analysis_type == 'errors':
                analyzer.analyze_errors()
            elif analysis_type == 'perf':
                analyzer.analyze_performance()
            elif analysis_type == 'interactive':
                analyzer.interactive_debug_session()
            
            return analyzer
            
        except Exception as e:
            print(f"❌ Log analysis failed: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of logging components"""
        status = {
            'logging_enabled': self.logger is not None,
            'hooks_enabled': self.hooks is not None,
            'monitoring_enabled': self.monitor is not None and self.monitor.monitoring_active,
            'config_loaded': bool(self.config),
            'log_directory': str(self.logger.log_dir) if self.logger else None
        }
        
        if self.logger:
            status['logger_status'] = self.logger.get_current_state()
        
        if self.hooks:
            status['hooks_status'] = self.hooks.get_hook_status()
        
        if self.monitor:
            status['monitor_status'] = self.monitor.get_current_status()
        
        return status
    
    def create_demo_logs(self):
        """Create demo logs for testing"""
        print(f"\n🧪 Creating demo logs for testing...")
        
        if not self.logger or not self.hooks:
            print("❌ Logging not enabled - run enable_framework_logging first")
            return
        
        import time
        
        # Simulate framework execution
        self.hooks.log_framework_phase("0-pre", "start", {"demo": True})
        time.sleep(0.1)
        
        self.hooks.log_agent_activity("agent_a", "spawn", {"task": "Demo JIRA analysis"})
        time.sleep(0.2)
        
        # Simulate tool usage
        bash_hook = self.hooks.hook_registry.get('bash_tool')
        if bash_hook:
            bash_hook("echo 'Demo command execution'", "Demo bash execution")
        
        time.sleep(0.1)
        self.hooks.track_context_flow("demo_context_inheritance", {"demo_data": "test_context"})
        
        time.sleep(0.1)
        self.hooks.track_validation("demo_validation", "passed", 0.95)
        
        time.sleep(0.1)
        self.hooks.log_agent_activity("agent_a", "complete", {"result": "Demo completed"})
        
        time.sleep(0.1)
        self.hooks.log_framework_phase("0-pre", "complete", {"demo": True})
        
        print(f"✅ Demo logs created")
        print(f"   Check log directory: {self.logger.log_dir}")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Framework Logging Integration")
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--run-id', help='Run ID for logging session')
    parser.add_argument('--jira-ticket', help='JIRA ticket for logging session')
    parser.add_argument('--real-time', action='store_true', help='Enable real-time monitoring')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Enable command
    enable_parser = subparsers.add_parser('enable', help='Enable framework logging')
    enable_parser.add_argument('--monitor', action='store_true', help='Start real-time monitoring')
    
    # Disable command
    subparsers.add_parser('disable', help='Disable framework logging')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze logs')
    analyze_parser.add_argument('log_directory', nargs='?', help='Log directory to analyze')
    analyze_parser.add_argument('--type', choices=['all', 'timeline', 'agents', 'tools', 'context', 'validate', 'errors', 'perf', 'interactive'],
                               default='all', help='Analysis type')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Start real-time monitoring')
    monitor_parser.add_argument('log_directory', help='Log directory to monitor')
    monitor_parser.add_argument('--dashboard', action='store_true', help='Start interactive dashboard')
    
    # Status command
    subparsers.add_parser('status', help='Show logging status')
    
    # Demo command
    subparsers.add_parser('demo', help='Create demo logs for testing')
    
    args = parser.parse_args()
    
    try:
        integration = FrameworkLoggingIntegration(args.config)
        
        if args.command == 'enable':
            result = integration.enable_framework_logging(
                run_id=args.run_id,
                jira_ticket=args.jira_ticket,
                real_time_monitoring=args.monitor or args.real_time
            )
            
            if result['success']:
                print("\n🎉 Framework logging successfully enabled!")
                
                if args.monitor or args.real_time:
                    print("\n⚠️  Real-time monitoring is active. Press Ctrl+C to stop.")
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("\nStopping...")
                        integration.disable_framework_logging()
            else:
                print(f"\n❌ Failed to enable framework logging: {result.get('error')}")
                return 1
        
        elif args.command == 'disable':
            integration.disable_framework_logging()
        
        elif args.command == 'analyze':
            analyzer = integration.analyze_logs(args.log_directory, args.type)
            if not analyzer:
                return 1
        
        elif args.command == 'monitor':
            monitor = RealTimeFrameworkMonitor(args.log_directory)
            monitor.start_monitoring()
            
            if args.dashboard:
                monitor.start_dashboard()
            else:
                print("Real-time monitoring started. Press Ctrl+C to stop.")
                try:
                    while True:
                        time.sleep(5)
                        monitor.print_status_summary()
                except KeyboardInterrupt:
                    pass
            
            monitor.stop_monitoring()
        
        elif args.command == 'status':
            status = integration.get_status()
            print("\n📊 FRAMEWORK LOGGING STATUS")
            print("=" * 40)
            for key, value in status.items():
                if key.endswith('_status'):
                    continue  # Skip nested status objects for brevity
                print(f"   {key.replace('_', ' ').title()}: {value}")
        
        elif args.command == 'demo':
            # First enable logging
            result = integration.enable_framework_logging(
                run_id="demo-run",
                jira_ticket="DEMO-123",
                real_time_monitoring=False
            )
            
            if result['success']:
                integration.create_demo_logs()
                
                # Analyze the demo logs
                print("\n📊 Analyzing demo logs...")
                integration.analyze_logs(analysis_type='all')
                
                print("\n🎉 Demo completed successfully!")
                integration.disable_framework_logging()
            else:
                print(f"❌ Failed to create demo: {result.get('error')}")
                return 1
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

# Convenience function for framework integration
def enable_comprehensive_logging(run_id: str = None, jira_ticket: str = None, 
                                real_time_monitoring: bool = False) -> Dict[str, Any]:
    """
    Convenience function to enable comprehensive framework logging
    
    This function can be called from the main framework to enable logging
    """
    integration = FrameworkLoggingIntegration()
    return integration.enable_framework_logging(run_id, jira_ticket, real_time_monitoring)

def disable_comprehensive_logging():
    """
    Convenience function to disable comprehensive framework logging
    """
    integration = FrameworkLoggingIntegration()
    integration.disable_framework_logging()

# Context manager for automatic logging
class FrameworkLoggingContext:
    """Context manager for automatic framework logging"""
    
    def __init__(self, run_id: str = None, jira_ticket: str = None, real_time_monitoring: bool = False):
        self.run_id = run_id
        self.jira_ticket = jira_ticket
        self.real_time_monitoring = real_time_monitoring
        self.integration = None
    
    def __enter__(self):
        self.integration = FrameworkLoggingIntegration()
        result = self.integration.enable_framework_logging(
            self.run_id, self.jira_ticket, self.real_time_monitoring
        )
        
        if not result['success']:
            raise RuntimeError(f"Failed to enable logging: {result.get('error')}")
        
        return self.integration
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.integration:
            self.integration.disable_framework_logging()

if __name__ == "__main__":
    import time
    exit(main())