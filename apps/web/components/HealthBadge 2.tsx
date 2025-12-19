/**
 * Health Badge Component
 * Displays KALDRA API connection status
 */

'use client';

import { useEffect, useState } from 'react';
import { fetchSupabaseHealth } from '@/lib/api/kaldra';
import { SupabaseHealthResponse } from '@/lib/types/kaldra';

export function HealthBadge() {
    const [health, setHealth] = useState<SupabaseHealthResponse | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkHealth = async () => {
            try {
                const result = await fetchSupabaseHealth();
                setHealth(result);
            } catch (error) {
                setHealth({
                    status: 'error',
                    supabase_connected: false,
                    error: 'Failed to check health'
                });
            } finally {
                setLoading(false);
            }
        };

        checkHealth();
        // Check health every 30 seconds
        const interval = setInterval(checkHealth, 30000);

        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return (
            <div className="flex items-center gap-2 text-xs text-gray-400">
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-pulse" />
                <span>Checking...</span>
            </div>
        );
    }

    const isHealthy = health?.status === 'ok' && health?.supabase_connected;

    return (
        <div
            className="flex items-center gap-2 text-xs group relative cursor-help"
            title={isHealthy ? 'API Connected' : 'API Offline'}
        >
            <div
                className={`w-2 h-2 rounded-full ${isHealthy ? 'bg-green-500' : 'bg-red-500'
                    } ${isHealthy ? 'animate-pulse' : ''}`}
            />
            <span className={isHealthy ? 'text-green-400' : 'text-red-400'}>
                {isHealthy ? 'KALDRA ↔ Supabase' : 'KALDRA offline'}
            </span>

            {/* Tooltip */}
            <div className="absolute bottom-full left-0 mb-2 hidden group-hover:block z-50">
                <div className="bg-gray-900 border border-gray-700 rounded px-3 py-2 text-xs whitespace-nowrap shadow-lg">
                    <div className="font-medium mb-1">
                        {isHealthy ? '✓ Connected' : '✗ Disconnected'}
                    </div>
                    {health?.signals_sample_count !== undefined && (
                        <div className="text-gray-400">
                            Signals: {health.signals_sample_count}
                        </div>
                    )}
                    {health?.error && (
                        <div className="text-red-400">
                            {health.error}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
