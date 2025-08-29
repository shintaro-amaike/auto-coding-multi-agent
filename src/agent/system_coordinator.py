#!/usr/bin/env python3
"""
Multi-agent system coordinator.

This module contains the main AutonomousMultiAgentSystem class that
coordinates all agents and manages the overall system workflow.
"""

import asyncio
import logging
import queue
import time
from datetime import datetime
from typing import Dict, List, Any

try:
    from .models import AgentRole, AgentMessage, SystemStatus, MessageType
    from .specialized_agents import (
        ProjectManagerAgent, FrontendCodingAgent, BackendCodingAgent, 
        DevOpsCodingAgent, create_agent_by_role
    )
    from .claude_sdk_interface import is_sdk_available
except ImportError:
    from models import AgentRole, AgentMessage, SystemStatus, MessageType
    from specialized_agents import (
        ProjectManagerAgent, FrontendCodingAgent, BackendCodingAgent, 
        DevOpsCodingAgent, create_agent_by_role
    )
    from claude_sdk_interface import is_sdk_available


class AutonomousMultiAgentSystem:
    """Autonomous multi-agent system coordinator."""
    
    def __init__(self):
        """Initialize the multi-agent system."""
        if not is_sdk_available():
            logging.warning("⚠️ Claude Code SDK not available. Running in fallback mode.")
            print("⚠️ Claude Code SDK not available. System will run in fallback mode with limited functionality.")
        else:
            logging.info("✅ Claude Code SDK available. Full functionality enabled.")
            
        # Initialize agents
        self.project_manager = ProjectManagerAgent()
        self.coding_agents = {
            "frontend_coder": FrontendCodingAgent(),
            "backend_coder": BackendCodingAgent(),
            "devops_coder": DevOpsCodingAgent()
        }
        self.all_agents = {"project_manager": self.project_manager, **self.coding_agents}
        
        # System state
        self.is_running = False
        self.message_log: List[AgentMessage] = []
        self.global_task_queue: queue.Queue = queue.Queue()
        self.completed_projects: List[Dict[str, Any]] = []
        
        # Logging configuration
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    async def start_system(self):
        """Start the multi-agent system."""
        logging.info("🚀 Starting autonomous multi-agent system...")
        
        self.is_running = True
        
        # Start all agents
        for agent_id, agent in self.all_agents.items():
            await agent.start()
            logging.info(f"✅ {agent_id} agent started")
        
        # Start system monitoring loop
        asyncio.create_task(self._system_monitoring_loop())
        
        logging.info("✨ System started successfully")
    
    async def stop_system(self):
        """Stop the multi-agent system."""
        logging.info("🛑 Stopping system...")
        
        self.is_running = False
        
        # Stop all agents
        for agent_id, agent in self.all_agents.items():
            await agent.stop()
            logging.info(f"⏹️ {agent_id} agent stopped")
        
        logging.info("✅ System stopped successfully")
    
    async def _system_monitoring_loop(self):
        """System monitoring loop."""
        while self.is_running:
            try:
                # Check each agent's status
                system_status = self.get_system_status()
                
                # Process tasks from global task queue
                if not self.global_task_queue.empty():
                    main_task = self.global_task_queue.get_nowait()
                    logging.info(f"🎯 System monitoring loop processing task: {main_task[:50]}...")
                    try:
                        await self._process_main_task(main_task)
                    except Exception as e:
                        logging.error(f"Task processing failed in monitoring loop: {e}")
                        # Add failed project record
                        failed_project = {
                            "task_description": main_task,
                            "start_time": datetime.now().isoformat(),
                            "end_time": datetime.now().isoformat(),
                            "status": "failed",
                            "error": f"Monitoring loop error: {e}",
                            "subtasks": [],
                            "results": [],
                            "created_files": []
                        }
                        self.completed_projects.append(failed_project)
                
                # Monitoring interval
                await asyncio.sleep(5.0)
                
            except Exception as e:
                logging.error(f"Error in system monitoring loop: {e}")
                await asyncio.sleep(10.0)
    
    async def _process_main_task(self, main_task: str):
        """Process main task."""
        logging.info(f"🎯 Processing new project task: {main_task[:100]}...")
        
        project_info = {
            "task_description": main_task,
            "start_time": datetime.now().isoformat(),
            "status": "in_progress",
            "subtasks": [],
            "results": [],
            "created_files": []
        }
        
        # Have project manager analyze the task
        try:
            subtasks = await self.project_manager.analyze_and_delegate_task(main_task)
        except Exception as e:
            logging.error(f"Project manager error: {e}")
            subtasks = []
        
        if not subtasks:
            logging.warning("Task analysis failed")
            project_info["status"] = "failed"
            project_info["error"] = "Task analysis failed"
            self.completed_projects.append(project_info)
            return
        
        # Assign subtasks to coding agents
        assigned_agents = []
        
        for subtask in subtasks:
            project_info["subtasks"].append({
                "id": subtask.id,
                "description": subtask.description,
                "assigned_to": subtask.assigned_to,
                "priority": subtask.priority
            })
            
            if subtask.assigned_to in self.coding_agents:
                agent = self.coding_agents[subtask.assigned_to]
                assigned_agents.append((agent, subtask.id))
                
                message = AgentMessage(
                    sender_id="project_manager",
                    receiver_id=subtask.assigned_to,
                    message_type=MessageType.TASK_REQUEST,
                    content=subtask.description,
                    metadata={
                        "task_id": subtask.id,
                        "priority": subtask.priority,
                        "tools_needed": subtask.tools_needed
                    }
                )
                await agent.send_message_to_agent(message)
                self.message_log.append(message)
                logging.info(f"📨 Assigned task to {subtask.assigned_to}: {subtask.description[:50]}...")
        
        # Wait for all agents to complete their tasks
        await self._wait_for_agents_completion(assigned_agents, project_info)
        
        # Determine project status based on results
        has_results = len(project_info["results"]) > 0
        has_files = len(project_info["created_files"]) > 0
        has_errors = any("error" in result for result in project_info["results"] if isinstance(result, dict))
        
        if has_results and (has_files or not has_errors):
            project_info["status"] = "completed"
            logging.info(f"✅ Project completed successfully with {len(project_info['created_files'])} files created")
        else:
            project_info["status"] = "failed"
            project_info["error"] = "No successful results or files created"
            logging.warning(f"⚠️ Project marked as failed - Results: {has_results}, Files: {has_files}, Errors: {has_errors}")
        
        project_info["end_time"] = datetime.now().isoformat()
        self.completed_projects.append(project_info)
    
    async def _wait_for_agents_completion(self, assigned_agents: List[tuple], project_info: Dict[str, Any]):
        """Wait for all assigned agents to complete their tasks."""
        max_wait_time = 300  # 5 minutes maximum
        check_interval = 2   # Check every 2 seconds
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            all_completed = True
            
            for agent, task_id in assigned_agents:
                # Check if agent has completed tasks (no current tasks)
                if len(agent.current_tasks) > 0:
                    all_completed = False
                    break
            
            if all_completed:
                logging.info("✅ All agents have completed their tasks!")
                
                # Collect results from all agents
                for agent, task_id in assigned_agents:
                    if hasattr(agent, 'recent_task_results') and agent.recent_task_results:
                        for result in agent.recent_task_results:
                            if isinstance(result, dict):
                                project_info["results"].append(result)
                                # Collect created files
                                if "created_files" in result and result["created_files"]:
                                    project_info["created_files"].extend(result["created_files"])
                                logging.info(f"📊 Collected result from {agent.agent_id}: {len(result.get('created_files', []))} files")
                
                break
            
            await asyncio.sleep(check_interval)
            elapsed_time += check_interval
        
        if elapsed_time >= max_wait_time:
            logging.warning("⚠️ Timeout reached, proceeding with current results")
    
    async def submit_project_task(self, task_description: str):
        """Submit project task to the system."""
        self.global_task_queue.put(task_description)
        logging.info(f"📝 New project task submitted: {task_description[:100]}...")
    
    def get_system_status(self) -> SystemStatus:
        """Get overall system status."""
        agent_statuses = {}
        total_completed_tasks = 0
        total_active_tasks = 0
        
        for agent_id, agent in self.all_agents.items():
            status = agent.get_status()
            agent_statuses[agent_id] = status.__dict__
            total_completed_tasks += status.completed_tasks
            total_active_tasks += status.current_tasks_count
        
        return SystemStatus(
            system_running=self.is_running,
            total_agents=len(self.all_agents),
            total_completed_tasks=total_completed_tasks,
            total_active_tasks=total_active_tasks,
            pending_projects=self.global_task_queue.qsize(),
            completed_projects=len(self.completed_projects),
            agent_details=agent_statuses,
            timestamp=datetime.now().isoformat()
        )
    
    async def wait_for_completion(self, timeout_minutes: int = 60) -> Dict[str, Any]:
        """Wait for task completion."""
        start_time = datetime.now()
        timeout = timeout_minutes * 60  # seconds
        
        while (datetime.now() - start_time).total_seconds() < timeout:
            status = self.get_system_status()
            
            # Check if all agents are idle
            all_idle = True
            for agent_status in status.agent_details.values():
                if agent_status["current_tasks_count"] > 0:
                    all_idle = False
                    break
            
            if all_idle and self.global_task_queue.empty():
                logging.info("✅ All tasks completed")
                return status.__dict__
            
            await asyncio.sleep(2.0)
        
        logging.warning(f"⚠️ Timeout ({timeout_minutes} minutes) reached")
        return self.get_system_status().__dict__
    
    def create_structured_task(self, main_objective: str, requirements: List[str] = None, 
                               constraints: List[str] = None, deliverables: List[str] = None) -> str:
        """Create structured project task."""
        task_parts = [f"Main Objective: {main_objective}"]
        
        if requirements:
            task_parts.append("Requirements:")
            task_parts.extend([f"- {req}" for req in requirements])
        
        if constraints:
            task_parts.append("Constraints:")
            task_parts.extend([f"- {constraint}" for constraint in constraints])
            
        if deliverables:
            task_parts.append("Deliverables:")
            task_parts.extend([f"- {deliverable}" for deliverable in deliverables])
        
        return "\n".join(task_parts)
    
    def get_agent_details(self, agent_id: str = None) -> Dict[str, Any]:
        """Get agent detailed information."""
        if agent_id:
            if agent_id in self.all_agents:
                agent = self.all_agents[agent_id]
                status = agent.get_status()
                return {
                    "agent_id": status.agent_id,
                    "role": status.role, 
                    "is_running": status.is_running,
                    "completed_tasks": status.completed_tasks,
                    "current_tasks": status.current_tasks_count,
                    "pending_messages": status.pending_messages,
                    "recent_results": status.recent_results,
                    "message_history_length": status.message_history_length
                }
            return {"error": f"Agent '{agent_id}' not found"}
        else:
            return {
                agent_id: {
                    "role": agent.role.value,
                    "is_running": agent.is_running,
                    "completed_tasks": agent.completed_tasks,
                    "current_tasks": len(agent.current_tasks),
                    "pending_messages": agent.message_queue.qsize(),
                    "message_history_length": len(agent.conversation_history)
                }
                for agent_id, agent in self.all_agents.items()
            }
    
    def get_message_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get inter-agent message log."""
        recent_messages = self.message_log[-limit:] if len(self.message_log) > limit else self.message_log
        return [
            {
                "timestamp": msg.timestamp.isoformat(),
                "sender_id": msg.sender_id,
                "receiver_id": msg.receiver_id,
                "message_type": msg.message_type,
                "content": msg.content[:200] + "..." if len(msg.content) > 200 else msg.content
            }
            for msg in recent_messages
        ]
    
    def display_system_dashboard(self):
        """Display system dashboard."""
        status = self.get_system_status()
        
        print("\n" + "="*60)
        print("🎆 Autonomous Multi-Agent System Dashboard")
        print("="*60)
        
        print(f"🟢 System Status: {'Running' if status.system_running else 'Stopped'}")
        print(f"🤖 Active Agents: {status.total_agents}")
        print(f"✅ Completed Tasks: {status.total_completed_tasks}")
        print(f"⏳ Active Tasks: {status.total_active_tasks}")
        print(f"📝 Pending Projects: {status.pending_projects}")
        print(f"🏆 Completed Projects: {status.completed_projects}")
        
        print("\n👥 Agent Details:")
        print("-" * 60)
        
        for agent_id, agent_status in status.agent_details.items():
            status_icon = "🟢" if agent_status["is_running"] else "🔴"
            print(f"{status_icon} {agent_id} ({agent_status['role']})")
            print(f"    ✅ Completed: {agent_status['completed_tasks']}, ⏳ Active: {agent_status['current_tasks_count']}, 📨 Pending: {agent_status['pending_messages']}")
            if agent_status["recent_results"]:
                # Format recent results for display
                results_summary = []
                for result in agent_status["recent_results"]:
                    if isinstance(result, dict):
                        if "created_files" in result:
                            file_count = len(result["created_files"])
                            results_summary.append(f"{file_count} files")
                        elif "error" in result:
                            results_summary.append("error")
                        else:
                            results_summary.append("completed")
                    else:
                        results_summary.append(str(result))
                print(f"    📈 Recent Results: {', '.join(results_summary)}")
        
        print("\n" + "="*60)
        print(f"📅 Last Updated: {status.timestamp}")
        print("="*60 + "\n")
    
    def add_custom_agent(self, agent_id: str, agent: 'AutonomousAgent'):
        """Add a custom agent to the system."""
        if agent_id not in self.all_agents:
            self.all_agents[agent_id] = agent
            if agent.role != AgentRole.PROJECT_MANAGER:
                self.coding_agents[agent_id] = agent
            logging.info(f"✅ Added custom agent: {agent_id}")
        else:
            logging.warning(f"⚠️ Agent {agent_id} already exists")
    
    def remove_agent(self, agent_id: str):
        """Remove an agent from the system."""
        if agent_id in self.all_agents and agent_id != "project_manager":
            agent = self.all_agents.pop(agent_id)
            if agent_id in self.coding_agents:
                del self.coding_agents[agent_id]
            logging.info(f"✅ Removed agent: {agent_id}")
            return True
        else:
            logging.warning(f"⚠️ Cannot remove agent {agent_id}")
            return False
    
    def get_active_agent_count(self) -> int:
        """Get the number of active agents in the system."""
        active_count = 0
        for agent in self.all_agents.values():
            if hasattr(agent, 'is_running') and agent.is_running:
                active_count += 1
        return active_count
    
    @property
    def agents(self) -> Dict[str, Any]:
        """Property to access all agents (for compatibility)."""
        return self.all_agents
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics."""
        status = self.get_system_status()
        
        # Calculate performance metrics
        total_tasks = status.total_completed_tasks + status.total_active_tasks
        completion_rate = (status.total_completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        agent_performance = {}
        for agent_id, agent_status in status.agent_details.items():
            agent_total = agent_status["completed_tasks"] + agent_status["current_tasks_count"]
            agent_completion_rate = (agent_status["completed_tasks"] / agent_total * 100) if agent_total > 0 else 0
            agent_performance[agent_id] = {
                "completion_rate": round(agent_completion_rate, 2),
                "total_tasks": agent_total,
                "workload": agent_status["current_tasks_count"]
            }
        
        return {
            "overall_completion_rate": round(completion_rate, 2),
            "total_system_tasks": total_tasks,
            "system_utilization": status.total_active_tasks,
            "agent_performance": agent_performance,
            "system_uptime": self.is_running,
            "message_throughput": len(self.message_log)
        }
    
    def get_project_results(self) -> List[Dict[str, Any]]:
        """Get completed project results."""
        return self.completed_projects
    
    def get_latest_project_result(self) -> Dict[str, Any]:
        """Get the latest completed project result."""
        if self.completed_projects:
            return self.completed_projects[-1]
        return {}
    
    def get_created_files(self) -> List[str]:
        """Get all files created by the system."""
        all_files = []
        for project in self.completed_projects:
            if 'created_files' in project:
                all_files.extend(project['created_files'])
        return all_files