#!/usr/bin/env python3
"""
Utility functions and helper classes for the multi-agent system.

This module contains essential utility functions and initialization helpers.
"""

import asyncio
import logging
from typing import List, Dict, Any

try:
    from .system_coordinator import AutonomousMultiAgentSystem
    from .claude_sdk_interface import is_sdk_available
except ImportError:
    from system_coordinator import AutonomousMultiAgentSystem
    from claude_sdk_interface import is_sdk_available


async def init_autonomous_system() -> AutonomousMultiAgentSystem:
    """Initialize autonomous multi-agent system."""
    try:
        system = AutonomousMultiAgentSystem()
        print("✅ Claude Code SDK autonomous multi-agent system initialized")
        print(f"🔧 Available agents: {list(system.all_agents.keys())}")
        return system
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        raise


def quick_task_examples() -> List[str]:
    """Return quick task examples."""
    return [
        "Create a simple Python calculator app with tests",
        "Design and implement a RESTful API with basic CRUD operations", 
        "Build a data analysis pipeline and visualize CSV data",
        "Create a web application security checklist",
        "Implement a machine learning model performance evaluation framework"
    ]


def get_system_info() -> Dict[str, Any]:
    """Get system information and requirements."""
    return {
        "sdk_available": is_sdk_available(),
        "required_packages": ["claude-code-sdk"],
        "supported_agents": ["project_manager", "frontend_coder", "backend_coder", "devops_coder"],
        "features": [
            "Autonomous task execution",
            "Multi-agent coordination",
            "Real-time progress monitoring", 
            "Structured task creation"
        ]
    }


def setup_logging(level: str = "INFO", format_string: str = None) -> None:
    """Setup logging configuration."""
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=log_level, format=format_string)


class TaskBuilder:
    """Helper class for building structured tasks."""
    
    def __init__(self):
        """Initialize task builder."""
        self.objective = ""
        self.requirements = []
        self.constraints = []
        self.deliverables = []
    
    def set_objective(self, objective: str) -> 'TaskBuilder':
        """Set the main objective."""
        self.objective = objective
        return self
    
    def add_requirement(self, requirement: str) -> 'TaskBuilder':
        """Add a requirement."""
        self.requirements.append(requirement)
        return self
    
    def add_requirements(self, requirements: List[str]) -> 'TaskBuilder':
        """Add multiple requirements."""
        self.requirements.extend(requirements)
        return self
    
    def add_constraint(self, constraint: str) -> 'TaskBuilder':
        """Add a constraint."""
        self.constraints.append(constraint)
        return self
    
    def add_constraints(self, constraints: List[str]) -> 'TaskBuilder':
        """Add multiple constraints."""
        self.constraints.extend(constraints)
        return self
    
    def add_deliverable(self, deliverable: str) -> 'TaskBuilder':
        """Add a deliverable."""
        self.deliverables.append(deliverable)
        return self
    
    def add_deliverables(self, deliverables: List[str]) -> 'TaskBuilder':
        """Add multiple deliverables."""
        self.deliverables.extend(deliverables)
        return self
    
    def build(self) -> str:
        """Build the structured task."""
        task_parts = []
        
        if self.objective:
            task_parts.append(f"Main Objective: {self.objective}")
        
        if self.requirements:
            task_parts.append("Requirements:")
            task_parts.extend([f"- {req}" for req in self.requirements])
        
        if self.constraints:
            task_parts.append("Constraints:")
            task_parts.extend([f"- {constraint}" for constraint in self.constraints])
            
        if self.deliverables:
            task_parts.append("Deliverables:")
            task_parts.extend([f"- {deliverable}" for deliverable in self.deliverables])
        
        return "\n".join(task_parts)
    
    def clear(self) -> 'TaskBuilder':
        """Clear all fields."""
        self.objective = ""
        self.requirements = []
        self.constraints = []
        self.deliverables = []
        return self


def get_example_tasks() -> Dict[str, List[str]]:
    """Get example tasks for different categories."""
    return {
        "simple_examples": quick_task_examples()
    }