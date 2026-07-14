"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface CodeViewerProps {
  code: string;
  language?: string;
  className?: string;
  title?: string;
}

export function CodeViewer({ code, language = "python", className, title }: CodeViewerProps) {
  return (
    <div className={cn("rounded-xl border border-white/10 bg-black/40 overflow-hidden", className)}>
      {title && (
        <div className="flex items-center justify-between border-b border-white/10 bg-white/5 px-4 py-2">
          <span className="text-xs font-medium text-zinc-400">{title}</span>
          <span className="text-xs text-zinc-500">{language}</span>
        </div>
      )}
      <div className="p-4 overflow-x-auto">
        <pre className="font-mono text-sm leading-relaxed text-zinc-300">
          <motion.code
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            {code}
          </motion.code>
        </pre>
      </div>
    </div>
  );
}
