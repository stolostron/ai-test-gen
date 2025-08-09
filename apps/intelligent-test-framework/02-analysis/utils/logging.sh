#!/bin/bash

# Logging utilities for the AI Test Framework

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
NC='\033[0m' # No Color

# Log levels
LOG_LEVEL=${LOG_LEVEL:-"INFO"}

# Print functions
print_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" >&2
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" >&2
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1" >&2
}

print_status() {
    echo -e "${CYAN}[STATUS]${NC} $1" >&2
}

print_debug() {
    if [[ "$LOG_LEVEL" == "DEBUG" ]]; then
        echo -e "${PURPLE}[DEBUG]${NC} $1"
    fi
}

# Log to file with timestamp
log_to_file() {
    local message="$1"
    local log_file="${LOG_FILE:-/tmp/ai-framework.log}"
    
    echo "$(date -Iseconds) - $message" >> "$log_file"
}