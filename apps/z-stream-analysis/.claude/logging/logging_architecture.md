# Z-Stream Analysis Comprehensive Logging Architecture

> **Claude Code Native Hook-Based Logging System for Complete Pipeline Analysis Observability**

## 🎯 **Design Goals**

Based on test-generator comprehensive logging system, implement enterprise-grade logging for z-stream-analysis with:

- **Complete Tool Interception**: All Claude Code tool executions logged automatically
- **Service-Based Organization**: Investigation Intelligence + Solution Intelligence service tracking  
- **Run-Based Structure**: Jenkins URL analysis runs organized by pipeline ID and timestamp
- **Real-Time Monitoring**: Live monitoring of analysis progress and performance
- **Security Compliance**: Automatic credential masking and secure data handling
- **Analysis Capabilities**: Built-in log analysis and debugging tools

## 🏗️ **Architecture Overview**

### **Hook-Based Interception System**
```
Claude Code Tool Execution
           ↓
    [Logging Hook System]
           ↓
    Automatic Log Capture
           ↓
    Structured Storage
           ↓
    Real-Time Analysis
```

### **Service Integration Points**
- **Jenkins Intelligence Service**: URL parsing, console analysis, metadata extraction
- **Investigation Intelligence Service**: Evidence gathering, environment validation  
- **Solution Intelligence Service**: Classification, fix generation, reporting
- **Evidence Validation Engine**: Validation checkpoints and quality gates
- **Progressive Context Architecture**: Context inheritance tracking

## 📁 **Log Directory Structure**

```
.claude/logging/
├── framework_config.json                    # Logging configuration
├── current_run_monitor.json                 # Current active run tracking
├── comprehensive_logging_hook.py            # Main Claude Code hook implementation
├── log_analyzer.py                          # Log analysis tools
├── realtime_monitor.py                      # Real-time monitoring
└── runs/                                     # Run-based organization
    └── pipeline_analysis_RUNID_TIMESTAMP/   # e.g., alc_e2e_tests_2420_20250826_003500
        ├── master_log.jsonl                  # Master log (all entries)
        ├── execution_summary.json            # High-level run summary
        ├── analysis_metadata.json            # Analysis-specific metadata
        ├── error_log.jsonl                   # Dedicated error tracking
        ├── performance_metrics.json          # Performance and timing data
        ├── services/                         # Service-specific logs
        │   ├── jenkins_intelligence.jsonl
        │   ├── investigation_intelligence.jsonl
        │   ├── solution_intelligence.jsonl
        │   └── evidence_validation.jsonl
        ├── stages/                           # Analysis stage logs
        │   ├── stage_1_jenkins_analysis.jsonl
        │   ├── stage_2_environment_validation.jsonl
        │   ├── stage_3_evidence_correlation.jsonl
        │   ├── stage_4_classification.jsonl
        │   └── stage_5_solution_generation.jsonl
        ├── tools/                            # Tool execution logs
        │   ├── bash_commands.jsonl
        │   ├── file_operations.jsonl
        │   ├── web_requests.jsonl
        │   └── general_tools.jsonl
        ├── context/                          # Progressive context tracking
        │   ├── context_inheritance.jsonl
        │   └── context_validation.jsonl
        └── security/                         # Security and credential handling
            ├── credential_masking.jsonl
            └── sensitive_data_audit.jsonl
```

## 🎣 **Hook System Integration**

### **Primary Hook Implementation**
- **File**: `.claude/logging/comprehensive_logging_hook.py`
- **Integration**: Claude Code native hook system via `.claude/hooks.json`
- **Automatic**: Triggers on all tool executions without code changes
- **Transparent**: Zero impact on existing z-stream-analysis functionality

### **Hook Configuration**
```json
{
  "hooks": {
    "before-tool-execution": ".claude/logging/comprehensive_logging_hook.py --stage pre-tool",
    "after-tool-execution": ".claude/logging/comprehensive_logging_hook.py --stage post-tool",
    "on-analysis-start": ".claude/logging/comprehensive_logging_hook.py --stage analysis-start",
    "on-analysis-complete": ".claude/logging/comprehensive_logging_hook.py --stage analysis-complete",
    "on-service-start": ".claude/logging/comprehensive_logging_hook.py --stage service-start",
    "on-service-complete": ".claude/logging/comprehensive_logging_hook.py --stage service-complete"
  }
}
```

## 📊 **Log Entry Format**

### **Standardized JSON-L Format**
```json
{
  "timestamp": "2025-08-26T03:45:12.123Z",
  "run_id": "alc_e2e_tests_2420_20250826_003500",
  "jenkins_url": "https://jenkins-server/job/pipeline/2420/",
  "log_level": "INFO",
  "component": "INVESTIGATION_INTELLIGENCE_SERVICE",
  "stage": "jenkins_analysis",
  "action": "extract_metadata",
  "tool": "bash",
  "command": "curl -k -s https://jenkins-server/job/pipeline/2420/api/json",
  "duration_ms": 1250,
  "success": true,
  "data": {
    "input": "jenkins_url_analysis",
    "output": "metadata_extracted",
    "confidence": 0.95
  },
  "context": {
    "phase": "evidence_gathering",
    "service": "investigation_intelligence",
    "pipeline_id": "alc_e2e_tests_2420"
  },
  "security": {
    "sensitive_data_detected": false,
    "credentials_masked": false
  }
}
```

## 🔧 **Implementation Phases**

### **Phase 1: Core Hook System** ✅ Next
- Implement basic Claude Code hook integration
- Create log directory structure
- Basic tool execution interception
- Simple JSON-L logging format

### **Phase 2: Service Integration**
- Investigation Intelligence Service logging
- Solution Intelligence Service logging  
- Evidence Validation Engine logging
- Progressive Context Architecture tracking

### **Phase 3: Advanced Features**
- Real-time monitoring dashboard
- Performance metrics collection
- Error detection and alerting
- Security and credential masking

### **Phase 4: Analysis & Debugging**
- Log analysis tools
- Timeline reconstruction
- Performance bottleneck detection
- Interactive debugging interface

### **Phase 5: Production Features**
- Automatic log rotation
- Compression and archival
- Export capabilities
- Integration with notification system

## 🛡️ **Security Features**

### **Automatic Data Protection**
- **Credential Detection**: Patterns for tokens, passwords, API keys
- **URL Sanitization**: Remove sensitive parameters from Jenkins URLs  
- **Output Masking**: Mask sensitive data in tool outputs
- **Audit Trail**: Complete audit of all credential handling

### **Masked Patterns**
```python
SENSITIVE_PATTERNS = [
    r'token=[^&\s]+',
    r'password=[^&\s]+',  
    r'Authorization:\s*Bearer\s+[^\s]+',
    r'oc login.*--token=[^\s]+',
    r'export.*TOKEN.*=.*',
    r'[A-Za-z0-9]{32,}',  # API keys
]
```

## 📈 **Performance Considerations**

### **Optimization Strategy**
- **Async Logging**: Non-blocking log writes
- **Lazy Evaluation**: Expensive operations only when needed
- **Intelligent Filtering**: Configurable log levels per component
- **Batch Writing**: Buffer log entries for efficient I/O

### **Resource Impact**
- **Logging Overhead**: Target <3% execution time impact
- **Storage**: ~10-20MB per analysis run
- **Memory**: ~15-25MB additional memory usage
- **CPU**: Minimal during normal operation

## 🔍 **Monitoring & Analysis**

### **Real-Time Capabilities**
- **Live Dashboard**: Current analysis progress
- **Performance Metrics**: Execution times, bottlenecks
- **Error Alerting**: Immediate notification of issues
- **Status Export**: Current state for external monitoring

### **Analysis Tools**
- **Timeline Analysis**: Complete execution flow reconstruction
- **Service Coordination**: Investigation → Solution service interaction
- **Tool Usage Statistics**: Performance optimization opportunities
- **Error Investigation**: Root cause analysis and patterns

## 🚀 **Usage Examples**

### **Automatic Activation**
```bash
# No code changes needed - hooks activate automatically
"Analyze https://jenkins-server/job/pipeline/2420/"

# Logging automatically captures:
# - All tool executions (bash, curl, etc.)
# - Service coordination
# - Analysis stages
# - Performance metrics
# - Security handling
```

### **Manual Monitoring**
```bash
# Real-time monitoring
python .claude/logging/realtime_monitor.py --current

# Analysis of completed run  
python .claude/logging/log_analyzer.py runs/alc_e2e_tests_2420_20250826_003500/

# Export for external systems
python .claude/logging/log_analyzer.py --export json runs/latest/
```

## 🎯 **Success Metrics**

### **Functionality Goals**
- ✅ **100% Tool Capture**: All Claude Code tool executions logged
- ✅ **Zero Code Changes**: Existing z-stream-analysis unchanged
- ✅ **Complete Traceability**: Every analysis step traceable
- ✅ **Performance Monitoring**: Bottleneck identification
- ✅ **Security Compliance**: No credential exposure

### **Quality Goals**
- ✅ **Real-Time Monitoring**: Live analysis progress tracking
- ✅ **Error Detection**: Immediate issue identification
- ✅ **Analysis Tools**: Deep investigation capabilities
- ✅ **Export Integration**: Support for external monitoring
- ✅ **Production Ready**: Enterprise-grade reliability

---

**Next Steps**: Begin Phase 1 implementation with core hook system and basic tool interception.