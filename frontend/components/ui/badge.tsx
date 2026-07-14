"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "success" | "error" | "warning" | "info" | "neutral";
  className?: string;
}

export function Badge({ children, variant = "neutral", className }: BadgeProps) {
  const variants = {
    success: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    error: "bg-red-500/10 text-red-400 border-red-500/20",
    warning: "bg-amber-500/10 text-amber-400 border-amber-500/20",
    info: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    neutral: "bg-zinc-500/10 text-zinc-400 border-zinc-500/20",
  };

  return (
    <motion.span
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium",
        variants[variant],
        className
      )}
    >
      {variant === "success" && (
        <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
      )}
      {variant === "error" && (
        <span className="h-1.5 w-1.5 rounded-full bg-red-400" />
      )}
      {variant === "warning" && (
        <span className="h-1.5 w-1.5 rounded-full bg-amber-400 animate-pulse" />
      )}
      {variant === "info" && (
        <span className="h-1.5 w-1.5 rounded-full bg-blue-400" />
      )}
      {children}
    </motion.span>
  );
}
