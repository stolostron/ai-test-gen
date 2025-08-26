# JIRA API Configuration Guide

## Overview
The Version Intelligence Service now supports real JIRA API integration with graceful fallback to simulation.

## Configuration Options

### Option 1: Environment Variables (Recommended)
```bash
export JIRA_BASE_URL="https://issues.redhat.com"
export JIRA_USERNAME="your.email@redhat.com" 
export JIRA_API_TOKEN="your_api_token"
export JIRA_VERIFY_SSL="true"
export JIRA_TIMEOUT="30"
export JIRA_CACHE_DURATION="300"
```

### Option 2: Configuration File
Create `.claude/config/jira_config.json`:
```json
{
  "base_url": "https://issues.redhat.com",
  "username": "your.email@redhat.com",
  "api_token": "your_api_token",
  "verify_ssl": true,
  "timeout": 30,
  "cache_duration": 300,
  "fallback_to_simulation": true
}
```

## Getting JIRA API Token

### Red Hat JIRA
1. Go to https://issues.redhat.com
2. Login → Profile → Personal Access Tokens
3. Create token with appropriate scopes
4. Use token as `JIRA_API_TOKEN`

### Other JIRA Instances  
1. Go to your JIRA instance
2. Account Settings → Security → API Tokens
3. Create new token
4. Use token as `JIRA_API_TOKEN`

## Testing Connection
```bash
# Test JIRA client directly
python3 .claude/ai-services/jira_api_client.py ACM-22079

# Test with Version Intelligence Service
python3 .claude/ai-services/version_intelligence_service.py ACM-22079
```

## Development Mode
- **No configuration needed** - automatically uses simulation
- All functionality works without JIRA credentials
- Enhanced simulation provides realistic data

## Production Benefits
- **Real ticket data** - latest status, versions, components
- **Caching** - improved performance with 5-minute cache
- **Error resilience** - automatic fallback to simulation on API failures
- **Authentication** - secure token-based access

## Troubleshooting

### Connection Issues
```
WARNING: JIRA API connection failed: Not authenticated
```
- Check credentials in environment variables or config file
- Verify network access to JIRA instance
- System will automatically use simulation fallback

### API Rate Limits
- Built-in caching reduces API calls
- Exponential backoff for retry logic
- Graceful degradation to simulation

### SSL Issues
```bash
export JIRA_VERIFY_SSL="false"  # Only for development
```

## Status Verification
The Version Intelligence Service logs show JIRA status:
```
INFO: JIRA API client connected successfully: Connected as John Doe
INFO: Successfully retrieved ACM-12345 via JIRA API
```

Or fallback mode:
```
WARNING: JIRA API connection failed: Not authenticated
INFO: Using enhanced simulation for ACM-12345
```