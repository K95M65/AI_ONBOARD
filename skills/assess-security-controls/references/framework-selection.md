# Framework selection

Select the framework that matches the decision. More requirements do not create better assurance.

## Common routes

| Decision | Suitable starting point | Use |
|---|---|---|
| Organization-wide cybersecurity outcomes and improvement profile | NIST Cybersecurity Framework 2.0 | Govern, Identify, Protect, Detect, Respond, and Recover outcomes |
| Software-security program maturity and roadmap | OWASP SAMM | Governance, design, implementation, verification, and operations practices |
| Web application technical control requirements | OWASP ASVS | Application requirements and verification depth |
| Technical security testing plan | NIST SP 800-115 plus the system's threat model | Test planning, methods, analysis, and mitigation |
| Contract, customer questionnaire, law, regulation, or sector standard | Exact current source supplied or retrieved from the authoritative publisher | Requirement-specific readiness and evidence mapping |

These frameworks are not interchangeable. NIST CSF is outcome-oriented; SAMM assesses software-assurance
practices; ASVS defines application verification requirements. Use more than one only when their roles are
explicit.

## Preserve the native result model

Before testing, retrieve and document the selected framework's current instructions for evaluating and
expressing results. Preserve its native result, such as a maturity level, current/target profile outcome or
gap, requirement verification result, or other defined scale. Do not calculate cross-framework averages or
replace the native method with the skill's optional control-effectiveness judgment.

When management needs a common portfolio view, keep any analyst-created normalization in a separate,
clearly labeled field with its mapping method, limitations, and source results intact.

## Selection record

Capture:

- decision and audience;
- framework title, publisher, version, and official URL;
- retrieval date and local snapshot or checksum where appropriate;
- target profile, tier, level, or subset;
- native result model, calculation or profile method, and aggregation rules;
- tailoring decisions and rationale;
- mappings to other frameworks, labeled as authoritative or analyst-created;
- excluded domains and shared-responsibility boundaries.

## Currency and licensing

Retrieve current framework text from the official publisher when possible. Do not redistribute restricted
standards or copy large portions into the skill. Store organization-permitted excerpts or identifiers in the
assessment artifact and link to the controlled source.

Useful public starting points:

- NIST CSF: https://www.nist.gov/cyberframework
- OWASP SAMM: https://owaspsamm.org/model/
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- NIST SP 800-115: https://csrc.nist.gov/pubs/sp/800/115/final
