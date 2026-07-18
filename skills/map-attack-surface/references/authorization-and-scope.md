# Authorization and scope

Attack-surface discovery is useful only when its authority and coverage are explicit.

## Action levels

| Level | Examples | Required basis |
|---|---|---|
| Passive | Supplied repositories, architecture, exports, public DNS, certificate records, RDAP, public websites and documentation | Affirmative ownership or explicit authorization for the mapped organization or system |
| Authorized read-only | Cloud-resource listing, CMDB, directory, SaaS admin inventory, flow logs, DNS logs, scanner-result import | User-provided access to the named organization or system |
| Authorized active | Port discovery, service identification, authenticated enumeration, application crawling, vulnerability scanning | Exact targets, written authorization, time window, source systems, traffic limits, contacts, stop conditions |
| Intrusive | Exploitation, credential attacks, access bypass, persistence, phishing, destructive or availability testing | Outside this skill; use a separately governed engagement |

Public visibility is not authorization to create a security target map or perform active testing. A parent
domain does not automatically authorize subsidiaries, vendors, customer tenants, shared hosting, acquired
brands, or cloud-provider infrastructure. Route ordinary unverified organization or domain research to
`conduct-open-source-investigation` and stop before attack-path or security-target prioritization.

## Scope record

Capture:

- organization and decision owner;
- legitimate purpose and intended decisions;
- exact included and excluded identifiers;
- environments and time window;
- permitted collection sources and action level;
- credentials or roles approved for read-only access;
- active-test source addresses and traffic limits, when applicable;
- safety contact, stop conditions, and evidence-handling requirements;
- regulated, safety-critical, operational-technology, or third-party constraints; and
- expected deliverables and retention period.

## Safe defaults

- Prefer passive or supplied evidence until a broader level is explicit.
- Use the least privileged read-only role that provides the required inventory.
- Validate ownership before sending traffic.
- Separate discovery evidence from vulnerability claims.
- Record inaccessible sources and blind spots instead of bypassing them.
- Stop active work on signs of instability, unintended third-party scope, sensitive data exposure, or
  conflicting instructions.
