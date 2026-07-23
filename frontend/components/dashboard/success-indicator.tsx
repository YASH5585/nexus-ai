"use client";

import { motion } from "framer-motion";
import { CheckCircle2, XCircle, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

type Status = "idle" | "running" | "success" | "error";

interface SuccessIndicatorProps {
  status: Status;
  message?: string;
  className?: string;
}

export function SuccessIndicator({ status, message, className }: SuccessIndicatorProps) {
  if (status === "idle") return null;

  const config = {
    running: {
      icon: Loader2,
      color: "text-blue-400",
      bg: "bg-blue-500/10",
      border: "border-blue-500/30",
      label: "Healing in progress...",
    },
    success: {
      icon: CheckCircle2,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10",
      border: "border-emerald-500/30",
      label: "All tests passed!",
    },
    error: {
      icon: XCircle,
      color: "text-red-400",
      bg: "bg-red-500/10",
      border: "border-red-500/30",
      label: "Max retries reached",
    },
  };

  const { icon: Icon, color, bg, border, label } = config[status];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className={cn("flex items-center gap-3 rounded-xl border p-4", bg, border, className)}
    >
      <motion.div
        animate={status === "running" ? { rotate: 360 } : {}}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
      >
        <Icon className={cn("h-6 w-6", color)} />
      </motion.div>
      <div>
        <p className={cn("font-semibold", color)}>{message || label}</p>
        {status === "success" && (
          <p className="text-sm text-zinc-400">Code has been self-healed successfully</p>
        )}
        {status === "error" && (
          <p className="text-sm text-zinc-400">Manual intervention required</p>
        )}
      </div>
    </motion.div>
  );
}
