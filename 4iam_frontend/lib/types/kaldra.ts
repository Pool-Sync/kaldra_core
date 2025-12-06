/**
 * KALDRA API Types
 * TypeScript interfaces for API responses
 */

export interface Signal {
    id: string;
    domain: string;
    title: string;
    summary?: string;
    source_anchor?: string;
    source_url?: string;
    delta144_state?: string;
    dominant_archetype?: string;
    dominant_polarity?: string;
    tw_regime?: string;
    journey_stage?: string;
    importance?: number;
    confidence?: number;
    divergence?: number;
    raw_payload?: Record<string, any>;
    created_at?: string;
}

export interface StoryEvent {
    id: string;
    signal_id?: string;
    stream_id?: string;
    text?: string;
    delta144_state?: string;
    polarities?: Record<string, number>;
    meta?: Record<string, any>;
    created_at?: string;
}

export interface SignalFilters {
    domain?: string;
    limit?: number;
}

export interface ApiError {
    detail: string;
    status?: number;
}

export interface SupabaseHealthResponse {
    status: string;
    supabase_connected?: boolean;
    signals_sample_count?: number;
    message?: string;
    error?: string;
}
