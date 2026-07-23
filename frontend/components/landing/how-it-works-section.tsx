"use client";

import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/glass-card";

const steps = [
  {
    number: "01",
    title: "Enter Prompt",
    description: "Describe your coding problem in natural language. No constraints, no templates.",
  },
  {
    number: "02",
    title: "AI Generates Code",
    description: "OpenAI GPT-4o produces production-ready code with full context awareness.",
  },
  {
    number: "03",
    title: "Sandbox Execution",
    description: "Code runs in an isolated environment with comprehensive unit tests.",
  },
  {
    number: "04",
    title: "Error Analysis",
    description: "Compiler errors, runtime failures, and test regressions are categorized and analyzed.",
  },
  {
    number: "05",
    title: "Autonomous Repair",
    description: "AI patches the code with precise modifications based on error context.",
  },
  {
    number: "06",
    title: "Retry & Iterate",
    description: "The loop continues until all tests pass or the retry limit is reached.",
  },
];

export function HowItWorksSection() {
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
            How it works
          </h2>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
            A fully autonomous loop from prompt to production-ready code.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {steps.map((step, i) => (
            <motion.div
              key={step.number}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
            >
              <GlassCard className="h-full p-6 relative overflow-hidden group">
                <div className="absolute top-4 right-4 text-6xl font-bold text-white/5 group-hover:text-white/10 transition-colors">
                  {step.number}
                </div>
                <div className="relative">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold mb-4">
                    {step.number}
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-2">{step.title}</h3>
                  <p className="text-sm text-zinc-400 leading-relaxed">{step.description}</p>
                </div>
              </GlassCard>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
