# ACM Scenario Pattern Guide

## 🧠 Intelligent Test Scenario Generation for ACM

### Core Testing Philosophy

**FEATURE-FOCUSED E2E** - Every test validates real user journeys from start to finish, ensuring the feature delivers its intended business value.

---

## 🎯 Universal Testing Principles (Apply to ALL patterns)

These principles ensure consistency and quality across all test scenarios:

1. **End-to-End User Journeys** 
   - Follow complete workflows as users would experience them
   - Start from login, end with verification of results
   - Include all intermediate steps users would take

2. **RBAC Validation** 
   - Test with different user roles when relevant
   - Verify both authorized and unauthorized access
   - Consider ACM's multi-tenancy model

3. **Multi-Cluster Awareness** 
   - Remember ACM's hub-spoke architecture
   - Test cross-cluster operations when applicable
   - Validate managed cluster behaviors

4. **Integration Testing** 
   - Verify component interactions
   - Test with related ACM features
   - Validate external integrations (Ansible, etc.)

5. **Error Handling** 
   - Test failure scenarios
   - Verify error messages are helpful
   - Ensure graceful degradation

---

## 📊 Pattern Recognition Guide

The AI analyzes tickets for these signals to understand testing needs:

### Fleet Management Patterns

**Recognition Signals**:
- Keywords: cluster, provision, import, destroy, hibernate, upgrade, managedcluster, clusterpool
- Components: Cluster Lifecycle, Hive, Infrastructure
- Context: Platform providers (AWS, Azure, VMware, etc.)

**Testing Focus**:
- Cluster state transitions (pending → provisioning → ready)
- Platform-specific validations
- Resource quota and limit handling
- Addon deployment and health
- Multi-cluster registration

**Common Validation Points**:
```yaml
- Hub connectivity established
- Managed cluster registered
- Klusterlet healthy
- Required addons deployed
- Platform resources created
- Cleanup successful
```

---

### Application Management Patterns

**Recognition Signals**:
- Keywords: application, gitops, placement, subscription, channel, helm, argocd
- Components: Application Lifecycle, GitOps
- Context: Multi-cluster deployments

**Testing Focus**:
- Application definition and packaging
- Channel connectivity (Git, Helm, ObjectStorage)
- Placement rule effectiveness
- Multi-cluster targeting
- Update propagation
- Rollback capabilities

**Common Validation Points**:
```yaml
- Channel health verified
- Subscription active
- Placement rules satisfied
- Resources deployed to targets
- Application topology accurate
- Updates propagate correctly
```

---

### Policy & Governance Patterns

**Recognition Signals**:
- Keywords: policy, compliance, violation, enforcement, remediation, configuration
- Components: GRC, Policy Framework
- Context: Security and compliance requirements

**Testing Focus**:
- Policy template usage
- Placement and targeting
- Compliance evaluation
- Enforcement actions
- Remediation workflows
- Audit trail generation

**Common Validation Points**:
```yaml
- Policy syntax valid
- Placement bindings created
- Compliance status accurate
- Violations detected correctly
- Remediation successful
- Audit events captured
```

---

### Observability & Search Patterns

**Recognition Signals**:
- Keywords: metrics, monitoring, alerts, dashboard, search, query, grafana, prometheus
- Components: Observability, Search
- Context: Monitoring and troubleshooting

**Testing Focus**:
- Metric collection from clusters
- Dashboard functionality
- Alert configuration and triggering
- Search query accuracy
- Data retention policies
- Integration with Red Hat Insights

**Common Validation Points**:
```yaml
- Metrics flowing from clusters
- Dashboards displaying data
- Alerts trigger correctly
- Search returns accurate results
- Historical data accessible
- Insights recommendations available
```

---

### Security & Access Control Patterns

**Recognition Signals**:
- Keywords: rbac, role, permission, user, group, authentication, authorization, identity
- Components: Security, RBAC, Identity Management
- Context: Access control and permissions

**Testing Focus**:
- User and group management
- Role definitions and bindings
- Permission boundaries
- Multi-cluster access control
- Identity provider integration
- Audit logging

**Common Validation Points**:
```yaml
- Users can authenticate
- Roles properly scoped
- Permissions enforced correctly
- Access denied when expected
- Audit trails complete
- Identity sync working
```

---

### Infrastructure & Automation Patterns

**Recognition Signals**:
- Keywords: ansible, automation, infrastructure, credentials, hypershift, virtualization
- Components: Infrastructure, Automation, Integration
- Context: Automated operations and integrations

**Testing Focus**:
- Credential management
- Automation job execution
- Integration connectivity
- Resource provisioning
- Error handling in automation
- Status reporting

**Common Validation Points**:
```yaml
- Credentials stored securely
- Automation jobs execute
- Integration authenticated
- Resources provisioned correctly
- Errors handled gracefully
- Status accurately reported
```

---

## 🌟 Adaptive Scenario Generation

### When patterns overlap (common in ACM):

**Example**: A ticket about "RBAC for cluster provisioning"
- Combines: Fleet Management + Security patterns
- AI generates scenarios covering both aspects
- Tests cluster creation WITH permission validation

### When encountering new patterns:

**The AI's approach**:
1. Analyze feature purpose from investigation
2. Identify closest known patterns
3. Generate comprehensive E2E scenarios
4. Include universal validations (RBAC, error handling)
5. Learn from results

**Minimum viable test always includes**:
- Feature functionality validation
- Basic RBAC testing (if users involved)
- Error scenario coverage
- Integration point verification
- Resource cleanup

---

## 📋 Scenario Structure Template

Regardless of pattern, maintain consistent structure:

```markdown
## Test Case X: [Descriptive Title]

**Description:** [Complete description of what this test validates and why]

**Prerequisites:**
- [Specific requirements for this test]
- [Including ACM version, operators needed]
- [User permissions required]

**Test Scope:**
- In scope: [What this test covers]
- Out of scope: [What it doesn't cover]
- Related tests: [Other test cases that complement this]

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login...` | Login successful |
| **Step 2: [Business description]** - [Technical action] | [Specific expected outcome] |
| ... | ... |
| **Final Step: Cleanup** - [Cleanup actions] | Resources removed, no contamination |
```

---

## 🔄 Continuous Learning

### The AI improves by:
- Tracking which patterns produce successful tests
- Learning new pattern combinations
- Identifying missing test scenarios
- Adapting to new ACM features

### Pattern evolution:
- New patterns emerge from unclassified tickets
- Successful adaptations become new patterns
- Pattern library grows with each release
- Knowledge transfers across similar features

---

## ✅ Quality Checklist for All Scenarios

Before finalizing any test scenario, ensure:

- [ ] Complete E2E workflow from user perspective
- [ ] All commands include expected outputs
- [ ] RBAC considered (when applicable)
- [ ] Multi-cluster aspects tested (when applicable)
- [ ] Error scenarios included
- [ ] Integration points verified
- [ ] Cleanup steps provided
- [ ] No assumptions about environment state

---

## 🎯 Remember

**Patterns guide but don't dictate**. The investigation phase reveals what really needs testing. Use patterns as intelligent starting points, but always prioritize:

1. What the feature actually does
2. How users will actually use it
3. What could actually go wrong
4. What actually provides value

The best test scenarios come from understanding + patterns, not patterns alone.