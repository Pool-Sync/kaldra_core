# API v3.1 Reference Documentation

**Version:** 3.1.0  
**Status:** Production Ready  
**Base URL:** `/api/v3.1`

---

## Overview

KALDRA API v3.1 introduces preset-based and profile-aware narrative analysis with enhanced signal output including Meta engines (Nietzsche, Aurelius, Campbell) and Kindra 3×48 vector analysis.

**Key Features:**
- Domain-specific presets (Alpha, Geo, Safeguard, Product)
- User profile customization
- Enhanced signal format with backward compatibility
- Meta-philosophical analysis outputs
- Detailed Kindra layer scores

---

## Endpoints

### 1. POST /api/v3.1/analyze

Execute KALDRA narrative analysis with preset and profile support.

**Request:**
```json
{
  "text": "string (required, 1-50000 chars)",
  "preset": "string (optional): alpha | geo | safeguard | product",
  "profile_id": "string (optional): user profile identifier"
}
```

**Response:** `AnalyzeV31Response`
```json
{
  "version": "3.1",
  "request_id": "string",
  "timestamp": 1701234567.89,
  "mode": "signal | full | story | safety-first",
  "degraded": false,
  
  "preset_used": "alpha",
  "preset_config": {
    "mode": "full",
    "emphasis": { "kindra.layer1": 1.0, ... },
    "thresholds": { "risk": 0.30, ... },
    "output_format": "financial_brief"
  },
  
  "meta": {
    "nietzsche": { ... },
    "aurelius": { ... },
    "campbell": { ... }
  },
  
  "kindra": {
    "layer1": { "E01": 0.23, ... },
    "layer2": { ... },
    "layer3": { ... },
    "tw_plane_distribution": { "3": 0.33, "6": 0.34, "9": 0.33 }
  },
  
  "archetypes": { ... },
  "drift": { ... },
  "risk": { ... },
  "summary": { ... }
}
```

**Example:**
```bash
curl -X POST /api/v3.1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Market volatility increased...",
    "preset": "alpha",
    "profile_id": "user_123"
  }'
```

**Error Responses:**
- `400` — Invalid preset name
- `404` — Profile not found
- `422` — Validation error (empty text, invalid fields)
- `500` — Analysis pipeline error

---

### 2. GET /api/v3.1/presets

List all available analysis presets.

**Request:** None (GET request)

**Response:** `PresetsResponse`
```json
{
  "presets": {
    "alpha": {
      "name": "alpha",
      "description": "Financial / earnings narrative analysis",
      "mode": "full",
      "emphasis": ["kindra.layer1", "meta.nietzsche", "core.archetypes"],
      "thresholds": { "risk": 0.30, "confidence_min": 0.60 },
      "output_format": "financial_brief",
      "metadata": { "domain": "finance", ... }
    },
    "geo": { ... },
    "safeguard": { ... },
    "product": { ... }
  }
}
```

**Example:**
```bash
curl /api/v3.1/presets
```

---

### 3. GET /api/v3.1/profile/{user_id}

Retrieve user profile by ID.

**Path Parameters:**
- `user_id` (string, required): User identifier

**Response:** `ProfileResponse`
```json
{
  "user_id": "user_123",
  "preferred_preset": "geo",
  "risk_tolerance": 0.7,
  "output_format": "json",
  "depth": "deep",
  "preferences": { "custom_field": "value" }
}
```

**Error Responses:**
- `404` — Profile not found

**Example:**
```bash
curl /api/v3.1/profile/user_123
```

---

### 4. PUT /api/v3.1/profile/{user_id}

Create or update user profile.

**Path Parameters:**
- `user_id` (string, required): User identifier

**Request:** `ProfileUpdateRequest`
```json
{
  "preferred_preset": "alpha | geo | safeguard | product (optional)",
  "risk_tolerance": "float [0.0, 1.0] (optional)",
  "output_format": "string (optional)",
  "depth": "fast | standard | deep | exploratory (optional)"
}
```

**Response:** `ProfileResponse` (updated profile)

**Example:**
```bash
curl -X PUT /api/v3.1/profile/user_123 \
  -H "Content-Type: application/json" \
  -d '{
    "preferred_preset": "geo",
    "risk_tolerance": 0.8,
    "depth": "deep"
  }'
```

---

## Preset Configurations

### Alpha (Financial Analysis)
- **Mode:** full
- **Emphasis:** Kindra Layer 1 (Cultural/Macro), Nietzsche (Power Dynamics), Archetypes
- **Use Case:** Earnings calls, financial reports, market narratives

### Geo (Geopolitical Analysis)
- **Mode:** story
- **Emphasis:** Kindra Layer 1 (Geopolitics), TW-plane, Aurelius (Stoic Crisis Management)
- **Use Case:** Political analysis, regime dynamics, international relations

### Safeguard (Safety-First)
- **Mode:** safety-first
- **Emphasis:** Safeguard systems, Tau, Bias detection, Kindra Layer 2 (Media Toxicity)
- **Use Case:** Content moderation, risk mitigation, safety reviews

### Product (Brand/Marketing)
- **Mode:** full
- **Emphasis:** Kindra Layer 2 (Semiotic/Media), Campbell (Hero's Journey), Polarities
- **Use Case:** Brand narratives, product launches, marketing campaigns

---

## Signal Format (v3.1)

### Enhanced Fields (New in v3.1)

**preset_used** (string): Name of preset used for analysis

**preset_config** (object): Resolved configuration
- `mode`: Execution mode
- `emphasis`: Weighted stage priorities
- `thresholds`: Risk and confidence limits
- `output_format`: Response format type

**meta** (object): Meta-philosophical engines
- `nietzsche`: Will to Power, Ressentiment, Master/Slave dynamics
- `aurelius`: Stoic principles, Control dichotomy, Virtue alignment
- `campbell`: Hero's Journey stage, Archetype, Transformation score

**kindra** (object): Enhanced 3×48 structure
- `layer1`: 48 cultural/macro vectors
- `layer2`: 48 semiotic/media vectors
- `layer3`: 48 structural/systemic vectors
- `tw_plane_distribution`: Temporal Wave distribution (3/6/9)
- `top_vectors`: Highest scoring vectors across layers

### Backward Compatibility

All v2.x and v3.0 fields are **preserved**:
- `version`, `request_id`, `timestamp`, `mode`, `degraded`
- `input`, `archetypes`, `drift`, `risk`, `summary`
- No field removal or renaming
- New fields additive only

---

## Error Handling

All errors return JSON:
```json
{
  "detail": "Error message"
}
```

**Common Errors:**
- `400 Bad Request` — Invalid input (preset, profile settings)
- `404 Not Found` — Resource doesn't exist (profile)
- `422 Unprocessable Entity` — Schema validation failed
- `500 Internal Server Error` — Pipeline failure (gracefully handled)

---

## Migration Guide (v3.0 → v3.1)

### For API Clients:

1. **No breaking changes** — All v3.0 clients continue to work
2. **New fields available** — Optionally consume `meta`, enhanced `kindra`, `preset_config`
3. **New endpoints** — Use `/api/v3.1/presets` and `/api/v3.1/profile` for enhanced features

### Recommended Updates:

```javascript
// Old (v3.0)
const response = await fetch('/analyze', {
  method: 'POST',
  body: JSON.stringify({ text })
});

// New (v3.1) - with preset
const response = await fetch('/api/v3.1/analyze', {
  method: 'POST',
  body: JSON.stringify({ 
    text, 
    preset: 'alpha',
    profile_id: userId 
  })
});

// Access new fields
const { meta, kindra, preset_config } = await response.json();
```

---

## Rate Limits

- Standard: 100 requests/minute
- Burst: 200 requests/minute
- Profile updates: 10 requests/minute per user

---

## Support

For issues or questions:
- Documentation: `/docs/api/`
- GitHub: kaldra-core/issues
- Contact: support@4iam.ai
