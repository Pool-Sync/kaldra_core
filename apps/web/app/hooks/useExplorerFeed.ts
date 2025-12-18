/**
 * useExplorerFeed Hook
 * React hook for fetching explorer feed from KALDRA services
 */

'use client';

import { useState, useEffect } from 'react';
import type { ExplorerFeedItem, ServiceKey, ApiResponse } from '../lib/api/types';
import { apiClient } from '../lib/api/client';

interface UseExplorerFeedResult {
    feed: ExplorerFeedItem[];
    loading: boolean;
    error: Error | null;
    refetch: () => void;
}

/**
 * Hook to fetch explorer feed from a specific KALDRA service
 * 
 * @param source - KALDRA service key (alpha, geo, product, safeguard) or undefined for all
 * @returns Explorer feed data, loading state, error, and refetch function
 * 
 * @example
 * ```tsx
 * const { feed, loading, error } = useExplorerFeed();
 * ```
 */
export function useExplorerFeed(source?: ServiceKey): UseExplorerFeedResult {
    const [feed, setFeed] = useState<ExplorerFeedItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);
    const [refetchTrigger, setRefetchTrigger] = useState(0);

    useEffect(() => {
        let isMounted = true;

        async function fetchFeed() {
            try {
                setLoading(true);
                setError(null);

                const response: ApiResponse<ExplorerFeedItem[]> = await apiClient.getExplorerFeed(source);

                if (isMounted) {
                    setFeed(response.data);
                }
            } catch (err) {
                if (isMounted) {
                    setError(err instanceof Error ? err : new Error('Failed to fetch explorer feed'));
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        }

        fetchFeed();

        return () => {
            isMounted = false;
        };
    }, [source, refetchTrigger]);

    const refetch = () => {
        setRefetchTrigger(prev => prev + 1);
    };

    return { feed, loading, error, refetch };
}
