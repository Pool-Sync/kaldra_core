# 📦 Painlevé Subsystem

> **Subsystem**: `painleve/`  
> **Engine**: [[../ENGINE_OVERVIEW|TW369]]  
> **Path**: `src/tw369/painleve/`  
> **Node ID**: `mod_tw369_painleve_subsystem`

---

## What It Is

The Painlevé Subsystem provides advanced mathematical machinery for calculating Tracy-Widom distributions using **Painlevé II transcendents**. This is the deep mathematical core of the TW369 engine, enabling precise calculation of edge statistics in random matrix theory.

While the main TW369 engine often uses pre-computed tables or approximations for speed (Models A/B), the Painlevé subsystem allows for *exact* calculation of the Hastings-McLeod solution to the Painlevé II differential equation:

$$ q''(s) = s q(s) + 2 q(s)^3 $$

This equation governs the cumulative distribution function of the Tracy-Widom distribution ($F_2$).

The subsystem includes numerical solvers (`solver.py`) to integrate this equation, handling the delicate boundary conditions required ($q(s) \sim \text{Ai}(s)$ as $s \to \infty$).

It also provides `asymptotics.py` for calculating tail behaviors where numerical integration is unstable.

This subsystem is used when `drift_model="D"` (Stochastic/Exact) is selected in the configuration. It is computationally expensive but mathematically rigorous.

---

## Directory Contents

| File | Purpose |
|------|---------|
| `__init__.py` | Package initialization |
| `solver.py` | Painlevé II numerical solver |
| `functions.py` | Airy functions & kernels |
| `asymptotics.py` | Asymptotic expansions |
| `tables.py` | Pre-computed lookups |

---

## Architecture

```mermaid
flowchart TB
    REQ[Request Exact TW] --> SOLVER[Painlevé Solver]
    SOLVER --> ODE[Integrate ODE]
    ODE --> BOUND[Check Boundary]
    BOUND --> Q[q(s) Solution]
    Q --> INT[Integrate Kernel]
    INT --> F2[F2 Distribution]
```

---

## With What It Works

### Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `scipy.integrate` | uses | ODE integration |
| `numpy` | uses | Vector math |

---

## Future Implementations

1. GPU-accelerated solvers
2. Painlevé V support (for other ensembles)
3. Fredholm determinant calculation

---

## Enhancements (Short/Medium Term)

1. Cache solver results
2. Add precision configuration
3. Visualize q(s) solution

---

## Research Track (Long Term)

1. Universality classes beyond TW
2. Riemann-Hilbert problems
3. Integrable systems integration

---

## Known Limitations

1. **Slow**: Solver takes ms to seconds
2. **Unstable**: Sensitive to initial conditions
3. **Complex**: High mathematical barrier

---

## Testing

| Test File | Coverage | Notes |
|-----------|----------|-------|
| `tests/tw369/` | 🔶 Partial | Covered in advanced tests |

---

## Next Steps

1. [ ] Optimize solver
2. [ ] Add caching
3. [ ] Improve docs

---

## Related

- [[../ENGINE_OVERVIEW]]
- [[tw369_integrator]]
- [[tracy_widom]]
