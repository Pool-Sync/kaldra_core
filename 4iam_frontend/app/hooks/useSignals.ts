/**
 * useSignals Hook
 * React hook for fetching signals from KALDRA services
 */

'use client';

import { useState, useEffect } from 'react';
import type { Signal, ServiceKey, ApiResponse } from '../lib/api/types';
import { apiClient } from '../lib/api/client';

interface UseSignalsResult {
    signals: Signal[];
    loading: boolean;
    error: Error | null;
    refetch: () => void;
}

/**
 * Hook to fetch signals from a specific KALDRA service
 * 
 * @param source - KALDRA service key (alpha, geo, product, safeguard) or undefined for all
 * @returns Signals data, loading state, error, and refetch function
 * 
 * @example
 * ```tsx
 * const { signals, loading, error } = useSignals('alpha');
 * ```
 */
export function useSignals(source?: ServiceKey): UseSignalsResult {
    const [signals, setSignals] = useState<Signal[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);
    const [refetchTrigger, setRefetchTrigger] = useState(0);

    useEffect(() => {
        let isMounted = true;

        async function fetchSignals() {
            try {
                setLoading(true);
                setError(null);

                const response: ApiResponse<Signal[]> = await apiClient.getSignals(source);

                if (isMounted) {
                    setSignals(response.data);
                }
            } catch (err) {
                if (isMounted) {
                    setError(err instanceof Error ? err : new Error('Failed to fetch signals'));
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        }

        fetchSignals();

        return () => {
            isMounted = false;
        };
    }, [source, refetchTrigger]);

    const refetch = () => {
        setRefetchTrigger(prev => prev + 1);
    };

    return { signals, loading, error, refetch };
}
