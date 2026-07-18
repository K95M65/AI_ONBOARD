# Analysis and monitoring

Turn the ledger into decisions without confusing incomplete discovery with measured risk.

## Attack-path record

For each material path, capture:

1. actor or starting condition;
2. externally or internally reachable entry point;
3. identity, privilege, or trust-boundary transition;
4. dependent assets and security controls;
5. protected data or business capability;
6. plausible outcome;
7. direct evidence and inference;
8. confidence and unresolved assumptions; and
9. next validation or remediation owner.

Use `threat-model` for STRIDE analysis of important paths. Map to current MITRE ATT&CK techniques only when a
threat-informed defense decision needs that vocabulary; ATT&CK labels do not prove feasibility.

## Relative priority

Prefer a transparent qualitative judgment over an arbitrary score:

- **Exposure:** internet, partner, workforce, restricted segment, local only
- **Privilege:** unauthenticated, ordinary, elevated, administrative, control plane
- **Consequence:** critical service, sensitive data, financial or safety impact, recovery authority
- **Control strength:** verified, present but untested, weak, absent, unknown
- **Path confidence:** observed, strongly supported, plausible, speculative

Prioritize observed paths to critical assets with weak or unverified boundaries. Keep low-confidence,
high-consequence paths visible as validation priorities rather than declaring them vulnerabilities.

## Coverage measures

Track:

- assets by source, class, environment, owner, and lifecycle;
- percentage with confirmed ownership and monitoring;
- unknown-owner and conflicting-source counts;
- externally reachable and privileged-control-plane counts;
- stale observations and unsupported assets;
- high-priority paths awaiting validation or remediation; and
- discovery cadence and source freshness.

These measures describe map quality and exposure. They are not a security score.

## Change monitoring

Define how each important asset class will be rediscovered. Compare snapshots for new, removed, ownership-
changed, newly public, newly privileged, or unmonitored assets. Route material changes back through attack-
path analysis, threat modeling, and the appropriate assessment skill.
