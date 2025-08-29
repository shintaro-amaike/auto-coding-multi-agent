#!/usr/bin/env python3
"""
Base autonomous agent implementation.

This module contains the core AutonomousAgent class that all
specialized agents inherit from.
"""

import asyncio
import logging
import queue
from datetime import datetime
from typing import Dict, List, Optional, Any

try:
    from .models import AgentRole, Task, Message, AgentMessage, AgentStatus, TaskStatus
    from .claude_sdk_interface import (
        execute_claude_query, create_claude_options, is_sdk_available,
        AssistantMessage, TextBlock, ResultMessage
    )
except ImportError:
    from models import AgentRole, Task, Message, AgentMessage, AgentStatus, TaskStatus
    from claude_sdk_interface import (
        execute_claude_query, create_claude_options, is_sdk_available,
        AssistantMessage, TextBlock, ResultMessage
    )


class AutonomousAgent:
    """Base class for autonomous agents using Claude Code SDK."""
    
    def __init__(self, agent_id: str, role: AgentRole, system_prompt: str):
        """Initialize the autonomous agent."""
        self.agent_id = agent_id
        self.role = role
        self.system_prompt = system_prompt
        self.conversation_history: List[Message] = []
        self.completed_tasks = 0
        self.current_tasks: List[Task] = []
        self.message_queue: queue.Queue = queue.Queue()
        self.is_running = False
        self.task_results: Dict[str, Any] = {}
        
        # Agent-specific configuration
        self.options = self._get_agent_options()
    
    def _get_agent_options(self):
        """Configure options based on agent role."""
        try:
            from .models import AgentTools
        except ImportError:
            from models import AgentTools
        
        base_tools = AgentTools.BASE_TOOLS
        
        if self.role == AgentRole.PROJECT_MANAGER:
            tools = AgentTools.PROJECT_MANAGER_TOOLS
        elif self.role in [AgentRole.FRONTEND_CODER, AgentRole.BACKEND_CODER]:
            tools = AgentTools.CODING_AGENT_TOOLS
        else:  # DEVOPS_CODER
            tools = AgentTools.DEVOPS_AGENT_TOOLS
            
        return create_claude_options(
            allowed_tools=tools,
            system_prompt=self.system_prompt,
            max_turns=10,
            permission_mode='acceptEdits'
        )
    
    async def start(self):
        """Start the agent."""
        if not is_sdk_available():
            logging.warning(f"{self.agent_id} starting in fallback mode (Claude Code SDK not available)")
        else:
            logging.info(f"{self.agent_id} starting with Claude Code SDK")
            
        self.is_running = True
        
        # Start message processing in background
        asyncio.create_task(self._run_autonomous_loop())
        
        logging.info(f"{self.agent_id} agent started")
    
    async def stop(self):
        """Stop the agent."""
        self.is_running = False
        logging.info(f"{self.agent_id} agent stopped")
    
    async def send_message_to_agent(self, message: AgentMessage):
        """Send message to another agent."""
        self.message_queue.put(message)
    
    async def _run_autonomous_loop(self):
        """Autonomous execution loop."""
        while self.is_running:
            try:
                # Check message queue
                if not self.message_queue.empty():
                    message = self.message_queue.get_nowait()
                    await self._process_agent_message(message)
                
                # Process current tasks
                for task in self.current_tasks[:]:
                    if task.status == TaskStatus.PENDING:
                        await self._execute_task(task)
                
                # Short wait
                await asyncio.sleep(1.0)
                
            except Exception as e:
                logging.error(f"Error in {self.agent_id} autonomous loop: {e}")
                await asyncio.sleep(5.0)
    
    async def _process_agent_message(self, message: AgentMessage):
        """Process message from another agent."""
        try:
            from .models import MessageType
        except ImportError:
            from models import MessageType
        
        if message.message_type == MessageType.TASK_REQUEST:
            task = Task(
                id=f"{self.agent_id}_{datetime.now().timestamp()}",
                description=message.content,
                assigned_to=self.agent_id,
                tools_needed=message.metadata.get("tools_needed", []),
                priority=message.metadata.get("priority", 1)
            )
            self.current_tasks.append(task)
            logging.info(f"{self.agent_id} received new task: {task.description[:50]}...")
    
    async def _execute_task(self, task: Task):
        """Execute a task."""
        try:
            task.status = TaskStatus.IN_PROGRESS
            logging.info(f"{self.agent_id} starting task: {task.description[:50]}...")
            
            # Execute task with Claude Code SDK
            prompt = self._build_task_prompt(task)
            
            # Collect responses
            result_parts = []
            async for msg in execute_claude_query(prompt, self.options):
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            result_parts.append(block.text)
                elif isinstance(msg, ResultMessage):
                    break
            
            task.result = "\n".join(result_parts) if result_parts else "Task completed"
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            self.completed_tasks += 1
            
            # Remove from task list
            self.current_tasks.remove(task)
            
            logging.info(f"{self.agent_id} completed task: {task.description[:50]}...")
            
            # Save results
            self.task_results[task.id] = {
                "task": task,
                "result": task.result,
                "completion_time": task.completed_at
            }
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.result = f"Error: {str(e)}"
            logging.error(f"Error executing task in {self.agent_id}: {e}")
    
    def _build_task_prompt(self, task: Task) -> str:
        """Build the prompt for task execution."""
        return f"""
As a {self.role.value}, please execute the following task:

Task: {task.description}

Use the following tools as needed:
- File operations (Read, Write, Edit)
- Command execution (Bash)
- File search (Glob, Grep)

Please report the execution results in detail.
"""
    
    def get_status(self) -> AgentStatus:
        """Get current agent status."""
        # Get recent results from different sources depending on agent type
        recent_results = []
        if hasattr(self, 'recent_task_results') and self.recent_task_results:
            recent_results = self.recent_task_results[-5:]  # Get last 5 results
        else:
            recent_results = list(self.task_results.keys())[-5:] if self.task_results else []
        
        return AgentStatus(
            agent_id=self.agent_id,
            role=self.role.value,
            is_running=self.is_running,
            completed_tasks=self.completed_tasks,
            current_tasks_count=len(self.current_tasks),
            pending_messages=self.message_queue.qsize(),
            recent_results=recent_results,
            message_history_length=len(self.conversation_history)
        )
    
    def add_conversation_message(self, message: Message):
        """Add a message to the conversation history."""
        self.conversation_history.append(message)
    
    def get_conversation_history(self) -> List[Message]:
        """Get the conversation history."""
        return self.conversation_history.copy()
    
    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history.clear()