/**
 * Explorer Story Timeline Component (Real Events)
 * Displays story events from API in timeline format
 */

'use client';

import type { ExplorerStoryEvent } from '@/lib/types/kaldra';

interface ExplorerStoryTimelineProps {
    events: ExplorerStoryEvent[];
    loading?: boolean;
    error?: string | null;
}

export function ExplorerStoryTimeline({ events, loading, error }: ExplorerStoryTimelineProps) {
    if (loading) {
        return (
            <div className="text-xs text-gray-500 dark:text-gray-400 py-4">
                Carregando eventos...
            </div>
        );
    }

    if (error) {
        return (
            <div className="space-y-2 py-4">
                <div className="text-sm text-red-500">{error}</div>
                <div className="text-xs text-gray-500 dark:text-gray-400">
                    Os dados principais do signal continuam disponíveis. Tente novamente mais tarde.
                </div>
            </div>
        );
    }

    if (!events || events.length === 0) {
        return (
            <div className="text-xs text-gray-500 dark:text-gray-400 py-4">
                Nenhum evento narrativo registrado para este signal ainda.
            </div>
        );
    }

    return (
        <div className="space-y-4">
            <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-3">
                Timeline de Eventos ({events.length})
            </h3>

            {events.map((ev, index) => (
                <div key={ev.id} className="flex gap-3 relative">
                    {/* Timeline line */}
                    {index < events.length - 1 && (
                        <div className="absolute left-[7px] top-6 bottom-0 w-px bg-gray-200 dark:bg-gray-700" />
                    )}

                    {/* Dot */}
                    <div className="mt-1.5 h-3 w-3 rounded-full bg-blue-500 dark:bg-blue-400 flex-shrink-0 relative z-10" />

                    {/* Content */}
                    <div className="flex-1 space-y-2 pb-6">
                        <div className="text-sm text-gray-900 dark:text-white leading-relaxed">
                            {ev.text}
                        </div>

                        <div className="flex flex-wrap gap-2 text-xs">
                            {/* Stream badge */}
                            {ev.streamLabel && ev.streamLabel !== 'unknown' && (
                                <span className="inline-flex items-center rounded-full border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800 px-2.5 py-0.5 text-gray-700 dark:text-gray-300">
                                    <svg className="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                                    </svg>
                                    {ev.streamLabel}
                                </span>
                            )}

                            {/* State badge */}
                            {ev.stateLabel && (
                                <span className="inline-flex items-center rounded-full border border-purple-300 dark:border-purple-600 bg-purple-50 dark:bg-purple-900/30 px-2.5 py-0.5 text-purple-700 dark:text-purple-300">
                                    Δ {ev.stateLabel}
                                </span>
                            )}

                            {/* Polarities */}
                            {ev.polarities && Object.keys(ev.polarities).length > 0 && (
                                <span className="inline-flex items-center rounded-full border border-green-300 dark:border-green-600 bg-green-50 dark:bg-green-900/30 px-2.5 py-0.5 text-green-700 dark:text-green-300">
                                    {Object.entries(ev.polarities)
                                        .map(([key, val]) => `${key}: ${(val * 100).toFixed(0)}%`)
                                        .join(', ')}
                                </span>
                            )}

                            {/* Timestamp */}
                            {ev.createdAtLabel && (
                                <span className="text-gray-500 dark:text-gray-400">
                                    {ev.createdAtLabel}
                                </span>
                            )}
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}
