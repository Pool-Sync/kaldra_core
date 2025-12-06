/**
 * KALDRA Explorer - React Hook
 * 
 * Custom hook for accessing Explorer data and functionality.
 * Now connects to KALDRA API Gateway for real data.
 */

'use client';

import { useState, useMemo, useEffect } from 'react';
import { ExplorerSignal, ExplorerFilters, ExplorerTimelinePoint, ExplorerStats } from '../(explorer)/explorer/lib/explorer.types';
import { getAllMockSignals, getMockSignalById } from '../(explorer)/explorer/lib/explorer.mock';
import { filterSignals, sortSignalsByTime, generateTimeline, calculateStats } from '../(explorer)/explorer/lib/explorer.utils';
import { fetchSignals } from '@/lib/api/kaldra';
import { convertSignalsToExplorerFormat } from '@/lib/api/utils';

const API_MODE = process.env.NEXT_PUBLIC_KALDRA_API_MODE || 'mock';

export function useExplorer() {
    const [filters, setFilters] = useState<ExplorerFilters>({ source: 'all' });
    const [selectedSignalId, setSelectedSignalId] = useState<string | null>(null);
    const [apiSignals, setApiSignals] = useState<ExplorerSignal[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Fetch signals from API when in real mode
    useEffect(() => {
        if (API_MODE !== 'real') return;

        const loadSignals = async () => {
            setLoading(true);
            setError(null);

            try {
                const domain = filters.source !== 'all' ? filters.source : undefined;
                const signals = await fetchSignals({ domain, limit: 100 });
                const converted = convertSignalsToExplorerFormat(signals);
                setApiSignals(converted);
            } catch (err) {
                console.error('Failed to load signals:', err);
                setError(err instanceof Error ? err.message : 'Failed to load signals');
                // Fallback to mocks on error
                setApiSignals(getAllMockSignals());
            } finally {
                setLoading(false);
            }
        };

        loadSignals();
    }, [filters.source]);

    // Get all signals (API or mock depending on mode)
    const allSignals = useMemo(() => {
        if (API_MODE === 'real') {
            return apiSignals;
        }
        return getAllMockSignals();
    }, [apiSignals]);

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

        // Find in current signals first
        const found = allSignals.find(s => s.id === selectedSignalId);
        if (found) return found;

        // Fallback to mock for backwards compatibility
        return getMockSignalById(selectedSignalId);
    }, [selectedSignalId, allSignals]);

    return {
        // Data
        signals: filteredSignals,
        timeline,
        stats,
        selectedSignal,
        loading,
        error,

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
