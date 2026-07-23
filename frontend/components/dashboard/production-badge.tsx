"use client";

import { motion } from "framer-motion";
import { Star } from "lucide-react";
import { cn } from "@/lib/utils";

interface ProductionBadgeProps {
  className?: string;
  variant?: "default" | "premium" | "success" | "warning";
}

export function ProductionBadge({ className, variant = "premium" }: ProductionBadgeProps) {
  const variants = {
    default: "bg-zinc-800/80 text-zinc-300 border-zinc-700",
    premium: "bg-gradient-to-r from-amber-500/20 to-yellow-500/20 text-amber-400 border-amber-500/30",
    success: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
    warning: "bg-amber-500/20 text-amber-400 border-amber-500/30",
  };

  return (
    <motion.div
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ type: "spring", stiffness: 120, damping: 15 }}
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-0.5 text-xs font-semibold",
        "rounded-full border",
        "backdrop-blur-sm",
        variants[variant],
        className
      )}
    >
      <Star className="h-3 w-3 fill-current" />
      <span>Production</span>
    </motion.div>
  );
}