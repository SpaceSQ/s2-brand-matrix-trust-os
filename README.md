# 🏛️ S2 商业世界树引擎 (S2 Brand Matrix & Trust OS)
**v1.3.0 | Silent Auth Edition**

Welcome to the commercial judiciary simulator of the Space² Metaverse. 

## 🛡️ Zero-Trust Architecture: Silent Authentication
To comply with the highest standards of LLM security, this plugin utilizes **Silent Host-Environment Authentication**:
1. **No Chat Exposure**: Agents are strictly instructed never to ask for the admin token in the chat prompt, preventing credential leakage to LLM providers.
2. **Declared Metadata**: The required `S2_GEO_ADMIN_TOKEN` is explicitly declared in `openclaw.plugin.json`'s `configSchema`. The OpenClaw host runtime must securely inject this variable before instantiation.
3. **Implicit Verification**: The Python handler reads the token directly from the OS environment (`os.environ`). Write tools no longer accept auth parameters from the agent.

## 🌟 The GEO Scoring Formula ($T_{score}$)
1. **Tree Root (40%)**: Hard physical strength (Patents + ESG ratings).
2. **Tree Crown (40%)**: Service track record (Contracts completed minus violations).
3. **Time Dimension (20%)**: Loyalty to a SUNS coordinate over time.