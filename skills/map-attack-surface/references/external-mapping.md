# External attack-surface mapping

Build an outside-in view only after affirmative ownership or explicit authorization has been established.
Do not treat public discoverability as authority to create a consolidated target map or send probes.

## Passive sources

Use only sources relevant to the declared target:

- Organizational records, official websites, acquisitions, brands, and published applications
- Domain registrations and RDAP, DNS records, nameservers, mail records, and delegated zones
- Public certificate transparency records and certificate metadata
- Published IP ranges, autonomous-system information, and cloud-hosting indicators
- Public websites, APIs, status pages, documentation, authentication portals, and administrative entry
  points
- Mobile and desktop application listings, update endpoints, deep links, and declared backends
- Public source repositories, package registries, container registries, release artifacts, and documentation
- Security contact, vulnerability-disclosure, and `security.txt` records
- Public job descriptions, architecture talks, incident reports, and vendor documentation when they reveal
  system relationships without unnecessary personal data

Follow the evidence and entity-resolution rules in `conduct-open-source-investigation` for substantial
public-source research.

## Ownership confidence

Classify each candidate:

- **Confirmed:** authoritative inventory, configuration, registration, or owner confirmation.
- **Strong:** multiple independent attributes tie it to the organization.
- **Possible:** a plausible relationship with incomplete or shared evidence.
- **Rejected:** evidence shows third-party or unrelated ownership.

Do not actively validate `possible` candidates. Shared IP space, CDN edges, vendor-branded portals, and
lookalike domains require special care.

## Exposure to capture

- Protocol or application entry point and observed public route
- Authentication requirement, user class, and administrative capability
- Environment and apparent lifecycle state
- Downstream dependency and protected business capability
- Publicly disclosed version or technology only when directly evidenced
- Security headers, certificate state, or service behavior only when observation is permitted
- Owner, monitoring source, last observation, and change history

## Active validation

Active enumeration is optional, never implied, and requires the authorized-active scope record. Use the
approved source, rate, schedule, protocol, credentials, and stop conditions. Collect the minimum evidence
needed to confirm reachability or service identity.

Do not exploit, bypass authentication, enumerate accounts, submit harmful payloads, access non-public data,
or pivot to related infrastructure. A discovered weakness becomes an assessment target, not permission to
demonstrate impact.
