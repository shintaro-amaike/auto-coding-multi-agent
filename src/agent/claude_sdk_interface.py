#!/usr/bin/env python3
"""
Claude Code SDK interface module.

Handles all interactions with the Claude Code SDK and provides
fallback implementations when the SDK is not available.
"""

# Claude Code SDK imports with fallback implementations
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
except ImportError:
    print("⚠️ claude_code_sdk package not found. Please install: pip install claude-code-sdk")
    query = None
    SDK_AVAILABLE = False
    
    # Fallback class definitions for required classes
    class ClaudeCodeOptions:
        """Fallback implementation for ClaudeCodeOptions."""
        def __init__(self, **kwargs):
            self.allowed_tools = kwargs.get('allowed_tools', [])
            self.system_prompt = kwargs.get('system_prompt', '')
            self.max_turns = kwargs.get('max_turns', 10)
            self.permission_mode = kwargs.get('permission_mode', 'acceptEdits')
    
    class AssistantMessage:
        """Fallback implementation for AssistantMessage."""
        def __init__(self, content=None):
            self.content = content or []
    
    class UserMessage:
        """Fallback implementation for UserMessage."""
        def __init__(self, content=None):
            self.content = content
    
    class SystemMessage:
        """Fallback implementation for SystemMessage."""
        def __init__(self, content=None):
            self.content = content
    
    class ResultMessage:
        """Fallback implementation for ResultMessage."""
        pass
    
    class TextBlock:
        """Fallback implementation for TextBlock."""
        def __init__(self, text=""):
            self.text = text
    
    class ToolUseBlock:
        """Fallback implementation for ToolUseBlock."""
        pass
    
    class ToolResultBlock:
        """Fallback implementation for ToolResultBlock."""
        pass
    
    class ClaudeSDKError(Exception):
        """Base exception for Claude SDK errors."""
        pass
    
    class CLINotFoundError(ClaudeSDKError):
        """Exception for CLI not found errors."""
        pass
    
    class CLIConnectionError(ClaudeSDKError):
        """Exception for CLI connection errors."""
        pass
    
    class ProcessError(ClaudeSDKError):
        """Exception for process errors."""
        pass
    
    class CLIJSONDecodeError(ClaudeSDKError):
        """Exception for JSON decode errors."""
        pass


def is_sdk_available() -> bool:
    """Check if Claude Code SDK is available."""
    return SDK_AVAILABLE


def apply_nested_asyncio():
    """Apply nested asyncio support for Jupyter environments."""
    try:
        import nest_asyncio
        nest_asyncio.apply()
    except ImportError:
        print("⚠️ nest_asyncio package not found. Install with: pip install nest-asyncio")
    except RuntimeError:
        # Already applied
        pass


def create_claude_options(allowed_tools: list, system_prompt: str, 
                         max_turns: int = 10, 
                         permission_mode: str = 'acceptEdits') -> ClaudeCodeOptions:
    """Create ClaudeCodeOptions with the given parameters."""
    return ClaudeCodeOptions(
        allowed_tools=allowed_tools,
        system_prompt=system_prompt,
        max_turns=max_turns,
        permission_mode=permission_mode
    )


async def execute_claude_query(prompt: str, options: ClaudeCodeOptions):
    """Execute a query using Claude Code SDK."""
    if not is_sdk_available():
        raise ImportError("Claude Code SDK is required but not available")
    
    async for message in query(prompt=prompt, options=options):
        yield message


# Export all necessary classes and functions
__all__ = [
    'query', 'ClaudeCodeOptions', 'AssistantMessage', 'UserMessage', 'SystemMessage',
    'ResultMessage', 'TextBlock', 'ToolUseBlock', 'ToolResultBlock',
    'ClaudeSDKError', 'CLINotFoundError', 'CLIConnectionError', 'ProcessError',
    'CLIJSONDecodeError', 'is_sdk_available', 'create_claude_options', 
    'execute_claude_query', 'SDK_AVAILABLE', 'apply_nested_asyncio'
]