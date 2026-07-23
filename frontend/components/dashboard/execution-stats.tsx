"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface ExecutionStatsProps {
  stats: Array<{
    label: string;
    value: string | number;
    change?: number;
    icon?: React.ReactNode;
    suffix?: string;
  }>;
}

export function ExecutionStats({ stats }: ExecutionStatsProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {stats.map((stat, index) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: index * 0.05, type: "spring", stiffness: 100 }}
          className="rounded-xl border border-white/10 bg-gradient-to-br from-white/5 to-transparent p-4 min-w-full"
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs text-zinc-500 uppercase tracking-wider">{stat.label}</span>
            <span className="text-xs text-zinc-500 font-mono">{stat.value}</span>
          </div>
          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-bold text-zinc-200">{stat.value}</span>
            {stat.suffix && <span className="text-sm text-zinc-400">{stat.suffix}</span>}
          </div>
          {stat.change !== undefined && (
            <div className="mt-1">
              <span className="text-xs font-medium">
                {stat.change > 0 ? "+" : ""}{stat.change}%
              </span>
              <span className="text-xs text-zinc-500/70 ml-1">vs last run</span>
            </div>
          )}
        </motion.div>
      ))}
    </div>
  );
}