#!/bin/bash

# Claude Code Notification Hooks for Z-Stream Analysis
# This script provides audio notifications for AI response completion

# Configuration
SOUND_ENABLED=true
NOTIFICATION_VOLUME=0.7
DEFAULT_SOUND="/System/Library/Sounds/Glass.aiff"
SUCCESS_SOUND="/System/Library/Sounds/Hero.aiff"
ERROR_SOUND="/System/Library/Sounds/Sosumi.aiff"

# Function to play notification sound
play_notification() {
    local sound_file="$1"
    local description="$2"
    
    if [ "$SOUND_ENABLED" = true ]; then
        if [ -f "$sound_file" ]; then
            echo "🔔 Playing notification: $description"
            afplay "$sound_file" &
        else
            echo "⚠️ Sound file not found: $sound_file"
            # Fallback to system beep
            osascript -e 'beep'
        fi
    fi
}

# Hook: AI Response Complete
on_response_complete() {
    play_notification "$DEFAULT_SOUND" "AI response complete"
}

# Hook: Analysis Complete  
on_analysis_complete() {
    play_notification "$SUCCESS_SOUND" "Jenkins analysis complete"
}

# Hook: Error Occurred
on_error() {
    play_notification "$ERROR_SOUND" "Analysis error occurred"
}

# Hook: User Query Submitted
on_query_submitted() {
    echo "🔍 Processing query..."
}

# Main hook dispatcher
case "$1" in
    "response-complete")
        on_response_complete
        ;;
    "analysis-complete")
        on_analysis_complete
        ;;
    "error")
        on_error
        ;;
    "query-submitted")
        on_query_submitted
        ;;
    *)
        echo "Unknown hook: $1"
        ;;
esac