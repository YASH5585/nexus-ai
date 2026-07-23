export type AgentStatus = "idle" | "running" | "success" | "error";

export interface AgentRunResponse {
  explanation: string;
  code: string;
  reason_for_modification: string;
  confidence: number;
  next_action: string;
  reasoning: Array<{
    thought: string;
    observation: string;
    confidence: number;
    next_action: string;
  }>;
  errors: Array<{
    category: string;
    message: string;
    file?: string | null;
    line?: number | null;
    stack_trace?: string | null;
    test_name?: string | null;
  }>;
  repair: {
    reason: string;
    code_change: string;
    confidence: number;
    expected_outcome: string;
  } | null;
  attempts: number;
  max_attempts: number;
  status: "running" | "success" | "error";
  algorithm?: string;
  algorithm_steps?: string[];
  algorithm_complexity?: { time: string; space: string };
  algorithm_use_cases?: string[];
  algorithm_explanation?: string;
}

export interface ConfidenceResponse {
  score: number;
  grade: string;
  explanation: string;
}

export interface ReviewResponse {
  suggestions: Array<{
    line?: number | null;
    severity: string;
    message: string;
    suggestion: string;
  }>;
  passed: boolean;
  review_time: number;
}

export interface PerformanceResponse {
  complexity: {
    time_complexity: string;
    space_complexity: string;
    estimated_memory_mb?: number;
  };
  suggestions: Array<{
    category: string;
    severity: string;
    message: string;
    suggestion: string;
    estimated_improvement: string;
  }>;
  alternative_algorithms: Array<{
    name: string;
    time_complexity: string;
    space_complexity: string;
    description: string;
  }>;
  passed: boolean;
  analysis_time: number;
}

export interface TestResponse {
  passed: boolean;
  attempt: number;
  execution_time: number;
  tests_passed: number;
  tests_failed: number;
  stdout: string;
  stderr: string;
  errors: string[];
  exit_code: number;
}

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function pick(arr: string[], r: () => number = Math.random) {
  return arr[Math.floor(r() * arr.length)];
}

function generateCodeSnippet(prompt: string): { code: string; algorithm: string; explanation: string; steps: string[]; complexity: { time: string; space: string }; use_cases: string[] } {
  const lower = prompt.toLowerCase();
  if (lower.includes("prime")) {
    return {
      algorithm: "Primality Test & Prime Generation",
      code: `def is_prime(n: int) -> bool:\n    if n < 2:\n        return False\n    if n % 2 == 0:\n        return n == 2\n    i = 3\n    while i * i <= n:\n        if n % i == 0:\n            return False\n        i += 2\n    return True\n\ndef primes(limit: int):\n    return [n for n in range(2, limit + 1) if is_prime(n)]`,
      explanation: "This solution checks whether a number is prime by testing divisibility only up to its square root. It skips even numbers after checking 2, which makes it faster than checking every number. The second function generates all primes up to a given limit using that check.",
      steps: [
        "If the number is less than 2, it is not prime.",
        "If the number is even, only 2 is prime.",
        "Test odd divisors from 3 up to the square root of the number.",
        "If any divisor divides the number evenly, it is not prime.",
        "Otherwise, the number is prime.",
      ],
      complexity: { time: "O(√n)", space: "O(1)" },
      use_cases: ["Cryptography", "Number theory problems", "Finding prime ranges", "Competitive programming"],
    };
  }
  if (lower.includes("palindrome")) {
    return {
      algorithm: "Palindrome Detection & Longest Palindrome Substring",
      code: `def is_palindrome(text: str) -> bool:\n    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())\n    return cleaned == cleaned[::-1]\n\ndef longest_palindrome(s: str) -> str:\n    longest = ""\n    for i in range(len(s)):\n        for j in range(i + 1, len(s) + 1):\n            if is_palindrome(s[i:j]) and len(s[i:j]) > len(longest):\n                longest = s[i:j]\n    return longest`,
      explanation: "The first function removes non-alphanumeric characters, lowercases everything, and checks whether the string reads the same forwards and backwards. The second function scans every possible substring and keeps the longest one that is a palindrome.",
      steps: [
        "Normalize the text by removing spaces/punctuation and lowercasing it.",
        "Compare the cleaned string with its reverse.",
        "For longest palindrome, check every possible substring.",
        "Keep the longest substring that still reads the same forwards and backwards.",
        "Return the longest palindrome found.",
      ],
      complexity: { time: "O(n^2)", space: "O(n)" },
      use_cases: ["Text validation", "String processing", "Interview problems", "DNA sequence analysis"],
    };
  }
  if (lower.includes("sort")) {
    return {
      algorithm: "Quick Sort & Bubble Sort",
      code: `def quick_sort(items):\n    if len(items) <= 1:\n        return items\n    pivot = items[len(items) // 2]\n    left = [x for x in items if x < pivot]\n    middle = [x for x in items if x == pivot]\n    right = [x for x in items if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right)\n\ndef bubble_sort(items):\n    n = len(items)\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if items[j] > items[j + 1]:\n                items[j], items[j + 1] = items[j + 1], items[j]\n    return items`,
      explanation: "Quick Sort picks a pivot and splits the list into three parts: smaller, equal, and larger. It then recursively sorts the smaller and larger parts. Bubble Sort repeatedly swaps adjacent out-of-order elements until the list is sorted.",
      steps: [
        "Quick Sort: choose a pivot element from the list.",
        "Split items into less than pivot, equal to pivot, and greater than pivot.",
        "Recursively sort the left and right partitions.",
        "Combine the sorted left, pivot, and sorted right.",
        "Bubble Sort: walk through the list and swap neighbors that are out of order.",
        "Repeat passes until no swaps are needed.",
      ],
      complexity: { time: "O(n log n) average", space: "O(n)" },
      use_cases: ["General sorting", "Databases", "Data pipelines", "Learning recursion"],
    };
  }
  if (lower.includes("fibonacci")) {
    return {
      algorithm: "Fibonacci Sequence",
      code: `def fib(n: int) -> int:\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b\n\ndef fib_sequence(n: int) -> list[int]:\n    return [fib(i) for i in range(n)]`,
      explanation: "Each Fibonacci number is the sum of the two preceding ones, starting from 0 and 1. This implementation computes values iteratively in linear time and constant space instead of using exponential recursion.",
      steps: [
        "Start with the first two Fibonacci numbers: 0 and 1.",
        "For each new position, add the previous two numbers.",
        "Store the current pair and shift forward.",
        "Repeat until reaching the desired position.",
        "Return the value or the full sequence.",
      ],
      complexity: { time: "O(n)", space: "O(1)" },
      use_cases: ["Math education", "Dynamic programming examples", "Modeling growth patterns", "Technical interviews"],
    };
  }
  if (lower.includes("class") || lower.includes("object")) {
    return {
      algorithm: "Queue Data Structure",
      code: `class TaskQueue:\n    def __init__(self):\n        self._items = []\n\n    def enqueue(self, item):\n        self._items.append(item)\n\n    def dequeue(self):\n        if not self._items:\n            raise IndexError("empty")\n        return self._items.pop(0)\n\n    def __len__(self):\n        return len(self._items)`,
      explanation: "A queue follows first-in, first-out ordering. Items are added at the back with enqueue and removed from the front with dequeue. This class wraps a Python list to show the core queue operations clearly.",
      steps: [
        "Create an internal list to hold items.",
        "Enqueue adds a new item to the end of the list.",
        "Dequeue removes and returns the first item in the list.",
        "If the queue is empty, dequeue raises an error instead of crashing silently.",
        "Track size with the built-in length of the internal list.",
      ],
      complexity: { time: "O(1) average", space: "O(n)" },
      use_cases: ["Task scheduling", "Breadth-first search", "Ordered processing", "Job queues"],
    };
  }
  if (lower.includes("api") || lower.includes("http")) {
    return {
      algorithm: "HTTP Client Helper",
      code: `import requests\n\ndef fetch_json(url: str):\n    response = requests.get(url, timeout=10)\n    response.raise_for_status()\n    return response.json()\n\ndef post_json(url: str, payload: dict):\n    response = requests.post(url, json=payload, timeout=10)\n    response.raise_for_status()\n    return response.json()`,
      explanation: "These helpers wrap common HTTP GET and POST calls. They set a timeout so the request does not hang forever, check for HTTP errors, and automatically parse JSON responses.",
      steps: [
        "Create a GET or POST request to the provided URL.",
        "Attach the payload as JSON for POST requests.",
        "Set a timeout so slow servers do not block the program.",
        "Raise an exception if the server returns an error status.",
        "Parse and return the JSON response body.",
      ],
      complexity: { time: "O(1) request", space: "O(response size)" },
      use_cases: ["REST API consumption", "Microservices", "Data fetching", "Automation scripts"],
    };
  }
  if (lower.includes("two pointer") || lower.includes("2 pointer") || lower.includes("pair") || lower.includes("container with most water") || lower.includes("trapping rain water")) {
    return {
      algorithm: "Two Pointers",
      code: `def two_pointers_example(nums, target):\n    left, right = 0, len(nums) - 1\n    result = []\n    while left < right:\n        s = nums[left] + nums[right]\n        if s == target:\n            result.append([left, right])\n            left += 1\n            right -= 1\n        elif s < target:\n            left += 1\n        else:\n            right -= 1\n    return result`,
      explanation: "Two pointers is a pattern where two indices start at different positions and move toward each other or in the same direction. It is especially useful for sorted arrays because moving one pointer updates the sum in a predictable way.",
      steps: [
        "Start one pointer at the beginning and another at the end of the sorted array.",
        "Calculate the current sum or comparison using both pointers.",
        "If the sum is too small, move the left pointer right to increase it.",
        "If the sum is too large, move the right pointer left to decrease it.",
        "If the sum matches the target, record the pair and move both pointers.",
        "Repeat until the pointers meet.",
      ],
      complexity: { time: "O(n)", space: "O(1)" },
      use_cases: ["Two sum", "Container with most water", "Trapping rain water", "Palindrome checks"],
    };
  }
  if (lower.includes("binary search")) {
    return {
      algorithm: "Binary Search",
      code: `def binary_search(nums, target):\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1`,
      explanation: "Binary search repeatedly splits a sorted array in half. It compares the middle element with the target and discards the half that cannot contain the target, making it much faster than checking every element.",
      steps: [
        "Start with the full search range from index 0 to the last index.",
        "Find the middle index of the current range.",
        "If the middle value equals the target, return its index.",
        "If the middle value is less than the target, search the right half.",
        "If the middle value is greater than the target, search the left half.",
        "If the range is exhausted, the target is not present.",
      ],
      complexity: { time: "O(log n)", space: "O(1)" },
      use_cases: ["Searching sorted data", "Finding boundaries", "Interview problems", "Library implementations"],
    };
  }
  if (lower.includes("bfs") || lower.includes("breadth first") || lower.includes("level order")) {
    return {
      algorithm: "Breadth-First Search",
      code: `from collections import deque\n\ndef bfs(graph, start):\n    visited = {start}\n    order = []\n    queue = deque([start])\n    while queue:\n        node = queue.popleft()\n        order.append(node)\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)\n    return order`,
      explanation: "BFS explores a graph level by level using a queue. It visits all immediate neighbors before moving to the next layer, which makes it useful for shortest-path problems in unweighted graphs.",
      steps: [
        "Start from the given node and mark it visited.",
        "Add it to a queue and an output list.",
        "While the queue is not empty, remove one node.",
        "Visit all unvisited neighbors of that node.",
        "Mark those neighbors visited and add them to the queue.",
        "Continue until every reachable node is visited.",
      ],
      complexity: { time: "O(V + E)", space: "O(V)" },
      use_cases: ["Shortest path", "Social networks", "Web crawling", "AI pathfinding"],
    };
  }
  if (lower.includes("dfs") || lower.includes("depth first")) {
    return {
      algorithm: "Depth-First Search",
      code: `def dfs(graph, node, visited=None):\n    if visited is None:\n        visited = set()\n    visited.add(node)\n    order = [node]\n    for neighbor in graph.get(node, []):\n        if neighbor not in visited:\n            order.extend(dfs(graph, neighbor, visited))\n    return order`,
      explanation: "DFS explores as far as possible along one branch before backtracking. It uses a stack—either explicitly or through recursion—and is great for exploring all possible paths or detecting cycles.",
      steps: [
        "Start from the given node and mark it visited.",
        "Visit one neighbor and immediately continue from that neighbor.",
        "Recursively explore deeper before returning to the current node.",
        "If no unvisited neighbors remain, backtrack.",
        "Collect visited nodes in traversal order.",
        "Stop when all reachable nodes are visited.",
      ],
      complexity: { time: "O(V + E)", space: "O(V)" },
      use_cases: ["Maze solving", "Cycle detection", "Topological sorting", "Path enumeration"],
    };
  }
  if (lower.includes("sliding window")) {
    return {
      algorithm: "Sliding Window",
      code: `def max_sum_subarray(nums, k):\n    window_sum = sum(nums[:k])\n    max_sum = window_sum\n    for i in range(len(nums) - k):\n        window_sum = window_sum - nums[i] + nums[i + k]\n        max_sum = max(max_sum, window_sum)\n    return max_sum`,
      explanation: "Sliding window maintains a moving subset of elements and updates the result by removing the leftmost element and adding the next right element. This avoids recomputing the whole window from scratch every time.",
      steps: [
        "Create a window covering the first k elements.",
        "Compute the initial result from that window.",
        "Slide the window right by one position.",
        "Subtract the element that leaves the window.",
        "Add the new element that enters the window.",
        "Update the best result and repeat until the end.",
      ],
      complexity: { time: "O(n)", space: "O(1)" },
      use_cases: ["Subarray sums", "Longest substring problems", "Anomaly detection", "Streaming analytics"],
    };
  }
  if (lower.includes("dynamic programming") || lower.includes("dp") || lower.includes("knapsack")) {
    return {
      algorithm: "Dynamic Programming",
      code: `def knapsack(weights, values, capacity):\n    n = len(weights)\n    dp = [[0] * (capacity + 1) for _ in range(n + 1)]\n    for i in range(1, n + 1):\n        for w in range(capacity + 1):\n            if weights[i - 1] <= w:\n                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])\n            else:\n                dp[i][w] = dp[i - 1][w]\n    return dp[n][capacity]`,
      explanation: "Dynamic programming solves overlapping subproblems by storing intermediate results in a table. Each decision builds on previously computed solutions, turning exponential recursion into polynomial time.",
      steps: [
        "Identify the subproblem structure and overlapping states.",
        "Create a table to store results for smaller inputs.",
        "Fill the table using previously computed values.",
        "Use recurrence relation to choose between including or excluding an item.",
        "Return the best value from the final table cell.",
        "Optionally backtrack to recover the selected items.",
      ],
      complexity: { time: "O(n * capacity)", space: "O(n * capacity)" },
      use_cases: ["Optimization", "Resource allocation", "Finance", "Bioinformatics"],
    };
  }
  if (lower.includes("hashing") || lower.includes("hash map") || lower.includes("counter") || lower.includes("duplicate")) {
    return {
      algorithm: "Hash Map / Frequency Count",
      code: `def first_unique_char(s: str):\n    from collections import Counter\n    counts = Counter(s)\n    for i, ch in enumerate(s):\n        if counts[ch] == 1:\n            return i\n    return -1`,
      explanation: "Hashing stores values in a map for fast lookups. This example counts character frequencies first, then scans once more to find the first character that appears exactly once.",
      steps: [
        "Count how many times each item appears using a hash map.",
        "Scan the original sequence in order.",
        "Return the first item whose stored count equals one.",
        "If none is found, return a sentinel value like -1.",
        "Use this pattern whenever you need fast membership checks or frequency data.",
      ],
      complexity: { time: "O(n)", space: "O(n)" },
      use_cases: ["Duplicate detection", "Anagram checks", "Counting frequencies", "Caching"],
    };
  }
  return {
    algorithm: "Generic Solution",
    code: `def solution(input_data):\n    result = []\n    for item in input_data:\n        processed = item * 2\n        result.append(processed)\n    return result`,
    explanation: "This is a simple generic template that processes each item in a collection and builds a new result list. It demonstrates basic iteration, transformation, and collection patterns.",
    steps: [
      "Create an empty result container.",
      "Loop through each input item.",
      "Transform the item using the desired operation.",
      "Append the transformed value to the result list.",
      "Return the completed result after processing all items.",
    ],
    complexity: { time: "O(n)", space: "O(n)" },
    use_cases: ["Data transformation", "List processing", "Mapping operations", "Simple demos"],
  };
}

function buildReasoning(prompt: string) {
  return [
    { thought: "Understand the request", observation: "Prompt received successfully", confidence: 0.95, next_action: "retry" },
    { thought: "Generate initial code", observation: `Created solution for: ${prompt.slice(0, 60)}`, confidence: 0.88, next_action: "retry" },
    { thought: "Review output", observation: "Code is runnable and matches prompt", confidence: 0.91, next_action: "succeed" },
  ];
}

function buildErrors(attempt: number) {
  if (attempt === 1) {
    return [
      { category: "test_failure", message: "edge case empty string", file: "solution.py", line: 1, stack_trace: null, test_name: "test_empty_input" },
    ];
  }
  return [];
}

async function mockRunAgent(prompt: string): Promise<AgentRunResponse> {
  await delay(1200);
  const attempts = 1;
  const generated = generateCodeSnippet(prompt);
  const code = generated.code;
  return {
    explanation: `${generated.algorithm}: ${generated.explanation} This implementation is clean, runnable, and validated against representative test cases.`,
    code,
    reason_for_modification: `Refined the ${generated.algorithm.toLowerCase()} solution for clarity and correctness while keeping the core logic easy to follow.`,
    confidence: Number((0.82 + Math.random() * 0.16).toFixed(2)),
    next_action: "succeed",
    reasoning: [
      { thought: "Understand the request", observation: `Identified algorithm pattern: ${generated.algorithm}`, confidence: 0.95, next_action: "retry" },
      { thought: "Generate initial code", observation: `Implemented ${generated.algorithm.toLowerCase()} with comments and example usage`, confidence: 0.88, next_action: "retry" },
      { thought: "Review output", observation: "Code is runnable and matches prompt", confidence: 0.91, next_action: "succeed" },
    ],
    errors: buildErrors(attempts),
    repair: {
      reason: "No repair needed after review.",
      code_change: "",
      confidence: 0.92,
      expected_outcome: "Code executes without runtime errors.",
    },
    attempts,
    max_attempts: 5,
    status: "success",
    algorithm: generated.algorithm,
    algorithm_steps: generated.steps,
    algorithm_complexity: generated.complexity,
    algorithm_use_cases: generated.use_cases,
    algorithm_explanation: generated.explanation,
  };
}

async function mockConfidence(): Promise<ConfidenceResponse> {
  await delay(300);
  const score = Number((0.75 + Math.random() * 0.22).toFixed(2));
  return {
    score,
    grade: score > 0.9 ? "A" : score > 0.8 ? "B" : "C",
    explanation: "Confidence is based on code clarity, test coverage, and simplicity.",
  };
}

async function mockReview(): Promise<ReviewResponse> {
  await delay(350);
  const passed = Math.random() > 0.3;
  return {
    suggestions: [
      { line: 2, severity: "low", message: "Add type hints for public helpers.", suggestion: "Use `def helper(x: int) -> int:` style." },
      { line: 5, severity: "medium", message: "Consider input validation.", suggestion: "Validate `input_data` before iteration." },
    ],
    passed,
    review_time: 0.42,
  };
}

async function mockPerformance(): Promise<PerformanceResponse> {
  await delay(400);
  return {
    complexity: {
      time_complexity: pick(["O(n)", "O(n log n)", "O(1)", "O(n^2)"]),
      space_complexity: pick(["O(n)", "O(1)", "O(log n)"]),
      estimated_memory_mb: Number((12 + Math.random() * 40).toFixed(1)),
    },
    suggestions: [
      { category: "performance", severity: "medium", message: "Avoid repeated list scans.", suggestion: "Use a single-pass approach where possible.", estimated_improvement: "~20% faster" },
      { category: "readability", severity: "low", message: "Extract magic numbers.", suggestion: "Move constants to named variables.", estimated_improvement: "easier maintenance" },
    ],
    alternative_algorithms: [
      { name: "Iterative", time_complexity: "O(n)", space_complexity: "O(1)", description: "Usually faster and simpler for linear workflows." },
      { name: "Recursive", time_complexity: "O(n)", space_complexity: "O(n)", description: "Cleaner for tree-style problems, but uses call stack." },
    ],
    passed: true,
    analysis_time: 0.38,
  };
}

async function mockTests(): Promise<TestResponse> {
  await delay(500);
  const tests_passed = 5;
  const tests_failed = 0;
  const execution_time = Number((0.28 + Math.random() * 0.4).toFixed(3));
  return {
    passed: true,
    attempt: 1,
    execution_time: execution_time,
    tests_passed,
    tests_failed,
    stdout: `============================= test session starts ==============================\nplatform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0\nrootdir: C:\\Users\\ASUS\\AppData\\Local\\Temp\\tmpdxafs5o4\ncollected 5 items\n\ntest_solution.py .....                                                       [100%]\n\n============================== ${tests_passed} passed in ${execution_time}s ==============================`,
    stderr: "",
    errors: [],
    exit_code: 0,
  };
}

export function runAgent(prompt: string, options?: { signal?: AbortSignal }): Promise<AgentRunResponse> {
  return mockRunAgent(prompt);
}

export function runConfidence(code: string): Promise<ConfidenceResponse> {
  return mockConfidence();
}

export function runReview(code: string): Promise<ReviewResponse> {
  return mockReview();
}

export function runPerformance(code: string): Promise<PerformanceResponse> {
  return mockPerformance();
}

export function runTests(code: string): Promise<TestResponse> {
  return mockTests();
}
