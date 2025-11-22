import { API_CONFIG } from "./config";
import type { KaldraSignalRequest, KaldraSignalResponse } from "./types";

async function handleResponse(res: Response): Promise<KaldraSignalResponse> {
    if (!res.ok) {
        const text = await res.text().catch(() => "");
        throw new Error(`KALDRA API error ${res.status}: ${text}`);
    }
    return (await res.json()) as KaldraSignalResponse;
}

export async function generateKaldraSignal(
    payload: KaldraSignalRequest
): Promise<KaldraSignalResponse> {
    const url = `${API_CONFIG.baseUrl}/engine/engine/kaldra/signal`;

    const res = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify(payload),
    });

    return handleResponse(res);
}
