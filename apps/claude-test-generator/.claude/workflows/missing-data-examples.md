# Missing Data Handling Examples

## Example Missing Data Report Template

```bash
🚨 MISSING DATA IDENTIFIED:
- ACM-22730: No PR attached (UI menu structure)
- Figma designs: Access denied (user workflows)  
- Backend architecture: Still being decided

✅ AVAILABLE FOR TESTING:
- ClusterPermissions CRD operations (any ACM-enabled cluster)
- Mock client API functionality  
- Backend infrastructure readiness

🌐 ENVIRONMENT OPTIONS:
- QE Environment: source setup_clc qe6
- Custom Clusters: export KUBECONFIG=/path/to/kubeconfig

📋 RECOMMENDATION: 
Execute available backend tests now on any environment, expand to UI testing when missing components are deployed.
```

## Framework Response Examples

### When PR Links Are Missing
```bash
⚠️ SCOPE LIMITATION: Cannot generate UI test cases for ACM-22730 (Overview menu)
- Missing: GitHub PR with implementation details
- Impact: Cannot validate actual menu structure or navigation flows
- Alternative: Generate API-level tests for backend readiness
```

### When Design Specifications Are Inaccessible
```bash
🔍 DESIGN ACCESS ISSUE: Figma design document requires authentication
- Missing: UX workflow specifications and user interaction patterns
- Impact: Cannot create end-to-end user journey test cases
- Alternative: Focus on API contract testing and backend validation
```

### When Backend Architecture Is Undefined
```bash
📋 ARCHITECTURE UNCERTAINTY: Backend implementation still being decided
- Missing: Final CRD specifications and API contracts
- Impact: Cannot generate integration test cases
- Alternative: Test available CRDs and prepare for future backend updates
```

## Investigation Checklist Examples

### Linked Ticket Analysis Template
```bash
TICKET: ACM-20640 (Main Story)
├── SUBTASKS (43 total)
│   ├── ACM-22611 ✅ Routes/Menu (Resolved) → PR: Check implementation
│   ├── ACM-22730 ❌ Overview Menu (New) → No PR attached
│   └── ACM-22925 🔄 RoleAssignment CRD (In Progress) → PR #4858
├── DEPENDENCIES
│   ├── ACM-22799 (QE) → Check for test specifications
│   └── ACM-22800 (QE Automation) → Check for automation requirements
├── BLOCKING EPICS
│   ├── HPUX-354 → Fine-grained RBAC requirements
│   └── HPUX-790 → UXD Phase II specifications
└── RELATED TICKETS
    └── ACM-18473 → Previous RBAC work context
```

### PR Investigation Template
```bash
PR ANALYSIS: https://github.com/stolostron/console/pull/4858
├── STATUS: In final review, awaiting approval
├── IMPLEMENTATION: RoleAssignment CRD modifications
├── FILES CHANGED: [List specific files and changes]
├── FUNCTIONALITY: [Describe what features are implemented]
└── DEPLOYMENT STATUS: [Determine if changes are live in test environment]
```