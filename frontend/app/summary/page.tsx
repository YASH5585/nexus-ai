"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/glass-card";

const ALGORITHMS = [
  "Prime number checker",
  "Palindrome detection",
  "Quick sort & bubble sort",
  "Fibonacci sequence",
  "Queue data structure",
  "HTTP client helper",
  "Two pointers",
  "Binary search",
  "Breadth-first search",
  "Depth-first search",
  "Sliding window",
  "Dynamic programming / knapsack",
  "Hash map / frequency count",
];

const FEATURES = [
  "Autonomous code generation from natural language prompts",
  "Live testing with pytest-based validation",
  "Self-healing repair suggestions with confidence scoring",
  "Code review, performance analysis, and security scan",
  "Execution logs and reasoning trace",
  "Built-in AI simulator with no backend or API key required",
  "Responsive dashboard with animated algorithm flow",
  "GitHub Pages deployment ready for hackathon submission",
];

export default function SummaryPage() {
  const [copied, setCopied] = useState(false);

  const linkedInText = `Nexus AI - Autonomous Self-Healing Software Engineer

A full-stack AI system that generates code from prompts, runs tests, and self-heals until everything passes.

Live project: https://yash5585.github.io/nexus-ai/

Tech Stack:
- Frontend: Next.js, TypeScript, Tailwind CSS, Framer Motion
- Backend: FastAPI, Python
- Algorithms: two pointers, binary search, BFS, DFS, sliding window, dynamic programming, hashing, sorting, primes, and more

Key Features:
- Autonomous code generation
- Live testing and repair loop
- Confidence scoring and review suggestions
- Performance analysis
- Animated algorithm flow
- Fully responsive UI
- No external API dependency for demo mode`;

  const handleCopy = async () => {
    await navigator.clipboard.writeText(linkedInText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6 sm:py-10">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6 sm:mb-8"
      >
        <h1 className="text-2xl sm:text-3xl font-bold text-white">Project Summary</h1>
        <p className="mt-1 text-zinc-400 text-sm sm:text-base">
          Use this page for your submission, PPT, or LinkedIn post.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        <div className="lg:col-span-1 space-y-6">
          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-3">
              Project
            </h3>
            <p className="text-sm text-zinc-300">
              <span className="text-white font-semibold">Nexus AI</span> is an autonomous
              software engineering agent that generates code from natural language prompts,
              tests it, and self-heals through repair loops until all tests pass.
            </p>
            <p className="mt-2 text-xs text-zinc-500">
              Live URL:{" "}
              <span className="font-mono text-zinc-300">https://yash5585.github.io/nexus-ai/</span>
            </p>
            <p className="mt-1 text-xs text-zinc-500">
              GitHub:{" "}
              <span className="font-mono text-zinc-300">https://github.com/YASH5585/nexus-ai</span>
            </p>
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-3">
              Tech Stack
            </h3>
            <ul className="space-y-2 text-xs text-zinc-300">
              <li>
                <span className="text-white">Frontend:</span> Next.js, TypeScript, Tailwind
                CSS, Framer Motion
              </li>
              <li>
                <span className="text-white">Backend:</span> FastAPI, Python
              </li>
              <li>
                <span className="text-white">Deployment:</span> GitHub Pages, Render-ready
              </li>
              <li>
                <span className="text-white">Execution:</span> Browser-native simulator with
                no mandatory API dependency
              </li>
            </ul>
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-3">
              Live Metrics
            </h3>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="rounded-lg border border-white/10 bg-black/40 p-3">
                <div className="text-zinc-500">Status</div>
                <div className="mt-1 text-emerald-400 font-mono">Live</div>
              </div>
              <div className="rounded-lg border border-white/10 bg-black/40 p-3">
                <div className="text-zinc-500">Mode</div>
                <div className="mt-1 text-white font-mono">Simulator</div>
              </div>
              <div className="rounded-lg border border-white/10 bg-black/40 p-3">
                <div className="text-zinc-500">Algorithms</div>
                <div className="mt-1 text-white font-mono">{ALGORITHMS.length}+</div>
              </div>
              <div className="rounded-lg border border-white/10 bg-black/40 p-3">
                <div className="text-zinc-500">API Key</div>
                <div className="mt-1 text-emerald-400 font-mono">Optional</div>
              </div>
            </div>
          </GlassCard>
        </div>

        <div className="lg:col-span-2 space-y-6">
          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-3">
              Key Features
            </h3>
            <div className="grid sm:grid-cols-2 gap-3 text-xs text-zinc-300">
              {FEATURES.map((feature, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05, duration: 0.3 }}
                  className="rounded-lg border border-white/10 bg-black/40 p-3"
                >
                  {feature}
                </motion.div>
              ))}
            </div>
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-3">
              Algorithm Patterns Covered
            </h3>
            <div className="flex flex-wrap gap-2 text-xs">
              {ALGORITHMS.map((algo, idx) => (
                <span
                  key={idx}
                  className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-zinc-300"
                >
                  {algo}
                </span>
              ))}
            </div>
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-3">
              LinkedIn / Submission Text
            </h3>
            <pre className="rounded-lg border border-white/10 bg-black/40 p-4 text-xs text-zinc-300 whitespace-pre-wrap">
              {linkedInText}
            </pre>
            <button
              onClick={handleCopy}
              className="mt-3 rounded-lg border border-white/10 bg-white/5 px-4 py-2 text-xs text-white hover:bg-white/10"
            >
              {copied ? "Copied" : "Copy to clipboard"}
            </button>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
