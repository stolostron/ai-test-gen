# ACM Test Pattern Library

## 🎯 Adaptive Testing Patterns for ACM Features

**IMPORTANT**: These are patterns the AI has learned from successful ACM test cases. They serve as helpful starting points, NOT rigid requirements. The AI adapts these patterns based on each feature's specific needs.

### Core Testing Philosophy
- **Feature-Focused E2E**: Every test validates complete user journeys
- **RBAC-Aware**: Include permission testing for all features
- **Multi-Cluster Ready**: Consider ACM's hub-spoke architecture
- **Integration-Minded**: Test how components work together

---

## 📚 Pattern Library (Continuously Learning)

### When dealing with Cluster Lifecycle & Fleet Management patterns:

**Common signals**: cluster creation, import, destroy, upgrade, hibernate, machine pools, cluster sets
**Typical user journey**:
1. Prerequisites validation (platform credentials, quotas)
2. Resource creation with appropriate RBAC
3. State monitoring and transitions
4. Integration verification (hub registration, addon installation)
5. Cleanup and resource verification

**Example the AI has learned from**:
```markdown
## Test Case: Cluster Creation and Lifecycle Management

**Description:** End-to-end validation of cluster provisioning, including creation, state verification, and addon deployment.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.cluster-url.com:6443 -u admin -p password --insecure-skip-tls-verify` | Login successful with cluster access confirmed |
| **Step 2: Create cluster namespace** - Run: `oc create namespace cluster-namespace` | Namespace created for cluster resources |
| **Step 3: Apply cluster configuration** - Apply manifest: `oc apply -f cluster-config.yaml` | Cluster provisioning initiated |
| **Step 4: Monitor cluster creation** - Check status: `oc get managedcluster` | Cluster shows as provisioning → ready |
| **Step 5: Verify hub connectivity** - Check registration: `oc get klusterletaddonconfig` | Klusterlet registered and healthy |
```

**Key learnings**: Platform-specific validations matter, state transitions are critical, addon health indicates success

---

### When dealing with Policy & Governance patterns:

**Common signals**: policy, compliance, violation, enforcement, remediation, configuration
**Typical user journey**:
1. Policy definition and template selection
2. Placement rule configuration
3. Multi-cluster deployment
4. Compliance monitoring
5. Remediation workflow (if needed)

**Example the AI has learned from**:
```markdown
## Test Case: Policy Creation and Enforcement

**Description:** Validates policy lifecycle from creation through enforcement and compliance reporting.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access hub cluster | Login successful |
| **Step 2: Create policy namespace** - Run: `oc create namespace policies` | Policy namespace ready |
| **Step 3: Apply policy configuration** - Create policy: `oc apply -f security-policy.yaml` | Policy created and validated |
| **Step 4: Verify placement** - Check placement: `oc get placementrule -n policies` | Placement shows clusters selected |
| **Step 5: Check compliance** - Monitor status: `oc get policy -A` | Policy shows compliant/non-compliant status |
```

**Key learnings**: Placement rules are critical, compliance status needs time to propagate, remediation options vary

---

### When dealing with Application Lifecycle patterns:

**Common signals**: application, gitops, subscription, channel, placement, helm, deployment
**Typical user journey**:
1. Application definition (Git/Helm/ObjectStorage)
2. Channel and subscription setup
3. Placement configuration
4. Multi-cluster deployment
5. Update and rollback validation

**Example the AI has learned from**:
```markdown
## Test Case: GitOps Application Deployment

**Description:** End-to-end GitOps application deployment across multiple clusters using subscriptions.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access hub | Login successful |
| **Step 2: Create application namespace** - Setup namespace | Namespace created |
| **Step 3: Create channel** - Define Git channel: `oc apply -f git-channel.yaml` | Channel connected to Git repo |
| **Step 4: Create subscription** - Subscribe to channel: `oc apply -f app-subscription.yaml` | Subscription active |
| **Step 5: Verify deployment** - Check app status: `oc get appsub,appsubstatus -A` | Application deployed to target clusters |
```

**Key learnings**: Channel health affects deployment, placement rules control targeting, status propagation takes time

---

### When dealing with Observability & Monitoring patterns:

**Common signals**: metrics, alerts, dashboards, search, grafana, prometheus, thanos
**Typical user journey**:
1. Observability addon enablement
2. Metric collection verification
3. Dashboard access and functionality
4. Alert configuration
5. Search and query validation

**Example the AI has learned from**:
```markdown
## Test Case: Observability Setup and Validation

**Description:** Validates observability stack deployment and metric collection across managed clusters.

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access hub | Login successful |
| **Step 2: Enable observability** - Install addon: `oc apply -f observability-config.yaml` | Observability components deployed |
| **Step 3: Verify metric collection** - Check metrics: `oc get po -n open-cluster-management-observability` | All pods running, metrics flowing |
| **Step 4: Access Grafana** - Open dashboard URL | Grafana accessible with cluster metrics |
| **Step 5: Test search** - Query resources: `oc exec -n open-cluster-management search-pod -- search "kind:pod"` | Search returns accurate results |
```

**Key learnings**: Storage requirements are significant, metric collection has delay, dashboards need customization

---

### When dealing with Security & Access Control patterns:

**Common signals**: RBAC, role, permission, user, group, authentication, authorization
**Typical user journey**:
1. User/group creation and identity setup
2. Role definition and binding
3. Permission boundary testing
4. Multi-cluster access validation
5. Audit trail verification

**Pattern guidance**: Always test both positive (access granted) and negative (access denied) scenarios

---

### When dealing with Infrastructure & Integration patterns:

**Common signals**: ansible, credentials, infrastructure environment, hypershift, virtualization
**Typical user journey**:
1. Integration setup (credentials, connections)
2. Automation workflow definition
3. Execution and monitoring
4. Result validation
5. Error handling scenarios

**Pattern guidance**: Integration points often have specific prerequisites and timing considerations

---

## 🌟 When the AI encounters patterns it hasn't seen before:

**The AI adapts by**:
1. Analyzing the feature's purpose from investigation
2. Identifying similar patterns from its knowledge
3. Creating appropriate E2E test scenarios
4. Including standard validations (RBAC, cleanup, error handling)
5. Learning from the results for future use

**Universal principles the AI applies**:
- Every feature needs E2E validation
- RBAC should be tested when relevant
- Error scenarios improve robustness
- Integration points need verification
- Cleanup prevents test contamination

---

## 📝 How to use these patterns effectively:

1. **Let investigation guide you**: The patterns are starting points, not endpoints
2. **Combine patterns as needed**: Many features involve multiple patterns
3. **Adapt to context**: Platform-specific or environment-specific needs override generic patterns
4. **Focus on user value**: Tests should validate what users actually need
5. **Learn and evolve**: Each test teaches the AI something new

---

## 🔧 Pattern Evolution

This library grows with every ticket. The AI:
- Recognizes when existing patterns don't quite fit
- Creates variations that work better
- Remembers successful adaptations
- Shares learnings across similar features

**Remember**: The best test is one that validates the feature works for real users in real scenarios. Patterns help us get there faster, but understanding the feature always comes first.