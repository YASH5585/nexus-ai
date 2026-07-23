"use client";

import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/glass-card";
import { mockRunHistory } from "@/lib/mock-data";
import { Badge } from "@/components/ui/badge";
import { Clock, CheckCircle2, XCircle } from "lucide-react";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    staggerChildren: 0.1,
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

export default function TimelinePage() {
  return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-white">Execution Timeline</h1>
        <p className="mt-1 text-zinc-400">Detailed view of AI self-healing execution flows</p>
      </motion.div>

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="space-y-6"
      >
        {mockRunHistory.map((run) => (
          <motion.div key={run.id} variants={item}>
            <GlassCard className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <Badge variant={run.status === "success" ? "success" : "error"}>
                      {run.status === "success" ? (
                        <CheckCircle2 className="h-3 w-3" />
                      ) : (
                        <XCircle className="h-3 w-3" />
                      )}
                      {run.status}
                    </Badge>
                    <span className="text-xs text-zinc-500 font-mono">
                      #{run.id}
                    </span>
                  </div>
                  <p className="text-white font-medium">{run.prompt}</p>
                  <div className="mt-2 flex items-center gap-4 text-xs text-zinc-400">
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {run.duration}
                    </span>
                    <span>{run.attempts} attempt{run.attempts > 1 ? "s" : ""}</span>
                    <span>{new Date(run.createdAt).toLocaleString()}</span>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-6 border-t border-white/10">
                <h4 className="text-sm font-semibold text-zinc-300 mb-4">Execution Steps</h4>
                <div className="space-y-4">
                  {[
                    { label: "Analyze Prompt", detail: "Identified problem type", status: "completed" as const },
                    { label: "Generate Code", detail: "Generated initial solution", status: "completed" as const },
                    { label: "Run Tests", detail: run.attempts > 1 ? `${run.attempts - 1} failures detected` : "All tests passed", status: run.attempts > 1 ? "error" as const : "completed" as const },
                    { label: "Analyze Failures", detail: "Identified edge cases", status: "completed" as const },
                    ...(run.attempts > 1 ? [
                      { label: "Patch Code", detail: "Applied fixes", status: "completed" as const },
                      { label: "Re-run Tests", detail: "All tests passed", status: "completed" as const },
                    ] : []),
                  ].map((step, i) => (
                    <motion.div
                      key={step.label}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="flex items-center gap-3"
                    >
                      <div className={`h-2 w-2 rounded-full ${step.status === "completed" ? "bg-emerald-400" : "bg-red-400"}`} />
                      <span className="text-sm text-zinc-300 flex-1">{step.label}</span>
                      <span className="text-xs text-zinc-500 font-mono">{step.detail}</span>
                    </motion.div>
                  ))}
                </div>
              </div>
            </GlassCard>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
