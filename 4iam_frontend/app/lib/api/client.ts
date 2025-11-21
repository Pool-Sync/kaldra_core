/**
 * 4IAM.AI API Client
 * Main API client for KALDRA services
 * 
 * Current mode: MOCK DATA
 * Future mode: Real API calls via fetch/axios
 */

import type { Signal, Insight, ExplorerFeedItem, ServiceKey, ApiResponse } from './types';
import { API_CONFIG } from './config';
import {
    getMockSignals,
    getMockInsights,
    getAllMockSignals,
    getAllMockInsights,
    mockExplorerFeed,
} from './mock_data';

/**
 * API Client Interface
 * Defines all available API methods
 */
export interface ApiClient {
    // Signals
    getSignals(source?: ServiceKey): Promise<ApiResponse<Signal[]>>;
    getSignalById(id: string): Promise<ApiResponse<Signal>>;

    // Insights
    getInsights(source?: ServiceKey): Promise<ApiResponse<Insight[]>>;
    getInsightById(id: string): Promise<ApiResponse<Insight>>;

    // Explorer
    getExplorerFeed(source?: ServiceKey): Promise<ApiResponse<ExplorerFeedItem[]>>;
}

/**
 * Simulate network delay for realistic mock behavior
 */
function simulateDelay(ms: number = 300): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Create API response wrapper
 */
function createResponse<T>(data: T, source: string = 'mock'): ApiResponse<T> {
    return {
        data,
        timestamp: new Date().toISOString(),
        source,
    };
}

/**
 * Mock API Client Implementation
 * Uses local mock data instead of real API calls
 */
class MockApiClient implements ApiClient {
    async getSignals(source?: ServiceKey): Promise<ApiResponse<Signal[]>> {
        await simulateDelay();

        const signals = source ? getMockSignals(source) : getAllMockSignals();
        return createResponse(signals, source || 'all');
    }

    async getSignalById(id: string): Promise<ApiResponse<Signal>> {
        await simulateDelay();

        const allSignals = getAllMockSignals();
        const signal = allSignals.find(s => s.id === id);

        if (!signal) {
            throw new Error(`Signal not found: ${id}`);
        }

        return createResponse(signal);
    }

    async getInsights(source?: ServiceKey): Promise<ApiResponse<Insight[]>> {
        await simulateDelay();

        const insights = source ? getMockInsights(source) : getAllMockInsights();
        return createResponse(insights, source || 'all');
    }

    async getInsightById(id: string): Promise<ApiResponse<Insight>> {
        await simulateDelay();

        const allInsights = getAllMockInsights();
        const insight = allInsights.find(i => i.id === id);

        if (!insight) {
            throw new Error(`Insight not found: ${id}`);
        }

        return createResponse(insight);
    }

    async getExplorerFeed(source?: ServiceKey): Promise<ApiResponse<ExplorerFeedItem[]>> {
        await simulateDelay();

        let feed = mockExplorerFeed;

        if (source) {
            feed = feed.filter(item => item.source === source);
        }

        return createResponse(feed, source || 'all');
    }
}

/**
 * Real API Client Implementation (Future)
 * Will use fetch/axios to call KALDRA API Gateway
 * 
 * TODO: Implement when API Gateway is ready
 */
class RealApiClient implements ApiClient {
    private baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    async getSignals(source?: ServiceKey): Promise<ApiResponse<Signal[]>> {
        // TODO: Implement real API call
        // const endpoint = source ? `${this.baseUrl}/signals?source=${source}` : `${this.baseUrl}/signals`;
        // const response = await fetch(endpoint);
        // return response.json();

        throw new Error('Real API not implemented yet. Set API_CONFIG.useMocks = true');
    }

    async getSignalById(id: string): Promise<ApiResponse<Signal>> {
        // TODO: Implement real API call
        throw new Error('Real API not implemented yet. Set API_CONFIG.useMocks = true');
    }

    async getInsights(source?: ServiceKey): Promise<ApiResponse<Insight[]>> {
        // TODO: Implement real API call
        throw new Error('Real API not implemented yet. Set API_CONFIG.useMocks = true');
    }

    async getInsightById(id: string): Promise<ApiResponse<Insight>> {
        // TODO: Implement real API call
        throw new Error('Real API not implemented yet. Set API_CONFIG.useMocks = true');
    }

    async getExplorerFeed(source?: ServiceKey): Promise<ApiResponse<ExplorerFeedItem[]>> {
        // TODO: Implement real API call
        throw new Error('Real API not implemented yet. Set API_CONFIG.useMocks = true');
    }
}

/**
 * Create and export API client instance
 * Automatically switches between mock and real based on configuration
 */
export const apiClient: ApiClient = API_CONFIG.useMocks
    ? new MockApiClient()
    : new RealApiClient(API_CONFIG.baseUrl);

/**
 * Export default client
 */
export default apiClient;
