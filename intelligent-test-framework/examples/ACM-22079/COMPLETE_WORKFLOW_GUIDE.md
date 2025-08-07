# 🚀 Complete ACM JIRA Analysis & Test Generation Workflow

## **Overview**

This is a **production-ready, single-command framework** that transforms JIRA ticket analysis into comprehensive test implementations for any QE team. Built with Claude Code integration and agentic AI capabilities.

## **✨ Key Features**

- **🎯 Single Command Execution**: `./analyze-jira.sh ACM-22079`
- **🔧 Framework Agnostic**: Supports Cypress, Selenium, Go, Playwright, and more
- **🤖 AI-Powered Analysis**: Claude Code integration at every stage
- **✅ Test Environment Validation**: Real OCP cluster + ACM validation
- **📋 Human Review Gates**: Critical checkpoints for quality assurance
- **🏗️ Production-Ready Code**: Generates deployment-ready test implementations

## **🚀 Quick Start**

### **1. Single Command - Complete Workflow**
```bash
./analyze-jira.sh ACM-22079
```

### **2. Test Plan Only**
```bash
./analyze-jira.sh ACM-22079 --test-plan-only
```

### **3. Custom Team Configuration**
```bash
./analyze-jira.sh ACM-22079 --config=configs/selenium-team-config.yaml
```

### **4. Dry Run (Preview)**
```bash
./analyze-jira.sh ACM-22079 --dry-run --verbose
```

## **📁 Framework Configurations**

### **Cypress (CLC Team) - Default**
```yaml
team:
  name: "CLC QE"
  framework: "cypress"
  repositories:
    automation: "clc-ui"
    automation_path: "/Users/ashafi/Documents/work/automation/clc-ui"
```

### **Selenium (Java Team)**
```bash
./analyze-jira.sh ACM-22079 --config=configs/selenium-team-config.yaml
```

### **Go Unit Testing (Backend Team)**
```bash
./analyze-jira.sh ACM-22079 --config=configs/go-team-config.yaml
```

## **🔄 Workflow Stages**

### **Stage 1: Environment Setup (Automated)**
- ✅ Claude Code environment validation
- ✅ Team configuration loading
- ✅ Required tools verification
- ✅ Project structure initialization

### **Stage 2: Repository Access (Semi-Automated)**
- 📁 QE automation repository access (e.g., clc-ui)
- 📁 Feature development repository cloning
- 📁 ACM ecosystem repository access
- 📁 Documentation and architecture gathering

### **Stage 3: AI-Powered Analysis (Fully Automated)**
- 🔍 JIRA ticket deep dive with linked issues
- 🔍 GitHub PR code analysis
- 🔍 Architecture context and integration points
- 🔍 Customer requirements and business drivers

### **Stage 4: Test Plan Generation (AI + Validation)**
- 🤖 AI generates comprehensive test scenarios
- ✅ **Smart Validation**: Environment-aware test validation
- ✅ **OCP Command Integration**: Proper `oc get`, `oc describe` usage
- ✅ **ACM Resource Validation**: ClusterCurator, ManagedCluster testing

### **Stage 5: Human Review Gate**
- 👥 Test plan presented for approval
- 📝 Interactive review and modification
- ✅ Approval gate before implementation
- 🔄 Iteration support for improvements

### **Stage 6: Test Implementation (Framework-Specific)**
- ⚙️ Production-ready code generation
- 🎯 Framework-specific best practices
- 🧪 Integration with existing test patterns
- 📚 Complete supporting files and utilities

### **Stage 7: Quality Validation (Automated + Human)**
- ✅ Code quality validation
- 🧪 Test environment connectivity checks
- 📊 Coverage analysis and reporting
- 📝 Integration instructions

## **🔧 Test Environment Integration**

### **OCP Cluster + ACM Validation**
The framework validates your test environment:

```yaml
test_environment:
  cluster_config_path: "/path/to/kubeconfig"
  acm_namespace: "open-cluster-management"
  validation_commands:
    - "oc get pods -n open-cluster-management"
    - "oc get clustercurator"
    - "oc get managedclusters"
```

### **Environment-Aware Test Generation**
Generated tests include proper validation commands:

```javascript
// Cypress example
cy.exec('oc get clustercurator test-curator -n test-namespace')
  .then((result) => {
    expect(result.code).to.eq(0)
    expect(result.stdout).to.contain('Completed')
  })
```

```java
// Selenium example with OCP validation
@Test
public void validateClusterCuratorStatus() {
    String command = "oc get clustercurator " + clusterName + " -o jsonpath='{.status.conditions[0].status}'";
    String result = executeOcCommand(command);
    assertEquals("True", result);
}
```

## **🎯 Smart Test Plan Validation**

### **Environment-Aware Validation**
The framework intelligently validates test plans:

- **Resource Existence Checks**: Validates `oc get` commands are appropriate
- **API Validation**: Ensures proper Kubernetes API usage
- **ACM Integration**: Validates hub-spoke cluster scenarios
- **Framework Optimization**: Generates framework-specific best practices

### **Example Validation Points**
```bash
# Resource validation
oc get clustercurator <name> -n <namespace>
oc describe managedcluster <cluster-name>

# Status validation  
oc get managedcluster <name> -o jsonpath='{.status.conditions[?(@.type=="ManagedClusterConditionAvailable")].status}'

# Log validation
oc logs <pod-name> -n open-cluster-management
```

## **📋 Generated Deliverables**

### **Complete Project Structure**
```
ACM-22079/
├── 01-analysis/                    # Comprehensive feature analysis
├── 02-test-planning/              # Validated test plans
├── 03-implementation/             # Production-ready test code
├── 04-quality/                    # Quality validation reports
├── 05-documentation/              # Team handoff materials
├── configs/                       # Framework configurations
├── workflow-state.json            # Real-time progress tracking
└── WORKFLOW_SUMMARY_*.md          # Complete execution summary
```

### **Framework-Specific Code**

**Cypress Implementation:**
- Complete `.spec.js` test files
- Page object models in `cypress/views/`
- Custom commands in `cypress/support/`
- Test fixtures and data

**Selenium Implementation:**
- Test class files with proper annotations
- Page object model classes
- Utility and helper classes
- Maven/Gradle integration

**Go Implementation:**
- Table-driven test functions
- Interface mocking
- Test helper functions
- Integration test suites

## **🔗 Repository Integration**

### **Multi-Repository Access**
The framework accesses multiple repositories:

1. **QE Automation Repo**: Your team's test automation (e.g., clc-ui)
2. **Feature Development Repo**: Where the feature is implemented
3. **ACM Ecosystem Repos**: Related ACM components and APIs
4. **Documentation Repos**: Architecture and design documentation

### **Local Repository Setup**
```bash
# Automated repository cloning and access
./01-setup/enable-github-pr-access.sh
./01-setup/comprehensive-research-setup.sh
```

## **🎨 Team Customization**

### **Creating Team-Specific Configurations**

1. **Copy existing configuration:**
```bash
cp team-config.yaml configs/myteam-config.yaml
```

2. **Customize for your framework:**
```yaml
team:
  name: "My QE Team"
  framework: "playwright"  # or selenium, go, etc.
  repositories:
    automation: "my-automation-repo"
    automation_path: "/path/to/my/repo"
```

3. **Use your configuration:**
```bash
./analyze-jira.sh ACM-22079 --config=configs/myteam-config.yaml
```

## **📊 Success Metrics**

### **Automation Goals**
- ✅ **95%+ Automated**: Minimal human intervention
- ✅ **Framework Agnostic**: Works with any testing framework
- ✅ **Production Quality**: Generates deployment-ready code
- ✅ **Environment Aware**: Validates real test environments

### **Quality Standards**
- ✅ **Comprehensive Coverage**: All feature aspects tested
- ✅ **Smart Validation**: Environment-aware test validation
- ✅ **Integration Ready**: Seamless integration with existing suites
- ✅ **Maintainable**: Clean, documented, reusable code

## **🔄 Advanced Usage**

### **Continuous Integration**
```bash
# CI/CD pipeline integration
./analyze-jira.sh ACM-22079 --test-plan-only --verbose > test-plan.log
```

### **Batch Processing**
```bash
# Process multiple tickets
for ticket in ACM-22079 ACM-22080 ACM-22081; do
  ./analyze-jira.sh $ticket --test-plan-only
done
```

### **Team Collaboration**
```bash
# Generate test plan for team review
./analyze-jira.sh ACM-22079 --test-plan-only
# Team reviews 02-test-planning/test-plan.md
# Generate implementation after approval
./analyze-jira.sh ACM-22079
```

## **🛠️ Troubleshooting**

### **Common Issues**

**Claude Code Connectivity:**
```bash
# Test Claude Code
claude --print "Test connection"
```

**Environment Variables:**
```bash
# Check required environment variables
echo $ANTHROPIC_VERTEX_PROJECT_ID
echo $CLAUDE_CODE_USE_VERTEX
```

**Repository Access:**
```bash
# Verify repository cloning
ls -la 06-reference/comprehensive-research/
```

**Test Environment:**
```bash
# Validate OCP access
oc cluster-info
oc get pods -n open-cluster-management
```

## **🔮 Future Enhancements**

### **Phase 1 (Complete)** ✅
- Single-script orchestrator
- Framework-agnostic architecture
- Test plan validation
- Human review gates

### **Phase 2 (Upcoming)**
- Direct GitHub integration (when Claude Code gains access)
- Multi-framework parallel generation
- Advanced CI/CD integration
- Team collaboration features

### **Phase 3 (Future)**
- Real-time test execution and validation
- Automated test maintenance
- Cross-team test sharing
- Enterprise governance features

## **📞 Support and Extensions**

### **Adding New Frameworks**
1. Create framework configuration in `configs/`
2. Add framework-specific prompts in `02-analysis/prompts/`
3. Update team configuration with framework details
4. Test with `--dry-run` mode

### **Custom Validation Commands**
```yaml
test_environment:
  validation_commands:
    - "oc get myresource"
    - "kubectl describe pod mypod"
    - "curl -k https://my-api/health"
```

This framework transforms JIRA analysis from a manual, time-consuming process into an **automated, intelligent, and production-ready workflow** that adapts to any QE team's needs while maintaining the highest quality standards.