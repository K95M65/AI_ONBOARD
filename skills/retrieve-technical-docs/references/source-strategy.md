# Source strategy

## Free-first retrieval paths

| Situation | Preferred path |
|-----------|----------------|
| Dependency is installed | Local types, package source, tests, and lockfile |
| Project publishes versioned docs | Official version selector or tagged documentation |
| API changed recently | Official changelog, release notes, migration guide, and tag diff |
| Site exposes `llms.txt` | Use it as an index, then open the cited official pages |
| Many common APIs are needed offline | DevDocs or locally downloaded official docs |
| Context7 is already connected | Use it to locate relevant passages, then verify primary sources |
| Durable team knowledge is requested | Write a sourced Obsidian/Markdown note with an invalidation condition |

Context7's MCP and CLI client are open source, but its indexing and crawling backend is a hosted service and
full self-hosting is not the default free path. Treat its free tier as optional convenience, not a framework
dependency.

## Obsidian note shape

```markdown
---
type: technical-decision
library: <name>
version: <version or commit>
retrieved: <YYYY-MM-DD>
---

# <Question>

Decision:
Evidence:
Sources:
Invalid when:
Related: [[Project or component]]
```
