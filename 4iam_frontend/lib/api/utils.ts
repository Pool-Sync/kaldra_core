/**
 * KALDRA API - Utilities
 * Helper functions for converting API data to Explorer types
 */

import type { Signal, StoryEvent } from '../types/kaldra';
import type { ExplorerSignal, ExplorerSource, TWRegime } from '@/app/(explorer)/explorer/lib/explorer.types';

/**
 * Convert API Signal to ExplorerSignal
 */
export function convertSignalToExplorerFormat(signal: Signal): ExplorerSignal {
    return {
        id: signal.id,
        source: (signal.domain || 'alpha') as ExplorerSource,
        title: signal.title,
        summary: signal.summary || '',
        archetype_id: signal.dominant_archetype || 'unknown',
        delta144_state: signal.delta144_state || 'unknown',
        kindra_vector: '', // Not in current API
        tw_regime: (signal.tw_regime || 'STABLE') as TWRegime,
        confidence: signal.confidence || 0.5,
        timestamp: signal.created_at || new Date().toISOString(),
    };
}

/**
 * Convert multiple signals
 */
export function convertSignalsToExplorerFormat(signals: Signal[]): ExplorerSignal[] {
    return signals.map(convertSignalToExplorerFormat);
}
