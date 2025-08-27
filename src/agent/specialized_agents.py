#!/usr/bin/env python3
"""
Specialized agent implementations.

This module contains the specific agent classes for different roles:
- ProjectManagerAgent
- CodingAgent (base for coding agents)
- FrontendCodingAgent
- BackendCodingAgent  
- DevOpsCodingAgent
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any

try:
    from .models import AgentRole, Task, AgentPrompts
    from .base_agent import AutonomousAgent
    from .claude_sdk_interface import (
        execute_claude_query, AssistantMessage, TextBlock, ResultMessage
    )
except ImportError:
    from models import AgentRole, Task, AgentPrompts
    from base_agent import AutonomousAgent
    from claude_sdk_interface import (
        execute_claude_query, AssistantMessage, TextBlock, ResultMessage
    )


class ProjectManagerAgent(AutonomousAgent):
    """Project manager agent - task distribution and progress management."""
    
    def __init__(self):
        """Initialize the project manager agent."""
        super().__init__(
            "project_manager", 
            AgentRole.PROJECT_MANAGER, 
            AgentPrompts.PROJECT_MANAGER
        )
        self.coding_agents: List[str] = ["frontend_coder", "backend_coder", "devops_coder"]
        self.project_status: Dict[str, Any] = {"active_tasks": {}, "completed_tasks": {}}
    
    async def analyze_and_delegate_task(self, main_task: str) -> List[Task]:
        """Analyze main task and split into subtasks."""
        analysis_prompt = f"""
Analyze the following project task and split it into subtasks to be assigned to three coding agents: frontend_coder, backend_coder, and devops_coder.

Main task: {main_task}

Please output in the following JSON format:
{{
  "subtasks": [
    {{
      "id": "task_1",
      "description": "Task description",
      "assigned_to": "frontend_coder|backend_coder|devops_coder",
      "priority": 1,
      "estimated_duration": 30,
      "tools_needed": ["Read", "Write", "Edit"],
      "dependencies": []
    }}
  ]
}}
"""
        
        response_parts = []
        async for msg in execute_claude_query(analysis_prompt, self.options):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        response_parts.append(block.text)
            elif isinstance(msg, ResultMessage):
                break
        
        # Parse JSON to create tasks
        tasks = []
        try:
            response_text = "\n".join(response_parts)
            # Extract JSON portion
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_text = response_text[json_start:json_end]
                task_data = json.loads(json_text)
                
                for subtask in task_data.get("subtasks", []):
                    task = Task(
                        id=subtask["id"],
                        description=subtask["description"],
                        assigned_to=subtask["assigned_to"],
                        priority=subtask.get("priority", 1),
                        estimated_duration=subtask.get("estimated_duration", 30),
                        tools_needed=subtask.get("tools_needed", []),
                        dependencies=subtask.get("dependencies", [])
                    )
                    tasks.append(task)
        except Exception as e:
            logging.error(f"Task analysis error: {e}")
        
        return tasks
    
    def get_project_status(self) -> Dict[str, Any]:
        """Get current project status."""
        return {
            **self.project_status,
            "agent_status": self.get_status().__dict__,
            "coding_agents": self.coding_agents
        }
    
    def update_project_status(self, task_id: str, status: str, result: Any = None):
        """Update project status for a task."""
        if status == "completed":
            self.project_status["completed_tasks"][task_id] = {
                "completion_time": datetime.now().isoformat(),
                "result": result
            }
            if task_id in self.project_status["active_tasks"]:
                del self.project_status["active_tasks"][task_id]
        else:
            self.project_status["active_tasks"][task_id] = {
                "status": status,
                "last_updated": datetime.now().isoformat()
            }


class CodingAgent(AutonomousAgent):
    """Base class for coding agents."""
    
    def __init__(self, agent_id: str, role: AgentRole, specialization: str):
        """Initialize the coding agent."""
        system_prompt = f"""You are an expert in {specialization}.
        Perform code design, implementation, and debugging. Follow best practices
        and write maintainable code. Actively use file operations, command execution,
        and code editing tools."""
        
        super().__init__(agent_id, role, system_prompt)
        self.specialization = specialization
        self.current_project_path = "/workspace"  # Default working directory
        
    def set_project_path(self, path: str):
        """Set the current project working directory."""
        self.current_project_path = path
        
    def get_specialization_info(self) -> Dict[str, Any]:
        """Get information about this agent's specialization."""
        return {
            "specialization": self.specialization,
            "role": self.role.value,
            "project_path": self.current_project_path,
            "tools_available": self.options.allowed_tools
        }


class FrontendCodingAgent(CodingAgent):
    """Frontend development agent."""
    
    def __init__(self):
        """Initialize the frontend coding agent."""
        super().__init__(
            "frontend_coder", 
            AgentRole.FRONTEND_CODER, 
            "React, Vue.js, Angular and other frontend technologies"
        )
        
        # Frontend-specific configurations
        self.preferred_frameworks = ["React", "Vue.js", "Angular", "Svelte"]
        self.ui_libraries = ["Bootstrap", "Tailwind CSS", "Material-UI", "Ant Design"]
        
    def get_frontend_capabilities(self) -> Dict[str, Any]:
        """Get frontend-specific capabilities."""
        return {
            **self.get_specialization_info(),
            "preferred_frameworks": self.preferred_frameworks,
            "ui_libraries": self.ui_libraries,
            "specialties": [
                "Responsive design",
                "Component architecture", 
                "State management",
                "Performance optimization",
                "Accessibility (a11y)"
            ]
        }


class BackendCodingAgent(CodingAgent):
    """Backend development agent."""
    
    def __init__(self):
        """Initialize the backend coding agent."""
        super().__init__(
            "backend_coder", 
            AgentRole.BACKEND_CODER,
            "Python, Node.js, Java and other backend technologies"
        )
        
        # Backend-specific configurations
        self.preferred_languages = ["Python", "Node.js", "Java", "Go"]
        self.frameworks = ["FastAPI", "Django", "Express.js", "Spring Boot"]
        self.databases = ["PostgreSQL", "MySQL", "MongoDB", "Redis"]
        
    def get_backend_capabilities(self) -> Dict[str, Any]:
        """Get backend-specific capabilities."""
        return {
            **self.get_specialization_info(),
            "preferred_languages": self.preferred_languages,
            "frameworks": self.frameworks,
            "databases": self.databases,
            "specialties": [
                "API design and development",
                "Database design and optimization",
                "Authentication and authorization",
                "Microservices architecture",
                "Performance tuning"
            ]
        }


class DevOpsCodingAgent(CodingAgent):
    """Infrastructure and DevOps agent."""
    
    def __init__(self):
        """Initialize the DevOps coding agent."""
        super().__init__(
            "devops_coder", 
            AgentRole.DEVOPS_CODER,
            "Docker, Kubernetes, CI/CD and other infrastructure/DevOps technologies"
        )
        
        # DevOps-specific configurations
        self.container_technologies = ["Docker", "Podman", "containerd"]
        self.orchestration_tools = ["Kubernetes", "Docker Swarm", "Nomad"]
        self.ci_cd_tools = ["GitHub Actions", "GitLab CI", "Jenkins", "CircleCI"]
        self.cloud_platforms = ["AWS", "Google Cloud", "Azure", "DigitalOcean"]
        
    def get_devops_capabilities(self) -> Dict[str, Any]:
        """Get DevOps-specific capabilities."""
        return {
            **self.get_specialization_info(),
            "container_technologies": self.container_technologies,
            "orchestration_tools": self.orchestration_tools,
            "ci_cd_tools": self.ci_cd_tools,
            "cloud_platforms": self.cloud_platforms,
            "specialties": [
                "Infrastructure as Code",
                "Containerization and orchestration",
                "CI/CD pipeline design",
                "Monitoring and logging",
                "Security and compliance",
                "Performance monitoring"
            ]
        }


def create_agent_by_role(role: AgentRole) -> AutonomousAgent:
    """Factory function to create agents by role."""
    if role == AgentRole.PROJECT_MANAGER:
        return ProjectManagerAgent()
    elif role == AgentRole.FRONTEND_CODER:
        return FrontendCodingAgent()
    elif role == AgentRole.BACKEND_CODER:
        return BackendCodingAgent()
    elif role == AgentRole.DEVOPS_CODER:
        return DevOpsCodingAgent()
    else:
        raise ValueError(f"Unknown agent role: {role}")


def get_available_agent_roles() -> List[str]:
    """Get list of available agent roles."""
    return [role.value for role in AgentRole]


def get_agent_description(role: AgentRole) -> str:
    """Get description for an agent role."""
    descriptions = {
        AgentRole.PROJECT_MANAGER: "Project management and task distribution",
        AgentRole.FRONTEND_CODER: "React, Vue.js frontend development",
        AgentRole.BACKEND_CODER: "Python, Node.js backend development", 
        AgentRole.DEVOPS_CODER: "Docker, CI/CD infrastructure"
    }
    return descriptions.get(role, "Unknown agent role")