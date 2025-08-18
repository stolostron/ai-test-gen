# Adding New Applications to AI Systems Suite

## Overview

This guide ensures new applications maintain complete isolation and follow established patterns.

## Required Structure

### 1. App Directory
```bash
apps/your-app-name/
├── .app-config              # App metadata and isolation config
├── CLAUDE.md               # Self-contained configuration
├── README.md               # User guide
├── docs/                   # App-specific documentation
├── runs/                   # App-specific results
└── [other app files]
```

### 2. App Configuration File (.app-config)
```json
{
  "name": "your-app-name",
  "version": "1.0",
  "description": "Brief description of app purpose",
  "isolation": true,
  "working_directory": "apps/your-app-name/",
  "ai_services_prefix": "yan",
  "dependencies": [
    "shared/docs/relevant-shared-doc.md"
  ],
  "isolation_rules": {
    "no_external_references": true,
    "no_cross_app_access": true,
    "self_contained_config": true
  },
  "capabilities": [
    "Primary capability",
    "Secondary capability"
  ]
}
```

### 3. Isolated CLAUDE.md Header
```markdown
# Application: your-app-name
# Working Directory: apps/your-app-name/
# Isolation Level: COMPLETE

## ISOLATION ENFORCEMENT
- This configuration ONLY applies in: apps/your-app-name/
- NEVER reference files outside this directory
- NEVER reference other applications
- NEVER load external configurations

## AI SERVICES PREFIX: yan
All AI services must use prefix: yan-service-name.md
```

## Isolation Requirements

### Mandatory Rules
1. **No Cross-App References**: Never reference other apps' files or directories
2. **Self-Contained**: All dependencies included or documented in .app-config
3. **Prefixed Services**: Use unique prefix for all AI service files
4. **Independent Commands**: Commands work only within app directory
5. **Isolated Storage**: Use only app-specific runs/ directory

### Forbidden Patterns
- `../` references to parent directories
- References to other apps (`apps/other-app/`)
- Shared AI service names without prefixes
- Global command definitions that conflict with other apps
- Loading configurations from outside app directory

## Testing Isolation

### Verification Checklist
- [ ] App works when moved to different location
- [ ] No references to files outside app directory
- [ ] All AI services have proper prefix
- [ ] Commands don't conflict with other apps
- [ ] Documentation is self-contained
- [ ] Results stored only in app runs/ directory

### Testing Commands
```bash
# Test app isolation:
cd apps/your-app-name/
grep -r "../" .                    # Should find no parent references
grep -r "apps/" .                  # Should find no cross-app references
grep -r "claude-test-generator" .  # Should find no other app references
grep -r "z-stream-analysis" .      # Should find no other app references
```

## Integration with Root

### Update Root CLAUDE.md
Add your app to the applications list:
```markdown
### Your App Name
**Location:** `apps/your-app-name/`
**Purpose:** Brief description of AI capabilities
**Usage:** `cd apps/your-app-name/` for specialized features
**Features:** Real data integration, universal component support (if applicable)
```

### Add Global Routing (Optional)
```markdown
/your-app-name {your-request}      # Routes to your app with complete isolation
```

## Best Practices

1. **Start Simple**: Begin with minimal functionality and expand
2. **Document Everything**: Include comprehensive README and docs
3. **Test Isolation**: Regularly verify no external dependencies
4. **Follow Patterns**: Study existing apps for guidance
5. **AI Service Design**: Consider real data integration and universal component support
6. **Professional Standards**: Implement HTML tag prevention and markdown-only formatting
7. **Quality Focus**: Design for high accuracy and user confidence

## Support

For questions about app development:
- Review existing apps: `apps/claude-test-generator/` and `apps/z-stream-analysis/`
- Check shared documentation: `shared/docs/`
- Follow isolation patterns established in this guide