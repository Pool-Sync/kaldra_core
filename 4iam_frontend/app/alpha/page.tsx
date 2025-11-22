// app/alpha/page.tsx
"use client";

import { useKaldraSignal } from "@/app/lib/hooks/useKaldraSignal";
import { KaldraSignalCard } from "@/components/kaldra/KaldraSignalCard";
import { KaldraSignalDistribution } from "@/components/kaldra/KaldraSignalDistribution";

export default function AlphaPage() {
    const { text, setText, data, isLoading, error, run } = useKaldraSignal();

    return (
        <main className="flex flex-col gap-6 p-6">
            <header className="space-y-1">
                <h1 className="text-2xl font-semibold text-slate-50">
                    KALDRA-ALPHA — Earnings Signals
                </h1>
                <p className="text-sm text-slate-400">
                    Envie um trecho de earnings call e veja o sinal KALDRA em tempo real.
                </p>
            </header>

            <section className="grid gap-4 md:grid-cols-[minmax(0,2fr)_minmax(0,3fr)]">
                <div className="space-y-3">
                    <label className="text-xs font-medium text-slate-300">
                        Earnings call transcript
                    </label>
                    <textarea
                        className="h-40 w-full rounded-xl border border-slate-800 bg-slate-950/80 p-3 text-sm text-slate-100 outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="Exemplo de earnings call para o KALDRA-ALPHA."
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
                        </>
                    ) : (
                        <div className="rounded-xl border border-dashed border-slate-700 bg-slate-950/60 p-4 text-sm text-slate-400">
                            Nenhum sinal gerado ainda. Envie um texto para ver o KALDRA
                            Signal.
                        </div>
                    )}
                </div>
            </section>
        </main>
    );
}
