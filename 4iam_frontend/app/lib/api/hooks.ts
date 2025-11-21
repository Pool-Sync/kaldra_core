// app/lib/api/hooks.ts
"use client";

import { useCallback, useState } from "react";
import { getKaldraSignal } from "./kaldra_client";
import type { KaldraSignal } from "./types";

interface UseKaldraSignalOptions {
    auto?: boolean;
}

export function useKaldraSignal(
    initialText: string = "",
    options: UseKaldraSignalOptions = {},
) {
    const [text, setText] = useState(initialText);
    const [data, setData] = useState<KaldraSignal | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);

    const run = useCallback(
        async (overrideText?: string) => {
            const payload = (overrideText ?? text).trim();
            if (!payload) return;

            setIsLoading(true);
            setError(null);

            try {
                const result = await getKaldraSignal(payload);
                setData(result);
            } catch (err) {
                setError(err as Error);
            } finally {
                setIsLoading(false);
            }
        },
        [text],
    );

    // Se quiser, no futuro dá para ativar auto-run com useEffect quando options.auto === true.

    return {
        text,
        setText,
        data,
        isLoading,
        error,
        run,
    };
}
