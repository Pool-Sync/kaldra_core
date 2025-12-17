# Module Card Template

> **Module**: `{{MODULE_NAME}}`  
> **Engine**: [[{{ENGINE_NAME}}/ENGINE_OVERVIEW|{{ENGINE_NAME}}]]  
> **Path**: `{{PATH}}`  
> **Node ID**: `{{NODE_ID}}`

---

## What It Is

{{DESCRIPTION - 10+ paragraphs covering purpose, design philosophy, and role in the system}}

---

## How It Works

### Step-by-Step Mechanics

1. **Step 1**: {{Description}}
2. **Step 2**: {{Description}}
3. **Step 3**: {{Description}}

### Mermaid Diagram

```mermaid
flowchart LR
    INPUT[Input] --> MODULE[{{MODULE_NAME}}]
    MODULE --> OUTPUT[Output]
```

---

## With What It Works

### Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `{{dep}}` | depends_on | {{purpose}} |

### Configurations

| Config | Path | Purpose |
|--------|------|---------|
| `{{config}}` | `{{path}}` | {{purpose}} |

### Schemas

| Schema | Path | Purpose |
|--------|------|---------|
| `{{schema}}` | `{{path}}` | {{purpose}} |

### Runtime

- **Environment Variables**: {{list}}
- **External Services**: {{list}}

---

## Connections

### Graph Relations

```csv
from,relation,to,notes
{{node_id}},depends_on,{{other}},{{notes}}
```

### Obsidian Links

- Depends on: [[{{link}}]]
- Feeds: [[{{link}}]]
- Tests: [[{{link}}]]

---

## Public Surface

| Item | Type | Description |
|------|------|-------------|
| `{{class/function}}` | {{type}} | {{description}} |

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

| Test File | Coverage | Notes |
|-----------|----------|-------|
| `{{test}}` | {{coverage}} | {{notes}} |

---

## Next Steps

1. [ ] {{Next step}}
2. [ ] {{Next step}}

---

## Related

- [[{{ENGINE_NAME}}/ENGINE_OVERVIEW]]
- [[MOC_HOME]]
