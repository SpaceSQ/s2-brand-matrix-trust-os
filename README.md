# 🏛️ S2 商业世界树引擎 (S2 Brand Matrix & Trust OS)
**v1.2.0 | Environment-Vault Security Edition**

Welcome to the commercial judiciary simulator of the Space² Metaverse. 

## 🛡️ Zero-Trust Architecture & Credential Management
**[CRITICAL SECURITY DISCLOSURE]** To ensure absolute integrity and comply with OWASP anti-hardcoding standards, this plugin enforces **Environment-Vault Authentication**:
1. **No Hardcoded Secrets**: The admin token is completely removed from the codebase and documentation. 
2. **Host-Level Injection**: System administrators MUST inject the credential into the host operating system before running the OpenClaw environment. 
   * *Example:* `export S2_GEO_ADMIN_TOKEN="Your_Super_Secret_Key"`
3. **Fail-Safe Mechanism**: If the `S2_GEO_ADMIN_TOKEN` environment variable is not detected during runtime, all write-operations to the local SQLite ledger are permanently frozen to prevent unauthorized autonomous manipulation.

## 🌟 The GEO Scoring Formula ($T_{score}$)
A brand's simulated visibility is strictly dictated by its inputted physical and commercial integrity:
1. **Tree Root (40%)**: Hard physical strength (Patents + ESG ratings).
2. **Tree Crown (40%)**: Service track record (Contracts completed minus violations).
3. **Time Dimension (20%)**: Loyalty to a SUNS coordinate over time.