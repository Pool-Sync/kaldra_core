/**
 * KALDRA Explorer - Type Definitions
 * 
 * Official TypeScript types for the Explorer module.
 * These types match the future API Gateway response structure.
 */

export type ExplorerSource = 'alpha' | 'geo' | 'product' | 'safeguard';

export type TWRegime = 'STABLE' | 'TURBULENT' | 'CRITICAL';

export interface ExplorerSignal {
    id: string;
    source: ExplorerSource;
    title: string;
    summary: string;
    archetype_id: string;
    delta144_state: string;
    kindra_vector: string;
    tw_regime: TWRegime;
    confidence: number;
    timestamp: string; // ISO 8601 format
}

export interface ExplorerFilters {
    source?: ExplorerSource | 'all';
    regime?: TWRegime | 'all';
    dateFrom?: string;
    dateTo?: string;
    minConfidence?: number;
}

export interface ExplorerTimelinePoint {
    timestamp: string;
    regime: TWRegime;
    count: number;
    signals: ExplorerSignal[];
}

export interface ExplorerStats {
    totalSignals: number;
    bySource: Record<ExplorerSource, number>;
    byRegime: Record<TWRegime, number>;
    avgConfidence: number;
}
