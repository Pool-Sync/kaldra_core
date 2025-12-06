/**
 * KALDRA Explorer - Details Component
 * 
 * Modal/panel showing detailed signal information + story events timeline.
 */

'use client';

import { useSignalDetails } from '@/app/hooks/useSignalDetails';
import { ExplorerSignal } from '../lib/explorer.types';
import { getRegimeColor, getSourceLabel, formatTimestamp } from '../lib/explorer.utils';
import { ExplorerStoryTimeline } from '@/components/ExplorerStoryTimeline';

interface ExplorerDetailsProps {
    signal: ExplorerSignal | null;
    onClose: () => void;
}

export function ExplorerDetails({ signal, onClose }: ExplorerDetailsProps) {
    // Fetch real signal details + story events from API
    const { events, loading, error } = useSignalDetails(signal?.id);

    if (!signal) return null;

    const regimeColor = getRegimeColor(signal.tw_regime);

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                {/* Header */}
                <div className="sticky top-0 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 px-6 py-4">
                    <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                                <div
                                    className="w-2 h-2 rounded-full"
                                    style={{ backgroundColor: regimeColor }}
                                />
                                <span className="text-sm font-medium text-gray-500 dark:text-gray-400">
                                    {getSourceLabel(signal.source)}
                                </span>
                            </div>
                            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                                {signal.title}
                            </h2>
                        </div>
                        <button
                            onClick={onClose}
                            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                        >
                            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                </div>

                {/* Content */}
                <div className="px-6 py-6 space-y-6">
                    {/* Summary */}
                    <div>
                        <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
                            Summary
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
                            {signal.summary}
                        </p>
                    </div>

                    {/* Metadata Grid */}
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <h3 className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
                                TW Regime
                            </h3>
                            <div className="flex items-center gap-2">
                                <div
                                    className="w-2 h-2 rounded-full"
                                    style={{ backgroundColor: regimeColor }}
                                />
                                <span className="text-sm font-medium text-gray-900 dark:text-white">
                                    {signal.tw_regime}
                                </span>
                            </div>
                        </div>

                        <div>
                            <h3 className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
                                Confidence
                            </h3>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">
                                {Math.round(signal.confidence * 100)}%
                            </span>
                        </div>

                        <div>
                            <h3 className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
                                Δ144 State
                            </h3>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">
                                {signal.delta144_state}
                            </span>
                        </div>

                        <div>
                            <h3 className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
                                Archetype
                            </h3>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">
                                {signal.archetype_id}
                            </span>
                        </div>

                        <div>
                            <h3 className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
                                Kindra Vector
                            </h3>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">
                                {signal.kindra_vector}
                            </span>
                        </div>

                        <div>
                            <h3 className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
                                Timestamp
                            </h3>
                            <span className="text-sm font-medium text-gray-900 dark:text-white">
                                {formatTimestamp(signal.timestamp)}
                            </span>
                        </div>
                    </div>

                    {/* Story Events Timeline */}
                    <div className="pt-4 border-t border-gray-200 dark:border-gray-800">
                        <ExplorerStoryTimeline
                            events={events}
                            loading={loading}
                            error={error}
                        />
                    </div>

                    {/* Signal ID */}
                    <div className="pt-4 border-t border-gray-200 dark:border-gray-800">
                        <h3 className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1">
                            Signal ID
                        </h3>
                        <code className="text-xs text-gray-600 dark:text-gray-400 font-mono">
                            {signal.id}
                        </code>
                    </div>
                </div>

                {/* Footer */}
                <div className="sticky bottom-0 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-200 dark:border-gray-800 px-6 py-4">
                    <button
                        onClick={onClose}
                        className="w-full px-4 py-2 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg hover:bg-gray-800 dark:hover:bg-gray-100 transition-colors text-sm font-medium"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
}
