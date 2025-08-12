# Z-Stream Analysis Templates

This directory contains templates and validation scripts for consistent analysis output.

## Report Templates

### `report-templates/`
- `executive-summary.md` - Template for high-level failure analysis
- `detailed-analysis.md` - Template for technical deep-dive reports
- `failure-classification.json` - Standard failure categorization schema
- `recommendations.md` - Template for actionable remediation steps

## Validation Scripts

### `validation-scripts/`
- `validate-analysis.py` - Validates analysis output completeness
- `check-jenkins-access.sh` - Verifies Jenkins connectivity and permissions
- `artifact-integrity.py` - Validates downloaded artifacts
- `report-quality.py` - Checks report quality and completeness

## Usage

Templates are automatically applied during analysis runs. For manual usage:

```bash
# Validate analysis output
python3 templates/validation-scripts/validate-analysis.py runs/pipeline-3223/

# Check Jenkins connectivity
./templates/validation-scripts/check-jenkins-access.sh
```