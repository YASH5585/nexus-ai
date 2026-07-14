"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface PromptEditorProps {
  prompt: string;
  onPromptChange: (value: string) => void;
  onGenerate: () => void;
  loading?: boolean;
  status?: "idle" | "running" | "success" | "error";
}

export function PromptEditor({
  prompt,
  onPromptChange,
  onGenerate,
  loading = false,
  status = "idle",
}: PromptEditorProps) {
  const statusConfig = {
    idle: { text: "Ready", variant: "neutral" as const },
    running: { text: "Running", variant: "info" as const },
    success: { text: "Success", variant: "success" as const },
    error: { text: "Failed", variant: "error" as const },
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white">Prompt</h2>
        <Badge variant={statusConfig[status].variant}>{statusConfig[status].text}</Badge>
      </div>
      <Textarea
        label="Describe the coding problem"
        placeholder="e.g., Write a Python function that finds the longest palindromic substring in O(n) time..."
        value={prompt}
        onChange={(e) => onPromptChange(e.target.value)}
        className="min-h-[160px]"
      />
      <div className="flex items-center justify-between">
        <div className="text-xs text-zinc-500">
          Press <kbd className="rounded bg-white/10 px-1.5 py-0.5 font-mono">Cmd</kbd> +{" "}
          <kbd className="rounded bg-white/10 px-1.5 py-0.5 font-mono">Enter</kbd> to run
        </div>
        <Button
          onClick={onGenerate}
          loading={loading}
          disabled={!prompt.trim() || loading}
          size="lg"
        >
          {loading ? "Healing..." : "Generate & Heal"}
        </Button>
      </div>
    </div>
  );
}
