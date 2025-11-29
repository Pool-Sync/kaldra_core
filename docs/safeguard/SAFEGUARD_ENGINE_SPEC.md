# KALDRA Safeguard Engine Specification (v2.8)

**Version:** 1.0 (KALDRA v2.8)
**Status:** Active
**Component:** Safety & Ethics Layer

## Overview

The **Safeguard Engine** is the final defense layer of the KALDRA architecture. While the Tau Layer manages epistemic reliability (truth/confidence), the Safeguard Engine manages **narrative and semantic safety** (harm/ethics). It evaluates the final system state to detect and mitigate risks such as toxicity, manipulation, extremism, and narrative entrapment (shadow loops).

## Core Concepts

### Safeguard Signal
The output of the engine, containing:
- **Final Risk Level**: LOW, MID, HIGH, CRITICAL.
- **Risk Score**: 0.0 - 1.0.
- **Mitigation Actions**: Specific interventions (e.g., BLOCK_OUTPUT, DAMPEN_DRIFT).
- **Risk Breakdown**: Detailed scores for bias, polarity, drift, journey, and meta risks.

### Risk Taxonomy

| Risk Category | Description |
| :--- | :--- |
| **Toxicity** | Harmful, offensive, or dangerous content. |
| **Manipulation** | Attempts to deceive or coercively influence. |
| **Polarization** | Extreme division or "us vs. them" framing. |
| **Extremism** | Radicalization of archetypal values (e.g., Ruler → Tyrant). |
| **Distortion** | Severe warping of reality or facts. |
| **Shadow Loops** | Narrative entrapment in negative archetypal states (e.g., stuck in "The Void"). |

## Architecture

### Components

- **`SafeguardEngine`**: Main evaluator.
- **`SafeguardRiskModel`**: Aggregates risk signals from Tau, TW369, Meta-Engines, and Story Engine.
- **`SafeguardPolicy`**: Maps risk levels to mitigation actions.

### Evaluation Logic

The Safeguard Engine aggregates inputs from the entire pipeline:

1.  **Tau State**: Epistemic confidence and detected anomalies.
2.  **Drift State**: Velocity and severity of narrative change.
3.  **Polarity Scores**: Extremity of dimensional tensions.
4.  **Meta-States**: Pathological philosophical states (e.g., Nihilism).
5.  **Journey State**: Progress and position in the hero's journey.

`RiskScore = WeightedAvg(Bias, Polarity, Drift, Journey, Meta)`

## Policies & Mitigation

### Actions

- **`FLAG_RISK`**: Mark the signal for review/logging.
- **`DAMPEN_DRIFT`**: Force reduction of temporal drift in the next cycle.
- **`SUPPRESS_POLARITY`**: Pull polarities back towards equilibrium.
- **`BLOCK_OUTPUT`**: Prevent the signal from being emitted (critical safety).
- **`FREEZE_STATE`**: Lock the narrative state to prevent further degradation.
- **`ALERT_ADMIN`**: High-priority alert.

### Thresholds

- **LOW (< 0.3)**: No action.
- **MID (0.3 - 0.6)**: Flag & Dampen.
- **HIGH (0.6 - 0.8)**: Suppress & Strong Dampen.
- **CRITICAL (> 0.8)**: Block & Freeze.

## Configuration

Configuration is stored in `schema/safeguard/safeguard_risk_rules.json` and `schema/safeguard/safeguard_journey_map.json`.
