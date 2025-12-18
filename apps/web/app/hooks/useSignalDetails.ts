/**
 * useSignalDetails Hook
 * Fetches signal details and story events together
 */

'use client';

import { useEffect, useState } from 'react';
import { fetchSignalById, fetchStoryEventsBySignalId } from '@/lib/api/kaldra';
import { convertStoryEventsToExplorerFormat } from '@/lib/api/utils';
import type { Signal, ExplorerStoryEvent } from '@/lib/types/kaldra';

type State = {
    signal: Signal | null;
    events: ExplorerStoryEvent[];
    loading: boolean;
    error: string | null;
};

const API_MODE = process.env.NEXT_PUBLIC_KALDRA_API_MODE || 'mock';

export function useSignalDetails(signalId?: string) {
    const [state, setState] = useState<State>({
        signal: null,
        events: [],
        loading: false,
        error: null,
    });

    useEffect(() => {
        if (!signalId) {
            setState({ signal: null, events: [], loading: false, error: null });
            return;
        }

        if (API_MODE === 'mock') {
            // Mock mode: don't fetch, return empty state
            setState({ signal: null, events: [], loading: false, error: null });
            return;
        }

        let cancelled = false;

        async function load() {
            setState(prev => ({ ...prev, loading: true, error: null }));

            try {
                const [signal, events] = await Promise.all([
                    fetchSignalById(signalId),
                    fetchStoryEventsBySignalId(signalId),
                ]);

                if (cancelled) return;

                setState({
                    signal: signal ?? null,
                    events: convertStoryEventsToExplorerFormat(events ?? []),
                    loading: false,
                    error: null,
                });
            } catch (err: any) {
                if (cancelled) return;

                console.error('Failed to load signal details:', err);
                setState(prev => ({
                    ...prev,
                    loading: false,
                    error: 'Não foi possível carregar a timeline desse signal.',
                }));
            }
        }

        load();

        return () => {
            cancelled = true;
        };
    }, [signalId]);

    return state;
}
