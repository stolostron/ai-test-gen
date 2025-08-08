#!/bin/bash

# Stage 2.5: Context Augmentation with Application Model
# 
# This stage sits between Context Gathering and AI Analysis to inject
# structured component information from the Application Model into AI prompts.
# It creates the RELEVANT_COMPONENTS section that guides AI reasoning.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/utils/logging.sh"
source "${SCRIPT_DIR}/utils/yaml-utils.sh"

print_status "🔗 Stage 2.5: Context Augmentation with Application Model"

# ============================================================================
# CONFIGURATION
# ============================================================================

JIRA_TICKET="${1:-}"
JIRA_CONTENT_FILE="${2:-02-analysis/jira-details.md}"
APPLICATION_MODEL_PATH="${APPLICATION_MODEL_PATH:-}"
DETECTED_TEAM="${DETECTED_TEAM:-GENERAL}"

if [[ -z "$JIRA_TICKET" ]]; then
    print_error "JIRA ticket is required"
    exit 1
fi

if [[ ! -f "$JIRA_CONTENT_FILE" ]]; then
    print_error "JIRA content file not found: $JIRA_CONTENT_FILE"
    exit 1
fi

print_info "🎯 Augmenting context for team: $DETECTED_TEAM"
print_debug "Application Model Path: $APPLICATION_MODEL_PATH"

# ============================================================================
# KEYWORD EXTRACTION AND MATCHING
# ============================================================================

extract_keywords_from_jira() {
    local jira_file="$1"
    
    print_info "🔍 Extracting keywords from JIRA content..."
    
    # Extract meaningful keywords from JIRA content
    local keywords=$(cat "$jira_file" | \
        # Remove markdown formatting
        sed 's/[*_`#]//g' | \
        # Extract words (alphanumeric + hyphens)
        grep -oE '[a-zA-Z][a-zA-Z0-9-]{2,}' | \
        # Convert to lowercase
        tr '[:upper:]' '[:lower:]' | \
        # Remove common words
        grep -vE '^(the|and|for|are|but|not|you|all|can|had|her|was|one|our|out|day|get|has|him|his|how|man|new|now|old|see|two|way|who|boy|did|its|let|put|say|she|too|use)$' | \
        # Sort and count
        sort | uniq -c | sort -nr | \
        # Take top keywords
        head -20 | \
        # Extract just the words
        awk '{print $2}')
    
    print_debug "Extracted keywords: $(echo $keywords | tr '\n' ' ')"
    echo "$keywords"
}

# ============================================================================
# APPLICATION MODEL MATCHING
# ============================================================================

find_relevant_components() {
    local keywords="$1"
    local team="$2"
    local model_path="$3"
    
    print_info "🧩 Finding relevant components from Application Model..."
    
    if [[ -z "$model_path" ]] || [[ ! -d "$model_path" ]]; then
        print_warning "⚠️ No Application Model available - using keyword-based matching"
        generate_generic_components "$keywords" "$team"
        return
    fi
    
    local component_library="${model_path}/component_library.yaml"
    if [[ ! -f "$component_library" ]]; then
        print_warning "⚠️ Component library not found - generating generic components"
        generate_generic_components "$keywords" "$team"
        return
    fi
    
    # Match keywords against component library
    local relevant_components=""
    
    print_debug "Analyzing component library: $component_library"
    
    # Use keyword matching to find relevant components
    while IFS= read -r keyword; do
        [[ -z "$keyword" ]] && continue
        
        # Search for keyword in component names and descriptions
        local matches=$(grep -i "$keyword" "$component_library" 2>/dev/null | head -5)
        
        if [[ -n "$matches" ]]; then
            print_debug "Found matches for '$keyword': $matches"
            relevant_components+="$matches"$'\n'
        fi
    done <<< "$keywords"
    
    if [[ -n "$relevant_components" ]]; then
        parse_component_matches "$relevant_components" "$component_library"
    else
        print_info "📝 No specific matches found - providing team defaults"
        generate_team_defaults "$team" "$component_library"
    fi
}

parse_component_matches() {
    local matches="$1"
    local component_library="$2"
    
    # Extract component names that were matched
    local component_names=$(echo "$matches" | \
        grep -E '^\s*-\s*name:' | \
        sed 's/.*name:\s*//' | \
        head -5)
    
    print_success "✅ Found relevant components: $(echo $component_names | tr '\n' ' ')"
    
    # Extract full component definitions
    echo "$component_names" | while IFS= read -r comp_name; do
        [[ -z "$comp_name" ]] && continue
        extract_component_definition "$comp_name" "$component_library"
    done
}

extract_component_definition() {
    local comp_name="$1"
    local component_library="$2"
    
    # Extract the full component definition from YAML
    # This is a simplified extraction - in production, would use proper YAML parsing
    local in_component=false
    local indent_level=""
    
    while IFS= read -r line; do
        if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*name:[[:space:]]*$comp_name ]]; then
            in_component=true
            indent_level=$(echo "$line" | sed 's/[^ ].*//')
            echo "$line"
        elif [[ "$in_component" == true ]]; then
            local current_indent=$(echo "$line" | sed 's/[^ ].*//')
            
            # If we're back to the same indent level with a new component, stop
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*name: ]] && [[ ${#current_indent} -le ${#indent_level} ]]; then
                break
            fi
            
            # If we're at a higher level, stop
            if [[ -n "$line" ]] && [[ ${#current_indent} -lt ${#indent_level} ]]; then
                break
            fi
            
            echo "$line"
        fi
    done < "$component_library"
}

generate_team_defaults() {
    local team="$1"
    local component_library="$2"
    
    print_info "📋 Generating team default components for: $team"
    
    # Extract first few components as defaults
    head -50 "$component_library" | grep -A 10 -E '^\s*-\s*name:'
}

generate_generic_components() {
    local keywords="$1"
    local team="$2"
    
    print_info "🔧 Generating generic components based on keywords..."
    
    cat << EOF
  # Generic components based on keyword analysis for team: $team
  
  Common UI Components:
  - Navigation elements (buttons, menus, links)
  - Form inputs (text fields, dropdowns, checkboxes)
  - Tables and data displays
  - Action buttons (create, edit, delete)
  - Search and filter controls
  
  Keywords detected: $(echo $keywords | tr '\n' ' ' | head -c 100)...
EOF
}

# ============================================================================
# ACTION MATCHING
# ============================================================================

find_relevant_actions() {
    local keywords="$1"
    local team="$2"
    local model_path="$3"
    
    print_info "⚡ Finding relevant actions from Action Catalog..."
    
    local action_catalog="${model_path}/action_catalog.yaml"
    if [[ ! -f "$action_catalog" ]]; then
        generate_generic_actions "$keywords" "$team"
        return
    fi
    
    # Match keywords against actions
    local relevant_actions=""
    
    while IFS= read -r keyword; do
        [[ -z "$keyword" ]] && continue
        
        local matches=$(grep -i "$keyword" "$action_catalog" 2>/dev/null | head -3)
        if [[ -n "$matches" ]]; then
            relevant_actions+="$matches"$'\n'
        fi
    done <<< "$keywords"
    
    if [[ -n "$relevant_actions" ]]; then
        echo "$relevant_actions" | head -20
    else
        generate_team_default_actions "$team"
    fi
}

generate_generic_actions() {
    local keywords="$1"
    local team="$2"
    
    cat << EOF
  # Generic actions based on analysis for team: $team
  
  Common Actions:
  - login: Authentication and session management
  - navigate: Moving between different pages/sections
  - create: Creating new resources or entities
  - edit: Modifying existing resources
  - delete: Removing resources
  - search: Finding and filtering content
  
  Keywords suggest focus on: $(echo $keywords | head -5 | tr '\n' ' ')
EOF
}

generate_team_default_actions() {
    local team="$1"
    
    case "$team" in
        "CLC")
            cat << 'EOF'
  Cluster Lifecycle Actions:
  - createCluster: Complete cluster creation workflow
  - importCluster: Import existing cluster into management
  - upgradeCluster: Perform cluster version upgrades
  - deleteCluster: Remove managed clusters
  - searchClusters: Find clusters by name or labels
EOF
            ;;
        "ALC")
            cat << 'EOF'
  Application Lifecycle Actions:
  - createApplication: Deploy new applications
  - syncApplication: Synchronize application state
  - updateApplication: Modify application configuration
  - deleteApplication: Remove applications
EOF
            ;;
        "GRC")
            cat << 'EOF'
  Governance Actions:
  - createPolicy: Define new governance policies
  - enforcePolicy: Apply policies to clusters
  - checkCompliance: Verify policy compliance
  - remediateViolation: Fix policy violations
EOF
            ;;
        *)
            cat << 'EOF'
  General Actions:
  - login: Authenticate to the system
  - navigate: Move between sections
  - search: Find resources
  - create: Create new items
  - manage: Perform management operations
EOF
            ;;
    esac
}

# ============================================================================
# DATA PERSONAS MATCHING
# ============================================================================

find_relevant_personas() {
    local keywords="$1"
    local team="$2"
    local model_path="$3"
    
    print_info "👥 Finding relevant data personas..."
    
    local data_personas="${model_path}/data_personas.yaml"
    if [[ ! -f "$data_personas" ]]; then
        generate_generic_personas "$team"
        return
    fi
    
    # For now, just provide the first few personas
    head -30 "$data_personas" | grep -A 5 -E '^\s*-\s*name:'
}

generate_generic_personas() {
    local team="$1"
    
    cat << EOF
  # Generic data personas for team: $team
  
  User Personas:
  - Admin User: Full administrative privileges
  - Standard User: Regular user permissions
  - Viewer User: Read-only access
  
  Test Data:
  - Standard configuration settings
  - Sample resource definitions
  - Environment-specific credentials
EOF
}

# ============================================================================
# CONTEXT AUGMENTATION GENERATION
# ============================================================================

generate_augmented_context() {
    local jira_file="$1"
    local output_file="$2"
    
    print_info "📝 Generating augmented context file..."
    
    # Extract keywords from JIRA content
    local keywords=$(extract_keywords_from_jira "$jira_file")
    
    # Find relevant components, actions, and personas
    local relevant_components=$(find_relevant_components "$keywords" "$DETECTED_TEAM" "$APPLICATION_MODEL_PATH")
    local relevant_actions=$(find_relevant_actions "$keywords" "$DETECTED_TEAM" "$APPLICATION_MODEL_PATH")
    local relevant_personas=$(find_relevant_personas "$keywords" "$DETECTED_TEAM" "$APPLICATION_MODEL_PATH")
    
    # Create the augmented context file
    cat << EOF > "$output_file"
# Augmented Context for $JIRA_TICKET
# Generated: $(date -Iseconds)
# Team: $DETECTED_TEAM

## Original JIRA Content

$(cat "$jira_file")

## RELEVANT_COMPONENTS

You are analyzing a feature that appears to be related to the following areas. The Application Model has identified these pre-defined components and actions that are relevant to your analysis. You MUST prioritize using these in your test plan:

### Relevant Components:

$relevant_components

### Relevant Actions:

$relevant_actions

### Relevant Data Personas:

$relevant_personas

## Analysis Guidance

Based on the Application Model analysis:

1. **Component Priority**: Use the components listed above as your primary building blocks
2. **Action Mapping**: Map test steps to the predefined actions when possible  
3. **Data Usage**: Utilize the relevant personas for test data and user scenarios
4. **Selector Stability**: Prefer data-testid attributes and stable selectors from the component definitions
5. **Team Context**: This analysis is for the $DETECTED_TEAM team - focus on their specific workflows and patterns

## Keywords Detected

$(echo "$keywords" | head -10 | sed 's/^/- /')

---

**Note**: This augmented context ensures your generated tests align with the established Application Model and use consistent, maintainable selectors and patterns.
EOF
    
    print_success "✅ Augmented context generated: $output_file"
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    local output_file="02-analysis/augmented-context.md"
    
    print_status "🔗 Starting Context Augmentation..."
    print_info "📋 Input: $JIRA_CONTENT_FILE"
    print_info "🎯 Team: $DETECTED_TEAM"
    print_info "📁 Model: $APPLICATION_MODEL_PATH"
    
    # Generate augmented context
    generate_augmented_context "$JIRA_CONTENT_FILE" "$output_file"
    
    # Verify output
    if [[ -f "$output_file" ]] && [[ -s "$output_file" ]]; then
        local line_count=$(wc -l < "$output_file")
        print_success "✅ Context Augmentation complete!"
        print_status "📄 Generated file: $output_file ($line_count lines)"
        
        # Return the augmented file path for use by subsequent stages
        echo "$output_file"
    else
        print_error "❌ Failed to generate augmented context"
        exit 1
    fi
}

# Execute if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi