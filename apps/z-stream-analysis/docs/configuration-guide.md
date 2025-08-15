# Configuration Guide - Z-Stream Analysis Engine

> **Comprehensive configuration guide for Enterprise AI Services Integration**

## 🎯 Overview

The Z-Stream Analysis Engine V3.0 uses intelligent configuration discovery and AI services integration. This guide covers all configuration aspects from basic setup to advanced AI services orchestration.

## 🚀 Quick Configuration

### **Intelligent Jenkins Parameter Extraction (Primary)**

The framework automatically discovers configuration from Jenkins run parameters - **no manual setup required** for most use cases.

```bash
# Framework automatically extracts from Jenkins parameters endpoint:
# https://jenkins-server/job/pipeline/123/parameters/
# 
# Common extracted parameters:
# - CLUSTER_URL, OCP_CLUSTER, K8S_SERVER (target test cluster)
# - KUBECONFIG, CLUSTER_KUBECONFIG (authentication)
# - NAMESPACE, TARGET_NAMESPACE (test namespace)
# - ENVIRONMENT, TEST_ENV (environment context)
# - CREDENTIALS, AUTH_TOKEN (access credentials)
```

### **Real-World Examples**

**UI Test Pipeline Configuration Discovery:**
```bash
# Source: https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/CI-Jobs/job/e2e_ui_test_pipeline/520/parameters/
curl -k -s "https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/CI-Jobs/job/e2e_ui_test_pipeline/520/parameters/" | jq '.parameter[] | {name, value}'

# Typical extracted configuration:
{
  "CLUSTER_URL": "https://api.qe6-v1.lab.psi.redhat.com:6443",
  "NAMESPACE": "acm-test",
  "KUBECONFIG": "/tmp/kubeconfig-qe6",
  "ENVIRONMENT": "qe6"
}
```

**CLC E2E Pipeline Configuration Discovery:**
```bash
# Source: https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc/job/clc-e2e-pipeline/3223/parameters/
curl -k -s "https://jenkins-csb-rhacm-tests.dno.corp.redhat.com/job/qe-acm-automation-poc/job/clc-e2e-pipeline/3223/parameters/" | jq '.parameter[] | {name, value}'

# Typical extracted configuration:
{
  "CLUSTER_URL": "https://api.qe7-v2.lab.psi.redhat.com:6443",
  "NAMESPACE": "open-cluster-management",
  "ENVIRONMENT": "qe7",
  "CLUSTER_KUBECONFIG": "/tmp/kubeconfig-qe7-v2"
}
```

## 🔧 **Environment Configuration**

### **Prerequisites**
- **Claude Code CLI** configured and authenticated
- **Jenkins API Access** to target instances (optional - can analyze public URLs)  
- **Network Access** to Jenkins instances and artifact storage
- **Self-Contained Operation** - No external dependencies or script requirements

### **Intelligent Discovery Process**

The AI Environment Validation Service uses a 4-tier discovery approach:

```python
# 1. Primary: Jenkins parameter extraction
def extract_environment_from_jenkins_parameters(jenkins_url):
    parameters_endpoint = f"{jenkins_url}/parameters/"
    jenkins_parameters = fetch_jenkins_parameters(parameters_endpoint)
    
    return {
        "cluster_url": extract_from_build_params(jenkins_parameters, 
            "CLUSTER_URL", "OCP_CLUSTER", "K8S_SERVER", "CLUSTER_SERVER"),
        "namespace": extract_from_build_params(jenkins_parameters,
            "NAMESPACE", "TARGET_NAMESPACE", "TEST_NAMESPACE", "ACM_NAMESPACE"),
        "credentials": extract_jenkins_credentials(jenkins_parameters,
            "KUBECONFIG", "CLUSTER_KUBECONFIG", "OCP_TOKEN", "CLUSTER_TOKEN"),
        "environment": extract_from_build_params(jenkins_parameters,
            "ENVIRONMENT", "TEST_ENV", "CLUSTER_ENV")
    }

# 2. Secondary: Console log parsing
def extract_environment_from_console_logs(console_log):
    return {
        "oc_login_commands": parse_oc_login_commands(console_log),
        "cluster_context": parse_cluster_context_switches(console_log),
        "environment_setup": parse_environment_variable_exports(console_log)
    }

# 3. Tertiary: Jenkins artifacts analysis
def extract_environment_from_artifacts(jenkins_artifacts):
    return {
        "kubeconfig_files": find_kubeconfig_artifacts(jenkins_artifacts),
        "credential_files": find_credential_artifacts(jenkins_artifacts),
        "environment_configs": find_environment_config_artifacts(jenkins_artifacts)
    }

# 4. Fallback: Interactive discovery
def interactive_environment_discovery():
    return prompt_for_missing_environment_details()
```

### **Manual Configuration (Fallback Only)**

Only needed when intelligent discovery fails:

```bash
# Jenkins access (for private instances)
export JENKINS_USER="your-username"
export JENKINS_TOKEN="your-api-token"

# Analysis settings (optional)
export ANALYSIS_OUTPUT_DIR="./runs"
export ARCHIVE_RETENTION_DAYS="90"
export DEBUG_MODE="false"
```

## 🤖 **AI Services Configuration**

### **Service Orchestration Settings**

Configure AI services behavior in `.claude/ai-services/ai-services-integration.md`:

```yaml
AI_Services_Configuration:
  execution_strategy:
    parallel_services: ["environment_validation", "repository_analysis"]
    sequential_services: ["evidence_correlation", "fix_generation"]
    performance_targets:
      environment_validation: "< 60 seconds"
      repository_analysis: "< 120 seconds"
      fix_generation: "< 180 seconds"
      total_execution: "< 300 seconds"
  
  quality_thresholds:
    minimum_confidence: 85
    evidence_consistency: 90
    fix_accuracy: 95
    cross_service_correlation: 96
  
  error_recovery:
    graceful_degradation: true
    intelligent_fallback: true
    retry_logic: "exponential_backoff"
    max_retries: 3
```

### **Environment Validation Service Configuration**

Configure in `.claude/ai-services/environment-validation-service.md`:

```yaml
Environment_Validation_Service:
  authentication_methods:
    primary: "jenkins_kubeconfig"
    secondary: "jenkins_credentials"
    tertiary: "environment_detection"
    fallback: "manual_discovery"
  
  validation_scope:
    api_testing: true
    ui_functionality: true
    integration_workflows: true
    environment_health: true
  
  performance_settings:
    connection_timeout: 30
    validation_timeout: 60
    retry_attempts: 3
    parallel_validation: true
  
  cluster_discovery:
    parameter_patterns:
      - "CLUSTER_URL"
      - "OCP_CLUSTER" 
      - "K8S_SERVER"
      - "CLUSTER_SERVER"
    
    credential_patterns:
      - "KUBECONFIG"
      - "CLUSTER_KUBECONFIG"
      - "OCP_TOKEN"
      - "CLUSTER_TOKEN"
```

### **Repository Analysis Service Configuration**

Configure in `.claude/ai-services/automation-repository-analysis-service.md`:

```yaml
Repository_Analysis_Service:
  access_methods:
    primary: "public_clone"
    secondary: "jenkins_credentials"
    tertiary: "token_authentication"
    fallback: "readonly_analysis"
  
  analysis_scope:
    test_code_analysis: true
    pattern_detection: true
    dependency_analysis: true
    framework_assessment: true
  
  pattern_detection:
    flaky_test_patterns:
      - "hard_coded_sleeps"
      - "unstable_locators"
      - "test_data_conflicts"
      - "network_timeouts"
    
    automation_issues:
      - "timing_dependencies"
      - "element_locator_problems"
      - "api_endpoint_issues"
      - "test_data_problems"
  
  repository_discovery:
    parameter_patterns:
      - "GIT_URL"
      - "REPO_URL"
      - "SCM_URL"
      - "AUTOMATION_REPO"
    
    branch_patterns:
      - "GIT_BRANCH"
      - "BRANCH_NAME"
      - "SCM_BRANCH"
```

### **Fix Generation Service Configuration**

Configure in `.claude/ai-services/fix-generation-service.md`:

```yaml
Fix_Generation_Service:
  fix_strategies:
    ui_locator_issues:
      strategies: ["css_selector_upgrade", "data_testid_implementation", "xpath_optimization"]
      priority: "css_selector_upgrade"
      validation: "ui_interaction_test"
    
    timing_issues:
      strategies: ["explicit_wait_implementation", "fluent_wait_setup", "retry_mechanism"]
      priority: "explicit_wait_implementation"
      validation: "timing_stability_test"
    
    test_data_conflicts:
      strategies: ["unique_data_generation", "test_isolation", "cleanup_automation"]
      priority: "unique_data_generation"
      validation: "parallel_execution_test"
  
  pull_request_automation:
    enabled: true
    branch_naming: "fix/automation-issues-{build_id}"
    auto_merge: false
    review_assignment: true
    validation_tests: true
  
  quality_targets:
    fix_accuracy: 95
    merge_readiness: 90
    pr_creation_success: 98
    validation_completeness: 95
```

## 📊 **Advanced Configuration Options**

### **Performance Optimization**

```yaml
Performance_Configuration:
  resource_allocation:
    cpu_utilization: 0.8
    memory_utilization: 0.9
    network_bandwidth: 0.7
  
  execution_optimization:
    parallel_execution: true
    concurrent_services: 3
    batch_processing: true
    intelligent_caching: true
  
  timeout_settings:
    service_timeout: 180
    total_timeout: 300
    retry_timeout: 30
    connection_timeout: 10
```

### **Quality Assurance Settings**

```yaml
Quality_Assurance_Configuration:
  validation_thresholds:
    evidence_consistency: 90
    verdict_confidence: 85
    fix_accuracy: 95
    analysis_completeness: 90
  
  quality_metrics:
    cross_service_correlation: 96
    environment_validation_accuracy: 98
    repository_analysis_depth: 95
    fix_generation_viability: 90
  
  continuous_improvement:
    pattern_learning: true
    feedback_integration: true
    performance_monitoring: true
    adaptive_optimization: true
```

### **Error Handling Configuration**

```yaml
Error_Handling_Configuration:
  recovery_strategies:
    partial_service_failure:
      strategy: "graceful_degradation"
      actions: ["continue_with_available_services", "enhance_remaining_analysis"]
    
    authentication_failure:
      strategy: "multi_method_fallback"
      actions: ["try_alternative_credentials", "use_readonly_access"]
    
    network_connectivity:
      strategy: "intelligent_retry"
      actions: ["retry_with_backoff", "use_alternative_endpoints"]
    
    resource_exhaustion:
      strategy: "resource_optimization"
      actions: ["reduce_parallel_execution", "increase_timeouts"]
  
  monitoring:
    error_tracking: true
    performance_monitoring: true
    quality_assessment: true
    alert_thresholds:
      error_rate: 5
      performance_degradation: 20
      quality_score_drop: 10
```

## 🔍 **Debugging and Troubleshooting Configuration**

### **Debug Mode Settings**

```bash
# Enable comprehensive debugging
export DEBUG_MODE="true"
export VERBOSE_LOGGING="true"
export TRACE_AI_SERVICES="true"

# Debug specific services
export DEBUG_ENVIRONMENT_VALIDATION="true"
export DEBUG_REPOSITORY_ANALYSIS="true"
export DEBUG_FIX_GENERATION="true"
export DEBUG_SERVICE_INTEGRATION="true"
```

### **Logging Configuration**

```yaml
Logging_Configuration:
  log_levels:
    ai_services: "INFO"
    environment_validation: "INFO"
    repository_analysis: "INFO"
    fix_generation: "INFO"
    service_integration: "DEBUG"
  
  log_destinations:
    console: true
    file: "./logs/zstream-analysis.log"
    structured: true
    rotation: "daily"
  
  monitoring:
    performance_metrics: true
    error_tracking: true
    quality_metrics: true
    service_health: true
```

### **Diagnostic Tools**

```bash
# Service health check
"Check AI services health and configuration"

# Performance monitoring
"Monitor AI services performance and resource usage"

# Quality assessment
"Validate analysis quality and confidence scores"

# Configuration validation
"Verify AI services configuration and settings"
```

## 🎯 **Environment-Specific Configuration**

### **Development Environment**

```yaml
Development_Configuration:
  ai_services:
    environment_validation:
      strict_validation: false
      mock_cluster_access: true
      fast_validation: true
    
    repository_analysis:
      local_repository: true
      skip_authentication: true
      enhanced_debugging: true
    
    fix_generation:
      dry_run_mode: true
      validation_only: true
      skip_pr_creation: true
```

### **Staging Environment**

```yaml
Staging_Configuration:
  ai_services:
    environment_validation:
      strict_validation: true
      real_cluster_access: true
      comprehensive_testing: true
    
    repository_analysis:
      full_repository_analysis: true
      pattern_detection: true
      quality_assessment: true
    
    fix_generation:
      generate_fixes: true
      create_draft_prs: true
      validation_required: true
```

### **Production Environment**

```yaml
Production_Configuration:
  ai_services:
    environment_validation:
      enterprise_validation: true
      security_compliance: true
      audit_logging: true
    
    repository_analysis:
      comprehensive_analysis: true
      security_scanning: true
      compliance_checking: true
    
    fix_generation:
      enterprise_fixes: true
      automated_pr_creation: true
      quality_enforcement: true
  
  security:
    credential_encryption: true
    secure_communication: true
    audit_trails: true
    compliance_reporting: true
```

## 📚 **Configuration Validation**

### **Automated Configuration Validation**

```bash
# Validate AI services configuration
"Validate AI services configuration and dependencies"

# Test environment connectivity
"Test environment connectivity and authentication"

# Verify repository access
"Verify repository access and permissions"

# Check fix generation capabilities
"Check fix generation capabilities and dependencies"
```

### **Configuration Health Monitoring**

```python
def validate_configuration_health():
    """Comprehensive configuration health monitoring"""
    
    health_checks = {
        "ai_services_config": validate_ai_services_configuration(),
        "environment_config": validate_environment_configuration(),
        "repository_config": validate_repository_configuration(),
        "integration_config": validate_integration_configuration()
    }
    
    overall_health = calculate_configuration_health_score(health_checks)
    
    if overall_health < 90:
        trigger_configuration_remediation()
    
    return {
        "health_score": overall_health,
        "configuration_status": health_checks,
        "recommendations": generate_configuration_improvements(health_checks)
    }
```

---

**🔧 Enterprise Configuration Framework:** The Z-Stream Analysis Engine provides comprehensive configuration management with intelligent discovery, AI services integration, and enterprise-grade quality assurance - ensuring optimal performance and reliability across all environments.**