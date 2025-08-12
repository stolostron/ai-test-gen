# Z-Stream Analysis Scripts

This directory contains the core analysis scripts for pipeline failure analysis.

## Core Scripts

- `pipeline_analyzer.py` - Main pipeline analysis engine
- `failure_classifier.py` - AI-powered failure classification
- `artifact_extractor.py` - Jenkins artifact extraction
- `report_generator.py` - Analysis report generation
- `quick-start.sh` - Quick launcher script

## Usage

Each script includes built-in help:
```bash
python3 scripts/pipeline_analyzer.py --help
```

For the unified interface, use:
```bash
./quick-start.sh <pipeline-url>
```