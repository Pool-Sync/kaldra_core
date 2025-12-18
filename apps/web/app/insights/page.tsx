/**
 * 4IAM.AI — Insights Page with Mock Data Integration
 * Status: Mock data integration — intelligence reports and analysis library
 * 
 * This page displays all KALDRA insights with filtering
 */

'use client';

import { useState } from 'react';
import { useInsights } from '../hooks/useInsights';
import type { ServiceKey } from '../lib/api/types';

export default function InsightsPage() {
    const [selectedSource, setSelectedSource] = useState<ServiceKey | undefined>(undefined);
    const { insights, loading, error } = useInsights(selectedSource);

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">KALDRA Insights</h1>
            <p className="text-gray-600 mb-8">Intelligence Reports & Analysis</p>

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

            {/* Insights Library */}
            {loading && (
                <div className="text-gray-500">Loading insights...</div>
            )}

            {error && (
                <div className="text-red-500">Error loading insights: {error.message}</div>
            )}

            {!loading && !error && (
                <div className="grid gap-6">
                    {insights.map((insight) => (
                        <div key={insight.id} className="border rounded-lg p-6 hover:shadow-md transition-shadow">
                            <div className="mb-3">
                                <span className="text-xs font-medium text-gray-500 uppercase">{insight.source}</span>
                                <span className="mx-2 text-gray-300">•</span>
                                <span className="text-xs font-medium text-gray-500 uppercase">{insight.type}</span>
                            </div>

                            <h3 className="text-2xl font-semibold mb-2">{insight.title}</h3>

                            {insight.subtitle && (
                                <p className="text-lg text-gray-600 mb-3">{insight.subtitle}</p>
                            )}

                            <p className="text-gray-700 mb-4">{insight.summary}</p>

                            <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
                                <span>{insight.author}</span>
                                <span>•</span>
                                <span>{insight.readTime} min read</span>
                                <span>•</span>
                                <span>{insight.views} views</span>
                                <span>•</span>
                                <span>{new Date(insight.publishedAt).toLocaleDateString()}</span>
                            </div>

                            {insight.tags && insight.tags.length > 0 && (
                                <div className="flex flex-wrap gap-2">
                                    {insight.tags.map((tag, idx) => (
                                        <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                                            {tag}
                                        </span>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}

            {!loading && !error && insights.length === 0 && (
                <div className="text-center py-12 text-gray-500">
                    No insights found for the selected filter.
                </div>
            )}
        </div>
    );
}
