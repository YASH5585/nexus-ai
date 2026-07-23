"""
Security Scanner for Nexus AI.

Scans Python code for security vulnerabilities including:
- eval() and exec() usage
- Command injection
- SQL injection
- Path traversal
- Unsafe subprocess usage
- Hardcoded secrets
- Unsafe pickle usage
"""

import ast
import re
import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Set, Tuple, Pattern
from collections import defaultdict
import structlog

logger = structlog.get_logger(__name__)


@dataclass
class SecurityIssue:
    """A single security issue found during scanning."""
    category: str
    severity: str
    risk: str
    line_number: Optional[int]
    code_snippet: Optional[str]
    recommendation: str


@dataclass
class SecurityScanReport:
    """Complete security scan report."""
    passed: bool
    total_issues: int
    issues: List[SecurityIssue]
    summary: Dict[str, int]
    scan_time: float


class SecurityScanner:
    """
    Static security analyzer for Python code.
    
    Scans code for common security vulnerabilities and provides
    actionable recommendations for remediation.
    """

    def __init__(self, strict: bool = False):
        """
        Initialize the security scanner.
        
        Args:
            strict: Enable strict mode for more thorough checks
        """
        self.strict = strict
        self.logger = logger.bind(component="SecurityScanner")
        
        # Patterns for detecting security issues
        self._patterns = {
            "eval": re.compile(r'\beval\s*\('),
            "exec": re.compile(r'\bexec\s*\('),
            "command_injection": re.compile(r'(os\.system|subprocess\.|shell=True|popen|call\(|check_output\()'),
            "sql_injection": re.compile(r'(execute\s*\(|executemany\s*\(|cursor\.execute|SELECT.*FROM|INSERT.*INTO|UPDATE.*SET|DELETE.*FROM).*%|\.format\('),
            "path_traversal": re.compile(r'(os\.path\.join|pathlib\.Path).*\.\.\/|\.\.'),
            "unsafe_subprocess": re.compile(r'subprocess\.(call|run|Popen|check_output|check_call)\s*\([^)]*shell\s*=\s*True'),
            "hardcoded_secret": re.compile(r'(password|secret|api_key|token|auth|credential)\s*=\s*["\'][^"\']+["\']', re.IGNORECASE),
            "unsafe_pickle": re.compile(r'\bpickle\.loads?\s*\('),
            "yaml_load": re.compile(r'yaml\.load\s*\([^)]*Loader\s*=\s*None'),
            "temp_file": re.compile(r'tempfile\.(mkstemp|mkdtemp|NamedTemporaryFile)\s*\('),
            "random": re.compile(r'\brandom\.(random|randint|choice)\s*\('),
            "md5": re.compile(r'\bhashlib\.md5\s*\('),
            "ssl_verify": re.compile(r'verify\s*=\s*False'),
            "http": re.compile(r'urllib\.request\.urlopen|requests\.(get|post|put|delete)\s*\('),
        }

    def scan(self, code: str) -> SecurityScanReport:
        """
        Scan Python code for security vulnerabilities.
        
        Args:
            code: Python source code to scan
            
        Returns:
            SecurityScanReport with all findings
        """
        start_time = time.perf_counter()
        issues: List[SecurityIssue] = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            self.logger.warning("Code has syntax errors, skipping AST analysis", error=str(e))
            return SecurityScanReport(
                passed=False,
                total_issues=1,
                issues=[
                    SecurityIssue(
                        category="syntax_error",
                        severity="critical",
                        risk="Code contains syntax errors which may hide security issues",
                        line_number=e.lineno,
                        code_snippet=None,
                        recommendation="Fix syntax errors before security scanning"
                    )
                ],
                summary={"syntax_error": 1},
                scan_time=time.perf_counter() - start_time
            )
        
        # Run all security checks
        issues.extend(self._check_eval_exec(tree, code))
        issues.extend(self._check_command_injection(tree, code))
        issues.extend(self._check_sql_injection(tree, code))
        issues.extend(self._check_path_traversal(tree, code))
        issues.extend(self._check_unsafe_subprocess(tree, code))
        issues.extend(self._check_hardcoded_secrets(tree, code))
        issues.extend(self._check_unsafe_pickle(tree, code))
        issues.extend(self._check_additional_issues(tree, code))
        
        # Build summary
        summary: Dict[str, int] = defaultdict(int)
        for issue in issues:
            summary[issue.category] += 1
        
        scan_time = time.perf_counter() - start_time
        
        self.logger.info(
            "Security scan completed",
            total_issues=len(issues),
            categories=dict(summary),
            scan_time=round(scan_time, 3)
        )
        
        return SecurityScanReport(
            passed=len(issues) == 0,
            total_issues=len(issues),
            issues=issues,
            summary=dict(summary),
            scan_time=round(scan_time, 3)
        )

    def _check_eval_exec(self, tree: ast.AST, code: str) -> List[SecurityIssue]:
        """Detect eval() and exec() usage."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ('eval', 'exec'):
                        line = getattr(node, 'lineno', None)
                        snippet = self._get_code_snippet(code, line)
                        issues.append(SecurityIssue(
                            category=node.func.id,
                            severity="critical",
                            risk=f"Use of {node.func.id}() can execute arbitrary code and is a major security risk",
                            line_number=line,
                            code_snippet=snippet,
                            recommendation=f"Avoid using {node.func.id}(). Use safer alternatives like ast.literal_eval() or explicit parsing"
                        ))
        
        return issues

    def _check_command_injection(self, tree: ast.AST, code: str) -> List[SecurityIssue]:
        """Detect potential command injection vulnerabilities."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node.func)
                
                # Check for os.system, subprocess calls, popen, etc.
                if any(pattern in func_name for pattern in ['os.system', 'subprocess', 'popen', 'call', 'check_output']):
                    line = getattr(node, 'lineno', None)
                    snippet = self._get_code_snippet(code, line)
                    
                    # Check for shell=True
                    has_shell_true = self._has_shell_true(node)
                    if has_shell_true:
                        issues.append(SecurityIssue(
                            category="command_injection",
                            severity="critical",
                            risk="Command injection vulnerability: shell=True allows arbitrary command execution",
                            line_number=line,
                            code_snippet=snippet,
                            recommendation="Avoid using shell=True. Use array-style arguments instead: subprocess.run(['command', 'arg'])"
                        ))
                    else:
                        issues.append(SecurityIssue(
                            category="command_injection",
                            severity="high",
                            risk="Potential command injection: user input may be passed to system commands",
                            line_number=line,
                            code_snippet=snippet,
                            recommendation="Validate and sanitize all user input before passing to system commands"
                        ))
        
        return issues

    def _check_sql_injection(self, tree: ast.AST, code: str) -> List[SecurityIssue]:
        """Detect SQL injection vulnerabilities."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node.func)
                
                # Check for SQL execution methods
                if any(pattern in func_name for pattern in ['execute', 'executemany', 'cursor.execute']):
                    line = getattr(node, 'lineno', None)
                    snippet = self._get_code_snippet(code, line)
                    
                    # Check for string formatting or concatenation in arguments
                    has_formatting = self._has_string_formatting(node)
                    if has_formatting:
                        issues.append(SecurityIssue(
                            category="sql_injection",
                            severity="critical",
                            risk="SQL injection vulnerability: user input may be interpolated directly into SQL queries",
                            line_number=line,
                            code_snippet=snippet,
                            recommendation="Use parameterized queries with placeholders (?, %s) instead of string formatting"
                        ))
        
        return issues

    def _check_path_traversal(self, tree: ast.AST, code: str) -> List[SecurityIssue]:
        """Detect path traversal vulnerabilities."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node.func)
                
                # Check for path joining with user input
                if any(pattern in func_name for pattern in ['os.path.join', 'pathlib.Path', 'open']):
                    line = getattr(node, 'lineno', None)
                    snippet = self._get_code_snippet(code, line)
                    
                    # Check for .. in arguments
                    has_path_traversal = self._has_path_traversal(node)
                    if has_path_traversal:
                        issues.append(SecurityIssue(
                            category="path_traversal",
                            severity="high",
                            risk="Path traversal vulnerability: user input may allow access to files outside intended directory",
                            line_number=line,
                            code_snippet=snippet,
                            recommendation="Validate and sanitize file paths. Use os.path.abspath() and check against allowed directories"
                        ))
        
        return issues

    def _check_unsafe_subprocess(self, tree: ast.AST, code: str) -> List[SecurityIssue]:
        """Detect unsafe subprocess usage."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node.func)
                
                if 'subprocess' in func_name:
                    line = getattr(node, 'lineno', None)
                    snippet = self._get_code_snippet(code, line)
                    
                    # Check for shell=True
                    has_shell_true = self._has_shell_true(node)
                    if has_shell_true:
                        issues.append(SecurityIssue(
                            category="unsafe_subprocess",
                            severity="critical",
                            risk="Unsafe subprocess usage with shell=True allows arbitrary command execution",
                            line_number=line,
                            code_snippet=snippet,
                            recommendation="Use shell=False and pass commands as a list of arguments"
                        ))
        
        return issues

    def _check_hardcoded_secrets(self, tree: ast.AST, code: str) -> List[SecurityIssue]:
        """Detect hardcoded secrets and credentials."""
        issues = []
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', "password", "high"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "secret", "high"),
            (r'api_key\s*=\s*["\'][^"\']+["\']', "API key", "critical"),
            (r'token\s*=\s*["\'][^"\']+["\']', "token", "high"),
            (r'auth\s*=\s*["\'][^"\']+["\']', "auth", "high"),
            (r'credential\s*=\s*["\'][^"\']+["\']', "credential", "critical"),
        ]
        
        for pattern, secret_type, severity in secret_patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                snippet = self._get_code_snippet(code, line_num)
                issues.append(SecurityIssue(
                    category="hardcoded_secret",
                    severity=severity,
                    risk=f"Hardcoded {secret_type} found in code. This is a major security risk if the code is exposed",
                    line_number=line_num,
                    code_snippet=snippet,
                    recommendation="Use environment variables or a secure secrets manager instead of hardcoding secrets"
                ))
        
        return issues

    def _check_unsafe_pickle(self, tree: ast.AST, code: str) -> List[SecurityIssue]:
        """Detect unsafe pickle usage."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node.func)
                
                if 'pickle' in func_name and ('load' in func_name or 'loads' in func_name):
                    line = getattr(node, 'lineno', None)
                    snippet = self._get_code_snippet(code, line)
                    issues.append(SecurityIssue(
                        category="unsafe_pickle",
                        severity="critical",
                        risk="Unsafe pickle deserialization can execute arbitrary code from malicious pickle data",
                        line_number=line,
                        code_snippet=snippet,
                        recommendation="Use JSON or other safe serialization formats instead of pickle for untrusted data"
                    ))
        
        return issues

    def _check_additional_issues(self, tree: ast.AST, code: str) -> List[SecurityIssue]:
        """Check for additional security issues."""
        issues = []
        
        # Check for yaml.load without safe loader
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node.func)
                if 'yaml.load' in func_name:
                    line = getattr(node, 'lineno', None)
                    snippet = self._get_code_snippet(code, line)
                    has_safe_loader = self._has_safe_loader(node)
                    if not has_safe_loader:
                        issues.append(SecurityIssue(
                            category="unsafe_yaml",
                            severity="high",
                            risk="yaml.load() without SafeLoader can execute arbitrary code from malicious YAML",
                            line_number=line,
                            code_snippet=snippet,
                            recommendation="Use yaml.safe_load() instead of yaml.load()"
                        ))
        
        # Check for SSL verification disabled
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == 'verify' and isinstance(keyword.value, ast.Constant) and keyword.value.value is False:
                        line = getattr(node, 'lineno', None)
                        snippet = self._get_code_snippet(code, line)
                        issues.append(SecurityIssue(
                            category="ssl_verify_disabled",
                            severity="high",
                            risk="SSL certificate verification is disabled, making the connection vulnerable to MITM attacks",
                            line_number=line,
                            code_snippet=snippet,
                            recommendation="Enable SSL verification by setting verify=True or removing the verify parameter"
                        ))
        
        # Check for random module usage (not cryptographically secure)
        if self.strict:
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    func_name = self._get_func_name(node.func)
                    if 'random.' in func_name:
                        line = getattr(node, 'lineno', None)
                        snippet = self._get_code_snippet(code, line)
                        issues.append(SecurityIssue(
                            category="insecure_random",
                            severity="medium",
                            risk="random module is not cryptographically secure and should not be used for security-sensitive operations",
                            line_number=line,
                            code_snippet=snippet,
                            recommendation="Use secrets module for cryptographically secure random numbers"
                        ))
        
        # Check for MD5 usage
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node.func)
                if 'hashlib.md5' in func_name:
                    line = getattr(node, 'lineno', None)
                    snippet = self._get_code_snippet(code, line)
                    issues.append(SecurityIssue(
                        category="weak_cryptography",
                        severity="high",
                        risk="MD5 is cryptographically broken and should not be used for security-sensitive applications",
                        line_number=line,
                        code_snippet=snippet,
                        recommendation="Use SHA-256 or SHA-3 instead of MD5"
                    ))
        
        return issues

    def _get_func_name(self, node: ast.AST) -> str:
        """Extract function name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_func_name(node.value)}.{node.attr}"
        return ""

    def _has_shell_true(self, node: ast.Call) -> bool:
        """Check if a call has shell=True argument."""
        for keyword in node.keywords:
            if keyword.arg == 'shell':
                if isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    return True
        return False

    def _has_string_formatting(self, node: ast.Call) -> bool:
        """Check if a call uses string formatting in arguments."""
        for arg in node.args:
            if isinstance(arg, (ast.BinOp, ast.Call, ast.JoinedStr)):
                return True
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                if '%' in arg.value or '{' in arg.value:
                    return True
        return False

    def _has_path_traversal(self, node: ast.Call) -> bool:
        """Check if a call has potential path traversal."""
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                if '..' in arg.value:
                    return True
            elif isinstance(arg, ast.Name):
                return True
        return False

    def _has_safe_loader(self, node: ast.Call) -> bool:
        """Check if yaml.load uses a safe loader."""
        for keyword in node.keywords:
            if keyword.arg == 'Loader':
                if isinstance(keyword.value, ast.Name):
                    return keyword.value.id == 'SafeLoader'
                elif isinstance(keyword.value, ast.Attribute):
                    return keyword.value.attr == 'SafeLoader'
        return False

    def _get_code_snippet(self, code: str, line_number: Optional[int], context: int = 2) -> Optional[str]:
        """Extract code snippet around a line number."""
        if line_number is None or line_number < 1:
            return None
        
        lines = code.splitlines()
        start = max(0, line_number - context - 1)
        end = min(len(lines), line_number + context)
        
        snippet_lines = lines[start:end]
        return '\n'.join(snippet_lines)

    def to_dict(self, report: SecurityScanReport) -> Dict[str, Any]:
        """
        Convert SecurityScanReport to dictionary for JSON serialization.
        
        Args:
            report: SecurityScanReport instance
            
        Returns:
            Dictionary representation
        """
        return {
            "passed": report.passed,
            "total_issues": report.total_issues,
            "issues": [
                {
                    "category": issue.category,
                    "severity": issue.severity,
                    "risk": issue.risk,
                    "line_number": issue.line_number,
                    "code_snippet": issue.code_snippet,
                    "recommendation": issue.recommendation
                }
                for issue in report.issues
            ],
            "summary": report.summary,
            "scan_time": report.scan_time
        }
