# ACM Codebase Reference Links

## Main ACM Automation Codebase
**Base Path**: `/Users/ashafi/Documents/work/automation`

## Key Components for ACM-22079 Testing

### ClusterCurator Related Components
```
automation/
├── clc-ui/                           # Cluster Lifecycle UI tests
│   ├── cypress/                      # E2E test framework
│   ├── cypress.config.js            # Cypress configuration
│   └── create_cluster_artifact.py   # Cluster creation utilities
├── clc-non-ui/                       # Cluster Lifecycle non-UI tests
│   └── acmqe-clc-test/              # Go-based test suite
└── clc_cicd/                        # CI/CD automation
    └── automation/                   # Automation scripts and configs
```

### Related ACM Components
```
automation/
├── alc-ui/                          # Application Lifecycle tests
├── grc-ui/                          # Governance, Risk, Compliance tests
├── console_dev/                     # Console development and testing
│   └── console/                     # Console-specific automation
└── misc/                            # Utility scripts and tools
```

## Relevant Files for ClusterCurator Testing

### Cypress Test Framework (clc-ui)
- **Main Tests**: `clc-ui/cypress/integration/`
- **Test Utilities**: `clc-ui/cypress/support/`
- **Test Data**: `clc-ui/cypress/fixtures/`
- **API Helpers**: `clc-ui/cypress/apis/`
- **Configuration**: `clc-ui/cypress/config/`

### Go Test Framework (clc-non-ui)
- **Test Implementation**: `clc-non-ui/acmqe-clc-test/pkg/`
- **Go Modules**: `clc-non-ui/acmqe-clc-test/go.mod`
- **Dockerfile**: `clc-non-ui/acmqe-clc-test/Dockerfile.interop`

### CI/CD Integration
- **Jenkins Configs**: `clc_cicd/ci/jenkinsfiles/`
- **Automation Scripts**: `clc_cicd/automation/`
- **Container Images**: `clc_cicd/ci/containerimages/`

## Test Integration Points

### For ClusterCurator Digest Testing
1. **UI Testing**: Integrate with `clc-ui/cypress/` framework
2. **API Testing**: Use patterns from `clc-ui/cypress/apis/`
3. **Non-UI Testing**: Extend `clc-non-ui/acmqe-clc-test/`
4. **CI/CD**: Update `clc_cicd/ci/jenkinsfiles/`

### Existing Test Patterns to Follow
- **Cluster Creation**: `clc-ui/create_cluster_artifact.py`
- **E2E Workflows**: `clc-ui/cypress/integration/`
- **Test Configuration**: `clc-ui/cypress/config/`
- **Resource Management**: `clc-ui/resources/`

## ACM-22079 Specific Integration

### Where to Add Digest-Based Upgrade Tests

#### 1. Cypress E2E Tests (clc-ui)
```
clc-ui/cypress/integration/
├── cluster-creation/
├── cluster-upgrades/                 # Add ACM-22079 tests here
│   ├── digest-based-upgrades.spec.js # New test file
│   ├── force-upgrade-annotation.spec.js
│   └── disconnected-upgrades.spec.js
└── cluster-management/
```

#### 2. Go Integration Tests (clc-non-ui)
```
clc-non-ui/acmqe-clc-test/pkg/
├── clustercurator/                   # Add ACM-22079 tests here
│   ├── digest_upgrade_test.go        # New test file
│   ├── force_annotation_test.go
│   └── disconnected_env_test.go
└── utils/
```

#### 3. Test Data and Fixtures
```
clc-ui/cypress/fixtures/
├── clustercurator/
│   ├── digest-upgrade-configs.yaml   # New test data
│   ├── force-annotation-examples.yaml
│   └── disconnected-scenarios.yaml
```

### Jenkins Pipeline Integration
```
clc_cicd/ci/jenkinsfiles/
├── clustercurator/
│   └── digest-upgrade-pipeline        # New pipeline
```

## External Repository References

### ClusterCurator Controller
- **Repository**: `stolostron/cluster-curator-controller`
- **PR Reference**: `#468 - ACM-22079 Initial non-recommended image digest feature`
- **Key Files**:
  - `cmd/curator/curator.go`
  - `pkg/jobs/hive/hive.go`
  - `pkg/jobs/hive/hive_test.go`
  - `pkg/jobs/utils/helpers.go`

### Related ACM Repositories
- **ACM API**: `stolostron/api`
- **ACM Operator**: `stolostron/multicluster-operator-subscription`
- **Hub Cluster**: `stolostron/registration-operator`
- **Managed Cluster**: `stolostron/klusterlet`

## Documentation Links

### ACM Documentation
- **Official Docs**: Red Hat ACM Documentation Portal
- **Developer Docs**: `stolostron/` GitHub organization
- **API Reference**: ACM API documentation

### ClusterCurator Specific
- **Architecture**: ClusterCurator design documents
- **Upgrade Workflows**: Existing upgrade process documentation
- **Disconnected Environments**: Air-gapped deployment guides

## Test Environment References

### Development Environments
- **Local Testing**: Development cluster configurations
- **Staging**: Pre-production test environments  
- **Integration**: Multi-cluster test setups

### Disconnected Environment Setup
- **Mirror Registries**: Configuration examples
- **Air-Gapped Networks**: Network isolation setups
- **Certificate Management**: TLS configuration for disconnected

## Utility Scripts and Tools

### Existing Utilities (automation/misc)
- **Cluster Management**: `automation/misc/tools/`
- **Resource Cleanup**: `automation/misc/cleanup_all_vms_and_storage.sh`
- **Network Tools**: `automation/misc/tcp_proxy/`

### For ACM-22079 Testing
- **Digest Generation**: Create scripts for test digest generation
- **Environment Setup**: Disconnected environment automation
- **Test Data Creation**: ClusterCurator configuration generators

## Integration Strategy

### Phase 1: Extend Existing Tests
1. Add digest-based scenarios to existing ClusterCurator tests
2. Enhance current upgrade test cases
3. Update test data with digest examples

### Phase 2: New Test Suites
1. Create dedicated digest-upgrade test files
2. Implement disconnected environment simulations
3. Add force annotation testing

### Phase 3: CI/CD Integration
1. Update Jenkins pipelines
2. Add automated test execution
3. Integrate with existing reporting

This reference provides the foundation for implementing ACM-22079 test cases within the existing ACM automation framework.