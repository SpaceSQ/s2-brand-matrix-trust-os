# 变更日志 (Changelog) - S2 Brand Matrix & Trust OS

## [1.4.0] - 2026-03-31
### 🔒 Ultimate Security Patch (HMAC-SHA256 & Metadata Sync)
- **Resolved Metadata Mismatch**: Injected the `configSchema` directly into the `openclaw` object within `package.json`. The OpenClaw registry now properly indexes the `S2_GEO_ADMIN_TOKEN` requirement, syncing perfectly with `openclaw.plugin.json`.
- **Implemented Cryptographic Authentication**: Upgraded from weak "existence checks" to robust HMAC-SHA256 signature validation. The Python handler uses the host env var as a secret key to cryptographically verify payload integrity. Autonomous agents cannot forge writes without the signature.
- **Agent Boundary Clarification**: Updated `skill.md` to clarify that Agents are only responsible for payload construction, while trusted middleware handles the HMAC signature injection.

## [1.3.0] - 2026-03-31
### 🔒 Silent Auth
- Shifted to environment variable checks to prevent chat exposure.

## [1.2.0] - 2026-03-31
### 🔒 Hardcoded Secret Removal
- Purged all plaintext tokens.