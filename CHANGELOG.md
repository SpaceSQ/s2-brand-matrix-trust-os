# 变更日志 (Changelog) - S2 Brand Matrix & Trust OS

## [1.2.0] - 2026-04-01
### 🔒 Security Patch (Hardcoded Secret Removal)
- **Environment-Vault Authentication**: Addressed critical security feedback regarding hardcoded secrets. The `ADMIN_TOKEN` has been entirely purged from `handler.py` and `skill.md`. 
- **Fail-Safe Implementation**: The Python handler now dynamically reads the `S2_GEO_ADMIN_TOKEN` environment variable from the host OS. If absent, all local write operations fail safely and are frozen.
- **User-in-the-loop Protocol**: Updated `skill.md` to explicitly forbid the agent from guessing the token, forcing it to ask the human administrator for the credential during runtime.

## [1.1.0] - 2026-04-01
### 🛡️ Zero-Trust Governance & Security Upgrade
- Implemented basic Write Authentication token requirements.
- Resolved Capability Mismatch (Clarified Local Simulator scope).

## [1.0.0] - Initial Release
- Initial local SQLite-based GEO scoring algorithm.