# Capture formats

| Format | Best for | Main limitation |
|--------|----------|-----------------|
| Screenshot | Visible layout, labels, and a specific UI state | No underlying requests, links, or replay |
| PDF | Human-readable page rendering and print-oriented review | May omit interactive state and loaded resources |
| HTML or saved response | Static source, headers, and text inspection | Often incomplete for client-rendered applications |
| HAR or browser trace | Diagnosing requests and interactions | Tool-specific, may contain secrets, not a preservation archive |
| WARC | Standardized request/response records and crawl payloads | Replay quality depends on capture coverage |
| WACZ | Portable indexed package for browser-based replay and sharing | Requires a compatible recorder and replay tool |

For JavaScript-heavy sites, prefer a browser-based recorder such as an already-installed Browsertrix
Crawler or ArchiveWeb.page workflow. Browsertrix can generate WACZ from a scoped local container crawl.
ArchiveWeb.page is suited to interactive manual capture. GNU Wget's WARC support can be useful for simpler
HTTP collections but does not reproduce every browser-executed state.

Always verify replay. A successfully created archive file can still be incomplete.
