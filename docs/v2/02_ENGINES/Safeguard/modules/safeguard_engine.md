# 📦 Safeguard Engine Module

> **Module**: `SafeguardEngine`  
> **Engine**: [[../ENGINE_OVERVIEW|Safeguard]]  
> **Path**: `packages/engine/kaldra_engine/safeguard/safeguard_engine.py`  
> **Node ID**: `mod_safeguard_engine`

---

## What It Is

The `SafeguardEngine` is the final and most authoritative gatekeeper in the `UnifiedKernel` pipeline. It essentially functions as a firewall for AI outputs, enforcing "hard" safety constraints that cannot be overridden by other engines.

Unlike `BiasDetector` (statistical/subtle) or `TauLayer` (epistemic/truth), `SafeguardEngine` focuses on **danger prevention**. It scans for:
- PII (Personally Identifiable Information) leakage
- Violation of content policies (violence, hate speech)
- Prompt injection / Jailbreak attempts
- High-stakes misinformation (medical/legal advice)

The engine uses a **Risk Score** model (0-100). Every output is assigned a risk score.
- 0-20: Green (Safe)
- 21-50: Yellow (Caution - append warnings)
- 51-80: Orange (Restricted - redact/modify)
- 81-100: Red (Block - refuse execution)

It has **Audit capability**. Every decision made by the Safeguard engine is logged to a secure, immutable audit trail (separate from standard logs) for compliance review.

The engine supports **intervention**. It doesn't just say "No". It can:
- **Redact**: Mask PII (`[REDACTED]`)
- **Truncate**: Cut off dangerous generation
- **Refuse**: Return a standard refusal message
- **Annotate**: Add a disclaimer to the output

Configuration is policy-driven. The `safety-first` execution mode sets thresholds extremely low. `exploratory` mode raises them for research tasks but maintains "Red" blocks.

---

## How It Works

### Step-by-Step Mechanics

1. **Input Inspection**: Scan prompt for injection patterns
2. **Wait for Pipeline**: Let other engines run (to inspect their *outputs*)
3. **Output Inspection**: Scan generated text/signals for violations
4. **PII Scan**: Regex/NER checks for email, phone, SSN
5. **Policy Check**: Compare risk vectors against active policy
6. **Intervention**: Apply Redact/Block/Warn logic
7. **Audit Log**: Record decision
8. **Final Release**: Allow output to pass to user

### Mermaid Diagram

```mermaid
flowchart TB
    OUTPUT[Generated Output] --> PII[PII Scanner]
    OUTPUT --> POLICY[Policy Matcher]
    OUTPUT --> RISK[Risk Model]
    
    PII & POLICY & RISK --> SCORE[Risk Score (0-100)]
    
    SCORE --> DECISION{Decision}
    
    DECISION -->|0-20| PASS[Pass]
    DECISION -->|21-50| WARN[Append Warning]
    DECISION -->|51-80| REDACT[Redact/Modify]
    DECISION -->|81+| BLOCK[Block]
    
    PASS & WARN & REDACT & BLOCK --> AUDIT[Audit Log]
    AUDIT --> FINAL[Final Response]
```

---

## With What It Works

### Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `safeguard_policy.py` | uses | Policy rules |
| `safeguard_risk_model.py` | uses | Scoring logic |

### Configurations

| Config | Path | Purpose |
|--------|------|---------|
| (Empty) | `schema/safeguard/` | ⚠️ Needs schema |

---

## Public Surface

| Item | Type | Description |
|------|------|-------------|
| `SafeguardEngine` | class | Main class |
| `assess_safety(output)` | method | Run checks |
| `enforce(assessment)` | method | Apply intervention |

---

## Future Implementations

1. Real-time PII masking (streaming)
2. Image safety scanning (for visual output)
3. Regulatory compliance export (GDPR/EU AI Act)

---

## Enhancements (Short/Medium Term)

1. **Add Configuration Schema** (Critical)
2. "Sandbox" mode for testing unsafe prompts safely
3. Granular error codes for refusals

---

## Research Track (Long Term)

1. Constituitonal AI (AI self-correction)
2. Formal verification of safety properties
3. Robustness against adversarial attacks

---

## Known Limitations

1. **Low Test Coverage**
2. **Missing Schema**
3. Regex-based PII is brittle

---

## Testing

| Test File | Coverage | Notes |
|-----------|----------|-------|
| `tests/safeguard/` | ⚠️ Low | Critical gap |

---

## Next Steps

1. [ ] **Create Schema**
2. [ ] Write tests
3. [ ] Improve PII detection

---

## Related

- [[../ENGINE_OVERVIEW]]
- [[../Tau/ENGINE_OVERVIEW]]
