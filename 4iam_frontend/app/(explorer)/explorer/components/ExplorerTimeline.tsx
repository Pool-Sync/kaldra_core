/**
 * KALDRA Explorer - Timeline Component
 * 
 * Visual timeline showing signal distribution over time.
 */

'use client';

import { ExplorerTimelinePoint } from '../lib/explorer.types';
import { getRegimeColor } from '../lib/explorer.utils';

interface ExplorerTimelineProps {
    timeline: ExplorerTimelinePoint[];
    onPointClick?: (point: ExplorerTimelinePoint) => void;
}

export function ExplorerTimeline({ timeline, onPointClick }: ExplorerTimelineProps) {
    if (timeline.length === 0) {
        return (
            <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
                <p className="text-sm text-gray-500 dark:text-gray-400 text-center">
                    No timeline data available
                </p>
            </div>
        );
    }

    return (
        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
            <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-4">
                Signal Timeline
            </h3>

            <div className="flex items-center gap-2 overflow-x-auto pb-2">
                {timeline.map((point, index) => {
                    const color = getRegimeColor(point.regime);
                    const date = new Date(point.timestamp);
                    const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

                    return (
                        <button
                            key={point.timestamp}
                            onClick={() => onPointClick?.(point)}
                            className="flex flex-col items-center gap-1 min-w-[60px] group"
                            title={`${dateStr}: ${point.count} signals (${point.regime})`}
                        >
                            <div
                                className="w-3 h-3 rounded-full transition-transform group-hover:scale-125"
                                style={{ backgroundColor: color }}
                            />
                            <div className="text-xs text-gray-500 dark:text-gray-400">
                                {dateStr}
                            </div>
                            <div className="text-xs font-medium text-gray-700 dark:text-gray-300">
                                {point.count}
                            </div>
                        </button>
                    );
                })}
            </div>

            <div className="mt-4 flex items-center gap-4 text-xs">
                <div className="flex items-center gap-1.5">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: getRegimeColor('STABLE') }} />
                    <span className="text-gray-600 dark:text-gray-400">Stable</span>
                </div>
                <div className="flex items-center gap-1.5">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: getRegimeColor('TURBULENT') }} />
                    <span className="text-gray-600 dark:text-gray-400">Turbulent</span>
                </div>
                <div className="flex items-center gap-1.5">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: getRegimeColor('CRITICAL') }} />
                    <span className="text-gray-600 dark:text-gray-400">Critical</span>
                </div>
            </div>
        </div>
    );
}
