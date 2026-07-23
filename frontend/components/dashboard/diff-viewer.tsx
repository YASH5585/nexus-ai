"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface DiffViewerProps {
  original: string;
  modified: string;
  language?: string;
  className?: string;
}

interface DiffLine {
  type: "added" | "removed" | "unchanged" | "header";
  content: string;
  lineNumber?: number;
}

function parseDiff(original: string, modified: string): DiffLine[] {
  const originalLines = original.split("\n");
  const modifiedLines = modified.split("\n");
  
  const diffs: DiffLine[] = [];
  const maxLen = Math.max(originalLines.length, modifiedLines.length);
  
  for (let i = 0; i < maxLen; i++) {
    if (i < originalLines.length && i < modifiedLines.length) {
      if (originalLines[i] !== modifiedLines[i]) {
        diffs.push({ type: "removed", content: originalLines[i], lineNumber: i + 1 });
        diffs.push({ type: "added", content: modifiedLines[i], lineNumber: i + 1 });
      } else {
        diffs.push({ type: "unchanged", content: originalLines[i], lineNumber: i + 1 });
      }
    } else if (i < originalLines.length) {
      diffs.push({ type: "removed", content: originalLines[i], lineNumber: i + 1 });
    } else if (i < modifiedLines.length) {
      diffs.push({ type: "added", content: modifiedLines[i], lineNumber: i + 1 });
    }
  }
  
  return diffs;
}

export function DiffViewer({ original, modified, className }: DiffViewerProps) {
  const diffs = parseDiff(original, modified);
  const addedCount = diffs.filter((d) => d.type === "added").length;
  const removedCount = diffs.filter((d) => d.type === "removed").length;

  return (
    <div className={cn("rounded-lg border border-white/10 overflow-hidden", className)}>
      <div className="flex items-center justify-between bg-zinc-900/50 px-4 py-2 border-b border-white/10">
        <div className="flex items-center gap-3 text-xs">
          <span className="text-zinc-400">Changes</span>
          <div className="flex items-center gap-2">
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              <span className="text-emerald-400">+{addedCount}</span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-red-400" />
              <span className="text-red-400">-{removedCount}</span>
            </span>
          </div>
        </div>
        <span className="text-xs text-zinc-500 font-mono">Unified Diff</span>
      </div>
      
      <div className="bg-zinc-950/50 font-mono text-sm">
        {diffs.map((diff, index) => {
          const key = `${diff.lineNumber}-${index}`;
          
          return (
            <motion.div
              key={key}
              initial={{ opacity: 0, x: -5 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.01 }}
              className={cn(
                "flex items-start gap-2 px-4 py-1.5",
                diff.type === "added" && "bg-emerald-500/5 border-l-2 border-emerald-500/20",
                diff.type === "removed" && "bg-red-500/5 border-l-2 border-red-500/20",
                diff.type === "header" && "bg-zinc-800/50 font-semibold"
              )}
            >
              {diff.type === "added" && (
                <span className="text-emerald-400 text-xs mt-0.5">+</span>
              )}
              {diff.type === "removed" && (
                <span className="text-red-400 text-xs mt-0.5">-</span>
              )}
              {diff.type === "unchanged" && (
                <span className="text-zinc-600 text-xs mt-0.5">{diff.lineNumber && '│'}</span>
              )}
              {diff.type === "header" && (
                <span className="text-zinc-500 text-xs w-6" />
              )}
              <span className="text-zinc-200 break-all">{diff.content}</span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}