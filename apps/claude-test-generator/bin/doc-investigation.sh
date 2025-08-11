#!/bin/bash

# Documentation Investigation Helper Script
# Comprehensive documentation discovery and analysis

set -e

TICKET_ID="${1:-}"
OUTPUT_DIR="/tmp/claude-doc-investigation"

if [ -z "$TICKET_ID" ]; then
    echo "Usage: $0 <TICKET_ID>"
    echo "Example: $0 ACM-22079"
    exit 1
fi

echo "📚 Starting Documentation Investigation for $TICKET_ID"

# Create investigation directory
mkdir -p "$OUTPUT_DIR"

# Function to extract URLs and links from JIRA tickets (including comments)
extract_jira_docs() {
    local ticket="$1"
    local depth="${2:-0}"
    local max_depth="${3:-3}"
    
    # Prevent infinite recursion and track depth
    if [ $depth -gt $max_depth ]; then
        echo "⚠️ Maximum depth ($max_depth) reached for ticket $ticket"
        return
    fi
    
    # Skip if already processed
    if [ -f "$OUTPUT_DIR/${ticket}_processed.flag" ]; then
        echo "✅ Already processed: $ticket (depth: $depth)"
        return
    fi
    
    echo "📋 Analyzing JIRA ticket: $ticket (depth: $depth)"
    
    # Get JIRA content with comments
    jira issue view "$ticket" > "$OUTPUT_DIR/${ticket}_content.txt" 2>/dev/null || echo "⚠️ Could not fetch $ticket"
    
    if [ -f "$OUTPUT_DIR/${ticket}_content.txt" ]; then
        # Extract URLs from entire content (description + comments)
        grep -oE 'https://[^[:space:]]+' "$OUTPUT_DIR/${ticket}_content.txt" > "$OUTPUT_DIR/${ticket}_urls.txt" || touch "$OUTPUT_DIR/${ticket}_urls.txt"
        
        # Extract GitHub URLs specifically
        grep -oE 'https://github\.com/[^[:space:]]+' "$OUTPUT_DIR/${ticket}_content.txt" > "$OUTPUT_DIR/${ticket}_github_urls.txt" || touch "$OUTPUT_DIR/${ticket}_github_urls.txt"
        
        # Extract documentation URLs specifically  
        grep -oE 'https://docs\.redhat\.com/[^[:space:]]+\|https://access\.redhat\.com/[^[:space:]]+' "$OUTPUT_DIR/${ticket}_content.txt" > "$OUTPUT_DIR/${ticket}_doc_urls.txt" || touch "$OUTPUT_DIR/${ticket}_doc_urls.txt"
        
        # Extract linked tickets (all formats: ACM-XXXXX, OCPBUGS-XXXXX, etc.)
        grep -oE '[A-Z]+-[0-9]+' "$OUTPUT_DIR/${ticket}_content.txt" | sort -u > "$OUTPUT_DIR/${ticket}_linked_tickets.txt" || touch "$OUTPUT_DIR/${ticket}_linked_tickets.txt"
        
        # Extract PR references from comments and descriptions
        grep -oE 'pull/[0-9]+\|PR #[0-9]+\|#[0-9]+' "$OUTPUT_DIR/${ticket}_content.txt" > "$OUTPUT_DIR/${ticket}_pr_refs.txt" || touch "$OUTPUT_DIR/${ticket}_pr_refs.txt"
        
        # Extract comments section specifically for additional analysis
        sed -n '/Comments/,$p' "$OUTPUT_DIR/${ticket}_content.txt" > "$OUTPUT_DIR/${ticket}_comments.txt" 2>/dev/null || touch "$OUTPUT_DIR/${ticket}_comments.txt"
        
        echo "📎 Found URLs in $ticket:"
        [ -s "$OUTPUT_DIR/${ticket}_urls.txt" ] && cat "$OUTPUT_DIR/${ticket}_urls.txt" || echo "  No URLs found"
        
        echo "🐙 Found GitHub links in $ticket:"
        [ -s "$OUTPUT_DIR/${ticket}_github_urls.txt" ] && cat "$OUTPUT_DIR/${ticket}_github_urls.txt" || echo "  No GitHub links found"
        
        echo "📚 Found documentation links in $ticket:"
        [ -s "$OUTPUT_DIR/${ticket}_doc_urls.txt" ] && cat "$OUTPUT_DIR/${ticket}_doc_urls.txt" || echo "  No documentation links found"
        
        echo "🔗 Found linked tickets in $ticket:"
        [ -s "$OUTPUT_DIR/${ticket}_linked_tickets.txt" ] && cat "$OUTPUT_DIR/${ticket}_linked_tickets.txt" || echo "  No linked tickets found"
        
        echo "🔀 Found PR references in $ticket:"
        [ -s "$OUTPUT_DIR/${ticket}_pr_refs.txt" ] && cat "$OUTPUT_DIR/${ticket}_pr_refs.txt" || echo "  No PR references found"
        
        # Mark as processed
        touch "$OUTPUT_DIR/${ticket}_processed.flag"
        
        # Recursively process linked tickets
        if [ -s "$OUTPUT_DIR/${ticket}_linked_tickets.txt" ]; then
            while read -r linked_ticket; do
                if [ -n "$linked_ticket" ] && [ "$linked_ticket" != "$ticket" ]; then
                    echo "🔄 Recursively processing linked ticket: $linked_ticket (from $ticket)"
                    extract_jira_docs "$linked_ticket" $((depth + 1)) $max_depth
                fi
            done < "$OUTPUT_DIR/${ticket}_linked_tickets.txt"
        fi
    fi
}

# Function to analyze documentation URLs
analyze_doc_urls() {
    echo "📖 Analyzing documentation URLs..."
    
    # Combine all URLs from all tickets
    cat "$OUTPUT_DIR"/*_urls.txt 2>/dev/null | sort -u > "$OUTPUT_DIR/all_urls.txt" || touch "$OUTPUT_DIR/all_urls.txt"
    
    # Categorize URLs
    echo "📚 Red Hat Documentation URLs:" > "$OUTPUT_DIR/redhat_docs.txt"
    grep -i "docs.redhat.com\|access.redhat.com" "$OUTPUT_DIR/all_urls.txt" >> "$OUTPUT_DIR/redhat_docs.txt" 2>/dev/null || echo "  None found" >> "$OUTPUT_DIR/redhat_docs.txt"
    
    echo "🐙 GitHub URLs:" > "$OUTPUT_DIR/github_links.txt"
    grep -i "github.com" "$OUTPUT_DIR/all_urls.txt" >> "$OUTPUT_DIR/github_links.txt" 2>/dev/null || echo "  None found" >> "$OUTPUT_DIR/github_links.txt"
    
    echo "📋 Confluence/Wiki URLs:" > "$OUTPUT_DIR/wiki_links.txt"
    grep -i "confluence\|wiki" "$OUTPUT_DIR/all_urls.txt" >> "$OUTPUT_DIR/wiki_links.txt" 2>/dev/null || echo "  None found" >> "$OUTPUT_DIR/wiki_links.txt"
    
    echo "🔗 Other Documentation URLs:" > "$OUTPUT_DIR/other_docs.txt"
    grep -v -i "docs.redhat.com\|access.redhat.com\|github.com\|confluence\|wiki" "$OUTPUT_DIR/all_urls.txt" >> "$OUTPUT_DIR/other_docs.txt" 2>/dev/null || echo "  None found" >> "$OUTPUT_DIR/other_docs.txt"
}

# Function to analyze comments for additional insights
analyze_comments() {
    echo "💬 Analyzing comments across all tickets for additional insights..."
    
    # Combine all comments for analysis
    cat "$OUTPUT_DIR"/*_comments.txt 2>/dev/null > "$OUTPUT_DIR/all_comments.txt" || touch "$OUTPUT_DIR/all_comments.txt"
    
    # Extract additional URLs from comments
    grep -oE 'https://[^[:space:]]+' "$OUTPUT_DIR/all_comments.txt" > "$OUTPUT_DIR/comments_urls.txt" 2>/dev/null || touch "$OUTPUT_DIR/comments_urls.txt"
    
    # Extract key insights from comments (implementation notes, decisions, etc.)
    grep -i -E '(implementation|decision|approach|solution|workaround|fix|bug|issue)' "$OUTPUT_DIR/all_comments.txt" > "$OUTPUT_DIR/comments_insights.txt" 2>/dev/null || touch "$OUTPUT_DIR/comments_insights.txt"
    
    echo "💬 Found additional URLs in comments:"
    [ -s "$OUTPUT_DIR/comments_urls.txt" ] && cat "$OUTPUT_DIR/comments_urls.txt" || echo "  No additional URLs in comments"
    
    echo "💡 Found implementation insights in comments:"
    [ -s "$OUTPUT_DIR/comments_insights.txt" ] && head -10 "$OUTPUT_DIR/comments_insights.txt" || echo "  No implementation insights found"
}

# Main investigation flow with complete hierarchy traversal
echo "🔍 Starting comprehensive documentation discovery with nested ticket analysis..."

# 1. Analyze main ticket and ALL linked tickets recursively (up to 3 levels deep)
echo "📋 Phase 1: Recursive ticket analysis (main ticket + all nested linked tickets)"
extract_jira_docs "$TICKET_ID" 0 3

# 2. Analyze comments across all discovered tickets
echo "💬 Phase 2: Comments analysis across all discovered tickets"
analyze_comments

# 3. Analyze and categorize all discovered URLs
analyze_doc_urls

# 4. Generate comprehensive summary report
echo "📊 Generating Comprehensive Documentation Investigation Summary..."
cat > "$OUTPUT_DIR/investigation_summary.md" << EOF
# Comprehensive Documentation Investigation Summary for $TICKET_ID

## 📋 Complete Ticket Hierarchy Analyzed
$(find "$OUTPUT_DIR" -name "*_processed.flag" -exec basename {} \; | sed 's/_processed.flag//' | sort)
**Total tickets processed:** $(find "$OUTPUT_DIR" -name "*_processed.flag" | wc -l)

## 📚 Documentation Categories Found

### Red Hat Documentation
$(cat "$OUTPUT_DIR/redhat_docs.txt")

### GitHub References  
$(cat "$OUTPUT_DIR/github_links.txt")

### Wiki/Confluence Links
$(cat "$OUTPUT_DIR/wiki_links.txt")

### Other Documentation
$(cat "$OUTPUT_DIR/other_docs.txt")

## 🔀 PR References Discovered
$(cat "$OUTPUT_DIR"/*_pr_refs.txt 2>/dev/null | sort -u | head -10)

## 💬 Comment Insights
### Additional URLs from Comments
$(cat "$OUTPUT_DIR/comments_urls.txt" 2>/dev/null | head -5)

### Implementation Insights from Comments  
$(cat "$OUTPUT_DIR/comments_insights.txt" 2>/dev/null | head -5)

## 🔍 Investigation Commands for Framework
\`\`\`bash
# Primary documentation URLs for WebFetch:
$(cat "$OUTPUT_DIR/all_urls.txt" 2>/dev/null | head -10 | sed 's/^/# WebFetch: /')

# GitHub URLs for repository investigation:
$(cat "$OUTPUT_DIR"/*_github_urls.txt 2>/dev/null | sort -u | head -5 | sed 's/^/# GitHub: /')

# PR references for detailed analysis:
$(cat "$OUTPUT_DIR"/*_pr_refs.txt 2>/dev/null | sort -u | head -5 | sed 's/^/# PR Analysis: /')
\`\`\`

## 📋 Complete Linked Ticket Network
$(cat "$OUTPUT_DIR"/*_linked_tickets.txt 2>/dev/null | sort -u)

## 🎯 Investigation Quality Metrics
- **Ticket Depth:** 3 levels of nested ticket analysis
- **Comments Coverage:** All comments analyzed for additional insights
- **URL Discovery:** $(cat "$OUTPUT_DIR/all_urls.txt" 2>/dev/null | wc -l) unique URLs found
- **GitHub Links:** $(cat "$OUTPUT_DIR"/*_github_urls.txt 2>/dev/null | sort -u | wc -l) GitHub references discovered
- **PR References:** $(cat "$OUTPUT_DIR"/*_pr_refs.txt 2>/dev/null | sort -u | wc -l) PR references found
EOF

echo "✅ Documentation Investigation complete!"
echo "📁 Results saved to: $OUTPUT_DIR/investigation_summary.md"
echo ""
echo "📖 Next Steps:"
echo "1. Review $OUTPUT_DIR/investigation_summary.md"
echo "2. Use WebFetch on discovered documentation URLs"
echo "3. Perform targeted internet searches based on findings"
echo "4. Cross-reference with GitHub repository documentation"