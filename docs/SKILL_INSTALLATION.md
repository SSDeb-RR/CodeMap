# Installing the CodeMap skill

CodeMap ships one canonical skill in `skills/codemap` plus repository-local compatibility copies in `.agents/skills/codemap` and `.claude/skills/codemap`.

## Codex and Claude Code user-level install

From a CodeMap clone, run:

```bash
./scripts/install-skills.sh
```

The installer copies the skill into:

- Codex: `${CODEX_HOME:-$HOME/.codex}/skills/codemap`
- Claude Code: `$HOME/.claude/skills/codemap`

It will not replace an existing skill unless you explicitly run `./scripts/install-skills.sh --force`. Restart or open a new agent session after installation so discovery refreshes.

## Claude Code plugin install

CodeMap is also a Claude Code plugin repository:

```text
/plugin marketplace add SSDeb-RR/CodeMap
/plugin install codemap@codemap-marketplace
```

## Usage

Invoke `$codemap` with a public GitHub URL, or omit the target to map the active project. The skill returns links to `index.html` and `graph.json`. It uses only local parsing and Git for public URL checkout.

## API keys

The CLI and skill need no API keys. Keys are only for the optional Next.js application. Run `./scripts/configure-env.sh`, then edit `.env.local` locally. Codex and Claude Code inherit environment variables from the shell that launches them, but the safer project setup is the ignored `.env.local` file.

Never place a key in `SKILL.md`, plugin manifests, prompts, command history, commits, or generated reports. Use provider dashboards to create and rotate Clerk, Supabase, OpenAI, and LangSmith credentials. The variable names are listed in `.env.example`.
