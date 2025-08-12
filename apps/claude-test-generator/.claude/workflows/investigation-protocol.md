# Missing Data Intelligence & Linked Ticket Investigation

## 🔍 Comprehensive Ticket Analysis Protocol

The framework performs **thorough investigation** of all related tickets:

### Multi-Level Ticket Investigation
1. **Main Ticket Analysis**: Requirements, acceptance criteria, technical specifications
2. **All Subtasks Investigation**: Implementation status, PR links, completion state
3. **Dependency Chain Analysis**: Blocking/blocked tickets, prerequisites
4. **Epic Context Review**: Parent epics, strategic objectives, architectural decisions
5. **Related Ticket Mining**: Historical context, previous implementations, lessons learned
6. **Nested Link Traversal**: Following all linked tickets to full depth for complete context

### PR and Implementation Deep Dive
- **Code Change Analysis**: Actual implementation details from attached PRs
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