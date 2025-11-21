/**
 * KALDRA Explorer - React Hook
 * 
 * Custom hook for accessing Explorer data and functionality.
 * Currently uses mocks; will be replaced with API calls in production.
 */

'use client';

import { useState, useMemo } from 'react';
import { ExplorerSignal, ExplorerFilters, ExplorerTimelinePoint, ExplorerStats } from '../(explorer)/explorer/lib/explorer.types';
import { getAllMockSignals, getMockSignalById } from '../(explorer)/explorer/lib/explorer.mock';
import { filterSignals, sortSignalsByTime, generateTimeline, calculateStats } from '../(explorer)/explorer/lib/explorer.utils';

export function useExplorer() {
    const [filters, setFilters] = useState<ExplorerFilters>({ source: 'all' });
    const [selectedSignalId, setSelectedSignalId] = useState<string | null>(null);

    // Get all signals
    const allSignals = useMemo(() => getAllMockSignals(), []);

    // Apply filters
    const filteredSignals = useMemo(() => {
        const filtered = filterSignals(allSignals, filters);
        return sortSignalsByTime(filtered);
    }, [allSignals, filters]);

    // Generate timeline
    const timeline = useMemo(() => {
        return generateTimeline(filteredSignals);
    }, [filteredSignals]);

    // Calculate stats
    const stats = useMemo(() => {
        return calculateStats(filteredSignals);
    }, [filteredSignals]);

    // Get selected signal
    const selectedSignal = useMemo(() => {
        if (!selectedSignalId) return null;
        return getMockSignalById(selectedSignalId);
    }, [selectedSignalId]);

    return {
        // Data
        signals: filteredSignals,
        timeline,
        stats,
        selectedSignal,

        // Filters
        filters,
        setFilters,

        // Selection
        selectedSignalId,
        setSelectedSignalId,

        // Actions
        clearFilters: () => setFilters({ source: 'all' }),
        clearSelection: () => setSelectedSignalId(null)
    };
}
