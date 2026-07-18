---
name: assess-security-controls
description: Evaluates security controls for an organization, system, product, or process against a selected current framework using scoped requirements, traceable evidence, design and operating-effectiveness tests, gap ratings, and an improvement plan. Use for security control reviews, readiness assessments, customer or board assurance, NIST CSF or OWASP ASVS/SAMM baselines, and evidence-based program assessments. It does not certify compliance, provide a legal opinion, or substitute checklist completion for tested evidence.
---

# Assess security controls

Produce an evidence-based assessment that says what was tested, what works, what does not, and what remains
unknown. Never imply certification or assurance beyond the work performed.

## Define the assessment

1. Name the organization, system, product, process, environments, time period, stakeholders, and decision the
   assessment must support.
2. Select the smallest suitable framework and target profile using
   [references/framework-selection.md](references/framework-selection.md).
3. Retrieve the current official framework or customer requirement when internet access is available.
   Record its version, publication source, retrieval date, and any tailoring.
4. Identify exclusions, inherited controls, shared-responsibility boundaries, materiality thresholds, and
   evidence-access limits.
5. State explicitly whether the work is self-assessment, readiness, internal audit support, or an independent
   consulting review. Do not call it certification, attestation, or legal compliance unless an authorized
   qualified party is performing that engagement.

## Route adjacent work

- Use `map-attack-surface` to establish assets, ownership, and exposure before judging coverage.
- Use `threat-model` to determine which control failures matter most.
- Use `security-audit` and specialized security skills for technical inspection.
- Use `manage-vulnerability-risk` to assess or improve finding remediation and exception handling.
- Use an incident, cloud, identity, supply-chain, or privacy specialist when the selected requirements need
  expertise this skill does not contain.

This skill owns evidence mapping and assessment judgments, not every domain test.

## Run the assessment

### 1. Build the requirement matrix

Copy [assets/control-assessment-template.md](assets/control-assessment-template.md) when a durable artifact
helps. For each selected requirement, record:

- exact identifier and requirement text or faithful summary;
- the framework-native result field and evaluation method;
- applicability and rationale;
- control objective and expected outcome;
- control owner and implementation;
- evidence requested and test procedure;
- related assets, risks, and inherited or shared controls.

Keep source requirements distinct from organization-specific control statements.

### 2. Collect evidence

Read [references/evidence-and-testing.md](references/evidence-and-testing.md). Prefer direct, current,
representative evidence over policy assertions. Preserve source, scope, date, collector, and limitations.
Minimize secrets and personal data; reference protected evidence rather than duplicating it.

Use interviews to explain process and locate evidence, not as sole proof that a technical or recurring
control operates.

### 3. Test design and operation

Evaluate separately:

- **Design:** would the control, as defined and implemented, meet the objective?
- **Operation:** did it operate consistently for the scoped period and population?
- **Coverage:** which relevant assets, identities, environments, or events were included?

Choose samples based on risk and population, document the method, and avoid generalizing beyond the sample.
Trace material exceptions to business impact and plausible threat paths.

### 4. Record framework-native results

Use the selected framework's current result model and calculation or profile method as the primary result.
Examples include a SAMM maturity level, a NIST CSF current/target profile outcome or gap, or an ASVS
requirement verification result. Document the method and do not translate or average results unless the
framework or an explicitly labeled analyst mapping supports it.

When a separate control-effectiveness judgment helps the assessment decision, record it as a supplemental
field using these statuses:

- **Effective:** suitably designed and supported by sufficient operating evidence.
- **Partially effective:** material scope, consistency, or evidence gaps remain.
- **Ineffective:** implemented but not capable of or consistently achieving the objective.
- **Not implemented:** no operative control was evidenced.
- **Not applicable:** excluded with a defensible scope rationale.
- **Not assessed:** evidence or access was insufficient; never convert this to a pass.

Do not force the supplemental scale onto a maturity model, profile, or requirement-verification method.
Record evidence sufficiency and confidence separately from both result fields.

### 5. Prioritize improvements

Group root causes and systemic gaps rather than producing a flat checklist. Prioritize using threat
relevance, exposure, business consequence, affected population, control dependency, and confidence.

For each improvement, identify the target outcome, accountable owner, milestones, validation method,
dependencies, expected residual risk, and target date. Separate quick containment from durable correction.

### 6. Review and report

Use an independent reviewer to challenge applicability, sampling, evidence sufficiency, and status
consistency. Use a verifier to reproduce a risk-based sample of evidence links and calculations when
available.

Report:

- scope, assessment type, framework/version, tailoring, and limitations;
- executive conclusion without unsupported assurance language;
- coverage and evidence summary;
- framework-native results, any supplemental effectiveness judgments, and confidence;
- material gaps, systemic themes, and affected risks;
- prioritized improvement roadmap; and
- unassessed areas, inherited dependencies, and residual risk.

## Guardrails

- Do not invent evidence, policies, owners, dates, control operation, or framework requirements.
- Do not mark a control effective from documentation alone when operation matters.
- Do not hide unavailable evidence in an average or maturity score.
- Do not treat a vendor certification as proof that the organization's configuration or use is effective.
- Do not make a paid compliance platform or assessment service a prerequisite.
- Verify current framework text from its official publisher instead of relying on embedded memory.

## Completion standard

The assessment is complete when every selected requirement has an applicability decision, traceable evidence
or an explicit gap, documented design and operation judgments, consistent status and confidence, and an
owned improvement or residual-risk decision for every material deficiency.
