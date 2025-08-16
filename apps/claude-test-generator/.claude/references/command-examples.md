# Command Examples and Usage Patterns

## Environment Setup Commands

### Command Chaining
Always chain commands after setup to maintain session state:

```bash
# Correct: source setup_clc qe6 && oc whoami && oc get namespaces
# Avoid: Running setup_clc separately from oc commands
```

### Login Format
Generated test cases MUST use generic `oc login` commands for team usability:

```bash
# Format: oc login https://api.cluster-url.com:6443 -u username -p password --insecure-skip-tls-verify
```

## Output Structure

```
runs/
├── <TICKET-ID>/                     # Main ticket folder (e.g., ACM-22079/)
│   ├── run-001-YYYYMMDD-HHMM/      # First run with timestamp
│   │   ├── Complete-Analysis.md     # Comprehensive analysis
│   │   ├── Test-Cases.md           # Clean test cases only
│   │   └── metadata.json           # Run metadata and settings
│   ├── run-002-YYYYMMDD-HHMM/      # Additional runs
│   └── latest -> run-XXX-YYYYMMDD-HHMM  # Symlink to latest run
```

## AI Service Integration

All bash operations are now handled through AI services for robust, consistent execution:

- **Environment Commands**: AI manages setup and validation workflows
- **Investigation Commands**: AI services handle GitHub, JIRA, and documentation analysis
- **Validation Commands**: AI performs intelligent output validation
- **Testing Commands**: AI orchestrates cluster testing and verification