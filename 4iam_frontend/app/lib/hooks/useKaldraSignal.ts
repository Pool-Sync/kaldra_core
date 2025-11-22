"use client";

import { useState } from "react";
import { generateKaldraSignal } from "../api/kaldra";
import type { KaldraSignalResponse } from "../api/types";

export function useKaldraSignal() {
    const [data, setData] = useState<KaldraSignalResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function run(text: string) {
        setLoading(true);
        setError(null);
        try {
            const res = await generateKaldraSignal({ text });
            setData(res);
        } catch (err: any) {
            setError(err.message ?? "Unknown error");
        } finally {
            setLoading(false);
        }
    }

    return { data, loading, error, run };
}
