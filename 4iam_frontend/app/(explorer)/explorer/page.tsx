/**
 * KALDRA Explorer - Main Page
 * 
 * Internal workstation for navigating KALDRA signals across all domains.
 */

'use client';

import { useExplorer } from '@/app/hooks/useExplorer';
import { ExplorerSidebar } from './components/ExplorerSidebar';
import { ExplorerTimeline } from './components/ExplorerTimeline';
import { ExplorerList } from './components/ExplorerList';
import { ExplorerDetails } from './components/ExplorerDetails';

export default function ExplorerPage() {
    const {
        signals,
        timeline,
        stats,
        selectedSignal,
        filters,
        setFilters,
        setSelectedSignalId,
        clearSelection
    } = useExplorer();

    return (
        <div className="flex h-screen">
            {/* Sidebar */}
            <ExplorerSidebar
                filters={filters}
                onFilterChange={setFilters}
                stats={stats}
            />

            {/* Main Content */}
            <div className="flex-1 overflow-y-auto">
                <div className="max-w-6xl mx-auto p-8">
                    {/* Header */}
                    <div className="mb-8">
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                            KALDRA Explorer
                        </h1>
                        <p className="text-gray-600 dark:text-gray-400">
                            Navigate signals across Alpha, GEO, Product, and Safeguard domains
                        </p>
                    </div>

                    {/* Timeline */}
                    <div className="mb-6">
                        <ExplorerTimeline timeline={timeline} />
                    </div>

                    {/* Stats Bar */}
                    <div className="mb-6 grid grid-cols-4 gap-4">
                        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                            <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Total Signals</div>
                            <div className="text-2xl font-bold text-gray-900 dark:text-white">{stats.totalSignals}</div>
                        </div>
                        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                            <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Stable</div>
                            <div className="text-2xl font-bold text-green-600">{stats.byRegime.STABLE}</div>
                        </div>
                        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                            <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Turbulent</div>
                            <div className="text-2xl font-bold text-yellow-600">{stats.byRegime.TURBULENT}</div>
                        </div>
                        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                            <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">Critical</div>
                            <div className="text-2xl font-bold text-red-600">{stats.byRegime.CRITICAL}</div>
                        </div>
                    </div>

                    {/* Signal List */}
                    <ExplorerList
                        signals={signals}
                        onSignalClick={(signal) => setSelectedSignalId(signal.id)}
                        selectedSignalId={selectedSignal?.id}
                    />
                </div>
            </div>

            {/* Details Modal */}
            <ExplorerDetails
                signal={selectedSignal}
                onClose={clearSelection}
            />
        </div>
    );
}
