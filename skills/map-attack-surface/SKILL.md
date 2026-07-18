---
name: map-attack-surface
description: Maps an owned or explicitly authorized system's internal, external, or combined attack surface into an evidence-backed asset ledger, reachability model, and prioritized attack paths. Use when inventorying exposed assets, reconciling shadow IT, scoping a security assessment, understanding trust and privilege boundaries beyond one codebase, or establishing a baseline for continuous exposure management. Passive discovery is the default; active probing requires explicit targets and rules of engagement.
---

# Map attack surface

Produce a defensible map of what can be reached, what it connects to, what it protects, and who owns it.
Keep discovery separate from vulnerability testing: this skill establishes coverage and attack paths, then
routes deeper assessment to narrower skills.

## Establish authority and scope

1. Name the organization, system, environments, business objective, time window, and decision owner.
2. Record target inclusions and exclusions using exact identifiers where possible: repositories, accounts,
   tenants, domains, CIDRs, applications, facilities, or business units.
3. Classify the permitted action level before collecting:
   - **Passive:** inspect supplied artifacts and public records without sending probes to a target.
   - **Authorized read-only:** query an approved inventory, cloud, directory, logging, or security system.
   - **Authorized active:** send bounded discovery or validation traffic under written rules of engagement.
4. Read [references/authorization-and-scope.md](references/authorization-and-scope.md). Do not infer that a
   hostname, shared-cloud address, vendor portal, or public record is owned or authorized.
5. If ownership or authorization is ambiguous, do not produce an attack-surface ledger, attack paths, or
   security-target priorities. Ask for authority or route proportionate general public-source research to
   `conduct-open-source-investigation`; do not widen it into security reconnaissance.

## Route adjacent work

- Use `conduct-open-source-investigation` for a substantial public-source evidence investigation.
- Use `threat-model` after the surface exists to apply STRIDE to important flows and boundaries.
- Use `security-audit` to inspect an application or codebase for concrete vulnerabilities.
- Use `manage-vulnerability-risk` when findings need prioritization, ownership, remediation, and retesting.
- Use `assess-security-controls` when the question is whether defined controls are designed and operating.
- Use `vulnerability-hardening`, `identity-management`, `secret-scan`, or `dependency-vuln-scan` for their
  bounded remediation or testing jobs.

Do not repeat those procedures inside the surface map.

## Build the map

### 1. Select the view

- For enterprise, cloud, SaaS, identity, endpoint, network, CI/CD, and administrative surfaces, read
  [references/internal-mapping.md](references/internal-mapping.md).
- For internet-reachable and publicly discoverable assets, read
  [references/external-mapping.md](references/external-mapping.md).
- For a combined assessment, read both and preserve an `internal`, `external`, or `both` marker on each
  record.

### 2. Collect from independent sources

Start with authoritative inventories and configuration, then compare them with observed sources. Record the
source, retrieval time, collection method, and scope for every import or observation. Treat absence from one
source as a coverage question, not proof that an asset does not exist.

Do not make a paid service, API key, account signup, or new scanner installation a prerequisite. Use free,
local, public, or already-authorized capabilities available in the environment.

### 3. Normalize and establish ownership

Use [assets/attack-surface-ledger-template.md](assets/attack-surface-ledger-template.md) when a durable
artifact helps. Deduplicate aliases without erasing source provenance. Assign:

- a stable asset identifier and asset class;
- business and technical owners, or an explicit `unknown`;
- environment and lifecycle state;
- source-backed ownership confidence;
- internal and external reachability;
- identities, privileges, trust zone, and administrative plane;
- data sensitivity, business criticality, and dependencies; and
- last observed date and monitoring source.

Keep ambiguous assets separate until evidence supports a merge.

### 4. Model exposure and attack paths

Draw a compact graph or table from potential actor to entry point, identity or control boundary, dependent
asset, protected data or capability, and plausible outcome. Include unauthenticated access, ordinary users,
privileged users, machine identities, vendors, and insiders where relevant.

Distinguish:

- observed reachability from inferred reachability;
- an exposure from a vulnerability;
- a control presence from verified control effectiveness; and
- a plausible path from a demonstrated path.

### 5. Prioritize and identify coverage gaps

Read [references/analysis-and-monitoring.md](references/analysis-and-monitoring.md). Rank paths using
exposure, privilege, asset criticality, data sensitivity, control strength, and confidence. Do not assign
false numerical precision when evidence is incomplete.

Call out unknown owners, conflicting inventories, unmanaged identities, stale assets, unmonitored zones,
unsupported systems, third-party dependencies, and areas the collection method could not observe.

### 6. Review and report

Use an independent reviewer to challenge ownership, source independence, missing asset classes, and attack
path assumptions when available. Use a verifier to reproduce a sample of high-impact records and confirm
that the report does not imply active validation that did not occur.

Report:

- scope, authority, action level, assumptions, and exclusions;
- source and coverage summary;
- asset ledger and ownership gaps;
- high-priority exposure and attack paths with confidence;
- unknowns and conflicting evidence;
- routed next assessments and remediation owners; and
- a monitoring plan for detecting material surface change.

## Safety rules

- Never exploit, bypass access controls, spray credentials, persist, exfiltrate, socially engineer, or run
  destructive or high-volume tests as part of mapping.
- Never expand from an authorized asset to a related third party without separate authority.
- Minimize personal data and secrets in the ledger; link to protected evidence rather than copying it.
- Stop active work when a target behaves unexpectedly, scope cannot be confirmed, or safety thresholds in
  the rules of engagement are reached.

## Completion standard

The map is complete when a decision-maker can see what was covered, which assets are owned, how important
assets may be reached, where evidence is weak, what requires deeper assessment, and how material change will
be detected.
