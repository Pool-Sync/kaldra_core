// components/kaldra/KaldraSignalCard.tsx
"use client";

import type { KaldraSignal } from "@/app/lib/api/types";

interface Props {
    signal: KaldraSignal;
}

export function KaldraSignalCard({ signal }: Props) {
    const regimeColor =
        signal.tw_regime === "UNSTABLE"
            ? "bg-red-500"
            : signal.tw_regime === "CRITICAL"
                ? "bg-amber-500"
                : "bg-emerald-500";

    const biasPercent = Math.round(signal.bias_score * 100);
    const confidencePercent = Math.round(signal.confidence * 100);

    return (
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 shadow-md space-y-3">
            <div className="flex items-center justify-between gap-4">
                <div>
                    <div className="text-xs uppercase tracking-wide text-slate-400">
                        KALDRA Signal
                    </div>
                    <div className="text-lg font-semibold text-slate-50">
                        {signal.archetype || "Archetype: n/d"}
                    </div>
                    <div className="text-xs text-slate-400">
                        Delta state:{" "}
                        <span className="font-mono text-slate-200">
                            {signal.delta_state}
                        </span>
                    </div>
                </div>
                <div className="flex flex-col items-end gap-1">
                    <div className="text-xs uppercase text-slate-400">TW Regime</div>
                    <div className="inline-flex items-center gap-2 rounded-full bg-slate-800 px-3 py-1">
                        <span className={`h-2 w-2 rounded-full ${regimeColor}`} />
                        <span className="text-xs font-semibold text-slate-50">
                            {signal.tw_regime}
                        </span>
                    </div>
                    {signal.bias_label && (
                        <div className="text-[10px] uppercase tracking-wide text-slate-400">
                            Bias: {signal.bias_label}
                        </div>
                    )}
                </div>
            </div>

            <div className="grid grid-cols-2 gap-4 text-xs text-slate-300">
                <div className="space-y-1">
                    <div className="flex justify-between">
                        <span>Bias score</span>
                        <span className="font-mono">{biasPercent}%</span>
                    </div>
                    <div className="h-1.5 w-full rounded-full bg-slate-800">
                        <div
                            className="h-1.5 rounded-full bg-fuchsia-500"
                            style={{ width: `${biasPercent}%` }}
                        />
                    </div>
                </div>

                <div className="space-y-1">
                    <div className="flex justify-between">
                        <span>Confidence</span>
                        <span className="font-mono">{confidencePercent}%</span>
                    </div>
                    <div className="h-1.5 w-full rounded-full bg-slate-800">
                        <div
                            className="h-1.5 rounded-full bg-sky-500"
                            style={{ width: `${confidencePercent}%` }}
                        />
                    </div>
                </div>
            </div>

            {signal.narrative_risk && (
                <div className="text-[11px] text-slate-400">
                    Narrative risk:{" "}
                    <span className="font-semibold text-slate-100">
                        {signal.narrative_risk}
                    </span>
                </div>
            )}

            <p className="text-xs text-slate-400 leading-relaxed">
                {signal.explanation}
            </p>
        </div>
    );
}
