# JIRA Ticket: ACM-22079

## Summary
Implement ClusterCurator digest upgrades for cluster lifecycle management

## Description
This feature enables cluster administrators to upgrade OpenShift clusters using digest-based image references instead of version tags, providing more precise control over cluster upgrades.

## Acceptance Criteria
- Create cluster upgrade workflow using digest references
- Validate upgrade process with different cluster configurations
- Ensure proper error handling and rollback capabilities
- Test with various cluster types (SNO, multi-node, hosted)

## Components Involved
- Cluster lifecycle management
- ClusterCurator controller
- Upgrade workflows
- Image digest validation
