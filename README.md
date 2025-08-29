# Claude Code SDK Autonomous Multi-Agent System

A production-ready autonomous multi-agent system that leverages the Claude Code SDK to execute complex development tasks. Features a project manager and specialized coding agents that work cooperatively to analyze, plan, and implement software projects with real file output.

## 🌟 Features

- **🤖 Autonomous Agents**: Four specialized agents with distinct roles and capabilities
- **📊 Project Management**: Intelligent task analysis and distribution by the project manager
- **🔄 Real-time Coordination**: Agents communicate and coordinate tasks automatically  
- **📈 Progress Monitoring**: Real-time system dashboard and performance metrics
- **🛠️ Multi-language Support**: Frontend, backend, and DevOps specializations
- **📝 Structured Tasks**: Flexible task creation with requirements and constraints
- **🔧 Modular Architecture**: Clean, maintainable, and extensible codebase
- **⚡ Claude Code SDK Integration**: Real file creation and code execution
- **📓 Interactive Notebook**: Jupyter notebook for interactive development and testing
- **📁 Real File Output**: All deliverables saved with proper file extensions

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Claude Code SDK (required for full functionality)
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

3. Install Claude Code SDK:
```bash
pip install claude-code-sdk
```

### Basic Usage

#### Interactive Jupyter Notebook

The easiest way to get started is using the provided interactive notebook:

1. Navigate to the agent directory:
```bash
cd src/agent
```

2. Start Jupyter Notebook:
```bash
jupyter notebook main.ipynb
```

3. Run the cells in order:
   - Import libraries and initialize system
   - Initialize the multi-agent system
   - Execute the basic task execution test

#### Python Script

```python
import asyncio
from src.agent import init_autonomous_system

async def main():
    # Initialize the system
    system = await init_autonomous_system()
    await system.start_system()
    
    # Submit a project task
    task = """
    Create a simple Python calculator application with the following features:
    - Basic arithmetic operations (add, subtract, multiply, divide)
    - Command-line interface for user input
    - Error handling for division by zero
    - Save as calculator.py in the output directory
    - Include proper documentation and comments
    """
    await system.submit_project_task(task)
    
    # Wait for completion
    result = await system.wait_for_completion(timeout_minutes=5)
    
    # Display results
    system.display_system_dashboard()
    
    # Stop the system
    await system.stop_system()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🏗️ Architecture

### System Components

The system is built with a modular architecture consisting of specialized components:

```
src/agent/
├── models.py                  # Data models and enums
├── claude_sdk_interface.py    # Claude Code SDK integration
├── base_agent.py             # Base agent functionality
├── specialized_agents.py     # Agent implementations
├── system_coordinator.py     # Multi-agent coordination
├── utils.py                  # Utilities and helpers
├── main.ipynb               # Interactive notebook for testing
└── __init__.py              # Package initialization
```

### Output Directory

All generated files and project deliverables are saved to the `output/` directory:

```
output/
├── calculator.py             # Generated Python programs
├── app.py                   # Generated web applications
├── Counter.js               # Generated React components
├── Counter.css              # Generated stylesheets
├── package.json             # Generated configuration files
└── requirements.txt         # Generated dependency files
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

## 🔧 System Operation

### Claude Code SDK Integration

The system requires Claude Code SDK and operates with full capabilities:
- Advanced task analysis and code generation
- Real-time file creation using Claude Code tools
- Full tool access for agents (Read, Write, Edit, Bash, Glob, Grep)
- Complex multi-file project handling
- Proper wait mechanisms for task completion
- Real deliverable output to the file system

## 📝 Usage Examples

### Built-in Task Examples

The system includes three built-in task examples in main.ipynb:

1. **Python Calculator**: Creates calculator.py with command-line interface
2. **REST API**: Creates app.py with Flask-based API and requirements.txt
3. **React Component**: Creates Counter.js and Counter.css with modern React hooks

```python
# Example task execution
calculator_task = """
Create a simple Python calculator application with the following features:
- Basic arithmetic operations (add, subtract, multiply, divide)
- Error handling for division by zero
- User-friendly command-line interface
- Save the calculator.py file to the output directory
- Include proper documentation and comments
"""

await system.submit_project_task(calculator_task)
result = await system.wait_for_completion(timeout_minutes=5)
```

### Structured Task Creation

```python
# Create a more complex task
task_description = """
Create a web-based todo application with the following features:
- User interface with HTML/CSS/JavaScript
- Add, edit, delete todo items
- Mark items as complete
- Local storage for persistence
- Responsive design for mobile devices
"""

await system.submit_project_task(task_description)
```

## 📊 Monitoring and Metrics

### System Dashboard

The system provides real-time monitoring through an integrated dashboard:

```python
# Display comprehensive system status
system.display_system_dashboard()

# Get detailed agent information
agent_details = system.get_agent_details("backend_coder")

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

### Interactive Testing

Use the Jupyter notebook for interactive testing:

```bash
cd src/agent
jupyter notebook main.ipynb
```

### Command Line Testing

```bash
# Test individual components
cd src/agent
python -c "from utils import init_autonomous_system; print('✅ Import test passed')"

# Validate system requirements
python -c "from claude_sdk_interface import is_sdk_available; print(f'SDK Available: {is_sdk_available()}')"
```

### Validation

```python
from src.agent import get_system_info

# Check system requirements
system_info = get_system_info()
print(f"SDK Available: {system_info['sdk_available']}")
print(f"Supported Agents: {', '.join(system_info['supported_agents'])}")
print(f"Features: {', '.join(system_info['features'])}")
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
   pip install nest-asyncio claude-code-sdk
   ```

3. **Jupyter Environment Issues**
   ```python
   # The system automatically applies nested asyncio support
   # If issues persist, restart the Jupyter kernel
   ```

4. **No Output Files Generated**
   - Check the `output/` directory in the project root
   - Ensure Claude Code SDK is properly installed
   - Verify agents have completed their tasks before checking for files
   - Use `system.wait_for_completion()` to ensure task completion

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

### Claude Code SDK Requirements

The system requires Claude Code SDK for proper operation:
- Real file creation and code execution
- Access to Claude Code tools (Read, Write, Edit, Bash, etc.)
- Advanced project analysis and implementation
- Multi-file project support with proper file extensions
- Integration with the Claude Code environment

## 🎯 Current Status

### ✅ Implemented Features
- Modular multi-agent architecture
- Project manager with intelligent task delegation
- Specialized coding agents (Frontend, Backend, DevOps)
- Real-time system coordination and monitoring
- Interactive Jupyter notebook interface
- Claude Code SDK integration for real file creation
- Proper task completion wait mechanisms
- Deliverable output with appropriate file extensions
- Three built-in task examples (Calculator, API, React Component)

### 🔄 In Progress
- Enhanced project templates and examples
- Advanced multi-file project coordination
- Performance optimization and monitoring

### 📋 Planned Features
- Web-based dashboard interface
- Template-based project generation
- Integration with version control systems
- Enhanced monitoring and analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Navigate to agent directory
cd src/agent

# Test imports
python -c "from utils import init_autonomous_system; print('✅ System ready')"

# Check code quality
python -m py_compile *.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Claude Code SDK](https://claude.ai/code) (optional dependency)
- Inspired by multi-agent system research
- Thanks to the open-source community for tools and libraries

## 🔗 Related Projects

- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- [Multi-Agent Systems Research](https://github.com/topics/multi-agent-systems)
- [Autonomous Software Development](https://github.com/topics/autonomous-development)

---

**⚡ Ready to revolutionize your development workflow with autonomous agents? Get started today!**

**Note**: This system requires Claude Code SDK for full functionality. It creates real files and executes actual code generation tasks, making it suitable for production development workflows.