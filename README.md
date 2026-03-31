# 🏛️ S2 商业世界树引擎 (S2 Brand Matrix & Trust OS)
**v1.4.0 | Cryptographic Auth Edition**

Welcome to the commercial judiciary simulator of the Space² Metaverse. 

## 🛡️ Zero-Trust Architecture: HMAC-SHA256 Signatures
To fully resolve metadata mismatches and weak authentication, this plugin enforces banking-grade cryptographic security:
1. **Host-Level Secret Key**: The `S2_GEO_ADMIN_TOKEN` (must be >= 16 chars) is declared explicitly in the registry `package.json` configSchema and stored purely in the host OS environment.
2. **Cryptographic Validation**: The Python handler no longer just checks if the token "exists". It uses the host token as a Private Key to compute an HMAC-SHA256 signature of the incoming JSON payload. If the `signature` passed in the parameters does not cryptographically match, the write request is rejected.
3. **Anti-Tampering**: This guarantees that even if an Agent autonomously attempts to write to the DB, it will fail unless the payload was cryptographically signed by an authorized external admin pipeline.

## 🌟 The GEO Scoring Formula ($T_{score}$)
1. **Tree Root (40%)**: Hard physical strength (Patents + ESG ratings).
2. **Tree Crown (40%)**: Service track record (Contracts completed minus violations).
3. **Time Dimension (20%)**: Loyalty to a SUNS coordinate over time.