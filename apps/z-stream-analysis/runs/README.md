# Analysis Runs Directory - Z-Stream Analysis Engine

**Directory:** `/runs/`  
**Purpose:** Organized storage of Jenkins pipeline failure analysis results  
**Format:** Timestamped analysis runs with comprehensive investigation reports

---

## Directory Structure Standard

### Naming Convention
```
runs/
├── README.md                                    # This documentation
├── <pipeline-id>_<YYYYMMDD_HHMMSS>/            # Timestamped analysis run
│   ├── Detailed-Analysis.md                    # Complete investigation report
│   ├── analysis-metadata.json                  # Analysis execution metadata
│   └── jenkins-metadata.json                   # Jenkins data extraction results
└── <pipeline-id>_<YYYYMMDD_HHMMSS>/            # Additional runs for same pipeline
    ├── Detailed-Analysis.md                    # Each run gets unique timestamp
    ├── analysis-metadata.json                  
    └── jenkins-metadata.json                   
```

### Example Structure
```
runs/
├── clc-e2e-pipeline-3223_20250812_174948/     # First analysis run
│   ├── Detailed-Analysis.md                   # Comprehensive investigation
│   ├── analysis-metadata.json                 # Analysis process tracking
│   └── jenkins-metadata.json                  # Jenkins API data extraction
├── clc-e2e-pipeline-3223_20250812_180000/     # Second analysis run (same pipeline)
│   ├── Detailed-Analysis.md                   # Updated investigation
│   ├── analysis-metadata.json                 
│   └── jenkins-metadata.json                  
└── clc-e2e-pipeline-3224_20250812_181500/     # Different pipeline analysis
    ├── Detailed-Analysis.md                   
    ├── analysis-metadata.json                 
    └── jenkins-metadata.json                  
```

---

## File Specifications

### 1. Detailed-Analysis.md
**Purpose:** Single comprehensive report containing all analysis phases  
**Format:** Markdown with structured sections  
**Content Includes:**
- 🎯 **Definitive Verdict** (PRODUCT BUG | AUTOMATION BUG | AUTOMATION GAP)
- 📋 **Executive Summary** with business impact
- 🔍 **6-Phase Investigation Methodology**
- 🛠️ **Complete Fix Implementation Guide**
- 📊 **Quality Assessment and Metrics**
- 📝 **Evidence Documentation and Validation**

### 2. analysis-metadata.json
**Purpose:** Analysis execution tracking and process metadata  
**Format:** Structured JSON  
**Content Includes:**
```json
{
  "analysis_id": "pipeline-id_timestamp",
  "pipeline_id": "clc-e2e-pipeline-3223", 
  "jenkins_url": "https://jenkins-server/job/pipeline/123/",
  "analysis_timestamp": "2025-08-12T17:49:48Z",
  "verdict": "AUTOMATION BUG",
  "confidence_level": 100,
  "investigation_phases": { ... },
  "quality_metrics": { ... },
  "fix_assessment": { ... }
}
```

### 3. jenkins-metadata.json
**Purpose:** Raw Jenkins data extraction results  
**Format:** Structured JSON  
**Content Includes:**
```json
{
  "extraction_timestamp": "2025-08-12T17:49:48Z",
  "jenkins_api_data": { ... },
  "git_information": { ... },
  "test_environment": { ... },
  "test_execution_summary": { ... },
  "failure_details": { ... },
  "api_status_evidence": { ... }
}
```

---

## Analysis Run Standards

### Timestamp Format
- **Pattern:** `YYYYMMDD_HHMMSS`
- **Example:** `20250812_174948` (2025-08-12 17:49:48)
- **Timezone:** Local system time
- **Uniqueness:** Ensures no directory conflicts for repeat analyses

### Multiple Runs Policy
- **Same Pipeline:** Each new analysis gets unique timestamp directory
- **Historical Preservation:** All previous analyses maintained
- **Comparison Support:** Easy comparison between analysis runs
- **Version Control:** Track investigation evolution over time

### Content Standards
- **Single Report Format:** One comprehensive `Detailed-Analysis.md` per run
- **Self-Contained:** Each analysis directory contains complete investigation
- **Standardized Structure:** Consistent format across all analysis runs
- **Quality Assured:** All reports include quality metrics and validation

---

## Usage Patterns

### Creating New Analysis
```bash
# Framework automatically creates timestamped directory
# Example: runs/clc-e2e-pipeline-3223_20250812_174948/

# User provides Jenkins URL, framework handles:
# 1. Timestamp generation
# 2. Directory creation
# 3. Data extraction
# 4. Analysis execution
# 5. Report generation
```

### Viewing Results
```bash
# List all analysis runs
ls -la runs/

# View latest analysis for specific pipeline
find runs/ -name "clc-e2e-pipeline-3223_*" | sort | tail -1

# Read comprehensive analysis
cat runs/clc-e2e-pipeline-3223_20250812_174948/Detailed-Analysis.md

# Check analysis metadata
jq . runs/clc-e2e-pipeline-3223_20250812_174948/analysis-metadata.json
```

### Comparison Analysis
```bash
# Compare verdicts across multiple runs
grep "VERDICT:" runs/clc-e2e-pipeline-3223_*/Detailed-Analysis.md

# Compare quality scores
jq '.quality_metrics.overall_score' runs/clc-e2e-pipeline-3223_*/analysis-metadata.json

# Track investigation evolution
diff runs/clc-e2e-pipeline-3223_20250812_174948/Detailed-Analysis.md \
     runs/clc-e2e-pipeline-3223_20250812_180000/Detailed-Analysis.md
```

---

## Quality Standards

### Analysis Quality Requirements
- ✅ **Definitive Verdict** with 90%+ confidence
- ✅ **Comprehensive Evidence** from multiple data sources
- ✅ **Actionable Solutions** with implementation details
- ✅ **Business Context** with stakeholder impact assessment
- ✅ **Quality Validation** with transparent metrics

### Documentation Standards
- ✅ **Consistent Format** across all analysis runs
- ✅ **Complete Investigation** covering all 6 phases
- ✅ **Evidence-Based** conclusions with data support
- ✅ **Professional Presentation** suitable for stakeholders
- ✅ **Technical Accuracy** verified against source data

### Organizational Standards
- ✅ **Unique Timestamps** prevent directory conflicts
- ✅ **Preserved History** maintains all analysis runs
- ✅ **Structured Storage** enables easy navigation and comparison
- ✅ **Metadata Tracking** supports process improvement
- ✅ **Self-Contained** analyses for distribution and archival

---

## Current Migration Status

### New Standard (Framework v2.0)
```
✅ clc-e2e-pipeline-3223_20250812_174948/   # New timestamped format
    ├── Detailed-Analysis.md                # Single comprehensive report
    ├── analysis-metadata.json             # Process tracking
    └── jenkins-metadata.json              # Data extraction results
```

### Legacy Directories (Framework v1.x)
```
📁 clc-e2e-pipeline-3223/                  # Legacy format (preserved)
📁 clc-e2e-pipeline-3223-analysis/         # Legacy format (preserved)
📁 clc-e2e-pipeline-3223-enhanced-test/    # Legacy format (preserved)
📁 clc-e2e-pipeline-3223-ai-test/          # Legacy format (preserved)
```

**Migration Policy:** Legacy directories preserved for historical reference. All new analyses use timestamped format.

---

## Integration Points

### AI-Powered Analysis Workflow
```markdown
# Natural language interface - no manual directory management
"Analyze this Jenkins pipeline failure: https://jenkins-url/job/pipeline/123/"

# Framework automatically:
# ✅ Generates timestamp: 20250812_174948
# ✅ Creates directory: runs/pipeline-123_20250812_174948/
# ✅ Extracts Jenkins data
# ✅ Performs comprehensive analysis
# ✅ Generates single detailed report
# ✅ Validates analysis quality
```

### Unified Commands (from root repository)
```bash
# These commands automatically use new standardized format
/analyze-pipeline-failures {JENKINS_URL}
/analyze-workflow pipeline-failure {PIPELINE_ID}  
/quick-start z-stream-analysis {PIPELINE_ID}
```

---

**Framework Version:** 2.0 - Standardized timestamped analysis runs with comprehensive single-report format  
**Status:** Production-ready with legacy preservation and new standard implementation