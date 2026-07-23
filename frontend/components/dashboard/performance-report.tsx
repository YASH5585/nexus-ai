"use client";

import { motion } from "framer-motion";
import { Activity, Cpu, HardDrive, Zap } from "lucide-react";
import { cn } from "@/lib/utils";

interface PerformanceReportProps {
  complexity: {
    time_complexity: string;
    space_complexity: string;
    estimated_memory_mb?: number;
  };
  suggestions: Array<{
    category: string;
    severity: string;
    message: string;
    suggestion: string;
    estimated_improvement: string;
  }>;
  alternativeAlgorithms: Array<{
    name: string;
    time_complexity: string;
    space_complexity: string;
    description: string;
  }>;
  passed: boolean;
  analysisTime: number;
}

const complexityColors: Record<string, string> = {
  "O(1)": "text-emerald-400",
  "O(log n)": "text-blue-400",
  "O(n)": "text-amber-400",
  "O(n log n)": "text-orange-400",
  "O(n^2)": "text-red-400",
  "O(n^3)": "text-red-500",
  "O(2^n)": "text-red-600",
};

export function PerformanceReport({
  complexity,
  suggestions,
  alternativeAlgorithms,
  passed,
  analysisTime,
}: PerformanceReportProps) {
  const timeColor = complexityColors[complexity.time_complexity] || "text-zinc-400";
  const spaceColor = complexityColors[complexity.space_complexity] || "text-zinc-400";

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className={cn("rounded-xl p-2.5", passed ? "bg-emerald-500/10" : "bg-amber-500/10")}>
            <Activity className={cn("h-5 w-5", passed ? "text-emerald-400" : "text-amber-400")} />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-zinc-200">Performance Analysis</h3>
            <p className="text-xs text-zinc-400">
              {passed ? "Performance looks good" : `${suggestions.length} optimization${suggestions.length > 1 ? 's' : ''} found`}
            </p>
          </div>
        </div>
        <span className="text-xs text-zinc-500 font-mono">{analysisTime.toFixed(2)}s</span>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="rounded-lg border border-white/10 bg-black/20 p-3">
          <div className="flex items-center gap-2 mb-1">
            <Cpu className="h-3.5 w-3.5 text-zinc-500" />
            <span className="text-[10px] text-zinc-500 uppercase tracking-wider">Time Complexity</span>
          </div>
          <div className={cn("text-lg font-bold font-mono", timeColor)}>
            {complexity.time_complexity}
          </div>
        </div>
        <div className="rounded-lg border border-white/10 bg-black/20 p-3">
          <div className="flex items-center gap-2 mb-1">
            <HardDrive className="h-3.5 w-3.5 text-zinc-500" />
            <span className="text-[10px] text-zinc-500 uppercase tracking-wider">Space Complexity</span>
          </div>
          <div className={cn("text-lg font-bold font-mono", spaceColor)}>
            {complexity.space_complexity}
          </div>
        </div>
      </div>

      {complexity.estimated_memory_mb !== undefined && (
        <div className="flex items-center gap-2 text-xs text-zinc-400">
          <Zap className="h-3.5 w-3.5 text-zinc-500" />
          <span>Estimated memory: <span className="text-zinc-300 font-mono">{complexity.estimated_memory_mb} MB</span></span>
        </div>
      )}

      {suggestions.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-xs font-medium text-zinc-400 uppercase tracking-wider">Optimization Suggestions</h4>
          <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
            {suggestions.slice(0, 5).map((suggestion, index) => (
              <motion.div
                key={`${suggestion.category}-${index}`}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="rounded-lg border border-white/5 bg-white/5 p-3"
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className={cn(
                    "text-[10px] font-medium uppercase tracking-wider px-2 py-0.5 rounded-full",
                    suggestion.severity === "high" && "bg-red-500/10 text-red-400",
                    suggestion.severity === "medium" && "bg-amber-500/10 text-amber-400",
                    suggestion.severity === "low" && "bg-blue-500/10 text-blue-400",
                  )}>
                    {suggestion.severity}
                  </span>
                  <span className="text-xs text-zinc-400 font-mono truncate max-w-20 inline-block">
                    {suggestion.category}
                  </span>
                </div>
                <p className="text-xs text-zinc-300 mb-1">{suggestion.message}</p>
                <p className="text-xs text-zinc-500 italic mb-1">{suggestion.suggestion}</p>
                <p className="text-xs text-emerald-400/80 font-mono">{suggestion.estimated_improvement}</p>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {alternativeAlgorithms.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-xs font-medium text-zinc-400 uppercase tracking-wider">Alternative Algorithms</h4>
          <div className="space-y-2">
            {alternativeAlgorithms.slice(0, 3).map((algo, index) => (
              <motion.div
                key={`${algo.name}-${index}`}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="rounded-lg border border-blue-500/20 bg-blue-500/5 p-3"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-blue-400">{algo.name}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-emerald-400 font-mono">{algo.time_complexity}</span>
                    <span className="text-xs text-zinc-500 font-mono">{algo.space_complexity}</span>
                  </div>
                </div>
                <p className="text-xs text-zinc-400">{algo.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
