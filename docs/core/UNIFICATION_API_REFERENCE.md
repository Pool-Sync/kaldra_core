# KALDRA v3.0 — API Reference

**Version:** 3.0.0  
**Date:** November 30, 2025

---

## Quick Start

```python
from src.unification import UnifiedKaldra

# Initialize
kaldra = UnifiedKaldra()

# Analyze text
result = kaldra.analyze("Your text here")

# Access results
print(result['archetypes']['delta144_state']['archetype']['label'])
print(result['risk']['final_risk'])
```

---

## UnifiedKaldra Class

### Constructor

```python
UnifiedKaldra(auto_load: bool = True)
```

**Parameters:**
- `auto_load` (bool, optional): Automatically load engines on initialization. Default: `True`

**Example:**
```python
kaldra = UnifiedKaldra()  # Auto-load engines
kaldra = UnifiedKaldra(auto_load=False)  # Manual loading
```

---

### analyze()

Analyze a single text input.

```python
analyze(
    text: str,
    mode: str = "full",
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `text` (str): Text to analyze
- `mode` (str, optional): Execution mode. Default: `"full"`
  - `"signal"` - Fast, core pipeline only
  - `"story"` - Full temporal analysis
  - `"full"` - Complete analysis (default)
  - `"safety-first"` - Strict safety checks
  - `"exploratory"` - Maximum depth
- `options` (dict, optional): Additional configuration options

**Returns:**
- `Dict[str, Any]`: Complete analysis signal in JSON format

**Example:**
```python
result = kaldra.analyze(
    "The company announced record profits.",
    mode="full"
)

print(result['version'])  # "3.0"
print(result['summary']['confidence'])  # 0.85
```

---

### analyze_batch()

Analyze multiple texts in batch.

```python
analyze_batch(
    texts: List[str],
    mode: str = "full",
    options: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]
```

**Parameters:**
- `texts` (List[str]): List of texts to analyze
- `mode` (str, optional): Execution mode. Default: `"full"`
- `options` (dict, optional): Additional configuration options

**Returns:**
- `List[Dict[str, Any]]`: List of analysis signals

**Example:**
```python
texts = [
    "Innovation drives progress.",
    "Uncertainty creates opportunity.",
    "Leadership requires vision."
]

results = kaldra.analyze_batch(texts, mode="signal")

for i, result in enumerate(results):
    print(f"Text {i+1}: {result['summary']['confidence']}")
```

---

### get_version()

Get KALDRA version.

```python
get_version() -> str
```

**Returns:**
- `str`: Version string (e.g., "3.0.0")

**Example:**
```python
version = kaldra.get_version()
print(version)  # "3.0.0"
```

---

### list_modules()

List all loaded modules.

```python
list_modules() -> List[str]
```

**Returns:**
- `List[str]`: List of module names

**Example:**
```python
modules = kaldra.list_modules()
print(modules)  # ['embeddings', 'archetypes', 'bias', 'tau', 'safeguard']
```

---

## Signal Format

### Top-Level Structure

```json
{
  "version": "3.0",
  "request_id": "uuid-string",
  "timestamp": 1234567890.0,
  "mode": "full",
  "input": {...},
  "kindra": {...},
  "archetypes": {...},
  "drift": {...},
  "meta": {...},
  "story": {...},
  "risk": {...},
  "summary": {...}
}
```

---

### input

Input processing results.

```json
{
  "text": "Original input text",
  "bias_score": 0.1,
  "tau_input": {
    "tau_score": 0.9,
    "tau_risk": "LOW",
    "tau_modifiers": {},
    "tau_actions": [],
    "details": {}
  }
}
```

**Fields:**
- `text` (str): Original input text
- `bias_score` (float): Bias detection score [0, 1]
- `tau_input` (object): Tau input phase state

---

### archetypes

Archetypal analysis results.

```json
{
  "delta12": {
    "values": {
      "A01_INNOCENT": 0.05,
      "A02_ORPHAN": 0.08,
      ...
    }
  },
  "delta144_state": {
    "archetype": {
      "id": "A07_RULER",
      "label": "The Ruler",
      "essence": "Control and Order"
    },
    "state": {
      "id": "A07_S05",
      "label": "Ruler - Contractive - Plane 6",
      "profile": "CONTRACTIVE",
      "description": "..."
    },
    "active_modifiers": [...],
    "scores": {...},
    "polarity_scores": {...}
  },
  "polarity_scores": {
    "POL_LIGHT_SHADOW": 0.6,
    "POL_ORDER_CHAOS": 0.7,
    ...
  }
}
```

**Fields:**
- `delta12` (object): 12-dimensional archetype vector
- `delta144_state` (object): Complete archetypal state
  - `archetype` (object): Identified archetype (1 of 12)
  - `state` (object): Specific state (1 of 144)
  - `active_modifiers` (array): Active modifiers
  - `polarity_scores` (object): 46 polarity dimensions
- `polarity_scores` (object): Polarity scores

---

### risk

Safety and risk analysis results.

```json
{
  "tau_output": {
    "tau_score": 0.85,
    "tau_risk": "LOW",
    "tau_modifiers": {},
    "tau_actions": [],
    "details": {}
  },
  "safeguard": {
    "bias": {"score": 0.1},
    "polarity_risk": {"score": 0.2},
    "drift_risk": {"score": 0.1},
    "journey_risk": {"score": 0.0},
    "meta_risk": {"score": 0.0},
    "final_risk": "LOW",
    "risk_score": 0.15,
    "mitigation_actions": []
  },
  "final_risk": "LOW",
  "risk_score": 0.15
}
```

**Fields:**
- `tau_output` (object): Tau output phase state
- `safeguard` (object): Safeguard evaluation
  - `final_risk` (str): Risk classification (LOW/MID/HIGH/CRITICAL)
  - `risk_score` (float): Numerical risk score [0, 1]
  - `mitigation_actions` (array): Recommended actions
- `final_risk` (str): Overall risk level
- `risk_score` (float): Overall risk score

---

### summary

Execution summary and metadata.

```json
{
  "confidence": 0.85,
  "routing": "full",
  "degraded": false
}
```

**Fields:**
- `confidence` (float): Overall confidence score [0, 1]
- `routing` (str): Execution mode used
- `degraded` (bool): Whether execution was degraded

---

## Execution Modes

### signal

**Fast mode** - Core pipeline only.

```python
result = kaldra.analyze(text, mode="signal")
```

**Characteristics:**
- ⚡ Fastest execution (~100ms)
- 🎯 Core analysis only
- ❌ Skips Story and Meta stages
- ✅ Best for API responses

---

### full

**Complete mode** - All stages (default).

```python
result = kaldra.analyze(text, mode="full")
```

**Characteristics:**
- ⚖️ Balanced execution (~300ms)
- 🎯 All stages executed
- ✅ Complete analysis
- ✅ Default mode

---

### story

**Temporal mode** - Emphasizes narrative analysis.

```python
result = kaldra.analyze(text, mode="story")
```

**Characteristics:**
- 📖 Story-focused (~400ms)
- 🎯 All stages executed
- ✅ Temporal coherence
- ✅ Narrative arcs

---

### safety-first

**Safety mode** - Strict safety checks.

```python
result = kaldra.analyze(text, mode="safety-first")
```

**Characteristics:**
- 🛡️ Safety-focused (~350ms)
- 🎯 All stages executed
- ✅ Strict safety checks
- ✅ High-risk content

---

### exploratory

**Deep mode** - Maximum depth.

```python
result = kaldra.analyze(text, mode="exploratory")
```

**Characteristics:**
- 🔬 Maximum detail (~500ms)
- 🎯 All stages executed
- ✅ Deep analysis
- ✅ Research use cases

---

## Error Handling

### Degraded Mode

When failures occur, the system enters **degraded mode**:

```python
result = kaldra.analyze(text)

if result['summary']['degraded']:
    print("Warning: Partial results")
    print(f"Confidence: {result['summary']['confidence']}")
    # Still usable, just incomplete
else:
    print("Complete analysis")
```

**Characteristics:**
- ✅ Always returns valid signal
- ⚠️ `degraded` flag set to `true`
- 📉 Reduced confidence score
- 🔄 Partial results available

---

## Best Practices

### 1. Choose the Right Mode

```python
# Fast API responses
result = kaldra.analyze(text, mode="signal")

# Complete analysis
result = kaldra.analyze(text, mode="full")

# High-risk content
result = kaldra.analyze(text, mode="safety-first")
```

---

### 2. Check Degraded Status

```python
result = kaldra.analyze(text)

if result['summary']['degraded']:
    logger.warning("Degraded execution")
    # Handle partial results
```

---

### 3. Use Batch Processing

```python
# Efficient batch processing
texts = [...]
results = kaldra.analyze_batch(texts, mode="signal")
```

---

### 4. Access Nested Fields Safely

```python
# Safe access
archetype_label = result.get('archetypes', {}) \
    .get('delta144_state', {}) \
    .get('archetype', {}) \
    .get('label', 'Unknown')
```

---

## Examples

### Example 1: Basic Analysis

```python
from src.unification import UnifiedKaldra

kaldra = UnifiedKaldra()
result = kaldra.analyze("Innovation drives progress.")

print(f"Archetype: {result['archetypes']['delta144_state']['archetype']['label']}")
print(f"Risk: {result['risk']['final_risk']}")
print(f"Confidence: {result['summary']['confidence']}")
```

---

### Example 2: Batch Processing

```python
texts = [
    "The market is uncertain.",
    "Leadership requires vision.",
    "Innovation creates opportunity."
]

results = kaldra.analyze_batch(texts, mode="signal")

for i, result in enumerate(results):
    arch = result['archetypes']['delta144_state']['archetype']['label']
    print(f"{i+1}. {texts[i]} → {arch}")
```

---

### Example 3: Safety Check

```python
high_risk_text = "..."

result = kaldra.analyze(high_risk_text, mode="safety-first")

if result['risk']['final_risk'] in ['HIGH', 'CRITICAL']:
    print("⚠️ High risk detected!")
    print(f"Actions: {result['risk']['safeguard']['mitigation_actions']}")
```

---

## Conclusion

The KALDRA v3.0 API provides:
- ✅ Simple, consistent interface
- ✅ Multiple execution modes
- ✅ Graceful error handling
- ✅ Complete signal format
- ✅ Production-ready

**One API. Many possibilities.** 🚀
