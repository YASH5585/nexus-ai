"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface LogEntry {
  id: string;
  timestamp: string;
  level: "info" | "warn" | "error" | "debug";
  message: string;
}

interface LogsPanelProps {
  logs: LogEntry[];
  className?: string;
}

const levelStyles = {
  info: "text-blue-400",
  warn: "text-amber-400",
  error: "text-red-400",
  debug: "text-zinc-500",
};

export function LogsPanel({ logs, className }: LogsPanelProps) {
  return (
    <div className={cn("rounded-xl border border-white/10 bg-black/40 overflow-hidden", className)}>
      <div className="flex items-center justify-between border-b border-white/10 bg-white/5 px-4 py-2">
        <span className="text-xs font-medium text-zinc-400">Execution Logs</span>
        <span className="text-xs text-zinc-500">{logs.length} entries</span>
      </div>
      <div className="max-h-[300px] overflow-y-auto p-4 space-y-2">
        {logs.length === 0 ? (
          <p className="text-sm text-zinc-500 italic">No logs yet...</p>
        ) : (
          logs.map((log, i) => (
            <motion.div
              key={log.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.03 }}
              className="flex gap-3 font-mono text-xs leading-relaxed"
            >
              <span className="text-zinc-600 shrink-0">{log.timestamp}</span>
              <span className={cn("uppercase font-bold w-10 shrink-0", levelStyles[log.level])}>
                {log.level}
              </span>
              <span className="text-zinc-300 break-all">{log.message}</span>
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
}
