/**
 * 4IAM.AI API Configuration
 * Endpoint configuration for KALDRA services
 */

import type { ServiceKey } from './types';

/**
 * API Endpoint Configuration
 * These paths will be used when switching from mocks to real API calls
 */
export const API_ENDPOINTS: Record<ServiceKey, { basePath: string }> = {
    alpha: { basePath: '/api/alpha' },
    geo: { basePath: '/api/geo' },
    product: { basePath: '/api/product' },
    safeguard: { basePath: '/api/safeguard' },
};

/**
 * API Configuration
 */
export const API_CONFIG = {
    // Base URL for API Gateway (will be used when switching to real API)
    baseUrl: process.env.NEXT_PUBLIC_KALDRA_API_URL ||
        process.env.NEXT_PUBLIC_API_URL ||
        'http://localhost:8000',

    // Timeout for API requests (ms)
    timeout: 15000,
    timeoutMs: 15000,

    // Enable mock mode (true = use mocks, false = use real API)
    useMocks: process.env.NEXT_PUBLIC_USE_MOCKS === 'true',

    // Retry configuration
    retry: {
        maxAttempts: 3,
        delay: 1000,
    },
};

/**
 * Service display names
 */
export const SERVICE_NAMES: Record<ServiceKey, string> = {
    alpha: 'KALDRA Alpha',
    geo: 'KALDRA GEO',
    product: 'KALDRA Product',
    safeguard: 'KALDRA Safeguard',
};

/**
 * Service descriptions
 */
export const SERVICE_DESCRIPTIONS: Record<ServiceKey, string> = {
    alpha: 'Earnings Intelligence & Market Analysis',
    geo: 'Geopolitical Intelligence & Risk Analysis',
    product: 'Product Intelligence & Market Trends',
    safeguard: 'Risk Intelligence & Narrative Monitoring',
};
