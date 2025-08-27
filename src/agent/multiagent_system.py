#!/usr/bin/env python3
"""
Autonomous Multi-Agent System with Claude Code SDK Support.

This is the main entry point that imports and re-exports all the modular components.
For backward compatibility, it provides the same interface as the original monolithic file.
"""

# Import all components from the modular structure
import sys
import os

# Try package imports first, fall back to direct imports
try:
    # When imported as a package (from parent directory)
    from . import (
        AgentRole, Message, Task, AgentMessage, SystemStatus, AgentStatus,
        TaskStatus, MessageType, AgentTools, AgentPrompts,
        query, ClaudeCodeOptions, AssistantMessage, UserMessage, SystemMessage,
        ResultMessage, TextBlock, ToolUseBlock, ToolResultBlock,
        ClaudeSDKError, CLINotFoundError, CLIConnectionError, ProcessError,
        CLIJSONDecodeError, is_sdk_available, create_claude_options, 
        execute_claude_query, SDK_AVAILABLE, apply_nested_asyncio,
        AutonomousAgent, ProjectManagerAgent, CodingAgent, FrontendCodingAgent,
        BackendCodingAgent, DevOpsCodingAgent, create_agent_by_role,
        get_available_agent_roles, get_agent_description,
        AutonomousMultiAgentSystem,
        init_autonomous_system, quick_task_examples, get_system_info,
        setup_logging, SystemMonitor, TaskBuilder, create_web_app_task,
        create_ml_pipeline_task, demo_autonomous_system, validate_system_requirements,
        print_system_requirements, get_example_tasks, ProgressTracker
    )
except (ImportError, ValueError):
    # When imported directly from the same directory
    from models import (
        AgentRole, Message, Task, AgentMessage, SystemStatus, AgentStatus,
        TaskStatus, MessageType, AgentTools, AgentPrompts
    )
    from claude_sdk_interface import (
        query, ClaudeCodeOptions, AssistantMessage, UserMessage, SystemMessage,
        ResultMessage, TextBlock, ToolUseBlock, ToolResultBlock,
        ClaudeSDKError, CLINotFoundError, CLIConnectionError, ProcessError,
        CLIJSONDecodeError, is_sdk_available, create_claude_options, 
        execute_claude_query, SDK_AVAILABLE, apply_nested_asyncio
    )
    from base_agent import AutonomousAgent
    from specialized_agents import (
        ProjectManagerAgent, CodingAgent, FrontendCodingAgent,
        BackendCodingAgent, DevOpsCodingAgent, create_agent_by_role,
        get_available_agent_roles, get_agent_description
    )
    from system_coordinator import AutonomousMultiAgentSystem
    from utils import (
        init_autonomous_system, quick_task_examples, get_system_info,
        setup_logging, SystemMonitor, TaskBuilder, create_web_app_task,
        create_ml_pipeline_task, demo_autonomous_system, validate_system_requirements,
        print_system_requirements, get_example_tasks, ProgressTracker
    )

# Apply nested asyncio support for Jupyter environments
apply_nested_asyncio()

# For backward compatibility, expose the main classes at module level
__all__ = [
    # Core classes (backward compatibility)
    'AgentRole', 'Message', 'Task', 'AgentMessage', 'AutonomousAgent',
    'ProjectManagerAgent', 'CodingAgent', 'FrontendCodingAgent',
    'BackendCodingAgent', 'DevOpsCodingAgent', 'AutonomousMultiAgentSystem',
    
    # Claude SDK components
    'query', 'ClaudeCodeOptions', 'AssistantMessage', 'UserMessage', 
    'SystemMessage', 'ResultMessage', 'TextBlock', 'ToolUseBlock', 
    'ToolResultBlock', 'ClaudeSDKError', 'CLINotFoundError', 
    'CLIConnectionError', 'ProcessError', 'CLIJSONDecodeError',
    
    # Utility functions
    'init_autonomous_system', 'quick_task_examples', 'demo_autonomous_system',
    
    # New modular components
    'SystemStatus', 'AgentStatus', 'TaskStatus', 'MessageType', 'AgentTools',
    'AgentPrompts', 'is_sdk_available', 'create_claude_options', 
    'execute_claude_query', 'SDK_AVAILABLE', 'apply_nested_asyncio', 'create_agent_by_role',
    'get_available_agent_roles', 'get_agent_description', 'get_system_info',
    'setup_logging', 'SystemMonitor', 'TaskBuilder', 'create_web_app_task',
    'create_ml_pipeline_task', 'validate_system_requirements',
    'print_system_requirements', 'get_example_tasks', 'ProgressTracker'
]

if __name__ == "__main__":
    # Demo execution
    print("🌆 Claude Code SDK Autonomous Multi-Agent System Demo")
    print("="*60)
    
    if not is_sdk_available():
        print("⚠️ claude_code_sdk package not installed")
        print("Installation command: pip install claude-code-sdk")
        print_system_requirements()
    else:
        import asyncio
        asyncio.run(demo_autonomous_system())