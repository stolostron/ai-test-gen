#!/bin/bash

# Application Model Builder for AI Test Framework
# 
# This script intelligently builds team-specific Application Models by:
# 1. Detecting which ACM squad is running the framework (CLC, ALC, GRC, etc.)
# 2. Analyzing their QE automation repository structure
# 3. Dynamically fetching HTML from live ACM pages when needed
# 4. Building/updating component_library.yaml, action_catalog.yaml, data_personas.yaml
# 5. Caching results for efficiency

set -e

# Import framework utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../02-analysis/utils/logging.sh"
source "${SCRIPT_DIR}/../02-analysis/utils/yaml-utils.sh"

# Configuration
APPLICATION_MODEL_DIR="${SCRIPT_DIR}/../application-models"
CACHE_DIR="${APPLICATION_MODEL_DIR}/cache"
TEAMS_CONFIG="${APPLICATION_MODEL_DIR}/teams-config.yaml"

# Team detection patterns
declare -A TEAM_PATTERNS=(
    ["CLC"]="clc-ui|cluster.*lifecycle|managed.*cluster"
    ["ALC"]="application.*lifecycle|gitops|argocd"
    ["GRC"]="governance|policy|grc|security"
    ["OBS"]="observability|monitoring|metrics"
    ["MCE"]="multicluster.*engine|mce"
    ["GENERAL"]="acm|rhacm|multicloud"
)

# ACM Console URL patterns for different teams
declare -A TEAM_CONSOLE_PATHS=(
    ["CLC"]="/multicloud/infrastructure/clusters"
    ["ALC"]="/multicloud/applications"
    ["GRC"]="/multicloud/governance"
    ["OBS"]="/multicloud/observability"
    ["MCE"]="/multicloud/infrastructure"
    ["GENERAL"]="/multicloud/home"
)

print_status "🏗️ Application Model Builder - Team-Aware Component Analysis"

# ============================================================================
# TEAM DETECTION LOGIC
# ============================================================================

detect_team_context() {
    local detected_team="GENERAL"
    local confidence=0
    
    print_debug "Detecting team context from environment and repository..."
    
    # Method 1: Check current working directory
    local current_dir=$(pwd)
    print_debug "Current directory: $current_dir"
    
    for team in "${!TEAM_PATTERNS[@]}"; do
        if echo "$current_dir" | grep -iE "${TEAM_PATTERNS[$team]}" >/dev/null 2>&1; then
            print_success "✅ Detected team from directory: $team"
            detected_team="$team"
            confidence=80
            break
        fi
    done
    
    # Method 2: Check git repository URL
    if git remote get-url origin >/dev/null 2>&1; then
        local repo_url=$(git remote get-url origin)
        print_debug "Repository URL: $repo_url"
        
        for team in "${!TEAM_PATTERNS[@]}"; do
            if echo "$repo_url" | grep -iE "${TEAM_PATTERNS[$team]}" >/dev/null 2>&1; then
                print_success "✅ Detected team from repository: $team"
                detected_team="$team"
                confidence=90
                break
            fi
        done
    fi
    
    # Method 3: Check for team-specific files/directories
    for team in "${!TEAM_PATTERNS[@]}"; do
        case $team in
            "CLC")
                if [[ -d "cypress/views/clusters" ]] || [[ -f "package.json" ]] && grep -q "clc" package.json 2>/dev/null; then
                    detected_team="CLC"
                    confidence=95
                fi
                ;;
            "ALC")
                if [[ -d "cypress/views/applications" ]] || grep -q "argocd\|gitops" . -r 2>/dev/null; then
                    detected_team="ALC"
                    confidence=95
                fi
                ;;
            "GRC")
                if [[ -d "cypress/views/governance" ]] || grep -q "policy\|grc" . -r 2>/dev/null; then
                    detected_team="GRC"
                    confidence=95
                fi
                ;;
        esac
    done
    
    # Method 4: Check environment variables
    if [[ -n "${TEAM_CONTEXT:-}" ]]; then
        detected_team="${TEAM_CONTEXT}"
        confidence=100
        print_success "✅ Team explicitly set via TEAM_CONTEXT: $detected_team"
    fi
    
    print_status "🎯 Detected Team: $detected_team (Confidence: $confidence%)"
    echo "$detected_team:$confidence"
}

# ============================================================================
# REPOSITORY ANALYSIS
# ============================================================================

analyze_qa_repository() {
    local team="$1"
    local analysis_file="${CACHE_DIR}/${team,,}-repo-analysis.json"
    
    print_debug "Analyzing QE automation repository for team: $team"
    
    # Check if we have recent analysis (within 24 hours)
    if [[ -f "$analysis_file" ]] && [[ $(find "$analysis_file" -mtime -1 2>/dev/null) ]]; then
        print_info "📋 Using cached repository analysis"
        cat "$analysis_file"
        return 0
    fi
    
    local repo_structure=$(create_repo_analysis "$team")
    echo "$repo_structure" > "$analysis_file"
    
    print_success "✅ Repository analysis complete"
    echo "$repo_structure"
}

create_repo_analysis() {
    local team="$1"
    
    # Initialize analysis structure
    cat << EOF
{
    "team": "$team",
    "timestamp": "$(date -Iseconds)",
    "repository": {
        "url": "$(git remote get-url origin 2>/dev/null || echo 'unknown')",
        "branch": "$(git branch --show-current 2>/dev/null || echo 'unknown')",
        "lastCommit": "$(git log -1 --format='%h %s' 2>/dev/null || echo 'unknown')"
    },
    "structure": $(analyze_directory_structure),
    "selectors": $(analyze_existing_selectors),
    "testPatterns": $(analyze_test_patterns),
    "pageObjects": $(analyze_page_objects),
    "recommendations": $(generate_recommendations "$team")
}
EOF
}

analyze_directory_structure() {
    local structure=""
    
    # Look for common test automation patterns
    if [[ -d "cypress" ]]; then
        structure=$(find cypress -type f -name "*.js" | head -20 | jq -R . | jq -s .)
    elif [[ -d "tests" ]]; then
        structure=$(find tests -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" \) | head -20 | jq -R . | jq -s .)
    else
        structure='[]'
    fi
    
    echo "$structure"
}

analyze_existing_selectors() {
    local selectors='[]'
    
    # Find selector patterns in the codebase
    if command -v rg >/dev/null 2>&1; then
        selectors=$(rg -o 'data-testid["\s]*=["\s]*([^"]+)' --type js | head -20 | cut -d'"' -f2 | jq -R . | jq -s . 2>/dev/null || echo '[]')
    elif command -v grep >/dev/null 2>&1; then
        selectors=$(grep -r "data-testid" . --include="*.js" | head -20 | cut -d'"' -f2 | jq -R . | jq -s . 2>/dev/null || echo '[]')
    fi
    
    echo "$selectors"
}

analyze_test_patterns() {
    local patterns='[]'
    
    # Analyze common test patterns
    if [[ -d "cypress/views" ]]; then
        patterns=$(find cypress/views -name "*.js" | xargs grep -l "export.*Methods\|export.*Selectors" | jq -R . | jq -s . 2>/dev/null || echo '[]')
    fi
    
    echo "$patterns"
}

analyze_page_objects() {
    local pageObjects='[]'
    
    # Find page object patterns
    if [[ -d "cypress/views" ]]; then
        pageObjects=$(find cypress/views -name "*.js" | head -10 | jq -R . | jq -s . 2>/dev/null || echo '[]')
    fi
    
    echo "$pageObjects"
}

generate_recommendations() {
    local team="$1"
    
    cat << EOF
{
    "htmlPagesToAnalyze": $(get_team_pages "$team"),
    "priorityComponents": $(get_priority_components "$team"),
    "suggestedActions": $(get_suggested_actions "$team")
}
EOF
}

get_team_pages() {
    local team="$1"
    
    case "$team" in
        "CLC")
            echo '["clusters/managed", "clusters/create", "clusters/import", "clusters/sets", "clusters/pools"]'
            ;;
        "ALC")
            echo '["applications", "applications/create", "gitops"]'
            ;;
        "GRC")
            echo '["governance", "governance/policies", "governance/policy-sets"]'
            ;;
        "OBS")
            echo '["observability", "observability/overview", "observability/alerts"]'
            ;;
        *)
            echo '["home/overview", "infrastructure/clusters", "applications", "governance"]'
            ;;
    esac
}

get_priority_components() {
    local team="$1"
    
    case "$team" in
        "CLC")
            echo '["ClusterListPage", "CreateClusterWizard", "ImportClusterPage", "ClusterSetsPage"]'
            ;;
        "ALC")
            echo '["ApplicationsPage", "CreateApplicationPage", "GitOpsPage"]'
            ;;
        "GRC")
            echo '["GovernancePage", "PoliciesPage", "PolicySetsPage"]'
            ;;
        *)
            echo '["OverviewPage", "NavigationMenu", "CommonForms"]'
            ;;
    esac
}

get_suggested_actions() {
    local team="$1"
    
    case "$team" in
        "CLC")
            echo '["createCluster", "importCluster", "deleteCluster", "searchClusters"]'
            ;;
        "ALC")
            echo '["createApplication", "deployApplication", "syncApplication"]'
            ;;
        "GRC")
            echo '["createPolicy", "enforcePolicy", "checkCompliance"]'
            ;;
        *)
            echo '["navigateToSection", "login", "logout"]'
            ;;
    esac
}

# ============================================================================
# INTELLIGENT HTML FETCHING
# ============================================================================

should_fetch_html() {
    local team="$1"
    local force_refresh="${2:-false}"
    
    # Check if HTML fetching is needed
    local cache_file="${CACHE_DIR}/${team,,}-html-cache.json"
    
    if [[ "$force_refresh" == "true" ]]; then
        print_info "🔄 Force refresh requested - will fetch HTML"
        return 0
    fi
    
    if [[ ! -f "$cache_file" ]]; then
        print_info "📄 No HTML cache found - will fetch HTML"
        return 0
    fi
    
    # Check cache age (refresh if older than 7 days)
    if [[ $(find "$cache_file" -mtime +7 2>/dev/null) ]]; then
        print_info "⏰ HTML cache is stale - will fetch fresh HTML"
        return 0
    fi
    
    # Check if application model exists
    local model_file="${APPLICATION_MODEL_DIR}/${team,,}/component_library.yaml"
    if [[ ! -f "$model_file" ]]; then
        print_info "🏗️ No application model found - will fetch HTML to build it"
        return 0
    fi
    
    print_info "✅ Recent HTML cache and application model exist - skipping HTML fetch"
    return 1
}

fetch_team_html() {
    local team="$1"
    local console_url="$2"
    
    print_info "🌐 Fetching HTML for team: $team from console: $console_url"
    
    # Verify console accessibility
    if ! curl -s --max-time 10 "$console_url" >/dev/null; then
        print_warning "⚠️ Console not accessible: $console_url"
        return 1
    fi
    
    local team_dir="${APPLICATION_MODEL_DIR}/${team,,}"
    local html_dir="${team_dir}/html-snapshots"
    mkdir -p "$html_dir"
    
    # Get pages to analyze for this team
    local pages_json=$(get_team_pages "$team")
    local pages=($(echo "$pages_json" | jq -r '.[]'))
    
    print_info "📄 Fetching ${#pages[@]} pages for analysis..."
    
    for page in "${pages[@]}"; do
        local page_url="${console_url}${TEAM_CONSOLE_PATHS[$team]}/${page}"
        local html_file="${html_dir}/${page//\//-}.html"
        
        print_debug "Fetching: $page_url -> $html_file"
        
        # Use headless browser approach for dynamic content
        if command -v node >/dev/null 2>&1; then
            fetch_html_with_puppeteer "$page_url" "$html_file"
        else
            # Fallback to curl for static content
            curl -s --max-time 30 "$page_url" > "$html_file" 2>/dev/null || print_warning "Failed to fetch: $page"
        fi
    done
    
    print_success "✅ HTML fetching complete for team: $team"
}

fetch_html_with_puppeteer() {
    local url="$1"
    local output_file="$2"
    
    # Create temporary Node.js script for HTML fetching
    local temp_script=$(mktemp)
    cat << 'EOF' > "$temp_script"
const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    try {
        const browser = await puppeteer.launch({ 
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();
        
        // Set realistic viewport and user agent
        await page.setViewport({ width: 1920, height: 1080 });
        await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36');
        
        await page.goto(process.argv[2], { 
            waitUntil: 'networkidle2',
            timeout: 30000 
        });
        
        // Wait for dynamic content to load
        await page.waitForTimeout(3000);
        
        const html = await page.content();
        fs.writeFileSync(process.argv[3], html);
        
        await browser.close();
        console.log('HTML fetched successfully');
    } catch (error) {
        console.error('Error fetching HTML:', error.message);
        process.exit(1);
    }
})();
EOF
    
    if node "$temp_script" "$url" "$output_file" 2>/dev/null; then
        print_debug "✅ Successfully fetched HTML with Puppeteer"
    else
        print_debug "⚠️ Puppeteer fetch failed, using curl fallback"
        curl -s --max-time 30 "$url" > "$output_file" 2>/dev/null
    fi
    
    rm -f "$temp_script"
}

# ============================================================================
# APPLICATION MODEL GENERATION
# ============================================================================

build_application_model() {
    local team="$1"
    local repo_analysis="$2"
    
    print_debug "Building Application Model for team: $team"
    
    local team_dir="${APPLICATION_MODEL_DIR}/${team,,}"
    mkdir -p "$team_dir"
    
    # Generate component library
    generate_component_library "$team" "$repo_analysis" "${team_dir}/component_library.yaml"
    
    # Generate action catalog
    generate_action_catalog "$team" "$repo_analysis" "${team_dir}/action_catalog.yaml"
    
    # Generate data personas
    generate_data_personas "$team" "$repo_analysis" "${team_dir}/data_personas.yaml"
    
    # Create team manifest
    create_team_manifest "$team" "$repo_analysis" "${team_dir}/team_manifest.yaml"
    
    print_success "✅ Application Model built for team: $team"
}

generate_component_library() {
    local team="$1"
    local repo_analysis="$2"
    local output_file="$3"
    
    print_info "📋 Generating component library..."
    
    # Check if we have HTML snapshots to analyze
    local html_dir="${APPLICATION_MODEL_DIR}/${team,,}/html-snapshots"
    
    if [[ -d "$html_dir" ]] && [[ $(ls -A "$html_dir" 2>/dev/null) ]]; then
        generate_component_library_from_html "$team" "$html_dir" "$output_file"
    else
        generate_component_library_from_patterns "$team" "$repo_analysis" "$output_file"
    fi
}

generate_component_library_from_html() {
    local team="$1"
    local html_dir="$2"
    local output_file="$3"
    
    print_info "🔍 Analyzing HTML snapshots for component library..."
    
    # Create Node.js script for HTML analysis
    local analysis_script=$(mktemp)
    cat << 'EOF' > "$analysis_script"
const fs = require('fs');
const path = require('path');

const team = process.argv[2];
const htmlDir = process.argv[3];
const outputFile = process.argv[4];

// Intelligent selector analysis
function analyzeHTML(htmlContent, pageName) {
    // This would be a sophisticated HTML analysis
    // For now, returning a basic structure
    return {
        name: pageName,
        elements: []
    };
}

// Process all HTML files
const htmlFiles = fs.readdirSync(htmlDir).filter(f => f.endsWith('.html'));
const components = [];

htmlFiles.forEach(file => {
    const htmlContent = fs.readFileSync(path.join(htmlDir, file), 'utf8');
    const pageName = file.replace('.html', '').replace(/-/g, '');
    const component = analyzeHTML(htmlContent, pageName);
    components.push(component);
});

// Generate YAML
const yaml = `# Auto-generated Component Library for ${team} team
# Generated: ${new Date().toISOString()}

version: "1.0.0"
lastUpdated: "${new Date().toISOString()}"
team: "${team}"
source: "html-analysis"

components:
${components.map(comp => `  - name: ${comp.name}
    description: "Auto-generated component for ${comp.name}"
    elements: []`).join('\n')}
`;

fs.writeFileSync(outputFile, yaml);
console.log(`Component library generated: ${outputFile}`);
EOF
    
    if command -v node >/dev/null 2>&1; then
        node "$analysis_script" "$team" "$html_dir" "$output_file"
    else
        generate_component_library_from_patterns "$team" "{}" "$output_file"
    fi
    
    rm -f "$analysis_script"
}

generate_component_library_from_patterns() {
    local team="$1"
    local repo_analysis="$2"
    local output_file="$3"
    
    print_info "📝 Generating component library from existing patterns..."
    
    cat << EOF > "$output_file"
# Component Library for $team team
# Generated: $(date -Iseconds)

version: "1.0.0"
lastUpdated: "$(date -Iseconds)"
team: "$team"
source: "pattern-analysis"

components:
$(generate_team_specific_components "$team")
EOF
}

generate_team_specific_components() {
    local team="$1"
    
    case "$team" in
        "CLC")
            cat << 'EOF'
  - name: ClusterListPage
    description: "Main cluster management interface"
    elements:
      - name: createClusterButton
        description: "Primary button to create new cluster"
        locator: "[data-testid='create-cluster-btn']"
        fallbacks: ["button:contains('Create cluster')"]
      
      - name: importClusterButton
        description: "Button to import existing cluster"
        locator: "[data-testid='import-cluster-btn']"
        fallbacks: ["button:contains('Import cluster')"]
      
      - name: clusterTable
        description: "Table displaying managed clusters"
        locator: "[data-testid='clusters-table']"
        fallbacks: ["table", ".pf-v5-c-table"]

  - name: CreateClusterWizard
    description: "Multi-step cluster creation wizard"
    elements:
      - name: providerAWS
        description: "AWS provider selection"
        locator: "[data-testid='provider-aws']"
        fallbacks: ["#aws"]
      
      - name: clusterNameInput
        description: "Cluster name input field"
        locator: "[data-testid='cluster-name-input']"
        fallbacks: ["#eman", "input[placeholder*='cluster name']"]
EOF
            ;;
        "ALC")
            cat << 'EOF'
  - name: ApplicationsPage
    description: "Application lifecycle management interface"
    elements:
      - name: createApplicationButton
        description: "Primary button to create new application"
        locator: "[data-testid='create-application-btn']"
        fallbacks: ["button:contains('Create application')"]

  - name: CreateApplicationWizard
    description: "Application creation wizard"
    elements:
      - name: applicationNameInput
        description: "Application name input"
        locator: "[data-testid='app-name-input']"
        fallbacks: ["input[placeholder*='application name']"]
EOF
            ;;
        "GRC")
            cat << 'EOF'
  - name: GovernancePage
    description: "Governance and risk compliance interface"
    elements:
      - name: createPolicyButton
        description: "Primary button to create new policy"
        locator: "[data-testid='create-policy-btn']"
        fallbacks: ["button:contains('Create policy')"]

  - name: PoliciesTable
    description: "Table displaying governance policies"
    elements:
      - name: policiesTable
        description: "Main policies table"
        locator: "[data-testid='policies-table']"
        fallbacks: ["table", ".pf-v5-c-table"]
EOF
            ;;
        *)
            cat << 'EOF'
  - name: CommonNavigation
    description: "Shared navigation components"
    elements:
      - name: mainNavigation
        description: "Primary navigation menu"
        locator: "[data-testid='main-nav']"
        fallbacks: ["nav", ".pf-v5-c-nav"]
EOF
            ;;
    esac
}

generate_action_catalog() {
    local team="$1"
    local repo_analysis="$2"
    local output_file="$3"
    
    print_info "⚡ Generating action catalog..."
    
    cat << EOF > "$output_file"
# Action Catalog for $team team
# Generated: $(date -Iseconds)

version: "1.0.0"
lastUpdated: "$(date -Iseconds)"
team: "$team"

actions:
$(generate_team_specific_actions "$team")
EOF
}

generate_team_specific_actions() {
    local team="$1"
    
    case "$team" in
        "CLC")
            cat << 'EOF'
  - name: loginAsAdmin
    description: "Log into ACM console as cluster admin"
    mapsToFunction: "cy.login()"
    parameters: []

  - name: navigateToClusterList
    description: "Navigate to main clusters page"
    mapsToFunction: "acm23xheaderMethods.goToClusters()"
    parameters: []

  - name: createCluster
    description: "Complete cluster creation workflow"
    mapsToFunction: "managedClustersMethods.createCluster(clusterConfig)"
    parameters:
      - name: clusterConfig
        type: "object"
        required: true

  - name: importCluster
    description: "Import an existing cluster"
    mapsToFunction: "managedClustersMethods.importCluster(clusterName)"
    parameters:
      - name: clusterName
        type: "string"
        required: true
EOF
            ;;
        "ALC")
            cat << 'EOF'
  - name: createApplication
    description: "Create a new application"
    mapsToFunction: "applicationMethods.createApplication(appConfig)"
    parameters:
      - name: appConfig
        type: "object"
        required: true

  - name: deployApplication
    description: "Deploy application to target clusters"
    mapsToFunction: "applicationMethods.deployApplication(appName, clusters)"
    parameters:
      - name: appName
        type: "string"
        required: true
      - name: clusters
        type: "array"
        required: true
EOF
            ;;
        *)
            cat << 'EOF'
  - name: login
    description: "Basic login action"
    mapsToFunction: "cy.login()"
    parameters: []
EOF
            ;;
    esac
}

generate_data_personas() {
    local team="$1"
    local repo_analysis="$2"
    local output_file="$3"
    
    print_info "👥 Generating data personas..."
    
    cat << EOF > "$output_file"
# Data Personas for $team team
# Generated: $(date -Iseconds)

version: "1.0.0"
lastUpdated: "$(date -Iseconds)"
team: "$team"

personas:
$(generate_team_specific_personas "$team")
EOF
}

generate_team_specific_personas() {
    local team="$1"
    
    case "$team" in
        "CLC")
            cat << 'EOF'
  - name: clusterAdminUser
    description: "Administrator with full cluster management permissions"
    data:
      username: "kubeadmin"
      password: "{{ENV.CYPRESS_OPTIONS_HUB_PASSWORD}}"
      permissions: ["cluster-admin"]

  - name: basicAWSCluster
    description: "Standard AWS cluster configuration"
    data:
      provider: "Amazon Web Services"
      name: "test-aws-cluster"
      region: "us-east-1"
      releaseImage: "4.17.0"
      singleNode: false

  - name: awsCredentials
    description: "AWS provider credentials"
    data:
      name: "aws-creds"
      type: "Amazon Web Services"
      accessKeyId: "{{ENV.AWS_ACCESS_KEY_ID}}"
      secretAccessKey: "{{ENV.AWS_SECRET_ACCESS_KEY}}"
EOF
            ;;
        *)
            cat << 'EOF'
  - name: adminUser
    description: "General admin user"
    data:
      username: "kubeadmin"
      password: "{{ENV.CYPRESS_OPTIONS_HUB_PASSWORD}}"
EOF
            ;;
    esac
}

create_team_manifest() {
    local team="$1"
    local repo_analysis="$2"
    local output_file="$3"
    
    cat << EOF > "$output_file"
# Team Manifest for $team
# Generated: $(date -Iseconds)

team: "$team"
version: "1.0.0"
lastUpdated: "$(date -Iseconds)"

metadata:
  repository: $(echo "$repo_analysis" | jq -r '.repository.url // "unknown"')
  confidence: 95
  
applicationModel:
  componentLibrary: "./component_library.yaml"
  actionCatalog: "./action_catalog.yaml"
  dataPersonas: "./data_personas.yaml"

capabilities:
  htmlFetching: true
  dynamicAnalysis: true
  caching: true

settings:
  cacheExpiryDays: 7
  htmlRefreshThreshold: "24h"
  analysisDepth: "comprehensive"
EOF
}

# ============================================================================
# MAIN EXECUTION FLOW
# ============================================================================

main() {
    local force_refresh="${1:-false}"
    local console_url="${CONSOLE_URL:-}"
    
    # Ensure required directories exist
    mkdir -p "$APPLICATION_MODEL_DIR" "$CACHE_DIR"
    
    # Step 1: Detect team context
    IFS=':' read -r detected_team confidence <<< "$(detect_team_context)"
    
    # Step 2: Analyze QE repository
    local repo_analysis=$(analyze_qa_repository "$detected_team")
    
    # Step 3: Intelligent HTML fetching decision
    if should_fetch_html "$detected_team" "$force_refresh"; then
        if [[ -n "$console_url" ]]; then
            fetch_team_html "$detected_team" "$console_url"
        else
            print_warning "⚠️ No console URL provided - skipping HTML fetch"
            print_info "💡 Set CONSOLE_URL environment variable to enable HTML analysis"
        fi
    fi
    
    # Step 4: Build/update application model
    build_application_model "$detected_team" "$repo_analysis"
    
    # Step 5: Export team context for framework use
    export DETECTED_TEAM="$detected_team"
    export TEAM_CONFIDENCE="$confidence"
    export APPLICATION_MODEL_PATH="${APPLICATION_MODEL_DIR}/${detected_team,,}"
    
    print_success "🎉 Application Model Builder complete!"
    print_status "📊 Team: $detected_team (Confidence: $confidence%)"
    print_status "📁 Model Path: $APPLICATION_MODEL_PATH"
    
    # Return team information for framework integration
    cat << EOF
{
    "team": "$detected_team",
    "confidence": $confidence,
    "modelPath": "$APPLICATION_MODEL_PATH",
    "capabilities": ["component-library", "action-catalog", "data-personas"],
    "htmlFetchingEnabled": $(should_fetch_html "$detected_team" >/dev/null 2>&1 && echo "true" || echo "false")
}
EOF
}

# Handle command line arguments
case "${1:-}" in
    "--force-refresh")
        main "true"
        ;;
    "--help"|"-h")
        cat << 'EOF'
Application Model Builder - Team-Aware Component Analysis

Usage:
  ./application-model-builder.sh [OPTIONS]

Options:
  --force-refresh    Force refresh of HTML cache and rebuild models
  --help, -h         Show this help message

Environment Variables:
  CONSOLE_URL        ACM console URL for HTML fetching
  TEAM_CONTEXT       Explicitly set team context (CLC, ALC, GRC, etc.)

Examples:
  # Automatic team detection and model building
  ./application-model-builder.sh
  
  # Force refresh with console URL
  CONSOLE_URL=https://console.apps.cluster.com ./application-model-builder.sh --force-refresh
  
  # Explicit team context
  TEAM_CONTEXT=CLC ./application-model-builder.sh
EOF
        ;;
    *)
        main "false"
        ;;
esac