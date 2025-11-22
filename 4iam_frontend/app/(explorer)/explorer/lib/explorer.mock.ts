/**
 * KALDRA Explorer - Mock Data
 * 
 * Realistic mock signals for development and testing.
 * In production, this will be replaced by API Gateway calls.
 */

import { ExplorerSignal } from './explorer.types';

/**
 * Generate mock signals across all KALDRA domains
 */
export const explorerMockSignals: ExplorerSignal[] = [
    // ALPHA Signals (Earnings)
    {
        id: 'alpha_001',
        source: 'alpha',
        title: 'NVDA Q4 Earnings Beat - AI Demand Surge',
        summary: 'NVIDIA reports 265% YoY revenue growth driven by datacenter AI chips. Guidance exceeds expectations, signaling sustained AI infrastructure buildout.',
        archetype_id: 'ARC_001',
        delta144_state: 'Δ_089',
        kindra_vector: 'K_EXPANSION_HIGH',
        tw_regime: 'TURBULENT',
        confidence: 0.92,
        timestamp: '2025-11-20T14:30:00Z'
    },
    {
        id: 'alpha_002',
        source: 'alpha',
        title: 'TSLA Margin Compression Warning',
        summary: 'Tesla automotive margins decline to 16.3% amid price cuts and competitive pressure. Energy storage segment shows strength but insufficient to offset.',
        archetype_id: 'ARC_045',
        delta144_state: 'Δ_112',
        kindra_vector: 'K_CONTRACTION_MED',
        tw_regime: 'CRITICAL',
        confidence: 0.87,
        timestamp: '2025-11-19T16:45:00Z'
    },
    {
        id: 'alpha_003',
        source: 'alpha',
        title: 'META Ad Revenue Stabilization',
        summary: 'Meta Platforms shows resilient ad pricing despite macro headwinds. Reality Labs losses narrow, suggesting path to profitability.',
        archetype_id: 'ARC_023',
        delta144_state: 'Δ_067',
        kindra_vector: 'K_STABLE_HIGH',
        tw_regime: 'STABLE',
        confidence: 0.78,
        timestamp: '2025-11-18T13:20:00Z'
    },
    {
        id: 'alpha_004',
        source: 'alpha',
        title: 'JPM Net Interest Income Pressure',
        summary: 'JPMorgan Chase faces NII headwinds as deposit costs rise faster than loan yields. Trading revenue provides partial offset.',
        archetype_id: 'ARC_098',
        delta144_state: 'Δ_134',
        kindra_vector: 'K_DRIFT_NEGATIVE',
        tw_regime: 'TURBULENT',
        confidence: 0.84,
        timestamp: '2025-11-17T11:00:00Z'
    },
    {
        id: 'alpha_005',
        source: 'alpha',
        title: 'AAPL Services Growth Acceleration',
        summary: 'Apple Services revenue grows 16% YoY, now representing 24% of total revenue. Subscription base reaches 1B users.',
        archetype_id: 'ARC_012',
        delta144_state: 'Δ_056',
        kindra_vector: 'K_EXPANSION_MED',
        tw_regime: 'STABLE',
        confidence: 0.91,
        timestamp: '2025-11-16T15:30:00Z'
    },

    // GEO Signals (Geopolitics)
    {
        id: 'geo_001',
        source: 'geo',
        title: 'US-China Tech Decoupling Accelerates',
        summary: 'New semiconductor export controls target AI chips and manufacturing equipment. China announces $50B domestic chip fund in response.',
        archetype_id: 'ARC_078',
        delta144_state: 'Δ_121',
        kindra_vector: 'K_POLARIZATION_HIGH',
        tw_regime: 'CRITICAL',
        confidence: 0.95,
        timestamp: '2025-11-20T09:15:00Z'
    },
    {
        id: 'geo_002',
        source: 'geo',
        title: 'EU AI Act Implementation Timeline',
        summary: 'European Parliament finalizes AI Act enforcement schedule. High-risk AI systems face compliance deadline of Q2 2026.',
        archetype_id: 'ARC_034',
        delta144_state: 'Δ_078',
        kindra_vector: 'K_REGULATION_TIGHTENING',
        tw_regime: 'TURBULENT',
        confidence: 0.88,
        timestamp: '2025-11-19T10:30:00Z'
    },
    {
        id: 'geo_003',
        source: 'geo',
        title: 'OPEC+ Production Cut Extension',
        summary: 'Saudi Arabia and Russia agree to extend 2M bpd production cuts through Q1 2026. Oil prices rally 8% on announcement.',
        archetype_id: 'ARC_056',
        delta144_state: 'Δ_092',
        kindra_vector: 'K_SUPPLY_CONSTRAINT',
        tw_regime: 'TURBULENT',
        confidence: 0.82,
        timestamp: '2025-11-18T07:45:00Z'
    },
    {
        id: 'geo_004',
        source: 'geo',
        title: 'India Digital Infrastructure Push',
        summary: 'India announces $30B digital infrastructure investment targeting 5G rollout and data center capacity. Aims to position as AI hub.',
        archetype_id: 'ARC_019',
        delta144_state: 'Δ_043',
        kindra_vector: 'K_INFRASTRUCTURE_BUILD',
        tw_regime: 'STABLE',
        confidence: 0.76,
        timestamp: '2025-11-17T12:00:00Z'
    },
    {
        id: 'geo_005',
        source: 'geo',
        title: 'Taiwan Strait Tensions Escalate',
        summary: 'Increased military exercises in Taiwan Strait raise semiconductor supply chain concerns. TSMC contingency planning intensifies.',
        archetype_id: 'ARC_103',
        delta144_state: 'Δ_138',
        kindra_vector: 'K_GEOPOLITICAL_RISK',
        tw_regime: 'CRITICAL',
        confidence: 0.89,
        timestamp: '2025-11-16T08:20:00Z'
    },

    // PRODUCT Signals (Brand/Consumer)
    {
        id: 'product_001',
        source: 'product',
        title: 'Nike DTC Strategy Pivot',
        summary: 'Nike reverses wholesale retreat, re-engaging with Foot Locker and Dick\'s. DTC-only approach proves unsustainable amid competition.',
        archetype_id: 'ARC_067',
        delta144_state: 'Δ_105',
        kindra_vector: 'K_STRATEGY_SHIFT',
        tw_regime: 'TURBULENT',
        confidence: 0.81,
        timestamp: '2025-11-20T11:30:00Z'
    },
    {
        id: 'product_002',
        source: 'product',
        title: 'Ozempic Cultural Moment Peak',
        summary: 'GLP-1 drugs reach cultural saturation point. Search interest plateaus, suggesting market maturation. Adjacent industries (fitness, food) adapt.',
        archetype_id: 'ARC_029',
        delta144_state: 'Δ_072',
        kindra_vector: 'K_CULTURAL_PEAK',
        tw_regime: 'STABLE',
        confidence: 0.74,
        timestamp: '2025-11-19T14:15:00Z'
    },
    {
        id: 'product_003',
        source: 'product',
        title: 'Shein Fast Fashion Backlash',
        summary: 'Sustainability concerns and labor practice scrutiny intensify. Gen Z sentiment shifts toward "slow fashion" alternatives.',
        archetype_id: 'ARC_087',
        delta144_state: 'Δ_126',
        kindra_vector: 'K_REPUTATION_DECLINE',
        tw_regime: 'CRITICAL',
        confidence: 0.79,
        timestamp: '2025-11-18T16:00:00Z'
    },
    {
        id: 'product_004',
        source: 'product',
        title: 'Liquid Death Brand Momentum',
        summary: 'Canned water brand achieves $1.4B valuation. Irreverent marketing resonates with younger demographics, challenging traditional beverage players.',
        archetype_id: 'ARC_014',
        delta144_state: 'Δ_038',
        kindra_vector: 'K_DISRUPTOR_RISE',
        tw_regime: 'STABLE',
        confidence: 0.72,
        timestamp: '2025-11-17T09:45:00Z'
    },
    {
        id: 'product_005',
        source: 'product',
        title: 'Luxury Resale Market Maturation',
        summary: 'TheRealReal and Vestiaire Collective show slowing growth. Luxury resale transitions from high-growth to steady-state market.',
        archetype_id: 'ARC_051',
        delta144_state: 'Δ_084',
        kindra_vector: 'K_MARKET_MATURITY',
        tw_regime: 'TURBULENT',
        confidence: 0.77,
        timestamp: '2025-11-16T13:30:00Z'
    },

    // SAFEGUARD Signals (Toxic Narratives)
    {
        id: 'safeguard_001',
        source: 'safeguard',
        title: 'AI Deepfake Election Interference',
        summary: 'Coordinated deepfake campaign targeting upcoming elections detected. Multi-platform spread suggests state-actor involvement.',
        archetype_id: 'ARC_109',
        delta144_state: 'Δ_142',
        kindra_vector: 'K_DISINFO_SURGE',
        tw_regime: 'CRITICAL',
        confidence: 0.94,
        timestamp: '2025-11-20T17:00:00Z'
    },
    {
        id: 'safeguard_002',
        source: 'safeguard',
        title: 'Crypto Scam Network Expansion',
        summary: 'Pig butchering scams evolve with AI-generated personas. Estimated $3B in losses YTD, up 180% from prior year.',
        archetype_id: 'ARC_092',
        delta144_state: 'Δ_131',
        kindra_vector: 'K_FRAUD_ESCALATION',
        tw_regime: 'CRITICAL',
        confidence: 0.91,
        timestamp: '2025-11-19T12:45:00Z'
    },
    {
        id: 'safeguard_003',
        source: 'safeguard',
        title: 'Health Misinformation Cluster',
        summary: 'Anti-vaccine narratives resurge on alternative platforms. Measles outbreak correlation observed in high-misinformation regions.',
        archetype_id: 'ARC_076',
        delta144_state: 'Δ_118',
        kindra_vector: 'K_HEALTH_MISINFO',
        tw_regime: 'TURBULENT',
        confidence: 0.86,
        timestamp: '2025-11-18T10:20:00Z'
    },
    {
        id: 'safeguard_004',
        source: 'safeguard',
        title: 'Financial Doom Narrative Spike',
        summary: 'Coordinated "imminent collapse" narratives across social platforms. Sentiment analysis shows bot amplification patterns.',
        archetype_id: 'ARC_084',
        delta144_state: 'Δ_123',
        kindra_vector: 'K_PANIC_AMPLIFICATION',
        tw_regime: 'TURBULENT',
        confidence: 0.83,
        timestamp: '2025-11-17T15:10:00Z'
    },
    {
        id: 'safeguard_005',
        source: 'safeguard',
        title: 'Synthetic Identity Fraud Wave',
        summary: 'AI-generated synthetic identities used for credit fraud increase 340%. Traditional verification systems prove inadequate.',
        archetype_id: 'ARC_101',
        delta144_state: 'Δ_137',
        kindra_vector: 'K_IDENTITY_THREAT',
        tw_regime: 'CRITICAL',
        confidence: 0.90,
        timestamp: '2025-11-16T11:55:00Z'
    }
];

/**
 * Get all mock signals
 */
export function getAllMockSignals(): ExplorerSignal[] {
    return explorerMockSignals;
}

/**
 * Get mock signal by ID
 */
export function getMockSignalById(id: string): ExplorerSignal | null {
    return explorerMockSignals.find(signal => signal.id === id) || null;
}

/**
 * Get mock signals by source
 */
export function getMockSignalsBySource(source: string): ExplorerSignal[] {
    if (source === 'all') return explorerMockSignals;
    return explorerMockSignals.filter(signal => signal.source === source);
}
