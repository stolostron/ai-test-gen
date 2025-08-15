# AI Real Data Collector Service

## 🚀 Live ACM Ecosystem Data Collection and Knowledge Base Population

**Purpose**: Collects real, live data from ACM environments, JIRA, GitHub, and Jenkins to populate the knowledge base with actual intelligence instead of sample data.

**Service Status**: V1.0 - Production Ready for Real Data Collection
**Integration Level**: Core Data Collection Engine - MANDATORY for knowledge base population

## 🎯 Real Data Collection Capabilities

### 🌐 Live ACM Cluster Data Collection
Real-time collection of actual ACM cluster data and resources:

- **Hub Cluster Discovery**: Connects to actual ACM hub cluster and discovers all managed clusters
- **Complete Resource Enumeration**: Collects all ACM resources (ManagedClusters, Policies, Applications, etc.)
- **Multi-Cluster Resource Scanning**: Gathers resources from all accessible managed clusters
- **Live Status Collection**: Captures real resource states, conditions, and health status
- **Relationship Discovery**: Maps actual ownership and targeting relationships from live data

### 📋 JIRA Intelligence Data Collection
Live JIRA data collection for comprehensive ticket intelligence:

- **Active Ticket Discovery**: Collects all active ACM-related JIRA tickets
- **Hierarchy Analysis**: Maps real parent-child and linked ticket relationships
- **Historical Pattern Learning**: Analyzes ticket patterns and quality correlations
- **Component Mapping**: Links tickets to actual ACM components and repositories
- **Status and Priority Intelligence**: Tracks real ticket progression and business impact

### 🔗 GitHub Repository Intelligence Collection
Comprehensive GitHub data collection for deployment evidence and code intelligence:

- **Repository Discovery**: Scans all stolostron GitHub repositories for complete coverage
- **PR and Commit Analysis**: Analyzes actual PRs, merges, and code changes
- **Deployment Evidence Collection**: Validates real deployment status and evidence
- **Branch and Release Tracking**: Monitors actual branch patterns and release cycles
- **Code Pattern Analysis**: Extracts real coding patterns and architectural insights

### 🔧 Jenkins Pipeline Intelligence Collection
Live Jenkins data collection for failure pattern analysis:

- **Pipeline Discovery**: Identifies all ACM-related Jenkins pipelines and builds
- **Failure Pattern Analysis**: Analyzes real pipeline failures and classifications
- **Build History Intelligence**: Processes historical build data for pattern recognition
- **Environment Correlation**: Links pipeline data with actual test environments
- **Fix Template Generation**: Creates fix templates from successful remediations

## Real Data Collection Architecture

### Live Data Collection Framework
```yaml
Real_Data_Sources:
  acm_hub_cluster:
    connection: "Direct kubectl/oc access to ACM hub cluster"
    scope: "All ACM control plane resources and managed cluster registry"
    authentication: "Service account or kubeconfig"
    
  managed_clusters:
    connection: "Cluster proxy through hub or direct access"
    scope: "All accessible managed clusters and their resources"
    authentication: "Hub proxy or individual cluster credentials"
    
  jira_api:
    connection: "JIRA REST API with authentication"
    scope: "All ACM project tickets and related issues"
    authentication: "API token or OAuth"
    
  github_api:
    connection: "GitHub REST API and Git CLI"
    scope: "All stolostron organization repositories"
    authentication: "GitHub token or SSH keys"
    
  jenkins_api:
    connection: "Jenkins REST API with authentication"
    scope: "All ACM-related pipelines and builds"
    authentication: "Jenkins API token"
```

### Real-Time Data Collection Pipeline
```yaml
Collection_Pipeline:
  discovery_phase:
    - "Connect to all data sources and validate access"
    - "Discover all available clusters, repositories, and pipelines"
    - "Enumerate all resource types and API endpoints"
    
  collection_phase:
    - "Parallel data collection from all sources"
    - "Resource instance enumeration and status collection"
    - "Relationship mapping and dependency analysis"
    
  processing_phase:
    - "AI analysis and intelligence generation"
    - "Pattern recognition and correlation analysis"
    - "Quality assessment and confidence scoring"
    
  storage_phase:
    - "Structure and organize collected intelligence"
    - "Update knowledge base with fresh data"
    - "Generate indexes and relationship graphs"
```

## Knowledge Base Population Implementation

### Step 1: ACM Cluster Data Collection
```bash
# Trigger real ACM data collection
"Collect real ACM cluster data from environment"

# This executes:
# 1. Connect to ACM hub cluster
oc login <hub-cluster-url>
oc get managedclusters -o json > raw-data/managed-clusters.json

# 2. Collect all ACM resources
oc get policies.policy.open-cluster-management.io -A -o json > raw-data/policies.json
oc get applications.apps.open-cluster-management.io -A -o json > raw-data/applications.json
oc get placementrules.apps.open-cluster-management.io -A -o json > raw-data/placementrules.json

# 3. Process each managed cluster
for cluster in $(oc get managedclusters -o name); do
    cluster_name=$(echo $cluster | cut -d'/' -f2)
    oc --context=$cluster_name get pods -A -o json > raw-data/pods-$cluster_name.json
    oc --context=$cluster_name get deployments -A -o json > raw-data/deployments-$cluster_name.json
done

# 4. AI processes raw data into intelligence
# Raw JSON → AI Analysis → Structured Intelligence → Knowledge Base
```

### Step 2: JIRA Intelligence Collection
```bash
# Trigger real JIRA data collection
"Collect JIRA intelligence for ACM tickets"

# This executes:
# 1. Connect to JIRA and search for ACM tickets
curl -u $JIRA_USER:$JIRA_TOKEN \
  "https://issues.redhat.com/rest/api/2/search?jql=project=ACM AND status!=Closed" \
  > raw-data/active-acm-tickets.json

# 2. For each ticket, get full details and relationships
for ticket_id in $(jq -r '.issues[].key' raw-data/active-acm-tickets.json); do
    curl -u $JIRA_USER:$JIRA_TOKEN \
      "https://issues.redhat.com/rest/api/2/issue/$ticket_id?expand=changelog,links" \
      > raw-data/jira-$ticket_id.json
done

# 3. AI processes JIRA data
# Raw JIRA JSON → AI Analysis → Ticket Intelligence → Knowledge Base
```

### Step 3: GitHub Repository Intelligence Collection
```bash
# Trigger real GitHub data collection
"Collect GitHub repository intelligence for stolostron"

# This executes:
# 1. Discover all stolostron repositories
gh repo list stolostron --json name,url,defaultBranch --limit 1000 > raw-data/stolostron-repos.json

# 2. For each repository, collect detailed information
for repo in $(jq -r '.[].name' raw-data/stolostron-repos.json); do
    # Clone and analyze repository
    git clone https://github.com/stolostron/$repo temp-repos/$repo
    
    # Get repository metadata
    gh repo view stolostron/$repo --json description,topics,languages,releases \
      > raw-data/repo-$repo-metadata.json
    
    # Get recent PRs and issues
    gh pr list -R stolostron/$repo --state all --limit 100 --json number,title,state,createdAt \
      > raw-data/repo-$repo-prs.json
done

# 3. AI processes GitHub data
# Raw Git/GitHub data → AI Analysis → Repository Intelligence → Knowledge Base
```

### Step 4: Jenkins Pipeline Intelligence Collection
```bash
# Trigger real Jenkins data collection
"Collect Jenkins pipeline intelligence for ACM pipelines"

# This executes:
# 1. Discover ACM-related Jenkins jobs
curl -u $JENKINS_USER:$JENKINS_TOKEN \
  "$JENKINS_URL/api/json?tree=jobs[name,url]" | \
  jq '.jobs[] | select(.name | contains("acm") or contains("clc"))' \
  > raw-data/jenkins-acm-jobs.json

# 2. For each job, collect build history
for job_name in $(jq -r '.name' raw-data/jenkins-acm-jobs.json); do
    curl -u $JENKINS_USER:$JENKINS_TOKEN \
      "$JENKINS_URL/job/$job_name/api/json?tree=builds[number,result,timestamp,duration]" \
      > raw-data/jenkins-$job_name-builds.json
    
    # Get recent build console logs for failure analysis
    for build_number in $(jq -r '.builds[0:10][].number' raw-data/jenkins-$job_name-builds.json); do
        curl -u $JENKINS_USER:$JENKINS_TOKEN \
          "$JENKINS_URL/job/$job_name/$build_number/consoleText" \
          > raw-data/jenkins-$job_name-$build_number-console.log
    done
done

# 3. AI processes Jenkins data
# Raw Jenkins data → AI Analysis → Pipeline Intelligence → Knowledge Base
```

## AI Data Processing and Intelligence Generation

### Real Data Processing Flow
```yaml
AI_Processing_Pipeline:
  raw_data_ingestion:
    input: "JSON files from APIs, logs from Jenkins, git repositories"
    processing: "Parse, validate, and structure raw data"
    output: "Normalized data structures"
    
  intelligence_generation:
    input: "Normalized data structures"
    processing: "AI analysis, pattern recognition, relationship mapping"
    output: "Comprehensive intelligence profiles"
    
  knowledge_base_population:
    input: "Intelligence profiles"
    processing: "Structure for fast access, generate indexes"
    output: "Populated knowledge base with real data"
```

### Example: Real ManagedCluster Intelligence Generation
```bash
# Input: Raw oc get managedclusters -o json
# Processing: AI analyzes actual cluster data
# Output: Real intelligence profile

{
  "resource_type": "ManagedCluster",
  "real_data_intelligence": {
    "live_clusters": [
      {
        "name": "prod-east-1",
        "status": "Available",
        "last_heartbeat": "2025-08-15T16:45:00Z",
        "version": "4.14.8",
        "nodes": 12,
        "conditions": [
          {
            "type": "ManagedClusterConditionAvailable",
            "status": "True",
            "lastTransitionTime": "2025-08-15T14:20:00Z"
          }
        ]
      }
    ],
    "real_patterns": {
      "import_success_rate": 0.94,
      "common_issues": ["Network timeouts in 6% of imports"],
      "average_import_time": "4.2 minutes"
    }
  }
}
```

## Automated Population Workflow

### Complete Knowledge Base Population Command
```bash
# Single command to populate entire knowledge base with real data
"Populate knowledge base with live ACM ecosystem data"

# This triggers complete collection workflow:
# 1. Discover and collect from all ACM clusters
# 2. Gather all JIRA ticket intelligence  
# 3. Analyze all stolostron repositories
# 4. Process all Jenkins pipeline data
# 5. Generate comprehensive intelligence
# 6. Populate knowledge base with real data
# 7. Generate indexes and relationship graphs
```

### Incremental Population Commands
```bash
# Targeted population for specific data sources
"Refresh ACM cluster data"
"Update JIRA intelligence"  
"Refresh GitHub repository analysis"
"Update Jenkins pipeline patterns"
"Discover new resources in production clusters"
```

## Real Data Validation and Quality Assurance

### Data Quality Metrics
```yaml
Quality_Assurance:
  data_completeness:
    acm_clusters: "All accessible clusters discovered and analyzed"
    jira_tickets: "All active ACM tickets with full hierarchy"
    github_repos: "All stolostron repositories analyzed"
    jenkins_pipelines: "All ACM pipelines with recent build history"
    
  data_freshness:
    cluster_data: "Real-time cluster status and resource states"
    jira_data: "Current ticket status and recent updates"
    github_data: "Latest commits, PRs, and releases"
    jenkins_data: "Recent build results and failure patterns"
    
  intelligence_accuracy:
    relationship_mapping: "Verified against live resource relationships"
    pattern_recognition: "Validated against actual operational patterns"
    confidence_scoring: "Based on real data volume and consistency"
```

This AI Real Data Collector Service provides the complete implementation for populating the knowledge base with actual, live ACM ecosystem data instead of sample data, ensuring that all intelligence APIs have access to real, current, and comprehensive information.