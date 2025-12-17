# 🏠 KALDRA Docs Vault v2 — Map of Content

> **Version**: v2.0 | **Generated**: 2024-12-17 | **Vault**: Obsidian-First

Welcome to the KALDRA documentation vault. This is your starting point for navigating the entire system.

---

## 🗺️ Quick Navigation

### Start Here
- [[GRAPH_VOCABULARY]] — Relation types used across the vault
- [[REPO_MAP]] — Repository domain structure
- [[GREY_ZONES]] — Ambiguous areas needing resolution
- [[ENGINE_INVENTORY]] — Full engine inventory (discovery)
- [[MODULE_INVENTORY]] — Full module inventory (discovery)
- [[DOMAIN_MAP]] — Domain groupings (discovery)

### Architecture
- [[SYSTEM_OVERVIEW]] — How the system flows
- [[TESTING_MAP]] — Test coverage per engine
- [[DUPLICATES_AND_CONFLICTS]] — Known duplicates

---

## ⚙️ Engine Overviews

| Engine | Path | Description | Overview |
|--------|------|-------------|----------|
| UnifiedKernel | `src/unification/` | v3.0 entry point | [[UnifiedKernel/ENGINE_OVERVIEW]] |
| Core | `src/core/` | v2 master engine | [[Core/ENGINE_OVERVIEW]] |
| TW369 | `src/tw369/` | Tracy-Widom drift | [[TW369/ENGINE_OVERVIEW]] |
| Kindra | `src/kindras/` | 3×48 cultural scoring | [[Kindra/ENGINE_OVERVIEW]] |
| Delta144 | `src/archetypes/` | 12×12 archetypes | [[Delta144/ENGINE_OVERVIEW]] |
| Meta | `src/meta/` | Philosophical engines | [[Meta/ENGINE_OVERVIEW]] |
| Story | `src/story/` | Narrative/temporal | [[Story/ENGINE_OVERVIEW]] |
| Explainability | `src/explainability/` | Human-readable output | [[Explainability/ENGINE_OVERVIEW]] |
| Bias | `src/bias/` | Bias detection | [[Bias/ENGINE_OVERVIEW]] |
| Tau | `src/tau/` | Epistemic limiter | [[Tau/ENGINE_OVERVIEW]] |
| Safeguard | `src/safeguard/` | Safety/risk | [[Safeguard/ENGINE_OVERVIEW]] |

---

## 📊 Graphs

- [[EDGES_V2.csv]] — Stable node-id dependency graph
- [[EDGES_DRAFT.csv]] — Original discovery edges

---

## 📁 Templates

- [[MODULE_CARD_TEMPLATE]] — Template for module cards
- [[ENGINE_OVERVIEW_TEMPLATE]] — Template for engine overviews

---

## 🔍 How to Use This Vault

1. **Start with [[SYSTEM_OVERVIEW]]** to understand the overall flow
2. **Explore engines** via the table above
3. **Dive into modules** from each engine's overview
4. **Use the graph** to understand dependencies
5. **Check [[GREY_ZONES]]** for areas needing clarification

---

## Future Implementations

1. Auto-generate MOC from file structure
2. Add search index for cross-references
3. Create interactive graph visualization

---

## Enhancements (Short/Medium Term)

1. Add tags for filtering (e.g., `#engine`, `#module`, `#api`)
2. Create changelog for documentation updates
3. Add version badges to each document

---

## Research Track (Long Term)

1. AI-assisted documentation updates
2. Automatic outdated-doc detection
3. Integration with code comments

---

## Known Limitations

1. Manual sync required between code and docs
2. No automatic validation of links
3. Some module cards are tier-2 index cards, not full docs

---

## Testing

| Aspect | Status |
|--------|--------|
| All links valid | ⏳ Pending |
| Templates complete | ✅ Done |
| All engines documented | ✅ Done |

---

## Next Steps

1. [ ] Review all engine overviews
2. [ ] Validate Obsidian link resolution
3. [ ] Add custom CSS for vault styling
4. [ ] Create dataview queries for dynamic lists

---

## Related

- [[SYSTEM_OVERVIEW]]
- [[REPO_MAP]]
- [[GRAPH_VOCABULARY]]
