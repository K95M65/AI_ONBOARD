# Security consulting workflows

The security library separates discovery, assessment, remediation, and assurance so an agent does not turn
one authorization into a broader test or confuse scanner output with risk.

## Capability loop

```text
map attack surface → threat model → inspect and test → manage vulnerability risk
         ↑                                            ↓
         └──────── monitor change ← assess controls ←─┘
```

| Job | Owning skill | Output |
|---|---|---|
| Establish owned assets, exposure, privilege boundaries, and attack paths | [`map-attack-surface`](../skills/map-attack-surface/) | Evidence-backed asset ledger, coverage gaps, attack paths, monitoring plan |
| Frame threats to important flows and assets | [`threat-model`](../skills/threat-model/) | DFD, STRIDE threats, mitigations, owners |
| Find concrete weaknesses in an application or codebase | [`security-audit`](../skills/security-audit/) | Confirmed, severity-ranked findings |
| Move findings from validation through verified closure | [`manage-vulnerability-risk`](../skills/manage-vulnerability-risk/) | Risk register, treatment decisions, due dates, retest evidence, metrics |
| Judge whether selected controls are designed and operating | [`assess-security-controls`](../skills/assess-security-controls/) | Requirement matrix, evidence, effectiveness judgments, improvement plan |
| Implement bounded fixes and preventive practices | Specialist security skills | Code, configuration, identity, secrets, dependency, and CI improvements |

## Internal and external mapping

`map-attack-surface` owns one job with two progressively loaded views:

- **Internal:** applications, endpoints, networks, cloud, SaaS, identities, CI/CD, data, administrative
  planes, vendors, and recovery systems.
- **External:** owned domains, DNS and certificate records, internet services, public applications,
  repositories, portals, and other publicly discoverable exposure.

Combined work correlates outside-in reachability with internal ownership, privilege, criticality, data, and
dependencies. The map records evidence and confidence; it does not claim that an exposure is a
vulnerability.

## Authorization model

| Level | Default posture |
|---|---|
| Passive | After ownership or authorization is affirmative, inspect supplied material and ordinary public records without probing |
| Authorized read-only | Query named inventories, clouds, directories, logs, or security systems using approved access |
| Authorized active | Require exact targets, rules of engagement, traffic limits, contacts, and stop conditions |
| Intrusive | Outside attack-surface mapping; require a separately governed engagement |

Public visibility is never treated as authorization to consolidate an organization into a security target
map or to perform active testing. Unverified public research routes to the OSINT workflow and stops before
attack-path prioritization. Exploitation, access bypass, credential attacks, persistence, social
engineering, destructive testing, and exfiltration are outside the mapping workflow.

## Framework alignment

The workflows are original, tool-free procedures informed by public guidance:

- [OWASP Attack Surface Analysis](https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html)
  for entry/exit paths, valuable assets, privileges, and surface change;
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) for outcome-oriented governance,
  asset, risk, protection, detection, response, and recovery profiles;
- [CISA BOD 23-01](https://www.cisa.gov/news-events/directives/bod-23-01-improving-asset-visibility-and-vulnerability-detection-federal-networks)
  for the distinction between asset discovery and vulnerability enumeration;
- [CISA Known Exploited Vulnerabilities](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) as
  one current input to vulnerability prioritization;
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) for application
  control requirements;
- [OWASP SAMM](https://owaspsamm.org/model/) for software-assurance program maturity; and
- [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) for technical assessment planning.

The skills require the current official framework to be retrieved and versioned for an assessment. They do
not embed a frozen control catalog, require a paid service, or claim certification.

## Next consulting additions

The highest-value future specialists are:

1. cloud security posture;
2. enterprise identity posture;
3. incident readiness;
4. tabletop exercise facilitation;
5. software supply-chain assurance; and
6. authorized security-test planning.

Each should remain a single repeatable job and compose with the discovery, vulnerability, and control
assessment skills rather than copying their procedures.
