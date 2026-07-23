"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface ConfidenceMeterProps {
  value: number;
  max?: number;
  size?: number;
  showLabel?: boolean;
  className?: string;
}

const colorZones = {
  critical: 0.3,
  low: 0.5,
  medium: 0.7,
  high: 0.9,
  excellent: 1,
};

export function ConfidenceMeter({
  value,
  max = 100,
  size = 120,
  showLabel = true,
  className,
}: ConfidenceMeterProps) {
  const percentage = Math.min(100, (value / max) * 100);
  const radius = (size - 20) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;

  let color = "#3b82f6";
  if (percentage < 30) color = "#ef4444";
  else if (percentage < 50) color = "#f97316";
  else if (percentage < 70) color = "#eab308";
  else if (percentage < 90) color = "#22c55e";
  else color = "#8b5cf6";

  const getLabel = (val: number) => {
    if (val >= 90) return "Excellent";
    if (val >= 70) return "High";
    if (val >= 50) return "Medium";
    if (val >= 30) return "Low";
    return "Critical";
  };

  return (
    <div className={cn("flex flex-col items-center", className)}>
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} viewBox="0 0 100 100" className="overflow-visible">
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="#1e293b"
            strokeWidth="8"
            className="opacity-20"
          />
          {[
            { threshold: colorZones.excellent, color: "#8b5cf6" },
            { threshold: colorZones.high, color: "#22c55e" },
            { threshold: colorZones.medium, color: "#eab308" },
            { threshold: colorZones.low, color: "#f97316" },
            { threshold: colorZones.critical, color: "#ef4444" },
          ].map((zone, index) => (
            <circle
              key={index}
              cx="50"
              cy="50"
              r={radius}
              fill="none"
              stroke={zone.color}
              strokeWidth="8"
              strokeDasharray={circumference}
              strokeDashoffset={circumference * (1 - zone.threshold)}
              className="transition-all duration-500"
            />
          ))}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth="8"
            strokeDasharray={circumference}
            strokeDashoffset={offset < 0 ? 0 : offset}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <span className="text-2xl font-bold" style={{ color }}>{Math.round(percentage)}%</span>
            {showLabel && (
              <span className="text-xs text-zinc-400 block mt-1">{getLabel(percentage)}</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}