// app/lib/api/client.ts

import { API_CONFIG } from "./config";
import { KaldraSignal } from "./types";
import { getMockKaldraSignal } from "./mock_data";

export class ApiError extends Error {
    status?: number;
    constructor(message: string, status?: number) {
        super(message);
        this.name = "ApiError";
        this.status = status;
    }
}

async function fetchJson<T>(
    path: string,
    options: RequestInit = {},
): Promise<T> {
    const controller = new AbortController();
    const timeout = setTimeout(
        () => controller.abort(),
        API_CONFIG.timeoutMs || 15000,
    );

    try {
        const res = await fetch(`${API_CONFIG.baseUrl}${path}`, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {}),
            },
            signal: controller.signal,
        });

        if (!res.ok) {
            const text = await res.text().catch(() => "");
            throw new ApiError(
                `API error ${res.status}: ${text || res.statusText}`,
                res.status,
            );
        }

        return (await res.json()) as T;
    } finally {
        clearTimeout(timeout);
    }
}

/**
 * Call the real KALDRA API when useMocks === false.
 * Fallback to mock implementation otherwise.
 */
export async function getKaldraSignal(text: string): Promise<KaldraSignal> {
    const trimmed = text.trim();
    if (!trimmed) {
        throw new ApiError("Input text must not be empty.");
    }

    if (API_CONFIG.useMocks) {
        return getMockKaldraSignal(trimmed);
    }

    return fetchJson<KaldraSignal>("/engine/kaldra/signal", {
        method: "POST",
        body: JSON.stringify({ text: trimmed }),
    });
}
