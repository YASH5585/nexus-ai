"use client";

import { motion } from "framer-motion";
import { Shield, ShieldAlert, ShieldCheck, ShieldX } from "lucide-react";
import { cn } from "@/lib/utils";

interface SecurityReportProps {
  issues: Array<{
    category: string;
    severity: string;
    risk: string;
    line_number?: number;
    recommendation: string;
  }>;
  passed: boolean;
  scanTime: number;
}

const severityConfig = {
  critical: {
    icon: ShieldX,
    color: "text-red-400",
    bg: "bg-red-500/10",
    border: "border-red-500/20",
    label: "Critical",
  },
  high: {
    icon: ShieldAlert,
    color: "text-orange-400",
    bg: "bg-orange-500/10",
    border: "border-orange-500/20",
    label: "High",
  },
  medium: {
    icon: Shield,
    color: "text-amber-400",
    bg: "bg-amber-500/10",
    border: "border-amber-500/20",
    label: "Medium",
  },
  low: {
    icon: ShieldCheck,
    color: "text-blue-400",
    bg: "bg-blue-500/10",
    border: "border-blue-500/20",
    label: "Low",
  },
};

export function SecurityReport({ issues, passed, scanTime }: SecurityReportProps) {
  const criticalCount = issues.filter((i) => i.severity === "critical").length;
  const highCount = issues.filter((i) => i.severity === "high").length;
  const mediumCount = issues.filter((i) => i.severity === "medium").length;
  const lowCount = issues.filter((i) => i.severity === "low").length;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className={cn("rounded-xl p-2.5", passed ? "bg-emerald-500/10" : "bg-red-500/10")}>
            {passed ? (
              <ShieldCheck className="h-5 w-5 text-emerald-400" />
            ) : (
              <ShieldX className="h-5 w-5 text-red-400" />
            )}
          </div>
          <div>
            <h3 className="text-sm font-semibold text-zinc-200">Security Scan</h3>
            <p className="text-xs text-zinc-400">
              {passed ? "No vulnerabilities found" : `${issues.length} issue${issues.length > 1 ? 's' : ''} detected`}
            </p>
          </div>
        </div>
        <span className="text-xs text-zinc-500 font-mono">{scanTime.toFixed(2)}s</span>
      </div>

      {!passed && (
        <div className="grid grid-cols-4 gap-2">
          {criticalCount > 0 && (
            <div className="rounded-lg bg-red-500/10 border border-red-500/20 p-2 text-center">
              <div className="text-lg font-bold text-red-400">{criticalCount}</div>
              <div className="text-[10px] text-red-400/70 uppercase tracking-wider">Critical</div>
            </div>
          )}
          {highCount > 0 && (
            <div className="rounded-lg bg-orange-500/10 border border-orange-500/20 p-2 text-center">
              <div className="text-lg font-bold text-orange-400">{highCount}</div>
              <div className="text-[10px] text-orange-400/70 uppercase tracking-wider">High</div>
            </div>
          )}
          {mediumCount > 0 && (
            <div className="rounded-lg bg-amber-500/10 border border-amber-500/20 p-2 text-center">
              <div className="text-lg font-bold text-amber-400">{mediumCount}</div>
              <div className="text-[10px] text-amber-400/70 uppercase tracking-wider">Medium</div>
            </div>
          )}
          {lowCount > 0 && (
            <div className="rounded-lg bg-blue-500/10 border border-blue-500/20 p-2 text-center">
              <div className="text-lg font-bold text-blue-400">{lowCount}</div>
              <div className="text-[10px] text-blue-400/70 uppercase tracking-wider">Low</div>
            </div>
          )}
        </div>
      )}

      <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
        {issues.map((issue, index) => {
          const config = severityConfig[issue.severity as keyof typeof severityConfig] || severityConfig.low;
          const SeverityIcon = config.icon;

          return (
            <motion.div
              key={`${issue.category}-${index}`}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className={cn("rounded-lg border p-3", config.bg, config.border)}
            >
              <div className="flex items-start gap-2.5">
                <SeverityIcon className={cn("h-4 w-4 mt-0.5 flex-shrink-0", config.color)} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={cn("text-xs font-medium uppercase tracking-wider", config.color)}>
                      {issue.severity}
                    </span>
                    <span className="text-xs text-zinc-500 font-mono truncate max-w-24">
                      {issue.category}
                      {issue.line_number ? `:${issue.line_number}` : ""}
                    </span>
                  </div>
                  <p className="text-xs text-zinc-300 leading-relaxed mb-1.5">{issue.risk}</p>
                  <p className="text-xs text-zinc-500 italic">Fix: {issue.recommendation}</p>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
