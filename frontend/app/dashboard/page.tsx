"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { PromptEditor } from "@/components/dashboard/prompt-editor";
import { CodeViewer } from "@/components/dashboard/code-viewer";
import { DiffViewer } from "@/components/dashboard/diff-viewer";
import { ExecutionTimeline } from "@/components/dashboard/execution-timeline";
import { LogsPanel } from "@/components/dashboard/logs-panel";
import { MetricCard } from "@/components/dashboard/metrics-grid";
import { SuccessIndicator } from "@/components/dashboard/success-indicator";
import { GlassCard } from "@/components/ui/glass-card";
import { mockExecutionSteps, mockLogs, mockMetrics } from "@/lib/mock-data";
import { Button } from "@/components/ui/button";
import { Activity, Zap, Shield, Clock } from "lucide-react";

export default function DashboardPage() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<"idle" | "running" | "success" | "error">("idle");
  const [showDiff, setShowDiff] = useState(false);
  const [retryCount, setRetryCount] = useState(0);

  const handleGenerate = () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setStatus("running");
    setRetryCount(0);
    setShowDiff(false);

    setTimeout(() => {
      setStatus("success");
      setLoading(false);
      setShowDiff(true);
    }, 3000);
  };

  const currentCode = `def longest_palindromic_substring(s: str) -> str:
    if not s:
        return ""
    
    start, max_len = 0, 1
    
    for i in range(len(s)):
        # Odd length palindromes
        l, r = i, i
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if r - l + 1 > max_len:
                start = l
                max_len = r - l + 1
            l -= 1
            r += 1
        
        # Even length palindromes
        l, r = i, i + 1
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if r - l + 1 > max_len:
                start = l
                max_len = r - l + 1
            l -= 1
            r += 1
    
    return s[start:start + max_len]`;

  const oldCode = `def longest_palindromic_substring(s: str) -> str:
    start, max_len = 0, 1
    
    for i in range(len(s)):
        l, r = i, i
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if r - l + 1 > max_len:
                start = l
                max_len = r - l + 1
            l -= 1
            r += 1
        
        l, r = i, i + 1
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if r - l + 1 > max_len:
                start = l
                max_len = r - l + 1
            l -= 1
            r += 1
    
    return s[start:start + max_len]`;

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="mt-1 text-zinc-400">Generate, test, and heal code autonomously</p>
      </motion.div>

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <GlassCard className="p-6">
            <PromptEditor
              prompt={prompt}
              onPromptChange={setPrompt}
              onGenerate={handleGenerate}
              loading={loading}
              status={status}
            />
          </GlassCard>

          <GlassCard className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider">
                Metrics
              </h3>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <MetricCard label="Total Runs" value={mockMetrics.totalRuns} icon={<Activity className="h-4 w-4" />} />
              <MetricCard label="Success Rate" value={`${mockMetrics.successRate}%`} trend="up" trendValue="+2.1%" icon={<Zap className="h-4 w-4" />} />
              <MetricCard label="Avg Attempts" value={mockMetrics.avgAttempts} icon={<Shield className="h-4 w-4" />} />
              <MetricCard label="Avg Duration" value={mockMetrics.avgDuration} icon={<Clock className="h-4 w-4" />} />
            </div>
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-4">
              Execution
            </h3>
            <ExecutionTimeline steps={mockExecutionSteps} currentStep={status === "running" ? 3 : 6} />
          </GlassCard>
        </div>

        <div className="lg:col-span-2 space-y-6">
          <AnimatePresence>
            {status !== "idle" && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
              >
                <SuccessIndicator status={status} />
              </motion.div>
            )}
          </AnimatePresence>

          <div className="grid md:grid-cols-2 gap-6">
            <GlassCard className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider">
                  Generated Code
                </h3>
                {showDiff && (
                  <Button variant="ghost" size="sm" onClick={() => setShowDiff(!showDiff)}>
                    {showDiff ? "Hide Diff" : "Show Diff"}
                  </Button>
                )}
              </div>
              {showDiff ? (
                <DiffViewer oldCode={oldCode} newCode={currentCode} />
              ) : (
                <CodeViewer code={currentCode} language="python" title="solution.py" />
              )}
            </GlassCard>

            <GlassCard className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider">
                  Unit Tests
                </h3>
                <span className="text-xs text-zinc-500">pytest</span>
              </div>
              <div className="rounded-xl border border-white/10 bg-black/40 p-4">
                <div className="space-y-3">
                  {[
                    { name: "test_empty_string", status: "pass" },
                    { name: "test_single_char", status: "pass" },
                    { name: "test_even_length", status: "pass" },
                    { name: "test_odd_length", status: "pass" },
                    { name: "test_long_palindrome", status: "pass" },
                  ].map((test, i) => (
                    <motion.div
                      key={test.name}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="flex items-center justify-between py-2 border-b border-white/5 last:border-0"
                    >
                      <span className="font-mono text-sm text-zinc-300">{test.name}</span>
                      <span className="text-xs text-emerald-400">PASS</span>
                    </motion.div>
                  ))}
                </div>
              </div>
            </GlassCard>
          </div>

          <GlassCard className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider">
                Execution Logs
              </h3>
              <div className="flex items-center gap-2">
                <span className="text-xs text-zinc-500">Retry count:</span>
                <span className="text-xs font-mono text-blue-400">{retryCount}</span>
              </div>
            </div>
            <LogsPanel logs={mockLogs} />
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
