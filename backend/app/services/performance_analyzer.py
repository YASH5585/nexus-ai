"""
Performance Analyzer for Nexus AI.

Analyzes Python code to estimate:
- Time Complexity
- Space Complexity
- Memory usage
- Possible optimizations
- Alternative algorithms

Uses AST-based static analysis for estimation.
"""

import ast
import re
import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Set, Tuple
from collections import defaultdict
import structlog

logger = structlog.get_logger(__name__)


@dataclass
class OptimizationSuggestion:
    """A single optimization suggestion."""
    category: str
    severity: str
    line_number: Optional[int]
    message: str
    suggestion: str
    estimated_improvement: str


@dataclass
class ComplexityEstimate:
    """Complexity estimation for code."""
    time_complexity: str
    space_complexity: str
    estimated_memory_mb: Optional[float] = None


@dataclass
class AlternativeAlgorithm:
    """Suggested alternative algorithm."""
    name: str
    time_complexity: str
    space_complexity: str
    description: str
    use_case: str


@dataclass
class PerformanceAnalysisReport:
    """Complete performance analysis report."""
    passed: bool
    total_suggestions: int
    complexity: ComplexityEstimate
    suggestions: List[OptimizationSuggestion]
    alternative_algorithms: List[AlternativeAlgorithm]
    summary: Dict[str, int]
    analysis_time: float


class PerformanceAnalyzer:
    """
    Static performance analyzer for Python code.
    
    Analyzes code for performance characteristics and provides
    optimization suggestions and alternative algorithm recommendations.
    """

    def __init__(self, strict: bool = False):
        """
        Initialize the performance analyzer.
        
        Args:
            strict: Enable strict mode for more thorough checks
        """
        self.strict = strict
        self.logger = logger.bind(component="PerformanceAnalyzer")
        
        # Algorithm detection patterns
        self._algorithm_patterns = {
            "linear_search": {
                "patterns": [r"for.*in.*:", r"if.*==.*:", r"if.*in.*:"],
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "description": "Linear search through a list",
                "use_case": "Small datasets or unsorted data"
            },
            "binary_search": {
                "patterns": [r"while.*<.*:", r"mid\s*=\s*\(.*\+\s*.*\)\s*/\s*2", r"//\s*2"],
                "time_complexity": "O(log n)",
                "space_complexity": "O(1)",
                "description": "Binary search on sorted data",
                "use_case": "Large sorted datasets"
            },
            "bubble_sort": {
                "patterns": [r"for.*in range.*:", r"for.*in range.*:", r"if.*>.*:", r"swap\("],
                "time_complexity": "O(n^2)",
                "space_complexity": "O(1)",
                "description": "Bubble sort algorithm",
                "use_case": "Educational purposes only"
            },
            "selection_sort": {
                "patterns": [r"min\(", r"for.*in range.*:", r"remove\("],
                "time_complexity": "O(n^2)",
                "space_complexity": "O(1)",
                "description": "Selection sort algorithm",
                "use_case": "Educational purposes only"
            },
            "insertion_sort": {
                "patterns": [r"for.*in range.*:", r"while.*>.*:", r"insert\("],
                "time_complexity": "O(n^2)",
                "space_complexity": "O(1)",
                "description": "Insertion sort algorithm",
                "use_case": "Small datasets or nearly sorted data"
            },
            "merge_sort": {
                "patterns": [r"def merge_sort", r"def merge", r"left\s*=", r"right\s*="],
                "time_complexity": "O(n log n)",
                "space_complexity": "O(n)",
                "description": "Merge sort algorithm",
                "use_case": "Large datasets, stable sort required"
            },
            "quick_sort": {
                "patterns": [r"def quick_sort", r"pivot\s*=", r"partition\("],
                "time_complexity": "O(n log n)",
                "space_complexity": "O(log n)",
                "description": "Quick sort algorithm",
                "use_case": "Large datasets, in-place sorting"
            },
            "fibonacci_recursive": {
                "patterns": [r"def fib\(", r"return fib\(", r"fib\(.*\)\s*\+\s*fib\("],
                "time_complexity": "O(2^n)",
                "space_complexity": "O(n)",
                "description": "Recursive Fibonacci without memoization",
                "use_case": "Educational purposes only"
            },
            "nested_loops": {
                "patterns": [r"for.*in.*:\s*\n\s*for.*in"],
                "time_complexity": "O(n^2)",
                "space_complexity": "O(1)",
                "description": "Nested loops",
                "use_case": "Matrix operations, pairwise comparisons"
            },
            "hash_table": {
                "patterns": [r"dict\(", r"\[\w+\]\s*=", r"\.get\("],
                "time_complexity": "O(1)",
                "space_complexity": "O(n)",
                "description": "Hash table / dictionary usage",
                "use_case": "Fast lookups, caching"
            },
            "list_comprehension": {
                "patterns": [r"\[.*for.*in.*\]"],
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "description": "List comprehension",
                "use_case": "Creating new lists from existing data"
            },
            "generator": {
                "patterns": [r"\(.*for.*in.*\)", r"yield\s+"],
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "description": "Generator expression or function",
                "use_case": "Memory-efficient iteration over large datasets"
            }
        }
        
        # Optimization patterns
        self._optimization_patterns = {
            "nested_loops": {
                "patterns": [r"for.*in.*:\s*\n\s*for.*in"],
                "severity": "high",
                "message": "Nested loops detected - potential O(n^2) complexity",
                "suggestion": "Consider using a hash table (dict) to reduce complexity to O(n)",
                "estimated_improvement": "From O(n^2) to O(n)"
            },
            "list_in_loop": {
                "patterns": [r"for.*in.*:\s*\n.*\.append\("],
                "severity": "medium",
                "message": "List append in loop detected",
                "suggestion": "Use list comprehension for better performance",
                "estimated_improvement": "10-20% faster"
            },
            "string_concatenation": {
                "patterns": [r"\+\=\s*['\"]", r"\+\s*['\"]"],
                "severity": "medium",
                "message": "String concatenation in loop detected",
                "suggestion": "Use join() or io.StringIO for string building",
                "estimated_improvement": "50-80% faster for large strings"
            },
            "repeated_calculation": {
                "patterns": [r"len\(", r"range\("],
                "severity": "low",
                "message": "Repeated function calls in loop condition",
                "suggestion": "Calculate once before the loop",
                "estimated_improvement": "10-30% faster"
            },
            "global_variables": {
                "patterns": [r"global\s+"],
                "severity": "medium",
                "message": "Global variables detected",
                "suggestion": "Pass variables as function parameters instead",
                "estimated_improvement": "Better code organization, potential performance gain"
            },
            "recursion": {
                "patterns": [r"def \w+\(.*\):\s*\n.*\w+\("],
                "severity": "medium",
                "message": "Recursive function detected",
                "suggestion": "Consider iterative solution or memoization to avoid stack overflow",
                "estimated_improvement": "Prevents stack overflow, potential speed improvement"
            },
            "multiple_passes": {
                "patterns": [r"for.*in.*:", r"for.*in.*:", r"for.*in.*:"],
                "severity": "medium",
                "message": "Multiple passes over data detected",
                "suggestion": "Combine operations into a single pass",
                "estimated_improvement": "Reduces constant factor"
            },
            "inefficient_data_structure": {
                "patterns": [r"if.*not in.*:", r"if.*in.*:"],
                "severity": "high",
                "message": "List membership check (O(n)) instead of set/dict (O(1))",
                "suggestion": "Use set() or dict() for membership checks",
                "estimated_improvement": "From O(n) to O(1)"
            },
            "file_operations": {
                "patterns": [r"open\(", r"\.read\(", r"\.write\("],
                "severity": "low",
                "message": "File I/O operations detected",
                "suggestion": "Use buffered I/O or async I/O for better performance",
                "estimated_improvement": "10-50% faster I/O"
            }
        }

    def analyze(self, code: str, input_size: int = 1000) -> PerformanceAnalysisReport:
        """
        Analyze Python code for performance characteristics.
        
        Args:
            code: Python source code to analyze
            input_size: Expected input size for estimation
            
        Returns:
            PerformanceAnalysisReport with all findings
        """
        start_time = time.perf_counter()
        suggestions: List[OptimizationSuggestion] = []
        alternative_algorithms: List[AlternativeAlgorithm] = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            self.logger.warning("Code has syntax errors, skipping AST analysis", error=str(e))
            return PerformanceAnalysisReport(
                passed=False,
                total_suggestions=1,
                complexity=ComplexityEstimate(
                    time_complexity="N/A",
                    space_complexity="N/A"
                ),
                suggestions=[
                    OptimizationSuggestion(
                        category="syntax_error",
                        severity="critical",
                        line_number=e.lineno,
                        message=f"Syntax error: {e.msg}",
                        suggestion="Fix the syntax error before performance analysis",
                        estimated_improvement="N/A"
                    )
                ],
                alternative_algorithms=[],
                summary={"syntax_error": 1},
                analysis_time=time.perf_counter() - start_time
            )
        
        # Detect algorithms
        detected_algorithms = self._detect_algorithms(tree, code)
        
        # Estimate complexity
        complexity = self._estimate_complexity(tree, code, detected_algorithms, input_size)
        
        # Generate alternative algorithm suggestions
        alternative_algorithms = self._suggest_alternative_algorithms(detected_algorithms, complexity)
        
        # Run all optimization checks
        suggestions.extend(self._check_optimizations(tree, code))
        suggestions.extend(self._check_algorithm_efficiency(tree, code, detected_algorithms))
        suggestions.extend(self._check_memory_usage(tree, code))
        suggestions.extend(self._check_loop_efficiency(tree, code))
        
        # Build summary
        summary: Dict[str, int] = defaultdict(int)
        for suggestion in suggestions:
            summary[suggestion.category] += 1
        
        analysis_time = time.perf_counter() - start_time
        
        self.logger.info(
            "Performance analysis completed",
            time_complexity=complexity.time_complexity,
            space_complexity=complexity.space_complexity,
            total_suggestions=len(suggestions),
            analysis_time=round(analysis_time, 3)
        )
        
        return PerformanceAnalysisReport(
            passed=len(suggestions) == 0 and complexity.time_complexity not in ["O(n^2)", "O(n^3)", "O(2^n)"],
            total_suggestions=len(suggestions),
            complexity=complexity,
            suggestions=suggestions,
            alternative_algorithms=alternative_algorithms,
            summary=dict(summary),
            analysis_time=round(analysis_time, 3)
        )

    def _detect_algorithms(self, tree: ast.AST, code: str) -> Dict[str, Dict[str, Any]]:
        """Detect algorithms used in the code."""
        detected = {}
        
        for algo_name, algo_info in self._algorithm_patterns.items():
            for pattern in algo_info["patterns"]:
                if re.search(pattern, code, re.MULTILINE | re.DOTALL):
                    detected[algo_name] = algo_info
                    break
        
        return detected

    def _estimate_complexity(
        self,
        tree: ast.AST,
        code: str,
        detected_algorithms: Dict[str, Dict[str, Any]],
        input_size: int
    ) -> ComplexityEstimate:
        """Estimate time and space complexity."""
        # Default complexity
        time_complexity = "O(n)"
        space_complexity = "O(1)"
        estimated_memory_mb = None
        
        # Check for nested loops (O(n^2) or worse)
        nested_loops = len(re.findall(r"for.*in.*:\s*\n\s*for.*in", code, re.MULTILINE))
        if nested_loops >= 2:
            time_complexity = f"O(n^{nested_loops})"
        elif nested_loops == 1:
            time_complexity = "O(n^2)"
        
        # Check for recursion without memoization
        if "fibonacci_recursive" in detected_algorithms:
            time_complexity = "O(2^n)"
            space_complexity = "O(n)"
        
        # Check for sorting algorithms
        if "bubble_sort" in detected_algorithms or "selection_sort" in detected_algorithms:
            time_complexity = "O(n^2)"
        elif "merge_sort" in detected_algorithms or "quick_sort" in detected_algorithms:
            time_complexity = "O(n log n)"
        
        # Check for binary search
        if "binary_search" in detected_algorithms:
            time_complexity = "O(log n)"
        
        # Estimate space complexity
        if "merge_sort" in detected_algorithms:
            space_complexity = "O(n)"
        elif "hash_table" in detected_algorithms:
            space_complexity = "O(n)"
        elif "list_comprehension" in detected_algorithms:
            space_complexity = "O(n)"
        
        # Estimate memory usage
        estimated_memory_mb = self._estimate_memory_usage(tree, code, input_size)
        
        return ComplexityEstimate(
            time_complexity=time_complexity,
            space_complexity=space_complexity,
            estimated_memory_mb=estimated_memory_mb
        )

    def _estimate_memory_usage(self, tree: ast.AST, code: str, input_size: int) -> float:
        """Estimate memory usage in MB."""
        # Simple heuristic-based estimation
        base_memory = 0.1  # Base overhead in MB
        
        # Count data structures
        lists = len(re.findall(r"\[\s*\]|list\(", code))
        dicts = len(re.findall(r"\{\s*\}|dict\(", code))
        strings = len(re.findall(r"['\"].*?['\"]", code))
        
        # Estimate memory per element
        list_memory = lists * input_size * 8 / (1024 * 1024)  # 8 bytes per element
        dict_memory = dicts * input_size * 50 / (1024 * 1024)  # ~50 bytes per entry
        string_memory = strings * 100 / (1024 * 1024)  # ~100 bytes per string
        
        total_memory = base_memory + list_memory + dict_memory + string_memory
        return round(total_memory, 2)

    def _suggest_alternative_algorithms(
        self,
        detected_algorithms: Dict[str, Dict[str, Any]],
        complexity: ComplexityEstimate
    ) -> List[AlternativeAlgorithm]:
        """Suggest alternative algorithms based on detected patterns."""
        alternatives = []
        
        # If nested loops detected, suggest hash table
        if "nested_loops" in detected_algorithms or "O(n^2)" in complexity.time_complexity:
            alternatives.append(AlternativeAlgorithm(
                name="Hash Table / Dictionary",
                time_complexity="O(n)",
                space_complexity="O(n)",
                description="Use a dictionary to store and lookup values in constant time",
                use_case="When you need to check membership or count occurrences"
            ))
        
        # If linear search detected, suggest binary search
        if "linear_search" in detected_algorithms:
            alternatives.append(AlternativeAlgorithm(
                name="Binary Search",
                time_complexity="O(log n)",
                space_complexity="O(1)",
                description="Use binary search on sorted data for faster lookups",
                use_case="When data is sorted and you need to search frequently"
            ))
        
        # If bubble sort detected, suggest better sort
        if "bubble_sort" in detected_algorithms or "selection_sort" in detected_algorithms or "insertion_sort" in detected_algorithms:
            alternatives.append(AlternativeAlgorithm(
                name="Timsort (Python's built-in sort)",
                time_complexity="O(n log n)",
                space_complexity="O(n)",
                description="Use Python's built-in sorted() or list.sort() which uses Timsort",
                use_case="General purpose sorting"
            ))
        
        # If recursive fibonacci detected, suggest memoization
        if "fibonacci_recursive" in detected_algorithms:
            alternatives.append(AlternativeAlgorithm(
                name="Memoized Fibonacci / Iterative",
                time_complexity="O(n)",
                space_complexity="O(n) or O(1)",
                description="Use memoization or iterative approach to avoid exponential time",
                use_case="Calculating Fibonacci numbers"
            ))
        
        # If list comprehension detected, suggest generator
        if "list_comprehension" in detected_algorithms:
            alternatives.append(AlternativeAlgorithm(
                name="Generator Expression",
                time_complexity="O(n)",
                space_complexity="O(1)",
                description="Use generator expression () instead of list comprehension [] for memory efficiency",
                use_case="When you only need to iterate once"
            ))
        
        return alternatives

    def _check_optimizations(self, tree: ast.AST, code: str) -> List[OptimizationSuggestion]:
        """Check for optimization opportunities."""
        suggestions = []
        
        for opt_name, opt_info in self._optimization_patterns.items():
            for pattern in opt_info["patterns"]:
                matches = list(re.finditer(pattern, code, re.MULTILINE | re.DOTALL))
                if matches:
                    for match in matches:
                        line_num = code[:match.start()].count('\n') + 1
                        suggestions.append(OptimizationSuggestion(
                            category=opt_name,
                            severity=opt_info["severity"],
                            line_number=line_num,
                            message=opt_info["message"],
                            suggestion=opt_info["suggestion"],
                            estimated_improvement=opt_info["estimated_improvement"]
                        ))
        
        return suggestions

    def _check_algorithm_efficiency(
        self,
        tree: ast.AST,
        code: str,
        detected_algorithms: Dict[str, Dict[str, Any]]
    ) -> List[OptimizationSuggestion]:
        """Check algorithm efficiency."""
        suggestions = []
        
        for algo_name, algo_info in detected_algorithms.items():
            if algo_info["time_complexity"] in ["O(n^2)", "O(n^3)", "O(2^n)"]:
                line = self._find_first_match(code, algo_info["patterns"][0])
                suggestions.append(OptimizationSuggestion(
                    category="algorithm_efficiency",
                    severity="high",
                    line_number=line,
                    message=f"Algorithm '{algo_name}' has {algo_info['time_complexity']} time complexity",
                    suggestion=f"Consider using a more efficient algorithm. {algo_info['description']}",
                    estimated_improvement=f"Could reduce from {algo_info['time_complexity']} to O(n log n) or better"
                ))
        
        return suggestions

    def _check_memory_usage(self, tree: ast.AST, code: str) -> List[OptimizationSuggestion]:
        """Check for memory usage issues."""
        suggestions = []
        
        # Check for large list comprehensions
        list_comp_matches = list(re.finditer(r"\[.*for.*in.*if.*\]", code, re.MULTILINE | re.DOTALL))
        if list_comp_matches:
            for match in list_comp_matches:
                line_num = code[:match.start()].count('\n') + 1
                suggestions.append(OptimizationSuggestion(
                    category="memory_usage",
                    severity="medium",
                    line_number=line_num,
                    message="List comprehension with filter creates intermediate list",
                    suggestion="Use generator expression () instead of list comprehension [] to save memory",
                    estimated_improvement="Reduces memory usage by 50-90%"
                ))
        
        # Check for unnecessary list copies
        copy_matches = list(re.finditer(r"\.copy\(\)|list\(|\[.*\]", code))
        if len(copy_matches) > 3:
            suggestions.append(OptimizationSuggestion(
                category="memory_usage",
                severity="low",
                line_number=None,
                message="Multiple list copies detected",
                suggestion="Consider using views or iterators instead of copying data",
                estimated_improvement="Reduces memory allocations"
            ))
        
        return suggestions

    def _check_loop_efficiency(self, tree: ast.AST, code: str) -> List[OptimizationSuggestion]:
        """Check loop efficiency."""
        suggestions = []
        
        # Check for loops with repeated calculations
        loop_pattern = r"for\s+\w+\s+in\s+.*:\s*\n(.*?\n)*?\s*(if|print|return|yield)"
        loop_matches = list(re.finditer(loop_pattern, code, re.MULTILINE | re.DOTALL))
        
        for match in loop_matches:
            loop_body = match.group(0)
            if re.search(r"len\(", loop_body) or re.search(r"range\(", loop_body):
                line_num = code[:match.start()].count('\n') + 1
                suggestions.append(OptimizationSuggestion(
                    category="loop_efficiency",
                    severity="low",
                    line_number=line_num,
                    message="Function calls in loop condition may be evaluated repeatedly",
                    suggestion="Calculate the value once before the loop",
                    estimated_improvement="10-30% faster loop execution"
                ))
        
        return suggestions

    def _find_first_match(self, code: str, pattern: str) -> Optional[int]:
        """Find the line number of the first match for a pattern."""
        match = re.search(pattern, code, re.MULTILINE | re.DOTALL)
        if match:
            return code[:match.start()].count('\n') + 1
        return None

    def to_dict(self, report: PerformanceAnalysisReport) -> Dict[str, Any]:
        """
        Convert PerformanceAnalysisReport to dictionary for JSON serialization.
        
        Args:
            report: PerformanceAnalysisReport instance
            
        Returns:
            Dictionary representation
        """
        return {
            "passed": report.passed,
            "total_suggestions": report.total_suggestions,
            "complexity": {
                "time_complexity": report.complexity.time_complexity,
                "space_complexity": report.complexity.space_complexity,
                "estimated_memory_mb": report.complexity.estimated_memory_mb
            },
            "suggestions": [
                {
                    "category": s.category,
                    "severity": s.severity,
                    "line_number": s.line_number,
                    "message": s.message,
                    "suggestion": s.suggestion,
                    "estimated_improvement": s.estimated_improvement
                }
                for s in report.suggestions
            ],
            "alternative_algorithms": [
                {
                    "name": a.name,
                    "time_complexity": a.time_complexity,
                    "space_complexity": a.space_complexity,
                    "description": a.description,
                    "use_case": a.use_case
                }
                for a in report.alternative_algorithms
            ],
            "summary": report.summary,
            "analysis_time": report.analysis_time
        }
