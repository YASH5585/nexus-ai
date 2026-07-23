"""
Reflection Engine for Nexus AI.

This engine analyzes tool execution results to improve decision making.
It provides structured analysis of tool outcomes to enhance the agent's reasoning.
"""

import hashlib
import json
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class ExecutionResult:
    """Structured representation of tool execution result."""
    tool_type: str
    input_data: Dict[str, Any]
    output: Any
    success: bool
    error: Optional[str] = None
    timestamp: Optional[datetime] = None
    duration_ms: Optional[float] = None
    step_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.duration_ms is None:
            self.duration_ms = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "tool_type": self.tool_type,
            "input_data": self.input_data,
            "output": self.output,
            "success": self.success,
            "error": self.error,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "step_id": self.step_id,
            "context": self.context,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExecutionResult":
        """Create ExecutionResult from dictionary."""
        return ExecutionResult(
            tool_type=data.get("tool_type", ""),
            input_data=data.get("input_data", {}),
            output=data.get("output", None),
            success=data.get("success", False),
            error=data.get("error"),
            timestamp=datetime.fromisoformat(data.get("timestamp", "")) if data.get("timestamp") else None,
            duration_ms=data.get("duration_ms", 0.0),
            step_id=data.get("step_id"),
            context=data.get("context", {}),
        )


class ReflectionEngine:
    """Analyzes execution results and produces structured reflection data."""

    def analyze(self, result: ExecutionResult) -> Dict[str, Any]:
        """Analyze tool execution result and return structured reflection."""
        analysis: Dict[str, Any] = {
            "tool_type": result.tool_type,
            "success": result.success,
            "timestamp": result.timestamp.isoformat() if result.timestamp else None,
            "duration_ms": result.duration_ms,
            "step_id": result.step_id,
            "context": result.context,
        }

        if not result.success:
            analysis["analysis"] = {
                "failure_type": self._analyze_failure_type(result),
                "root_causes": self._identify_root_causes(result),
                "recommended_actions": self._recommend_actions(result),
                "confidence_in_next_action": self._assess_next_action_feasibility(result),
            }

        logger.info(
            "Reflection complete",
            tool_type=result.tool_type,
            success=result.success,
            failure_type=analysis.get("analysis", {}).get("failure_type"),
        )
        return analysis

    def _analyze_failure_type(self, result: ExecutionResult) -> str:
        """Analyze the type of failure."""
        error_msg = (result.error or "").lower()
        if "timeout" in error_msg:
            return "timeout"
        if "permission" in error_msg:
            return "permission"
        if "resource" in error_msg:
            return "resource_exhaustion"
        if "network" in error_msg or "connection" in error_msg:
            return "network"
        if "unauthorized" in error_msg:
            return "authentication"
        if "not_found" in error_msg:
            return "not_found"
        if "invalid" in error_msg:
            return "invalid_input"
        return "unknown"

    def _identify_root_causes(self, result: ExecutionResult) -> List[str]:
        """Identify potential root causes of failure."""
        causes: List[str] = []
        error_msg = (result.error or "").lower()
        context = result.context or {}

        if "timeout" in error_msg:
            causes.extend([
                "Timeout during execution",
                "Long-running operation exceeded timeout",
                "Resource-intensive operation exceeded limits",
            ])
        if "invalid" in error_msg:
            causes.extend([
                "Invalid input parameters",
                "Malformed input data",
                "Invalid syntax or structure",
            ])
        if context.get("timeout"):
            causes.append("Execution timeout occurred")
        if context.get("resource_limit"):
            causes.append("Resource constraints exceeded")
        if context.get("invalid_input"):
            causes.append("Invalid input parameters")
        if context.get("malformed_data"):
            causes.append("Malformed input data")
        if context.get("missing_dependency"):
            causes.append("Missing required dependency")
        if context.get("incompatible_version"):
            causes.append("Incompatible software version")
        if not causes:
            causes.append("Tool execution failed")
        return causes

    def _recommend_actions(self, result: ExecutionResult) -> List[str]:
        """Recommend actions based on analysis."""
        error_msg = (result.error or "").lower()
        if "timeout" in error_msg:
            return [
                "Increase timeout limits",
                "Optimize tool execution",
                "Increase resource allocation",
                "Implement timeout handling",
                "Review timeout configuration",
            ]
        if "invalid" in error_msg or "format" in error_msg:
            return [
                "Validate input format",
                "Verify parameter types",
                "Check input data integrity",
                "Add input validation",
                "Implement input sanitization",
            ]
        return [
            "Analyze error details thoroughly",
            "Check tool documentation",
            "Review error handling in tool implementation",
            "Test with similar inputs",
            "Consult documentation",
        ]

    def _assess_next_action_feasibility(self, result: ExecutionResult) -> float:
        """Assess how feasible the next action is given current state."""
        error_msg = (result.error or "").lower()
        if "timeout" in error_msg:
            return 0.4
        if "invalid" in error_msg:
            return 0.6
        if not result.success:
            return 0.3
        return 0.8
