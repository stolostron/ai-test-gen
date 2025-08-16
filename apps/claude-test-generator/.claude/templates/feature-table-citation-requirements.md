# Feature Table Citation Requirements

## 🚨 CITATION REQUIREMENTS FOR FEATURE TABLES

**SCOPE**: Complete reports only - feature analysis tables must include learning citations
**PURPOSE**: Help readers explore and learn more about specific ACM features
**FORMAT**: Add citations to feature descriptions, not test case summaries

## 📋 CITATION-ENHANCED FEATURE TABLE TEMPLATE

### ACM Feature Analysis Table (WITH CITATIONS)

| Feature Component | Description | Implementation Status | Learning Resources |
|-------------------|-------------|---------------------|-------------------|
| Cluster Lifecycle Management | Automated cluster provisioning and decommissioning [JIRA:ACM-22156:Closed:2024-01-15] | ✅ DEPLOYED [Code:pkg/controllers/cluster.go:89-156:c4d5e6f7] | [Docs:https://access.redhat.com/documentation/acm#cluster-lifecycle:2024-01-15] |
| Policy Governance | Security and compliance policy enforcement [JIRA:ACM-22234:Closed:2024-01-12] | ✅ DEPLOYED [Code:pkg/policy/engine.go:45-89:d7e8f9g0] | [Docs:https://access.redhat.com/documentation/acm#governance:2024-01-15] |
| Application Deployment | GitOps-based application lifecycle management [JIRA:ACM-22189:Open:2024-01-14] | 🔄 PARTIALLY DEPLOYED [GitHub:stolostron/multicloud-operators-application#456:merged:e8f9g0h1] | [Docs:https://access.redhat.com/documentation/acm#application-lifecycle:2024-01-15] |
| Observability | Multi-cluster monitoring and alerting [JIRA:ACM-22201:In Progress:2024-01-13] | 🚧 IN DEVELOPMENT [GitHub:stolostron/multicluster-observability-operator#789:open:f9g0h1i2] | [Docs:https://access.redhat.com/documentation/acm#observability:2024-01-15] |

### API Endpoint Analysis Table (WITH CITATIONS)

| Endpoint | Method | Purpose | Implementation | Learning Resources |
|----------|--------|---------|----------------|-------------------|
| `/api/v1/clusters` | POST | Create managed cluster [JIRA:ACM-22156:Closed:2024-01-15] | [Code:pkg/api/cluster.go:123-156:a1b2c3d4] | [Docs:https://access.redhat.com/documentation/acm#api-cluster-create:2024-01-15] |
| `/api/v1/policies` | GET | List governance policies [JIRA:ACM-22234:Closed:2024-01-12] | [Code:pkg/api/policy.go:78-102:b2c3d4e5] | [Docs:https://access.redhat.com/documentation/acm#api-policy-list:2024-01-15] |
| `/api/v1/applications` | PUT | Update application deployment [JIRA:ACM-22189:Open:2024-01-14] | [Code:pkg/api/application.go:234-267:c3d4e5f6] | [Docs:https://access.redhat.com/documentation/acm#api-app-update:2024-01-15] |

### Component Architecture Table (WITH CITATIONS)

| Component | Responsibility | Dependencies | Source Location | Learning Resources |
|-----------|---------------|--------------|-----------------|-------------------|
| Cluster Controller | Manages cluster lifecycle operations [JIRA:ACM-22156:Closed:2024-01-15] | Kubernetes API, RBAC | [Code:pkg/controllers/cluster.go:1-156:a1b2c3d4] | [Docs:https://access.redhat.com/documentation/acm#architecture-cluster:2024-01-15] |
| Policy Engine | Evaluates and enforces governance policies [JIRA:ACM-22234:Closed:2024-01-12] | OPA, Gatekeeper | [Code:pkg/policy/engine.go:1-234:b2c3d4e5] | [Docs:https://access.redhat.com/documentation/acm#architecture-policy:2024-01-15] |
| Application Manager | Handles GitOps application deployments [JIRA:ACM-22189:Open:2024-01-14] | ArgoCD, Flux | [Code:pkg/application/manager.go:1-189:c3d4e5f6] | [Docs:https://access.redhat.com/documentation/acm#architecture-apps:2024-01-15] |

## 🚫 TEST SUMMARY TABLES - NO CITATIONS

### Clean Test Case Summary (NO CITATIONS)

| Test Case ID | Priority | Category | Expected Result |
|--------------|----------|----------|----------------|
| TC-001 | High | Cluster Management | Cluster created successfully |
| TC-002 | Medium | Policy Governance | Policy enforced correctly |
| TC-003 | High | Application Deployment | Application deployed via GitOps |
| TC-004 | Low | Observability | Metrics collected and displayed |

**IMPORTANT**: Test summary tables maintain clean format without citations for readability and execution clarity.

## 📋 CITATION GUIDELINES FOR FEATURE TABLES

### When to Include Citations
- **Feature descriptions**: Help readers understand the feature's purpose and scope
- **Implementation status**: Provide evidence of current deployment state
- **Architecture explanations**: Link to source code and design documentation
- **API specifications**: Reference official API documentation
- **Component relationships**: Link to architectural documentation

### When NOT to Include Citations
- **Test execution steps**: Keep clean for test execution
- **Expected results**: Maintain clarity for validation
- **Priority assignments**: No citations needed for test categorization
- **Test case IDs**: Pure identifiers don't need citations

### Citation Placement Best Practices
1. **Feature Name**: Include JIRA ticket for feature development
2. **Description**: Add documentation links for learning
3. **Implementation**: Reference source code location
4. **Status**: Provide evidence of current state
5. **Learning Column**: Always include documentation links

This approach ensures feature tables serve as learning resources while keeping test execution tables clean and focused.