"""
AI Code Reviewer for Nexus AI.

Performs static analysis on generated code to detect:
- Unused variables
- Duplicate code blocks
- Magic numbers
- Poor naming conventions
- Missing comments and docstrings
- Missing type hints

Uses Python's AST module for accurate analysis.
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
class ReviewSuggestion:
    """A single code review suggestion."""
    category: str
    severity: str
    line_number: Optional[int]
    message: str
    suggestion: str


@dataclass
class CodeReviewReport:
    """Complete code review report."""
    passed: bool
    total_issues: int
    suggestions: List[ReviewSuggestion]
    summary: Dict[str, int]
    review_time: float


class CodeReviewer:
    """
    Static code analyzer for Python code.
    
    Analyzes code for common issues and provides actionable suggestions.
    Uses AST-based analysis for accurate detection.
    """

    def __init__(self, strict: bool = False):
        """
        Initialize the code reviewer.
        
        Args:
            strict: Enable strict mode for more thorough checks
        """
        self.strict = strict
        self.logger = logger.bind(component="CodeReviewer")
        
        # Naming convention patterns
        self._snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')
        self._camel_case_pattern = re.compile(r'^[a-z][a-zA-Z0-9]*$')
        self._pascal_case_pattern = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
        
        # Common magic number patterns (exclude 0, 1, -1, 2, 100)
        self._magic_number_pattern = re.compile(r'\b(?![01]|100|-?1|-?2)\d+\b')

    def review(self, code: str) -> CodeReviewReport:
        """
        Review Python code and return a report.
        
        Args:
            code: Python source code to review
            
        Returns:
            CodeReviewReport with all findings
        """
        start_time = time.perf_counter()
        suggestions: List[ReviewSuggestion] = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            self.logger.warning("Code has syntax errors, skipping AST analysis", error=str(e))
            return CodeReviewReport(
                passed=False,
                total_issues=1,
                suggestions=[
                    ReviewSuggestion(
                        category="syntax_error",
                        severity="critical",
                        line_number=e.lineno,
                        message=f"Syntax error: {e.msg}",
                        suggestion="Fix the syntax error before reviewing"
                    )
                ],
                summary={"syntax_error": 1},
                review_time=time.perf_counter() - start_time
            )
        
        # Run all checks
        suggestions.extend(self._check_unused_variables(tree, code))
        suggestions.extend(self._check_duplicate_code(tree))
        suggestions.extend(self._check_magic_numbers(tree, code))
        suggestions.extend(self._check_poor_naming(tree))
        suggestions.extend(self._check_missing_comments(tree, code))
        suggestions.extend(self._check_missing_type_hints(tree))
        
        # Build summary
        summary: Dict[str, int] = defaultdict(int)
        for suggestion in suggestions:
            summary[suggestion.category] += 1
        
        review_time = time.perf_counter() - start_time
        
        self.logger.info(
            "Code review completed",
            total_issues=len(suggestions),
            categories=dict(summary),
            review_time=round(review_time, 3)
        )
        
        return CodeReviewReport(
            passed=len(suggestions) == 0,
            total_issues=len(suggestions),
            suggestions=suggestions,
            summary=dict(summary),
            review_time=round(review_time, 3)
        )

    def _check_unused_variables(self, tree: ast.AST, code: str) -> List[ReviewSuggestion]:
        """Detect unused variables in the code."""
        suggestions = []
        assigned_names: Set[str] = set()
        used_names: Set[str] = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned_names.add(target.id)
            elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name):
                assigned_names.add(node.target.id)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Load):
                    used_names.add(node.id)
        
        unused = assigned_names - used_names
        for name in unused:
            if name.startswith('_'):
                continue
            line = self._find_line(code, name)
            suggestions.append(ReviewSuggestion(
                category="unused_variable",
                severity="medium",
                line_number=line,
                message=f"Variable '{name}' is assigned but never used",
                suggestion=f"Remove the unused variable '{name}' or use it in the code"
            ))
        
        return suggestions

    def _check_duplicate_code(self, tree: ast.AST) -> List[ReviewSuggestion]:
        """Detect duplicate code blocks."""
        suggestions = []
        function_bodies = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                body_source = ast.unparse(node.body)
                function_bodies.append((node.name, body_source, node.lineno))
        
        seen_bodies = {}
        for name, body, lineno in function_bodies:
            if body in seen_bodies:
                suggestions.append(ReviewSuggestion(
                    category="duplicate_code",
                    severity="high",
                    line_number=lineno,
                    message=f"Function '{name}' has duplicate code similar to '{seen_bodies[body][0]}'",
                    suggestion=f"Extract the common logic into a shared helper function"
                ))
            else:
                seen_bodies[body] = (name, lineno)
        
        return suggestions

    def _check_magic_numbers(self, tree: ast.AST, code: str) -> List[ReviewSuggestion]:
        """Detect magic numbers in the code."""
        suggestions = []
        allowed_numbers = {0, 1, -1, 2, 100, 0.0, 1.0, -1.0, 2.0, 100.0}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                if node.value not in allowed_numbers:
                    line = getattr(node, 'lineno', None)
                    suggestions.append(ReviewSuggestion(
                        category="magic_number",
                        severity="medium",
                        line_number=line,
                        message=f"Magic number {node.value} found",
                        suggestion=f"Define {node.value} as a named constant with a descriptive name"
                    ))
        
        return suggestions

    def _check_poor_naming(self, tree: ast.AST) -> List[ReviewSuggestion]:
        """Check for poor naming conventions."""
        suggestions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('_') and not node.name.startswith('__'):
                    continue
                if not self._camel_case_pattern.match(node.name) and not self._snake_case_pattern.match(node.name):
                    suggestions.append(ReviewSuggestion(
                        category="poor_naming",
                        severity="low",
                        line_number=node.lineno,
                        message=f"Function name '{node.name}' does not follow naming conventions",
                        suggestion="Use snake_case for function names"
                    ))
                
                if len(node.name) <= 2 and not node.name.startswith('_'):
                    suggestions.append(ReviewSuggestion(
                        category="poor_naming",
                        severity="medium",
                        line_number=node.lineno,
                        message=f"Function name '{node.name}' is too short to be descriptive",
                        suggestion="Use a more descriptive function name"
                    ))
            
            elif isinstance(node, ast.ClassDef):
                if not self._pascal_case_pattern.match(node.name):
                    suggestions.append(ReviewSuggestion(
                        category="poor_naming",
                        severity="low",
                        line_number=node.lineno,
                        message=f"Class name '{node.name}' should use PascalCase",
                        suggestion="Rename class to use PascalCase"
                    ))
        
        return suggestions

    def _check_missing_comments(self, tree: ast.AST, code: str) -> List[ReviewSuggestion]:
        """Check for missing comments and docstrings."""
        suggestions = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    suggestions.append(ReviewSuggestion(
                        category="missing_comments",
                        severity="low" if isinstance(node, ast.ClassDef) else "medium",
                        line_number=node.lineno,
                        message=f"{'Class' if isinstance(node, ast.ClassDef) else 'Function'} '{node.name}' is missing a docstring",
                        suggestion="Add a docstring explaining the purpose, parameters, and return value"
                    ))
        
        return suggestions

    def _check_missing_type_hints(self, tree: ast.AST) -> List[ReviewSuggestion]:
        """Check for missing type hints."""
        suggestions = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.returns is None:
                    suggestions.append(ReviewSuggestion(
                        category="missing_type_hints",
                        severity="medium",
                        line_number=node.lineno,
                        message=f"Function '{node.name}' is missing a return type annotation",
                        suggestion="Add a return type annotation (e.g., -> int, -> str, -> None)"
                    ))
                
                missing_arg_types = []
                for arg in node.args.args:
                    if arg.arg != 'self' and not arg.annotation:
                        missing_arg_types.append(arg.arg)
                
                if missing_arg_types and len(missing_arg_types) > 0:
                    if len(missing_arg_types) <= 3:
                        suggestions.append(ReviewSuggestion(
                            category="missing_type_hints",
                            severity="medium",
                            line_number=node.lineno,
                            message=f"Function '{node.name}' has arguments missing type annotations: {', '.join(missing_arg_types)}",
                            suggestion="Add type annotations for function arguments"
                        ))
        
        return suggestions

    def _find_line(self, code: str, identifier: str) -> Optional[int]:
        """Find the line number of an identifier in the source code."""
        lines = code.splitlines()
        for i, line in enumerate(lines, start=1):
            if identifier in line:
                return i
        return None

    def to_dict(self, report: CodeReviewReport) -> Dict[str, Any]:
        """
        Convert CodeReviewReport to dictionary for JSON serialization.
        
        Args:
            report: CodeReviewReport instance
            
        Returns:
            Dictionary representation
        """
        return {
            "passed": report.passed,
            "total_issues": report.total_issues,
            "suggestions": [
                {
                    "category": s.category,
                    "severity": s.severity,
                    "line_number": s.line_number,
                    "message": s.message,
                    "suggestion": s.suggestion
                }
                for s in report.suggestions
            ],
            "summary": report.summary,
            "review_time": report.review_time
        }
