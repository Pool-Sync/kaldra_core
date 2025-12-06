/**
 * KALDRA API Client
 * Functions for interacting with the KALDRA API Gateway
 */

import { Signal, StoryEvent, SignalFilters, ApiError, SupabaseHealthResponse } from '../types/kaldra';

const API_BASE_URL = process.env.NEXT_PUBLIC_KALDRA_API_URL || 'http://localhost:8000';

/**
 * Fetch signals from the API
 */
export async function fetchSignals(params?: SignalFilters): Promise<Signal[]> {
    const queryParams = new URLSearchParams();

    if (params?.domain) {
        queryParams.append('domain', params.domain);
    }

    if (params?.limit) {
        queryParams.append('limit', params.limit.toString());
    }

    const url = `${API_BASE_URL}/signals?${queryParams.toString()}`;

    try {
        const response = await fetch(url, {
            cache: 'no-store',
            headers: {
                'Accept': 'application/json',
            },
        });

        if (response.status === 503) {
            throw new Error('API_UNAVAILABLE');
        }

        if (!response.ok) {
            const error: ApiError = await response.json();
            throw new Error(error.detail || 'Failed to fetch signals');
        }

        const data: Signal[] = await response.json();
        return data;
    } catch (error) {
        if (error instanceof Error && error.message === 'API_UNAVAILABLE') {
            throw error;
        }
        console.error('Error fetching signals:', error);
        throw new Error('API_UNAVAILABLE');
    }
}

/**
 * Fetch a single signal by ID
 */
export async function fetchSignalById(id: string): Promise<Signal | null> {
    const url = `${API_BASE_URL}/signals/${id}`;

    try {
        const response = await fetch(url, {
            cache: 'no-store',
            headers: {
                'Accept': 'application/json',
            },
        });

        if (response.status === 404) {
            return null;
        }

        if (response.status === 503) {
            throw new Error('API_UNAVAILABLE');
        }

        if (!response.ok) {
            const error: ApiError = await response.json();
            throw new Error(error.detail || 'Failed to fetch signal');
        }

        const data: Signal = await response.json();
        return data;
    } catch (error) {
        if (error instanceof Error && error.message === 'API_UNAVAILABLE') {
            throw error;
        }
        console.error('Error fetching signal:', error);
        throw new Error('API_UNAVAILABLE');
    }
}

/**
 * Fetch story events for a signal
 */
export async function fetchStoryEventsBySignalId(signalId: string): Promise<StoryEvent[]> {
    const url = `${API_BASE_URL}/story-events/by-signal/${signalId}`;

    try {
        const response = await fetch(url, {
            cache: 'no-store',
            headers: {
                'Accept': 'application/json',
            },
        });

        if (response.status === 503) {
            throw new Error('API_UNAVAILABLE');
        }

        if (!response.ok) {
            const error: ApiError = await response.json();
            throw new Error(error.detail || 'Failed to fetch story events');
        }

        const data: StoryEvent[] = await response.json();
        return data;
    } catch (error) {
        if (error instanceof Error && error.message === 'API_UNAVAILABLE') {
            throw error;
        }
        console.error('Error fetching story events:', error);
        throw new Error('API_UNAVAILABLE');
    }
}

/**
 * Check Supabase health status
 */
export async function fetchSupabaseHealth(): Promise<SupabaseHealthResponse> {
    const url = `${API_BASE_URL}/health/supabase`;

    try {
        const response = await fetch(url, {
            cache: 'no-store',
            headers: {
                'Accept': 'application/json',
            },
        });

        const data: SupabaseHealthResponse = await response.json();
        return data;
    } catch (error) {
        console.error('Error checking Supabase health:', error);
        return {
            status: 'error',
            supabase_connected: false,
            error: 'Connection failed'
        };
    }
}
