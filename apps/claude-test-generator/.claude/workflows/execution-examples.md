# Workflow Execution Examples

## Input Requirements

User MUST provide:
- **JIRA Ticket ID** (e.g., ACM-22079) 

User MAY provide:
- **Target Environment** (qe6, qe7, qe8, custom) - defaults to qe6
- **Custom Environment Config** (if not using standard QE environments)

**Automatic Handling:**
- **Environment setup** will be attempted via `source setup_clc <environment>`
- **Graceful fallback** if environment unavailable - test generation continues
- **Clear status reporting** about environment accessibility and feature availability

**Output Format** (markdown preferred)
**Repository Access** (public repos supported)

## Enhanced Analysis Pattern with Organized Output

```bash
# 1. Determine run directory and number
TICKET_ID="ACM-22079"  # Extract from user input or JIRA analysis
RUN_DIR="runs/${TICKET_ID}"

# Check existing runs and auto-increment
if [ -d "$RUN_DIR" ]; then
    NEXT_RUN=$(ls -1 "$RUN_DIR" | grep "^run-" | wc -l | xargs expr 1 +)
else
    mkdir -p "$RUN_DIR"
    NEXT_RUN=1
fi

# Create timestamped run directory
TIMESTAMP=$(date +%Y%m%d-%H%M)
CURRENT_RUN_DIR="$RUN_DIR/run-$(printf "%03d" $NEXT_RUN)-$TIMESTAMP"
mkdir -p "$CURRENT_RUN_DIR"

# 2. Environment setup (flexible)
ENVIRONMENT="${USER_ENVIRONMENT:-qe6}"  # Default to qe6 if not specified
echo "🌍 Setting up environment: $ENVIRONMENT"
if source setup_clc "$ENVIRONMENT" 2>/dev/null; then
    echo "✅ Environment $ENVIRONMENT ready"
    ENV_STATUS="available"
else
    echo "⚠️ Environment $ENVIRONMENT unavailable - proceeding with test generation"
    ENV_STATUS="unavailable"
fi

# 3. Systematic JIRA analysis
jira issue view $TICKET_ID --plain

# 4. Subtask and linked ticket analysis
# (Extract subtask IDs from main ticket and analyze each)

# 5. PR analysis via WebFetch
# (Extract GitHub URLs from JIRA comments and analyze)

# 6. Generate organized output files in current run directory
# Create: $CURRENT_RUN_DIR/Complete-Analysis.md
# Create: $CURRENT_RUN_DIR/Test-Cases.md  
# Create: $CURRENT_RUN_DIR/Test-Plan.md
# Create: $CURRENT_RUN_DIR/metadata.json

# 7. Update latest symlink
cd "$RUN_DIR" && ln -sfn "$(basename $CURRENT_RUN_DIR)" latest

# 8. Report completion
echo "✅ Analysis complete in: $CURRENT_RUN_DIR"
echo "📂 Quick access via: $RUN_DIR/latest/"
```

## Execution Status Reporting

```markdown
## Execution Status
**Environment**: [qe6/qe7/custom/unavailable]
**Feature Deployment**: [✅ Available / ⚠️ Partial / ❌ Not Available / 🔍 Unknown]
**Immediate Execution**: [✅ Ready / ⚠️ Limited / ❌ Requires Deployment / 🌍 Requires Environment]

### Current Limitations
- Environment access: [Details about environment accessibility]
- Feature availability: [Details about feature deployment status]
- Validation scope: [What can/cannot be validated currently]

### Future Execution
- When environment available: [All test cases executable]
- When feature deployed: [All test cases executable]  
- Alternative environments: [List other suitable environments]
```

## Example Usage Scenarios

### Scenario 1: Standard Analysis with Default Environment
```bash
# User provides: ACM-22079
# System uses: qe6 (default)
# Expected: Full analysis with qe6 environment validation
```

### Scenario 2: Custom Environment Specification
```bash
# User provides: ACM-22079, qe7
# System uses: qe7 environment
# Expected: Full analysis with qe7 environment validation
```

### Scenario 3: Environment Unavailable
```bash
# User provides: ACM-22079, custom-env
# System detects: custom-env not accessible
# Expected: Complete test plan generated for future execution
```

### Scenario 4: Feature Not Yet Deployed
```bash
# User provides: ACM-22079
# System detects: Feature implementation not in current qe6 build
# Expected: Comprehensive test plan ready for post-deployment execution
```
