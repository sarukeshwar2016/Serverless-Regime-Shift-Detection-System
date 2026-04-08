"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, Grid } from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Deep Dive", path: "/", icon: <Activity size={20} /> },
    { name: "Macro Screener", path: "/screener", icon: <Grid size={20} /> },
  ];

  return (
    <div className="w-64 min-h-screen border-r border-white/5 bg-slate-950/50 flex flex-col p-6 space-y-8 backdrop-blur-md">
      <div>
        <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-300">
          Macro Regime
        </h1>
        <p className="text-xs text-slate-500 mt-1">Quantitative Platform</p>
      </div>

      <nav className="flex flex-col space-y-3">
        {navItems.map((item) => {
          const isActive = pathname === item.path;
          return (
            <Link
              key={item.path}
              href={item.path}
              className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                isActive
                  ? "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 shadow-lg shadow-indigo-500/5"
                  : "text-slate-400 hover:bg-white/5 hover:text-slate-200 border border-transparent"
              }`}
            >
              {item.icon}
              <span className="font-semibold text-sm tracking-wide">{item.name}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
