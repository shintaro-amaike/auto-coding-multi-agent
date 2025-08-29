#!/usr/bin/env python3
"""
Claude Code SDK interface module.

This module handles all interactions with the Claude Code SDK.
"""

import asyncio
from typing import AsyncIterator, List, Optional, Any

# Claude Code SDK imports - required
try:
    from claude_code_sdk import (
        query,
        ClaudeCodeOptions,
        AssistantMessage,
        UserMessage,
        SystemMessage,
        ResultMessage,
        TextBlock,
        ToolUseBlock,
        ToolResultBlock,
        ClaudeSDKError,
        CLINotFoundError,
        CLIConnectionError,
        ProcessError,
        CLIJSONDecodeError
    )
    SDK_AVAILABLE = True
except ImportError as e:
    raise ImportError(
        "claude_code_sdk package is required but not found. "
        "Please install it using: pip install claude-code-sdk"
    ) from e


def is_sdk_available() -> bool:
    """Check if Claude Code SDK is available."""
    return SDK_AVAILABLE


def create_claude_options(
    allowed_tools: Optional[List[str]] = None,
    system_prompt: str = "",
    max_turns: int = 10,
    permission_mode: str = "acceptEdits"
) -> ClaudeCodeOptions:
    """Create Claude Code options with specified parameters."""
    if allowed_tools is None:
        allowed_tools = ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
    
    return ClaudeCodeOptions(
        allowed_tools=allowed_tools,
        system_prompt=system_prompt,
        max_turns=max_turns,
        permission_mode=permission_mode
    )


async def execute_claude_query(
    prompt: str,
    options: ClaudeCodeOptions
) -> AsyncIterator[Any]:
    """Execute a query using Claude Code SDK."""
    if not SDK_AVAILABLE:
        raise RuntimeError("Claude Code SDK is not available")
    
    try:
        async for message in query(prompt=prompt, options=options):
            yield message
    except Exception as e:
        raise RuntimeError(f"Claude Code SDK query failed: {e}") from e


def apply_nested_asyncio():
    """Apply nested asyncio support for Jupyter environments."""
    try:
        import nest_asyncio
        nest_asyncio.apply()
    except ImportError:
        # nest_asyncio is optional, only warn if we're in Jupyter
        try:
            import IPython
            print("⚠️  nest_asyncio not installed. Install with: pip install nest-asyncio")
        except ImportError:
            # Not in Jupyter, no problem
            pass


# Export all necessary classes and functions
__all__ = [
    # Core SDK classes
    "query",
    "ClaudeCodeOptions",
    "AssistantMessage", 
    "UserMessage",
    "SystemMessage",
    "ResultMessage",
    "TextBlock",
    "ToolUseBlock", 
    "ToolResultBlock",
    
    # Exception classes
    "ClaudeSDKError",
    "CLINotFoundError",
    "CLIConnectionError", 
    "ProcessError",
    "CLIJSONDecodeError",
    
    # Utility functions
    "is_sdk_available",
    "create_claude_options",
    "execute_claude_query",
    "apply_nested_asyncio",
    
    # Module state
    "SDK_AVAILABLE"
]