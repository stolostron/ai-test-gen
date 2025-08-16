# Implementation Reality Validation

## 🔍 Critical Pre-Generation Validation

Before generating any test cases, the framework must verify actual implementation details to prevent assumption-based errors:

### Resource Schema Validation
- **Purpose**: Verify field existence in OpenShift/ACM custom resources before generating queries
- **Approach**: Check actual resource definitions when available
- **Graceful Handling**: If validation fails, use generic resource inspection commands and document limitations
 - **Automation**: Use AI Schema Service to dynamically generate YAML skeletons for any CRD-backed resource

### Component Architecture Discovery
- **Purpose**: Understand how ACM/OpenShift components actually operate (controllers, operators, jobs)
- **Investigation**: Identify operational patterns and log locations for accurate test commands
- **Fallback**: If architecture unclear, provide multiple validation approaches and document uncertainty

### Feature Availability Assessment ⚠️ CRITICAL
- **Purpose**: Determine if ticket features are deployed and testable in current environment
- **MANDATORY Validation**: Perform evidence-based verification of feature deployment status
- **Implementation vs. Deployment**: Clear distinction between code merged and feature available in test environment
- **Assessment**: Test basic functionality when possible to guide test plan scope
- **Adaptive Planning**: Always generate comprehensive test plan regardless of current deployment status

### ⚠️ DEPLOYMENT STATUS VALIDATION PROTOCOL

**MANDATORY EVIDENCE COLLECTION:**

1. **Container Image Verification**:
   ```bash
   # Extract running controller images
   oc get pods -n <NAMESPACE> | grep <CONTROLLER>
   oc get pod <POD> -n <NAMESPACE> -o jsonpath='{.spec.containers[0].image}'
   ```

2. **Image Build Date Analysis**:
   ```bash
   # Cross-reference with PR merge dates
   # Determine if image was built after feature implementation
   ```

3. **Feature Behavior Testing**:
   ```bash
   # Attempt to exercise new functionality
   # Verify new fields/behavior work as expected
   # Document what works vs. what's missing
   ```

4. **Version Correlation**:
   ```bash
   # Map PR merge date to product releases
   # Compare test environment version to minimum required version
   ```

**DEPLOYMENT STATUS REPORTING REQUIREMENTS:**

- **🟢 DEPLOYED**: Feature confirmed working in test environment with supporting evidence
- **🟡 PARTIALLY DEPLOYED**: Some components available, others missing - specify what works
- **🔴 NOT DEPLOYED**: Feature code merged but not yet available in test environment
- **❓ UNKNOWN**: Unable to verify - provide evidence of validation attempts

**SUPPORTING EVIDENCE MUST INCLUDE:**
- Container image digests and build correlation
- Actual feature behavior test results
- Version analysis supporting conclusions
- Specific validation commands executed

## 🎯 Adaptive Test Generation Guidelines

### Always Generate Best Possible Test Plan
- **Primary Goal**: Create comprehensive test cases even when validation information is incomplete
- **Validation Failures**: Document limitations clearly in report, but continue with test generation
- **Multiple Approaches**: Provide alternative validation methods when specific approaches fail
- **Future-Ready**: Ensure test plans work when limitations are resolved

### Graceful Validation Handling
- **Resource Fields**: If field verification fails, use generic inspection commands (`oc get resource -o yaml`)
 - **Generic Skeletons**: Generate schema-aware skeletons using AI Schema Service and `oc explain` commands
- **Component Architecture**: If unclear, provide both controller and operational logging approaches
- **Feature Deployment**: If uncertain, generate tests for both current and post-deployment scenarios
- **Clear Documentation**: Report all validation limitations and assumptions in final analysis

### OpenShift/ACM Best Practices
- **Resource Patterns**: Leverage common OpenShift custom resource structures
- **Namespace Awareness**: Consider ACM hub vs managed cluster contexts
- **Operator Patterns**: Account for standard OpenShift operator deployment patterns
- **Testing Approaches**: Use standard oc/kubectl commands that work across environments