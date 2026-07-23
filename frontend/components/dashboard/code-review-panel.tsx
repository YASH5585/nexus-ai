"use client";

import { motion } from "framer-motion";
import { MessageSquare, AlertTriangle, Lightbulb, XCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface CodeReviewPanelProps {
  suggestions: Array<{
    category: string;
    severity: string;
    line_number?: number;
    message: string;
    suggestion: string;
  }>;
  passed: boolean;
  reviewTime: number;
}

const categoryIcons: Record<string, React.ReactNode> = {
  unused_variable: <AlertTriangle className="h-4 w-4" />,
  duplicate_code: <MessageSquare className="h-4 w-4" />,
  magic_number: <Lightbulb className="h-4 w-4" />,
  poor_naming: <MessageSquare className="h-4 w-4" />,
  missing_comments: <MessageSquare className="h-4 w-4" />,
  missing_type_hints: <AlertTriangle className="h-4 w-4" />,
  syntax_error: <XCircle className="h-4 w-4" />,
};

const severityColors: Record<string, { bg: string; border: string; text: string }> = {
  critical: { bg: "bg-red-500/10", border: "border-red-500/20", text: "text-red-400" },
  high: { bg: "bg-orange-500/10", border: "border-orange-500/20", text: "text-orange-400" },
  medium: { bg: "bg-amber-500/10", border: "border-amber-500/20", text: "text-amber-400" },
  low: { bg: "bg-blue-500/10", border: "border-blue-500/20", text: "text-blue-400" },
};

export function CodeReviewPanel({ suggestions, passed, reviewTime }: CodeReviewPanelProps) {
  const highIssues = suggestions.filter((s) => s.severity === "high" || s.severity === "critical").length;
  const mediumIssues = suggestions.filter((s) => s.severity === "medium").length;
  const lowIssues = suggestions.filter((s) => s.severity === "low").length;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className={cn("rounded-xl p-2.5", passed ? "bg-emerald-500/10" : "bg-amber-500/10")}>
            <MessageSquare className={cn("h-5 w-5", passed ? "text-emerald-400" : "text-amber-400")} />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-zinc-200">Code Review</h3>
            <p className="text-xs text-zinc-400">
              {passed ? "Code looks clean" : `${suggestions.length} issue${suggestions.length > 1 ? 's' : ''} found`}
            </p>
          </div>
        </div>
        <span className="text-xs text-zinc-500 font-mono">{reviewTime.toFixed(2)}s</span>
      </div>

      {!passed && (
        <div className="flex items-center gap-4 text-xs">
          {highIssues > 0 && (
            <div className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-red-400" />
              <span className="text-red-400">{highIssues} high</span>
            </div>
          )}
          {mediumIssues > 0 && (
            <div className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-amber-400" />
              <span className="text-amber-400">{mediumIssues} medium</span>
            </div>
          )}
          {lowIssues > 0 && (
            <div className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-blue-400" />
              <span className="text-blue-400">{lowIssues} low</span>
            </div>
          )}
        </div>
      )}

      <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
        {suggestions.map((suggestion, index) => {
          const colors = severityColors[suggestion.severity] || severityColors.low;
          const icon = categoryIcons[suggestion.category] || <Lightbulb className="h-4 w-4" />;

          return (
            <motion.div
              key={`${suggestion.category}-${index}`}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className={cn("rounded-lg border p-3", colors.bg, colors.border)}
            >
              <div className="flex items-start gap-2.5">
                <div className={cn("mt-0.5 flex-shrink-0", colors.text)}>{icon}</div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={cn("text-[10px] font-medium uppercase tracking-wider", colors.text)}>
                      {suggestion.severity}
                    </span>
                    {suggestion.line_number && (
                      <span className="text-xs text-zinc-500 font-mono">Line {suggestion.line_number}</span>
                    )}
                  </div>
                  <p className="text-xs text-zinc-300 mb-1">{suggestion.message}</p>
                  <p className="text-xs text-zinc-500 italic">{suggestion.suggestion}</p>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}