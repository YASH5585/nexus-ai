export const mockRunHistory = [
  {
    id: "1",
    prompt: "Write a Python function to find the longest palindromic substring",
    status: "success" as const,
    attempts: 2,
    duration: "4.2s",
    createdAt: "2026-07-14T14:32:00Z",
  },
  {
    id: "2",
    prompt: "Implement a binary search tree with insert and search",
    status: "success" as const,
    attempts: 1,
    duration: "2.8s",
    createdAt: "2026-07-14T13:15:00Z",
  },
  {
    id: "3",
    prompt: "Create a REST API endpoint for user authentication",
    status: "error" as const,
    attempts: 5,
    duration: "12.1s",
    createdAt: "2026-07-14T11:45:00Z",
  },
  {
    id: "4",
    prompt: "Write a function to merge two sorted linked lists",
    status: "success" as const,
    attempts: 3,
    duration: "6.5s",
    createdAt: "2026-07-13T16:20:00Z",
  },
];

export const mockExecutionSteps = [
  { id: "1", label: "Analyze Prompt", status: "completed" as const, detail: "Identified problem type: Algorithm" },
  { id: "2", label: "Generate Code", status: "completed" as const, detail: "Generated 45 lines of Python" },
  { id: "3", label: "Run Unit Tests", status: "completed" as const, detail: "3/5 tests passed" },
  { id: "4", label: "Analyze Failures", status: "completed" as const, detail: "Edge case: empty string" },
  { id: "5", label: "Patch Code", status: "completed" as const, detail: "Added null check and input validation" },
  { id: "6", label: "Re-run Tests", status: "completed" as const, detail: "5/5 tests passed" },
];

export const mockLogs = [
  { id: "1", timestamp: "14:32:01.234", level: "info" as const, message: "Starting execution run #1042" },
  { id: "2", timestamp: "14:32:01.456", level: "info" as const, message: "Prompt analysis complete: longest_palindromic_substring" },
  { id: "3", timestamp: "14:32:02.123", level: "info" as const, message: "Generated initial solution" },
  { id: "4", timestamp: "14:32:02.890", level: "warn" as const, message: "Test case failed: input='' expected='' got=None" },
  { id: "5", timestamp: "14:32:03.012", level: "info" as const, message: "Analyzing failure: missing empty string guard" },
  { id: "6", timestamp: "14:32:03.456", level: "info" as const, message: "Applying patch: add if not s: return ''" },
  { id: "7", timestamp: "14:32:04.123", level: "info" as const, message: "Re-running test suite" },
  { id: "8", timestamp: "14:32:04.567", level: "info" as const, message: "All tests passed (5/5)" },
  { id: "9", timestamp: "14:32:04.890", level: "info" as const, message: "Execution completed successfully" },
];

export const mockMetrics = {
  totalRuns: 1042,
  successRate: 94,
  avgAttempts: 2.3,
  avgDuration: "3.2s",
};
