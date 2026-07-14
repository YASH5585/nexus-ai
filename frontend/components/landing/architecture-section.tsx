"use client";

import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/glass-card";
import { Box, Server, Shield, GitBranch } from "lucide-react";

const architecture = [
  {
    icon: Box,
    title: "Frontend Layer",
    description: "Next.js 15 + React + TypeScript + Tailwind CSS + Framer Motion. Glassmorphism UI with real-time updates.",
    tech: ["Next.js", "React", "TypeScript", "Tailwind", "Framer Motion"],
  },
  {
    icon: Server,
    title: "Backend Layer",
    description: "FastAPI + Python. Modular routers, dependency injection, structured logging with structlog.",
    tech: ["FastAPI", "Python", "Pydantic", "Structlog", "Uvicorn"],
  },
  {
    icon: Shield,
    title: "AI Layer",
    description: "OpenAI Responses API (GPT-4o). Autonomous agent with structured reasoning and self-healing loops.",
    tech: ["OpenAI", "GPT-4o", "Agents", "Reasoning", "Self-Healing"],
  },
  {
    icon: GitBranch,
    title: "Execution Layer",
    description: "Secure sandbox with subprocess isolation. pytest integration, syntax validation, and timeout protection.",
    tech: ["Sandbox", "pytest", "Subprocess", "Timeout", "Isolation"],
  },
];

export function ArchitectureSection() {
  return (
    <section className="py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Production-grade architecture
          </h2>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
            Built with modern, scalable technologies. Every layer designed for reliability and performance.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {architecture.map((layer, i) => (
            <motion.div
              key={layer.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
            >
              <GlassCard className="h-full p-6 hover:border-white/20 transition-colors">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500/20 to-purple-500/20 shrink-0">
                    <layer.icon className="h-6 w-6 text-blue-400" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-white mb-2">{layer.title}</h3>
                    <p className="text-sm text-zinc-400 leading-relaxed mb-4">{layer.description}</p>
                    <div className="flex flex-wrap gap-2">
                      {layer.tech.map((t) => (
                        <span
                          key={t}
                          className="text-xs px-2 py-1 rounded-full bg-white/5 border border-white/10 text-zinc-300"
                        >
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </GlassCard>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
