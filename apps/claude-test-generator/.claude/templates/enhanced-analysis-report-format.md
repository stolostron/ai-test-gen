# Enhanced Complete Analysis Report Format Requirements

## 🚨 MANDATORY CITATION ENFORCEMENT

**CRITICAL REQUIREMENT**: All factual claims in complete reports MUST include verified citations using standardized formats:
- **JIRA**: [JIRA:ACM-XXXXX:status:last_updated]
- **GitHub**: [GitHub:org/repo#PR/issue:state:commit_sha]  
- **Documentation**: [Docs:URL#section:last_verified]
- **Code**: [Code:file_path:lines:commit_sha]

**SCOPE**: Complete reports only - test summary tables maintain clean format without citations

## 🚨 MANDATORY STRUCTURE ENFORCEMENT

All Complete-Analysis.md files MUST follow this exact 5-section structure. Reports deviating from this format will be REJECTED.

### Section 1: 🚨 DEPLOYMENT STATUS (FIRST SECTION - MANDATORY)

**Purpose**: Provide definitive deployment assessment with concrete evidence

**Required Elements**:
- **Environment Specification**: MUST clearly state which environment was used for validation [Env:cluster_url:connectivity:timestamp]
  - Examples: "qe6 cluster (OpenShift 4.16.37, ACM 2.13.2) [Env:https://api.qe6.example.com:200:2024-01-15T10:30:00Z]", "local test environment", "simulated AI analysis due to cluster unavailability"
- **Feature Status Assessment**: MUST provide one of four definitive statuses with citations:
  - ✅ **FULLY OPERATIONAL**: Feature deployed and working with concrete validation data [JIRA:ACM-XXXXX:status:last_updated] [Docs:URL#section:last_verified]
  - 🔄 **PARTIALLY OPERATIONAL**: Specific components working/missing with detailed breakdown [Code:file_path:lines:commit_sha]  
  - ❌ **NOT DEPLOYED**: Feature unavailable with concrete evidence and timeline [GitHub:org/repo#PR:state:commit_sha]
  - 🐛 **IMPLEMENTATION BUG**: Feature deployed but malfunctioning with error analysis [JIRA:ticket_id:status:last_updated]
- **Supporting Evidence**: MUST provide concrete data collected during validation with citations:
  - Version checks and correlation results [Env:cluster_url:connectivity:timestamp]
  - Behavioral testing outcomes [Code:test_file_path:lines:commit_sha]
  - Schema validation results [Docs:URL#schema-section:last_verified]
  - Error logs or success confirmations [Code:log_file_path:lines:commit_sha]
- **Version Correlation**: MUST correlate ACM/MCE versions with feature availability and deployment timeline [JIRA:ACM-XXXXX:status:last_updated] [Docs:URL#version-matrix:last_verified]

**Format Example**:
```markdown
## 🚨 DEPLOYMENT STATUS

**Environment**: qe6 cluster (OpenShift 4.16.37, ACM 2.13.2) [Env:https://api.qe6.example.com:200:2024-01-15T10:30:00Z]
**Status**: ❌ NOT DEPLOYED [JIRA:ACM-22079:Open:2024-01-15]
**Evidence**: Feature API endpoint not accessible, version mismatch detected [Code:pkg/api/routes.go:45-52:a1b2c3d4]
**Version Correlation**: Target version 2.14 not yet available in cluster running 2.13.2 [Docs:https://access.redhat.com/documentation/acm#version-matrix:2024-01-15]
```

### Section 2: Implementation Status (SECOND SECTION - MANDATORY)

**Purpose**: Detailed investigation of actual implementation work and PRs

**Required Elements**:
- **PR Investigation Results**: MANDATORY detailed analysis including:
  - **When PRs Found**: 
    - PR status (open/closed/merged)
    - Creation and merge dates
    - Author and repository information
    - Review and approval timeline
    - Link to actual PR
  - **When No PRs Found**: 
    - Explicitly state "No related PRs found after comprehensive search"
    - List search criteria and repositories checked
    - Explanation of why PRs might not be found (feature not yet implemented, different naming, etc.)
- **Code Change Analysis**: When PRs are found, provide:
  - Specific code modifications
  - New functions or classes added
  - Modified configuration files
  - Integration points changed
- **Implementation Timeline**: 
  - Development start/completion dates
  - Target release cycle information
  - Current development phase

**Format Example**:
```markdown
## Implementation Status

**PR Investigation Results**: 
- **PR Found**: stolostron/cluster-curator-controller#123 (Merged: 2025-07-15, Author: developer-name)
- **Code Changes**: [Detailed analysis of actual code]
- **Implementation Timeline**: [Development timeline with dates]

OR

**PR Investigation Results**:
- **No related PRs found** after comprehensive search of stolostron repositories
- **Search Criteria**: "ACM-22079", "digest upgrade", "non-recommended", "ClusterCurator"
- **Explanation**: Feature appears to be in early planning phase, implementation PRs not yet created
```

### Section 3: Feature Details (THIRD SECTION - MANDATORY)

**Purpose**: Technical deep-dive into the feature using actual implementation details

**Required Elements**:
- **Technical Implementation**: Detailed explanation using actual code from PRs (when available)
- **Code Analysis**: Specific code changes, functions, logic modifications
- **Integration Points**: How feature integrates with existing systems
- **Architecture Impact**: Structural changes and system modifications  
- **Configuration Requirements**: New annotations, parameters, setup requirements

**Format Example**:
```markdown
## Feature Details

**Technical Implementation**: 
[Detailed explanation with actual code snippets from PRs]

**Code Analysis**:
[Specific analysis of implementation details]

**Integration Points**:
[How feature connects with existing components]

**Configuration Requirements**:
[New settings, annotations, or parameters needed]
```

### Section 4: Business Impact (FOURTH SECTION - MANDATORY)

**Purpose**: Business justification and customer value analysis

**Required Elements**:
- **Customer Value**: Clear business benefits and justification
- **Use Cases**: Primary and secondary scenarios where feature adds value
- **Problem Resolution**: Specific customer problems this feature solves
- **Market Impact**: Competitive advantages and strategic positioning

**Format Example**:
```markdown
## Business Impact

**Customer Value**: 
[Clear business benefits]

**Use Cases**:
- Primary: [Main use case scenario]
- Secondary: [Additional scenarios]

**Problem Resolution**:
[Customer problems solved]

**Market Impact**:
[Competitive and strategic benefits]
```

### Section 5: Relevant Links (FINAL SECTION - MANDATORY)

**Purpose**: Comprehensive reference collection for future investigation

**Required Elements**:
- **Documentation Links**: Official docs, user guides, technical specifications
- **JIRA References**: All related tickets with hierarchical relationships
- **PR References**: All implementation PRs with direct links (when found)
- **External Resources**: Community discussions, technical resources, related documentation

**Format Example**:
```markdown
## Relevant Links

**Documentation Links**:
- [Official Red Hat ACM Documentation](URL)
- [Technical Specifications](URL)

**JIRA References**:
- ACM-22079: [Main story](URL)
- ACM-22080: [QE validation](URL)
- ACM-22081: [QE automation](URL)
- ACM-22457: [Documentation](URL)

**PR References**:
- stolostron/cluster-curator-controller#123: [Implementation PR](URL)

**External Resources**:
- [OpenShift Conditional Updates Documentation](URL)
- [Community Discussion](URL)
```

## 🚨 VALIDATION REQUIREMENTS

**All sections are MANDATORY** - no exceptions allowed.

**Evidence Requirements**:
- All claims must be supported with concrete evidence
- All investigation results must be documented with specific details
- All status assessments must include supporting data

**Quality Standards**:
- Information must be factual and verifiable
- Analysis must be comprehensive and detailed
- Format must be professional and consistent

**Enforcement**:
- Reports not following this structure will be REJECTED
- Missing sections will trigger framework BLOCKING
- Insufficient evidence will cause validation FAILURE