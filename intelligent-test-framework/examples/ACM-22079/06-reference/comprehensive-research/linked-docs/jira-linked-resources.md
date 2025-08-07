# JIRA ACM-22079 Linked Resources

## Direct Links from JIRA Ticket
Based on typical JIRA ticket structure, these resources are commonly linked:

### Related JIRA Tickets
- **Parent Epic**: Look for epic link in ACM-22079
- **Related Stories**: Search for "digest", "upgrade", "disconnected" in ACM project
- **Dependency Tickets**: ClusterCurator enhancement tickets
- **Customer Escalations**: Amadeus-related tickets

### Design Documents
- ClusterCurator upgrade workflow design
- Disconnected environment deployment guides
- Image digest vs tag comparison documentation
- Non-recommended upgrade path policies

### Technical Specifications
- OpenShift ClusterVersion API documentation
- ACM ManagedClusterView specifications  
- ManagedClusterAction API reference
- Force upgrade annotation specifications

### Customer Requirements
- Amadeus use case documentation
- Disconnected environment requirements
- Air-gapped deployment constraints
- Enterprise upgrade scenarios

## Searches to Perform in JIRA
1. `project = ACM AND text ~ "digest" AND text ~ "upgrade"`
2. `project = ACM AND text ~ "disconnected" AND text ~ "ClusterCurator"`
3. `project = ACM AND text ~ "Amadeus" AND priority = High`
4. `project = ACM AND component = "Cluster Lifecycle"`
5. `fixVersion in (2.8.0, 2.9.0) AND text ~ "upgrade"`

## Related PRs to Investigate
- Previous ClusterCurator enhancement PRs
- Disconnected environment fixes
- ManagedClusterView improvements
- Image digest support implementations

## Documentation Repositories
- stolostron/enhancements (Design proposals)
- stolostron/cluster-curator-controller (Technical docs)
- stolostron/backlog (Requirements and planning)
- openshift/api (ClusterVersion API specs)
