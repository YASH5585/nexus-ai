"use client";

import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface MetricCardProps {
  label: string;
  value: string | number;
  unit?: string;
  trend?: "up" | "down" | "neutral";
  trendValue?: string;
  icon?: React.ReactNode;
  className?: string;
}

export function MetricCard({ label, value, unit, trend, trendValue, icon, className }: MetricCardProps) {
  return (
    <motion.div
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      className={cn(
        "relative overflow-hidden rounded-xl border border-white/10 bg-white/5 p-5 backdrop-blur-xl",
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium text-zinc-400 uppercase tracking-wider">{label}</p>
          <div className="mt-2 flex items-baseline gap-1">
            <span className="text-2xl font-bold text-white">{value}</span>
            {unit && <span className="text-sm text-zinc-400">{unit}</span>}
          </div>
        </div>
        {icon && <div className="text-zinc-400">{icon}</div>}
      </div>
      {trend && trendValue && (
        <div className="mt-3 flex items-center gap-1">
          <Badge
            variant={
              trend === "up" ? "success" : trend === "down" ? "error" : "neutral"
            }
          >
            {trend === "up" ? "↑" : trend === "down" ? "↓" : "−"}
            {trendValue}
          </Badge>
          <span className="text-xs text-zinc-500">vs last run</span>
        </div>
      )}
    </motion.div>
  );
}

interface MetricsGridProps {
  metrics: {
    label: string;
    value: string | number;
    unit?: string;
    trend?: "up" | "down" | "neutral";
    trendValue?: string;
    icon?: React.ReactNode;
  }[];
  className?: string;
}

export function MetricsGrid({ metrics, className }: MetricsGridProps) {
  return (
    <div className={cn("grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4", className)}>
      {metrics.map((metric) => (
        <MetricCard key={metric.label} {...metric} />
      ))}
    </div>
  );
}
