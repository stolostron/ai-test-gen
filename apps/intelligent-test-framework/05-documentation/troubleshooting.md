# Troubleshooting Guide

## Common Issues

### Claude Code Connection Issues
```bash
# Test Claude Code connectivity
claude --version
claude --print "test connection"
```

### GitHub SSH Access Issues
```bash
# Test SSH access
ssh -T git@github.com
```

### Environment Validation Failures
The framework includes intelligent handling for missing features and environment issues. Check `validation-results.json` for detailed analysis.

## Getting Help

- Check logs in `02-analysis/sessions/`
- Review validation results in `validation-results.json`  
- Use `--verbose` flag for detailed output
