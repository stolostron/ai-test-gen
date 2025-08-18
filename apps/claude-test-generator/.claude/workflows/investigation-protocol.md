# Advanced Deep Reasoning Investigation Protocol

## 🧠 Comprehensive AI-Powered Analysis with Advanced Cognitive Processing

The framework performs **thorough investigation** with **advanced deep reasoning analysis** of all related tickets and code changes:

### Optimized Investigation Workflow with Phase 1a/1b Dependencies

#### **Phase 1a: Independent Parallel Investigation**
**Agent A (JIRA Analysis) - Comprehensive Ticket Investigation:**
1. **Main Ticket Analysis**: Requirements, acceptance criteria, technical specifications - EXTRACT ALL INFORMATION
2. **All Subtasks Investigation**: Implementation status, PR links, completion state - MANDATORY deep content extraction
3. **Dependency Chain Analysis**: Blocking/blocked tickets, prerequisites - COMPLETE dependency mapping
4. **Epic Context Review**: Parent epics, strategic objectives, architectural decisions - FULL context extraction
5. **Related Ticket Mining**: Historical context, previous implementations, lessons learned - COMPREHENSIVE analysis
6. **Nested Link Traversal**: Following all linked tickets to full depth for complete context
7. **PR Reference Extraction**: Extract all GitHub PR links and component references for Agent E
8. **Component Identification**: Identify specific components and repositories for targeted analysis

**Agent D (Environment Validation) - Parallel Independent Task:**
- Environment authentication and cluster connectivity validation
- ACM/MCE version detection and component health assessment
- Infrastructure readiness determination

#### **Phase 1b: Context-Informed Feature Detection**
**Agent E (Feature Detection) - Sequential after Agent A Completion:**
- **Input Required**: Complete JIRA context from Agent A including specific PRs and components
- **Targeted Analysis**: Use exact PR references and component details for precise deployment validation  
- **Enhanced Confidence**: Higher accuracy through context-driven analysis vs pattern guessing
- **Evidence-Based Assessment**: Specific behavioral testing based on JIRA-identified feature scope

#### **Phase 2: Enhanced Context-Aware Parallel Execution**
**Agent B (Documentation Intelligence) - Enhanced Multi-Method Approach:**
- **GitHub CLI Priority**: Primary method for enhanced documentation analysis with correct branch structure
- **Correct Branch Detection**: Use actual repository structure ({version}_stage, {version}_prod)  
- **WebFetch Fallback**: Reliable fallback when GitHub CLI unavailable
- **Intelligent Internet Search**: Automatic internet search when documentation insufficient
- **Comprehensive Synthesis**: Combine git documentation with internet research for complete understanding

**Agent C (GitHub Investigation) - AI-Powered Parallel Investigation:**
- **Input Context**: Complete JIRA context with ALL PRs and repositories from Phase 1a
- **AI Strategic Analysis**: AI service analyzes ALL PRs and determines investigation depth per PR based on impact
- **AI Investigation Planning**: AI determines focus areas, code analysis scope, and related work priority for each PR
- **Script Execution Control**: Reliable execution of AI-determined investigation plan with gh CLI priority + WebFetch fallback
- **AI Result Synthesis**: AI processes ALL investigation data to identify E2E testing implications and implementation patterns

### 📚 Enhanced AI Documentation Intelligence Service (CORRECTED)
**Primary Source**: Red Hat ACM Official Documentation Repository
- **Repository**: https://github.com/stolostron/rhacm-docs with correct branch structure
- **Branch Pattern**: {version}_stage (development), {version}_prod (production), main (fallback)
- **GitHub CLI Integration**: Enhanced analysis with gh api and gh search capabilities
- **WebFetch Fallback**: Universal compatibility when CLI unavailable
- **Intelligence Assessment**: Automatic evaluation of documentation completeness
- **Internet Research Enhancement**: Smart internet search when git documentation insufficient
- **Comprehensive Synthesis**: Combined analysis of official docs + community knowledge

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

### 🧠 Advanced Deep Reasoning Analysis Integration ⚠️ NEW MANDATORY STAGE

**COMPREHENSIVE COGNITIVE ANALYSIS** - This stage applies advanced AI reasoning to all gathered investigation data:

**Advanced Analysis Requirements**:

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

**Advanced Analysis Outputs**:
- **Comprehensive Impact Report**: Natural language summary of all change implications
- **Risk-Prioritized Test Recommendations**: Optimized testing strategy focusing on critical areas
- **Scope Optimization Guidance**: Minimal viable test sets for maximum effectiveness
- **Cross-Repository Intelligence**: Automation gaps and alignment opportunities
- **Strategic Implementation Advice**: Clear, actionable recommendations for optimal outcomes

**MANDATORY ENFORCEMENT**: All investigations MUST include advanced deep reasoning analysis stage before proceeding to test generation - NO EXCEPTIONS.

### Missing Data Detection & Response
When critical data is missing, the framework:
- **🚨 Identifies Gaps**: Missing PRs, inaccessible designs, undefined architectures
- **📊 Quantifies Impact**: What specific testing cannot be performed
- **✅ Scopes Available Work**: Focus on testable components
- **📋 Provides Future Roadmap**: Test cases ready for when missing data becomes available

## 🎯 Enhanced Investigation Quality Standards

- **100% Ticket Coverage**: Every linked ticket analyzed regardless of nesting level with advanced reasoning
- **PR Verification**: All attached PRs examined for implementation details with deep code impact analysis
- **Cross-Reference Validation**: Ensuring consistency across related tickets enhanced by AI correlation analysis
- **Context Preservation**: Understanding full feature history and evolution with strategic intelligence integration
- **🧠 Advanced Analysis Completion**: ALL investigations must include comprehensive deep reasoning analysis
- **🎯 Strategic Test Optimization**: AI-powered test scoping and prioritization based on cognitive insights
- **🔄 Cross-Repository Intelligence**: Comprehensive analysis of development-automation alignment and gaps
- **📊 Evidence-Based Recommendations**: All strategic guidance supported by concrete analysis and reasoning

### 🚨 Mandatory Advanced Analysis Requirements

- ❌ **BLOCKED**: Investigation completion without advanced deep reasoning analysis stage
- ❌ **BLOCKED**: Test strategy generation without cognitive-informed optimization and prioritization
- ❌ **BLOCKED**: Strategic recommendations without comprehensive cognitive analysis and evidence
- ✅ **REQUIRED**: Advanced reasoning analysis for all complex changes and architectural modifications
- ✅ **REQUIRED**: Cross-repository correlation analysis for all feature implementations
- ✅ **MANDATORY**: Strategic test optimization based on cognitive insights and recommendations

This enhanced investigation protocol ensures that all analysis benefits from advanced AI reasoning capabilities, resulting in significantly more accurate, focused, and effective test strategies that maximize quality outcomes while optimizing resource utilization.