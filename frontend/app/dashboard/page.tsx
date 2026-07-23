"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { GlassCard } from "@/components/ui/glass-card";
import { ExecutionStats } from "@/components/dashboard/execution-stats";
import { ConfidenceMeter } from "@/components/dashboard/confidence-meter";
import { RepairHistory } from "@/components/dashboard/repair-history";
import { SecurityReport } from "@/components/dashboard/security-report";
import { PerformanceReport } from "@/components/dashboard/performance-report";
import { CodeReviewPanel } from "@/components/dashboard/code-review-panel";
import { LogsPanel } from "@/components/dashboard/logs-panel";
import { PromptEditor } from "@/components/dashboard/prompt-editor";
import { ProductionBadge } from "@/components/dashboard/production-badge";
import { runAgent, runConfidence, runReview, runPerformance, runTests, type AgentRunResponse } from "@/lib/api";

type AgentStatus = "idle" | "running" | "success" | "error";

interface ExecutionStat {
  label: string;
  value: string | number;
}

interface RepairEntry {
  id: string;
  timestamp: number;
  type: string;
  file: string;
  status: "success" | "failed" | "partial";
  duration: number;
  issues_fixed?: number;
  issues_remaining?: number;
  message?: string;
}

interface LogEntry {
  id: string;
  timestamp: string;
  level: "info" | "warn" | "error" | "debug";
  message: string;
}

function generateDemoResult(prompt: string): AgentRunResponse {
  const code = `def solution(input_data):\n    # Auto-generated for: ${prompt.slice(0, 40)}...\n    result = []\n    for item in input_data:\n        processed = item * 2\n        result.append(processed)\n    return result\n\n# Example usage\nif __name__ == "__main__":\n    data = [1, 2, 3, 4, 5]\n    print(solution(data))`;

  return {
    explanation: `Demo mode: generated a simple solution for "${prompt.slice(0, 60)}" because live OpenAI execution is unavailable right now.`,
    code,
    reason_for_modification: "Demo fallback generated a runnable Python skeleton.",
    confidence: 0.85,
    next_action: "succeed",
    reasoning: [
      { thought: "Understand the request", observation: "Prompt received successfully", confidence: 0.95, next_action: "retry" },
      { thought: "Generate initial code", observation: "Created Python function skeleton", confidence: 0.85, next_action: "retry" },
      { thought: "Review output", observation: "Code is runnable and matches prompt", confidence: 0.88, next_action: "succeed" },
    ],
    errors: [],
    repair: {
      reason: "No repair needed in demo mode.",
      code_change: "",
      confidence: 0.9,
      expected_outcome: "Code executes without runtime errors.",
    },
    attempts: 1,
    max_attempts: 5,
    status: "success",
  };
}

export default function DashboardPage() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<AgentStatus>("idle");
  const [result, setResult] = useState<AgentRunResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<number | null>(null);
  const [review, setReview] = useState<{ suggestions: Array<{ line?: number | null; severity: string; message: string; suggestion: string }>; passed: boolean; reviewTime: number } | null>(null);
  const [performance, setPerformance] = useState<{ complexity: { time_complexity: string; space_complexity: string; estimated_memory_mb?: number }; suggestions: Array<{ category: string; severity: string; message: string; suggestion: string; estimated_improvement: string }>; alternativeAlgorithms: Array<{ name: string; time_complexity: string; space_complexity: string; description: string }>; passed: boolean; analysisTime: number } | null>(null);
  const [testResult, setTestResult] = useState<{ passed: boolean; tests_passed: number; tests_failed: number; stdout: string; stderr: string; errors: string[]; exit_code: number } | null>(null);
  const [mode, setMode] = useState<"live" | "demo">("live");

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setStatus("running");
    setResult(null);
    setError(null);
    setConfidence(null);
    setReview(null);
    setPerformance(null);
    setTestResult(null);

    try {
      const agentResult = await runAgent(prompt);
      setResult(agentResult);
      setStatus(agentResult.status === "success" ? "success" : agentResult.status === "error" ? "error" : "running");
      setMode("live");
      await analyzeCode(agentResult.code || "");
    } catch (err) {
      const message = err instanceof Error ? err.message : "Something went wrong";
      setError(message);
      setStatus("error");
    } finally {
      setLoading(false);
    }
  };

  const analyzeCode = async (code: string) => {
    try {
      const [confidenceRes, reviewRes, performanceRes, testRes] = await Promise.all([
        runConfidence(code).catch(() => null),
        runReview(code).catch(() => null),
        runPerformance(code).catch(() => null),
        runTests(code).catch(() => null),
      ]);

      if (confidenceRes) setConfidence(confidenceRes.score);
      if (reviewRes) setReview({ ...reviewRes, reviewTime: (reviewRes as any).review_time });
      if (performanceRes) setPerformance({ ...performanceRes, alternativeAlgorithms: (performanceRes as any).alternative_algorithms ?? [], analysisTime: (performanceRes as any).analysis_time ?? 0 });
      if (testRes) setTestResult(testRes);
    } catch {
      // analysis is best-effort
    }
  };

  const currentCode = result?.code ?? "";

  const executionStats: ExecutionStat[] = result
    ? [
        { label: "Total Runs", value: result.attempts },
        { label: "Success Rate", value: result.status === "success" ? "100%" : "0%" },
        { label: "Attempts", value: `${result.attempts}/${result.max_attempts}` },
        { label: "Status", value: result.status },
      ]
    : [
        { label: "Total Runs", value: 0 },
        { label: "Success Rate", value: "0%" },
        { label: "Attempts", value: "0/0" },
        { label: "Status", value: "idle" },
      ];

  const confidenceValue = confidence ?? result?.confidence ?? 0;

  const repairs: RepairEntry[] = result?.repair
    ? [
        {
          id: "repair-1",
          timestamp: Date.now(),
          type: result.next_action,
          file: "solution.py",
          status: result.status === "success" ? "success" : result.status === "error" ? "failed" : "partial",
          duration: 0,
          issues_fixed: result.errors.length,
          issues_remaining: 0,
          message: result.repair.reason,
        },
      ]
    : [];

  const logs: LogEntry[] = result?.reasoning.map((step, index) => ({
    id: `log-${index}`,
    timestamp: new Date(Date.now() - (result.reasoning.length - index) * 1000).toISOString(),
    level: step.next_action === "succeed" ? "info" : "warn",
    message: `${step.thought} | ${step.observation}`,
  })) ?? [];

  const normalizedReview = review
    ? {
        ...review,
        suggestions: review.suggestions.map((s) => ({
          category: (s as any).category ?? "general",
          severity: s.severity,
          line_number: (s as any).line ?? (s as any).line_number ?? null,
          message: s.message,
          suggestion: s.suggestion,
        })),
      }
    : null;

  const securityScan = {
    issues: [],
    passed: true,
    scanTime: 0,
  };

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6 sm:mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3"
      >
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white flex items-center gap-3">
            Nexus AI Dashboard
            <ProductionBadge />
          </h1>
          <p className="mt-1 text-zinc-400 text-sm sm:text-base">Generate, test, and heal code autonomously</p>
        </div>
        <span className="text-xs text-zinc-500">Mode: {mode === "demo" ? "Demo" : "Live"}</span>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
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
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-4">
              Execution Stats
            </h3>
            <ExecutionStats stats={executionStats} />
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-4">
              Confidence Score
            </h3>
            <div className="flex justify-center">
              <ConfidenceMeter value={confidenceValue * 100} size={140} />
            </div>
            {confidence !== null && (
              <p className="text-center text-xs text-zinc-500 mt-2">Live confidence</p>
            )}
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-4">
              Recent Repairs
            </h3>
            <RepairHistory repairs={repairs} />
          </GlassCard>
        </div>

        <div className="lg:col-span-2 space-y-6">
          <GlassCard className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider">
                Generated Code
              </h3>
              {result?.status && (
                <span className="text-xs text-zinc-500 font-mono">{result.status}</span>
              )}
            </div>
            <div className="rounded-lg border border-white/10 bg-black/40 p-4">
              {currentCode ? (
                <pre className="text-sm text-zinc-200 font-mono whitespace-pre-wrap">{currentCode}</pre>
              ) : (
                <p className="text-sm text-zinc-500">No code generated yet. Enter a prompt and click Generate & Heal.</p>
              )}
            </div>
            {error && <p className="mt-2 text-sm text-red-400">{error}</p>}
            {testResult && (
              <div className="mt-3 text-xs text-zinc-400">
                <span className="font-mono">tests: </span>
                <span className={testResult.passed ? "text-emerald-400" : "text-red-400"}>
                  {testResult.passed ? "passed" : "failed"}
                </span>
                <span className="ml-2 font-mono">{testResult.tests_passed}/{testResult.tests_passed + testResult.tests_failed}</span>
                {testResult.errors.length > 0 && (
                  <span className="ml-2 text-red-300">{testResult.errors.join("; ")}</span>
                )}
              </div>
            )}
          </GlassCard>

          {result?.algorithm && (
            <GlassCard className="p-6">
              <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-2">
                Algorithm Flow: {result.algorithm}
              </h3>
              {result.algorithm_explanation && (
                <p className="text-xs text-zinc-400 mb-4">{result.algorithm_explanation}</p>
              )}
              <div className="flex flex-wrap gap-3">
                {(result.algorithm_steps || []).map((step, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.12, duration: 0.35 }}
                    className="flex-1 min-w-[140px] rounded-lg border border-white/10 bg-black/40 p-3 text-xs text-zinc-300"
                  >
                    <span className="mb-1 block text-emerald-400 font-mono">Step {idx + 1}</span>
                    {step}
                  </motion.div>
                ))}
              </div>
              {result.algorithm_complexity && (
                <div className="mt-4 flex flex-wrap gap-3 text-xs text-zinc-400">
                  <span className="rounded-full border border-white/10 bg-black/40 px-3 py-1 font-mono">
                    Time: {result.algorithm_complexity.time}
                  </span>
                  <span className="rounded-full border border-white/10 bg-black/40 px-3 py-1 font-mono">
                    Space: {result.algorithm_complexity.space}
                  </span>
                </div>
              )}
              {result.algorithm_use_cases && result.algorithm_use_cases.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2 text-[10px] text-zinc-500">
                  {result.algorithm_use_cases.map((item, idx) => (
                    <span key={idx} className="rounded-full border border-white/10 bg-white/5 px-2 py-1">
                      {item}
                    </span>
                  ))}
                </div>
              )}
            </GlassCard>
          )}

          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-4">
              Security Scan
            </h3>
            <SecurityReport
              issues={securityScan.issues}
              passed={securityScan.passed}
              scanTime={securityScan.scanTime}
            />
            <p className="mt-2 text-xs text-zinc-500">Security scan endpoint not yet exposed; showing placeholder.</p>
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-4">
              Performance Analysis
            </h3>
            {performance ? (
              <PerformanceReport
                complexity={performance.complexity}
                suggestions={performance.suggestions}
                alternativeAlgorithms={performance.alternativeAlgorithms}
                passed={performance.passed}
                analysisTime={performance.analysisTime}
              />
            ) : (
              <p className="text-sm text-zinc-500">Run a prompt to see performance analysis.</p>
            )}
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-4">
              Code Review
            </h3>
            {normalizedReview ? (
              <CodeReviewPanel
                suggestions={normalizedReview.suggestions}
                passed={normalizedReview.passed}
                reviewTime={normalizedReview.reviewTime}
              />
            ) : (
              <p className="text-sm text-zinc-500">Run a prompt to see code review.</p>
            )}
          </GlassCard>

          <GlassCard className="p-6">
            <h3 className="text-sm font-semibold text-zinc-300 uppercase tracking-wider mb-4">
              Execution Logs
            </h3>
            <LogsPanel logs={logs} />
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
