# Active Analysis Runs

This directory contains active pipeline analysis runs organized by:

```
runs/
├── <PIPELINE-ID>/
│   ├── latest -> run-XXX-YYYYMMDD-HHMM
│   ├── run-001-YYYYMMDD-HHMM/
│   │   ├── Executive-Summary.md
│   │   ├── Detailed-Analysis.md
│   │   ├── pipeline_data.json
│   │   ├── failed_tests.json
│   │   ├── intelligent_analysis.json
│   │   ├── artifacts/
│   │   └── metadata.json
│   └── run-002-YYYYMMDD-HHMM/
```

## Historical Data

Previous runs have been moved to `../archive/test-runs/` for reference.

## Usage

New analysis runs are automatically created here when using:
- `./quick-start.sh <pipeline-url>`
- `./scripts/analyze-pipeline.sh`
- `python3 scripts/modular-analysis-engine.py`