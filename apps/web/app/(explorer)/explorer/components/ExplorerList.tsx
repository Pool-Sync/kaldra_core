/**
 * KALDRA Explorer - List Component
 * 
 * Displays signals as clickable cards.
 */

'use client';

import { ExplorerSignal } from '../lib/explorer.types';
import { getRegimeColor, getSourceLabel, formatTimestamp } from '../lib/explorer.utils';

interface ExplorerListProps {
    signals: ExplorerSignal[];
    onSignalClick: (signal: ExplorerSignal) => void;
    selectedSignalId?: string | null;
}

export function ExplorerList({ signals, onSignalClick, selectedSignalId }: ExplorerListProps) {
    if (signals.length === 0) {
        return (
            <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-12">
                <p className="text-center text-gray-500 dark:text-gray-400">
                    No signals found matching current filters
                </p>
            </div>
        );
    }

    return (
        <div className="space-y-3">
            {signals.map(signal => {
                const isSelected = signal.id === selectedSignalId;
                const regimeColor = getRegimeColor(signal.tw_regime);

                return (
                    <button
                        key={signal.id}
                        onClick={() => onSignalClick(signal)}
                        className={`
              w-full text-left bg-white dark:bg-gray-900 border rounded-lg p-4 transition-all
              hover:shadow-md hover:border-gray-300 dark:hover:border-gray-700
              ${isSelected
                                ? 'border-blue-500 dark:border-blue-500 shadow-md'
                                : 'border-gray-200 dark:border-gray-800'
                            }
            `}
                    >
                        <div className="flex items-start justify-between gap-4">
                            <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2 mb-2">
                                    <div
                                        className="w-2 h-2 rounded-full flex-shrink-0"
                                        style={{ backgroundColor: regimeColor }}
                                    />
                                    <span className="text-xs font-medium text-gray-500 dark:text-gray-400">
                                        {getSourceLabel(signal.source)}
                                    </span>
                                    <span className="text-xs text-gray-400 dark:text-gray-500">
                                        {formatTimestamp(signal.timestamp)}
                                    </span>
                                </div>

                                <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-1">
                                    {signal.title}
                                </h3>

                                <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                                    {signal.summary}
                                </p>

                                <div className="flex items-center gap-3 mt-3 text-xs">
                                    <span className="text-gray-500 dark:text-gray-500">
                                        {signal.delta144_state}
                                    </span>
                                    <span className="text-gray-500 dark:text-gray-500">
                                        {signal.tw_regime}
                                    </span>
                                    <span className="text-gray-500 dark:text-gray-500">
                                        {Math.round(signal.confidence * 100)}% confidence
                                    </span>
                                </div>
                            </div>
                        </div>
                    </button>
                );
            })}
        </div>
    );
}
