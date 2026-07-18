# Internal attack-surface mapping

Map the enterprise as assets, identities, control planes, data, and reachable relationships—not only IP
addresses.

## Source hierarchy

Prefer and reconcile:

1. Architecture, network, data-flow, and identity diagrams.
2. Infrastructure as code, deployment manifests, repositories, and CI/CD configuration.
3. Cloud organizations/accounts/projects/subscriptions and resource inventories.
4. CMDB, endpoint management, directory, SaaS, certificate, DNS, DHCP, and IPAM inventories.
5. Flow, proxy, authentication, EDR, vulnerability, and asset-discovery telemetry.
6. Owner interviews and manually maintained lists.

No single source is authoritative for every asset class. Preserve source disagreements.

## Asset classes

- Applications, services, APIs, message consumers, scheduled jobs, and data pipelines
- Servers, endpoints, mobile devices, network devices, appliances, containers, clusters, and serverless
  workloads
- Cloud organizations, accounts, projects, subscriptions, virtual networks, storage, databases, secrets,
  keys, registries, and management services
- SaaS tenants, integrations, OAuth grants, service principals, bots, and automation accounts
- Workforce, privileged, emergency, vendor, service, workload, and unmanaged identities
- Source repositories, build runners, package registries, artifact stores, deployment systems, and signing
  services
- Administrative consoles, remote-access paths, observability, security tools, backup, and recovery systems
- Data stores, sensitive datasets, encryption boundaries, exports, replicas, and retention systems
- Vendor connections, managed services, support channels, acquisitions, and shared dependencies

## Relationships to capture

- Network or application reachability and direction
- Authentication mechanism and authorization boundary
- Privileged control, impersonation, delegation, and credential storage
- Data read/write/admin capability and data sensitivity
- Deployment, update, signing, backup, and recovery authority
- Logging and monitoring coverage
- Business ownership, criticality, lifecycle, and support status

## Common blind spots

Look deliberately for ephemeral workloads, roaming devices, dormant identities, shadow SaaS, orphaned cloud
accounts, old acquisitions, bypass networks, build infrastructure, break-glass access, vendor support
channels, unmanaged certificates, test environments with production data, and security tools whose control
planes create privileged paths.
