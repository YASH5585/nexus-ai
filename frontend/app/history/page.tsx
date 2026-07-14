"use client";

import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/glass-card";
import { Badge } from "@/components/ui/badge";
import { mockRunHistory } from "@/lib/mock-data";
import { CheckCircle2, XCircle, Clock, ChevronRight } from "lucide-react";
import Link from "next/link";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    staggerChildren: 0.05,
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

export default function HistoryPage() {
  return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-white">Run History</h1>
        <p className="mt-1 text-zinc-400">All previous AI self-healing executions</p>
      </motion.div>

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="space-y-4"
      >
        {mockRunHistory.map((run) => (
          <motion.div key={run.id} variants={item}>
            <Link href={`/dashboard`}>
              <GlassCard className="p-5 hover:border-white/20 transition-colors cursor-pointer group">
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-2">
                      {run.status === "success" ? (
                        <CheckCircle2 className="h-5 w-5 text-emerald-400 shrink-0" />
                      ) : (
                        <XCircle className="h-5 w-5 text-red-400 shrink-0" />
                      )}
                      <Badge variant={run.status === "success" ? "success" : "error"}>
                        {run.status}
                      </Badge>
                      <span className="text-xs text-zinc-500 font-mono">#{run.id}</span>
                    </div>
                    <p className="text-sm text-zinc-300 truncate group-hover:text-white transition-colors">
                      {run.prompt}
                    </p>
                    <div className="mt-2 flex items-center gap-4 text-xs text-zinc-500">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {run.duration}
                      </span>
                      <span>{run.attempts} attempt{run.attempts > 1 ? "s" : ""}</span>
                      <span>{new Date(run.createdAt).toLocaleDateString()}</span>
                    </div>
                  </div>
                  <ChevronRight className="h-5 w-5 text-zinc-600 group-hover:text-white transition-colors shrink-0 ml-4" />
                </div>
              </GlassCard>
            </Link>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
