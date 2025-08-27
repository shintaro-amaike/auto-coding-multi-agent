# Autonomous Multi-Agent System

A sophisticated autonomous multi-agent system powered by Claude Code SDK, featuring a project manager and specialized coding agents that work cooperatively to execute complex development tasks.

## 🌟 Features

- **🤖 Autonomous Agents**: Four specialized agents with distinct roles and capabilities
- **📊 Project Management**: Intelligent task analysis and distribution by the project manager
- **🔄 Real-time Coordination**: Agents communicate and coordinate tasks automatically  
- **📈 Progress Monitoring**: Real-time system dashboard and performance metrics
- **🛠️ Multi-language Support**: Frontend, backend, and DevOps specializations
- **📝 Structured Tasks**: Flexible task creation with requirements and constraints
- **🔧 Modular Architecture**: Clean, maintainable, and extensible codebase

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Claude Code SDK
- nest-asyncio (for Jupyter environments)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd auto-coding-multi-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

#### Python Script
```python
import asyncio
from src.agent import init_autonomous_system

async def main():
    # Initialize the system
    system = await init_autonomous_system()
    await system.start_system()
    
    # Submit a project task
    task = "Create a simple Python web API with FastAPI and include tests"
    await system.submit_project_task(task)
    
    # Wait for completion
    result = await system.wait_for_completion(timeout_minutes=30)
    
    # Display results
    system.display_system_dashboard()
    
    # Stop the system
    await system.stop_system()

if __name__ == "__main__":
    asyncio.run(main())
```

#### Jupyter Notebook
```python
# Use the provided main.ipynb for interactive development
from multiagent_system import (
    init_autonomous_system, 
    AutonomousMultiAgentSystem,
    quick_task_examples
)

# Initialize and run tasks interactively
system = init_jupyter_system()
await system.initialize_system()

# Execute tasks
result = run_autonomous_task(system, "Your project description", timeout_minutes=60)
```

## 🏗️ Architecture

### System Components

The system is built with a modular architecture consisting of specialized components:

```
src/agent/
├── models.py                  # Data models and enums
├── claude_sdk_interface.py    # Claude SDK integration
├── base_agent.py             # Base agent functionality
├── specialized_agents.py     # Agent implementations
├── system_coordinator.py     # Multi-agent coordination
├── utils.py                  # Utilities and helpers
├── multiagent_system.py      # Main entry point
├── main.ipynb               # Interactive notebook
└── __init__.py              # Package initialization
```

### Agent Types

#### 🎯 Project Manager Agent
- **Role**: Task analysis and distribution
- **Capabilities**: 
  - Breaks down complex projects into subtasks
  - Assigns tasks to appropriate coding agents
  - Monitors overall progress
  - Coordinates agent communication

#### 🎨 Frontend Coding Agent
- **Specialization**: React, Vue.js, Angular, Svelte
- **Capabilities**:
  - Responsive web design
  - Component architecture
  - State management
  - UI/UX implementation
  - Performance optimization

#### ⚙️ Backend Coding Agent
- **Specialization**: Python, Node.js, Java, Go
- **Capabilities**:
  - API design and development
  - Database integration
  - Authentication systems
  - Microservices architecture
  - Server-side optimization

#### 🔧 DevOps Coding Agent
- **Specialization**: Docker, Kubernetes, CI/CD
- **Capabilities**:
  - Infrastructure as Code
  - Container orchestration
  - Deployment pipelines
  - Monitoring and logging
  - Security configuration

## 📝 Usage Examples

### Structured Task Creation

```python
from src.agent import TaskBuilder

# Create a structured project task
task = (TaskBuilder()
    .set_objective("Build a full-stack e-commerce application")
    .add_requirements([
        "User authentication system",
        "Product catalog with search",
        "Shopping cart functionality",
        "Payment processing integration"
    ])
    .add_constraints([
        "Use React for frontend",
        "Use Python FastAPI for backend",
        "Include comprehensive tests",
        "Complete within 2 hours"
    ])
    .add_deliverables([
        "Working web application",
        "API documentation",
        "Test suite",
        "Deployment guide"
    ])
    .build())

# Execute the structured task
await system.submit_project_task(task)
```

### Real-time Monitoring

```python
from src.agent import SystemMonitor

# Create system monitor
monitor = SystemMonitor(system)

# Collect metrics
metrics = monitor.collect_metrics()
print(f"System completion rate: {metrics['performance_metrics']['overall_completion_rate']}%")

# Get performance history
history = monitor.get_metrics_history()
average_performance = monitor.get_average_performance()
```

### Multi-Phase Projects

```python
from src.agent import ProgressTracker

# Track complex multi-phase projects
tracker = ProgressTracker()
tracker.add_phase("Design & Planning", "System architecture and requirements", 30)
tracker.add_phase("Backend Development", "API and database implementation", 60)
tracker.add_phase("Frontend Development", "User interface implementation", 45)
tracker.add_phase("Testing & Deployment", "Quality assurance and deployment", 30)

# Start tracking
tracker.start_tracking()

# Execute each phase and update progress
for phase_index, phase in enumerate(phases):
    tracker.start_phase(phase_index)
    result = await execute_phase(phase)
    tracker.complete_phase(phase_index)

# Get final summary
summary = tracker.get_progress_summary()
```

## 🔧 Configuration

### Agent Tool Configuration

Each agent type has access to specific tools:

- **Project Manager**: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
- **Coding Agents**: Read, Write, Edit, Bash, Glob, Grep, MultiEdit, NotebookEdit  
- **DevOps Agent**: Read, Write, Edit, Bash, Glob, Grep, TodoWrite

### System Settings

```python
from src.agent import setup_logging, validate_system_requirements

# Configure logging
setup_logging(level="INFO")

# Validate requirements
requirements = validate_system_requirements()
if not all(requirements.values()):
    print("Missing requirements detected")
```

## 📊 Monitoring and Metrics

### System Dashboard

The system provides real-time monitoring through an integrated dashboard:

```python
# Display comprehensive system status
system.display_system_dashboard()

# Get detailed agent information
agent_details = system.get_agent_details("frontend_coder")

# View inter-agent communication
messages = system.get_message_log(limit=20)

# Get performance metrics
performance = system.get_performance_metrics()
```

### Performance Metrics

- **Completion Rate**: Percentage of successfully completed tasks
- **System Utilization**: Number of active tasks across all agents
- **Agent Performance**: Individual agent completion rates and workload
- **Message Throughput**: Inter-agent communication frequency
- **Response Time**: Average task completion times

## 🧪 Testing

### Run Comprehensive Tests

```bash
# Test modular structure
cd src/agent
python test_modular_structure.py

# Test individual components
python -c "from multiagent_system import quick_task_examples; print('✅ Import test passed')"
```

### Validation

```python
from src.agent import print_system_requirements

# Check system requirements
print_system_requirements()

# Validate all dependencies
requirements = validate_system_requirements()
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the correct directory
   cd src/agent
   # Or add to Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```

2. **Missing Dependencies**
   ```bash
   pip install claude-code-sdk nest-asyncio
   ```

3. **Jupyter Environment Issues**
   ```python
   # Apply nested asyncio support
   from src.agent import apply_nested_asyncio
   apply_nested_asyncio()
   ```

### Debug Mode

```python
from src.agent import setup_logging

# Enable debug logging
setup_logging(level="DEBUG")

# Get detailed system information
from src.agent import get_system_info
info = get_system_info()
print(info)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install in development mode
pip install -e .

# Run tests
python src/agent/test_modular_structure.py

# Check code quality
python -m py_compile src/agent/*.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Claude Code SDK](https://claude.ai/code)
- Inspired by multi-agent system research
- Thanks to the open-source community for tools and libraries

## 🔗 Related Projects

- [Claude Code SDK Documentation](https://docs.anthropic.com/claude/docs)
- [Multi-Agent Systems Research](https://github.com/topics/multi-agent-systems)
- [Autonomous Software Development](https://github.com/topics/autonomous-development)

---

**⚡ Ready to revolutionize your development workflow with autonomous agents? Get started today!**

