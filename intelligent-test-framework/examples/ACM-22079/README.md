# ACM-22079 Claude Analysis Project

## Project Overview
**JIRA Ticket**: ACM-22079 - Support digest-based upgrades via ClusterCurator for non-recommended upgrades  
**Analysis Date**: January 2025  
**Analyst**: ACM QE Team  
**AI Tool**: Claude Code CLI  

## Project Structure
```
/Users/ashafi/Documents/work/ai/claude/ACM-22079/
├── README.md                          # This file - project overview
├── 01-setup/                          # Setup and configuration files
│   ├── environment-check.sh           # Verify Claude Code setup
│   ├── project-init.sh                # Initialize project
│   └── claude-config.md               # Claude Code configuration guide
├── 02-analysis/                       # Analysis files and prompts
│   ├── jira-details.md                # JIRA ticket information
│   ├── pr-analysis.md                 # Pull request details
│   ├── prompts/                       # Claude prompts library
│   │   ├── initial-analysis.txt       # First analysis prompt
│   │   ├── code-deep-dive.txt         # Code analysis prompt
│   │   ├── test-generation.txt        # Test case generation prompt
│   │   └── acm-integration.txt        # ACM QE integration prompt
│   └── sessions/                      # Claude session logs
│       └── [timestamped session files]
├── 03-results/                        # Generated analysis and test cases
│   ├── feature-analysis.md            # Conceptual and technical analysis
│   ├── implementation-details.md      # Code implementation breakdown
│   ├── test-cases/                    # Generated test cases
│   │   ├── unit-tests.md              # Unit test scenarios
│   │   ├── integration-tests.md       # Integration test scenarios
│   │   ├── e2e-tests.md               # End-to-end test scenarios
│   │   └── acm-specific-tests.md      # ACM QE specific test cases
│   └── recommendations.md             # Implementation recommendations
├── 04-implementation/                 # Implementation files
│   ├── cypress-tests/                 # Cypress test implementations
│   ├── test-data/                     # Test data and fixtures
│   ├── automation-scripts/            # Automation helper scripts
│   └── jenkins-configs/               # CI/CD configuration updates
├── 05-documentation/                  # Project documentation
│   ├── workflow-guide.md              # How to use this project
│   ├── lessons-learned.md             # Insights and best practices
│   ├── team-sharing.md                # Information for QE team
│   └── next-steps.md                  # Future work and follow-ups
└── 06-reference/                      # Reference materials
    ├── acm-codebase-links.md          # Links to ACM automation codebase
    ├── clustercurator-docs.md         # ClusterCurator documentation
    ├── pr-files/                      # Copy of PR files for reference
    └── related-tickets.md             # Related JIRA tickets and PRs
```

## Quick Start Guide

### Prerequisites
✅ Claude Code CLI installed and configured  
✅ Access to ACM automation codebase  
✅ JIRA and GitHub access  
✅ Understanding of ClusterCurator functionality  

### Getting Started
1. **Navigate to project**: `cd /Users/ashafi/Documents/work/ai/claude/ACM-22079`
2. **Run setup**: `./01-setup/project-init.sh`
3. **Start analysis**: Follow workflow in `05-documentation/workflow-guide.md`
4. **Generate tests**: Use prompts from `02-analysis/prompts/`
5. **Implement results**: Use files from `04-implementation/`

## Key Files to Start With
- `01-setup/claude-config.md` - Verify your Claude setup
- `02-analysis/jira-details.md` - Understand the JIRA ticket
- `05-documentation/workflow-guide.md` - Follow the analysis workflow
- `02-analysis/prompts/initial-analysis.txt` - First prompt to use with Claude

## Project Goals
1. 🎯 **Understand ACM-22079**: Complete technical and conceptual analysis
2. 🧪 **Generate Test Cases**: Comprehensive test suite for digest-based upgrades
3. 🔧 **Create Implementation**: Ready-to-use test automation code
4. 📚 **Document Process**: Reusable workflow for future JIRA analysis
5. 👥 **Share Knowledge**: Documentation for ACM QE team

## Success Criteria
- [ ] Complete understanding of digest-based upgrade feature
- [ ] Comprehensive test case suite generated
- [ ] Test cases implemented in ACM automation framework
- [ ] Documentation ready for team sharing
- [ ] Workflow validated and documented for reuse

## Next Steps
See `05-documentation/next-steps.md` for detailed execution plan.