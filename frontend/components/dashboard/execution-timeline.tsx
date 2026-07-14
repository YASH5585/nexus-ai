"use client";

import { motion } from "framer-motion";
import { CheckCircle2, XCircle, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface TimelineStep {
  id: string;
  label: string;
  status: "pending" | "running" | "completed" | "error";
  detail?: string;
}

interface ExecutionTimelineProps {
  steps: TimelineStep[];
  currentStep?: number;
}

const icons = {
  pending: () => (
    <div className="h-5 w-5 rounded-full border-2 border-zinc-600" />
  ),
  running: () => (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
    >
      <Loader2 className="h-5 w-5 text-blue-400" />
    </motion.div>
  ),
  completed: () => <CheckCircle2 className="h-5 w-5 text-emerald-400" />,
  error: () => <XCircle className="h-5 w-5 text-red-400" />,
};

export function ExecutionTimeline({ steps, currentStep = 0 }: ExecutionTimelineProps) {
  return (
    <div className="relative space-y-0">
      {steps.map((step, index) => {
        const isActive = index === currentStep && step.status === "running";
        const isCompleted = index < currentStep || step.status === "completed";
        const isPending = index > currentStep;

        return (
          <motion.div
            key={step.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="relative flex gap-4 pb-6 last:pb-0"
          >
            <div className="flex flex-col items-center">
              <motion.div
                animate={isActive ? { scale: [1, 1.2, 1] } : {}}
                transition={{ duration: 1.5, repeat: Infinity }}
                className={cn(
                  "relative z-10 flex h-10 w-10 items-center justify-center rounded-full",
                  isCompleted && "bg-emerald-500/10",
                  step.status === "error" && "bg-red-500/10",
                  isPending && "bg-zinc-500/5"
                )}
              >
                {icons[step.status]()}
              </motion.div>
              {index < steps.length - 1 && (
                <div
                  className={cn(
                    "h-full w-px",
                    isCompleted ? "bg-emerald-500/30" : "bg-zinc-700/50"
                  )}
                />
              )}
            </div>
            <div className="flex-1 pt-1">
              <div className="flex items-center gap-2">
                <h3
                  className={cn(
                    "text-sm font-medium",
                    isCompleted && "text-emerald-400",
                    step.status === "error" && "text-red-400",
                    isPending && "text-zinc-500"
                  )}
                >
                  {step.label}
                </h3>
              </div>
              {step.detail && (
                <p className="mt-1 text-xs text-zinc-400 font-mono">{step.detail}</p>
              )}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
