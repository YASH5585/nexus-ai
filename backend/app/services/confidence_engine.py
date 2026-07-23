"""
Confidence Engine for Nexus AI.

Calculates confidence scores for generated code based on:
- Test results
- Security scan
- Performance analysis
- Repair attempts
- Documentation
- Code complexity

Returns a score (0-100), letter grade, production readiness, and explanation.
"""

import ast
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import structlog

logger = structlog.get_logger(__name__)


@dataclass
class ConfidenceBreakdown:
    """Detailed breakdown of confidence calculation."""
    test_score: float = 0.0
    security_score: float = 0.0
    performance_score: float = 0.0
    repair_score: float = 0.0
    documentation_score: float = 0.0
    complexity_score: float = 0.0
    weights: Dict[str, float] = field(default_factory=dict)


class ConfidenceEngine:
    """
    Calculates confidence scores for generated code.
    
    Uses weighted scoring across multiple dimensions to provide
    a comprehensive confidence assessment.
    """

    def __init__(self):
        """Initialize the confidence engine with default weights."""
        self.logger = logger.bind(component="ConfidenceEngine")
        
        # Default weights for each factor
        self._weights = {
            "test": 0.30,
            "security": 0.20,
            "performance": 0.15,
            "repair": 0.10,
            "documentation": 0.10,
            "complexity": 0.15
        }
        
        # Grade thresholds
        self._grade_thresholds = {
            "A": (90, 100),
            "B": (80, 89),
            "C": (70, 79),
            "D": (60, 69),
            "F": (0, 59)
        }
        
        # Production ready threshold
        self._production_ready_threshold = 80.0

    def calculate(
        self,
        code: str,
        test_results: Optional[Any] = None,
        security_scan: Optional[Any] = None,
        performance_analysis: Optional[Any] = None,
        code_review: Optional[Any] = None,
        repair_attempts: int = 0,
        max_attempts: int = 5,
        has_documentation: bool = False,
        complexity_score: Optional[float] = None,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Calculate confidence score for generated code.
        
        Args:
            code: Python source code
            test_results: Test results (optional)
            security_scan: Security scan results (optional)
            performance_analysis: Performance analysis results (optional)
            code_review: Code review results (optional)
            repair_attempts: Number of repair attempts needed
            max_attempts: Maximum allowed repair attempts
            has_documentation: Whether code has documentation
            complexity_score: Optional complexity score (0-1, lower is better)
            language: Programming language
            
        Returns:
            Dictionary with confidence score, grade, and explanation
        """
        start_time = time.perf_counter()
        
        breakdown = ConfidenceBreakdown(weights=self._weights.copy())
        
        # Calculate individual scores
        breakdown.test_score = self._calculate_test_score(test_results)
        breakdown.security_score = self._calculate_security_score(security_scan)
        breakdown.performance_score = self._calculate_performance_score(performance_analysis, code_review)
        breakdown.repair_score = self._calculate_repair_score(repair_attempts, max_attempts)
        breakdown.documentation_score = self._calculate_documentation_score(code, has_documentation)
        breakdown.complexity_score = self._calculate_complexity_score(code, complexity_score)
        
        # Calculate weighted total
        total_score = (
            breakdown.test_score * self._weights["test"] +
            breakdown.security_score * self._weights["security"] +
            breakdown.performance_score * self._weights["performance"] +
            breakdown.repair_score * self._weights["repair"] +
            breakdown.documentation_score * self._weights["documentation"] +
            breakdown.complexity_score * self._weights["complexity"]
        )
        
        # Ensure score is within bounds
        total_score = max(0.0, min(100.0, total_score))
        
        # Determine letter grade
        letter_grade = self._get_letter_grade(total_score)
        
        # Determine production readiness
        production_ready = self._is_production_ready(
            total_score, breakdown, security_scan, test_results
        )
        
        # Generate explanation
        explanation = self._generate_explanation(breakdown, total_score, letter_grade, production_ready)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(breakdown, security_scan, test_results)
        
        self.logger.info(
            "Confidence calculated",
            score=round(total_score, 1),
            grade=letter_grade,
            production_ready=production_ready,
            calculation_time=round(time.perf_counter() - start_time, 3)
        )
        
        return {
            "score": round(total_score, 1),
            "letter_grade": letter_grade,
            "production_ready": production_ready,
            "explanation": explanation,
            "breakdown": {
                "test_score": round(breakdown.test_score, 1),
                "security_score": round(breakdown.security_score, 1),
                "performance_score": round(breakdown.performance_score, 1),
                "repair_score": round(breakdown.repair_score, 1),
                "documentation_score": round(breakdown.documentation_score, 1),
                "complexity_score": round(breakdown.complexity_score, 1),
                "weights": self._weights
            },
            "recommendations": recommendations
        }

    def _calculate_test_score(self, test_results: Optional[Any]) -> float:
        """Calculate test score (0-100)."""
        if test_results is None:
            return 50.0  # Neutral score if no tests run
        
        score = 0.0
        
        # Base score on pass/fail
        if test_results.passed:
            score = 100.0
        else:
            # Partial credit based on pass rate
            total_tests = test_results.tests_passed + test_results.tests_failed
            if total_tests > 0:
                pass_rate = test_results.tests_passed / total_tests
                score = pass_rate * 80.0  # Max 80 if some tests failed
            else:
                score = 20.0  # No tests run
        
        # Penalty for execution errors
        if hasattr(test_results, 'errors') and test_results.errors:
            score -= min(20.0, len(test_results.errors) * 5.0)
        
        return max(0.0, min(100.0, score))

    def _calculate_security_score(self, security_scan: Optional[Any]) -> float:
        """Calculate security score (0-100)."""
        if security_scan is None:
            return 70.0  # Neutral-positive if no scan run
        
        score = 100.0
        
        # Deduct for issues by severity
        if hasattr(security_scan, 'critical_issues'):
            score -= security_scan.critical_issues * 30.0
        if hasattr(security_scan, 'high_issues'):
            score -= security_scan.high_issues * 20.0
        if hasattr(security_scan, 'medium_issues'):
            score -= security_scan.medium_issues * 10.0
        if hasattr(security_scan, 'low_issues'):
            score -= security_scan.low_issues * 5.0
        
        # If scan has total_issues but not breakdown, use total
        if security_scan.total_issues > 0 and not hasattr(security_scan, 'critical_issues'):
            score -= security_scan.total_issues * 10.0
        
        return max(0.0, min(100.0, score))

    def _calculate_performance_score(self, performance_analysis: Optional[Any], code_review: Optional[Any]) -> float:
        """Calculate performance score (0-100)."""
        if performance_analysis is None and code_review is None:
            return 70.0  # Neutral if no analysis run
        
        score = 100.0
        
        # Deduct for performance issues
        if performance_analysis:
            if hasattr(performance_analysis, 'high_suggestions'):
                score -= performance_analysis.high_suggestions * 15.0
            if hasattr(performance_analysis, 'medium_suggestions'):
                score -= performance_analysis.medium_suggestions * 8.0
            if hasattr(performance_analysis, 'low_suggestions'):
                score -= performance_analysis.low_suggestions * 3.0
            
            # Deduct for poor complexity
            if hasattr(performance_analysis, 'time_complexity'):
                complexity = performance_analysis.time_complexity
                if "n^3" in complexity or "2^n" in complexity:
                    score -= 20.0
                elif "n^2" in complexity:
                    score -= 10.0
        
        # Deduct for code review issues
        if code_review:
            if hasattr(code_review, 'high_issues'):
                score -= code_review.high_issues * 10.0
            if hasattr(code_review, 'medium_issues'):
                score -= code_review.medium_issues * 5.0
            if hasattr(code_review, 'low_issues'):
                score -= code_review.low_issues * 2.0
        
        return max(0.0, min(100.0, score))

    def _calculate_repair_score(self, repair_attempts: int, max_attempts: int) -> float:
        """Calculate repair score (0-100)."""
        if max_attempts <= 0:
            return 100.0
        
        # Score based on repair efficiency
        # 0 attempts = 100, max attempts = 0
        repair_ratio = repair_attempts / max_attempts
        
        # Exponential decay for repair attempts
        score = 100.0 * (1.0 - repair_ratio) ** 2
        
        return max(0.0, min(100.0, score))

    def _calculate_documentation_score(self, code: str, has_documentation: bool) -> float:
        """Calculate documentation score (0-100)."""
        if not code or not code.strip():
            return 0.0
        
        score = 0.0
        
        # Check for docstrings
        try:
            tree = ast.parse(code)
            docstring_count = 0
            total_functions = 0
            total_classes = 0
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    total_functions += 1
                    if ast.get_docstring(node):
                        docstring_count += 1
                elif isinstance(node, ast.ClassDef):
                    total_classes += 1
                    if ast.get_docstring(node):
                        docstring_count += 1
            
            # Calculate documentation coverage
            total_defs = total_functions + total_classes
            if total_defs > 0:
                coverage = docstring_count / total_defs
                score = coverage * 100.0
            else:
                # No functions/classes, check for module docstring
                if ast.get_docstring(tree):
                    score = 50.0
                else:
                    score = 0.0
        except SyntaxError:
            score = 0.0
        
        # If explicitly marked as having documentation, ensure minimum score
        if has_documentation and score < 30.0:
            score = max(score, 30.0)
        
        return max(0.0, min(100.0, score))

    def _calculate_complexity_score(self, code: str, complexity_score: Optional[float]) -> float:
        """Calculate complexity score (0-100)."""
        if complexity_score is not None:
            # Use provided complexity score (0-1, lower is better)
            return (1.0 - complexity_score) * 100.0
        
        if not code or not code.strip():
            return 50.0
        
        try:
            tree = ast.parse(code)
            
            # Calculate cyclomatic complexity
            complexity = 1  # Base complexity
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                    complexity += 1
                elif isinstance(node, ast.ExceptHandler):
                    complexity += 1
                elif isinstance(node, (ast.BoolOp,)):
                    complexity += len(node.values) - 1
            
            # Normalize complexity to 0-100 score
            # Assume complexity > 20 is very complex
            if complexity <= 5:
                score = 100.0
            elif complexity <= 10:
                score = 80.0
            elif complexity <= 15:
                score = 60.0
            elif complexity <= 20:
                score = 40.0
            else:
                score = max(0.0, 40.0 - (complexity - 20) * 2.0)
            
            return score
            
        except SyntaxError:
            return 20.0  # Syntax errors indicate high complexity

    def _get_letter_grade(self, score: float) -> str:
        """Get letter grade from score."""
        for grade, (min_score, max_score) in self._grade_thresholds.items():
            if min_score <= score <= max_score:
                return grade
        return "F"

    def _is_production_ready(
        self,
        score: float,
        breakdown: ConfidenceBreakdown,
        security_scan: Optional[Any],
        test_results: Optional[Any]
    ) -> bool:
        """Determine if code is production ready."""
        # Must meet minimum score threshold
        if score < self._production_ready_threshold:
            return False
        
        # Must have passing tests
        if test_results is not None and not test_results.passed:
            return False
        
        # Must not have critical security issues
        if security_scan is not None:
            if hasattr(security_scan, 'critical_issues') and security_scan.critical_issues > 0:
                return False
            if hasattr(security_scan, 'total_issues') and security_scan.total_issues > 0:
                if not hasattr(security_scan, 'critical_issues'):
                    return False
        
        return True

    def _generate_explanation(
        self,
        breakdown: ConfidenceBreakdown,
        score: float,
        letter_grade: str,
        production_ready: bool
    ) -> str:
        """Generate human-readable confidence explanation."""
        parts = []
        
        # Overall assessment
        if production_ready:
            parts.append(f"Code is production-ready with a confidence score of {score:.1f}/100 (Grade: {letter_grade}).")
        else:
            parts.append(f"Code has a confidence score of {score:.1f}/100 (Grade: {letter_grade}) and is NOT production-ready.")
        
        # Test assessment
        if breakdown.test_score >= 90:
            parts.append("Tests are passing successfully.")
        elif breakdown.test_score >= 70:
            parts.append("Most tests are passing, but some failures remain.")
        elif breakdown.test_score >= 50:
            parts.append("Tests show significant issues that need attention.")
        else:
            parts.append("Tests are failing or not running. This is a critical issue.")
        
        # Security assessment
        if breakdown.security_score >= 90:
            parts.append("No significant security vulnerabilities detected.")
        elif breakdown.security_score >= 70:
            parts.append("Minor security issues found that should be addressed.")
        elif breakdown.security_score >= 50:
            parts.append("Security vulnerabilities detected that need immediate attention.")
        else:
            parts.append("Critical security vulnerabilities found. Code should not be deployed.")
        
        # Performance assessment
        if breakdown.performance_score >= 90:
            parts.append("Performance looks good.")
        elif breakdown.performance_score >= 70:
            parts.append("Performance is acceptable but could be optimized.")
        else:
            parts.append("Performance issues detected that may affect user experience.")
        
        # Repair assessment
        if breakdown.repair_score >= 90:
            parts.append("Code required minimal or no repairs.")
        elif breakdown.repair_score >= 70:
            parts.append("Code required some repairs but was relatively stable.")
        elif breakdown.repair_score >= 50:
            parts.append("Code required multiple repairs, indicating some instability.")
        else:
            parts.append("Code required extensive repairs, indicating significant instability.")
        
        # Documentation assessment
        if breakdown.documentation_score >= 80:
            parts.append("Documentation is comprehensive.")
        elif breakdown.documentation_score >= 50:
            parts.append("Documentation is partial.")
        else:
            parts.append("Documentation is missing or insufficient.")
        
        # Complexity assessment
        if breakdown.complexity_score >= 80:
            parts.append("Code complexity is well-managed.")
        elif breakdown.complexity_score >= 50:
            parts.append("Code complexity is moderate.")
        else:
            parts.append("Code complexity is high and may be difficult to maintain.")
        
        return " ".join(parts)

    def _generate_recommendations(
        self,
        breakdown: ConfidenceBreakdown,
        security_scan: Optional[Any],
        test_results: Optional[Any]
    ) -> List[str]:
        """Generate actionable recommendations for improving confidence."""
        recommendations = []
        
        # Test recommendations
        if breakdown.test_score < 80:
            recommendations.append("Improve test coverage and fix failing tests to increase confidence.")
        if test_results is None:
            recommendations.append("Run tests to validate code correctness.")
        
        # Security recommendations
        if breakdown.security_score < 90:
            recommendations.append("Address security vulnerabilities before deployment.")
        if security_scan and hasattr(security_scan, 'critical_issues') and security_scan.critical_issues > 0:
            recommendations.append("Fix all critical security issues immediately.")
        
        # Performance recommendations
        if breakdown.performance_score < 80:
            recommendations.append("Optimize performance bottlenecks identified in analysis.")
        
        # Repair recommendations
        if breakdown.repair_score < 60:
            recommendations.append("Code required extensive repairs - consider reviewing the generation logic.")
        
        # Documentation recommendations
        if breakdown.documentation_score < 60:
            recommendations.append("Add docstrings and comments to improve code maintainability.")
        
        # Complexity recommendations
        if breakdown.complexity_score < 60:
            recommendations.append("Refactor code to reduce complexity and improve maintainability.")
        
        return recommendations[:5]  # Limit to top 5 recommendations

    def to_dict(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Return result as dictionary (already in dict format)."""
        return result
