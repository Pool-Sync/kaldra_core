# Engine Overview Template

> **Engine**: `{{ENGINE_NAME}}`  
> **Path**: `{{PATH}}`  
> **Node ID**: `engine_{{engine_id}}`  
> **Status**: {{Active/Partial/Stub}}

---

## What It Is

{{Brief description of the engine - purpose, role in KALDRA}}

---

## Repo Paths & Entry Points

| Component | Path | Description |
|-----------|------|-------------|
| Main Directory | `{{path}}` | {{description}} |
| Entry Point | `{{entry}}` | {{description}} |

---

## Core Modules

| Module | Path | Purpose | Module Card |
|--------|------|---------|-------------|
| {{module}} | `{{path}}` | {{purpose}} | [[modules/{{MODULE_ID}}]] |

---

## Flow Diagram

```mermaid
flowchart TB
    INPUT[Input] --> ENGINE[{{ENGINE_NAME}}]
    ENGINE --> OUTPUT[Output]
```

---

## With What It Works

### Dependencies

| Dependency | Engine | Relation |
|------------|--------|----------|
| [[{{engine}}]] | {{engine}} | depends_on |

### Configurations

| Config | Path |
|--------|------|
| `{{config}}` | `{{path}}` |

### Schemas

| Schema | Path |
|--------|------|
| `{{schema}}` | `{{path}}` |

### Runtime

- **Environment Variables**: {{list}}
- **External Services**: {{list}}

---

## Module Cards

- [[modules/{{MODULE_1}}|{{Module 1}}]]
- [[modules/{{MODULE_2}}|{{Module 2}}]]

---

## Future Implementations

1. {{Future implementation}}
2. {{Future implementation}}

---

## Enhancements (Short/Medium Term)

1. {{Enhancement}}
2. {{Enhancement}}

---

## Research Track (Long Term)

1. {{Research topic}}
2. {{Research topic}}

---

## Known Limitations

1. {{Limitation}}
2. {{Limitation}}

---

## Testing

| Test Directory | Files | Coverage |
|----------------|-------|----------|
| `{{test_dir}}` | {{count}} | {{coverage}} |

---

## Next Steps

1. [ ] {{Next step}}
2. [ ] {{Next step}}

---

## Related

- [[MOC_HOME]]
- [[SYSTEM_OVERVIEW]]
- [[DOMAIN_MAP_V2]]
