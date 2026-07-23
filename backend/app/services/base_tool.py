"""
Base Tool Interface.

All tools in the Nexus AI ecosystem must implement this common interface
to enable dynamic tool selection by the agent orchestrator.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
import time


class ToolResult:
    """Standard result format for all tools."""
    
    def __init__(
        self,
        success: bool,
        output: Any = None,
        error: Optional[str] = None,
        metadata: Optional[dict] = None,
        duration_ms: Optional[float] = None
    ):
        self.success = success
        self.output = output
        self.error = error
        self.metadata = metadata or {}
        self.duration_ms = duration_ms
    
    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "metadata": self.metadata,
            "duration_ms": self.duration_ms
        }


class BaseTool(ABC):
    """Abstract base class for all Nexus AI tools."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool with the given parameters.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            ToolResult: Standard result format
        """
        pass
    
    def _create_result(
        self,
        success: bool,
        output: Any = None,
        error: Optional[str] = None,
        metadata: Optional[dict] = None,
        duration_ms: Optional[float] = None
    ) -> ToolResult:
        """Helper to create a ToolResult."""
        return ToolResult(
            success=success,
            output=output,
            error=error,
            metadata=metadata or {"tool": self.name},
            duration_ms=duration_ms
        )


class ToolRegistry:
    """Registry for managing available tools."""
    
    _instance = None
    _tools: dict[str, BaseTool] = {}
    
    @classmethod
    def get_instance(cls) -> "ToolRegistry":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def register(self, tool: BaseTool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def list_tools(self) -> list[str]:
        """List all registered tool names."""
        return list(self._tools.keys())
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name (alias for get)."""
        return self.get(name)


def register_tool(tool_class):
    """Decorator to register a tool with the registry."""
    def wrapper(*args, **kwargs):
        tool = tool_class(*args, **kwargs)
        ToolRegistry.get_instance().register(tool)
        return tool
    return wrapper