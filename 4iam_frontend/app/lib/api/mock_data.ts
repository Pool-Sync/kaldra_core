/**
 * 4IAM.AI Mock Data
 * Mock data for KALDRA services (Alpha, GEO, Product, Safeguard)
 * 
 * This data simulates responses from the KALDRA API Gateway
 * When the real API is ready, this file will no longer be used
 */

import type { Signal, Insight, ExplorerFeedItem } from './types';

// ============================================================================
// ALPHA - Earnings Intelligence
// ============================================================================

export const mockAlphaSignals: Signal[] = [
    {
        id: 'alpha-001',
        title: 'Apple Q4 Earnings Beat Expectations',
        source: 'alpha',
        summary: 'Apple reported Q4 revenue of $89.5B, beating analyst estimates by 3.2%. iPhone sales drove growth with 12% YoY increase.',
        archetype_id: 3,
        delta144_state: 42,
        kindra_vector: [0.8, 0.3, 0.6],
        tw_regime: 'STABLE',
        confidence: 0.92,
        priority: 'high',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        entities: ['Apple Inc.', 'Tim Cook', 'iPhone'],
        tags: ['earnings', 'tech', 'revenue-beat'],
    },
    {
        id: 'alpha-002',
        title: 'Tesla Margin Compression Signals Shift',
        source: 'alpha',
        summary: 'Tesla gross margins declined to 17.9% from 25.1% YoY. Price cuts and increased competition impacting profitability.',
        archetype_id: 7,
        delta144_state: 89,
        kindra_vector: [0.4, 0.7, 0.3],
        tw_regime: 'TURBULENT',
        confidence: 0.87,
        priority: 'critical',
        timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
        entities: ['Tesla', 'Elon Musk'],
        tags: ['earnings', 'automotive', 'margins'],
    },
    {
        id: 'alpha-003',
        title: 'Microsoft Cloud Revenue Accelerates',
        source: 'alpha',
        summary: 'Azure revenue grew 29% YoY, driven by AI services adoption. Commercial cloud surpassed $35B quarterly run rate.',
        archetype_id: 5,
        delta144_state: 67,
        kindra_vector: [0.9, 0.2, 0.7],
        tw_regime: 'STABLE',
        confidence: 0.94,
        priority: 'medium',
        timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
        entities: ['Microsoft', 'Satya Nadella', 'Azure'],
        tags: ['earnings', 'cloud', 'AI'],
    },
    {
        id: 'alpha-004',
        title: 'Meta Advertising Revenue Rebounds',
        source: 'alpha',
        summary: 'Meta platforms ad revenue increased 23% to $31.5B. Daily active users across family of apps reached 3.14B.',
        archetype_id: 2,
        delta144_state: 28,
        tw_regime: 'STABLE',
        confidence: 0.89,
        priority: 'medium',
        timestamp: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
        entities: ['Meta', 'Mark Zuckerberg', 'Facebook', 'Instagram'],
        tags: ['earnings', 'advertising', 'social-media'],
    },
    {
        id: 'alpha-005',
        title: 'Amazon AWS Growth Slows to 12%',
        source: 'alpha',
        summary: 'AWS revenue growth decelerated to 12% YoY, lowest in company history. Enterprise customers optimizing cloud spend.',
        archetype_id: 8,
        delta144_state: 103,
        kindra_vector: [0.5, 0.6, 0.4],
        tw_regime: 'TURBULENT',
        confidence: 0.91,
        priority: 'high',
        timestamp: new Date(Date.now() - 18 * 60 * 60 * 1000).toISOString(),
        entities: ['Amazon', 'AWS', 'Andy Jassy'],
        tags: ['earnings', 'cloud', 'slowdown'],
    },
];

export const mockAlphaInsights: Insight[] = [
    {
        id: 'alpha-insight-001',
        title: 'Big Tech Earnings Season Analysis',
        subtitle: 'Q4 2024 Performance Review',
        summary: 'Comprehensive analysis of FAANG earnings reveals diverging trends in cloud, advertising, and hardware segments.',
        content: 'Full analysis content here...',
        type: 'analysis',
        source: 'alpha',
        category: 'Quarterly Review',
        author: 'KALDRA Alpha Team',
        publishedAt: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
        archetypes: [3, 5, 7],
        tags: ['earnings', 'tech', 'quarterly'],
        readTime: 12,
        views: 1247,
    },
];

// ============================================================================
// GEO - Geopolitical Intelligence
// ============================================================================

export const mockGeoSignals: Signal[] = [
    {
        id: 'geo-001',
        title: 'China-Taiwan Tensions Escalate',
        source: 'geo',
        summary: 'Increased military activity in Taiwan Strait. PLA conducted largest air drills in 6 months with 47 aircraft.',
        archetype_id: 9,
        delta144_state: 118,
        kindra_vector: [0.3, 0.9, 0.5],
        tw_regime: 'TURBULENT',
        confidence: 0.88,
        priority: 'critical',
        timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
        entities: ['China', 'Taiwan', 'PLA'],
        tags: ['geopolitical', 'military', 'asia'],
    },
    {
        id: 'geo-002',
        title: 'EU Energy Security Improves',
        source: 'geo',
        summary: 'European gas storage reaches 95% capacity ahead of winter. Diversification from Russian supply successful.',
        archetype_id: 4,
        delta144_state: 52,
        tw_regime: 'STABLE',
        confidence: 0.91,
        priority: 'medium',
        timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
        entities: ['European Union', 'Russia'],
        tags: ['energy', 'europe', 'security'],
    },
    {
        id: 'geo-003',
        title: 'Middle East Peace Talks Resume',
        source: 'geo',
        summary: 'Saudi Arabia and Iran agree to normalize relations mediated by China. Regional stability implications significant.',
        archetype_id: 6,
        delta144_state: 78,
        kindra_vector: [0.7, 0.4, 0.8],
        tw_regime: 'TURBULENT',
        confidence: 0.85,
        priority: 'high',
        timestamp: new Date(Date.now() - 10 * 60 * 60 * 1000).toISOString(),
        entities: ['Saudi Arabia', 'Iran', 'China'],
        tags: ['diplomacy', 'middle-east', 'peace'],
    },
    {
        id: 'geo-004',
        title: 'African Union Trade Agreement Expands',
        source: 'geo',
        summary: 'AfCFTA adds 5 new member states. Continental free trade zone now covers 1.3B people and $3.4T GDP.',
        archetype_id: 1,
        delta144_state: 15,
        tw_regime: 'STABLE',
        confidence: 0.82,
        priority: 'low',
        timestamp: new Date(Date.now() - 20 * 60 * 60 * 1000).toISOString(),
        entities: ['African Union', 'AfCFTA'],
        tags: ['trade', 'africa', 'economic'],
    },
];

export const mockGeoInsights: Insight[] = [
    {
        id: 'geo-insight-001',
        title: 'Global Power Dynamics Shift',
        subtitle: 'Multipolar World Order Analysis',
        summary: 'Analysis of emerging geopolitical alignments and their implications for global trade and security.',
        content: 'Full analysis content here...',
        type: 'report',
        source: 'geo',
        category: 'Strategic Analysis',
        author: 'KALDRA GEO Team',
        publishedAt: new Date(Date.now() - 48 * 60 * 60 * 1000).toISOString(),
        archetypes: [6, 9, 11],
        tags: ['geopolitics', 'strategy', 'global'],
        readTime: 18,
        views: 892,
    },
];

// ============================================================================
// PRODUCT - Product Intelligence
// ============================================================================

export const mockProductSignals: Signal[] = [
    {
        id: 'product-001',
        title: 'iPhone 15 Demand Exceeds Supply',
        source: 'product',
        summary: 'Pre-orders for iPhone 15 Pro Max sold out within 2 hours. Delivery times extended to 4-6 weeks globally.',
        archetype_id: 3,
        delta144_state: 38,
        kindra_vector: [0.9, 0.2, 0.7],
        tw_regime: 'STABLE',
        confidence: 0.95,
        priority: 'high',
        timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
        entities: ['Apple', 'iPhone 15'],
        tags: ['product-launch', 'consumer-tech', 'demand'],
    },
    {
        id: 'product-002',
        title: 'ChatGPT Enterprise Adoption Surges',
        source: 'product',
        summary: 'OpenAI reports 80% of Fortune 500 companies now using ChatGPT Enterprise. Enterprise revenue up 300% QoQ.',
        archetype_id: 5,
        delta144_state: 71,
        tw_regime: 'TURBULENT',
        confidence: 0.89,
        priority: 'critical',
        timestamp: new Date(Date.now() - 7 * 60 * 60 * 1000).toISOString(),
        entities: ['OpenAI', 'ChatGPT'],
        tags: ['AI', 'enterprise', 'adoption'],
    },
    {
        id: 'product-003',
        title: 'Tesla Cybertruck Production Ramps',
        source: 'product',
        summary: 'Tesla begins mass production of Cybertruck. Initial reviews mixed but reservation backlog exceeds 1.5M units.',
        archetype_id: 7,
        delta144_state: 95,
        kindra_vector: [0.6, 0.5, 0.6],
        tw_regime: 'TURBULENT',
        confidence: 0.84,
        priority: 'medium',
        timestamp: new Date(Date.now() - 14 * 60 * 60 * 1000).toISOString(),
        entities: ['Tesla', 'Cybertruck'],
        tags: ['automotive', 'EV', 'launch'],
    },
];

export const mockProductInsights: Insight[] = [
    {
        id: 'product-insight-001',
        title: 'AI Product Landscape 2024',
        subtitle: 'Enterprise AI Adoption Trends',
        summary: 'Comprehensive review of AI product adoption across enterprise segments and vertical markets.',
        content: 'Full analysis content here...',
        type: 'report',
        source: 'product',
        category: 'Market Analysis',
        author: 'KALDRA Product Team',
        publishedAt: new Date(Date.now() - 72 * 60 * 60 * 1000).toISOString(),
        archetypes: [5, 3],
        tags: ['AI', 'enterprise', 'trends'],
        readTime: 15,
        views: 1543,
    },
];

// ============================================================================
// SAFEGUARD - Risk Intelligence
// ============================================================================

export const mockSafeguardSignals: Signal[] = [
    {
        id: 'safeguard-001',
        title: 'Coordinated Disinformation Campaign Detected',
        source: 'safeguard',
        summary: 'Network of 2,400 fake accounts spreading false narratives about climate policy. Attribution: state-sponsored.',
        archetype_id: 10,
        delta144_state: 127,
        kindra_vector: [0.2, 0.9, 0.7],
        tw_regime: 'TURBULENT',
        confidence: 0.93,
        priority: 'critical',
        timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        entities: ['Social Media', 'Disinformation'],
        tags: ['disinformation', 'social-media', 'risk'],
    },
    {
        id: 'safeguard-002',
        title: 'Corporate Reputation Risk: Supply Chain',
        source: 'safeguard',
        summary: 'Major retailer faces backlash over labor practices in supplier factories. Social media sentiment -73%.',
        archetype_id: 11,
        delta144_state: 138,
        tw_regime: 'TURBULENT',
        confidence: 0.87,
        priority: 'high',
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
        entities: ['Retail', 'Supply Chain'],
        tags: ['reputation', 'ESG', 'labor'],
    },
    {
        id: 'safeguard-003',
        title: 'Cybersecurity Threat Level Elevated',
        source: 'safeguard',
        summary: 'New ransomware variant targeting healthcare sector. 47 hospitals affected globally in past 72 hours.',
        archetype_id: 12,
        delta144_state: 144,
        kindra_vector: [0.1, 0.8, 0.9],
        tw_regime: 'TURBULENT',
        confidence: 0.96,
        priority: 'critical',
        timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
        entities: ['Healthcare', 'Ransomware'],
        tags: ['cybersecurity', 'healthcare', 'threat'],
    },
];

export const mockSafeguardInsights: Insight[] = [
    {
        id: 'safeguard-insight-001',
        title: 'Narrative Warfare in 2024',
        subtitle: 'Disinformation Tactics and Countermeasures',
        summary: 'Analysis of evolving disinformation tactics and effective organizational response strategies.',
        content: 'Full analysis content here...',
        type: 'briefing',
        source: 'safeguard',
        category: 'Threat Intelligence',
        author: 'KALDRA Safeguard Team',
        publishedAt: new Date(Date.now() - 96 * 60 * 60 * 1000).toISOString(),
        archetypes: [10, 11, 12],
        tags: ['disinformation', 'risk', 'security'],
        readTime: 22,
        views: 678,
    },
];

// ============================================================================
// EXPLORER - Symbolic Feed
// ============================================================================

export const mockExplorerFeed: ExplorerFeedItem[] = [
    {
        id: 'explorer-001',
        title: 'Archetype Shift Detected',
        source: 'alpha',
        archetype_id: 3,
        delta144_state: 42,
        kindra_id: 'K-037',
        tw_score: 0.73,
        timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
        intensity: 0.82,
    },
    {
        id: 'explorer-002',
        title: 'Critical TW Regime',
        source: 'safeguard',
        archetype_id: 10,
        delta144_state: 127,
        kindra_id: 'K-089',
        tw_score: 0.94,
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        intensity: 0.96,
    },
    {
        id: 'explorer-003',
        title: 'Polarity Inversion',
        source: 'geo',
        archetype_id: 6,
        delta144_state: 78,
        tw_score: 0.65,
        timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
        intensity: 0.71,
    },
];

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Get all signals from a specific source
 */
export function getMockSignals(source: 'alpha' | 'geo' | 'product' | 'safeguard'): Signal[] {
    switch (source) {
        case 'alpha':
            return mockAlphaSignals;
        case 'geo':
            return mockGeoSignals;
        case 'product':
            return mockProductSignals;
        case 'safeguard':
            return mockSafeguardSignals;
    }
}

/**
 * Get all insights from a specific source
 */
export function getMockInsights(source: 'alpha' | 'geo' | 'product' | 'safeguard'): Insight[] {
    switch (source) {
        case 'alpha':
            return mockAlphaInsights;
        case 'geo':
            return mockGeoInsights;
        case 'product':
            return mockProductInsights;
        case 'safeguard':
            return mockSafeguardInsights;
    }
}

/**
 * Get all signals (combined)
 */
export function getAllMockSignals(): Signal[] {
    return [
        ...mockAlphaSignals,
        ...mockGeoSignals,
        ...mockProductSignals,
        ...mockSafeguardSignals,
    ];
}

/**
 * Get all insights (combined)
 */
export function getAllMockInsights(): Insight[] {
    return [
        ...mockAlphaInsights,
        ...mockGeoInsights,
        ...mockProductInsights,
        ...mockSafeguardInsights,
    ];
}

// ============================================================================
// KALDRA CORE Signal Mock
// ============================================================================

import type { KaldraSignal } from './types';

export function getMockKaldraSignal(text: string): KaldraSignal {
    // Mock simples baseado no tamanho do texto
    const length = Math.max(text.split(/\s+/).length, 1);
    const biasScore = Math.min(length / 50, 1);

    return {
        archetype: "UNSPECIFIED",
        delta_state: "GENERIC",
        tw_regime: biasScore > 0.5 ? "UNSTABLE" : "STABLE",
        kindra_distribution: [
            { state_index: 1, prob: 0.6 },
            { state_index: 2, prob: 0.2 },
            { state_index: 3, prob: 0.2 },
        ],
        bias_score: biasScore,
        meta_modifiers: {
            strength: [1, 2, 3],
            journey: [2, 3, 4],
            discipline: [1.5, 1.5, 1.5],
        },
        confidence: 0.8,
        explanation: "Mock KALDRA signal generated locally (useMocks = true).",
        bias_label: biasScore > 0.7 ? "extreme" : biasScore > 0.4 ? "negative" : "neutral",
        narrative_risk: biasScore > 0.7 ? 0.9 : biasScore > 0.4 ? 0.5 : 0.1,
    };
}
