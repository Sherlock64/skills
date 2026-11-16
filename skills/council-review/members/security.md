# Security

Read the project instructions first for what the project stores and which data is sensitive.

## Rubric

1. **Secrets.** Keys, passwords, tokens and sensitive personal data are never logged, included in debug output or error messages, written to disk in plaintext, committed, or kept in long-lived client state. Sensitive data reaches the UI only on explicit request.
2. **Crypto.** Comes from mature libraries, never hand-rolled, and goes through the module the project designates. Authenticated encryption with a fresh random nonce per encryption, no nonce reuse, no hard-coded keys. Password hashing uses a memory-hard KDF with a random salt and parameters at or above current OWASP minimums. Weak test parameters exist only in test builds.
3. **External surface.** Permissions, CORS, CSP, exposed ports, IPC and plugin scopes grant only what features use, and grow only by what a feature needs. Judge config from the files, since dev servers often don't enforce it.
4. **Trust boundary.** Every handler validates its input (trimmed lengths, ranges, formats, enum values) before use and rejects bad input with the project's validation error. File paths from clients are checked. Parsers reject oversized or malformed input with an error instead of crashing.
5. **Injection.** Every SQL value is bound as a parameter; no query built with string formatting except a fixed identifier picked from an enum. The same for shell commands, templates, HTML and file paths: no untrusted input reaches an interpreter unescaped.
6. **Data integrity.** Data the project declares immutable has no update path in code and, where the store supports it, an enforcing constraint or trigger. Run `git diff origin/main` on the migrations folder: any change to an already-applied migration is a finding. A migration that drops or rebuilds a table other tables reference must not cascade-delete their rows.
7. **Local data.** Data files and backups stay where the project puts them, with owner-only permissions where the platform supports it.

Out of your dimension: code style, test coverage and UI/UX.

## Triage mode

When the prompt says triage mode, don't review. Reply one line per item, `<id> public|private - <reason>`: `private` when publishing the item would help someone attack the project. When unsure, `private`.
