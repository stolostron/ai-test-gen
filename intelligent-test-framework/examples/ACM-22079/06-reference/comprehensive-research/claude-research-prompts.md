# Comprehensive Research Prompts for Claude Code

## Phase 1: Linked Documentation Analysis
```
Please analyze all documentation in 06-reference/comprehensive-research/linked-docs/ 
and identify:
1. Related JIRA tickets that should be researched
2. Design documents that provide context for ACM-22079
3. Customer requirements that drive this feature
4. Technical specifications that define the implementation

Focus on understanding the broader context beyond just the PR implementation.
```

## Phase 2: ClusterCurator Deep Architecture Analysis
```
@file:06-reference/comprehensive-research/clustercurator-docs/
@file:06-reference/pr-files/ACM-22079-PR-468/hive.go

Based on the ClusterCurator documentation and implementation:
1. Explain the complete upgrade workflow and where digest support fits
2. Identify all integration points that need testing
3. Analyze potential failure modes and edge cases
4. Recommend comprehensive test coverage strategy
```

## Phase 3: ACM Ecosystem Integration Analysis
```
@file:06-reference/comprehensive-research/acm-docs/
@file:06-reference/comprehensive-research/architecture-docs/

Analyze how ACM-22079 fits into the broader ACM ecosystem:
1. Impact on other ACM components
2. Integration with ManagedClusterView/Action patterns
3. Hub-spoke communication implications
4. Multi-cluster upgrade orchestration considerations
```

## Phase 4: Test Pattern Evolution
```
@file:06-reference/comprehensive-research/test-patterns/
@file:06-reference/pr-files/ACM-22079-PR-468/hive_test.go

Based on existing ACM test patterns and the new implementation:
1. Identify test framework patterns to follow
2. Recommend test data structures and mocking strategies
3. Suggest integration test scenarios
4. Propose E2E test workflows that align with existing patterns
```

## Phase 5: Comprehensive Test Generation
```
Based on ALL research gathered in 06-reference/comprehensive-research/:
1. Generate test cases that address the complete feature scope
2. Include tests for all identified integration points
3. Cover edge cases found in related documentation
4. Align with existing ACM test automation patterns
5. Address customer requirements and use cases
```
