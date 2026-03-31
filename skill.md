---
name: s2-brand-matrix-trust-os
description: Local logic-plane simulator for the S2 GEO (Generative Engine Optimization) ranking system.
version: 1.2.0
---

# S2 Brand Matrix & Trust OS Reference

This skill acts as a local Trust Matrix sandbox. It calculates Brand Trust Scores using the GEO formula based on manually inputted parameters.

## Access Control & Authentication (User-in-the-Loop)
**CRITICAL SECURITY DIRECTIVE FOR AGENT:**
Write Operations (`register_brand_root`, `evaluate_crown_performance`) are strictly protected by a host-level environment variable. 
1. **You DO NOT know the `auth_token`.** It is not written anywhere in this documentation.
2. Before invoking any write tool, you **MUST explicitly ask the human user** to provide the Admin Token in the chat prompt.
3. Do not attempt to guess, hallucinate, or bypass this token requirement.

Read Operations (`query_geo_ranking`) are public and do not require a token.

## Tool Operations

### 1. register_brand_root (Admin Only)
* **Function**: Initializes a brand's "Tree Root" score into the local SQLite matrix.
* **Parameters**: `auth_token` (Ask the human for this), `brand_did`, `suns_address`, `patents_count`, `esg_rating`.

### 2. evaluate_crown_performance (Admin Only)
* **Function**: Updates a brand's "Tree Crown" score.
* **Parameters**: `auth_token` (Ask the human for this), `brand_did`, `smart_contracts_completed`, `service_violations`.

### 3. query_geo_ranking (Public)
* **Function**: Returns the top trustworthy SSSU coordinates for a specific industry based on the local database computation.
* **Parameters**: `industry_category` (e.g., "SmartHome").