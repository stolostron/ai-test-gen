# Claude Test Generator Framework - Workflow Summary

> **Quick Reference Guide** - For complete details see [framework-workflow-detailed.md](framework-workflow-detailed.md)

## 🎯 What It Does

**AI-Powered Test Analysis Engine** that generates comprehensive E2E test cases for ACM/OCM components in **5-10 minutes** by:

1. **Analyzing JIRA tickets** with 3-level deep investigation
2. **Validating feature deployment** with concrete evidence  
3. **Generating category-aware test cases** with 85-95+ point quality
4. **Providing dual outputs** - analysis + clean test cases

## 🚀 Simple Usage

```bash
# Navigate to framework
cd ai_systems/apps/claude-test-generator

# Ask Claude to analyze any JIRA ticket
"Analyze ACM-22079"                           # Uses default qe6 environment
"Analyze ACM-22079 using qe7 environment"    # Uses specific environment
```

**Result**: Professional test cases ready for manual execution or Polarion import

## 🔄 7-Stage AI Workflow

### Stage 0: 🎯 AI Category Classification (NEW in V2.0)
- **Purpose**: Intelligently classify ticket and select optimal template
- **AI Processing**: Analyzes JIRA content to determine category and confidence
- **Categories**: Upgrade (95+ pts), Security (95+ pts), UI (90+ pts), Import/Export (92+ pts), etc.
- **Output**: Category classification with quality target

### Stage 1: 🌍 Environment Setup & Validation  
- **Purpose**: Establish robust connection with graceful degradation
- **Process**: Uses AI Environment Setup Service internally (NEVER exposed to users)
- **Flexibility**: Works with available environments, continues even if unavailable
- **Output**: Environment status (AVAILABLE/LIMITED/UNAVAILABLE)

### Stage 2: 🔍 Multi-Source Intelligence Gathering ⚠️ **MANDATORY**
- **Purpose**: Comprehensive investigation using AI services
- **Requirements**: **NO SHORTCUTS ALLOWED** - ALL steps must execute
- **Process**: 
  - **JIRA**: 3-level deep hierarchy analysis with ALL nested links
  - **GitHub**: ALL related PRs with implementation details
  - **Internet**: Comprehensive technology and best practices research
  - **Documentation**: ALL documentation links with nested discovery
- **Output**: Complete feature understanding with smart test scoping

### Stage 3: 🔒 AI Feature Deployment Validation ⚠️ **CRITICAL**
- **Purpose**: Validate ALL PR changes are actually deployed and operational
- **Process**: Schema validation + behavioral testing + version correlation + evidence collection
- **Verdict**: FULLY DEPLOYED / PARTIALLY DEPLOYED / NOT DEPLOYED / IMPLEMENTATION BUG
- **Critical**: **NO assumptions** - concrete evidence required
- **Output**: Definitive deployment status with supporting proof

### Stage 4: 🧠 AI Strategic Intelligence
- **Purpose**: Apply sophisticated reasoning for business impact and priorities
- **Process**: Semantic analysis + architectural reasoning + business impact modeling
- **Focus**: High-value, high-risk scenarios based on actual code changes
- **Output**: Strategic test approach with prioritized scenarios

### Stage 5: 📊 Category-Aware Test Generation & AI Validation ⚠️ **REAL-TIME QUALITY**
- **Purpose**: Generate high-quality test cases with real-time AI validation
- **AI Loop**: Pattern learning + quality prediction + iterative refinement
- **Requirements**: 
  - **2-column tables ONLY** (Step | Expected Result)
  - **Verbal instructions FIRST** (never command-only steps)
  - **Zero HTML tags** (25-point deduction)
  - **Generic oc login** commands (NEVER mention AI environment setup)
  - **Sample outputs** with explanations
- **Output**: 85-95+ point quality test cases

### Stage 6: 📋 Dual Output Generation
- **Purpose**: Create both detailed analysis and clean test cases
- **Outputs**:
  - **Complete-Analysis.md**: Full investigation + deployment status + evidence
  - **Test-Cases.md**: Clean, professional test cases with standard OpenShift commands
  - **metadata.json**: Run statistics and quality metrics
- **Policy**: Internal scripts hidden from users, professional format only

### Stage 7: 🧠 Intelligent Learning & Continuous Improvement
- **Purpose**: Framework evolution through AI learning
- **Process**: Pattern recognition + template evolution + quality prediction + adaptive optimization
- **Benefits**: Continuous improvement, better quality prediction, enhanced templates
- **Triggers**: After 3 runs, quality plateau, low scores, production usage

## ⚠️ Critical Enforcement Policies

### 🔒 MANDATORY Requirements - NO EXCEPTIONS
1. **Complete AI Investigation**: Framework **REFUSES** generation without ALL investigation steps
2. **Feature Deployment Validation**: **BLOCKS** generation without thorough feature validation  
3. **AI Validation Loop**: **REQUIRES** real-time AI validation and feedback
4. **Enhanced Format**: **REJECTS** outputs below 85+ point quality targets

### 🚨 Zero Tolerance Failures (Immediate Quality Deduction)
- **HTML Tags**: 25-point deduction for ANY HTML tags (`<br/>`, `<b>`, `<i>`, etc.)
- **Internal AI Services**: 10-point deduction for mentioning internal environment automation
- **Wrong Login Format**: 15-point deduction for incorrect Step 1 format
- **Missing Verbal Instructions**: 20-point deduction for command-only steps
- **Wrong Table Format**: 15-point deduction for 3-column tables

### 🔐 Internal vs External Usage
- **Framework Internal**: Uses AI Environment Setup Service for intelligent operations (hidden from users)
- **Generated Outputs**: ALWAYS show generic `oc login <cluster-url>` commands
- **User Experience**: Professional, standard OpenShift patterns only
- **Security**: No internal framework details exposed to end users

## 📊 Quality Scoring System

### Category-Aware Targets (85-95+ Points)
- **Upgrade/Security**: 95+ points (version validation, rollback procedures)
- **Import/Export**: 92+ points (state validation, error recovery)
- **Resource Management**: 93+ points (performance baselines, stress testing)
- **UI Component**: 90+ points (visual validation, accessibility)  
- **Tech Preview**: 88+ points (feature gates, GA transition)

### Scoring Breakdown
- **Base Score**: 75 points (files exist, format correct, no violations)
- **Category Enhancement**: +10-20 points (category-specific requirements)
- **AI Validation**: Real-time optimization until target achieved

## 🎯 Expected Results

### Performance Metrics
- **⏱️ Time**: 5-10 minutes per analysis
- **📋 Test Cases**: 3-5 comprehensive E2E scenarios
- **🎯 Quality**: 85-95+ points (category-dependent)
- **📝 Coverage**: ALL NEW functionality with realistic validation
- **🔒 Status**: Evidence-based deployment assessment

### Output Quality
- **Professional Format**: Ready for manual execution or Polarion import
- **Complete Coverage**: E2E workflows tailored to ticket category
- **Realistic Examples**: Sample outputs with proper explanations
- **Standard Commands**: Generic OpenShift patterns (no internal scripts)

## 🛠️ Configuration Options

### Environment Selection
- **Default**: `qe6` environment automatic setup
- **Custom**: Specify any QE environment (qe7, qe8, etc.)
- **Override**: Use custom kubeconfig for any cluster

### Framework Customization
- **Test Scoping**: `.claude/prompts/test-scoping-rules.md` - Smart scoping methodology
- **Output Format**: `.claude/templates/` - Test case structure and validation
- **Quality Rules**: `.claude/templates/ai-validation-enhancement.md` - Validation logic
- **Category Templates**: `.claude/templates/category-specific-templates.md` - Category-specific scenarios

## 🔧 Troubleshooting

### Common Issues
- **Environment Problems**: Framework continues with test generation for future execution
- **Low Quality Scores**: AI feedback loop provides specific improvement suggestions
- **Missing Information**: Smart scoping focuses on available data, documents limitations
- **Format Violations**: Real-time AI validation prevents and corrects format issues

### Support Resources
- **Quick Start**: `docs/quick-start.md` - Detailed setup guidance
- **Examples**: `examples/` - Sample outputs and patterns
- **Best Practices**: `.claude/docs/framework-best-practices.md`
- **API Reference**: `.claude/references/` - Command examples

## 🧠 AI Services Integration

### Core AI Services
1. **AI Environment Setup Service**: Intelligent environment discovery, authentication, and cluster connectivity
2. **AI Documentation Service**: JIRA hierarchy and recursive link analysis
3. **AI GitHub Investigation Service**: PR discovery and implementation validation
4. **AI Feature Deployment Validation Service**: Comprehensive feature verification
5. **AI Schema Service**: Dynamic CRD analysis and YAML generation  
6. **AI Validation Service**: Quality assurance and compliance verification
7. **AI Category Classification Service**: Intelligent ticket categorization
8. **AI Learning Service**: Continuous improvement through pattern recognition

### Service Benefits
- **Human-Level Reasoning**: Sophisticated analysis beyond automation
- **Quality Consistency**: 85-95+ point targets with automated validation
- **Continuous Learning**: Framework improves through AI feedback loops
- **Error Prevention**: Real-time validation prevents common issues
- **Efficiency Gains**: 50% reduction in generation time

## 📈 Framework Evolution

### Version History
- **V1.0**: Foundation framework with basic AI investigation
- **V2.0** (Current): Intelligent enhancement with category classification, learning system, enhanced validation

### Performance Progression
- **Baseline**: 60/100 average quality → **Target**: 95+/100 consistent
- **Current**: 85+ points through V2.0 enhancements
- **Efficiency**: 50% faster generation through AI optimization
- **Consistency**: 98% standardization through AI validation

---

## 🚀 Getting Started

1. **Navigate**: `cd ai_systems/apps/claude-test-generator`
2. **Execute**: Ask Claude to "Analyze ACM-XXXXX"
3. **Wait**: 5-10 minutes for complete AI analysis
4. **Review**: Professional test cases in `runs/<TICKET>/latest/Test-Cases.md`
5. **Execute**: Copy-paste test steps for immediate validation

**Result**: Production-ready E2E test cases with evidence-based deployment status and 85-95+ point quality scoring.

---

**Framework Version**: 2.0 (Intelligent Enhancement System)  
**Maintained by**: ACM QE Team  
**Technology**: Claude AI with integrated AI service ecosystem
