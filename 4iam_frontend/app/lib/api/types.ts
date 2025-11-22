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

export type KaldraTWRegime = "STABLE" | "CRITICAL" | "UNSTABLE";

export interface KaldraSignal {
    archetype: string;
    delta_state: string;
    tw_regime: KaldraTWRegime;
    kindra_distribution: Record<string, number>;
    bias_score: number;
    meta_modifiers: Record<string, number[]>;
    confidence: number;
    explanation: string;

    // campos adicionais opcionais, retornados pelo backend
    bias_label?: string;
    narrative_risk?: string;
}

// Alias for compatibility
export type KaldraSignalResponse = KaldraSignal;
