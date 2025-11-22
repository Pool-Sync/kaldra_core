"use client";

import { useState } from "react";
import { useKaldraSignal } from "../lib/hooks/useKaldraSignal";

export default function KaldraPlaygroundPage() {
    const [text, setText] = useState(
        "The CEO is optimistic about revenue growth"
    );
    const { data, isLoading, error, run } = useKaldraSignal();

    return (
        <main className="max-w-3xl mx-auto py-10 space-y-6">
            <h1 className="text-2xl font-semibold">KALDRA Engine Playground</h1>

            <textarea
                className="w-full border rounded-lg p-3 min-h-[120px]"
                value={text}
                onChange={(e) => setText(e.target.value)}
            />

            <button
                onClick={() => run(text)}
                disabled={isLoading}
                className="px-4 py-2 rounded-lg border"
            >
                {isLoading ? "Gerando sinal..." : "Gerar KALDRA Signal"}
            </button>

            {error && (
                <p className="text-red-500 text-sm">
                    Erro ao chamar API: {error}
                </p>
            )}

            {data && (
                <pre className="mt-4 text-sm bg-black text-green-300 rounded-lg p-4 overflow-auto">
                    {JSON.stringify(data, null, 2)}
                </pre>
            )}
        </main>
    );
}
