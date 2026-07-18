---
name: retrieve-technical-docs
description: Retrieves version-matched, current technical documentation and release evidence for libraries, frameworks, APIs, protocols, and developer tools. Use when implementation depends on unstable or unfamiliar APIs, migration details, exact configuration, deprecations, or current best practices; do not use for general market research, product recommendations, or repository facts already available locally.
---

# Retrieve technical docs

Ground technical decisions in the version the project actually uses. Prefer local and primary evidence over
aggregated snippets, and keep retrieval separate from implementation.

## Identify the real version

Inspect manifests, lockfiles, runtime output, generated clients, deployment targets, feature flags, and
existing imports before searching. Record the library, version or commit, language, platform, and exact
question. If version cannot be established, state the range and uncertainty.

## Follow the source hierarchy

Read [references/source-strategy.md](references/source-strategy.md). Search in this order:

1. repository instructions, vendored docs, types, tests, examples, and installed package source;
2. versioned official documentation and API references;
3. official source repository, tags, release notes, migration guides, and issue tracker;
4. official `llms.txt` or downloadable documentation when available;
5. a documentation index such as Context7 or DevDocs for discovery, followed by primary-source
   verification.

Use Context7 only when already available and useful. Do not make an account, API key, paid plan, or hosted
service a prerequisite. Its result is a retrieval aid, not authority.

## Resolve the question

- Query for the exact symbol, configuration key, error, version transition, or behavioral contract.
- Separate current guidance from historical examples and unreleased main-branch behavior.
- Verify code examples against the target language and version.
- Check deprecation, platform, security, and deployment constraints.
- When primary sources disagree, show the conflict and prefer the source tied most directly to the released
  artifact.
- Cite the page, version/tag, and retrieval date close to each material conclusion.

## Return a compact evidence brief

Include:

- target package/API and resolved version;
- answer and implementation consequence;
- supported example or configuration fragment;
- primary sources and relevant release boundary;
- uncertainty, contradiction, or follow-up check.

Do not paste entire documentation pages or fill context with unrelated reference material.

## Persist only when useful

If the user requests durable knowledge, compose with `obsidian` and create a concise note containing the
question, version, decision, sources, retrieval date, and invalidation condition. Prefer Markdown files and
wikilinks; do not require Obsidian Sync, Publish, a community plugin, or any paid service.

Finish when the answer is version-matched, traceable to primary evidence, and small enough to guide the
implementation without replacing the official documentation.
