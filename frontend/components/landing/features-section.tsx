"use client";

import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/glass-card";
import { Code2, ShieldCheck, Zap, Workflow } from "lucide-react";

const features = [
  {
    icon: Code2,
    title: "Autonomous Code Generation",
    description: "AI writes production-ready code from natural language prompts in seconds.",
  },
  {
    icon: ShieldCheck,
    title: "Self-Healing Pipeline",
    description: "Detects compiler errors, runtime failures, and test regressions automatically.",
  },
  {
    icon: Workflow,
    title: "Sandbox Execution",
    description: "Secure, isolated execution environment with full test suite integration.",
  },
  {
    icon: Zap,
    title: "Iterative Refinement",
    description: "Continuous patching loop with intelligent error analysis until all tests pass.",
  },
];

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    staggerChildren: 0.1,
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

export function FeaturesSection() {
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
            Built for the future of software engineering
          </h2>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
            Every component designed for scale, security, and developer experience.
          </p>
        </motion.div>

        <motion.div
          variants={container}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          {features.map((feature) => (
            <motion.div key={feature.title} variants={item}>
              <GlassCard className="h-full p-6 hover:border-white/20 transition-colors group">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500/20 to-purple-500/20 mb-4 group-hover:scale-110 transition-transform">
                  <feature.icon className="h-6 w-6 text-blue-400" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-sm text-zinc-400 leading-relaxed">{feature.description}</p>
              </GlassCard>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
