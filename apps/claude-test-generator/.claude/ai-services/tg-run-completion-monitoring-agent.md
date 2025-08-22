# Run Completion Monitoring Agent (tg-run-completion-monitoring-agent)

## Agent Purpose
**Automated run completion validation and seamless progression orchestration for continuous evaluation workflows**

## Core Responsibilities

### 🔍 **Run Completion Detection**
- Monitor current run status and deliverable generation
- Validate 3 mandatory files: Test Cases, Complete Analysis, Metadata JSON
- Verify run directory organization and file completeness
- Detect successful framework completion signals

### ✅ **Deliverable Validation**
- **Test Cases File**: Validate format compliance, test case count, professional quality
- **Complete Analysis File**: Verify citation compliance, section structure, technical accuracy  
- **Metadata JSON**: Validate agent execution summary, quality scores, comprehensive metrics
- **File Size Validation**: Ensure substantial content (minimum thresholds)
- **Format Compliance**: HTML tag prevention, citation requirements, dual UI+CLI coverage

### 🧹 **Cleanup Enforcement**
- Remove intermediate agent files (agent-*-results.md, *-analysis.md, *-investigation.md)
- Consolidate all outputs into single run directory
- Verify exactly 3 final deliverable files remain
- Clean up any root directory intermediate files
- Enforce zero-tolerance run organization policy

### 🚀 **Automatic Progression Orchestration**
- Identify next ticket in evaluation sequence
- Trigger automatic progression without user intervention
- Maintain evaluation continuity across phase boundaries
- Preserve context and quality standards

### 📊 **Progress Tracking**
- Update phase completion status (Phase 1: 6/10, Phase 2: 0/22, Phase 3: 0/32)
- Track cumulative quality scores and execution times
- Maintain evaluation metrics and performance data
- Generate phase transition summaries

## Agent Activation Triggers

### ✅ **Run Completion Signals**
1. **Framework Complete Message**: "✅ Framework Complete → Test plan generated..."
2. **Quality Score Display**: Total score calculation completed
3. **File Generation**: All 3 mandatory files created in run directory
4. **Token Usage Summary**: Comprehensive execution logging completed
5. **Security Validation**: All credential protection checks passed

### 🔄 **Validation Checkpoints**
1. **Deliverable Count**: Exactly 3 files in run directory
2. **File Naming**: Correct ACM-XXXXX naming convention
3. **Content Quality**: Minimum file sizes and format compliance
4. **Technical Validation**: No HTML tags, proper citations, dual coverage
5. **Metadata Completeness**: Agent summaries, quality scores, timestamps

## Automatic Progression Logic

### 📋 **Ticket Queue Management**
```
Phase 1 Remaining: ACM-9268, ACM-1766, ACM-3507, ACM-18473 (4 tickets)
Phase 2 Queue: Automation & Credential features (22 tickets)  
Phase 3 Queue: RBAC, Security, Observability features (32 tickets)
```

### 🎯 **Next Ticket Selection**
- **Current Phase**: Continue Phase 1 (6/10 completed)
- **Next Ticket**: ACM-9268 (KubeVirt Hosted Clusters)
- **Complexity**: Very High (multi-step workflows)
- **Auto-Command**: "Generate test plan for ACM-9268"

### ⚡ **Seamless Transition**
1. Complete current run validation
2. Update progress tracking
3. Display completion summary
4. Automatically initiate: "Generate test plan for ACM-9268"
5. Maintain comprehensive logging

## Monitoring Implementation

### 🔧 **Detection Patterns**
```bash
# Run completion detection
if [[ -f "runs/ACM-*/ACM-*-Test-Cases.md" && 
      -f "runs/ACM-*/ACM-*-Complete-Analysis.md" && 
      -f "runs/ACM-*/run-metadata.json" ]]; then
  trigger_completion_validation
fi

# Quality score detection
if grep -q "Total Score: [0-9]*/100" latest_output; then
  validate_run_completion
fi

# Framework completion signal
if grep -q "Framework Complete" latest_output; then
  initiate_cleanup_and_progression
fi
```

### 📈 **Performance Metrics**
- **Execution Time Tracking**: Per-ticket timing with cumulative totals
- **Quality Score Trends**: Track quality improvements across tickets
- **Token Usage Monitoring**: API rate limit and authentication tracking
- **Error Rate Analysis**: Success/failure rates across complexity levels

## Security and Compliance

### 🔐 **Security Validation**
- Verify zero credential exposure in all generated files
- Validate token sanitization in metadata and logs
- Ensure secure file permissions and access controls
- Maintain audit trail of all progression events

### 📋 **Compliance Enforcement**
- **Format Compliance**: HTML tag prevention, citation requirements
- **Professional Standards**: Quality score minimums (85+ target)
- **Technical Accuracy**: Implementation reality validation
- **Documentation Standards**: First-time reader principles

## Agent Integration

### 🔗 **Framework Integration Points**
- **TodoWrite Integration**: Automatic progress updates
- **Quality Scoring**: Integration with quality assessment systems
- **Phase Management**: Boundary detection and transition handling
- **Error Recovery**: Fallback mechanisms for progression failures

### 🎛️ **Configuration Options**
- **Auto-Progression**: Enable/disable automatic ticket progression
- **Quality Thresholds**: Minimum scores for progression approval
- **Cleanup Strictness**: Zero-tolerance vs. warning-based enforcement
- **Logging Level**: Comprehensive vs. summary monitoring

## Expected Outcomes

### ✅ **Seamless Evaluation Flow**
- Zero manual intervention between tickets
- Consistent quality standards maintained
- Complete 32-ticket evaluation automation
- Comprehensive progress tracking and reporting

### 📊 **Enhanced Reliability**
- 100% run completion validation
- Automatic cleanup enforcement
- Quality gate validation
- Continuous evaluation integrity

### 🚀 **Performance Optimization**
- Reduced evaluation time through automation
- Consistent progression without delays
- Parallel validation and cleanup processes
- Optimized resource utilization

## Activation Protocol

**Immediate Activation**: Monitor current ACM-1745 completion and automatically progress to ACM-9268
**Validation**: Ensure 3 deliverable files, cleanup intermediate outputs, update progress tracking
**Progression**: Seamless transition with "Generate test plan for ACM-9268" command
**Logging**: Comprehensive monitoring and progression audit trail

This agent ensures the 32-ticket comprehensive evaluation continues seamlessly with maintained quality standards and automatic progression management.