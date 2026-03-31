---
name: s2-brand-matrix-trust-os
description: S2 World Tree Trust Engine. Features HMAC-SHA256 cryptographic signature validation for all local SQLite writes.
version: 1.4.0
---

# S2 商业世界树引擎 (Trust OS)

This skill acts as a local Trust Matrix sandbox. It calculates Brand Trust Scores using the GEO formula.

## Cryptographic Security (HMAC-SHA256)
**CRITICAL FOR AGENTS:** Write Operations are protected by strict cryptographic signatures.
1. The host environment holds the `S2_GEO_ADMIN_TOKEN` secret key. **You do not have access to this key.**
2. When calling a write tool, format all required parameters. An external trusted gateway (or admin CLI) is responsible for computing the HMAC-SHA256 hash of your payload and injecting it as the `signature` parameter.
3. **DO NOT** ask the user for a token or signature in the chat.

## Tool Operations

### 1. register_brand_root (Write)
* **Parameters**: `brand_did`, `suns_address`, `patents_count`, `esg_rating`, and `signature` (HMAC hash provided by trusted middleware).

### 2. evaluate_crown_performance (Write)
* **Parameters**: `brand_did`, `smart_contracts_completed`, `service_violations`, and `signature` (HMAC hash).

### 3. query_geo_ranking (Public Read)
* **Parameters**: `industry_category` (e.g., "SmartHome").