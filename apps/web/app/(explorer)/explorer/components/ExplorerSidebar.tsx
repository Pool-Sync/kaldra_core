/**
 * KALDRA Explorer - Sidebar Component
 * 
 * Domain filters and navigation for the Explorer.
 */

'use client';

import { ExplorerSource, ExplorerFilters } from '../lib/explorer.types';

interface ExplorerSidebarProps {
    filters: ExplorerFilters;
    onFilterChange: (filters: ExplorerFilters) => void;
    stats: {
        totalSignals: number;
        bySource: Record<ExplorerSource, number>;
    };
}

export function ExplorerSidebar({ filters, onFilterChange, stats }: ExplorerSidebarProps) {
    const sources: Array<{ id: ExplorerSource | 'all'; label: string; color: string }> = [
        { id: 'all', label: 'All Signals', color: 'bg-gray-500' },
        { id: 'alpha', label: 'KALDRA Alpha', color: 'bg-blue-500' },
        { id: 'geo', label: 'KALDRA GEO', color: 'bg-purple-500' },
        { id: 'product', label: 'KALDRA Product', color: 'bg-green-500' },
        { id: 'safeguard', label: 'KALDRA Safeguard', color: 'bg-red-500' }
    ];

    const handleSourceClick = (source: ExplorerSource | 'all') => {
        onFilterChange({ ...filters, source });
    };

    return (
        <div className="w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 p-6">
            <div className="mb-8">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    KALDRA Explorer
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                    Internal Workstation
                </p>
            </div>

            <div className="space-y-2">
                <h3 className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
                    Domains
                </h3>

                {sources.map(source => {
                    const isActive = filters.source === source.id;
                    const count = source.id === 'all'
                        ? stats.totalSignals
                        : stats.bySource[source.id as ExplorerSource] || 0;

                    return (
                        <button
                            key={source.id}
                            onClick={() => handleSourceClick(source.id)}
                            className={`
                w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-colors
                ${isActive
                                    ? 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white font-medium'
                                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50'
                                }
              `}
                        >
                            <div className="flex items-center gap-2">
                                <div className={`w-2 h-2 rounded-full ${source.color}`} />
                                <span>{source.label}</span>
                            </div>
                            <span className="text-xs text-gray-500 dark:text-gray-500">
                                {count}
                            </span>
                        </button>
                    );
                })}
            </div>

            <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-800">
                <div className="text-xs text-gray-500 dark:text-gray-400">
                    <div className="flex justify-between mb-2">
                        <span>Total Signals</span>
                        <span className="font-medium">{stats.totalSignals}</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
