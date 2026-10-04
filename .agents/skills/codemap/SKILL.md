---
name: codemap
description: Generate a deterministic interactive dependency map for the current JavaScript, TypeScript, or Python project, or for a public GitHub repository URL. Use when the user asks to map, visualize, or understand codebase architecture and dependencies. Do not use for code review or inferred relationships.
---

# CodeMap

Generate the map with the bundled runner. If the user provides a public GitHub URL, pass it as the first argument. Otherwise run it without a target so it analyzes the active project directory.

```bash
"<skill-directory>/scripts/run.sh"
"<skill-directory>/scripts/run.sh" https://github.com/owner/repository
```

Optionally append `--out <directory>`. Return clickable links to the generated `index.html` and `graph.json`.

The report is deterministic and keyless. Never invent relationships or supplement unresolved imports with guesses. Report unsupported languages explicitly. Read `references/api-keys.md` only when the user asks about configuring the optional web application.
