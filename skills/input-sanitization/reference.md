# Input sanitization — per-sink reference

The rule is always **validate at the boundary, encode at the sink**. What "encode" means depends entirely on
the sink:

| Sink | Attack | Do | Don't |
|------|--------|----|-------|
| SQL / NoSQL | SQLi | Parameterized queries / prepared statements; ORM bindings | String-concatenate values into the query |
| OS / shell | Command injection | Pass an **arg array** to exec; avoid shelling out | Build a shell string from input; `shell=True` |
| HTML body | Stored/reflected XSS | Context-aware escaping; framework auto-escape | `innerHTML` / `dangerouslySetInnerHTML` with input |
| HTML attribute / JS / URL | XSS | Encode for that specific context | Assume body-escaping covers attributes |
| Filesystem path | Path traversal | Resolve, then confirm inside an allowed root | Join input to a base path unchecked |
| Outbound HTTP | SSRF | Allow-list hosts; block internal/link-local IPs | Fetch an arbitrary user-supplied URL |
| LDAP / XPath | Injection | Parameterized APIs / escaping for that grammar | Concatenate filters |
| Regex (from input) | ReDoS | Bound input length; avoid catastrophic backtracking | Compile user-supplied patterns unbounded |
| Redirect target | Open redirect | Allow-list relative/known targets | Redirect to a raw input URL |
| File upload | Malware / overwrite | Validate type by content, random server-side names, size caps | Trust the client filename or content-type |

## Validation checklist

- [ ] Normalize (Unicode NFC, path canonicalization, lowercasing where relevant) **before** validating.
- [ ] Allow-list: type, length/range, format (regex anchored), enum membership.
- [ ] Reject early with a clear error; don't silently coerce.
- [ ] Apply the same validation to **every** entry: body, query, headers, cookies, path params, CLI args,
      env, file contents, message payloads.
- [ ] Encode/parameterize at each sink independently — one input can reach several sinks.
