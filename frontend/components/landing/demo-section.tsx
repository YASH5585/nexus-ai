"use client";

import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/glass-card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

export function DemoSection() {
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
            See it in action
          </h2>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto">
            Watch Nexus AI autonomously solve a coding problem from start to finish.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <GlassCard className="p-8 lg:p-12">
            <div className="grid lg:grid-cols-2 gap-8 items-center">
              <div>
                <h3 className="text-2xl font-bold text-white mb-4">
                  From Prompt to Production in Seconds
                </h3>
                <p className="text-zinc-400 leading-relaxed mb-6">
                  Describe your coding problem. Nexus AI generates the solution, validates it against
                  unit tests, and automatically patches any issues through an intelligent self-healing loop.
                </p>
                <ul className="space-y-3 mb-8">
                  {["Natural language prompt input", "Automated unit test generation", "Secure sandbox execution", "Intelligent error analysis", "Autonomous code patching"].map((item, i) => (
                    <motion.li
                      key={item}
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.3 + i * 0.1 }}
                      className="flex items-center gap-3 text-sm text-zinc-300"
                    >
                      <span className="h-1.5 w-1.5 rounded-full bg-blue-400" />
                      {item}
                    </motion.li>
                  ))}
                </ul>
                <Link href="/dashboard">
                  <Button size="lg" className="group">
                    Try it Live
                    <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                  </Button>
                </Link>
              </div>
              <div className="rounded-xl border border-white/10 bg-black/40 p-6 font-mono text-sm">
                <div className="flex items-center gap-2 mb-4">
                  <div className="h-3 w-3 rounded-full bg-red-500/80" />
                  <div className="h-3 w-3 rounded-full bg-amber-500/80" />
                  <div className="h-3 w-3 rounded-full bg-emerald-500/80" />
                  <span className="ml-2 text-xs text-zinc-500">terminal</span>
                </div>
                <div className="space-y-2 text-zinc-300">
                  <p><span className="text-blue-400">$</span> nexus run --prompt &ldquo;longest palindrome&rdquo;</p>
                  <p className="text-zinc-500">[INFO] Analyzing prompt...</p>
                  <p className="text-zinc-500">[INFO] Generating solution (attempt 1/5)...</p>
                  <p className="text-amber-400">[WARN] Test failed: edge case empty string</p>
                  <p className="text-zinc-500">[INFO] Analyzing failure...</p>
                  <p className="text-zinc-500">[INFO] Patching code...</p>
                  <p className="text-zinc-500">[INFO] Re-running tests...</p>
                  <p className="text-emerald-400">[SUCCESS] All tests passed (5/5)</p>
                  <p className="text-emerald-400">[DONE] Self-healing complete in 4.2s</p>
                </div>
              </div>
            </div>
          </GlassCard>
        </motion.div>
      </div>
    </section>
  );
}
