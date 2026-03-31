# 变更日志 (Changelog) - S2 Brand Matrix & Trust OS

## [1.3.0] - 2026-03-31
### 🔒 Security Patch (Silent Auth & Metadata Sync)
- **Resolved Metadata Inconsistency**: Explicitly declared the `S2_GEO_ADMIN_TOKEN` in `openclaw.plugin.json` under `configSchema` so the host platform is aware of the required environment variable.
- **Eliminated User-Exposure Risk**: Completely removed the `auth_token` parameter from all write tools. The Python handler now reads the token directly and silently from the host OS environment.
- **Agent Prompt Purge**: Overhauled `skill.md` to explicitly forbid the agent from asking the human for the token in the chat interface, protecting sensitive credentials from being logged in LLM context histories.

## [1.2.0] - 2026-04-01
### 🔒 Hardcoded Secret Removal
- Purged all plaintext tokens from the repository.

## [1.1.0] - 2026-04-01
### 🛡️ Zero-Trust Governance
- Clarified local simulation scope and added basic auth checks.