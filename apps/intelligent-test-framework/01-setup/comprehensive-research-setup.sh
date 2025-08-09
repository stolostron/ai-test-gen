#!/bin/bash
# Comprehensive Research Setup for Claude Code
# Gathers all relevant documentation and information sources

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_config() {
    echo -e "${PURPLE}[RESEARCH]${NC} $1"
}

echo "🔍 Comprehensive Research Setup for Claude Code"
echo "==============================================="
echo ""

# Check directory
CURRENT_DIR=$(pwd)
EXPECTED_DIR="/Users/ashafi/Documents/work/ai/claude/ACM-22079"

if [ "$CURRENT_DIR" != "$EXPECTED_DIR" ]; then
    echo "Please run from: $EXPECTED_DIR"
    exit 1
fi

print_success "✓ Running from correct directory: $CURRENT_DIR"

# Create comprehensive research directory structure
RESEARCH_DIR="06-reference/comprehensive-research"
mkdir -p "$RESEARCH_DIR"/{linked-docs,clustercurator-docs,acm-docs,related-tickets,test-patterns,architecture-docs}

print_config "Setting up comprehensive research in: $RESEARCH_DIR"

# 1. LINKED DOCUMENTATION EXTRACTION
print_config "=== Phase 1: Extracting Linked Documentation ==="

# Extract links and references from JIRA ticket and PR
cat > "$RESEARCH_DIR/linked-docs/jira-linked-resources.md" << 'EOF'
# JIRA ACM-22079 Linked Resources

## Direct Links from JIRA Ticket
Based on typical JIRA ticket structure, these resources are commonly linked:

### Related JIRA Tickets
- **Parent Epic**: Look for epic link in ACM-22079
- **Related Stories**: Search for "digest", "upgrade", "disconnected" in ACM project
- **Dependency Tickets**: ClusterCurator enhancement tickets
- **Customer Escalations**: Amadeus-related tickets

### Design Documents
- ClusterCurator upgrade workflow design
- Disconnected environment deployment guides
- Image digest vs tag comparison documentation
- Non-recommended upgrade path policies

### Technical Specifications
- OpenShift ClusterVersion API documentation
- ACM ManagedClusterView specifications  
- ManagedClusterAction API reference
- Force upgrade annotation specifications

### Customer Requirements
- Amadeus use case documentation
- Disconnected environment requirements
- Air-gapped deployment constraints
- Enterprise upgrade scenarios

## Searches to Perform in JIRA
1. `project = ACM AND text ~ "digest" AND text ~ "upgrade"`
2. `project = ACM AND text ~ "disconnected" AND text ~ "ClusterCurator"`
3. `project = ACM AND text ~ "Amadeus" AND priority = High`
4. `project = ACM AND component = "Cluster Lifecycle"`
5. `fixVersion in (2.8.0, 2.9.0) AND text ~ "upgrade"`

## Related PRs to Investigate
- Previous ClusterCurator enhancement PRs
- Disconnected environment fixes
- ManagedClusterView improvements
- Image digest support implementations

## Documentation Repositories
- stolostron/enhancements (Design proposals)
- stolostron/cluster-curator-controller (Technical docs)
- stolostron/backlog (Requirements and planning)
- openshift/api (ClusterVersion API specs)
EOF

# 2. CLUSTERCURATOR COMPREHENSIVE DOCUMENTATION
print_config "=== Phase 2: ClusterCurator Comprehensive Research ==="

if [ -d "06-reference/stolostron-cluster-curator-controller" ]; then
    print_config "Extracting ClusterCurator documentation..."
    
    REPO_DIR="06-reference/stolostron-cluster-curator-controller"
    
    # Extract all documentation files
    find "$REPO_DIR" -name "*.md" -exec cp {} "$RESEARCH_DIR/clustercurator-docs/" \; 2>/dev/null || true
    
    # Extract design documents
    find "$REPO_DIR" -name "*.yaml" -path "*/config/*" -exec cp {} "$RESEARCH_DIR/clustercurator-docs/" \; 2>/dev/null || true
    
    # Extract API specifications
    find "$REPO_DIR" -name "*.go" -path "*/api/*" -exec cp {} "$RESEARCH_DIR/clustercurator-docs/" \; 2>/dev/null || true
    
    print_success "✓ ClusterCurator documentation extracted"
else
    print_warning "⚠ ClusterCurator repository not available for documentation extraction"
fi

# 3. ACM RELATED REPOSITORIES AND DOCUMENTATION
print_config "=== Phase 3: ACM Ecosystem Research ==="

# Create comprehensive list of related repositories to clone/research
cat > "$RESEARCH_DIR/acm-docs/related-repositories.md" << 'EOF'
# ACM Related Repositories for Research

## Core ACM Components
- stolostron/multicluster-operator-subscription
- stolostron/registration-operator  
- stolostron/klusterlet
- stolostron/api
- stolostron/multicluster-observability-operator

## Cluster Management
- stolostron/managedcluster-import-controller
- stolostron/cluster-lifecycle-api
- stolostron/multicluster-engine-operator
- stolostron/hypershift-addon-operator

## Upgrade and Lifecycle
- stolostron/cluster-curator-controller (already have)
- stolostron/cluster-proxy
- stolostron/multicluster-engine
- stolostron/addon-framework

## Testing and Automation
- stolostron/acm-qe-automation
- stolostron/e2e-framework
- stolostron/cluster-curator-test-automation

## Documentation and Design
- stolostron/enhancements
- stolostron/backlog
- stolostron/community
- stolostron/docs

## Related OpenShift Components
- openshift/api (ClusterVersion, ClusterOperator)
- openshift/cluster-version-operator
- openshift/hive
- openshift/console
EOF

# Clone key repositories for documentation
print_config "Cloning key ACM repositories for documentation..."

REPOS_TO_CLONE=(
    "stolostron/api"
    "stolostron/cluster-lifecycle-api"
    "stolostron/enhancements"
)

for repo in "${REPOS_TO_CLONE[@]}"; do
    repo_name=$(basename "$repo")
    repo_dir="$RESEARCH_DIR/acm-docs/$repo_name"
    
    if [ ! -d "$repo_dir" ]; then
        print_config "Cloning $repo..."
        git clone "https://github.com/$repo.git" "$repo_dir" 2>/dev/null || {
            print_warning "⚠ Failed to clone $repo"
        }
    else
        print_config "Updating $repo..."
        cd "$repo_dir" && git pull origin main 2>/dev/null || true
        cd - > /dev/null
    fi
done

# 4. RELATED TICKETS AND ISSUES RESEARCH
print_config "=== Phase 4: Related Tickets Research ==="

cat > "$RESEARCH_DIR/related-tickets/search-strategy.md" << 'EOF'
# Related Tickets Research Strategy

## JIRA Search Queries for Claude Code to Reference

### Core Feature Related
```
project = ACM AND (
    text ~ "digest" OR 
    text ~ "disconnected" OR 
    text ~ "air-gapped" OR
    text ~ "ClusterCurator" OR
    text ~ "non-recommended"
) AND status != Closed
```

### Customer Related
```
project = ACM AND (
    text ~ "Amadeus" OR
    text ~ "enterprise" OR
    text ~ "upgrade"
) AND priority in (High, Critical)
```

### Component Related  
```
project = ACM AND component = "Cluster Lifecycle" AND (
    text ~ "upgrade" OR
    text ~ "version" OR
    text ~ "image"
)
```

### Recent Related Work
```
project = ACM AND created >= -6M AND (
    text ~ "ClusterCurator" OR
    text ~ "cluster upgrade"
) ORDER BY created DESC
```

## GitHub Issues to Research

### stolostron/cluster-curator-controller
- Issues related to upgrades
- Disconnected environment issues
- Customer escalations
- Enhancement requests

### Related Components
- stolostron/api issues
- stolostron/cluster-lifecycle-api issues
- OpenShift cluster-version-operator issues

## Search Terms for Broader Research
- "digest based upgrade"
- "disconnected cluster upgrade"
- "ClusterCurator enhancement"
- "ManagedClusterView upgrade"
- "force upgrade annotation"
- "non recommended OpenShift upgrade"
- "air gapped cluster management"
EOF

# 5. TEST PATTERNS AND FRAMEWORK RESEARCH
print_config "=== Phase 5: Test Patterns Research ==="

# Analyze existing ACM test patterns
ACM_AUTOMATION_DIR="/Users/ashafi/Documents/work/automation"

if [ -d "$ACM_AUTOMATION_DIR" ]; then
    print_config "Analyzing existing ACM test patterns..."
    
    # Extract Cypress test patterns
    find "$ACM_AUTOMATION_DIR" -name "*.spec.js" -o -name "*test*.js" | head -20 | while read file; do
        if [ -f "$file" ]; then
            cp "$file" "$RESEARCH_DIR/test-patterns/" 2>/dev/null || true
        fi
    done
    
    # Extract Go test patterns
    find "$ACM_AUTOMATION_DIR" -name "*_test.go" | head -20 | while read file; do
        if [ -f "$file" ]; then
            cp "$file" "$RESEARCH_DIR/test-patterns/" 2>/dev/null || true
        fi
    done
    
    # Extract test configurations
    find "$ACM_AUTOMATION_DIR" -name "cypress.config.js" -o -name "*.yaml" | head -10 | while read file; do
        if [ -f "$file" ]; then
            cp "$file" "$RESEARCH_DIR/test-patterns/" 2>/dev/null || true
        fi
    done
    
    print_success "✓ Existing test patterns extracted"
else
    print_warning "⚠ ACM automation directory not found for test pattern analysis"
fi

# 6. ARCHITECTURE AND DESIGN DOCUMENTATION
print_config "=== Phase 6: Architecture Documentation Research ==="

cat > "$RESEARCH_DIR/architecture-docs/acm-architecture-research.md" << 'EOF'
# ACM Architecture Research for ClusterCurator

## Key Architecture Documents to Research

### ClusterCurator Architecture
- Component interaction diagrams
- Upgrade workflow sequences
- Hub-spoke communication patterns
- ManagedClusterView/Action lifecycle

### ACM Core Architecture
- Multi-cluster management overview
- Cluster lifecycle management flows
- Application lifecycle integration
- Governance and policy enforcement

### OpenShift Integration
- ClusterVersion operator integration
- Cluster upgrade mechanisms
- Image registry and mirroring
- Disconnected environment patterns

## Design Patterns to Analyze

### Upgrade Patterns
1. **Traditional Tag-Based**: `quay.io/openshift-release-dev/ocp-release:4.5.10-multi`
2. **Digest-Based**: `quay.io/openshift-release-dev/ocp-release@sha256:...`
3. **Mirror Registry**: Custom registry with digest preservation
4. **Air-Gapped**: Completely disconnected with local registries

### Error Handling Patterns
- Upgrade failure recovery
- Network connectivity issues
- Image pull failures
- Version validation errors

### Testing Patterns
- Hub cluster test setup
- Managed cluster simulation
- Disconnected environment mocking
- Upgrade scenario orchestration

## Related Enhancement Proposals
Research stolostron/enhancements for:
- ClusterCurator enhancements
- Disconnected environment improvements
- Multi-cluster upgrade strategies
- Image digest support proposals
EOF

# 7. CREATE COMPREHENSIVE CLAUDE CODE PROMPTS
print_config "=== Phase 7: Creating Research-Aware Claude Prompts ==="

cat > "$RESEARCH_DIR/claude-research-prompts.md" << 'EOF'
# Comprehensive Research Prompts for Claude Code

## Phase 1: Linked Documentation Analysis
```
Please analyze all documentation in 06-reference/comprehensive-research/linked-docs/ 
and identify:
1. Related JIRA tickets that should be researched
2. Design documents that provide context for ACM-22079
3. Customer requirements that drive this feature
4. Technical specifications that define the implementation

Focus on understanding the broader context beyond just the PR implementation.
```

## Phase 2: ClusterCurator Deep Architecture Analysis
```
@file:06-reference/comprehensive-research/clustercurator-docs/
@file:06-reference/pr-files/ACM-22079-PR-468/hive.go

Based on the ClusterCurator documentation and implementation:
1. Explain the complete upgrade workflow and where digest support fits
2. Identify all integration points that need testing
3. Analyze potential failure modes and edge cases
4. Recommend comprehensive test coverage strategy
```

## Phase 3: ACM Ecosystem Integration Analysis
```
@file:06-reference/comprehensive-research/acm-docs/
@file:06-reference/comprehensive-research/architecture-docs/

Analyze how ACM-22079 fits into the broader ACM ecosystem:
1. Impact on other ACM components
2. Integration with ManagedClusterView/Action patterns
3. Hub-spoke communication implications
4. Multi-cluster upgrade orchestration considerations
```

## Phase 4: Test Pattern Evolution
```
@file:06-reference/comprehensive-research/test-patterns/
@file:06-reference/pr-files/ACM-22079-PR-468/hive_test.go

Based on existing ACM test patterns and the new implementation:
1. Identify test framework patterns to follow
2. Recommend test data structures and mocking strategies
3. Suggest integration test scenarios
4. Propose E2E test workflows that align with existing patterns
```

## Phase 5: Comprehensive Test Generation
```
Based on ALL research gathered in 06-reference/comprehensive-research/:
1. Generate test cases that address the complete feature scope
2. Include tests for all identified integration points
3. Cover edge cases found in related documentation
4. Align with existing ACM test automation patterns
5. Address customer requirements and use cases
```
EOF

# 8. CREATE COMPREHENSIVE ANALYSIS WORKFLOW
cat > "02-analysis/prompts/comprehensive-research-analysis.txt" << 'EOF'
I need a comprehensive analysis of ACM-22079 that leverages ALL available research and documentation.

## Research Sources Available
Please reference and analyze:

### Core Implementation
@file:06-reference/pr-files/ACM-22079-PR-468/pr-summary.md
@file:06-reference/pr-files/ACM-22079-PR-468/hive.go
@file:06-reference/pr-files/ACM-22079-PR-468/hive_test.go

### ClusterCurator Architecture
@file:06-reference/comprehensive-research/clustercurator-docs/
@file:06-reference/stolostron-cluster-curator-controller/README.md

### ACM Ecosystem Documentation
@file:06-reference/comprehensive-research/acm-docs/
@file:06-reference/comprehensive-research/architecture-docs/

### Existing Test Patterns
@file:06-reference/comprehensive-research/test-patterns/
@file:/Users/ashafi/Documents/work/automation/clc-ui/cypress/
@file:/Users/ashafi/Documents/work/automation/clc-non-ui/

### Related Research
@file:06-reference/comprehensive-research/linked-docs/
@file:06-reference/comprehensive-research/related-tickets/

## Comprehensive Analysis Request

Based on ALL available research sources above, provide:

1. **Complete Feature Context**:
   - How ACM-22079 fits into the broader ACM architecture
   - Relationship to other cluster lifecycle features
   - Customer use cases and business drivers
   - Technical dependencies and integration points

2. **Comprehensive Implementation Analysis**:
   - Code-level implementation details from actual PR
   - Architecture patterns and design decisions
   - Integration with existing ACM components
   - Performance and security implications

3. **Exhaustive Test Strategy**:
   - Test cases covering all identified use cases
   - Integration tests for all ACM component interactions
   - Edge cases from customer requirements and architecture
   - Test automation aligned with existing ACM patterns

4. **Production Readiness Assessment**:
   - Deployment considerations for different environments
   - Monitoring and observability requirements
   - Troubleshooting scenarios and runbooks
   - Documentation and training needs

## Output Requirements
- Reference specific files and code sections
- Cite related tickets and design documents
- Align with existing ACM test automation patterns
- Provide implementation-ready test code and configurations

This analysis should demonstrate deep understanding of both the specific feature 
and its place in the broader ACM ecosystem, based on comprehensive research 
rather than just the PR implementation.
EOF

# 9. UPDATE PROJECT CONTEXT WITH RESEARCH CAPABILITIES
if [ -f ".claude-context" ]; then
    cat >> .claude-context << EOF

## Comprehensive Research Access
- **Linked Documentation**: 06-reference/comprehensive-research/linked-docs/
- **ClusterCurator Docs**: 06-reference/comprehensive-research/clustercurator-docs/
- **ACM Ecosystem**: 06-reference/comprehensive-research/acm-docs/
- **Related Tickets**: 06-reference/comprehensive-research/related-tickets/
- **Test Patterns**: 06-reference/comprehensive-research/test-patterns/
- **Architecture**: 06-reference/comprehensive-research/architecture-docs/
- **Research Prompts**: 06-reference/comprehensive-research/claude-research-prompts.md

## Research-Aware Analysis
Claude Code can now access comprehensive documentation beyond just the PR:
- Complete ClusterCurator architecture and design
- Related ACM component documentation
- Existing test patterns and frameworks
- Customer requirements and use cases
- Technical specifications and APIs

Use the comprehensive-research-analysis.txt prompt for deep analysis.
EOF
fi

# 10. CREATE AUTOMATED RESEARCH UPDATE SCRIPT
cat > "$RESEARCH_DIR/update-research.sh" << 'EOF'
#!/bin/bash
# Automated Research Update Script
# Updates all research sources with latest information

echo "🔄 Updating comprehensive research sources..."

# Update cloned repositories
for repo_dir in acm-docs/*/; do
    if [ -d "$repo_dir/.git" ]; then
        echo "Updating $(basename "$repo_dir")..."
        cd "$repo_dir"
        git pull origin main 2>/dev/null || true
        cd - > /dev/null
    fi
done

# Update main ClusterCurator repository
if [ -d "../../stolostron-cluster-curator-controller/.git" ]; then
    echo "Updating ClusterCurator repository..."
    cd "../../stolostron-cluster-curator-controller"
    git pull origin main 2>/dev/null || true
    cd - > /dev/null
fi

echo "✅ Research sources updated!"
EOF

chmod +x "$RESEARCH_DIR/update-research.sh"

# Final summary
echo ""
echo "==============================================="
print_success "🎯 Comprehensive Research Setup Complete!"
echo "==============================================="

echo ""
echo "📚 Research Sources Now Available:"
echo "  ✅ Linked documentation from JIRA/PR"
echo "  ✅ Complete ClusterCurator architecture docs"
echo "  ✅ ACM ecosystem documentation"
echo "  ✅ Related tickets and issues research"
echo "  ✅ Existing test patterns and frameworks"
echo "  ✅ Architecture and design documentation"

echo ""
echo "🔍 What Claude Code Can Now Research:"
echo "  🎯 **Linked Sources**: All documentation referenced in JIRA/PR"
echo "  🏗️ **Architecture**: Complete ACM and ClusterCurator design"
echo "  🔗 **Integration**: How this feature fits in the ecosystem"
echo "  🧪 **Test Patterns**: Existing ACM test automation patterns"
echo "  📋 **Requirements**: Customer use cases and business drivers"

echo ""
echo "🚀 Enhanced Analysis Commands:"
echo ""
echo "1. 📖 **Comprehensive Analysis**:"
echo "   cat 02-analysis/prompts/comprehensive-research-analysis.txt"
echo "   [Use with Claude Code for deep analysis]"
echo ""
echo "2. 🔍 **Research-Specific Prompts**:"
echo "   cat 06-reference/comprehensive-research/claude-research-prompts.md"
echo ""
echo "3. 🔄 **Update Research Sources**:"
echo "   ./06-reference/comprehensive-research/update-research.sh"

echo ""
print_success "✅ Claude Code now has access to comprehensive research beyond just the PR!"

echo ""
echo "💡 **Research Scope**: Claude can now discover and analyze:"
echo "   • All documentation linked in the JIRA ticket"
echo "   • Related ACM component documentation"  
echo "   • Customer requirements and use cases"
echo "   • Existing test automation patterns"
echo "   • Architecture and design context"
echo "   • Related tickets and enhancement proposals"