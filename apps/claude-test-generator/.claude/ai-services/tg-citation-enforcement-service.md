# Test Generator Citation Enforcement Service

## 🔒 AI Service Overview

**Service Name**: TG Citation Enforcement Service  
**Purpose**: Real-time validation of all citations in complete reports before AI response generation  
**Integration Level**: MANDATORY - All complete reports must pass citation validation  
**Service Status**: V1.0 - Production Ready with Zero-Tolerance Policy

## 🚨 CRITICAL ENFORCEMENT PROTOCOL

### 🔍 Pre-Response Citation Validation
**MANDATORY PROCESS**: Every complete report undergoes citation validation BEFORE user delivery:

1. **Extract All Claims**: Identify every factual statement in the draft response
2. **Require Citation Evidence**: Each claim must include proper citation format
3. **Real-Time Validation**: Validate each citation against live sources
4. **Block Invalid Responses**: Prevent delivery of responses with failed citations
5. **Audit Trail Generation**: Log all validation attempts for compliance

### 📋 Citation Validation Framework

#### JIRA Ticket Validation
```markdown
## JIRA Citation Validation Protocol

**Format Required**: [JIRA:ACM-XXXXX:status:last_updated]

**Validation Steps**:
1. **Ticket Existence Check**: Verify ticket exists in JIRA system
2. **Status Verification**: Confirm current status matches citation
3. **Accessibility Test**: Ensure ticket is readable (not restricted)
4. **Timestamp Validation**: Verify last_updated timestamp accuracy
5. **Content Correlation**: Ensure claim semantically matches ticket content

**Validation Examples**:
✅ VALID: [JIRA:ACM-22079:Closed:2024-01-15] - Verified ticket exists, status correct
❌ INVALID: [JIRA:ACM-99999:Open:2024-01-15] - Ticket does not exist
❌ INVALID: [JIRA:ACM-22079:Open:2024-01-15] - Status mismatch (actually Closed)
```

#### GitHub Reference Validation
```markdown
## GitHub Citation Validation Protocol

**Format Required**: [GitHub:org/repo#PR/issue:state:commit_sha]

**Validation Steps**:
1. **Repository Access**: Verify repository exists and is accessible
2. **PR/Issue Existence**: Confirm PR or issue number exists
3. **State Verification**: Validate current state (open/closed/merged)
4. **Commit Verification**: Verify commit SHA exists and is accessible
5. **Content Correlation**: Ensure claim matches PR/issue content

**Validation Examples**:
✅ VALID: [GitHub:stolostron/cluster-curator-controller#468:merged:a1b2c3d4]
❌ INVALID: [GitHub:stolostron/nonexistent-repo#468:merged:a1b2c3d4] - Repository not found
❌ INVALID: [GitHub:stolostron/cluster-curator-controller#999999:merged:a1b2c3d4] - PR does not exist
```

#### Documentation Reference Validation
```markdown
## Documentation Citation Validation Protocol

**Format Required**: [Docs:URL#section:last_verified]

**Validation Steps**:
1. **URL Accessibility**: HTTP GET request returns 200 status
2. **Content Retrieval**: Successfully fetch page content
3. **Section Verification**: Locate specified section in content (if provided)
4. **Timestamp Validation**: Verify last_verified timestamp is recent
5. **Content Correlation**: Ensure claim is supported by documentation

**Validation Examples**:
✅ VALID: [Docs:https://access.redhat.com/documentation/acm#cluster-management:2024-01-15]
❌ INVALID: [Docs:https://nonexistent.redhat.com/docs:2024-01-15] - URL returns 404
❌ INVALID: [Docs:https://access.redhat.com/documentation/acm#nonexistent-section:2024-01-15] - Section not found
```

#### Code Reference Validation
```markdown
## Code Citation Validation Protocol

**Format Required**: [Code:file_path:lines:commit_sha]

**Validation Steps**:
1. **Repository State**: Verify repository is accessible and current
2. **File Existence**: Confirm file exists at specified path
3. **Line Range Validation**: Verify line numbers exist and are valid
4. **Commit Verification**: Ensure commit SHA is valid and accessible
5. **Content Correlation**: Confirm claim matches actual code content

**Validation Examples**:
✅ VALID: [Code:pkg/controllers/cluster.go:156-162:a1b2c3d4]
❌ INVALID: [Code:nonexistent/file.go:1-10:a1b2c3d4] - File not found
❌ INVALID: [Code:pkg/controllers/cluster.go:999-1005:a1b2c3d4] - Line numbers exceed file length
```

#### Environment Reference Validation
```markdown
## Environment Citation Validation Protocol

**Format Required**: [Env:environment_name:health_status:last_verified]

**Validation Steps**:
1. **Environment Accessibility**: Verify API endpoint responds (200 OK)
2. **Console Accessibility**: Verify console URL responds (200 OK)  
3. **Health Status Verification**: Confirm current health matches citation
4. **Timestamp Validation**: Verify last_verified is recent (within 24 hours)
5. **Environment Data Correlation**: Ensure claim matches actual environment state

**Validation Examples**:
✅ VALID: [Env:ashafi-atif-test:healthy:2025-08-21] - Environment accessible, health verified
❌ INVALID: [Env:nonexistent-cluster:healthy:2025-08-21] - Environment not accessible
❌ INVALID: [Env:ashafi-atif-test:unhealthy:2025-08-21] - Health status mismatch
❌ INVALID: [Env:ashafi-atif-test:healthy:2025-07-01] - Timestamp too old (over 30 days)
```

## 🚫 CITATION ENFORCEMENT RULES

### Blocked Response Categories
**COMPLETE REPORTS ONLY** - The following responses are BLOCKED without valid citations:

#### Feature Analysis Claims
- ❌ "ACM supports automated cluster management"
- ✅ "ACM supports automated cluster management [JIRA:ACM-22156:Closed:2024-01-15] [Docs:https://access.redhat.com/documentation/acm#auto-management:2024-01-15]"

#### Component Behavior Claims
- ❌ "The cluster controller handles lifecycle operations"
- ✅ "The cluster controller handles lifecycle operations [Code:pkg/controllers/cluster.go:89-156:c4d5e6f7] including creation, scaling, and deletion"

#### API Endpoint Claims
- ❌ "The /api/v1/clusters endpoint accepts POST requests"
- ✅ "The /api/v1/clusters endpoint accepts POST requests [Code:pkg/api/routes.go:45-52:d5e6f7g8] for cluster creation operations"

#### Test Strategy Claims
- ❌ "E2E tests should verify cluster provisioning"
- ✅ "E2E tests should verify cluster provisioning [Code:tests/e2e/cluster_provision_test.go:23-67:e6f7g8h9] following the established pattern"

## 🎯 CITATION SCOPE ENFORCEMENT

### Complete Reports - MANDATORY CITATIONS
**Sections Requiring Citations**:
- Feature analysis tables (with learning references)
- Technical architecture descriptions
- Component behavior explanations
- API endpoint documentation
- Test strategy justifications
- Risk assessments and assumptions

### Test Tables Only - NO CITATIONS
**Clean Format Maintained**:
- Summary test case tables
- Test execution steps
- Expected results columns
- Priority classifications

## 🔧 VALIDATION IMPLEMENTATION

### Real-Time Citation Format Enforcement Engine
```python
def enforce_citation_metadata_format(complete_report_content):
    """
    Critical: Validate all citations follow exact metadata format requirements
    """
    # Define exact citation format patterns
    valid_citation_patterns = {
        'jira': r'\[JIRA:[A-Z]+-\d+:(Open|In Progress|Review|Resolved|Closed):\d{4}-\d{2}-\d{2}\]',
        'github': r'\[GitHub:[^/]+/[^#]+#\d+:(open|closed|merged):\d{4}-\d{2}-\d{2}\]',
        'environment': r'\[Env:[^:]+:(healthy|unhealthy|unknown):\d{4}-\d{2}-\d{2}\]',
        'documentation': r'\[Docs:https://[^#]+#[^:]+:\d{4}-\d{2}-\d{2}\]',
        'code': r'\[Code:[^:]+:\d+-\d+:[a-f0-9]{7,40}\]'
    }
    
    # Find all citation-like patterns
    all_citations = re.findall(r'\[[^\]]+\](?=\(https?://[^\)]+\))', complete_report_content)
    
    violations = []
    for citation in all_citations:
        is_valid = False
        for citation_type, pattern in valid_citation_patterns.items():
            if re.match(pattern, citation):
                is_valid = True
                break
        
        if not is_valid:
            violations.append({
                "citation": citation,
                "error": "Invalid metadata format - missing or incorrect status/date",
                "required_formats": [
                    "[JIRA:ACM-XXXXX:status:YYYY-MM-DD]",
                    "[GitHub:org/repo#PR:state:YYYY-MM-DD]", 
                    "[Env:name:health:YYYY-MM-DD]",
                    "[Docs:URL#section:YYYY-MM-DD]",
                    "[Code:file:lines:commit]"
                ]
            })
    
    if violations:
        return {
            "status": "CRITICAL_BLOCK",
            "violations": violations,
            "action": "FIX_CITATION_METADATA",
            "message": "All citations must include required metadata (status/state/health + date)",
            "blocking_priority": "ABSOLUTE"
        }
    
    return {"status": "APPROVED", "citation_format": "valid_metadata"}

def enforce_citation_accessibility(complete_report_content):
    """
    Validate that all cited sources are accessible and current
    """
    import requests
    import re
    from datetime import datetime, timedelta
    
    # Extract all clickable citations with URLs
    citation_url_pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    citations_with_urls = re.findall(citation_url_pattern, complete_report_content)
    
    validation_results = []
    for citation_text, url in citations_with_urls:
        result = {
            "citation": citation_text,
            "url": url,
            "status": "UNKNOWN",
            "error": None
        }
        
        try:
            # Test URL accessibility
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                result["status"] = "ACCESSIBLE"
            else:
                result["status"] = "INACCESSIBLE" 
                result["error"] = f"HTTP {response.status_code}"
        except Exception as e:
            result["status"] = "INACCESSIBLE"
            result["error"] = str(e)
        
        # Validate date freshness for environment citations
        if citation_text.startswith("Env:"):
            parts = citation_text.split(":")
            if len(parts) >= 4:
                try:
                    citation_date = datetime.strptime(parts[3], "%Y-%m-%d")
                    age_days = (datetime.now() - citation_date).days
                    if age_days > 1:  # Environment citations must be recent
                        result["status"] = "STALE"
                        result["error"] = f"Environment citation {age_days} days old (max 1 day)"
                except ValueError:
                    result["status"] = "INVALID_DATE"
                    result["error"] = "Invalid date format in environment citation"
        
        validation_results.append(result)
    
    # Check for critical failures
    critical_failures = [r for r in validation_results if r["status"] in ["INACCESSIBLE", "STALE", "INVALID_DATE"]]
    
    if critical_failures:
        return {
            "status": "CRITICAL_BLOCK",
            "failures": critical_failures,
            "action": "FIX_INACCESSIBLE_CITATIONS", 
            "message": f"{len(critical_failures)} citations failed accessibility validation",
            "blocking_priority": "ABSOLUTE"
        }
    
    return {"status": "APPROVED", "accessibility": "all_citations_validated"}
```

### Real-Time Validation Service
```markdown
## Citation Validation Workflow

**PRE-RESPONSE VALIDATION**:
1. Parse draft response for citation patterns using format enforcement engine
2. Extract all [Type:reference:metadata] patterns with metadata validation
3. Validate each citation against live sources using accessibility engine
4. Check date freshness and metadata accuracy requirements
5. Generate validation report with pass/fail status for each citation
6. BLOCK response if any citation fails format or accessibility validation
7. Require AI to fix invalid citations before proceeding

**VALIDATION ERROR HANDLING**:
- Invalid Format: Force AI to update citation to include required metadata
- Inaccessible Source: Require AI to find accessible alternative source  
- Stale Citation: Force AI to update with current date after re-verification
- Missing Citation: Block response until citation is provided
- Content Mismatch: Force AI to revise claim to match cited source
```

### Audit Trail Requirements
```markdown
## Citation Audit Framework

**LOGGING REQUIREMENTS**:
- Timestamp of all validation attempts
- Citation format and validation result
- Source accessibility status
- Content correlation assessment
- Response blocking decisions
- AI revision requirements

**AUDIT TRAIL FORMAT**:
{
  "timestamp": "2024-01-15T10:30:00Z",
  "citation": "[JIRA:ACM-22079:Closed:2024-01-15]",
  "validation_result": "PASS",
  "source_status": "accessible",
  "content_match": "verified",
  "action": "approved"
}
```

## ✅ IMPLEMENTATION SUCCESS CRITERIA

### Enforcement Metrics
- **Citation Coverage**: 100% of factual claims in complete reports must include valid citations
- **Validation Success Rate**: 95%+ citation validation success rate
- **Response Blocking**: Zero tolerance for invalid citations in delivered reports
- **Audit Compliance**: Complete validation logs for all citation attempts

### Quality Assurance
- **Source Verification**: All cited sources must be accessible and current
- **Content Correlation**: Claims must semantically match cited sources
- **Format Compliance**: All citations must follow standardized formats
- **Real-Time Validation**: All citations validated against live sources before delivery

This citation enforcement service ensures every complete report delivers only verified, evidence-backed information with complete audit trails for enterprise compliance and quality assurance.