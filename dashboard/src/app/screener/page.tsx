"use client";

import React, { useState, useEffect } from "react";
import { Grid, AlertTriangle, CheckCircle, TrendingUp } from "lucide-react";

type Regime = "STABLE" | "TRANSITIONING" | "STRESSED";

interface StateData {
  regime: Regime;
  confidence: number;
  mean_value: number;
  pelt_triggered: boolean;
  drift_triggered: boolean;
  updated_at: number;
}

export default function MacroScreener() {
  const [liveState, setLiveState] = useState<Record<string, StateData>>({});

  useEffect(() => {
    const fetchLiveState = async () => {
      try {
        const res = await fetch("/api/state/all");
        if (res.ok) {
          const data = await res.json();
          setLiveState(data.data || {});
        }
      } catch (e) {
        // silent
      }
    };
    
    fetchLiveState();
    const interval = setInterval(fetchLiveState, 1500); // Poll aggressively for the screener
    return () => clearInterval(interval);
  }, []);

  const getCardStyle = (regime: string) => {
    switch (regime) {
      case "STABLE":
        return "border-emerald-500/40 bg-emerald-500/5 shadow-[0_0_30px_rgba(16,185,129,0.15)] hover:border-emerald-400";
      case "TRANSITIONING":
        return "border-amber-500/60 bg-amber-500/10 shadow-[0_0_40px_rgba(245,158,11,0.2)] hover:border-amber-400";
      case "STRESSED":
        return "border-rose-500/80 bg-rose-500/15 shadow-[0_0_50px_rgba(244,63,94,0.3)] hover:border-rose-400 transform hover:-translate-y-1 transition-all";
      default:
        return "border-slate-800 bg-white/[0.02]";
    }
  };

  const getTextColor = (regime: string) => {
    switch (regime) {
      case "STABLE": return "text-emerald-400";
      case "TRANSITIONING": return "text-amber-400";
      case "STRESSED": return "text-rose-500";
      default: return "text-slate-400";
    }
  };

  const assets = Object.keys(liveState);

  return (
    <div className="p-8">
      <header className="mb-10">
        <h1 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400 flex items-center gap-3">
          <Grid className="text-blue-500 w-10 h-10" />
          Macro Matrix Screener
        </h1>
        <p className="text-slate-400 mt-3 max-w-2xl text-lg">
          Simultaneous real-time analysis of quantitative streams. The serverless architecture scales horizontally to track shifting macro environments across high-liquidity pairs.
        </p>
      </header>

      {assets.length === 0 ? (
        <div className="flex h-64 items-center justify-center border border-dashed border-slate-700 rounded-3xl">
          <div className="text-center text-slate-500 animate-pulse">
            <TrendingUp className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p className="text-xl">Waiting for multiplexed streams to initialize...</p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
          {assets.map((key) => {
            const state = liveState[key];
            const parts = key.split(":");
            const assetName = parts[parts.length - 1];
            
            return (
              <div 
                key={key} 
                className={`rounded-3xl p-8 border backdrop-blur-xl transition-all duration-500 ${getCardStyle(state.regime)} relative overflow-hidden`}
              >
                {/* Glow Orb */}
                <div className={`absolute -top-20 -right-20 w-40 h-40 rounded-full blur-[80px] opacity-50 ${state.regime === "STABLE" ? "bg-emerald-500" : state.regime === "STRESSED" ? "bg-rose-500" : "bg-amber-500"}`} />

                <div className="flex justify-between items-start mb-8 relative z-10">
                  <div>
                    <p className="text-sm font-bold text-slate-500 tracking-widest mb-1">ASSET</p>
                    <h2 className="text-3xl font-black text-white">{assetName}</h2>
                  </div>
                  <div className={`flex items-center gap-2 px-4 py-2 rounded-full border border-current ${getTextColor(state.regime)} bg-white/5`}>
                    {state.regime === "STRESSED" ? <AlertTriangle size={16} /> : <CheckCircle size={16} />}
                    <span className="font-bold tracking-wider text-sm">{state.regime}</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-6 relative z-10 mb-8">
                  <div className="bg-slate-950/40 rounded-2xl p-4 border border-white/5">
                    <p className="text-xs font-bold text-slate-500 mb-2">MEAN VALUE</p>
                    <p className="text-2xl font-mono text-slate-200">
                      ${state.mean_value < 10 ? state.mean_value.toFixed(4) : state.mean_value.toFixed(2)}
                    </p>
                  </div>
                  <div className="bg-slate-950/40 rounded-2xl p-4 border border-white/5">
                    <p className="text-xs font-bold text-slate-500 mb-2">CONFIDENCE</p>
                    <p className="text-2xl font-mono text-slate-200">
                      {(state.confidence * 100).toFixed(0)}%
                    </p>
                  </div>
                </div>

                {/* Math Logic indicators */}
                <div className="flex gap-4 pt-4 border-t border-white/10 relative z-10">
                  <div className={`text-xs font-bold px-3 py-1.5 rounded bg-slate-950/40 flex items-center gap-2 ${state.pelt_triggered ? "text-rose-400 border border-rose-500/30" : "text-slate-500 border border-transparent"}`}>
                    <div className={`w-2 h-2 rounded-full ${state.pelt_triggered ? "bg-rose-400 animate-pulse" : "bg-slate-700"}`} />
                    PELT (L2)
                  </div>
                  <div className={`text-xs font-bold px-3 py-1.5 rounded bg-slate-950/40 flex items-center gap-2 ${state.drift_triggered ? "text-amber-400 border border-amber-500/30" : "text-slate-500 border border-transparent"}`}>
                    <div className={`w-2 h-2 rounded-full ${state.drift_triggered ? "bg-amber-400 animate-pulse" : "bg-slate-700"}`} />
                    ADWIN
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
