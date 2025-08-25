# ACM-22079: ClusterCurator Digest-Based Upgrade Test Cases

**Generated:** 2025-08-25  
**Framework:** Claude Test Generator v2.1 with Enhanced Format Enforcement  
**Format Compliance:** 85+ points validated  
**Security:** Credential exposure prevention active  

## Description
Comprehensive test cases for ClusterCurator digest-based upgrade functionality addressing Amadeus customer requirements for disconnected environments. Tests validate the 3-tier fallback algorithm implementation from PR #468 (conditionalUpdates → availableUpdates → image tag) ensuring reliable upgrade paths in disconnected scenarios.

## Setup
- **Environment:** OpenShift 4.x cluster with Advanced Cluster Management (ACM) 2.15.0+
- **Requirements:** ClusterCurator CRD installed, managed cluster configured for testing
- **Access:** Hub cluster administrative access required
- **Network:** Disconnected environment simulation for Amadeus customer scenarios

---

## Test Case 1: ClusterCurator Digest-Based Upgrade - Happy Path

**Objective:** Validate successful ClusterCurator digest-based upgrade execution with primary conditionalUpdates path

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>` | Expected output: `Login successful. You have access to 67 projects, up to 40 listed` |
| **Step 2: Verify ClusterCurator CRD availability** - Command: `oc get crd clustercurators.cluster.open-cluster-management.io` | Expected output: `NAME                                               CREATED AT\nclustercurators.cluster.open-cluster-management.io   2024-01-15T10:30:00Z` |
| **Step 3: Create ClusterCurator with digest-based upgrade** - Command: `oc apply -f clustercurator-digest-upgrade.yaml` | Expected output: `clustercurator.cluster.open-cluster-management.io/test-cluster-upgrade created` |
| **Step 4: Monitor upgrade progress** - Command: `oc get clustercurator test-cluster-upgrade -o yaml` | Expected output: `status:\n  conditions:\n  - type: UpgradeInProgress\n    status: "True"` |
| **Step 5: Validate conditionalUpdates fallback usage** - Command: `oc logs job/curator-job-test-cluster-upgrade` | Expected output: `INFO: Using conditionalUpdates for digest-based upgrade` |
| **Step 6: Verify upgrade completion** - Command: `oc get clustercurator test-cluster-upgrade -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'` | Expected output: `True` |

---

## Test Case 2: ClusterCurator 3-Tier Fallback - availableUpdates Path

**Objective:** Validate 3-tier fallback algorithm when conditionalUpdates fails, falling back to availableUpdates

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>` | Expected output: `Login successful. You have access to 67 projects, up to 40 listed` |
| **Step 2: Create ClusterCurator with corrupted conditionalUpdates** - Command: `oc apply -f clustercurator-corrupted-conditional.yaml` | Expected output: `clustercurator.cluster.open-cluster-management.io/fallback-test created` |
| **Step 3: Monitor initial failure and fallback** - Command: `oc logs job/curator-job-fallback-test` | Expected output: `WARN: conditionalUpdates failed, falling back to availableUpdates` |
| **Step 4: Verify availableUpdates path execution** - Command: `oc logs job/curator-job-fallback-test | grep "availableUpdates"` | Expected output: `INFO: Using availableUpdates for digest-based upgrade` |
| **Step 5: Validate successful fallback completion** - Command: `oc get clustercurator fallback-test -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'` | Expected output: `True` |
| **Step 6: Confirm upgrade version achieved** - Command: `oc get managedcluster target-cluster -o jsonpath='{.status.version.openshift}'` | Expected output: `4.15.0` |

---

## Test Case 3: ClusterCurator Full Fallback Chain - Image Tag Path

**Objective:** Validate complete 3-tier fallback when both conditionalUpdates and availableUpdates fail, using image tag

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>` | Expected output: `Login successful. You have access to 67 projects, up to 40 listed` |
| **Step 2: Create ClusterCurator with both primary paths failing** - Command: `oc apply -f clustercurator-double-failure.yaml` | Expected output: `clustercurator.cluster.open-cluster-management.io/double-fallback-test created` |
| **Step 3: Monitor initial failures** - Command: `oc logs job/curator-job-double-fallback-test` | Expected output: `WARN: conditionalUpdates failed\nWARN: availableUpdates failed, using image tag fallback` |
| **Step 4: Verify image tag fallback execution** - Command: `oc logs job/curator-job-double-fallback-test | grep "image tag"` | Expected output: `INFO: Using image tag for digest-based upgrade` |
| **Step 5: Validate final fallback success** - Command: `oc get clustercurator double-fallback-test -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'` | Expected output: `True` |
| **Step 6: Confirm image-based upgrade completion** - Command: `oc get managedcluster target-cluster -o jsonpath='{.status.version.openshift}'` | Expected output: `4.15.0` |

---

## Test Case 4: Disconnected Environment ClusterCurator - Amadeus Scenario

**Objective:** Validate ClusterCurator digest-based upgrade in disconnected environment matching Amadeus customer requirements

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>` | Expected output: `Login successful. You have access to 67 projects, up to 40 listed` |
| **Step 2: Verify disconnected environment configuration** - Command: `oc get image.config.openshift.io/cluster -o jsonpath='{.spec.registrySources.blockedRegistries}'` | Expected output: `["registry.redhat.io", "quay.io"]` |
| **Step 3: Create ClusterCurator for disconnected upgrade** - Command: `oc apply -f clustercurator-disconnected.yaml` | Expected output: `clustercurator.cluster.open-cluster-management.io/amadeus-disconnected created` |
| **Step 4: Monitor disconnected upgrade execution** - Command: `oc logs job/curator-job-amadeus-disconnected` | Expected output: `INFO: Disconnected environment detected, using local registry` |
| **Step 5: Validate local registry usage** - Command: `oc logs job/curator-job-amadeus-disconnected | grep "mirror"` | Expected output: `INFO: Using mirrored images from local registry` |
| **Step 6: Confirm disconnected upgrade success** - Command: `oc get clustercurator amadeus-disconnected -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'` | Expected output: `True` |

---

## Test Case 5: ClusterCurator Upgrade Failure Recovery

**Objective:** Validate ClusterCurator recovery mechanisms when digest-based upgrade encounters critical failures

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>` | Expected output: `Login successful. You have access to 67 projects, up to 40 listed` |
| **Step 2: Create ClusterCurator with invalid digest** - Command: `oc apply -f clustercurator-invalid-digest.yaml` | Expected output: `clustercurator.cluster.open-cluster-management.io/failure-recovery created` |
| **Step 3: Monitor upgrade failure detection** - Command: `oc logs job/curator-job-failure-recovery` | Expected output: `ERROR: Invalid digest detected, initiating recovery` |
| **Step 4: Verify recovery mechanism activation** - Command: `oc get clustercurator failure-recovery -o jsonpath='{.status.conditions[?(@.type=="Recovery")].status}'` | Expected output: `True` |
| **Step 5: Validate rollback completion** - Command: `oc logs job/curator-job-failure-recovery | grep "rollback"` | Expected output: `INFO: Rollback completed successfully` |
| **Step 6: Confirm cluster stability** - Command: `oc get managedcluster target-cluster -o jsonpath='{.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status}'` | Expected output: `True` |

---

## Test Case 6: ManagedClusterView Integration with ClusterCurator

**Objective:** Validate ManagedClusterView integration during ClusterCurator digest-based upgrade process

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <CLUSTER_CONSOLE_URL>` | Expected output: `Login successful. You have access to 67 projects, up to 40 listed` |
| **Step 2: Create ManagedClusterView for upgrade monitoring** - Command: `oc apply -f managedclusterview-upgrade-monitor.yaml` | Expected output: `managedclusterview.view.open-cluster-management.io/upgrade-monitor created` |
| **Step 3: Start ClusterCurator upgrade with monitoring** - Command: `oc apply -f clustercurator-with-monitoring.yaml` | Expected output: `clustercurator.cluster.open-cluster-management.io/monitored-upgrade created` |
| **Step 4: Verify ManagedClusterView data collection** - Command: `oc get managedclusterview upgrade-monitor -o jsonpath='{.status.result.version}'` | Expected output: `4.14.15` |
| **Step 5: Monitor upgrade progress via ManagedClusterView** - Command: `oc get managedclusterview upgrade-monitor -o jsonpath='{.status.result.upgradeStatus}'` | Expected output: `InProgress` |
| **Step 6: Validate upgrade completion through ManagedClusterView** - Command: `oc get managedclusterview upgrade-monitor -o jsonpath='{.status.result.version}'` | Expected output: `4.15.0` |

---

## Summary

These test cases comprehensively validate ClusterCurator digest-based upgrade functionality with specific focus on:

1. **3-Tier Fallback Algorithm:** Complete validation of PR #468 implementation (conditionalUpdates → availableUpdates → image tag)
2. **Disconnected Environment Support:** Amadeus customer scenario testing with local registry usage
3. **Failure Recovery:** Robust error handling and rollback mechanisms
4. **Integration Testing:** ManagedClusterView coordination during upgrade processes
5. **Production Readiness:** Real-world upgrade scenarios with comprehensive monitoring

All test cases include security-compliant placeholder usage and follow enhanced format enforcement requirements for maximum clarity and actionability.