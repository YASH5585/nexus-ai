"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface TextareaProps {
  label?: string;
  error?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  className?: string;
}

export function Textarea({
  label,
  error,
  value,
  onChange,
  placeholder,
  className,
}: TextareaProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="mb-1.5 block text-sm font-medium text-zinc-300">
          {label}
        </label>
      )}
      <motion.textarea
        whileFocus={{ scale: 1.005 }}
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className={cn(
          "w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-zinc-500",
          "backdrop-blur-sm transition-all duration-300",
          "focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 focus:outline-none",
          "disabled:opacity-50 disabled:cursor-not-allowed",
          "font-mono text-sm leading-relaxed resize-none",
          error && "border-red-500/50 focus:border-red-500/50 focus:ring-red-500/20",
          className
        )}
      />
      {error && (
        <motion.p
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-1.5 text-sm text-red-400"
        >
          {error}
        </motion.p>
      )}
    </div>
  );
}
