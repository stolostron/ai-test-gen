# Related Tickets Research Strategy

## JIRA Search Queries for Claude Code to Reference

### Core Feature Related
```
project = ACM AND (
    text ~ "digest" OR 
    text ~ "disconnected" OR 
    text ~ "air-gapped" OR
    text ~ "ClusterCurator" OR
    text ~ "non-recommended"
) AND status != Closed
```

### Customer Related
```
project = ACM AND (
    text ~ "Amadeus" OR
    text ~ "enterprise" OR
    text ~ "upgrade"
) AND priority in (High, Critical)
```

### Component Related  
```
project = ACM AND component = "Cluster Lifecycle" AND (
    text ~ "upgrade" OR
    text ~ "version" OR
    text ~ "image"
)
```

### Recent Related Work
```
project = ACM AND created >= -6M AND (
    text ~ "ClusterCurator" OR
    text ~ "cluster upgrade"
) ORDER BY created DESC
```

## GitHub Issues to Research

### stolostron/cluster-curator-controller
- Issues related to upgrades
- Disconnected environment issues
- Customer escalations
- Enhancement requests

### Related Components
- stolostron/api issues
- stolostron/cluster-lifecycle-api issues
- OpenShift cluster-version-operator issues

## Search Terms for Broader Research
- "digest based upgrade"
- "disconnected cluster upgrade"
- "ClusterCurator enhancement"
- "ManagedClusterView upgrade"
- "force upgrade annotation"
- "non recommended OpenShift upgrade"
- "air gapped cluster management"
