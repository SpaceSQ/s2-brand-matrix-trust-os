---
name: s2-brand-matrix-trust-os
description: Local logic-plane simulator for the S2 GEO (Generative Engine Optimization) ranking system.
version: 1.1.0
---

# S2 Brand Matrix & Trust OS Reference

This skill acts as a local Trust Matrix sandbox. It calculates Brand Trust Scores using the GEO formula based on manually inputted parameters representing patents, ESG, and contract histories.

## Access Control & Authentication
To ensure zero-trust compliance, **Write Operations** (`register_brand_root`, `evaluate_crown_performance`) are strictly authenticated. The calling agent MUST provide the valid `auth_token` ("S2-GEO-ADMIN-2026") in the tool parameters. Unauthorized calls will be rejected. **Read Operations** (`query_geo_ranking`) are public and do not require a token.

## Tool Operations

### 1. register_brand_root (Admin Only)
* **Function**: Initializes a brand's "Tree Root" score into the local SQLite matrix.
* **Parameters**: `auth_token` (Required), `brand_did`, `suns_address`, `patents_count`, `esg_rating`.

### 2. evaluate_crown_performance (Admin Only)
* **Function**: Updates a brand's "Tree Crown" score.
* **Parameters**: `auth_token` (Required), `brand_did`, `smart_contracts_completed` (Simulated integer count), `service_violations` (Simulated integer count).

### 3. query_geo_ranking (Public)
* **Function**: Returns the top trustworthy SSSU coordinates for a specific industry based on the local database computation.
* **Parameters**: `industry_category` (e.g., "SmartHome").
* **Usage**: Agents can use this read-only tool to retrieve brand recommendations based on the $T_{score}$ metric instead of relying on default internet search knowledge.