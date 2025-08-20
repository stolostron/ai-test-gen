# Run Analysis Engine - Quality Assessment & Improvement Tracking

## Purpose
This engine provides automated quality assessment, run comparison, and improvement tracking for the feedback loop system.

## Quality Metrics Framework

### Core Quality Dimensions
```json
{
  "quality_framework": {
    "test_coverage_completeness": {
      "weight": 20,
      "criteria": [
        "All new functionality covered",
        "Edge cases identified", 
        "Error scenarios included",
        "Integration points tested"
      ]
    },
    "business_value_alignment": {
      "weight": 25,
      "criteria": [
        "Customer requirements addressed",
        "Business impact validated",
        "Stakeholder needs met",
        "ROI considerations included"
      ]
    },
    "technical_depth_score": {
      "weight": 20,
      "criteria": [
        "Architecture understanding",
        "Implementation details",
        "Technology stack coverage",
        "Security considerations"
      ]
    },
    "execution_readiness": {
      "weight": 15,
      "criteria": [
        "Commands copy-pasteable",
        "Prerequisites clear",
        "Environment requirements",
        "Expected outputs defined"
      ]
    },
    "risk_mitigation_coverage": {
      "weight": 15,
      "criteria": [
        "Failure scenarios covered",
        "Rollback procedures",
        "Performance impact",
        "Security validation"
      ]
    },
    "security_compliance": {
      "weight": 5,
      "criteria": [
        "Security controls validated",
        "Audit trail included",
        "Access controls verified",
        "Compliance requirements"
      ]
    }
  }
}
```

## Run Comparison Algorithm

### Quality Score Calculation
```bash
calculate_quality_score() {
    local run_metadata="$1"
    local total_score=0
    local max_score=100
    
    # Extract metrics from metadata
    local coverage=$(jq '.quality_metrics.test_coverage_score' "$run_metadata")
    local business=$(jq '.quality_metrics.business_value_alignment' "$run_metadata") 
    local technical=$(jq '.quality_metrics.technical_depth_score' "$run_metadata")
    local execution=$(jq '.validation_results.execution_readiness // 80' "$run_metadata")
    local risk=$(jq '.quality_metrics.risk_mitigation_coverage' "$run_metadata")
    local security=$(jq '.comprehensive_security_enhancements.enterprise_compliance.compliance_ready // 85' "$run_metadata")
    
    # Apply weighted scoring
    total_score=$((
        ($coverage * 20 / 100) + 
        ($business * 25 / 100) + 
        ($technical * 20 / 100) + 
        ($execution * 15 / 100) + 
        ($risk * 15 / 100) + 
        ($security * 5 / 100)
    ))
    
    echo "$total_score"
}
```

### Improvement Trend Analysis
```bash
analyze_improvement_trend() {
    local ticket_id="$1"
    local runs_dir="runs/$ticket_id"
    
    # Get all runs sorted by timestamp
    local runs=($(ls "$runs_dir" | grep "^run-" | sort))
    local run_count=${#runs[@]}
    
    if [ $run_count -lt 2 ]; then
        echo "insufficient_data"
        return
    fi
    
    # Calculate quality scores for recent runs
    local scores=()
    for run in "${runs[@]:(-3)}"; do  # Last 3 runs
        local score=$(calculate_quality_score "$runs_dir/$run/metadata.json")
        scores+=("$score")
    done
    
    # Determine trend
    local latest=${scores[-1]}
    local previous=${scores[-2]}
    local improvement=$((latest - previous))
    
    if [ $improvement -gt 5 ]; then
        echo "improving"
    elif [ $improvement -gt 0 ]; then
        echo "slight_improvement"
    elif [ $improvement -eq 0 ]; then
        echo "plateau" 
    else
        echo "declining"
    fi
}
```

### Gap Identification System
```bash
identify_quality_gaps() {
    local run_metadata="$1"
    local gaps=()
    
    # Check each quality dimension
    local coverage=$(jq '.quality_metrics.test_coverage_score' "$run_metadata")
    local business=$(jq '.quality_metrics.business_value_alignment' "$run_metadata")
    local technical=$(jq '.quality_metrics.technical_depth_score' "$run_metadata")
    local security=$(jq '.comprehensive_security_enhancements.enterprise_compliance.compliance_ready // 75' "$run_metadata")
    
    # Identify gaps (threshold: 85%)
    [ $coverage -lt 85 ] && gaps+=("test_coverage")
    [ $business -lt 85 ] && gaps+=("business_alignment")
    [ $technical -lt 85 ] && gaps+=("technical_depth")
    [ $security -lt 85 ] && gaps+=("security_compliance")
    
    printf '%s\n' "${gaps[@]}"
}
```

## Run Comparison Dashboard Generator

### Dashboard Template
```bash
generate_comparison_dashboard() {
    local ticket_id="$1"
    local runs_dir="runs/$ticket_id"
    
    cat << EOF
# 📊 RUN ANALYSIS DASHBOARD - $ticket_id

## Quality Progression Analysis

$(generate_quality_table "$runs_dir")

## 📈 Improvement Trends

$(analyze_trends "$runs_dir")

## 🎯 Quality Gap Analysis

$(generate_gap_analysis "$runs_dir")

## 🔍 Detailed Comparison

$(generate_detailed_comparison "$runs_dir")

## 📋 Recommendations

$(generate_recommendations "$runs_dir")

---
*Generated by Run Analysis Engine - $(date)*
EOF
}
```

### Quality Table Generator
```bash
generate_quality_table() {
    local runs_dir="$1"
    local runs=($(ls "$runs_dir" | grep "^run-" | sort -r | head -5))
    
    echo "| Run | Timestamp | Overall | Coverage | Business | Technical | Security |"
    echo "|-----|-----------|---------|----------|----------|-----------|----------|"
    
    for run in "${runs[@]}"; do
        local metadata="$runs_dir/$run/metadata.json"
        if [ -f "$metadata" ]; then
            local timestamp=$(jq -r '.timestamp // .run_metadata.timestamp // "unknown"' "$metadata")
            local overall=$(calculate_quality_score "$metadata")
            local coverage=$(jq '.quality_metrics.test_coverage_score // 80' "$metadata")
            local business=$(jq '.quality_metrics.business_value_alignment // 80' "$metadata")
            local technical=$(jq '.quality_metrics.technical_depth_score // 80' "$metadata")
            local security=$(jq '.comprehensive_security_enhancements.enterprise_compliance.compliance_ready // 75' "$metadata")
            
            echo "| $run | $timestamp | ${overall}% | ${coverage}% | ${business}% | ${technical}% | ${security}% |"
        fi
    done
}
```

## Feedback Trigger Logic Implementation

### Multi-Criteria Trigger System
```bash
should_trigger_human_review() {
    local ticket_id="$1"
    local current_run="$2"
    
    # Criterion 1: Run count threshold
    local run_count=$(count_runs "$ticket_id")
    if [ $run_count -ge 3 ]; then
        echo "trigger:run_count_threshold:$run_count"
        return 0
    fi
    
    # Criterion 2: Quality plateau
    local trend=$(analyze_improvement_trend "$ticket_id")
    if [ "$trend" = "plateau" ] || [ "$trend" = "declining" ]; then
        echo "trigger:quality_plateau:$trend"
        return 0
    fi
    
    # Criterion 3: Low quality score
    local quality=$(calculate_quality_score "runs/$ticket_id/$current_run/metadata.json")
    if [ $quality -lt 85 ]; then
        echo "trigger:low_quality:$quality"
        return 0
    fi
    
    # Criterion 4: Time threshold (24 hours)
    local last_review=$(get_last_review_time "$ticket_id")
    local current_time=$(date +%s)
    local time_diff=$((current_time - last_review))
    if [ $time_diff -gt 86400 ]; then
        echo "trigger:time_threshold:$time_diff"
        return 0
    fi
    
    echo "no_trigger"
    return 1
}
```

### Human Review Request Generator
```bash
request_human_review() {
    local ticket_id="$1"
    local trigger_reason="$2"
    local current_run="$3"
    
    cat << EOF

🔔 ═══════════════════════════════════════════════════════════════
   HUMAN REVIEW REQUIRED - INTELLIGENT TEST ANALYSIS ENGINE
═══════════════════════════════════════════════════════════════

📋 **Ticket**: $ticket_id
🎯 **Current Run**: $current_run
⚡ **Trigger Reason**: $trigger_reason
📅 **Review Date**: $(date)

$(generate_comparison_dashboard "$ticket_id")

❓ **REVIEW QUESTIONS FOR HUMAN FEEDBACK**:

1. **Overall Quality Assessment** (1-10): 
   How would you rate the overall quality of the latest test plan?

2. **Test Coverage Adequacy** (1-10):
   Does the test plan adequately cover all necessary scenarios?

3. **Business Requirement Alignment** (1-10):
   How well does the test plan align with business requirements?

4. **Technical Approach Effectiveness** (1-10):
   Is the technical approach sound and comprehensive?

5. **Security Consideration Completeness** (1-10):
   Are security aspects adequately addressed?

📝 **IMPROVEMENT AREAS TO CONSIDER**:
$( identify_quality_gaps "runs/$ticket_id/$current_run/metadata.json" | sed 's/^/   - /' )

🔧 **SPECIFIC FEEDBACK NEEDED**:
   - [ ] More edge case coverage needed
   - [ ] Better business requirement alignment
   - [ ] security validation
   - [ ] Improved technical depth
   - [ ] Additional error handling scenarios
   - [ ] Performance testing considerations
   - [ ] Other: _______________

📋 **MISSING REQUIREMENTS** (if any):
   [Please list any requirements not adequately addressed]

🎯 **PRIORITY ADJUSTMENTS** (if needed):
   [Suggest any priority changes for test scenarios]

💬 **ADDITIONAL COMMENTS**:
   [Open feedback and suggestions]

═══════════════════════════════════════════════════════════════

Please provide your feedback above. The next test plan generation will incorporate your input for enhanced quality and alignment.

EOF
}
```

## Implementation Integration

### Main Workflow Integration Point
```bash
# Add to main test generation workflow
post_generation_feedback_check() {
    local ticket_id="$1"
    local current_run="$2"
    
    echo "🔍 Checking feedback trigger conditions..."
    
    local trigger_result=$(should_trigger_human_review "$ticket_id" "$current_run")
    
    if [[ $trigger_result != "no_trigger" ]]; then
        echo "📢 Human review triggered: $trigger_result"
        request_human_review "$ticket_id" "$trigger_result" "$current_run"
        
        echo ""
        echo "⏸️  Workflow paused for human feedback."
        echo "📋 Please provide feedback above to continue with enhanced generation."
        echo ""
        
        return 0  # Indicates human review requested
    else
        echo "✅ No human review needed at this time."
        return 1  # Continue normal workflow
    fi
}
```

### Quality Assessment Integration
```bash
# Add quality assessment to metadata generation
enhance_metadata_with_quality_assessment() {
    local metadata_file="$1"
    local ticket_id="$2"
    local current_run="$3"
    
    # Calculate quality metrics
    local quality_score=$(calculate_quality_score "$metadata_file")
    local gaps=($(identify_quality_gaps "$metadata_file"))
    local trend=$(analyze_improvement_trend "$ticket_id")
    
    # Add quality assessment to metadata
    local temp_file=$(mktemp)
    jq ". + {
        \"quality_assessment\": {
            \"overall_score\": $quality_score,
            \"improvement_trend\": \"$trend\",
            \"identified_gaps\": $(printf '%s\n' "${gaps[@]}" | jq -R . | jq -s .),
            \"assessment_timestamp\": \"$(date -Iseconds)\",
            \"ready_for_review\": $([ $quality_score -lt 85 ] && echo true || echo false)
        }
    }" "$metadata_file" > "$temp_file"
    
    mv "$temp_file" "$metadata_file"
}
```

---

**This run analysis engine provides the missing quality assessment and improvement tracking components essential for effective feedback loop operation.**