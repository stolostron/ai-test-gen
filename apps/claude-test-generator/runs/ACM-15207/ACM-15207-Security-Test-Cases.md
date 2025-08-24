# ACM-15207 Security Test Cases

## Test Case 1: Validate TLS Certificate Security Configuration in Multicluster Observability Operator

**Description**: Verify that the multicluster-observability-operator properly handles TLS certificate validation and security configuration across both secure and insecure modes, focusing on the CreateFromClient and CreateToClient methods identified in the security issue.

**Setup**: 
- ACM 2.14.0-62 environment with multicluster-observability-operator deployed
- Administrative access to OpenShift cluster
- Access to ACM Console and OpenShift CLI

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|---------|-----------|------------|------------------|
| 1 | Log into ACM Console - Access ACM Console for security configuration testing | Navigate to https://console-openshift-console.apps.{cluster-host} | oc login https://api.{cluster-host}:6443 -u kubeadmin -p {password} --insecure-skip-tls-verify=true | Successfully authenticated with admin privileges |
| 2 | Verify multicluster-observability-operator status | ACM Console → Infrastructure → Clusters → Observability | oc get pods -n ocm -l app=multicluster-observability-operator | Pod multicluster-observability-operator-xxxxx-xxxxx shows Running status (1/1) |
| 3 | Examine current TLS configuration in operator deployment | ACM Console → Administration → Workloads → Deployments → ocm namespace | oc get deployment multicluster-observability-operator -n ocm -o yaml \| grep -A 10 -B 10 TLS | Deployment YAML shows current TLS configuration settings |
| 4 | Check for existing TLS secrets and certificates | ACM Console → Administration → Workloads → Secrets → ocm namespace | oc get secrets -n ocm \| grep -E "(tls\|cert)" | List shows available TLS secrets and certificate configurations |
| 5 | Create secure TLS configuration for testing | ACM Console → Administration → Workloads → ConfigMaps → Create ConfigMap | Create ConfigMap with name: observability-tls-config, namespace: ocm, data: ca.crt containing valid CA certificate content | ConfigMap observability-tls-config created successfully with CA certificate |
| 6 | Test secure TLS mode configuration | ACM Console → Infrastructure → Clusters → Observability → Configuration | oc patch deployment multicluster-observability-operator -n ocm --type='merge' -p='{"spec":{"template":{"spec":{"containers":[{"name":"multicluster-observability-operator","env":[{"name":"TLS_CA_FILE","value":"/etc/tls/ca.crt"}]}]}}}}' | Operator deployment updated with TLS CA configuration |
| 7 | Verify secure TLS behavior in operator logs | ACM Console → Administration → Workloads → Pods → {operator-pod} → Logs | oc logs deployment/multicluster-observability-operator -n ocm \| grep -i "tls\|certificate\|secure" | Logs show secure TLS configuration and certificate validation enabled |
| 8 | Test insecure fallback mode configuration | ACM Console → Infrastructure → Clusters → Observability → Configuration | oc patch deployment multicluster-observability-operator -n ocm --type='merge' -p='{"spec":{"template":{"spec":{"containers":[{"name":"multicluster-observability-operator","env":[{"name":"TLS_CA_FILE","value":""}]}]}}}}' | Operator deployment updated to remove TLS CA configuration |

## Test Case 2: Verify Secure Metrics Pipeline Communication with TLS Certificate Validation

**Description**: Validate end-to-end metrics collection and forwarding security by testing both Prometheus federation (CreateFromClient) and Thanos Receive communication (CreateToClient) with proper TLS certificate validation.

**Setup**:
- ACM 2.14.0-62 environment with multicluster-observability-operator running
- MultiClusterObservability CR configured for testing
- Access to cluster metrics and observability components

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|---------|-----------|------------|------------------|
| 1 | Log into ACM Console - Access ACM Console for metrics pipeline security testing | Navigate to https://console-openshift-console.apps.{cluster-host} | oc login https://api.{cluster-host}:6443 -u kubeadmin -p {password} --insecure-skip-tls-verify=true | Successfully authenticated for metrics security testing |
| 2 | Create MultiClusterObservability configuration with secure TLS | ACM Console → Infrastructure → Clusters → Observability → Create MultiClusterObservability | Create MultiClusterObservability CR: name: observability-security-test, namespace: ocm, enableMetrics: true, storageConfig with thanos-object-storage | MultiClusterObservability CR observability-security-test created with secure configuration |
| 3 | Verify Prometheus metrics collection with TLS security | ACM Console → Infrastructure → Clusters → Observability → Metrics | oc get pods -n openshift-monitoring -l app.kubernetes.io/name=prometheus | Prometheus pods running and metrics collection active with secure communication |
| 4 | Test Thanos Receive communication security | ACM Console → Infrastructure → Clusters → Observability → Dashboards | oc get pods -n ocm -l app.kubernetes.io/name=thanos-receive | Thanos Receive pods show Running status with secure communication configured |
| 5 | Validate metrics forwarding with certificate verification | ACM Console → Infrastructure → Clusters → Observability → Query | oc exec -n ocm deployment/observability-thanos-query -- curl -s "http://localhost:9090/api/v1/query?query=up" | Query returns metrics data confirming secure end-to-end communication |
| 6 | Check TLS certificate validation in forwarder logs | ACM Console → Administration → Workloads → Pods → {metrics-collector-pod} → Logs | oc logs -n openshift-addon-observability {metrics-collector-pod} \| grep -E "(tls\|certificate\|verification)" | Logs confirm TLS certificate verification enabled for both CreateFromClient and CreateToClient |
| 7 | Test certificate rotation scenario | ACM Console → Administration → Workloads → Secrets → Rotate certificates | oc delete secret observability-tls-secret -n ocm && oc create secret tls observability-tls-secret --cert=new-cert.pem --key=new-key.pem -n ocm | Certificate rotation successful, metrics communication continues with new certificates |
| 8 | Verify metrics data integrity after security configuration | ACM Console → Infrastructure → Clusters → Observability → Dashboards → Security Metrics | oc exec -n ocm deployment/observability-thanos-query -- curl -s "http://localhost:9090/api/v1/query?query=cluster_infrastructure_provider" | Metrics data shows consistent collection with secure TLS communication maintained |

## Test Case 3: Test Security Fallback Behavior and Certificate Lifecycle Management

**Description**: Comprehensive testing of InsecureSkipVerify fallback scenarios, certificate expiration handling, and security event monitoring to validate the complete security behavior identified in ACM-15207.

**Setup**:
- ACM 2.14.0-62 environment with full observability stack
- Certificate management tools and test certificates
- Security monitoring and audit logging enabled

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|---------|-----------|------------|------------------|
| 1 | Log into ACM Console - Access ACM Console for certificate lifecycle and security fallback testing | Navigate to https://console-openshift-console.apps.{cluster-host} | oc login https://api.{cluster-host}:6443 -u kubeadmin -p {password} --insecure-skip-tls-verify=true | Successfully authenticated for comprehensive security testing |
| 2 | Create test scenario with no TLS configuration | ACM Console → Administration → Workloads → ConfigMaps → Remove TLS configs | oc delete configmap observability-tls-config -n ocm --ignore-not-found=true | TLS configuration removed to trigger InsecureSkipVerify fallback |
| 3 | Verify InsecureSkipVerify fallback activation | ACM Console → Administration → Workloads → Pods → {operator-pod} → Logs | oc logs deployment/multicluster-observability-operator -n ocm --tail=50 \| grep -E "(InsecureSkipVerify\|nosec G402\|fallback)" | Logs show InsecureSkipVerify fallback activated with security exemption comments |
| 4 | Test with expired certificate scenario | ACM Console → Administration → Workloads → Secrets → Create expired cert | Create TLS Secret: name: expired-tls-secret, namespace: ocm, type: kubernetes.io/tls with expired certificate data | Secret expired-tls-secret created with intentionally expired certificate |
| 5 | Monitor security events and warnings | ACM Console → Administration → Events → Filter by Warning | oc get events -n ocm --sort-by='.lastTimestamp' \| grep -E "(security\|tls\|certificate\|warning)" | Security events show appropriate warnings for insecure configuration |
| 6 | Validate security audit logging | ACM Console → Administration → Cluster Settings → Global Configuration → Audit | oc logs -n openshift-kube-apiserver-operator deployment/kube-apiserver-operator \| grep -E "(observability\|tls\|insecure)" | Audit logs record security configuration changes and insecure modes |
| 7 | Test certificate validation enforcement | ACM Console → Infrastructure → Clusters → Observability → Security Settings | oc patch deployment multicluster-observability-operator -n ocm --type='merge' -p='{"spec":{"template":{"spec":{"containers":[{"name":"multicluster-observability-operator","env":[{"name":"TLS_VERIFY_CERTS","value":"true"}]}]}}}}' | Deployment updated with certificate verification enforcement |
| 8 | Verify complete security behavior validation | ACM Console → Infrastructure → Clusters → Observability → Health Check | oc get pods -n ocm -o wide && oc exec -n ocm deployment/multicluster-observability-operator -- ps aux \| grep -E "(CreateFromClient\|CreateToClient)" | All components running with proper security configuration, CreateFromClient and CreateToClient methods operating with validated TLS behavior |