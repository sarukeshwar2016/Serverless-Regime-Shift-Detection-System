"use client";

import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Activity, Clock, AlertTriangle, CheckCircle, Database, Server } from "lucide-react";

// Types
type Regime = "STABLE" | "TRANSITIONING" | "STRESSED";

interface StateData {
  regime: Regime;
  confidence: number;
  mean_value: number;
  pelt_triggered: boolean;
  drift_triggered: boolean;
  updated_at: number;
}

interface AnomalyLog {
  source: string;
  asset: string;
  regime_data: StateData;
  timestamp: number;
}

export default function Dashboard() {
  const [liveState, setLiveState] = useState<Record<string, StateData>>({});
  const [history, setHistory] = useState<AnomalyLog[]>([]);
  const [apiConnected, setApiConnected] = useState<boolean>(false);
  const [chartData, setChartData] = useState<{ time: string; value: number }[]>([]);

  // Fetch Live State (Redis Hot Layer)
  const fetchLiveState = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/state/all");
      if (res.ok) {
        setApiConnected(true);
        const data = await res.json();
        setLiveState(data.data || {});

        // Update synthetic chart data based on BTC-USD or first available asset
        const assetKeys = Object.keys(data.data || {});
        if (assetKeys.length > 0) {
          const mainAsset = data.data[assetKeys[0]];
          const timeLabel = new Date().toLocaleTimeString();
          setChartData((prev) => {
            const newData = [...prev, { time: timeLabel, value: mainAsset.mean_value }];
            return newData.slice(-30); // keep last 30 ticks
          });
        }
      }
    } catch {
      setApiConnected(false);
    }
  };

  // Fetch History (MongoDB Cold Layer)
  const fetchHistory = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/history?limit=10");
      if (res.ok) {
        const data = await res.json();
        setHistory(data.data || []);
      }
    } catch (e) {
      console.error("Failed to fetch history:", e);
    }
  };

  useEffect(() => {
    fetchLiveState();
    fetchHistory();
    const interval = setInterval(() => {
      fetchLiveState();
      // Fetch history less frequently
      if (Math.random() > 0.5) fetchHistory(); 
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const getRegimeColor = (regime: string) => {
    switch (regime) {
      case "STABLE":
        return "text-emerald-400 border-emerald-400/30 bg-emerald-400/10";
      case "TRANSITIONING":
        return "text-amber-400 border-amber-400/30 bg-amber-400/10";
      case "STRESSED":
        return "text-rose-500 border-rose-500/30 bg-rose-500/10";
      default:
        return "text-gray-400 border-gray-400/30 bg-gray-400/10";
    }
  };

  const activeAssets = Object.keys(liveState);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans p-6 selection:bg-indigo-500/30">
      {/* Header */}
      <header className="flex flex-col md:flex-row justify-between items-center mb-8 pb-6 border-b border-white/5">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent flex items-center gap-3">
            <Activity className="w-8 h-8 text-indigo-400" />
            Regime Shift Detection
          </h1>
          <p className="text-slate-400 mt-2 text-sm">Serverless Financial Monitoring Platform</p>
        </div>
        <div className="mt-4 md:mt-0 flex items-center gap-4">
          <div className="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/10 shadow-sm backdrop-blur-sm">
            <Server className={`w-4 h-4 ${apiConnected ? "text-emerald-400" : "text-rose-500"}`} />
            <span className="text-sm font-medium">{apiConnected ? "API Connected (Hot Layer)" : "API Offline"}</span>
          </div>
          <div className="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/10 shadow-sm backdrop-blur-sm">
            <Database className="w-4 h-4 text-sky-400" />
            <span className="text-sm font-medium">MongoDB (Cold Layer)</span>
          </div>
        </div>
      </header>

      <main className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Live State Cards */}
        <div className="space-y-6">
          <h2 className="text-xl font-semibold flex items-center gap-2 text-slate-100">
            <Activity className="w-5 h-5 text-indigo-400" /> Live Data Streams
          </h2>
          {activeAssets.length === 0 ? (
            <div className="bg-white/5 border border-white/10 rounded-2xl p-8 text-center text-slate-400">
              No live streams detected.<br/>
              Run <code className="text-indigo-300">python ingestion/run.py</code>
            </div>
          ) : (
            activeAssets.map((key) => {
              const state = liveState[key];
              const parts = key.split(":");
              const assetName = parts[parts.length - 1];
              return (
                <div key={key} className="bg-white/[0.02] border border-white/5 rounded-2xl p-6 shadow-xl backdrop-blur-md relative overflow-hidden group hover:border-white/10 transition-colors">
                  <div className={`absolute top-0 left-0 w-1 h-full ${state.regime === "STABLE" ? "bg-emerald-500" : state.regime === "TRANSITIONING" ? "bg-amber-500" : "bg-rose-500"}`} />
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-sm text-slate-400 font-medium">ASSET</h3>
                      <p className="text-2xl font-bold text-slate-100">{assetName}</p>
                    </div>
                    <div className={`px-3 py-1 rounded-full text-xs font-bold border flex items-center gap-1.5 ${getRegimeColor(state.regime)}`}>
                      {state.regime === "STRESSED" && <AlertTriangle className="w-3.5 h-3.5" />}
                      {state.regime === "STABLE" && <CheckCircle className="w-3.5 h-3.5" />}
                      {state.regime}
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 mt-6">
                    <div>
                      <p className="text-xs text-slate-500 font-medium tracking-wider">MEAN VALUE</p>
                      <p className="text-lg font-mono text-slate-300">${state.mean_value?.toFixed(2)}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500 font-medium tracking-wider">CONFIDENCE</p>
                      <p className="text-lg font-mono text-slate-300">{(state.confidence * 100).toFixed(0)}%</p>
                    </div>
                  </div>

                  <div className="mt-6 pt-4 border-t border-white/5 flex gap-4 text-xs">
                    <span className={`flex items-center gap-1 ${state.pelt_triggered ? "text-rose-400" : "text-slate-500"}`}>
                      ● PELT (Ruptures)
                    </span>
                    <span className={`flex items-center gap-1 ${state.drift_triggered ? "text-amber-400" : "text-slate-500"}`}>
                      ● ADWIN (River)
                    </span>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Middle/Right Column: Charts & History */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Chart Panel */}
          <div className="bg-white/[0.02] border border-white/5 rounded-2xl p-6 shadow-xl backdrop-blur-md">
            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2 text-slate-100">
              <Activity className="w-5 h-5 text-indigo-400" /> Real-Time Analytics
            </h2>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="time" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis domain={['auto', 'auto']} stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(v)=>`$${v}`} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                    itemStyle={{ color: '#818cf8' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="value" 
                    stroke="#818cf8" 
                    strokeWidth={3} 
                    dot={false}
                    animationDuration={300}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            {chartData.length === 0 && (
              <div className="absolute inset-0 flex items-center justify-center text-slate-500">
                Waiting for streaming data...
              </div>
            )}
          </div>

          {/* History Panel */}
          <div className="bg-white/[0.02] border border-white/5 rounded-2xl shadow-xl backdrop-blur-md overflow-hidden">
             <div className="p-6 border-b border-white/5 bg-white/[0.01]">
                <h2 className="text-xl font-semibold flex items-center gap-2 text-slate-100">
                  <Clock className="w-5 h-5 text-indigo-400" /> Anomaly Ledger (Permanent Storage)
                </h2>
             </div>
             
             <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-white/10 text-xs tracking-wider text-slate-400 uppercase bg-white/[0.02]">
                      <th className="px-6 py-4 font-medium">Timestamp</th>
                      <th className="px-6 py-4 font-medium">Asset</th>
                      <th className="px-6 py-4 font-medium">Event Regime</th>
                      <th className="px-6 py-4 font-medium">Value</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {history.length === 0 ? (
                      <tr>
                        <td colSpan={4} className="px-6 py-8 text-center text-slate-500">
                          No anomalies logged in MongoDB yet.
                        </td>
                      </tr>
                    ) : (
                      history.map((log, idx) => {
                        const date = new Date(log.timestamp * 1000).toLocaleString();
                        const reg = log.regime_data?.regime || "UNKNOWN";
                        return (
                          <tr key={idx} className="hover:bg-white/[0.02] transition-colors group">
                            <td className="px-6 py-4 text-sm text-slate-400 font-mono">{date}</td>
                            <td className="px-6 py-4 text-sm text-slate-200 font-medium">{log.asset}</td>
                            <td className="px-6 py-4">
                              <span className={`px-2.5 py-1 rounded inline-flex text-xs font-semibold ${getRegimeColor(reg)}`}>
                                {reg}
                              </span>
                            </td>
                            <td className="px-6 py-4 text-sm font-mono text-slate-300">
                              ${log.regime_data?.mean_value?.toFixed(2) || "---"}
                            </td>
                          </tr>
                        );
                      })
                    )}
                  </tbody>
                </table>
             </div>
          </div>

        </div>
      </main>
    </div>
  );
}
