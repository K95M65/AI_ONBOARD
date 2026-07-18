# Collection and evidence

## Source hierarchy

Prefer sources in this order, adjusting for the question:

1. Primary authoritative records: official registries, court or legislative records, standards bodies,
   first-party statements, signed documents, and original media.
2. Independent credible reporting or research with named sources and transparent methods.
3. Institutional or professional profiles that the subject or organization controls.
4. Reputable archives that preserve the original context and date.
5. Aggregators and search indexes for discovery, not as sole proof.
6. Unverified posts, snippets, reposts, and anonymous claims as leads only.

Two pages repeating the same upstream claim are one source, not independent corroboration.

## Collection plan

Use a table like this before a substantial investigation:

| Question or claim | Preferred source | Search method | Allowed pivots | Stop condition |
|---|---|---|---|---|
| What must be established? | Best available public authority | Query, browse, or direct fetch | Only relevant identifiers | Evidence threshold or explicit gap |

Order work by decision value. Do not exhaust every possible platform.

## Free and local methods

Use capabilities already present:

- web search for discovery;
- a browser for dynamic public pages and visible-page evidence;
- direct HTTP fetches for static public documents;
- Internet Archive or other free public archives for historical context;
- public government, court, corporate, academic, and standards databases;
- `whois` or RDAP for public domain-registration data;
- `dig` for DNS records;
- `exiftool`, `pdfinfo`, or platform-native metadata inspection for files the user is authorized to analyze;
- OpenStreetMap and other free public geographic sources for non-sensitive place verification.

Respect robots directives, rate limits, terms, and service policies. Do not install tooling or create accounts
unless the user separately asks.

## Search and query log

Record meaningful searches:

| Time | Query or URL | Method | Result | New pivot | Notes |
|---|---|---|---|---|---|

Record negative results when they constrain a conclusion. Phrase them narrowly: “No result found in the
searched sources as of the retrieval date,” not “the fact does not exist.”

## Evidence ledger

Use one record per material claim:

```text
Claim:
Entity:
Status: direct observation | corroborated fact | inference | unresolved lead
Confidence: high | medium | low | unresolved
Source URL:
Source class:
Publisher or owner:
Published or effective date:
Retrieved:
Collection method:
Relevant evidence:
Independent corroboration:
Contradiction:
Identity-resolution basis:
Privacy or handling note:
```

Quote only the minimum text needed to anchor the claim. Preserve enough surrounding context to avoid changing
its meaning.

## Entity resolution

Keep entities separate until evidence supports a merge. Compare:

- authoritative cross-links;
- full name plus role, organization, or geography;
- consistent historical dates;
- self-declared usernames or domains;
- multiple independent attributes; and
- conflicting attributes or impossible timelines.

Do not treat matching names, handles, avatars, writing style, or location as identity proof. Record alternative
explanations and collision risk.

## Confidence and contradiction

Confidence reflects evidence quality, independence, recency, and identity certainty—not the analyst's
intuition.

When sources conflict:

1. Verify that they refer to the same entity and time period.
2. Prefer original and contemporaneous evidence.
3. Check whether one source corrected or superseded another.
4. Record both claims and the reason one is stronger.
5. Leave the issue unresolved when evidence cannot decide it.

Never convert ambiguity into a numerical personal risk score.

## Collection artifacts

Use screenshots only when dynamic state, layout, or visible context is material. Record the URL and retrieval
time next to each screenshot. Avoid screenshots containing unrelated personal information.

Save raw evidence only inside the authorized workspace. Do not commit sensitive artifacts or include them in
public reports.
