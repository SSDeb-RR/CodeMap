# Optional application credentials

The CodeMap CLI and skill require no API keys. The optional web application uses the variables listed in the repository's `.env.example` for Clerk, Supabase, OpenAI, and LangSmith.

Run `./scripts/configure-env.sh` from the repository, then edit `.env.local` locally. Keep that file untracked. Never ask the user to paste a secret into chat, place credentials in this skill, or write credentials into a generated report.
