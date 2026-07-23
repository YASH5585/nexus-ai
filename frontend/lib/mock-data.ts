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

export const mockSecurityIssues = [
  {
    category: "injection",
    severity: "critical" as const,
    risk: "Potential SQL injection vulnerability in database queries",
    line_number: 42,
    recommendation: "Use parameterized queries or prepared statements",
  },
  {
    category: "authentication",
    severity: "high" as const,
    risk: "Passwords stored in plain text without hashing",
    line_number: 18,
    recommendation: "Implement bcrypt or argon2 password hashing",
  },
  {
    category: "xss",
    severity: "high" as const,
    risk: "User input rendered without sanitization",
    line_number: 67,
    recommendation: "Escape HTML entities or use templating engine auto-escaping",
  },
  {
    category: "config",
    severity: "medium" as const,
    risk: "Hardcoded API keys in source code",
    line_number: 5,
    recommendation: "Move secrets to environment variables or secret management",
  },
  {
    category: "logging",
    severity: "low" as const,
    risk: "Sensitive data may be logged in error messages",
    line_number: 123,
    recommendation: "Sanitize logs before writing to file",
  },
];

export const mockSecurityScan = {
  passed: false,
  scanTime: 1.24,
  issues: mockSecurityIssues,
};

export const mockPerformanceData = {
  complexity: {
    time_complexity: "O(n^2)",
    space_complexity: "O(n)",
    estimated_memory_mb: 12.5,
  },
  suggestions: [
    {
      category: "algorithm",
      severity: "high" as const,
      message: "Nested loop creates quadratic time complexity",
      suggestion: "Consider using a hash map for O(n) lookup",
      estimated_improvement: "-50% runtime",
    },
    {
      category: "memory",
      severity: "medium" as const,
      message: "Creating unnecessary string copies in loop",
      suggestion: "Use string builder pattern or yield results",
      estimated_improvement: "-30% memory",
    },
  ],
  alternativeAlgorithms: [
    {
      name: "Manacher's Algorithm",
      time_complexity: "O(n)",
      space_complexity: "O(n)",
      description: "Linear time palindrome detection",
    },
    {
      name: "Rolling Hash",
      time_complexity: "O(n)",
      space_complexity: "O(1)",
      description: "Constant space with rolling hash technique",
    },
  ],
};

export const mockCodeReview = {
  suggestions: [
    {
      category: "unused_variable",
      severity: "low" as const,
      line_number: 15,
      message: "Variable 'temp' is never used",
      suggestion: "Remove unused variable to improve clarity",
    },
    {
      category: "magic_number",
      severity: "low" as const,
      line_number: 22,
      message: "Magic number 100 used for threshold",
      suggestion: "Define as named constant MAX_THRESHOLD",
    },
    {
      category: "poor_naming",
      severity: "medium" as const,
      line_number: 8,
      message: "Variable name 'x' is not descriptive",
      suggestion: "Rename to 'index' or 'position'",
    },
    {
      category: "missing_type_hints",
      severity: "medium" as const,
      line_number: 5,
      message: "Function lacks type hints for parameters",
      suggestion: "Add type hints: def func(s: str) -> str:",
    },
    {
      category: "duplicate_code",
      severity: "high" as const,
      line_number: 35,
      message: "Similar palindrome expansion logic duplicated",
      suggestion: "Extract to helper function expand_palindrome()",
    },
  ],
  passed: false,
  reviewTime: 0.87,
};

export const mockRepairHistory = [
  {
    id: "repair-1",
    timestamp: Date.now() - 1000 * 60 * 5,
    type: "patch",
    file: "solution.py:15-18",
    status: "success" as const,
    duration: 0.45,
    issues_fixed: 3,
    message: "Fixed edge cases and added input validation",
  },
  {
    id: "repair-2",
    timestamp: Date.now() - 1000 * 60 * 15,
    type: "refactor",
    file: "solution.py:35-50",
    status: "success" as const,
    duration: 1.23,
    issues_fixed: 2,
    message: "Refactored palindrome expansion logic",
  },
  {
    id: "repair-3",
    timestamp: Date.now() - 1000 * 60 * 30,
    type: "optimize",
    file: "solution.py:1-10",
    status: "partial" as const,
    duration: 2.67,
    issues_fixed: 1,
    issues_remaining: 1,
    message: "Partial optimization - memory improved but time complexity same",
  },
];

export const mockExecutionStats = [
  {
    label: "Total Runs",
    value: 1042,
    icon: "activity",
  },
  {
    label: "Success Rate",
    value: 94,
    suffix: "%",
    change: 2.1,
    icon: "zap",
  },
  {
    label: "Avg Attempts",
    value: 2.3,
    change: -0.4,
    icon: "shield",
  },
  {
    label: "Avg Duration",
    value: "3.2s",
    change: -0.5,
    icon: "clock",
  },
];

export const mockComplexity = {
  time: "O(n^2)",
  space: "O(n)",
  confidence: 78,
};
