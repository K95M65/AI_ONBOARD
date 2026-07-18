---
name: conduct-open-source-investigation
description: Plans and conducts lawful, ethical open-source intelligence investigations using public sources and free or local tools, with evidence provenance, entity resolution, confidence grading, contradiction and gap analysis, and decision-ready reporting. Use for public-source research on organizations, domains, public events, a public figure's public activity, journalist fact-checking, defensive threat intelligence, or a consented or self-directed digital-footprint review. Do not use for market or competitor research when those skills fit, stalking, doxxing, real-time location, minors, private data, authentication bypass, paid data brokers, or regulated decisions about a person.
---

# Conduct Open-Source Investigation

Run a public-source investigation as an evidence workflow, not a hunt for maximum personal data. Use the
smallest collection surface that can answer the stated questions, preserve provenance, and separate verified
facts from leads and inference.

This skill owns the investigation from scope through report. It requires no API key, paid service, account
signup, or specific browser package.

## Operating boundaries

Read [references/scope-and-safety.md](references/scope-and-safety.md) before collecting information about a
person, handling sensitive data, or pursuing a target whose purpose or authorization is unclear.

Apply these rules throughout:

- Use publicly accessible sources and free or already-available local tools only.
- Do not use paid or metered research APIs, data brokers, CAPTCHA bypass, auth-wall bypass, leaked
  credentials, private accounts, deceptive contact, or covert interaction.
- Do not contact subjects or associates, create research personas, subscribe, post, upload sensitive
  material, or change external state without separate authorization.
- Minimize personal data. Do not collect data merely because it is findable.
- Stop or narrow the work when the requested purpose creates a material privacy, safety, or high-impact
  decision risk.

## Route adjacent work

Keep the investigation distinct from neighboring workflows:

- Use `market-research` for market structure and sizing.
- Use `competitive-intel` for ethical competitor analysis.
- Use `map-attack-surface` for internal or external exposure mapping when the user affirmatively owns or is
  explicitly authorized to assess the named system. Keep general public organization or domain research in
  this skill and do not turn it into attack-path or security-target prioritization.
- Use `security-audit` or `threat-model` for an owned or authorized system.
- Use `secret-scan` for secrets in a repository the user is authorized to inspect.
- Use `data-storytelling` or `dataviz` for a substantial final narrative or relationship visualization.

Do not duplicate those procedures inside this skill. An investigation may compose with them when its scope
crosses a legitimate boundary.

## Workflow

### 1. Scope and authorize

State:

- the target class: organization, domain, event, public record, public activity, or consented/self review;
- the legitimate purpose and the questions the work must answer;
- the relevant time window and geography;
- prohibited or unnecessary data;
- the stopping condition; and
- any uncertainty about identity, consent, jurisdiction, or authorization.

Ask only for missing information that would materially change safety or method. If a safe, narrow scope is
obvious, state the assumption and proceed.

### 2. Plan collection

Read [references/collection-and-evidence.md](references/collection-and-evidence.md).

Create a compact collection plan:

1. List the claims or questions to resolve.
2. Prioritize primary and authoritative public sources.
3. Define search queries, date ranges, and allowed pivots.
4. Identify likely entity-collision risks.
5. Decide which negative results should be recorded.
6. Assign independent research lanes only when they do not duplicate work.

Prefer browser or web-search capabilities already present in the environment. Use direct fetches for static
public pages. Use local tools such as `curl`, `whois`, `dig`, `exiftool`, or `pdfinfo` only when installed and
relevant; never make installation a prerequisite.

### 3. Collect minimally

Start broad enough to disambiguate, then narrow. For each meaningful search or fetch:

- record the query or URL, retrieval date, and collection method;
- capture only information relevant to the scoped questions;
- distinguish a search-result snippet from the underlying source;
- preserve the source context needed to interpret the finding;
- record useful negative results; and
- note access or tooling gaps without attempting to bypass them.

Treat archives and aggregators as discovery or corroboration sources unless they preserve enough provenance
to support the claim.

### 4. Resolve entities and build evidence

Maintain an evidence ledger rather than a free-form dossier. Each material claim needs:

- claim text;
- subject or entity;
- source URL and source class;
- retrieval date and method;
- direct observation, corroborated fact, inference, or unresolved lead;
- confidence and reason;
- contradicting evidence; and
- privacy or handling note when relevant.

Do not merge identities from a matching name, handle, avatar, or location alone. Require multiple independent
attributes or an authoritative link. Keep ambiguous entities separate.

### 5. Correlate and verify

For every conclusion that could affect a person, organization, or security decision:

1. Prefer the original source over summaries.
2. Seek independent corroboration.
3. Check dates and whether the fact was true during the scoped period.
4. Surface contradictions rather than averaging them away.
5. Label inference explicitly and name the facts that support it.
6. Downgrade confidence when sources share the same upstream origin.
7. Avoid personality, intent, or protected-characteristic profiling.

Use confidence labels consistently:

- **High** — direct authoritative evidence or strong independent corroboration;
- **Medium** — credible but incomplete corroboration;
- **Low** — single-source, ambiguous, stale, or indirect evidence;
- **Unresolved** — conflicting evidence or an unverified lead.

### 6. Assess coverage and stop

Before expanding collection, ask:

- Which unanswered question could materially change the conclusion?
- Is another public source likely to resolve it?
- Would the next step collect disproportionate personal data?
- Would it require a paid service, account, interaction, or bypass?

Continue only for material, proportionate gaps. Stop when the scoped questions are answered, remaining gaps
are explicit, or the next step would cross a boundary.

### 7. Review independently

Use a researcher agent for isolated, non-overlapping public-source lanes when parallelism helps. Use a
reviewer to challenge entity resolution, source independence, and inference. Use a verifier to confirm
citations, accessible sources, dates, and reproducibility before presenting high-confidence findings.

Do not have collection agents contact people, log into accounts, or persist sensitive data outside the
authorized workspace.

### 8. Report

Read [references/reporting.md](references/reporting.md) and match the report depth to the decision.

Always include:

- scope and legitimate purpose;
- concise answer to the stated questions;
- material findings with inline confidence;
- evidence table with URLs and retrieval dates;
- contradictions and unresolved leads;
- coverage gaps and collection limits;
- clear separation of fact and inference; and
- a sensitive-data and retention note when personal data appears.

Use a timeline or entity map only when it materially improves understanding. Redact unnecessary personal
identifiers from the user-facing report.

## Completion standard

The investigation is complete when another analyst can reproduce the important findings from the evidence
ledger, understand why each conclusion has its confidence level, see what remains unknown, and confirm that
the collection stayed within the declared public-source and no-paid-service boundaries.
