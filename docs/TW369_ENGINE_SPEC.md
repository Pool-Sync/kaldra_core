

## Schema Definitions

### TWState Schema
Referenced from `schema/tw369/tw_state_schema.json`.

Defines structure of the TW369 state: planes 3, 6, 9 with score ranges [-1,1].

**Structure**:
- `plane3_cultural_macro`: Layer 1 (Cultural Macro) scores
- `plane6_semiotic_media`: Layer 2 (Semiotic/Media) scores  
- `plane9_structural_systemic`: Layer 3 (Structural/Systemic) scores
- `metadata`: Optional context information

All three planes are required fields.

### Drift Parameters Schema
Referenced from `schema/tw369/drift_parameters.json`.

Contains the mathematical constants for Modelo A:

**Tension Calculation**:
```
Tension = 0.6 · mean(|scores|) + 0.4 · sqrt(variance(scores))
```

**Severity Factor**:
```
Severity = 1 - exp(-mean_tension)
```

**Drift Gradients**:
```
g_3_6 = t6 - t3  (Plane 3 → 6)
g_6_9 = t9 - t6  (Plane 6 → 9)
g_9_3 = t3 - t9  (Plane 9 → 3, feedback)
```

**Normalization**:
```
k = max(1, |g_3_6| + |g_6_9| + |g_9_3|)
drift[plane_x_to_y] = (gradient / k) * severity
```

**Evolution**:
```
factor[plane] = 1 + drift[into_plane] * damping_factor * step_size
where damping_factor = 0.5, min_factor = 0.1
```

### Engine Config Schema
Referenced from `schema/tw369/tw369_config_schema.json`.

Defines runtime controls for TW369 drift execution:

- `enabled`: Enable/disable TW369 drift (default: true)
- `max_time_steps`: Maximum evolution steps (default: 10)
- `default_step_size`: Default temporal step size (default: 1.0)
- `use_painleve_filter`: Future Painlevé II filter flag (default: false)
- `severity_cap`: Upper bound on severity factor (default: 1.0)
- `planes`: Per-plane enable/disable overrides
- `drift_parameters_ref`: Path to drift parameters file

**Default Configuration**: `schema/tw369/tw369_default_config.json`

