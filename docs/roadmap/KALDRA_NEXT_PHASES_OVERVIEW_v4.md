# **KALDRA — Next Phases Roadmap (v4.0 Preparation)**

**Version:** Draft v1  
**Date:** December 6, 2025  
**Owner:** Pool (ChatGPT) & Nikolas  
**Scope:** Full backend + frontend + API evolution

---

## **1. Executive Summary**

This document consolidates the roadmap from KALDRA v3.3 (Explorer Integration & Story Timeline) toward **KALDRA v4.0**, the next major evolution of the symbolic intelligence platform.

**Current State (v3.3):**
- ✅ API Gateway operational with `/signals` and `/story-events` endpoints
- ✅ Explorer frontend connected to Supabase via API
- ✅ Story events timeline integrated into signal details
- ✅ Health monitoring and graceful fallback mechanisms
- ✅ Dual-mode operation (mock/real)

**Target State (v4.0):**
- Unified signal output object consolidating all KALDRA dimensions
- Real-time WebSocket engine for live signal streaming
- Advanced analytics endpoints and aggregations
- TW369 profile control plane
- Kindra scoring mode selector (rule/LLM/hybrid/adaptive)
- Narrative pattern engine and story reconstruction
- Explorer v4 with heatmaps, radars, and interactive visualizations
- Production-grade pipeline optimization and validation

**Scope:** This document governs the next **6–8 development cycles**, establishing the architectural foundation for KALDRA's evolution into a production-ready symbolic intelligence platform.

---

## **2. Architecture Overview**

### 2.1 Current Architecture (v3.3)

```
User Input (Text Stream)
    ↓
KALDRA Master Engine
    ├─ Alpha Analysis
    ├─ GEO Analysis  
    ├─ Product Analysis
    ├─ Safeguard Analysis
    └─ Unified Context
         ↓
SignalAdapter
    ├─ Signal Persistence (SignalRepository)
    └─ Story Events Persistence (StoryEventRepository)
         ↓
Supabase PostgreSQL
    ├─ public.signals
    └─ public.story_events
         ↓
FastAPI Gateway
    ├─ GET /signals
    ├─ GET /signals/{id}
    ├─ GET /story-events/by-signal/{id}
    └─ GET /health/supabase
         ↓
4iam.ai Explorer (Next.js)
    ├─ Signal List
    ├─ Signal Details
    └─ Story Timeline
```

### 2.2 Target Architecture (v4.0)

```
User Input (Multi-Source Streams)
    ↓
KALDRA Master Engine v4
    ├─ Domain Analyzers (Alpha, GEO, Product, Safeguard)
    ├─ Δ144 Mapping Engine (Learned + Fixed)
    ├─ Kindra Engine (Rule/LLM/Hybrid/Adaptive)
    ├─ TW369 Engine (Profile-Based)
    ├─ Painlevé Analyzer
    ├─ Polarity Engine
    ├─ Story Arc Classifier
    └─ **UnifiedKaldraOutput** Builder
         ↓
Persistence Layer
    ├─ UnifiedSignalRepository
    ├─ StoryEventRepository
    ├─ AnalyticsAggregator
    └─ Cache Layer (Redis)
         ↓
Supabase PostgreSQL
    ├─ public.unified_signals (JSONB rich schema)
    ├─ public.story_events
    ├─ public.analytics_snapshots
    └─ public.narrative_patterns
         ↓
API Gateway v4 (FastAPI)
    ├─ REST Endpoints
    │   ├─ /signals/{id}/full
    │   ├─ /signals/stats/*
    │   ├─ /kindra/score?mode=*
    │   └─ /tw369/run?profile=*
    └─ WebSocket Endpoints
        ├─ /ws/signals/live
        └─ /ws/story-events/live
         ↓
Explorer v4 (Next.js + D3.js)
    ├─ Signal Grid with Heatmaps
    ├─ Δ144 State Visualizer
    ├─ Kindra Vector Radar
    ├─ TW369 Drift Plot
    ├─ Polarity Spectrum
    ├─ Narrative Flow Sankey
    ├─ Archetype Journey Map
    └─ Real-Time Updates (WebSocket)
```

---

## **3. Phase 3.3 — API Gateway Expansion**

**Objective:** Enhance the API Gateway with comprehensive endpoints for full signal data, analytics, and advanced filtering.

### 3.3.1 Signal Full Data Endpoint

**Endpoint:** `GET /signals/{id}/full`

**Returns:**
```json
{
  "id": "uuid",
  "domain": "alpha",
  "title": "Signal title",
  "summary": "Description",
  "timestamp": "2025-12-06T14:30:00Z",
  
  "delta144": {
    "state": "threshold",
    "confidence": 0.87,
    "learned_contribution": 0.65,
    "fixed_contribution": 0.35
  },
  
  "kindra": {
    "mode": "hybrid",
    "dominant_kindra": "expansion",
    "weights": {"order": 0.7, "chaos": 0.3},
    "rule_score": 0.82,
    "llm_score": 0.78,
    "composite_score": 0.80
  },
  
  "tw369": {
    "profile": "stable",
    "regime": "STABLE",
    "drift_rate": 0.12,
    "tau": 0.65,
    "tw1": 0.85,
    "tw2": 0.60,
    "tw3": 0.45
  },
  
  "painleve": {
    "score": 0.23,
    "threshold_crossed": false
  },
  
  "polarities": {
    "order": 0.72,
    "chaos": 0.28,
    "expansion": 0.65,
    "contraction": 0.35
  },
  
  "story_arc": {
    "archetype": "hero_journey",
    "stage": "threshold",
    "coherence": 0.88
  },
  
  "story_events": [
    {
      "id": "event-uuid",
      "text": "Event description",
      "stream_id": "twitter",
      "delta144_state": "threshold",
      "created_at": "2025-12-06T14:30:00Z"
    }
  ],
  
  "importance": 0.85,
  "confidence": 0.87,
  "raw_payload": {...}
}
```

### 3.3.2 Cursor-Based Pagination

**Endpoint:** `GET /signals?cursor={token}&limit=20`

**Implementation:**
- Use `created_at` + `id` for stable cursors
- Return `next_cursor` in response
- Support bidirectional pagination

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJjcmVhdGVkX2F0IjoiMjAyNS0xMi0wNiIsImlkIjoidXVpZCJ9",
    "has_more": true
  }
}
```

### 3.3.3 Advanced Filtering

**Endpoint:** `GET /signals?domain=alpha&regime=CRITICAL&archetype=hero&from=2025-12-01&to=2025-12-06&min_importance=0.7`

**Query Parameters:**
- `domain`: alpha | geo | product | safeguard
- `regime`: STABLE | TURBULENT | CRITICAL
- `archetype`: Filter by dominant archetype
- `from` / `to`: Date range (ISO 8601)
- `min_importance`: Float 0.0-1.0
- `min_confidence`: Float 0.0-1.0
- `kindra`: Filter by Kindra type
- `delta144_state`: Filter by Δ144 state

### 3.3.4 Analytics Endpoints

#### Archetype Distribution
`GET /signals/stats/archetypes?from=2025-12-01&to=2025-12-06`

**Returns:**
```json
{
  "period": {"from": "...", "to": "..."},
  "archetypes": [
    {"name": "hero_journey", "count": 45, "percentage": 0.32},
    {"name": "trickster", "count": 28, "percentage": 0.20}
  ]
}
```

#### TW Regime Statistics
`GET /signals/stats/tw-regimes?domain=alpha`

**Returns:**
```json
{
  "domain": "alpha",
  "regimes": {
    "STABLE": {"count": 120, "avg_confidence": 0.85},
    "TURBULENT": {"count": 85, "avg_confidence": 0.78},
    "CRITICAL": {"count": 15, "avg_confidence": 0.92}
  }
}
```

#### Kindra Distribution
`GET /signals/stats/kindra`

**Returns:**
```json
{
  "kindras": [
    {"name": "expansion", "count": 67, "avg_weight": 0.72},
    {"name": "contraction", "count": 42, "avg_weight": 0.65}
  ]
}
```

#### Timeline Aggregation
`GET /signals/stats/timeline?interval=day&from=2025-12-01&to=2025-12-06`

**Returns:**
```json
{
  "interval": "day",
  "data": [
    {"date": "2025-12-01", "count": 24, "avg_importance": 0.67},
    {"date": "2025-12-02", "count": 31, "avg_importance": 0.72}
  ]
}
```

### 3.3.5 Error Model Refinements

**Standardized Error Response:**
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Signal with ID xyz not found",
    "details": {...},
    "timestamp": "2025-12-06T14:30:00Z"
  }
}
```

**Error Codes:**
- `RESOURCE_NOT_FOUND` (404)
- `VALIDATION_ERROR` (422)
- `RATE_LIMIT_EXCEEDED` (429)
- `DATABASE_UNAVAILABLE` (503)
- `INTERNAL_ERROR` (500)

---

## **4. Phase 3.4 — Real-Time Engine**

**Objective:** Enable live signal and event streaming to Explorer via WebSockets for real-time updates.

### 4.1 WebSocket Endpoints

#### Live Signals Stream
**Endpoint:** `ws://localhost:8000/ws/signals/live?domain=alpha`

**Query Parameters:**
- `domain`: Filter by domain (optional)
- `min_importance`: Minimum importance threshold (optional)

**Message Format:**
```json
{
  "event_type": "signal_created",
  "timestamp": "2025-12-06T14:30:00Z",
  "payload": {
    "id": "uuid",
    "domain": "alpha",
    "title": "...",
    "importance": 0.85,
    "summary": "..."
  }
}
```

#### Live Story Events Stream
**Endpoint:** `ws://localhost:8000/ws/story-events/live?signal_id={id}`

**Message Format:**
```json
{
  "event_type": "story_event_created",
  "timestamp": "2025-12-06T14:30:00Z",
  "payload": {
    "id": "event-uuid",
    "signal_id": "signal-uuid",
    "text": "Event description",
    "stream_id": "twitter"
  }
}
```

### 4.2 Event Model

**Event Types:**
- `signal_created`
- `signal_updated`
- `story_event_created`
- `analytics_updated`

**Compression:**
- Use JSON compression for large payloads
- Optional binary protocol for high-frequency updates

### 4.3 Real-Time Timeline Updates

**Implementation:**
- Explorer subscribes to `/ws/story-events/live?signal_id={id}` when detail modal is open
- New events appear in timeline automatically
- Smooth animations for new entries
- Notification badge for events arriving while modal closed

### 4.4 Scaling Considerations

**Architecture:**
- Redis Pub/Sub for message distribution
- Connection pooling (max 10k concurrent)
- Heartbeat every 30s
- Automatic reconnection with exponential backoff
- Rate limiting per connection (100 messages/min)

---

## **5. Unified Signal Output (v4.0 Core)**

**Objective:** Create a single, comprehensive output object that consolidates all KALDRA analysis dimensions.

### 5.1 New Class: `UnifiedKaldraOutput`

**Location:** `src/core/unified_output.py`

**Structure:**
```python
class UnifiedKaldraOutput:
    # Metadata
    id: str
    domain: str
    timestamp: datetime
    
    # Core Content
    title: str
    summary: str
    source_anchor: str
    source_url: Optional[str]
    
    # Δ144 Final State
    delta144_state: str
    delta144_confidence: float
    delta144_learned_weight: float
    delta144_fixed_weight: float
    
    # Kindra (Multi-Mode)
    kindra_mode: str  # rule | llm_scoring | hybrid | hybrid_adaptive
    dominant_kindra: str
    kindra_weights: Dict[str, float]
    kindra_rule_score: float
    kindra_llm_score: Optional[float]
    kindra_composite_score: float
    
    # TW369 Drift & Regime
    tw369_profile: str  # stable | conservative_v1 | exploratory_v1
    tw_regime: str  # STABLE | TURBULENT | CRITICAL
    tw_drift_rate: float
    tw_tau: float
    tw1: float
    tw2: float
    tw3: float
    
    # Painlevé
    painleve_score: float
    painleve_threshold_crossed: bool
    
    # Polarities
    polarities: Dict[str, float]  # order, chaos, expansion, contraction
    
    # Modifiers
    modifiers: List[str]
    modifier_scores: Dict[str, float]
    
    # Story Arc
    story_archetype: str
    story_stage: str
    story_coherence: float
    story_arc_summary: str
    
    # Story Events
    story_events_count: int
    story_events_summary: str
    
    # Confidence & Importance
    overall_confidence: float
    importance: float
    
    # Raw Payload
    raw_payload: Dict[str, Any]
```

### 5.2 Schema Stored in Supabase

**Option A: New Table**
```sql
CREATE TABLE public.unified_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    domain TEXT NOT NULL,
    title TEXT NOT NULL,
    summary TEXT,
    
    -- JSONB for rich structure
    delta144 JSONB,
    kindra JSONB,
    tw369 JSONB,
    painleve JSONB,
    polarities JSONB,
    story_arc JSONB,
    
    -- Scalar fields for indexing
    importance FLOAT,
    confidence FLOAT,
    tw_regime TEXT,
    
    raw_payload JSONB
);

CREATE INDEX idx_unified_signals_domain ON public.unified_signals(domain);
CREATE INDEX idx_unified_signals_tw_regime ON public.unified_signals(tw_regime);
CREATE INDEX idx_unified_signals_importance ON public.unified_signals(importance DESC);
```

**Option B: Extend Existing Table**
```sql
ALTER TABLE public.signals 
ADD COLUMN unified_output JSONB;
```

### 5.3 Endpoint Integration

**Expose through:**
- `GET /signals/{id}/full` - Returns complete UnifiedKaldraOutput
- `GET /signals` - Returns summary fields
- `POST /signals/analyze` - Creates new unified signal

---

## **6. Explorer v4 — Advanced UI**

**Objective:** Transform Explorer into a comprehensive visualization platform for KALDRA insights.

### 6.1 Heatmaps & Visualizations

#### Δ144 State Heatmap
**Component:** `ExplorerDelta144Heatmap.tsx`

**Features:**
- 12×12 grid representing Δ144 states
- Color intensity = signal count
- Hover shows state name + count
- Click filters to that state

#### Polarity Radar Chart
**Component:** `ExplorerPolarityRadar.tsx`

**Features:**
- 4-axis radar (order, chaos, expansion, contraction)
- Show aggregate across selected signals
- Animate transitions
- Compare domains side-by-side

#### Kindra Vector Visualizer
**Component:** `ExplorerKindraVisualizer.tsx`

**Features:**
- Scatter plot or force-directed graph
- Each point = signal
- Color = dominant Kindra
- Size = importance

#### TW Plane Scatter
**Component:** `ExplorerTWScatter.tsx`

**Features:**
- 2D plot: tw1 vs tw2
- Color by regime (green, yellow, red)
- Regions marked (STABLE, TURBULENT, CRITICAL)
- Interactive zoom/pan

### 6.2 Narrative Graphs

#### Archetype Flow (Sankey Diagram)
**Component:** `ExplorerArchetypeSankey.tsx`

**Features:**
- Flow from source → archetype → outcome
- Width = signal count
- Hover shows details
- Filter by domain

#### Archetype Drift Timeline
**Component:** `ExplorerArchetypeDrift.tsx`

**Features:**
- Line chart showing archetype distribution over time
- Stacked area chart alternative
- Toggle between archetypes
- Date range selector

#### TW Drift Timeline
**Component:** `ExplorerTWDriftTimeline.tsx`

**Features:**
- Multi-line chart (tw1, tw2, tw3)
- Regime zones (background colors)
- Show drift rate
- Event markers

### 6.3 Data Navigation Tools

#### Advanced Filter Panel
**Component:** `ExplorerAdvancedFilters.tsx`

**Features:**
- Domain multi-select
- Date range picker
- Importance slider (0-1)
- Confidence slider (0-1)
- Regime checkboxes
- Archetype dropdown
- Kindra selector

#### Timeline Scrubber
**Component:** `ExplorerTimelineScrubber.tsx`

**Features:**
- Horizontal timeline with zoom
- Brushing to select range
- Playback mode (animate through time)
- Speed control

---

## **7. Kindra Mode Control Plane**

**Objective:** Allow users to select and compare different Kindra scoring modes.

### 7.1 Modes

**Available Modes:**

1. **rule**: Pure rule-based scoring using fixed weights
2. **llm_scoring**: LLM-only scoring via prompt analysis
3. **hybrid**: Weighted average of rule + LLM
4. **hybrid_adaptive**: Dynamic weight adjustment based on confidence

### 7.2 Endpoint

#### Score with Mode
`POST /kindra/score?mode=hybrid_adaptive`

**Body:**
```json
{
  "text": "Input text to analyze",
  "domain": "alpha"
}
```

**Response:**
```json
{
  "mode": "hybrid_adaptive",
  "dominant_kindra": "expansion",
  "weights": {"order": 0.72, "chaos": 0.28},
  "rule_score": 0.85,
  "llm_score": 0.78,
  "composite_score": 0.82,
  "adaptive_weights": {"rule": 0.6, "llm": 0.4}
}
```

### 7.3 Frontend Selector Component

**Component:** `ExplorerKindraModeSelector.tsx`

**Features:**
- Radio buttons for mode selection
- Tooltip explaining each mode
- Visual indicator of current mode
- Re-run analysis button
- Comparison view (side-by-side results)

---

## **8. TW369 Profiles Control Plane**

**Objective:** Enable profile-based TW369 analysis for different use cases.

### 8.1 Profiles

**Available Profiles:**

1. **stable**: Conservative thresholds, high tau (0.75)
2. **conservative_v1**: Moderate sensitivity
3. **exploratory_v1**: Aggressive thresholds, low tau (0.45)

**Configuration:**
```yaml
profiles:
  stable:
    tau: 0.75
    threshold_critical: 0.85
    threshold_turbulent: 0.60
    
  conservative_v1:
    tau: 0.65
    threshold_critical: 0.75
    threshold_turbulent: 0.50
    
  exploratory_v1:
    tau: 0.45
    threshold_critical: 0.65
    threshold_turbulent: 0.40
```

### 8.2 Endpoint

#### Run with Profile
`POST /tw369/run?profile=exploratory_v1`

**Body:**
```json
{
  "text": "Input text",
  "current_state": {...}
}
```

**Response:**
```json
{
  "profile": "exploratory_v1",
  "regime": "TURBULENT",
  "drift_rate": 0.18,
  "tau": 0.45,
  "tw1": 0.72,
  "tw2": 0.55,
  "tw3": 0.38
}
```

### 8.3 Explorer UI Integration

**Component:** `ExplorerTWProfileSelector.tsx`

**Features:**
- Dropdown for profile selection
- Profile descriptions
- Visual comparison (before/after)
- Regime distribution by profile

---

## **9. Narrative Pattern Engine (v4.2)**

**Objective:** Detect and analyze patterns across signals and story events.

### 9.1 Pattern Similarity Module

**Functionality:**
- Compare story event sequences
- Detect recurring narrative patterns
- Cluster similar signals by story structure

**Algorithm:**
- Sequence alignment (edit distance)
- Embedding-based similarity
- Archetype co-occurrence

### 9.2 Archetype Drift Detection

**Functionality:**
- Track archetype transitions over time
- Identify unusual archetype shifts
- Predict next likely archetype

### 9.3 Fracture Analysis

**Functionality:**
- Detect narrative coherence breaks
- Identify conflicting story elements
- Score narrative fragmentation

### 9.4 Divergence Forecasting

**Functionality:**
- Predict signal importance trajectory
- Forecast regime transitions
- Estimate narrative completion

---

## **10. Story Reconstruction Engine (v4.3)**

**Objective:** Reconstruct complete narratives from fragmented story events.

### 10.1 Arc Inference

**Process:**
1. Collect all events for signal
2. Sort by timestamp
3. Identify arc pattern (hero, trickster, etc.)
4. Map events to arc stages

### 10.2 Causality Extraction

**Process:**
1. Analyze event text for causal connectors
2. Build causal graph
3. Identify cause → effect chains

### 10.3 Stage Classification

**Process:**
1. Classify each event into story stage
2. Stages: call, threshold, ordeal, return, etc.
3. Use LLM + rules for classification

### 10.4 Coherence Scoring

**Metrics:**
- Event sequence consistency (0-1)
- Causal chain completeness (0-1)
- Stage progression logic (0-1)
- Overall coherence = weighted average

### 10.5 Output

**Stored in:**
```json
{
  "story_reconstruction": {
    "arc_type": "hero_journey",
    "stages": [
      {"name": "call", "events": [...]},
      {"name": "threshold", "events": [...]}
    ],
    "causal_graph": {...},
    "coherence_score": 0.88
  }
}
```

---

## **11. Pipeline Audit & Optimization**

**Objective:** Ensure pipeline reliability, performance, and maintainability.

### 11.1 Execution Order Validation

**Tasks:**
- Document exact execution flow
- Identify dependencies between modules
- Create execution DAG
- Validate no circular dependencies

### 11.2 Cache Design (Redis)

**Strategy:**
- Cache LLM responses (1 hour TTL)
- Cache learned mapping lookups (24 hour TTL)
- Cache aggregated analytics (15 min TTL)

**Implementation:**
```python
@cache(ttl=3600, key_prefix="llm_response")
def get_llm_score(text: str, prompt: str):
    ...
```

### 11.3 Stress Testing

**Scenarios:**
- 1000 concurrent signal requests
- 100 signals/second ingestion
- 10k WebSocket connections
- Database failover

**Tools:**
- Locust for load testing
- pytest-benchmark for performance regression

### 11.4 Error Isolation Models

**Requirements:**
- Module failures don't cascade
- Partial results returned when possible
- Graceful degradation to simpler modes

**Implementation:**
```python
try:
    delta144 = delta144_engine.run(ctx)
except Exception as e:
    logger.error(f"Δ144 failed: {e}")
    delta144 = None  # Continue without Δ144
```

### 11.5 Logging Normalization

**Standard Format:**
```json
{
  "timestamp": "2025-12-06T14:30:00Z",
  "level": "INFO",
  "module": "delta144_mapping_engine",
  "message": "State mapped: threshold",
  "context": {
    "signal_id": "uuid",
    "confidence": 0.87
  }
}
```

**Levels:**
- DEBUG: Detailed execution traces
- INFO: Normal operations
- WARNING: Degraded mode
- ERROR: Failures with fallback
- CRITICAL: System-wide failures

---

## **12. Deployment Strategy**

### 12.1 API Versioning

**Strategy:**
- `/api/v3/*` - Current stable
- `/api/v4/*` - Next generation (parallel deployment)
- Deprecation timeline: 6 months

**Versions:**
- v3: Signals + story events (basic)
- v4: Unified output + real-time + analytics

### 12.2 Frontend Migration Plan

**Phases:**
1. **Parallel Deployment** - Run v3 and v4 Explorer side-by-side
2. **Feature Flag** - Toggle v4 features per user
3. **Gradual Rollout** - 10% → 50% → 100%
4. **v3 Sunset** - 6 months post v4 GA

### 12.3 Backward Compatibility Guarantees

**Requirements:**
- Existing `/signals` endpoint unchanged
- New fields added, never removed
- v3 contracts honored for 12 months
- Clear migration guides

---

## **13. Appendix**

### 13.1 Diagrams

#### Unified Signal Flow
```
Input Text
    ↓
Domain Analysis
    ↓
Δ144 Mapping (Hybrid)
    ↓
Kindra Scoring (Mode-Based)
    ↓
TW369 Analysis (Profile-Based)
    ↓
Painlevé Check
    ↓
Polarity Calculation
    ↓
Story Arc Classification
    ↓
UnifiedKaldraOutput
    ↓
Persistence (Supabase)
    ↓
API Exposure + WebSocket Push
    ↓
Explorer v4 Visualization
```

### 13.2 Schemas

Refer to:
- `supabase/migrations/0001_init_kaldra_core.sql`
- `src/core/unified_output.py` (to be created)
- `kaldra_api/routers/router_signals.py`

### 13.3 Examples

#### Full Signal Object (v4)
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "domain": "alpha",
  "title": "NVDA Q4 Earnings Beat",
  "delta144": {"state": "threshold", "confidence": 0.92},
  "kindra": {"mode": "hybrid", "dominant": "expansion"},
  "tw369": {"profile": "stable", "regime": "TURBULENT"},
  "polarities": {"order": 0.72, "chaos": 0.28},
  "story_arc": {"archetype": "hero_journey", "stage": "threshold"},
  "importance": 0.95,
  "confidence": 0.92
}
```

### 13.4 Sequence Maps

#### Signal Creation Flow
```
POST /signals/analyze
    ↓
KALDRA Engine processes input
    ↓
UnifiedKaldraOutput created
    ↓
Persisted to Supabase
    ↓
WebSocket broadcast (if subscribed)
    ↓
Return ID + summary to client
```

---

**END OF ROADMAP**

This document serves as the master reference for KALDRA v4.0 development. All phases should be implemented incrementally with testing, documentation, and user feedback at each step.

**Next Actions:**
1. Review and approve roadmap
2. Prioritize phases (3.3 → 3.4 → 5.0 recommended)
3. Create implementation plans for each phase
4. Begin Phase 3.3 API expansion

**Document Status:** Draft v1 - Awaiting Review
