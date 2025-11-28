# KINDRA SCORING RULES (Sprint 1.3 — Rule-Based Engine)

## 1. Overview

This document describes the rule-based Kindra scoring engine implemented in:

- `src/kindras/scoring/rule_engine_base.py`
- `src/kindras/scoring/layer1_rules.py`
- `src/kindras/scoring/layer2_rules.py`
- `src/kindras/scoring/layer3_rules.py`
- `src/kindras/scoring/dispatcher.py`
- `src/kindras/scoring/twstate_adapter.py`

All scores are clamped to **[-1.0, 1.0]**.

## 2. Layer 1 — Cultural Macro

### Context fields used
- `country` (BR, US, JP, IN, DE, FR, CN, ...)
- `sector` (tech, finance, energy, healthcare, retail, industrial, ...)

### Country Rules

| Country | E01 (Expressiveness) | P17 (Hierarchy) | R33 (Risk) | T25 (Innovation) |
|---------|---------------------|-----------------|------------|------------------|
| **BR** (Brazil) | +0.6 | -0.2 | -0.1 | - |
| **US** | +0.3 | +0.1 | -0.3 | - |
| **JP** (Japan) | -0.4 | +0.5 | +0.2 | - |
| **IN** (India) | +0.4 | +0.3 | -0.1 | - |
| **DE** (Germany) | -0.2 | +0.2 | - | +0.3 |
| **FR** (France) | +0.3 | +0.1 | -0.1 | - |
| **CN** (China) | -0.2 | +0.6 | +0.2 | - |

### Sector Rules

| Sector | T25 (Innovation) | R33 (Risk) | P17 (Hierarchy) | Other |
|--------|------------------|------------|-----------------|-------|
| **tech** | +0.6 | -0.2 | - | - |
| **finance/banking** | - | +0.3 | +0.2 | - |
| **energy/oil_gas** | -0.1 | +0.1 | - | - |
| **healthcare/pharma** | - | +0.2 | - | G21 +0.2 |
| **retail/consumer** | - | - | - | E01 +0.2, S09 +0.1 |
| **industrial/manufacturing** | +0.2 | +0.1 | - | - |

### Example

```python
from src.kindras.scoring.layer1_rules import KindraLayer1CulturalMacroRules

scorer = KindraLayer1CulturalMacroRules()
context = {"country": "BR", "sector": "tech"}
scores = scorer.score(context, {})

# Produces:
# E01 (Expressiveness) → +0.6
# P17 (Hierarchy) → -0.2
# T25 (Innovation) → +0.6
# R33 (Risk aversion) → -0.3 (cumulative)
```

## 3. Layer 2 — Semiotic / Media

### Context fields used
- `media_tone` (sensational, analytical, neutral, opinionated, editorial, ...)
- `channel` (social, tv_news, newspaper, radio, podcast, blog, ...)
- `sentiment` (positive, negative)
- `intensity` (0.0–1.0)

### Tone Rules

| Tone | M12 (Sensationalism) | E01 (Expressiveness) | T25 (Technical) | S09 (Tension) |
|------|---------------------|---------------------|-----------------|---------------|
| **sensational/alarmist** | +0.7 | +0.3 | - | - |
| **analytical/neutral** | -0.3 | - | +0.2 | - |
| **opinionated/editorial** | - | +0.2 | - | +0.2 |

### Channel Rules

| Channel | M12 | E01 | R33 | T25 | S09 |
|---------|-----|-----|-----|-----|-----|
| **social/twitter/tiktok/instagram** | - | +0.3 | -0.1 | - | - |
| **newspaper/print** | -0.1 | - | - | - | - |
| **tv_news/cable_news** | +0.2 | - | - | - | - |
| **radio** | +0.1 | - | - | - | - |
| **podcast** | - | - | - | +0.2 | +0.2 (if opinionated) |
| **blog** | - | +0.1 | - | - | - |

### Sentiment & Intensity

- **Positive sentiment**: E01 += 0.2 × intensity
- **Negative sentiment**: R33 += 0.2 × intensity
- **High intensity (≥0.7)**: S09 += 0.4

### Example

```python
from src.kindras.scoring.layer2_rules import KindraLayer2SemioticMediaRules

scorer = KindraLayer2SemioticMediaRules()
context = {
    "media_tone": "sensational",
    "channel": "social",
    "sentiment": "negative",
    "intensity": 0.9
}
scores = scorer.score(context, {})

# Produces:
# M12 (sensationalism) → +0.7
# S09 (semiotic tension) → +0.4
# E01 → +0.6 (cumulative)
# R33 → +0.18 (0.2 × 0.9)
```

## 4. Layer 3 — Structural / Systemic

### Context fields used
- `institutional_strength` (0.0–1.0)
- `power_concentration` (0.0–1.0)
- `regulatory_stability` (0.0–1.0)

### Rules

| Parameter | Threshold | Vector | Effect |
|-----------|-----------|--------|--------|
| **institutional_strength** | ≥0.7 | G21 | +0.5 |
| **institutional_strength** | ≤0.3 | G21 | -0.4 |
| **power_concentration** | ≥0.7 | P17 | +0.4 |
| **power_concentration** | ≤0.3 | P17 | -0.3 |
| **regulatory_stability** | ≥0.7 | R33 | -0.3 |
| **regulatory_stability** | ≤0.3 | R33 | +0.4 |

### Example

```python
from src.kindras.scoring.layer3_rules import KindraLayer3StructuralSystemicRules

scorer = KindraLayer3StructuralSystemicRules()
context = {
    "institutional_strength": 0.9,
    "power_concentration": 0.8,
    "regulatory_stability": 0.7
}
scores = scorer.score(context, {})

# Produces:
# G21 (guardian/order) → +0.5
# P17 (hierarchy/control) → +0.4
# R33 (structural risk) → -0.3
```

## 5. TWState Integration

The adapter `src/kindras/scoring/twstate_adapter.py` runs all three layers and maps:

- **Layer 1** → **Plane 3** (Cultural Macro)
- **Layer 2** → **Plane 6** (Semiotic / Media)
- **Layer 3** → **Plane 9** (Structural / Systemic)

This TWState is ready to be consumed by the TW369 engine, completing the bridge between Kindra scoring and Δ144 dynamical evolution.

### Example

```python
from src.kindras.scoring.twstate_adapter import build_twstate_from_context

context = {
    "country": "BR",
    "sector": "tech",
    "media_tone": "sensational",
    "channel": "social",
    "sentiment": "negative",
    "intensity": 0.9,
    "institutional_strength": 0.9,
    "power_concentration": 0.8,
    "regulatory_stability": 0.2
}

tw_state = build_twstate_from_context(context)

# tw_state.plane3_cultural_macro = {'E01': 0.6, 'P17': -0.2, 'R33': -0.3, 'T25': 0.6}
# tw_state.plane6_semiotic_media = {'M12': 0.7, 'E01': 0.6, 'R33': 0.18, 'S09': 0.4}
# tw_state.plane9_structural_systemic = {'G21': 0.5, 'P17': 0.4, 'R33': 0.4}
```

## 6. Tuning Guide

### Increasing Sensitivity

To make a rule more sensitive to context, **increase the delta values**:

```python
# Before:
scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.3)

# After (more sensitive):
scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.6)
```

### Making Rules More Conservative

To make a rule more conservative, **reduce delta values**:

```python
# Before:
scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.4)

# After (more conservative):
scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.2)
```

### Adding New Countries/Sectors/Channels

Simply add new `elif` blocks in the respective rule files:

```python
# In layer1_rules.py
elif country == "MX":
    scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.5)
    scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.2)
```

### Testing Changes

Always add tests when modifying rules:

```python
def test_layer1_scoring_new_country():
    scorer = KindraLayer1CulturalMacroRules()
    context = {"country": "MX"}
    scores = scorer.score(context, {})
    
    assert "E01" in scores
    assert scores["E01"] > 0
```

## 7. Coverage Summary

### Layer 1
- **7 countries**: BR, US, JP, IN, DE, FR, CN
- **6 sectors**: tech, finance, energy, healthcare, retail, industrial

### Layer 2
- **4 tones**: sensational, analytical, opinionated, neutral
- **7 channels**: social, print, TV, radio, podcast, blog, newspaper

### Layer 3
- **3 parameters**: institutional_strength, power_concentration, regulatory_stability
- **Threshold-based**: High (≥0.7), Low (≤0.3), Neutral (0.3-0.7)

## 8. Future Enhancements

### Option B (LLM-Based)
- Replace rule-based scoring with LLM inference
- Use cultural database for few-shot examples
- Maintain score clamping and structure

### Option C (Hybrid)
- Populate cultural database from historical data
- Use LLM for edge cases not covered by rules
- Fall back to rules when LLM unavailable

### Expanded Coverage
- Add more countries (50+ target)
- Add more sectors (20+ target)
- Add more media channels (streaming, forums, etc.)
- Add temporal/seasonal modifiers
