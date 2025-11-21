/**
 * 4IAM.AI — Signals Page with Mock Data Integration
 * Status: Mock data integration — real-time intelligence signals feed
 * 
 * This page displays all KALDRA signals with filtering
 */

'use client';

import { useState } from 'react';
import { useSignals } from '../hooks/useSignals';
import type { ServiceKey } from '../lib/api/types';

export default function SignalsPage() {
    const [selectedSource, setSelectedSource] = useState<ServiceKey | undefined>(undefined);
    const { signals, loading, error } = useSignals(selectedSource);

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">KALDRA Signals</h1>
            <p className="text-gray-600 mb-8">Real-time Intelligence Signals</p>

            {/* Filter Controls */}
            <div className="mb-6 flex gap-2">
                <button
                    onClick={() => setSelectedSource(undefined)}
                    className={`px-4 py-2 rounded ${selectedSource === undefined
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}
                >
                    All
                </button>
                <button
                    onClick={() => setSelectedSource('alpha')}
                    className={`px-4 py-2 rounded ${selectedSource === 'alpha'
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}
                >
                    Alpha
                </button>
                <button
                    onClick={() => setSelectedSource('geo')}
                    className={`px-4 py-2 rounded ${selectedSource === 'geo'
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}
                >
                    GEO
                </button>
                <button
                    onClick={() => setSelectedSource('product')}
                    className={`px-4 py-2 rounded ${selectedSource === 'product'
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}
                >
                    Product
                </button>
                <button
                    onClick={() => setSelectedSource('safeguard')}
                    className={`px-4 py-2 rounded ${selectedSource === 'safeguard'
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}
                >
                    Safeguard
                </button>
            </div>

            {/* Signals Feed */}
            {loading && (
                <div className="text-gray-500">Loading signals...</div>
            )}

            {error && (
                <div className="text-red-500">Error loading signals: {error.message}</div>
            )}

            {!loading && !error && (
                <div className="grid gap-4">
                    {signals.map((signal) => (
                        <div key={signal.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                            <div className="flex items-start justify-between mb-2">
                                <div>
                                    <span className="text-xs font-medium text-gray-500 uppercase">{signal.source}</span>
                                    <h3 className="text-lg font-semibold">{signal.title}</h3>
                                </div>
                                <span className={`px-2 py-1 rounded text-xs font-medium ${signal.priority === 'critical' ? 'bg-red-100 text-red-800' :
                                        signal.priority === 'high' ? 'bg-orange-100 text-orange-800' :
                                            signal.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                                                'bg-gray-100 text-gray-800'
                                    }`}>
                                    {signal.priority.toUpperCase()}
                                </span>
                            </div>

                            <p className="text-gray-700 mb-3">{signal.summary}</p>

                            <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                                <div>
                                    <span className="font-medium">Archetype:</span> #{signal.archetype_id}
                                </div>
                                <div>
                                    <span className="font-medium">Δ144 State:</span> {signal.delta144_state}
                                </div>
                                <div>
                                    <span className="font-medium">TW Regime:</span>{' '}
                                    <span className={`font-medium ${signal.tw_regime === 'CRITICAL' ? 'text-red-600' :
                                            signal.tw_regime === 'TURBULENT' ? 'text-orange-600' :
                                                'text-green-600'
                                        }`}>
                                        {signal.tw_regime}
                                    </span>
                                </div>
                                <div>
                                    <span className="font-medium">Confidence:</span> {(signal.confidence * 100).toFixed(0)}%
                                </div>
                            </div>

                            {signal.entities && signal.entities.length > 0 && (
                                <div className="mt-3 flex flex-wrap gap-2">
                                    {signal.entities.map((entity, idx) => (
                                        <span key={idx} className="px-2 py-1 bg-blue-50 text-blue-700 rounded text-xs">
                                            {entity}
                                        </span>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}

            {!loading && !error && signals.length === 0 && (
                <div className="text-center py-12 text-gray-500">
                    No signals found for the selected filter.
                </div>
            )}
        </div>
    );
}
