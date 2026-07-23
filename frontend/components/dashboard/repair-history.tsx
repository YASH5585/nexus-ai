"use client";

import { motion } from "framer-motion";
import { History, CheckCircle, XCircle, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface RepairHistoryProps {
  repairs: Array<{
    id: string;
    timestamp: number;
    type: string;
    file: string;
    status: "success" | "failed" | "partial";
    duration: number;
    issues_fixed?: number;
    issues_remaining?: number;
    message?: string;
  }>;
}

const statusIcons = {
  success: CheckCircle,
  failed: XCircle,
  partial: AlertCircle,
};

const statusColors = {
  success: "text-emerald-400",
  failed: "text-red-400",
  partial: "text-amber-400",
};

export function RepairHistory({ repairs }: RepairHistoryProps) {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 mb-2">
        <History className="h-4 w-4 text-zinc-500" />
        <h3 className="text-sm font-semibold text-zinc-200">Recent Repairs</h3>
        <span className="text-xs text-zinc-500">({repairs.length})</span>
      </div>

      <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
        {repairs.map((repair, index) => {
          const StatusIcon = statusIcons[repair.status];
          const colorClass = statusColors[repair.status];
          const date = new Date(repair.timestamp).toISOString().split('T')[0];
          const time = new Date(repair.timestamp).toISOString().split('T')[1].slice(0, 5);

          return (
            <motion.div
              key={repair.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="rounded-lg border border-white/10 bg-black/20 p-3"
            >
              <div className="flex items-start gap-3">
                <div className={cn("h-8 w-8 rounded-full flex items-center justify-center", colorClass.replace('text-', 'bg-').replace('400', '400/10'))}>
                  <StatusIcon className={cn("h-4 w-4", colorClass)} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={cn("text-xs font-medium uppercase tracking-wider", colorClass)}>
                      {repair.status}
                    </span>
                    <span className="text-xs text-zinc-400 font-mono">{repair.type}</span>
                  </div>
                  <p className="text-xs text-zinc-300 mb-1.5">{repair.file}</p>
                  <div className="flex items-center gap-3 text-xs text-zinc-500">
                    <span>{date} at {time}</span>
                    <span>{repair.duration.toFixed(2)}s</span>
                    {repair.issues_fixed !== undefined && (
                      <span>{repair.issues_fixed} fixed, {repair.issues_remaining ?? 0} remaining</span>
                    )}
                  </div>
                  {repair.message && (
                    <p className="mt-1 text-xs text-zinc-500 italic">{repair.message}</p>
                  )}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}