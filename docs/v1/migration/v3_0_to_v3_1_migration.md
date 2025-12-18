# Migration Guide: v3.0 → v3.1

**Version:** KALDRA v3.1.0  
**Date:** 2025-12-03  
**Status:** Production Ready

---

## Overview

KALDRA v3.1 introduces the **Exoskeleton Layer** with presets and user profiles, along with significantly enhanced signal output. **This is a fully backward-compatible release** — all existing v3.0 clients will continue to work without modification.

This guide helps you understand what's new and how to adopt v3.1 features.

---

## What's New in v3.1

### 1. Exoskeleton Layer

**Presets** — Domain-specific analysis configurations:
- `alpha`: Financial/earnings analysis
- `geo`: Geopolitical narratives
- `safeguard`: Safety-first risk assessment
- `product`: Brand/marketing resonance

**Profiles** — Persistent user preferences:
- Preferred preset
- Risk tolerance
- Analysis depth
- Output format

**PresetRouter** — Intelligent config merging:
- Combines preset + profile
- Applies user overrides
- Automatic fallback

### 2. Enhanced Signal Format

**Meta Engines** now exposed:
```json
"meta": {
  "nietzsche": { "will_to_power": 0.75, ... },
  "aurelius": { "stoic_acceptance": 0.82, ... },
  "campbell": { "journey_stage": "ordeal", ... }
}
```

**Kindra 3×48** structure:
```json
"kindra": {
  "layer1": { "E01": 0.23, ... },
  "layer2": { ... },
  "layer3": { ... },
  "tw_plane_distribution": { "3": 0.33, "6": 0.34, "9": 0.33 }
}
```

**Preset Metadata**:
```json
"preset_used": "alpha",
"preset_config": {
  "mode": "full",
  "emphasis": { ... },
  "thresholds": { ... }
}
```

### 3. New API Endpoints

- `POST /api/v3.1/analyze` — Preset + profile aware analysis
- `GET /api/v3.1/presets` — List available presets
- `GET /api/v3.1/profile/{user_id}` — Get user profile
- `PUT /api/v3.1/profile/{user_id}` — Create/update profile

---

## API Differences

### Endpoint Changes

| v3.0 | v3.1 | Status |
|------|------|--------|
| Legacy `/analyze` | `/api/v3.1/analyze` | Both supported |
| N/A | `/api/v3.1/presets` | New |
| N/A | `/api/v3.1/profile/{user_id}` | New |

### Request Differences

**v3.0 Analyze:**
```json
{
  "text": "Analysis text"
}
```

**v3.1 Analyze (Enhanced):**
```json
{
  "text": "Analysis text",
  "preset": "alpha",        // NEW: optional
  "profile_id": "user_123"  // NEW: optional
}
```

### Response Differences

**v3.0 Response** (all fields preserved):
```json
{
  "version": "3.0",
  "request_id": "...",
  "timestamp": 123456789.0,
  "mode": "full",
  "archetypes": { ... },
  "risk": { ... },
  "summary": { ... }
}
```

**v3.1 Response** (backward compatible + new fields):
```json
{
  "version": "3.1",
  "request_id": "...",
  "timestamp": 123456789.0,
  "mode": "full",
  
  // NEW v3.1 fields
  "preset_used": "alpha",
  "preset_config": { ... },
  "meta": { ... },
  "kindra": { ... },
  
  // All v3.0 fields still present
  "archetypes": { ... },
  "risk": { ... },
  "summary": { ... }
}
```

---

## How to Migrate Clients

### Step 1: Update Endpoint (Optional)

**Before (v3.0):**
```javascript
const response = await fetch('/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: analysisText })
});
```

**After (v3.1):**
```javascript
const response = await fetch('/api/v3.1/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    text: analysisText,
    preset: 'alpha',           // Optional
    profile_id: currentUserId  // Optional
  })
});
```

### Step 2: Handle New Response Fields (Optional)

**v3.0 Client (still works):**
```javascript
const { archetypes, risk, summary } = await response.json();
// Use existing fields
```

**v3.1 Client (enhanced):**
```javascript
const { 
  archetypes, 
  risk, 
  summary,
  // NEW fields
  meta,
  kindra, 
  preset_used,
  preset_config 
} = await response.json();

// Access new outputs
if (meta?.nietzsche) {
  console.log('Will to Power:', meta.nietzsche.will_to_power);
}

if (kindra?.layer1) {
  console.log('Layer 1 vectors:', kindra.layer1);
}
```

### Step 3: Implement Profile Management (Optional)

```javascript
// Create user profile
async function createProfile(userId, preferences) {
  await fetch(`/api/v3.1/profile/${userId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      preferred_preset: 'geo',
      risk_tolerance: 0.7,
      depth: 'deep'
    })
  });
}

// Use profile in analysis
async function analyzeWithProfile(text, userId) {
  const response = await fetch('/api/v3.1/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      text,
      profile_id: userId  // Automatically applies user preferences
    })
  });
  return response.json();
}
```

### Step 4: Display Preset Selection (Optional)

```javascript
// Get available presets
const response = await fetch('/api/v3.1/presets');
const { presets } = await response.json();

// Display in UI
Object.entries(presets).forEach(([name, config]) => {
  console.log(`${name}: ${config.description}`);
});

// Use selected preset
const result = await fetch('/api/v3.1/analyze', {
  method: 'POST',
  body: JSON.stringify({ 
    text: analysisText,
    preset: selectedPreset  // e.g., 'alpha', 'geo', 'safeguard', 'product'
  })
});
```

---

## Deprecated Endpoints

### Soft Deprecations

The following are still supported but discouraged:

- **Legacy `/analyze`** endpoint (use `/api/v3.1/analyze`)
- Old v2.x/v3.0 signal outputs without meta/kindra

### Deprecation Timeline

- **v3.1** (current): Fully supported
- **v3.2**: Marked as deprecated (warnings)
- **v3.4**: Begin sunset period
- **v3.6**: Potential removal (with migration notice)

---

## Example Migration Code

### Python Client

**Before (v3.0):**
```python
import requests

response = requests.post('http://api.kaldra.io/analyze', json={
    'text': 'Analysis text'
})
result = response.json()
archetypes = result.get('archetypes')
```

**After (v3.1):**
```python
import requests

# With preset
response = requests.post('http://api.kaldra.io/api/v3.1/analyze', json={
    'text': 'Analysis text',
    'preset': 'alpha',
    'profile_id': 'user_123'
})
result = response.json()

# Access new fields
meta = result.get('meta', {})
kindra = result.get('kindra', {})
preset_used = result.get('preset_used')

# Old fields still work
archetypes = result.get('archetypes')
risk = result.get('risk')
```

### React/TypeScript Client

**Updated Type Definitions:**
```typescript
interface AnalyzeV31Request {
  text: string;
  preset?: 'alpha' | 'geo' | 'safeguard' | 'product';
  profile_id?: string;
}

interface AnalyzeV31Response {
  version: string;
  request_id: string;
  timestamp: number;
  mode: string;
  degraded: boolean;
  
  // v3.1 new fields
  preset_used?: string;
  preset_config?: PresetConfig;
  meta?: MetaEngines;
  kindra?: Kindra3x48;
  
  // v3.0 legacy fields
  archetypes?: any;
  drift?: any;
  risk?: any;
  summary?: any;
}

interface MetaEngines {
  nietzsche?: {
    will_to_power: number;
    ressentiment: number;
    // ...
  };
  aurelius?: {
    stoic_acceptance: number;
    // ...
  };
  campbell?: {
    journey_stage: string;
    // ...
  };
}
```

---

## Breaking Changes

**None.** This is a fully backward-compatible release.

All v3.0 clients continue to work without modification. New fields are additive only.

---

## Recommended Adoption Steps

### Phase 1: Monitor (Immediate)
1. Deploy v3.1 backend
2. Monitor existing v3.0 clients
3. Verify no regressions

### Phase 2: Explore (Week 1-2)
1. Test new `/api/v3.1/analyze` endpoint
2. Explore available presets
3. Review enhanced signal outputs

### Phase 3: Adopt (Week 3-4)
1. Update client to use v3.1 endpoints
2. Implement preset selection UI
3. Add profile management features
4. Display meta + kindra outputs

### Phase 4: Optimize (Month 2+)
1. Collect user feedback on presets
2. Customize profile defaults
3. Build analytics on preset usage
4. Prepare for v3.2 features

---

## Support

**Questions?**
- Documentation: `/docs/api/v3_1_api_reference.md`
- Examples: `/examples/v3_1_client_examples/`
- Issues: GitHub Issues
- Email: support@4iam.ai

---

## Next Versions

### v3.2 — Temporal Mind (Q1 2026)
- Story Buffer & Arc Detection
- TW-Enriched Kindra
- Timeline Builder

### v3.3 — Multi-Stream (Q2 2026)
- Multi-source analysis
- Domain calibration

### v3.4 — Explainability (Q3 2026)
- Explanation generator
- Confidence scoring

---

**Happy migrating! 🚀**
