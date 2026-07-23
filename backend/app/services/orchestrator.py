"""
Agent Orchestrator Service.

This module implements the core orchestration layer for the autonomous
AI Software Engineering Agent. It receives user goals, creates execution plans,
selects and executes tools, observes results, stores memory, and decides next actions
until the goal is completed.
"""

import asyncio
import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ToolType(str, Enum):
    """Types of tools available to the agent."""
    CODE_GENERATION = "code_generation"
    CODE_EXECUTION = "code_execution"
    CODE_REVIEW = "code_review"
    SECURITY_SCAN = "security_scan"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    TEST_EXECUTION = "test_execution"
    CODE_REPAIR = "code_repair"
    FILE_OPERATIONS = "file_operations"


class ActionType(str, Enum):
    """Possible actions the agent can take."""
    PLAN = "plan"
    EXECUTE_TOOL = "execute_tool"
    OBSERVE = "observe"
    STORE_MEMORY = "store_memory"
    DECIDE = "decide"
    REFLECT = "reflect"
    TERMINATE = "terminate"


class ToolCall(BaseModel):
    """Represents a tool call request."""
    tool_type: ToolType
    parameters: dict[str, Any]
    confidence: float = Field(ge=0.0, le=1.0)
    priority: int = 1


class ToolResult(BaseModel):
    """Represents a tool execution result."""
    success: bool
    output: Any
    error: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class MemoryEntry(BaseModel):
    """A memory entry for the agent's working memory."""
    key: str
    value: Any
    timestamp: datetime = Field(default_factory=datetime.now)
    importance: float = Field(ge=0.0, le=1.0, default=0.5)


class Decision(BaseModel):
    """A decision made by the agent."""
    action: ActionType
    reason: str
    confidence: float = Field(ge=0.0, le=1.0)
    next_tool: Optional[ToolType] = None
    tool_call: Optional[ToolCall] = None


class ExecutionStep(BaseModel):
    """A single step in the execution timeline."""
    step_number: int
    timestamp: datetime = Field(default_factory=datetime.now)
    action: ActionType
    tool_type: Optional[ToolType] = None
    input_data: Optional[dict] = None
    result: Optional[ToolResult] = None
    decision: Optional[Decision] = None
    duration_ms: Optional[float] = None


class AgentState(str, Enum):
    """Possible states of the agent."""
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    REFLECTING = "reflecting"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentContext(BaseModel):
    """The context for agent execution."""
    session_id: UUID = Field(default_factory=uuid4)
    user_goal: str
    current_step: int = 0
    state: AgentState = AgentState.IDLE
    plan: list[ToolType] = Field(default_factory=list)
    reasoning_trace: list[str] = Field(default_factory=list)
    execution_timeline: list[ExecutionStep] = Field(default_factory=list)
    working_memory: dict[str, Any] = Field(default_factory=dict)
    long_term_memory: list[MemoryEntry] = Field(default_factory=list)
    current_code: str = ""
    current_tests: str = ""
    errors: list[str] = Field(default_factory=list)
    confidence: float = 1.0
    max_steps: int = 50


class AgentOrchestrator:
    """
    The central orchestrator for the autonomous agent.
    
    Responsibilities:
    - Receive user goals
    - Create execution plans
    - Select and execute tools
    - Observe results
    - Store memory
    - Decide next actions
    - Repeat until goal completion
    - Return structured timeline
    """
    
    def __init__(self):
        self.context: AgentContext | None = None
        self._tool_registry: dict[ToolType, Any] = {}
        self._decision_history: list[Decision] = []
    
    def register_tool(self, tool_type: ToolType, tool_instance: Any) -> None:
        """Register a tool with the orchestrator."""
        self._tool_registry[tool_type] = tool_instance
        logger.info(f"Registered tool: {tool_type}")
    
    def start_session(self, user_goal: str, max_steps: int = 50) -> UUID:
        """Start a new execution session."""
        self.context = AgentContext(
            user_goal=user_goal,
            max_steps=max_steps
        )
        logger.info(f"Started session {self.context.session_id} for goal: {user_goal[:50]}...")
        return self.context.session_id
    
    async def run(self) -> dict[str, Any]:
        """Main execution loop until goal completion."""
        if not self.context:
            raise RuntimeError("No active session. Call start_session first.")
        
        self.context.state = AgentState.PLANNING
        
        # Phase 1: Planning
        await self._plan()
        
        # Phase 2: Execution Loop
        while (
            self.context.state != AgentState.COMPLETED and
            self.context.state != AgentState.FAILED and
            self.context.current_step < self.context.max_steps
        ):
            step_start = datetime.now()
            
            # Phase 3: Tool Selection
            tool_call = await self._select_tool()
            
            if not tool_call:
                self.context.state = AgentState.FAILED
                break
            
            # Phase 4: Tool Execution
            result = await self._execute_tool(tool_call)
            
            # Phase 5: Observation
            await self._observe(result)
            
            # Phase 6: Memory Storage
            await self._store_memory(tool_call, result)
            
            # Phase 7: Decision Making
            decision = await self._decide(result)
            
            # Record step
            step_duration = (datetime.now() - step_start).total_seconds() * 1000
            self.context.execution_timeline.append(ExecutionStep(
                step_number=self.context.current_step,
                action=decision.action,
                tool_type=tool_call.tool_type,
                input_data=tool_call.parameters,
                result=result,
                decision=decision,
                duration_ms=step_duration
            ))
            
            self.context.current_step += 1
            
            # Phase 8: Check termination
            if decision.action == ActionType.TERMINATE:
                break
        
        return self._build_result()
    
    async def _plan(self) -> None:
        """Create an execution plan based on the user goal."""
        logger.info("Planning execution...")
        
        # Use the planner tool if available
        if ToolType.CODE_GENERATION in self._tool_registry:
            # Create initial plan
            self.context.plan = [
                ToolType.CODE_GENERATION,
                ToolType.CODE_EXECUTION,
                ToolType.CODE_REVIEW,
                ToolType.SECURITY_SCAN,
                ToolType.PERFORMANCE_ANALYSIS,
            ]
            self.context.reasoning_trace.append(
                f"Planned execution sequence: {[t.value for t in self.context.plan]}"
            )
            self.context.state = AgentState.EXECUTING
        else:
            # Default minimal plan
            self.context.plan = [ToolType.CODE_GENERATION, ToolType.CODE_EXECUTION]
            self.context.state = AgentState.EXECUTING
    
    async def _select_tool(self) -> Optional[ToolCall]:
        """Select the next tool to use based on current state."""
        if not self.context or not self.context.plan:
            return None
        
        # Determine next action based on state
        if self.context.current_code and not self.context.errors:
            # Success path
            self.context.state = AgentState.COMPLETED
            return None
        
        if self.context.errors:
            # Error path - need repair
            return ToolCall(
                tool_type=ToolType.CODE_REPAIR,
                parameters={
                    "code": self.context.current_code,
                    "errors": self.context.errors
                },
                confidence=0.8
            )
        
        # Continue with plan
        if self.context.current_step < len(self.context.plan):
            next_tool = self.context.plan[self.context.current_step]
            return ToolCall(
                tool_type=next_tool,
                parameters={"goal": self.context.user_goal},
                confidence=0.9
            )
        
        return None
    
    async def _execute_tool(self, tool_call: ToolCall) -> ToolResult:
        """Execute a tool and return the result."""
        logger.info(f"Executing tool: {tool_call.tool_type}")
        
        if tool_call.tool_type not in self._tool_registry:
            return ToolResult(
                success=False,
                output=None,
                error=f"Tool not registered: {tool_call.tool_type}"
            )
        
        tool = self._tool_registry[tool_call.tool_type]
        
        try:
            # Call the tool's execute method
            if hasattr(tool, 'execute'):
                result = await tool.execute(**tool_call.parameters)
            elif hasattr(tool, 'run'):
                result = await tool.run(**tool_call.parameters)
            else:
                result = await tool(**tool_call.parameters)
            
            return ToolResult(
                success=True,
                output=result,
                metadata={"tool": tool_call.tool_type.value}
            )
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return ToolResult(
                success=False,
                output=None,
                error=str(e)
            )
    
    async def _observe(self, result: ToolResult) -> None:
        """Observe and analyze the tool result."""
        logger.info(f"Observing result: success={result.success}")
        
        if not result.success:
            self.context.errors.append(result.error or "Unknown error")
            self.context.confidence *= 0.9
            return
        
        # Extract relevant information
        output = result.output
        if isinstance(output, dict):
            if 'code' in output:
                self.context.current_code = output['code']
            if 'tests' in output:
                self.context.current_tests = output.get('tests', '')
            if 'errors' in output:
                self.context.errors.extend(output['errors'])
            if 'confidence' in output:
                self.context.confidence = min(1.0, self.context.confidence + 0.1)
    
    async def _store_memory(self, tool_call: ToolCall, result: ToolResult) -> None:
        """Store observations in memory."""
        if not self.context:
            return
        
        memory_entry = MemoryEntry(
            key=f"step_{self.context.current_step}_{tool_call.tool_type.value}",
            value={
                "input": tool_call.parameters,
                "output": result.output,
                "success": result.success,
                "timestamp": datetime.now().isoformat()
            },
            importance=0.5
        )
        
        self.context.working_memory[memory_entry.key] = memory_entry.value
        
        # Trim old memories if too large
        if len(self.context.working_memory) > 100:
            keys_to_remove = list(self.context.working_memory.keys())[:50]
            for key in keys_to_remove:
                del self.context.working_memory[key]
    
    async def _decide(self, result: ToolResult) -> Decision:
        """Make a decision about the next action."""
        if not self.context:
            return Decision(
                action=ActionType.TERMINATE,
                reason="No context available",
                confidence=0.0
            )
        
        # Decision logic based on result
        if not result.success:
            return Decision(
                action=ActionType.REFLECT,
                reason=f"Tool failed: {result.error}",
                confidence=0.8,
                next_tool=ToolType.CODE_REPAIR
            )
        
        if self.context.errors:
            return Decision(
                action=ActionType.REFLECT,
                reason=f"Errors detected: {len(self.context.errors)}",
                confidence=0.7,
                next_tool=ToolType.CODE_REPAIR
            )
        
        if self.context.current_step >= len(self.context.plan) - 1:
            return Decision(
                action=ActionType.TERMINATE,
                reason="Execution plan complete, all tests passed",
                confidence=0.9
            )
        
        return Decision(
            action=ActionType.EXECUTE_TOOL,
            reason="Continuing with execution plan",
            confidence=0.8,
            next_tool=self.context.plan[self.context.current_step + 1] if self.context.current_step + 1 < len(self.context.plan) else None
        )
    
    def _build_result(self) -> dict[str, Any]:
        """Build the final result dictionary."""
        if not self.context:
            return {"error": "No active session"}
        
        return {
            "session_id": str(self.context.session_id),
            "goal": self.context.user_goal,
            "status": self.context.state.value,
            "attempts": self.context.current_step,
            "final_code": self.context.current_code,
            "confidence": self.context.confidence,
            "errors": self.context.errors,
            "timeline": [
                {
                    "step": step.step_number,
                    "action": step.action.value,
                    "tool": step.tool_type.value if step.tool_type else None,
                    "duration_ms": step.duration_ms,
                    "success": step.result.success if step.result else None
                }
                for step in self.context.execution_timeline
            ],
            "reasoning_trace": self.context.reasoning_trace,
            "memory_size": len(self.context.working_memory),
            "completed_at": datetime.now().isoformat()
        }


# Singleton instance for the orchestrator
_orchestrator: AgentOrchestrator | None = None

def get_orchestrator() -> AgentOrchestrator:
    """Get or create the singleton orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    return _orchestrator