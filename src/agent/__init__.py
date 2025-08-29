#!/usr/bin/env python3
"""
Multi-Agent System Package.

This package provides a modular autonomous multi-agent system with Claude Code SDK support.
"""

from .models import (
    AgentRole, Message, Task, AgentMessage, SystemStatus, AgentStatus,
    TaskStatus, MessageType, AgentTools, AgentPrompts
)

from .claude_sdk_interface import (
    query, ClaudeCodeOptions, AssistantMessage, UserMessage, SystemMessage,
    ResultMessage, TextBlock, ToolUseBlock, ToolResultBlock,
    ClaudeSDKError, CLINotFoundError, CLIConnectionError, ProcessError,
    CLIJSONDecodeError, is_sdk_available, create_claude_options, 
    execute_claude_query, SDK_AVAILABLE, apply_nested_asyncio
)

from .base_agent import AutonomousAgent

from .specialized_agents import (
    ProjectManagerAgent, CodingAgent, FrontendCodingAgent,
    BackendCodingAgent, DevOpsCodingAgent, create_agent_by_role,
    get_available_agent_roles, get_agent_description
)

from .system_coordinator import AutonomousMultiAgentSystem

from .utils import (
    init_autonomous_system, quick_task_examples, get_system_info,
    setup_logging, TaskBuilder, get_example_tasks
)

__version__ = "1.0.0"
__author__ = "Multi-Agent System Team"
__description__ = "Autonomous Multi-Agent System with Claude Code SDK Support"

__all__ = [
    # Models
    "AgentRole", "Message", "Task", "AgentMessage", "SystemStatus", "AgentStatus",
    "TaskStatus", "MessageType", "AgentTools", "AgentPrompts",
    
    # Claude SDK Interface
    "query", "ClaudeCodeOptions", "AssistantMessage", "UserMessage", "SystemMessage",
    "ResultMessage", "TextBlock", "ToolUseBlock", "ToolResultBlock",
    "ClaudeSDKError", "CLINotFoundError", "CLIConnectionError", "ProcessError",
    "CLIJSONDecodeError", "is_sdk_available", "create_claude_options", 
    "execute_claude_query", "SDK_AVAILABLE", "apply_nested_asyncio",
    
    # Agents
    "AutonomousAgent", "ProjectManagerAgent", "CodingAgent", "FrontendCodingAgent",
    "BackendCodingAgent", "DevOpsCodingAgent", "create_agent_by_role",
    "get_available_agent_roles", "get_agent_description",
    
    # System Coordinator
    "AutonomousMultiAgentSystem",
    
    # Utils
    "init_autonomous_system", "quick_task_examples", "get_system_info",
    "setup_logging", "TaskBuilder", "get_example_tasks"
]