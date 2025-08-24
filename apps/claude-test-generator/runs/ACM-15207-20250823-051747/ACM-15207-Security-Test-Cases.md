# ACM-15207 Security Test Cases

## Test Case 1: Validate TLS Certificate Configuration and InsecureSkipVerify Behavior

**Description**: Verify that the multicluster-observability-operator properly handles TLS certificate validation and demonstrates the InsecureSkipVerify security vulnerability behavior in both CreateFromClient and CreateToClient methods.

**Setup**: 
- ACM 2.14+ environment with multicluster-observability-operator deployed
- Administrative access to OpenShift cluster
- Access to ACM Console and OpenShift CLI

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|---------|-----------|------------|------------------|
| 1 | Log into ACM Console - Access ACM Console for security vulnerability testing | Navigate to https://console-openshift-console.apps.<cluster-host> | oc login https://api.<cluster-host>:6443 -u kubeadmin -p <password> --insecure-skip-tls-verify=true | Successfully authenticated with admin privileges |
| 2 | Verify multicluster-observability-operator deployment status | ACM Console → Administration → Workloads → Deployments → Search "observability" | oc get deployment multicluster-observability-operator -n ocm -o wide | Deployment shows Running status with 1/1 replicas available |
| 3 | Examine current TLS configuration in operator pod | ACM Console → Administration → Workloads → Pods → Select operator pod → Environment tab | oc get pod -l app=multicluster-observability-operator -n ocm -o yaml \| grep -A 5 -B 5 TLS | Pod environment shows TLS-related configuration variables |
| 4 | Check for existing certificate secrets in namespace | ACM Console → Administration → Workloads → Secrets → Filter by Type "TLS" | oc get secrets -n ocm --field-selector type=kubernetes.io/tls | List displays available TLS certificate secrets |
| 5 | Create test configuration without TLS certificates | ACM Console → Administration → Workloads → ConfigMaps → Create | oc create configmap observability-test-config -n ocm --from-literal=enable_tls=false | ConfigMap created successfully triggering InsecureSkipVerify fallback |
| 6 | Monitor operator logs for InsecureSkipVerify activation | ACM Console → Administration → Workloads → Pods → Select operator pod → Logs tab | oc logs deployment/multicluster-observability-operator -n ocm --tail=50 \| grep -E "InsecureSkipVerify\|nosec G402" | Logs show InsecureSkipVerify: true activation with security exemption comments |
| 7 | Verify security vulnerability behavior in CreateFromClient method | ACM Console → Observe → Metrics → Query prometheus metrics | oc exec -n ocm deployment/multicluster-observability-operator -- curl -k https://prometheus-route-url/federate | Prometheus federation request succeeds without certificate validation |
| 8 | Test CreateToClient method security behavior | ACM Console → Administration → Workloads → Pods → Check Thanos components | oc logs -n ocm -l app.kubernetes.io/name=thanos-receive --tail=20 \| grep -E "tls\|certificate\|insecure" | Thanos Receive logs show insecure communication patterns |

## Test Case 2: Verify Security Impact of TLS Certificate Validation Bypass

**Description**: Validate the security implications of the InsecureSkipVerify vulnerability by testing metrics pipeline communication security and demonstrating potential attack vectors.

**Setup**:
- ACM 2.14+ environment with observability components deployed
- MultiClusterObservability CR configured for testing
- Network access to metrics endpoints

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|---------|-----------|------------|------------------|
| 1 | Log into ACM Console - Access ACM Console for metrics security testing | Navigate to https://console-openshift-console.apps.<cluster-host> | oc login https://api.<cluster-host>:6443 -u kubeadmin -p <password> --insecure-skip-tls-verify=true | Successfully authenticated for security impact testing |
| 2 | Create MultiClusterObservability with minimal TLS configuration | ACM Console → Infrastructure → Clusters → Observability → Create | oc apply -f - <<EOF<br>apiVersion: observability.open-cluster-management.io/v1beta2<br>kind: MultiClusterObservability<br>metadata:<br>  name: security-test<br>  namespace: ocm<br>spec:<br>  enableMetrics: true<br>  observabilityAddonSpec:<br>    enableMetrics: true<br>  storageConfig:<br>    metricObjectStorage:<br>      name: thanos-object-storage<br>      key: thanos.yaml<br>EOF | MultiClusterObservability created with basic configuration |
| 3 | Verify Prometheus federation vulnerability exposure | ACM Console → Observe → Metrics → Prometheus UI | oc get route -n openshift-monitoring prometheus-k8s -o jsonpath='{.spec.host}' && curl -k https://$(oc get route -n openshift-monitoring prometheus-k8s -o jsonpath='{.spec.host}')/federate | Prometheus federation endpoint accessible without proper certificate validation |
| 4 | Test Thanos Receive remote write security behavior | ACM Console → Infrastructure → Clusters → Observability → Metrics | oc get pods -n ocm -l app.kubernetes.io/name=thanos-receive -o wide | Thanos Receive pods running and accepting remote write connections |
| 5 | Demonstrate man-in-the-middle attack potential | ACM Console → Administration → Events → Filter security events | oc exec -n ocm deployment/multicluster-observability-operator -- netstat -tlnp \| grep :9090 | Network connections show open ports vulnerable to interception |
| 6 | Verify metrics data transmission without encryption | ACM Console → Observe → Dashboards → ACM Overview | oc exec -n ocm deployment/observability-thanos-query -- curl -s "http://localhost:9090/api/v1/query?query=up" | Metrics data returned confirming unencrypted communication |
| 7 | Check certificate validation bypass in forwarder | ACM Console → Administration → Workloads → Jobs → Check metrics collection | oc logs -n openshift-addon-observability -l component=metrics-collector --tail=30 \| grep -E "certificate\|validation\|skip" | Logs confirm certificate validation bypassed in forwarder operations |
| 8 | Document security event logging for audit compliance | ACM Console → Administration → Events → Export events | oc get events -n ocm --sort-by='.lastTimestamp' -o yaml > security-events.yaml && grep -E "Warning\|security\|tls" security-events.yaml | Security events documented showing insecure configuration warnings |

## Test Case 3: Test Certificate Lifecycle and Security Monitoring

**Description**: Comprehensive testing of certificate management, security event logging, and operational security scenarios related to the InsecureSkipVerify vulnerability.

**Setup**:
- ACM 2.14+ environment with full observability stack
- Certificate management capabilities enabled
- Security monitoring and audit logging configured

**Test Table**:

| Step | Action | UI Method | CLI Method | Expected Results |
|------|---------|-----------|------------|------------------|
| 1 | Log into ACM Console - Access ACM Console for certificate lifecycle security testing | Navigate to https://console-openshift-console.apps.<cluster-host> | oc login https://api.<cluster-host>:6443 -u kubeadmin -p <password> --insecure-skip-tls-verify=true | Successfully authenticated for comprehensive security testing |
| 2 | Create expired certificate for vulnerability testing | ACM Console → Administration → Workloads → Secrets → Create TLS Secret | oc create secret tls expired-observability-cert -n ocm --cert=<(openssl req -x509 -newkey rsa:2048 -keyout /dev/stdout -out /dev/stdout -days -1 -nodes -subj "/CN=expired-test") --key=<(openssl req -x509 -newkey rsa:2048 -keyout /dev/stdout -out /dev/stdout -days -1 -nodes -subj "/CN=expired-test" 2>/dev/null) | Expired certificate secret created for security testing |
| 3 | Configure operator to use expired certificate | ACM Console → Administration → Workloads → Deployments → Edit environment | oc patch deployment multicluster-observability-operator -n ocm --type='merge' -p='{"spec":{"template":{"spec":{"containers":[{"name":"multicluster-observability-operator","env":[{"name":"TLS_CERT_FILE","value":"/etc/certs/tls.crt"},{"name":"TLS_KEY_FILE","value":"/etc/certs/tls.key"}]}]}}}}' | Deployment updated with expired certificate configuration |
| 4 | Monitor security warnings and certificate validation failures | ACM Console → Administration → Events → Filter by Warning type | oc get events -n ocm --field-selector type=Warning --sort-by='.lastTimestamp' \| grep -E "certificate\|tls\|expired" | Warning events show certificate validation failures |
| 5 | Verify InsecureSkipVerify fallback activation | ACM Console → Administration → Workloads → Pods → View operator logs | oc logs deployment/multicluster-observability-operator -n ocm --since=5m \| grep -A 3 -B 3 "InsecureSkipVerify\|fallback\|G402" | Logs confirm fallback to InsecureSkipVerify due to certificate issues |
| 6 | Test certificate rotation with security monitoring | ACM Console → Administration → Workloads → Secrets → Update TLS secret | oc delete secret expired-observability-cert -n ocm && oc create secret tls valid-observability-cert -n ocm --cert=<(openssl req -x509 -newkey rsa:2048 -keyout /dev/stdout -out /dev/stdout -days 365 -nodes -subj "/CN=valid-test") --key=<(openssl req -x509 -newkey rsa:2048 -keyout /dev/stdout -out /dev/stdout -days 365 -nodes -subj "/CN=valid-test" 2>/dev/null) | Certificate rotated from expired to valid certificate |
| 7 | Validate security audit trail compliance | ACM Console → Administration → Cluster Settings → Global Configuration → Audit | oc logs -n openshift-kube-apiserver-operator deployment/kube-apiserver-operator --since=10m \| grep -E "observability\|tls\|certificate\|insecure" | Audit logs record all certificate and security configuration changes |
| 8 | Verify complete security behavior validation | ACM Console → Infrastructure → Clusters → Observability → Health Status | oc get pods -n ocm -o wide && oc exec -n ocm deployment/multicluster-observability-operator -- ps aux \| grep observability | All components running with documented security configuration behavior |