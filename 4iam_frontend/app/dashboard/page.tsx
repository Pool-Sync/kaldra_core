/**
 * 4IAM.AI — Dashboard Page with Mock Data Integration
 * Status: Mock data integration — unified view of all KALDRA products
 * 
 * This is the main unified dashboard showing overview of all products
 */

'use client';

import { useSignals } from '../hooks/useSignals';

export default function DashboardPage() {
    // Fetch signals from all sources
    const { signals, loading, error } = useSignals();

    // Calculate metrics
    const criticalSignals = signals.filter(s => s.priority === 'critical').length;
    const twCritical = signals.filter(s => s.tw_regime === 'CRITICAL').length;
    const twTurbulent = signals.filter(s => s.tw_regime === 'TURBULENT').length;
    const twStable = signals.filter(s => s.tw_regime === 'STABLE').length;

    // Group signals by source
    const signalsBySource = {
        alpha: signals.filter(s => s.source === 'alpha'),
        geo: signals.filter(s => s.source === 'geo'),
        product: signals.filter(s => s.source === 'product'),
        safeguard: signals.filter(s => s.source === 'safeguard'),
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">KALDRA Dashboard</h1>
            <p className="text-gray-600 mb-8">Unified Intelligence Platform</p>

            {/* Metrics Overview */}
            <section className="mb-8">
                <h2 className="text-2xl font-semibold mb-4">Overview</h2>

                {loading && (
                    <div className="text-gray-500">Loading dashboard...</div>
                )}

                {error && (
                    <div className="text-red-500">Error loading dashboard: {error.message}</div>
                )}

                {!loading && !error && (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                        <div className="border rounded-lg p-4">
                            <div className="text-sm text-gray-600 mb-1">Total Signals</div>
                            <div className="text-3xl font-bold">{signals.length}</div>
                        </div>

                        <div className="border rounded-lg p-4">
                            <div className="text-sm text-gray-600 mb-1">Critical Priority</div>
                            <div className="text-3xl font-bold text-red-600">{criticalSignals}</div>
                        </div>

                        <div className="border rounded-lg p-4">
                            <div className="text-sm text-gray-600 mb-1">TW Critical</div>
                            <div className="text-3xl font-bold text-red-600">{twCritical}</div>
                        </div>

                        <div className="border rounded-lg p-4">
                            <div className="text-sm text-gray-600 mb-1">TW Turbulent</div>
                            <div className="text-3xl font-bold text-orange-600">{twTurbulent}</div>
                        </div>
                    </div>
                )}
            </section>

            {/* Product Summaries */}
            <section className="mb-8">
                <h2 className="text-2xl font-semibold mb-4">Product Summaries</h2>

                {!loading && !error && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Alpha */}
                        <div className="border rounded-lg p-4">
                            <h3 className="text-lg font-semibold mb-2">KALDRA Alpha</h3>
                            <p className="text-sm text-gray-600 mb-3">Earnings Intelligence</p>
                            <div className="text-2xl font-bold mb-2">{signalsBySource.alpha.length} signals</div>
                            <div className="text-sm text-gray-600">
                                {signalsBySource.alpha.filter(s => s.priority === 'critical').length} critical
                            </div>
                        </div>

                        {/* GEO */}
                        <div className="border rounded-lg p-4">
                            <h3 className="text-lg font-semibold mb-2">KALDRA GEO</h3>
                            <p className="text-sm text-gray-600 mb-3">Geopolitical Intelligence</p>
                            <div className="text-2xl font-bold mb-2">{signalsBySource.geo.length} signals</div>
                            <div className="text-sm text-gray-600">
                                {signalsBySource.geo.filter(s => s.priority === 'critical').length} critical
                            </div>
                        </div>

                        {/* Product */}
                        <div className="border rounded-lg p-4">
                            <h3 className="text-lg font-semibold mb-2">KALDRA Product</h3>
                            <p className="text-sm text-gray-600 mb-3">Product Intelligence</p>
                            <div className="text-2xl font-bold mb-2">{signalsBySource.product.length} signals</div>
                            <div className="text-sm text-gray-600">
                                {signalsBySource.product.filter(s => s.priority === 'critical').length} critical
                            </div>
                        </div>

                        {/* Safeguard */}
                        <div className="border rounded-lg p-4">
                            <h3 className="text-lg font-semibold mb-2">KALDRA Safeguard</h3>
                            <p className="text-sm text-gray-600 mb-3">Risk Intelligence</p>
                            <div className="text-2xl font-bold mb-2">{signalsBySource.safeguard.length} signals</div>
                            <div className="text-sm text-gray-600">
                                {signalsBySource.safeguard.filter(s => s.priority === 'critical').length} critical
                            </div>
                        </div>
                    </div>
                )}
            </section>

            {/* Recent Signals */}
            <section>
                <h2 className="text-2xl font-semibold mb-4">Recent Signals (All Products)</h2>

                {!loading && !error && (
                    <div className="grid gap-4">
                        {signals.slice(0, 5).map((signal) => (
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
                            </div>
                        ))}
                    </div>
                )}
            </section>
        </div>
    );
}
