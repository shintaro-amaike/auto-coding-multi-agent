#!/usr/bin/env python3
"""
Data models and base classes for the autonomous multi-agent system.

This module contains all the data structures, enums, and base classes
used throughout the multi-agent system.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class AgentRole(Enum):
    """Enum defining the different types of agents in the system."""
    PROJECT_MANAGER = "project_manager"
    FRONTEND_CODER = "frontend_coder"
    BACKEND_CODER = "backend_coder"
    DEVOPS_CODER = "devops_coder"


@dataclass
class Message:
    """Base message class for agent communications."""
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    agent_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """Represents a task that can be assigned to an agent."""
    id: str
    description: str
    assigned_to: str
    status: str = "pending"  # pending, in_progress, completed, failed
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    priority: int = 1
    parent_task_id: Optional[str] = None
    subtasks: List[str] = field(default_factory=list)
    tools_needed: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: Optional[int] = None  # minutes


@dataclass
class AgentMessage:
    """Message passed between agents for coordination."""
    sender_id: str
    receiver_id: str
    message_type: str  # task_request, task_result, status_update, coordination
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemStatus:
    """Represents the overall system status."""
    system_running: bool
    total_agents: int
    total_completed_tasks: int
    total_active_tasks: int
    pending_projects: int
    completed_projects: int
    agent_details: Dict[str, Any]
    timestamp: str


@dataclass
class AgentStatus:
    """Represents the status of a single agent."""
    agent_id: str
    role: str
    is_running: bool
    completed_tasks: int
    current_tasks_count: int
    pending_messages: int
    recent_results: List[str]
    message_history_length: Optional[int] = None


class TaskStatus:
    """Constants for task status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class MessageType:
    """Constants for message types between agents."""
    TASK_REQUEST = "task_request"
    TASK_RESULT = "task_result"
    STATUS_UPDATE = "status_update"
    COORDINATION = "coordination"


class AgentTools:
    """Constants for available tools per agent type."""
    BASE_TOOLS = ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
    
    PROJECT_MANAGER_TOOLS = BASE_TOOLS + ["WebSearch", "WebFetch"]
    CODING_AGENT_TOOLS = BASE_TOOLS + ["MultiEdit", "NotebookEdit"]
    DEVOPS_AGENT_TOOLS = BASE_TOOLS + ["TodoWrite"]


class AgentPrompts:
    """System prompts for different agent types."""
    
    PROJECT_MANAGER = """You are an experienced project manager.
    Analyze tasks, assign work to appropriate coding agents, and manage overall progress.
    Perform efficient work division and scheduling, and lead the team."""
    
    FRONTEND_CODER = """You are an expert in React, Vue.js, Angular and other frontend technologies.
    Perform code design, implementation, and debugging. Follow best practices
    and write maintainable code. Actively use file operations, command execution,
    and code editing tools."""
    
    BACKEND_CODER = """You are an expert in Python, Node.js, Java and other backend technologies.
    Perform code design, implementation, and debugging. Follow best practices
    and write maintainable code. Actively use file operations, command execution,
    and code editing tools."""
    
    DEVOPS_CODER = """You are an expert in Docker, Kubernetes, CI/CD and other infrastructure/DevOps technologies.
    Perform code design, implementation, and debugging. Follow best practices
    and write maintainable code. Actively use file operations, command execution,
    and code editing tools."""