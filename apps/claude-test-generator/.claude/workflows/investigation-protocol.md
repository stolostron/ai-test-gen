# Missing Data Intelligence & Linked Ticket Investigation

## 🔍 Comprehensive Ticket Analysis Protocol

The framework performs **thorough investigation** of all related tickets:

### Multi-Level Ticket Investigation ⚠️ ENHANCED REQUIREMENTS
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

### Missing Data Detection & Response
When critical data is missing, the framework:
- **🚨 Identifies Gaps**: Missing PRs, inaccessible designs, undefined architectures
- **📊 Quantifies Impact**: What specific testing cannot be performed
- **✅ Scopes Available Work**: Focus on testable components
- **📋 Provides Future Roadmap**: Test cases ready for when missing data becomes available

## 🎯 Investigation Quality Standards

- **100% Ticket Coverage**: Every linked ticket analyzed regardless of nesting level
- **PR Verification**: All attached PRs examined for implementation details
- **Cross-Reference Validation**: Ensuring consistency across related tickets
- **Context Preservation**: Understanding full feature history and evolution