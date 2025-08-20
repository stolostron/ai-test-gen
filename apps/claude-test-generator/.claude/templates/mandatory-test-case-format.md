# Mandatory Test Case Format Enforcement

## 🚨 **CRITICAL: ZERO-CITATION TEST CASES POLICY**

### **ABSOLUTE REQUIREMENT: Clean Test Cases File**
- ❌ **COMPLETELY BANNED**: All citations, sources, brackets, references in test cases file
- ❌ **ZERO TOLERANCE**: No `[Source: ...]`, `*[Source: ...]*`, `(Source: ...)` patterns
- ✅ **CLEAN FORMAT**: Pure test steps without any reference annotations

**ENFORCEMENT**: Framework MUST scan and BLOCK any test cases containing citation patterns.

### **Example - WRONG (Contains Citations):**
```markdown
| 1 | Log into ACM Console | Login successful *[Source: Real environment data]* |
| 2 | Create ClusterCurator | ClusterCurator created *[Source: API validation]* |
```

### **Example - CORRECT (Clean Format):**
```markdown
| 1 | Log into ACM Console | Login successful with dashboard access |
| 2 | Create ClusterCurator | ClusterCurator created successfully |
```

## 🔧 **MANDATORY: COMPLETE CLI COMMANDS + FULL YAML**

### **REQUIREMENT: Dual Method Coverage**
Every test step MUST include:
- **UI Method**: Clear verbal explanation of console navigation
- **CLI Method**: Complete executable command with full YAML manifests

### **YAML Manifest Requirements**
- **COMPLETE YAML**: Full manifest, not truncated or "etc."
- **REALISTIC VALUES**: Use real namespace, cluster names from environment
- **READY-TO-USE**: Tester can copy-paste and execute immediately

### **Example - WRONG (Incomplete):**
```markdown
Create ClusterCurator: `oc apply -f -` with ClusterCurator manifest containing digest...
```

### **Example - CORRECT (Complete):**
```markdown
**UI Method**: Console → Infrastructure → Clusters → Actions → "Upgrade cluster"  
**CLI Method**: 
```bash
oc apply -f - <<EOF
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: ClusterCurator
metadata:
  name: digest-upgrade-test
  namespace: target-cluster
  annotations:
    cluster.open-cluster-management.io/upgrade-allow-not-recommended-versions: "true"
spec:
  desiredCuration: upgrade
  cluster: target-cluster
  upgrade:
    desiredUpdate: "4.16.37"
    channel: stable-4.16
EOF
```
```

## 📊 **MANDATORY: ENHANCED EXPECTED RESULTS**

### **REQUIREMENT: Real Environment Data Integration**
- **Specific Values**: Use actual cluster names, namespaces, URLs from environment
- **Realistic Outputs**: Show actual command outputs, not generic descriptions
- **Sample YAML**: Include relevant YAML portions from real resources

### **Example Format:**
```markdown
| Monitor upgrade status | `oc get clustercurator digest-upgrade-test -n target-cluster -o yaml` | Status shows:
```yaml
status:
  conditions:
  - type: "Progressing" 
    status: "True"
    reason: "DigestDiscovery"
    message: "Processing digest upgrade to 4.16.37"
```
Curator job pod: `curator-job-abcd1234 Running` in target-cluster namespace |
```

## 🎯 **STEP STRUCTURE ENFORCEMENT**

### **MANDATORY STEP FORMAT:**
```markdown
|| Step | UI Method | CLI Method | Expected Results |
||------|-----------|------------|------------------|
|| 1 | **Console Navigation**: Navigate to Infrastructure → Clusters | **CLI Command**: `oc get managedclusters` | **Output**: List of managed clusters with Ready status |
```

### **DUAL METHOD REQUIREMENTS:**
- **UI Method**: Always start with "**Console Navigation**:" or "**UI Action**:"
- **CLI Method**: Always start with "**CLI Command**:" followed by complete executable command
- **Expected Results**: Always start with "**Output**:" or "**Status**:" followed by realistic samples

## 🚨 **FRAMEWORK BLOCKING CONDITIONS**

### **AUTOMATIC CONTENT BLOCKING:**
- ❌ **BLOCK**: Any citation patterns in test cases file
- ❌ **BLOCK**: Incomplete CLI commands or truncated YAML
- ❌ **BLOCK**: Generic expected results without specifics
- ❌ **BLOCK**: Missing UI or CLI method in any step

### **MANDATORY VALIDATION:**
- ✅ **REQUIRE**: Clean test cases with zero citations
- ✅ **REQUIRE**: Complete executable CLI commands
- ✅ **REQUIRE**: Full YAML manifests ready for copy-paste
- ✅ **REQUIRE**: Both UI and CLI methods for every step
