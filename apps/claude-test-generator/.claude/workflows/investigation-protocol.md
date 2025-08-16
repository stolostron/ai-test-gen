# AI Ultrathink Investigation Protocol

## 🧠 Comprehensive AI-Powered Analysis with Deep Reasoning

The framework performs **thorough investigation** with **AI Ultrathink deep analysis** of all related tickets and code changes:

### Multi-Level Ticket Investigation ⚠️ ULTRATHINK-ENHANCED REQUIREMENTS
1. **Main Ticket Analysis**: Requirements, acceptance criteria, technical specifications - EXTRACT ALL INFORMATION
2. **All Subtasks Investigation**: Implementation status, PR links, completion state - MANDATORY deep content extraction
3. **Dependency Chain Analysis**: Blocking/blocked tickets, prerequisites - COMPLETE dependency mapping
4. **Epic Context Review**: Parent epics, strategic objectives, architectural decisions - FULL context extraction
5. **Related Ticket Mining**: Historical context, previous implementations, lessons learned - COMPREHENSIVE analysis
6. **Nested Link Traversal**: Following all linked tickets to full depth for complete context - REGARDLESS OF BRANCH AVAILABILITY
7. **⚠️ CRITICAL: Extract ALL Content from JIRA**: When external documentation is limited/unavailable, MUST extract ALL technical details, specifications, and implementation information directly from JIRA ticket content
8. **Documentation Fallback Protocol**: When docs.redhat.com or stolostron/rhacm-docs branches are unavailable, use comprehensive JIRA content extraction as primary information source

### 📚 AI Documentation Intelligence Service (NEW - MANDATORY)
**Primary Source**: Red Hat ACM Official Documentation Repository
- **Repository Analysis**: https://github.com/stolostron/rhacm-docs (branch-aware feature discovery)
- **Architecture Documentation**: Technical implementation patterns and design decisions
- **User Guide Analysis**: Feature usage patterns and expected behaviors
- **API Reference Validation**: CRD schemas and field specification verification
- **Version Correlation**: Documentation version mapping to ACM/MCE releases
- **Best Practice Extraction**: Official Red Hat recommended usage patterns
- **Configuration Intelligence**: Validated YAML examples and schema compliance

### PR and Implementation Deep Dive ⚠️ MANDATORY ENHANCED INVESTIGATION
- **⚠️ CRITICAL: PR Status Investigation**: MANDATORY detailed analysis including:
  - **PR Found**: Status (open/closed/merged), creation and merge dates, author information, repository location
  - **PR Not Found**: Explicitly document "No related PRs found" with comprehensive search criteria used
  - **Search Methodology**: Document all repositories searched, search terms used, and why PRs might not exist
- **Code Change Analysis**: When PRs found, provide actual implementation details:
  - **Specific Code Changes**: New functions, modified classes, configuration updates
  - **Implementation Details**: How the feature is technically implemented
  - **Integration Logic**: How new code integrates with existing systems
- **Implementation Timeline Analysis**: 
  - **Development Phases**: PR creation, review, merge dates
  - **Release Mapping**: Target ACM/MCE version, release cycle information
  - **Team Information**: Developer names, reviewer approvals, project ownership
- **Implementation Reality Validation**: ⚠️ MANDATORY verification of actual feature deployment status
- **Environment Feature Detection**: Active validation that implementation is live in test environment
- **Deployment Status Assessment**: Evidence-based determination of what's available for testing
- **Feature Availability Determination**: Clear distinction between implemented vs. deployed features
- **Integration Point Identification**: How components connect and interact

### ⚠️ CRITICAL: Implementation Reality Validation Protocol

**MANDATORY STEPS - NO EXCEPTIONS:**

1. **Container Image Analysis**: 
   - Extract running controller/operator image digests from test environment
   - Cross-reference image build dates with PR merge dates
   - Validate image contains the specific feature implementation

2. **Feature Behavior Verification**:
   - Test actual feature behavior in environment (not just CRD schema)
   - Verify new code paths are accessible and functional
   - Confirm implementation matches PR specifications

3. **Version Correlation Analysis**:
   - Map PR merge dates to release cycles
   - Identify minimum product version containing feature
   - Compare against test environment version

4. **Evidence-Based Status Reporting**:
   - Provide concrete evidence supporting deployment status claims
   - Document specific validation steps performed
   - Clear separation of "implemented in codebase" vs. "deployed in test env"

**FAILURE TO VALIDATE = INVALID DEPLOYMENT ASSESSMENT**

### 🧠 AI Ultrathink Deep Analysis Integration ⚠️ NEW MANDATORY STAGE

**COMPREHENSIVE COGNITIVE ANALYSIS** - This stage applies advanced AI reasoning to all gathered investigation data:

**Ultrathink Analysis Requirements**:

1. **Deep Code Impact Reasoning**:
   - AI comprehends what code modifications accomplish in business and technical terms
   - Advanced analysis of how changes affect system architecture and user experience
   - Prediction of behavioral changes and integration implications
   - Identification of potential edge cases and failure modes

2. **Architectural Implication Assessment**:
   - AI evaluates how changes affect overall system design and component relationships
   - Analysis of API contract changes and compatibility implications
   - Assessment of performance and scalability impacts
   - Security implication evaluation and risk assessment

3. **Strategic Test Optimization Intelligence**:
   - AI determines optimal testing approach balancing coverage with efficiency
   - Risk-weighted prioritization focusing on highest-impact areas
   - Cross-repository correlation analysis for automation gaps
   - Smart test scoping to minimize effort while maximizing defect detection

4. **Cross-Repository Intelligence Integration**:
   - Analysis of development-automation alignment and coverage gaps
   - Identification of automation patterns applicable to new functionality
   - Documentation synchronization assessment and recommendations
   - Strategic guidance for improving repository ecosystem health

**Ultrathink Analysis Outputs**:
- **Comprehensive Impact Report**: Natural language summary of all change implications
- **Risk-Prioritized Test Recommendations**: Optimized testing strategy focusing on critical areas
- **Scope Optimization Guidance**: Minimal viable test sets for maximum effectiveness
- **Cross-Repository Intelligence**: Automation gaps and alignment opportunities
- **Strategic Implementation Advice**: Clear, actionable recommendations for optimal outcomes

**MANDATORY ENFORCEMENT**: All investigations MUST include AI Ultrathink deep analysis stage before proceeding to test generation - NO EXCEPTIONS.

### Missing Data Detection & Response
When critical data is missing, the framework:
- **🚨 Identifies Gaps**: Missing PRs, inaccessible designs, undefined architectures
- **📊 Quantifies Impact**: What specific testing cannot be performed
- **✅ Scopes Available Work**: Focus on testable components
- **📋 Provides Future Roadmap**: Test cases ready for when missing data becomes available

## 🎯 Ultrathink-Enhanced Investigation Quality Standards

- **100% Ticket Coverage**: Every linked ticket analyzed regardless of nesting level with AI ultrathink reasoning
- **PR Verification**: All attached PRs examined for implementation details with deep code impact analysis
- **Cross-Reference Validation**: Ensuring consistency across related tickets enhanced by AI correlation analysis
- **Context Preservation**: Understanding full feature history and evolution with strategic intelligence integration
- **🧠 Ultrathink Analysis Completion**: ALL investigations must include comprehensive AI ultrathink deep analysis
- **🎯 Strategic Test Optimization**: AI-powered test scoping and prioritization based on ultrathink insights
- **🔄 Cross-Repository Intelligence**: Comprehensive analysis of development-automation alignment and gaps
- **📊 Evidence-Based Recommendations**: All strategic guidance supported by concrete ultrathink analysis and reasoning

### 🚨 Mandatory Ultrathink Integration Requirements

- ❌ **BLOCKED**: Investigation completion without AI Ultrathink deep analysis stage
- ❌ **BLOCKED**: Test strategy generation without ultrathink-informed optimization and prioritization
- ❌ **BLOCKED**: Strategic recommendations without comprehensive cognitive analysis and evidence
- ✅ **REQUIRED**: AI Ultrathink analysis for all complex changes and architectural modifications
- ✅ **REQUIRED**: Cross-repository correlation analysis for all feature implementations
- ✅ **MANDATORY**: Strategic test optimization based on ultrathink insights and recommendations

This enhanced investigation protocol ensures that all analysis benefits from advanced AI reasoning capabilities, resulting in significantly more accurate, focused, and effective test strategies that maximize quality outcomes while optimizing resource utilization.