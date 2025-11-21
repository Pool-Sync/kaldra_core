/**
 * useInsights Hook
 * React hook for fetching insights from KALDRA services
 */

'use client';

import { useState, useEffect } from 'react';
import type { Insight, ServiceKey, ApiResponse } from '../lib/api/types';
import { apiClient } from '../lib/api/client';

interface UseInsightsResult {
    insights: Insight[];
    loading: boolean;
    error: Error | null;
    refetch: () => void;
}

/**
 * Hook to fetch insights from a specific KALDRA service
 * 
 * @param source - KALDRA service key (alpha, geo, product, safeguard) or undefined for all
 * @returns Insights data, loading state, error, and refetch function
 * 
 * @example
 * ```tsx
 * const { insights, loading, error } = useInsights('geo');
 * ```
 */
export function useInsights(source?: ServiceKey): UseInsightsResult {
    const [insights, setInsights] = useState<Insight[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);
    const [refetchTrigger, setRefetchTrigger] = useState(0);

    useEffect(() => {
        let isMounted = true;

        async function fetchInsights() {
            try {
                setLoading(true);
                setError(null);

                const response: ApiResponse<Insight[]> = await apiClient.getInsights(source);

                if (isMounted) {
                    setInsights(response.data);
                }
            } catch (err) {
                if (isMounted) {
                    setError(err instanceof Error ? err : new Error('Failed to fetch insights'));
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        }

        fetchInsights();

        return () => {
            isMounted = false;
        };
    }, [source, refetchTrigger]);

    const refetch = () => {
        setRefetchTrigger(prev => prev + 1);
    };

    return { insights, loading, error, refetch };
}
