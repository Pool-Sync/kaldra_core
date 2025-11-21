// components/kaldra/KaldraSignalDistribution.tsx
"use client";

import type { KaldraSignal } from "@/app/lib/api/types";

interface Props {
    signal: KaldraSignal;
    maxBars?: number;
}

export function KaldraSignalDistribution({ signal, maxBars = 6 }: Props) {
    const entries = Object.entries(signal.kindra_distribution || {});
    const sorted = [...entries].sort((a, b) => b[1] - a[1]).slice(0, maxBars);

    if (!sorted.length) {
        return (
            <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-3 text-xs text-slate-400">
                No Kindra distribution available.
            </div>
        );
    }

    const maxValue = Math.max(...sorted.map(([, v]) => v));

    return (
        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-3 space-y-2">
            <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                Kindra distribution (top {sorted.length})
            </div>
            <div className="space-y-1.5">
                {sorted.map(([id, value]) => {
                    const pct = Math.round(value * 100);
                    const width = (value / maxValue) * 100;
                    return (
                        <div key={id} className="space-y-0.5">
                            <div className="flex justify-between text-[11px] text-slate-300">
                                <span className="font-mono">{id}</span>
                                <span className="font-mono">{pct}%</span>
                            </div>
                            <div className="h-1.5 w-full rounded-full bg-slate-800">
                                <div
                                    className="h-1.5 rounded-full bg-emerald-500"
                                    style={{ width: `${width}%` }}
                                />
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
