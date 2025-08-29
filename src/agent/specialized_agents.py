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
import os
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
        logging.info(f"ProjectManager analyzing task: {main_task}")
        
        try:
            # First, check if Claude SDK is available
            from claude_sdk_interface import is_sdk_available
            if not is_sdk_available():
                logging.error("Claude Code SDK not available for task analysis")
                # Create a simple fallback task assignment
                return self._create_fallback_task(main_task)
            
            analysis_prompt = f"""
You are a project manager for a software development team. Analyze the following project task and split it into specific, actionable subtasks to be assigned to coding agents.

Main task: {main_task}

Please output ONLY a JSON response in the following format:
{{
  "subtasks": [
    {{
      "id": "task_1",
      "description": "Specific task description with clear deliverables",
      "assigned_to": "frontend_coder|backend_coder|devops_coder",
      "priority": 1,
      "estimated_duration": 30,
      "tools_needed": ["Write", "Edit"],
      "dependencies": []
    }}
  ]
}}

Guidelines:
- Create specific, actionable tasks with clear deliverables  
- Assign tasks to the most appropriate agent type
- For Python/Flask/API tasks: assign to backend_coder
- For React/Vue/HTML/CSS tasks: assign to frontend_coder
- For Docker/CI/CD/deployment tasks: assign to devops_coder
- Include tools needed: Write, Edit, Read, Bash, Glob, Grep
- Ensure tasks create actual files in the output directory
"""
            
            response_parts = []
            logging.info("Sending task analysis request to Claude Code SDK...")
            
            try:
                async for msg in execute_claude_query(analysis_prompt, self.options):
                    if isinstance(msg, AssistantMessage):
                        for block in msg.content:
                            if isinstance(block, TextBlock):
                                response_parts.append(block.text)
                                logging.debug(f"Received response block: {block.text[:100]}...")
                    elif isinstance(msg, ResultMessage):
                        logging.info("Received ResultMessage, ending query")
                        break
            except Exception as e:
                logging.error(f"Claude Code SDK query failed: {e}")
                return self._create_fallback_task(main_task)
            
            # Parse response and create tasks
            response_text = "\n".join(response_parts)
            logging.info(f"Full response text: {response_text}")
            
            if not response_text.strip():
                logging.error("Empty response from Claude Code SDK")
                return self._create_fallback_task(main_task)
            
            # Try to extract JSON - look for the most complete JSON block
            import re
            json_matches = re.findall(r'\{[^}]*"subtasks"[^}]*\[.*?\]\s*\}', response_text, re.DOTALL)
            
            if not json_matches:
                # Fallback: simple JSON extraction
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_text = response_text[json_start:json_end]
                else:
                    logging.error("No JSON found in response")
                    return self._create_fallback_task(main_task)
            else:
                json_text = json_matches[0]
            
            logging.info(f"Extracted JSON: {json_text}")
            
            try:
                task_data = json.loads(json_text)
                tasks = []
                
                for subtask in task_data.get("subtasks", []):
                    task = Task(
                        id=subtask.get("id", f"task_{len(tasks)+1}"),
                        description=subtask.get("description", ""),
                        assigned_to=subtask.get("assigned_to", "backend_coder"),
                        priority=subtask.get("priority", 1),
                        estimated_duration=subtask.get("estimated_duration", 30),
                        tools_needed=subtask.get("tools_needed", ["Write", "Edit"]),
                        dependencies=subtask.get("dependencies", [])
                    )
                    tasks.append(task)
                    logging.info(f"Created subtask: {task.id} -> {task.assigned_to}: {task.description[:50]}...")
                
                if not tasks:
                    logging.warning("No subtasks created from response, using fallback")
                    return self._create_fallback_task(main_task)
                    
                return tasks
                    
            except json.JSONDecodeError as e:
                logging.error(f"JSON parsing failed: {e}")
                logging.error(f"Attempted to parse: {json_text}")
                return self._create_fallback_task(main_task)
                
        except Exception as e:
            logging.error(f"Task analysis failed with exception: {e}")
            import traceback
            traceback.print_exc()
            return self._create_fallback_task(main_task)
    
    def _create_fallback_task(self, main_task: str) -> List[Task]:
        """Create a simple fallback task when analysis fails."""
        logging.info("Creating fallback task assignment")
        
        # Determine the most appropriate agent based on task content
        task_lower = main_task.lower()
        if any(word in task_lower for word in ['react', 'vue', 'html', 'css', 'frontend', 'ui', 'component']):
            assigned_to = "frontend_coder"
        elif any(word in task_lower for word in ['docker', 'deploy', 'ci', 'cd', 'kubernetes', 'devops']):
            assigned_to = "devops_coder" 
        else:
            assigned_to = "backend_coder"
        
        fallback_task = Task(
            id="fallback_task_1",
            description=main_task,
            assigned_to=assigned_to,
            priority=1,
            estimated_duration=30,
            tools_needed=["Write", "Edit", "Read"],
            dependencies=[]
        )
        
        logging.info(f"Created fallback task assigned to {assigned_to}")
        return [fallback_task]
    
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
        
        # Set output directory based on current working directory
        current_dir = os.getcwd()
        if 'src/agent' in current_dir:
            self.output_directory = "../../output"  # From src/agent
        else:
            # Find the project root and set output directory
            project_root = current_dir
            while not os.path.exists(os.path.join(project_root, 'src')):
                parent = os.path.dirname(project_root)
                if parent == project_root:  # Reached filesystem root
                    break
                project_root = parent
            self.output_directory = os.path.join(project_root, "output")
        
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
    
    async def execute_coding_task(self, task_description: str) -> Dict[str, Any]:
        """Execute a coding task using Claude Code SDK."""
        logging.info(f"{self.agent_id} executing coding task: {task_description}")
        
        try:
            from claude_sdk_interface import is_sdk_available
            if not is_sdk_available():
                logging.error("Claude Code SDK not available for task execution")
                return {
                    "task_description": task_description,
                    "agent_id": self.agent_id,
                    "specialization": self.specialization,
                    "error": "Claude Code SDK not available",
                    "created_files": [],
                    "timestamp": datetime.now().isoformat()
                }
            
            # Get list of files before execution
            output_dir = "../../output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logging.info(f"Created output directory: {output_dir}")
            
            files_before = set()
            try:
                files_before = set(os.listdir(output_dir))
            except Exception as e:
                logging.warning(f"Could not list output directory: {e}")
            
            coding_prompt = f"""
You are an expert {self.specialization} developer. Execute the following coding task:

{task_description}

IMPORTANT REQUIREMENTS:
1. You MUST use the Write tool to create files in the ../../output directory
2. Create functional, well-documented code with appropriate file extensions
3. For Python files: use .py extension
4. For web files: use .html, .css, .js extensions
5. For config files: use appropriate extensions (.json, .txt, .yml, etc.)
6. Test your code if possible using available tools

Example file paths:
- ../../output/calculator.py
- ../../output/app.py
- ../../output/Counter.js
- ../../output/Counter.css
- ../../output/package.json
- ../../output/requirements.txt

Focus on creating high-quality, production-ready code that fulfills the requirements.
REMEMBER: Use the Write tool to actually create the files!
"""
            
            response_parts = []
            logging.info("Sending coding task to Claude Code SDK...")
            
            try:
                async for msg in execute_claude_query(coding_prompt, self.options):
                    if isinstance(msg, AssistantMessage):
                        for block in msg.content:
                            if isinstance(block, TextBlock):
                                response_parts.append(block.text)
                                logging.debug(f"Received response: {block.text[:100]}...")
                    elif isinstance(msg, ResultMessage):
                        logging.info("Received ResultMessage, task execution complete")
                        break
            except Exception as e:
                logging.error(f"Claude Code SDK execution failed: {e}")
                return {
                    "task_description": task_description,
                    "agent_id": self.agent_id,
                    "specialization": self.specialization,
                    "error": f"SDK execution failed: {e}",
                    "created_files": [],
                    "timestamp": datetime.now().isoformat()
                }
            
            response_text = "\n".join(response_parts)
            
            # Check for created files
            created_files = []
            try:
                files_after = set(os.listdir(output_dir))
                created_files = list(files_after - files_before)
                logging.info(f"Files created: {created_files}")
            except Exception as e:
                logging.warning(f"Could not check created files: {e}")
            
            result = {
                "task_description": task_description,
                "agent_id": self.agent_id,
                "specialization": self.specialization,
                "response": response_text,
                "created_files": created_files,
                "timestamp": datetime.now().isoformat()
            }
            
            if not created_files:
                logging.warning(f"No files were created by {self.agent_id} for task")
                result["warning"] = "No files were created - Claude Code SDK may not have executed tools"
            
            # Mark task as completed
            self.completed_tasks += 1
            
            return result
            
        except Exception as e:
            logging.error(f"Coding task execution failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                "task_description": task_description,
                "agent_id": self.agent_id,
                "specialization": self.specialization,
                "error": str(e),
                "created_files": [],
                "timestamp": datetime.now().isoformat()
            }
    
    async def _execute_task(self, task):
        """Override base class to execute coding-specific tasks."""
        try:
            try:
                from .models import TaskStatus
            except ImportError:
                from models import TaskStatus
            
            task.status = TaskStatus.IN_PROGRESS
            logging.info(f"{self.agent_id} starting coding task: {task.description[:50]}...")
            
            # Execute the coding task and create actual files
            result = await self.execute_coding_task(task.description)
            
            # Store the result with created files information
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            self.completed_tasks += 1
            
            # Store result in agent's recent results for system coordinator to access
            if not hasattr(self, 'recent_task_results'):
                self.recent_task_results = []
            self.recent_task_results.append(result)
            
            # Keep only the most recent 10 results
            if len(self.recent_task_results) > 10:
                self.recent_task_results = self.recent_task_results[-10:]
            
            # Remove from task list
            if task in self.current_tasks:
                self.current_tasks.remove(task)
            
            logging.info(f"{self.agent_id} completed coding task")
            
        except Exception as e:
            logging.error(f"{self.agent_id} task execution failed: {e}")
            task.status = TaskStatus.FAILED
            task.result = {"error": str(e), "created_files": []}


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
