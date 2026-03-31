---
name: s2-brand-matrix-trust-os
description: Local logic-plane simulator for the S2 GEO ranking system. Features silent host-environment authentication.
version: 1.3.0
---

# S2 Brand Matrix & Trust OS Reference

This skill acts as a local Trust Matrix sandbox. It calculates Brand Trust Scores based on manually inputted parameters.

## Authentication Security (Silent Auth)
**CRITICAL:** Authentication for Write Operations is handled entirely under the hood by the host operating system. 
* **DO NOT** ask the human user to provide an auth token in the chat.
* **DO NOT** pass any token in the tool parameters.
If the host has not configured the environment variable, the tool will safely return an Access Denied error. You should simply relay this error to the user and ask them to check their system configuration.

## Tool Operations

### 1. register_brand_root 
* **Function**: Initializes a brand's "Tree Root" score into the local SQLite matrix.
* **Parameters**: `brand_did`, `suns_address`, `patents_count`, `esg_rating`. (No auth token required in parameters).

### 2. evaluate_crown_performance 
* **Function**: Updates a brand's "Tree Crown" score.
* **Parameters**: `brand_did`, `smart_contracts_completed`, `service_violations`. (No auth token required in parameters).

### 3. query_geo_ranking 
* **Function**: Returns the top trustworthy SSSU coordinates for a specific industry.
* **Parameters**: `industry_category` (e.g., "SmartHome").