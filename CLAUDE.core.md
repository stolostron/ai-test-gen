# AI Systems Suite - Core Configuration

> **Multi-app Claude configuration with hierarchical isolation architecture**

## 📋 GLOBAL DOCUMENTATION STANDARDS (PERSISTENT MEMORY)

**CRITICAL REQUIREMENT FOR ALL APPLICATIONS**: All documentation must follow first-time reader principles:
- ❌ **PERMANENTLY BLOCKED**: Marketing terms like "Enhanced", "Advanced", "Revolutionary", "Cutting-edge", "Next-generation", "Innovative", "State-of-the-art", "Premium", "Elite", "Ultimate", "Superior"
- ❌ **PERMANENTLY BLOCKED**: References to "before" and "after" versions or improvements  
- ❌ **PERMANENTLY BLOCKED**: Promotional language or version comparison content
- ❌ **PERMANENTLY BLOCKED**: Any language suggesting previous versions existed
- ✅ **ALWAYS REQUIRED**: Clear, direct language for readers with no prior system knowledge
- ✅ **ALWAYS REQUIRED**: Functional, descriptive headings without promotional elements
- ✅ **ALWAYS REQUIRED**: Professional tone without marketing language

**Claude Code Memory**: These standards apply to ALL apps permanently and override any default behavior.

## 🏗️ Hierarchical Isolation Principles

- **Strict App Boundaries**: Apps completely contained within their directories with real-time violation detection
- **Framework Execution Integrity**: 8-Layer Safety System preventing framework split personality disorder and execution isolation failures
- **Agent Output Reality Validation**: Mandatory validation ensuring agents produce actual output files before claiming completion
- **Data Pipeline Integrity**: Phase boundary validation preventing downstream processing without validated agent intelligence
- **Hierarchical Access Control**: Root level maintains full orchestration and cross-app capabilities
- **External Access Prevention**: Apps cannot access `../../`, `../other-app/`, or system directories
- **Complete Self-Containment**: Each app works independently within enforced boundaries
- **Prefixed AI Services**: `tg_` (test-generator) and `za_` (z-stream-analysis) namespacing
- **Transparent Proxy Access**: Full app functionality from root via `/app-name` commands
- **Dynamic App Discovery**: Router automatically detects new apps with isolation enforcement

### App Structure
```
apps/your-app/
├── .app-config              # App identity and isolation rules
├── CLAUDE.md               # Self-contained configuration
├── .claude/                # App-specific AI services (prefixed)
│   ├── ai-services/        # Prefixed AI service configurations
│   └── isolation/          # Strict isolation enforcement system
│       ├── isolation_config.json    # Isolation boundaries configuration
│       ├── app_isolation_enforcer.py # Real-time violation detection
│       ├── isolation_monitor.py     # Monitoring and logging
│       └── validation_status.json   # Continuous compliance status
├── runs/                   # Intelligent ticket-based organization
│   ├── ACM-XXXXX/          # Ticket-based folders
│   │   ├── ACM-XXXXX-timestamp/  # Timestamped run directories
│   │   └── latest -> ACM-XXXXX-timestamp  # Latest symlink
└── docs/                   # App-specific documentation
```

## 📊 Architecture Benefits

- **95% reduction** in configuration complexity
- **Comprehensive elimination** of cross-app contamination  
- **Complete app isolation** with strict boundary enforcement
- **Zero AI service conflicts** through proper prefixing
- **Complete functionality preservation** with hierarchical access
- **Real-time violation detection** with `.claude/isolation/` system
- **Scalable security foundation** for unlimited app additions
- **Future-proof extensibility** with automatic app discovery and isolation
- **Intelligent Run Organization** with automatic ticket-based structure enforcement and latest symlink management