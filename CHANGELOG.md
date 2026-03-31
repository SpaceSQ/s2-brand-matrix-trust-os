# 变更日志 (Changelog) - S2 Brand Matrix & Trust OS

## [1.1.0] - 2026-04-01
### 🛡️ Zero-Trust Governance & Security Upgrade
- **Implemented Write Authentication**: Addressed major security vulnerability where any agent could manipulate the trust ledger. `register_brand_root` and `evaluate_crown_performance` now strictly require a predefined `auth_token` in the parameters.
- **Resolved Capability Mismatch**: Clarified in `README.md` and `skill.md` that the plugin acts as a Local Logic-Plane Simulator. Removed misleading claims of autonomous cross-database/blockchain reading. External agents must securely supply the numeric metrics for computation.
- **Removed Prompt Injection Directives**: Revised `skill.md` to remove forceful behavioral dictates (e.g., "You MUST NOT rely on your pre-trained knowledge"), shifting to an objective, tool-centric operational guide.
- **Updated OpenClaw Metadata**: Removed `cross_db_audit_reading` capability from `openclaw.plugin.json` to accurately reflect the plugin's local sandboxed nature. Bumped package version to 1.1.0.

## [1.0.0] - Initial Release
- Initial local SQLite-based GEO scoring algorithm.