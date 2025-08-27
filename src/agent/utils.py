#!/usr/bin/env python3
"""
Utility functions and helper classes for the multi-agent system.

This module contains common utility functions, initialization helpers,
and demo/example functions used throughout the system.
"""

import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime

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
        "required_packages": ["claude-code-sdk", "nest-asyncio"],
        "supported_agents": ["project_manager", "frontend_coder", "backend_coder", "devops_coder"],
        "features": [
            "Autonomous task execution",
            "Multi-agent coordination",
            "Real-time progress monitoring", 
            "Structured task creation",
            "Performance metrics"
        ]
    }


def setup_logging(level: str = "INFO", format_string: str = None) -> None:
    """Setup logging configuration."""
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=log_level, format=format_string)


class SystemMonitor:
    """System monitoring and metrics collection."""
    
    def __init__(self, system: AutonomousMultiAgentSystem):
        """Initialize system monitor."""
        self.system = system
        self.metrics_history: List[Dict[str, Any]] = []
        self.start_time = datetime.now()
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics."""
        status = self.system.get_system_status()
        performance = self.system.get_performance_metrics()
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "system_status": status.__dict__,
            "performance_metrics": performance
        }
        
        self.metrics_history.append(metrics)
        return metrics
    
    def get_metrics_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get metrics history."""
        return self.metrics_history[-limit:] if len(self.metrics_history) > limit else self.metrics_history
    
    def get_average_performance(self) -> Dict[str, float]:
        """Get average performance metrics."""
        if not self.metrics_history:
            return {}
        
        total_completion_rate = sum(
            m["performance_metrics"]["overall_completion_rate"] 
            for m in self.metrics_history
        )
        
        return {
            "average_completion_rate": total_completion_rate / len(self.metrics_history),
            "total_samples": len(self.metrics_history),
            "monitoring_duration_hours": (datetime.now() - self.start_time).total_seconds() / 3600
        }


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


def create_web_app_task() -> str:
    """Create a sample web application task."""
    return (TaskBuilder()
            .set_objective("Develop a full-stack web application")
            .add_requirements([
                "User authentication system",
                "Database integration",
                "Responsive design",
                "RESTful API"
            ])
            .add_constraints([
                "Use modern frameworks",
                "Follow security best practices",
                "Complete within reasonable time"
            ])
            .add_deliverables([
                "Working web application",
                "API documentation", 
                "Test suite",
                "Deployment guide"
            ])
            .build())


def create_ml_pipeline_task() -> str:
    """Create a sample ML pipeline task."""
    return (TaskBuilder()
            .set_objective("Build machine learning pipeline and dashboard")
            .add_requirements([
                "Data preprocessing capabilities",
                "Multiple ML algorithms",
                "Model evaluation framework",
                "Interactive dashboard",
                "Real-time predictions"
            ])
            .add_constraints([
                "Python-based implementation", 
                "Use scikit-learn and common libraries",
                "Docker deployment ready"
            ])
            .add_deliverables([
                "Data preprocessing pipeline",
                "Trained ML models",
                "Web dashboard",
                "API server",
                "Documentation"
            ])
            .build())


async def demo_autonomous_system():
    """Demo execution of autonomous system."""
    try:
        # Initialize system
        system = await init_autonomous_system()
        
        # Start system
        await system.start_system()
        
        # Display initial status
        system.display_system_dashboard()
        
        # Execute sample project
        sample_task = "Create a simple React counter app with component separation and state management"
        
        print(f"\n🚀 Starting sample project: {sample_task}")
        
        await system.submit_project_task(sample_task)
        
        # Run system for 30 seconds
        for i in range(6):
            await asyncio.sleep(5)
            print(f"\n🔄 System status update ({(i+1)*5} seconds elapsed)")
            system.display_system_dashboard()
        
        # Stop system
        await system.stop_system()
        
        print("✅ Demo execution completed")
        
    except Exception as e:
        print(f"❌ Error during demo execution: {e}")
        import traceback
        traceback.print_exc()


def validate_system_requirements() -> Dict[str, bool]:
    """Validate system requirements."""
    requirements = {
        "claude_code_sdk": is_sdk_available(),
        "asyncio_support": True,  # Always available in Python 3.7+
        "logging_support": True   # Always available
    }
    
    return requirements


def print_system_requirements():
    """Print system requirements and status."""
    print("🔍 System Requirements Check:")
    print("=" * 40)
    
    requirements = validate_system_requirements()
    
    for req, available in requirements.items():
        status = "✅" if available else "❌"
        print(f"{status} {req}: {'Available' if available else 'Not Available'}")
    
    if not all(requirements.values()):
        print("\n⚠️ Some requirements are missing. Please install:")
        if not requirements["claude_code_sdk"]:
            print("  pip install claude-code-sdk")
    else:
        print("\n✅ All requirements satisfied!")


def get_example_tasks() -> Dict[str, str]:
    """Get example tasks for different categories."""
    return {
        "web_application": create_web_app_task(),
        "ml_pipeline": create_ml_pipeline_task(),
        "simple_examples": quick_task_examples()
    }


class ProgressTracker:
    """Track progress of multi-phase projects."""
    
    def __init__(self):
        """Initialize progress tracker."""
        self.phases = []
        self.current_phase = 0
        self.start_time = None
        self.phase_start_time = None
    
    def add_phase(self, name: str, description: str, estimated_duration: int = 30):
        """Add a phase to track."""
        self.phases.append({
            "name": name,
            "description": description,
            "estimated_duration": estimated_duration,
            "status": "pending",
            "start_time": None,
            "end_time": None,
            "actual_duration": None
        })
    
    def start_tracking(self):
        """Start progress tracking."""
        self.start_time = datetime.now()
        if self.phases:
            self.start_phase(0)
    
    def start_phase(self, phase_index: int):
        """Start a specific phase."""
        if 0 <= phase_index < len(self.phases):
            self.current_phase = phase_index
            self.phases[phase_index]["status"] = "in_progress"
            self.phases[phase_index]["start_time"] = datetime.now()
            self.phase_start_time = datetime.now()
    
    def complete_phase(self, phase_index: int = None):
        """Complete a phase."""
        if phase_index is None:
            phase_index = self.current_phase
        
        if 0 <= phase_index < len(self.phases):
            phase = self.phases[phase_index]
            phase["status"] = "completed"
            phase["end_time"] = datetime.now()
            
            if phase["start_time"]:
                duration = (phase["end_time"] - phase["start_time"]).total_seconds() / 60
                phase["actual_duration"] = round(duration, 2)
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get progress summary."""
        completed = sum(1 for p in self.phases if p["status"] == "completed")
        in_progress = sum(1 for p in self.phases if p["status"] == "in_progress")
        pending = sum(1 for p in self.phases if p["status"] == "pending")
        
        total_time = 0
        if self.start_time:
            total_time = (datetime.now() - self.start_time).total_seconds() / 60
        
        return {
            "total_phases": len(self.phases),
            "completed_phases": completed,
            "in_progress_phases": in_progress,
            "pending_phases": pending,
            "completion_percentage": (completed / len(self.phases) * 100) if self.phases else 0,
            "total_time_minutes": round(total_time, 2),
            "phases": self.phases
        }