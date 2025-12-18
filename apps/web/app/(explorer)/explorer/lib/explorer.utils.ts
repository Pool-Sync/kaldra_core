/**
 * KALDRA Explorer - Utility Functions
 * 
 * Helper functions for signal processing, filtering, and normalization.
 */

import { ExplorerSignal, ExplorerFilters, ExplorerTimelinePoint, ExplorerStats, TWRegime, ExplorerSource } from './explorer.types';

/**
 * Filter signals based on provided criteria
 */
export function filterSignals(
    signals: ExplorerSignal[],
    filters: ExplorerFilters
): ExplorerSignal[] {
    return signals.filter(signal => {
        // Source filter
        if (filters.source && filters.source !== 'all' && signal.source !== filters.source) {
            return false;
        }

        // Regime filter
        if (filters.regime && filters.regime !== 'all' && signal.tw_regime !== filters.regime) {
            return false;
        }

        // Date range filter
        if (filters.dateFrom && signal.timestamp < filters.dateFrom) {
            return false;
        }
        if (filters.dateTo && signal.timestamp > filters.dateTo) {
            return false;
        }

        // Confidence filter
        if (filters.minConfidence && signal.confidence < filters.minConfidence) {
            return false;
        }

        return true;
    });
}

/**
 * Sort signals by timestamp (newest first)
 */
export function sortSignalsByTime(signals: ExplorerSignal[]): ExplorerSignal[] {
    return [...signals].sort((a, b) =>
        new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );
}

/**
 * Group signals into timeline points
 */
export function generateTimeline(signals: ExplorerSignal[]): ExplorerTimelinePoint[] {
    const grouped = new Map<string, ExplorerSignal[]>();

    signals.forEach(signal => {
        const date = signal.timestamp.split('T')[0]; // Get date part only
        if (!grouped.has(date)) {
            grouped.set(date, []);
        }
        grouped.get(date)!.push(signal);
    });

    const timeline: ExplorerTimelinePoint[] = [];
    grouped.forEach((daySignals, date) => {
        // Determine dominant regime for the day
        const regimeCounts = daySignals.reduce((acc, s) => {
            acc[s.tw_regime] = (acc[s.tw_regime] || 0) + 1;
            return acc;
        }, {} as Record<TWRegime, number>);

        const dominantRegime = (Object.entries(regimeCounts)
            .sort(([, a], [, b]) => b - a)[0]?.[0] || 'STABLE') as TWRegime;

        timeline.push({
            timestamp: date,
            regime: dominantRegime,
            count: daySignals.length,
            signals: daySignals
        });
    });

    return timeline.sort((a, b) =>
        new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );
}

/**
 * Calculate statistics for a set of signals
 */
export function calculateStats(signals: ExplorerSignal[]): ExplorerStats {
    const bySource: Record<ExplorerSource, number> = {
        alpha: 0,
        geo: 0,
        product: 0,
        safeguard: 0
    };

    const byRegime: Record<TWRegime, number> = {
        STABLE: 0,
        TURBULENT: 0,
        CRITICAL: 0
    };

    let totalConfidence = 0;

    signals.forEach(signal => {
        bySource[signal.source]++;
        byRegime[signal.tw_regime]++;
        totalConfidence += signal.confidence;
    });

    return {
        totalSignals: signals.length,
        bySource,
        byRegime,
        avgConfidence: signals.length > 0 ? totalConfidence / signals.length : 0
    };
}

/**
 * Get color for TW regime
 */
export function getRegimeColor(regime: TWRegime): string {
    switch (regime) {
        case 'STABLE':
            return 'rgb(34, 197, 94)'; // green-500
        case 'TURBULENT':
            return 'rgb(234, 179, 8)'; // yellow-500
        case 'CRITICAL':
            return 'rgb(239, 68, 68)'; // red-500
        default:
            return 'rgb(156, 163, 175)'; // gray-400
    }
}

/**
 * Get label for source
 */
export function getSourceLabel(source: ExplorerSource): string {
    switch (source) {
        case 'alpha':
            return 'KALDRA Alpha';
        case 'geo':
            return 'KALDRA GEO';
        case 'product':
            return 'KALDRA Product';
        case 'safeguard':
            return 'KALDRA Safeguard';
        default:
            return source;
    }
}

/**
 * Format timestamp for display
 */
export function formatTimestamp(timestamp: string): string {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}
