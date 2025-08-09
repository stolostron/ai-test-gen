#!/bin/bash

# YAML Utilities for Application Model Management
# Provides functions for reading, writing, and manipulating YAML files

# Check if yq is available
check_yq() {
    if ! command -v yq >/dev/null 2>&1; then
        print_warning "⚠️ yq not found - using basic text processing"
        return 1
    fi
    return 0
}

# Read YAML value
read_yaml() {
    local file="$1"
    local path="$2"
    
    if [[ ! -f "$file" ]]; then
        echo ""
        return 1
    fi
    
    if check_yq; then
        yq eval "$path" "$file" 2>/dev/null || echo ""
    else
        # Basic fallback - not as robust as yq
        grep "^${path//./}: " "$file" | cut -d':' -f2- | xargs || echo ""
    fi
}

# Write YAML value
write_yaml() {
    local file="$1"
    local path="$2"
    local value="$3"
    
    if check_yq; then
        yq eval "${path} = \"${value}\"" -i "$file" 2>/dev/null
    else
        # Basic fallback
        if grep -q "^${path//./}: " "$file" 2>/dev/null; then
            sed -i.bak "s|^${path//./}: .*|${path//./}: ${value}|" "$file"
        else
            echo "${path//./}: ${value}" >> "$file"
        fi
    fi
}

# Merge YAML files
merge_yaml() {
    local target="$1"
    local source="$2"
    
    if check_yq; then
        yq eval-all 'select(fileIndex == 0) * select(fileIndex == 1)' "$target" "$source" > "${target}.tmp"
        mv "${target}.tmp" "$target"
    else
        # Basic append for fallback
        cat "$source" >> "$target"
    fi
}

# Validate YAML syntax
validate_yaml() {
    local file="$1"
    
    if check_yq; then
        yq eval '.' "$file" >/dev/null 2>&1
    else
        # Basic check - just ensure file is readable
        [[ -r "$file" ]]
    fi
}

# Convert JSON to YAML
json_to_yaml() {
    local json_data="$1"
    
    if check_yq; then
        echo "$json_data" | yq eval -P '.'
    else
        # Basic conversion - just format as YAML-like
        echo "$json_data" | sed 's/{//' | sed 's/}//' | sed 's/,$//' | sed 's/"//g' | sed 's/:/: /'
    fi
}