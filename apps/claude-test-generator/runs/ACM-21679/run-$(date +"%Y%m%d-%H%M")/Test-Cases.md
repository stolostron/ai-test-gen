# E2E Test Cases: ACM-21679 - End to end testing of live migration tech preview

## Test Case 1: Validate CNV infrastructure and VM lifecycle management on hub cluster

**Description**: Verify that Container Native Virtualization is properly deployed and functional on the ACM hub cluster, with ability to create, manage, and perform basic VM operations as foundation for cross-cluster migration testing.

**Setup**: 
- ACM hub cluster with CNV operator deployed
- Sufficient compute and storage resources for VM operations
- Network connectivity configured for VM access
- Valid VM images available for testing

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-url> --username=<username> --password=<password>` | Login successful and cluster access confirmed |
| **Step 2: Verify CNV operator deployment** - Check HyperConverged operator status: `oc get hyperconverged -n openshift-cnv` | ```<br>NAME                      AGE<br>kubevirt-hyperconverged   28h<br>``` |
| **Step 3: Validate KubeVirt deployment** - Check KubeVirt resource status: `oc get kubevirt -A` | ```<br>NAMESPACE       NAME                               AGE   PHASE<br>openshift-cnv   kubevirt-kubevirt-hyperconverged   28h   Deployed<br>``` |
| **Step 4: Check existing virtual machines** - List current VMs: `oc get virtualmachines --all-namespaces` | ```<br>NAMESPACE       NAME                AGE   STATUS    READY<br>default         fedora-dev          27h   Running   True<br>openshift-cnv   rhel10-levenhagen   27h   Running   True<br>``` |
| **Step 5: Create test virtual machine** - Apply VM definition: `oc apply -f test-vm.yaml` | VM created successfully and shows in Running state within 5 minutes |
| **Step 6: Verify VM migration capabilities** - Check migration CRDs: `oc get crd \| grep migration` | ```<br>migrationpolicies.migrations.kubevirt.io<br>virtualmachineinstancemigrations.kubevirt.io<br>``` |
| **Step 7: Test basic VM live migration** - Initiate migration within cluster: `oc apply -f vm-migration.yaml` | Migration initiated successfully and VM maintains running state during migration |
| **Step 8: Validate VM accessibility** - Connect to VM console: `virtctl console <vm-name>` | Console access successful, VM responsive and network connectivity confirmed |
| **Step 9: Check migration completion** - Monitor migration status: `oc get virtualmachineinstancemigration <migration-name> -o yaml` | Migration completed successfully with VM running on target node |
| **Step 10: Cleanup test resources** - Remove test VM and migration objects: `oc delete vm <test-vm>` | Test resources cleaned up successfully, environment ready for next test |

## Test Case 2: Investigate MTV addon deployment and cross-cluster migration preparation

**Description**: Evaluate the current state of Migration Toolkit for Virtualization (MTV) addon integration with ACM and prepare environment for cross-cluster VM migration testing.

**Setup**:
- ACM hub cluster with multiple managed clusters
- CNV deployed on participating clusters
- Network connectivity between clusters for migration traffic
- Understanding of MTV deployment requirements

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-url> --username=<username> --password=<password>` | Login successful and cluster access confirmed |
| **Step 2: Check available managed clusters** - List managed clusters: `oc get managedclusters` | ```<br>NAME                         AVAILABLE   JOINED<br>local-cluster                True        True<br>staging-cluster-01           True        True<br>clc-aws-1754999178646        Unknown     True<br>``` |
| **Step 3: Verify cluster management addons** - Check available addons: `oc get clustermanagementaddons` | Current addon list displayed without MTV addon present |
| **Step 4: Check for MTV-related CRDs** - Search for migration toolkit CRDs: `oc get crd \| grep -E "(mtv\|forklift\|migration-toolkit)"` | No MTV-specific CRDs found, indicating addon not yet deployed |
| **Step 5: Investigate managed cluster capabilities** - Check cluster claims for virtualization: `oc get managedcluster <cluster-name> -o yaml \| grep -A 10 clusterClaims` | Cluster capabilities listed without specific virtualization claims |
| **Step 6: Verify CNV deployment on managed clusters** - Check via ManagedClusterView: Create ManagedClusterView for CNV resources | CNV status on managed clusters assessed for migration readiness |
| **Step 7: Test basic cluster connectivity** - Verify network paths: `oc get managedcluster <cluster> -o jsonpath='{.status.conditions}'` | Cluster connectivity confirmed, ready for future migration setup |
| **Step 8: Document MTV deployment requirements** - Research MTV addon prerequisites: Review ACM-22348 epic requirements | MTV deployment requirements documented for future implementation |
| **Step 9: Prepare migration network configuration** - Plan cross-cluster networking: Document network requirements for VM migration | Network configuration plan prepared for MTV deployment |
| **Step 10: Create MTV deployment readiness report** - Summarize current state and requirements: Document findings and next steps | Readiness report created with deployment roadmap and prerequisites |

## Test Case 3: Validate ACM console integration for virtual machine management

**Description**: Test the current state of ACM console features for virtual machine visibility and management, preparing for future live migration UI integration.

**Setup**:
- ACM console accessible via hub cluster
- Virtual machines running on hub and managed clusters
- Search functionality enabled for resource discovery
- User permissions configured for VM management

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-url> --username=<username> --password=<password>` | Login successful and cluster access confirmed |
| **Step 2: Access ACM console** - Navigate to ACM web interface: Open browser to ACM console URL | ACM console accessible with proper authentication |
| **Step 3: Navigate to Infrastructure section** - Find virtual machine management: Browse to Infrastructure > Virtual Machines | Infrastructure section accessible, VM management area located |
| **Step 4: Test VM search functionality** - Search for virtual machines: Use global search for VM resources | Search results show VMs from hub cluster: fedora-dev, rhel10-levenhagen |
| **Step 5: Verify VM details display** - Check VM information: Click on VM to view details | VM details displayed including status, resource usage, and basic information |
| **Step 6: Test cluster-wide VM visibility** - Search across managed clusters: Query for VMs on different clusters | ```<br>Results show VMs from multiple clusters with cluster context:<br>- local-cluster: fedora-dev, rhel10-levenhagen<br>- staging-cluster-01: (VM status from managed cluster)<br>``` |
| **Step 7: Check available VM actions** - Review action menu: Right-click or action menu on VM | Available actions displayed, migration actions noted as unavailable (development phase) |
| **Step 8: Test VM filtering and sorting** - Use console filters: Filter VMs by cluster, status, or other criteria | Filtering functionality works for organizing VM views across clusters |
| **Step 9: Verify RBAC integration** - Test permission model: Attempt VM operations with different user roles | RBAC properly enforced, appropriate permissions required for VM management |
| **Step 10: Document UI enhancement requirements** - Capture current limitations: Note missing features for live migration support | UI enhancement requirements documented for MTV integration and cross-cluster actions |

## Test Case 4: Test VM snapshot and backup capabilities in preparation for migration scenarios

**Description**: Validate virtual machine snapshot and backup functionality that will support migration rollback and data protection during cross-cluster migrations.

**Setup**:
- VMs running with persistent volumes
- Snapshot functionality enabled in CNV
- Storage classes supporting volume snapshots
- Backup and restore tools available

| Step | Expected Result |
|------|-----------------|
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login <cluster-url> --username=<username> --password=<password>` | Login successful and cluster access confirmed |
| **Step 2: Verify snapshot CRDs availability** - Check snapshot capabilities: `oc get crd \| grep snapshot` | ```<br>virtualmachinesnapshotcontents.snapshot.kubevirt.io<br>virtualmachinesnapshots.snapshot.kubevirt.io<br>virtualmachinerestores.snapshot.kubevirt.io<br>``` |
| **Step 3: Create VM snapshot** - Take snapshot of running VM: `oc apply -f vm-snapshot.yaml` | VM snapshot created successfully without interrupting VM operation |
| **Step 4: Verify snapshot status** - Check snapshot completion: `oc get virtualmachinesnapshot <snapshot-name> -o yaml` | ```<br>status:<br>  phase: Succeeded<br>  readyToUse: true<br>  creationTime: "2025-08-13T..."<br>``` |
| **Step 5: Test snapshot content validation** - Verify snapshot data: `oc get virtualmachinesnapshotcontent <content-name> -o yaml` | Snapshot content shows valid data references and storage information |
| **Step 6: Create VM from snapshot** - Restore VM from snapshot: `oc apply -f vm-restore.yaml` | New VM created from snapshot data with identical configuration |
| **Step 7: Validate restored VM functionality** - Test restored VM: Start and connect to restored VM | Restored VM boots successfully with same data and configuration as original |
| **Step 8: Test export functionality** - Export VM for migration: `oc apply -f vm-export.yaml` | ```<br>VM export created successfully:<br>virtualmachineexport/<export-name> created<br>Export URL generated for download<br>``` |
| **Step 9: Verify export accessibility** - Download VM export: Access export URL to retrieve VM data | VM export accessible and downloadable, suitable for cross-cluster import |
| **Step 10: Cleanup snapshot resources** - Remove test snapshots: `oc delete virtualmachinesnapshot <snapshot-name>` | Snapshot resources cleaned up successfully, storage reclaimed |