// app/safeguard/page.tsx
"use client";

import { useState } from "react";
import { useKaldraSignal } from "@/app/lib/api/hooks";
import { KaldraSignalCard } from "@/components/kaldra/KaldraSignalCard";
import { KaldraSignalDistribution } from "@/components/kaldra/KaldraSignalDistribution";

export default function SafeguardPage() {
    const [input, setInput] = useState(
        "Exemplo de narrativa para monitoramento pelo KALDRA-SAFEGUARD.",
    );
    const { text, setText, data, isLoading, error, run } = useKaldraSignal(input);

    const risk = data?.narrative_risk ?? "n/d";

    return (
        <main className="flex flex-col gap-6 p-6">
            <header className="space-y-1">
                <h1 className="text-2xl font-semibold text-slate-50">
                    KALDRA-SAFEGUARD — Narrative Guard
                </h1>
                <p className="text-sm text-slate-400">
                    Use o KALDRA CORE para monitorar riscos narrativos e viés extremo.
                </p>
            </header>

            <section className="grid gap-4 md:grid-cols-[minmax(0,2fr)_minmax(0,3fr)]">
                <div className="space-y-3">
                    <label className="text-xs font-medium text-slate-300">
                        Narrative text
                    </label>
                    <textarea
                        className="h-40 w-full rounded-xl border border-slate-800 bg-slate-950/80 p-3 text-sm text-slate-100 outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500"
                        value={text || input}
                        onChange={(e) => {
                            setText(e.target.value);
                            setInput(e.target.value);
                        }}
                    />
                    <button
                        type="button"
                        onClick={() => run()}
                        disabled={isLoading}
                        className="inline-flex items-center justify-center rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500 disabled:opacity-60"
                    >
                        {isLoading ? "Analyzing..." : "Generate KALDRA Signal"}
                    </button>
                    {error && (
                        <p className="text-xs text-red-400 mt-1">
                            {error.message || "Unexpected error"}
                        </p>
                    )}
                </div>

                <div className="space-y-4">
                    {data ? (
                        <>
                            <KaldraSignalCard signal={data} />
                            <KaldraSignalDistribution signal={data} />
                            <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-3 text-xs text-slate-300">
                                <div className="font-semibold text-slate-100">
                                    Narrative risk level: {risk}
                                </div>
                                <p className="mt-1 text-slate-400">
                                    Este nível é derivado do bias_score e do regime TW. A lógica
                                    detalhada será refinada em versões futuras.
                                </p>
                            </div>
                        </>
                    ) : (
                        <div className="rounded-xl border border-dashed border-slate-700 bg-slate-950/60 p-4 text-sm text-slate-400">
                            Nenhum sinal gerado ainda. Envie um texto para avaliar o risco
                            narrativo.
                        </div>
                    )}
                </div>
            </section>
        </main>
    );
}
