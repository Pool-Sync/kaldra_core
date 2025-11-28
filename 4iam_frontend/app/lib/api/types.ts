/**
 * 4IAM.AI API Types
 * TypeScript interfaces for KALDRA API data structures
 */

export type ServiceKey = 'alpha' | 'geo' | 'product' | 'safeguard';

export type TWRegime = 'STABLE' | 'TURBULENT' | 'CRITICAL';

export type SignalPriority = 'low' | 'medium' | 'high' | 'critical';

export type InsightType = 'report' | 'analysis' | 'briefing' | 'forecast';

/**
 * Signal - Real-time intelligence signal from KALDRA products
 */
export interface Signal {
    id: string;
    title: string;
    source: ServiceKey;
    summary: string;

    // KALDRA Symbolic Data
    archetype_id: number; // 1-12
    delta144_state: number; // 1-144
    kindra_vector?: number[];
    tw_regime: TWRegime;

    // Metadata
    confidence: number; // 0-1
    priority: SignalPriority;
    timestamp: string;

    // Optional fields
    content?: string;
    entities?: string[];
    tags?: string[];
}

/**
 * Insight - In-depth intelligence report
 */
export interface Insight {
    id: string;
    title: string;
    subtitle?: string;
    summary: string;
    content: string;

    // Classification
    type: InsightType;
    source: ServiceKey;
    category: string;

    // Authorship
    author: string;
    publishedAt: string;

    // KALDRA Analysis
    archetypes?: number[];
    kindras?: string[];
    symbolicSummary?: string;

    // Metadata
    tags: string[];
    readTime: number; // minutes
    views: number;
}

/**
 * Explorer Feed Item - Symbolic visualization data
 */
export interface ExplorerFeedItem {
    id: string;
    title: string;
    source: ServiceKey;

    // Symbolic Data
    archetype_id: number;
    delta144_state: number;
    kindra_id?: string;
    tw_score: number;

    // Visualization metadata
    timestamp: string;
    intensity: number; // 0-1
}

/**
 * Dashboard Metrics
 */
export interface DashboardMetrics {
    totalSignals: number;
    criticalSignals: number;
    activeInsights: number;
    twRegimeDistribution: Record<TWRegime, number>;
    archetypeDistribution: Record<number, number>;
}

/**
 * API Response wrapper
 */
export interface ApiResponse<T> {
    data: T;
    timestamp: string;
    source: string;
}

/**
 * API Error
 */
export interface ApiError {
    code: string;
    message: string;
    details?: any;
}

// --- KALDRA CORE Signal Types (synced with backend schema) ---

export interface KaldraSignalRequest {
    text: string;
}

export type KaldraTWRegime = "STABLE" | "ANOMALY" | "CRITICAL" | "UNSTABLE";

/**
 * KALDRA Signal Response from Master Engine V2
 * Updated to reflect Phase 4 API enrichment (bias, narrative risk, real Delta144 state)
 */
export interface KaldraSignalResponse {
    // Delta144 Archetype & State
    archetype: string;              // Real archetype ID (e.g., "A07_RULER")
    delta_state: string;            // Real state ID (e.g., "A07_05")

    // TW-Painlevé Oracle
    tw_regime: KaldraTWRegime;      // "STABLE" or "ANOMALY"

    // Kindra Cultural Modulation (top-5 states)
    kindra_distribution: Array<{
        state_index: number;
        prob: number;
    }>;

    // Bias Engine
    bias_score: number;             // 0.0 - 1.0
    bias_label: string | null;      // e.g., "neutral", "moderate", "extreme"

    // Narrative Risk (heuristic v0.1)
    narrative_risk: number;         // 0.0 - 1.0

    // Epistemic Limiter
    confidence: number;             // 0.0 - 1.0
    explanation: string;            // e.g., "Master Engine V2: OK"

    // Meta Modifiers (future use)
    meta_modifiers: Record<string, number[]>;
}

// Alias for compatibility
export type KaldraSignal = KaldraSignalResponse;

