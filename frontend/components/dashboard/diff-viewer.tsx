"use client";

import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface DiffViewerProps {
  oldCode: string;
  newCode: string;
  className?: string;
}

export function DiffViewer({ oldCode, newCode, className }: DiffViewerProps) {
  const oldLines = oldCode.split("\n");
  const newLines = newCode.split("\n");

  return (
    <div className={cn("rounded-xl border border-white/10 bg-black/40 overflow-hidden", className)}>
      <div className="flex items-center justify-between border-b border-white/10 bg-white/5 px-4 py-2">
        <span className="text-xs font-medium text-zinc-400">Diff</span>
        <Badge variant="info">AI Patch</Badge>
      </div>
      <div className="grid grid-cols-2 divide-x divide-white/10">
        <div className="p-4">
          <div className="mb-2 text-xs font-medium text-red-400/80">Removed</div>
          <div className="space-y-1">
            {oldLines.map((line, i) => (
              <motion.div
                key={`old-${i}`}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.02 }}
                className="font-mono text-sm leading-relaxed text-red-400/60 line-through"
              >
                {line || "\u00A0"}
              </motion.div>
            ))}
          </div>
        </div>
        <div className="p-4">
          <div className="mb-2 text-xs font-medium text-emerald-400/80">Added</div>
          <div className="space-y-1">
            {newLines.map((line, i) => (
              <motion.div
                key={`new-${i}`}
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.02 }}
                className="font-mono text-sm leading-relaxed text-emerald-400/80"
              >
                {line || "\u00A0"}
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
