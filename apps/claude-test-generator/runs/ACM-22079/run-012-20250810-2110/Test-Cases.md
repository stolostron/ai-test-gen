# Test Cases - ACM-22079
## Support digest-based upgrades via ClusterCurator for non-recommended upgrades

**Generated:** August 10, 2025  
**Target Feature:** Digest-based upgrade support for disconnected environments  
**Customer:** Amadeus - Critical requirement for production deployment

---

## Test Case 1: Complete Digest-Based Upgrade Workflow

### Description
This test case validates the complete end-to-end digest-based upgrade workflow for non-recommended OpenShift versions. It verifies that ClusterCurator can successfully resolve image digests from the conditionalUpdates API and execute upgrades without requiring force flags. This addresses Amadeus's critical requirement for reliable upgrades in disconnected environments where image tags fail to resolve.

### Setup
**Prerequisites**:
- Hub cluster login: `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 -u kubeadmin -p Ia7MN-3cr6c-C3Z5k-bvSPc --insecure-skip-tls-verify`
- Environment verification: `oc whoami && oc get managedclusters`
- ACM environment with ClusterCurator controller deployed
- Managed cluster available for upgrade testing

**Required Files**: 
- `digest-upgrade-test.yaml` (created during test execution)

| Steps | Expected Result |
|-------|-----------------|
| **Step 1: Environment Validation**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 -u kubeadmin -p Ia7MN-3cr6c-C3Z5k-bvSPc --insecure-skip-tls-verify && oc whoami && oc get managedclusters` | **Success Criteria**: Authenticated connection to ACM hub with managed clusters visible<br/><br/>**Expected Output**:<br/>```<br/>Login successful.<br/>kubeadmin<br/>NAME                          HUB ACCEPTED   JOINED   AVAILABLE   AGE<br/>local-cluster                 true           True     True        2d<br/>clc-aws-1754653080744         true           True     Unknown     2d<br/>tfitzger-rosa-hcp-demo-test   true           Unknown             2d<br/>```<br/><br/>*Confirms hub cluster access and managed cluster availability for testing* |
| **Step 2: Create ClusterCurator with Non-Recommended Version**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `cat > digest-upgrade-test.yaml << 'EOF'`<br/>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br/>`kind: ClusterCurator`<br/>`metadata:`<br/>`  name: digest-upgrade-test`<br/>`  namespace: local-cluster`<br/>`  annotations:`<br/>`    curator.open-cluster-management.io/allow-non-recommended-version: "true"`<br/>`spec:`<br/>`  desiredCuration: upgrade`<br/>`  upgrade:`<br/>`    desiredUpdate: "4.14.15"`<br/>`    channel: "stable-4.14"`<br/>`EOF && oc apply -f digest-upgrade-test.yaml` | **Success Criteria**: ClusterCurator resource created successfully with non-recommended version annotation<br/><br/>**Expected Output**:<br/>```<br/>clustercurator.cluster.open-cluster-management.io/digest-upgrade-test created<br/>```<br/><br/>**YAML Result**:<br/>```yaml<br/>apiVersion: cluster.open-cluster-management.io/v1beta1<br/>kind: ClusterCurator<br/>metadata:<br/>  name: digest-upgrade-test<br/>  annotations:<br/>    curator.open-cluster-management.io/allow-non-recommended-version: "true"<br/>status:<br/>  phase: "UpgradeInitiated"<br/>``` |
| **Step 3: Verify Digest Discovery Process**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `oc logs -n multicluster-engine deployment/cluster-curator-controller --tail=30 \| grep -E "(digest\|validateUpgradeVersion\|4.14.15)"` | **Success Criteria**: Controller logs show successful digest resolution from conditionalUpdates<br/><br/>**Expected Output**:<br/>```<br/>INFO: validateUpgradeVersion called for version 4.14.15<br/>INFO: Querying conditionalUpdates API for digest information<br/>INFO: Found digest: sha256:abc123def456... for version 4.14.15<br/>INFO: Digest-based upgrade path selected<br/>```<br/><br/>*Demonstrates the NEW validateUpgradeVersion function returning digest instead of tag* |
| **Step 4: Validate Smart Force Flag Logic**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `oc get clustercurator digest-upgrade-test -o jsonpath='{.status.upgrade.forceUpgrade}'` | **Success Criteria**: Force flag is false because digest provides exact version match<br/><br/>**Expected Output**:<br/>```<br/>false<br/>```<br/><br/>*NEW smart logic eliminates need for force flag when using digest-based upgrades* |
| **Step 5: Monitor Upgrade Progress with Digest**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `oc get clustercurator digest-upgrade-test -o jsonpath='{.status.phase}' && echo " | Method: " && oc get clustercurator digest-upgrade-test -o jsonpath='{.status.upgrade.method}'` | **Success Criteria**: Upgrade proceeds using digest-based method<br/><br/>**Expected Output**:<br/>```<br/>UpgradeInProgress | Method: digest-based<br/>```<br/><br/>**YAML Result**:<br/>```yaml<br/>status:<br/>  phase: "UpgradeInProgress"<br/>  upgrade:<br/>    method: "digest-based"<br/>    digest: "sha256:abc123def456..."<br/>    targetVersion: "4.14.15"<br/>    forceUpgrade: false<br/>``` |

---

## Test Case 2: Digest Resolution Fallback Mechanism

### Description
This test case validates the complete fallback algorithm when the primary digest source (conditionalUpdates) is unavailable or returns empty results. It tests the fallback chain: conditionalUpdates → availableUpdates → tag-based upgrade. This ensures robust operation in various network conditions and registry scenarios, critical for disconnected environment reliability.

### Setup
**Prerequisites**:
- Hub cluster login: `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 -u kubeadmin -p Ia7MN-3cr6c-C3Z5k-bvSPc --insecure-skip-tls-verify`
- Environment verification: `oc whoami && oc get managedclusters`
- Test scenario with version likely not in conditionalUpdates

**Required Files**: 
- `fallback-test.yaml` (created during test execution)

| Steps | Expected Result |
|-------|-----------------|
| **Step 1: Create Fallback Test Scenario**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `cat > fallback-test.yaml << 'EOF'`<br/>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br/>`kind: ClusterCurator`<br/>`metadata:`<br/>`  name: fallback-test`<br/>`  namespace: local-cluster`<br/>`  annotations:`<br/>`    curator.open-cluster-management.io/allow-non-recommended-version: "true"`<br/>`spec:`<br/>`  desiredCuration: upgrade`<br/>`  upgrade:`<br/>`    desiredUpdate: "4.14.99"`<br/>`    channel: "stable-4.14"`<br/>`EOF && oc apply -f fallback-test.yaml` | **Success Criteria**: ClusterCurator created with uncommon version to trigger fallback<br/><br/>**Expected Output**:<br/>```<br/>clustercurator.cluster.open-cluster-management.io/fallback-test created<br/>```<br/><br/>*Version 4.14.99 is intentionally uncommon to test fallback mechanism* |
| **Step 2: Verify conditionalUpdates Failure and Fallback Initiation**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `oc logs -n multicluster-engine deployment/cluster-curator-controller --tail=20 \| grep -E "(conditionalUpdates\|fallback\|4.14.99)"` | **Success Criteria**: Controller detects conditionalUpdates failure and initiates fallback<br/><br/>**Expected Output**:<br/>```<br/>INFO: validateUpgradeVersion called for version 4.14.99<br/>ERROR: conditionalUpdates API returned empty for version 4.14.99<br/>INFO: Initiating fallback to availableUpdates API<br/>```<br/><br/>*Shows NEW fallback algorithm detecting primary source failure* |
| **Step 3: Validate availableUpdates Fallback Success**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `oc logs -n multicluster-engine deployment/cluster-curator-controller --tail=15 \| grep availableUpdates` | **Success Criteria**: Controller successfully queries availableUpdates as secondary source<br/><br/>**Expected Output**:<br/>```<br/>INFO: Querying availableUpdates API for version 4.14.99<br/>INFO: Found digest: sha256:def456ghi789... from availableUpdates<br/>INFO: Fallback to availableUpdates successful<br/>```<br/><br/>*Demonstrates successful fallback to secondary digest source* |
| **Step 4: Confirm Complete Fallback Status**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `oc get clustercurator fallback-test -o jsonpath='{.status.upgrade.discoverySource}' && echo " | FallbackUsed: " && oc get clustercurator fallback-test -o jsonpath='{.status.upgrade.fallbackUsed}'` | **Success Criteria**: Status shows successful digest-based upgrade using fallback source<br/><br/>**Expected Output**:<br/>```<br/>availableUpdates | FallbackUsed: true<br/>```<br/><br/>**YAML Result**:<br/>```yaml<br/>status:<br/>  upgrade:<br/>    method: "digest-based"<br/>    discoverySource: "availableUpdates"<br/>    fallbackUsed: true<br/>    originalSource: "conditionalUpdates"<br/>    digest: "sha256:def456ghi789..."<br/>``` |

---

## Test Case 3: Annotation-Based Security Validation

### Description
This test case validates the NEW annotation-based security mechanism that controls access to non-recommended version upgrades. It tests both the security blocking mechanism (unauthorized attempts) and the authorization process (proper annotation). This ensures that only explicitly authorized upgrades proceed, providing enterprise-grade security controls for upgrade operations.

### Setup
**Prerequisites**:
- Hub cluster login: `oc login https://api.qe6-vmware-ibm.install.dev09.red-chesterfield.com:6443 -u kubeadmin -p Ia7MN-3cr6c-C3Z5k-bvSPc --insecure-skip-tls-verify`
- Environment verification: `oc whoami && oc get managedclusters`
- ClusterCurator controller with annotation security logic

**Required Files**: 
- `security-block-test.yaml` and `security-allow-test.yaml` (created during test execution)

| Steps | Expected Result |
|-------|-----------------|
| **Step 1: Test Security Blocking Without Authorization**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `cat > security-block-test.yaml << 'EOF'`<br/>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br/>`kind: ClusterCurator`<br/>`metadata:`<br/>`  name: security-block-test`<br/>`  namespace: local-cluster`<br/>`spec:`<br/>`  desiredCuration: upgrade`<br/>`  upgrade:`<br/>`    desiredUpdate: "4.14.15"`<br/>`    channel: "stable-4.14"`<br/>`EOF && oc apply -f security-block-test.yaml` | **Success Criteria**: ClusterCurator created but upgrade blocked due to missing annotation<br/><br/>**Expected Output**:<br/>```<br/>clustercurator.cluster.open-cluster-management.io/security-block-test created<br/>```<br/><br/>*Resource creates successfully but upgrade will be blocked by security logic* |
| **Step 2: Verify Security Blocking Mechanism**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `oc get clustercurator security-block-test -o jsonpath='{.status.phase}' && echo " | Reason: " && oc get clustercurator security-block-test -o jsonpath='{.status.conditions[?(@.type=="UpgradeBlocked")].reason}'` | **Success Criteria**: NEW security logic blocks upgrade and provides clear reason<br/><br/>**Expected Output**:<br/>```<br/>Failed | Reason: MissingNonRecommendedAnnotation<br/>```<br/><br/>*Shows NEW security gating successfully preventing unauthorized upgrades* |
| **Step 3: Create Authorized Upgrade with Proper Annotation**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `cat > security-allow-test.yaml << 'EOF'`<br/>`apiVersion: cluster.open-cluster-management.io/v1beta1`<br/>`kind: ClusterCurator`<br/>`metadata:`<br/>`  name: security-allow-test`<br/>`  namespace: local-cluster`<br/>`  annotations:`<br/>`    curator.open-cluster-management.io/allow-non-recommended-version: "true"`<br/>`spec:`<br/>`  desiredCuration: upgrade`<br/>`  upgrade:`<br/>`    desiredUpdate: "4.14.15"`<br/>`    channel: "stable-4.14"`<br/>`EOF && oc apply -f security-allow-test.yaml` | **Success Criteria**: ClusterCurator created with proper authorization annotation<br/><br/>**Expected Output**:<br/>```<br/>clustercurator.cluster.open-cluster-management.io/security-allow-test created<br/>```<br/><br/>*Creates authorized ClusterCurator with required security annotation* |
| **Step 4: Confirm Authorization and Upgrade Initiation**<br/><br/>Instructions:<br/>1. Go to your terminal<br/>2. Run the following command: `oc get clustercurator security-allow-test -o jsonpath='{.status.phase}' && echo " | Authorized: " && oc get clustercurator security-allow-test -o jsonpath='{.status.conditions[?(@.type=="NonRecommendedVersionAllowed")].status}'` | **Success Criteria**: NEW annotation logic authorizes upgrade and allows initiation<br/><br/>**Expected Output**:<br/>```<br/>UpgradeInitiated | Authorized: True<br/>```<br/><br/>**YAML Result**:<br/>```yaml<br/>status:<br/>  phase: "UpgradeInitiated"<br/>  conditions:<br/>  - type: "NonRecommendedVersionAllowed"<br/>    status: "True"<br/>    reason: "AnnotationPresent"<br/>  - type: "SecurityGatePassed"<br/>    status: "True"<br/>``` |

---

## Test Execution Summary

### Coverage Overview
- **Test Case 1**: Complete digest-based upgrade workflow (25-30 minutes)
- **Test Case 2**: Fallback mechanism validation (15-20 minutes)  
- **Test Case 3**: Security authorization validation (15-20 minutes)
- **Total Execution Time**: 55-70 minutes

### Business Value
- **Customer Impact**: Direct validation of Amadeus critical requirement
- **Production Readiness**: Comprehensive validation of disconnected environment support
- **Security Assurance**: Enterprise-grade security controls verified
- **Reliability Validation**: Fallback mechanisms ensure robust operation

### Expected Outcomes
All test cases validate the NEW digest-based upgrade functionality, ensuring reliable operation in disconnected environments while maintaining proper security controls and fallback mechanisms for various network scenarios.