# Autonomous Multi-Agent System

A sophisticated autonomous multi-agent system featuring a project manager and specialized coding agents that work cooperatively to execute complex development tasks. The system supports both full Claude Code SDK integration and fallback mode for environments where the SDK is not available.

## 🌟 Features

- **🤖 Autonomous Agents**: Four specialized agents with distinct roles and capabilities
- **📊 Project Management**: Intelligent task analysis and distribution by the project manager
- **🔄 Real-time Coordination**: Agents communicate and coordinate tasks automatically  
- **📈 Progress Monitoring**: Real-time system dashboard and performance metrics
- **🛠️ Multi-language Support**: Frontend, backend, and DevOps specializations
- **📝 Structured Tasks**: Flexible task creation with requirements and constraints
- **🔧 Modular Architecture**: Clean, maintainable, and extensible codebase
- **⚡ Fallback Mode**: Functions without Claude Code SDK with limited capabilities
- **📓 Interactive Notebook**: Jupyter notebook for interactive development and testing

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- nest-asyncio (for Jupyter environments)
- Claude Code SDK (optional - system works in fallback mode without it)

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

3. (Optional) Install Claude Code SDK for full functionality:
```bash
npm install -g @anthropic-ai/claude-code
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
    # Initialize the system (works with or without Claude Code SDK)
    system = await init_autonomous_system()
    await system.start_system()
    
    # Submit a project task
    task = """
    Create a simple Python calculator application with the following features:
    - Basic arithmetic operations (add, subtract, multiply, divide)
    - Command-line interface for user input
    - Error handling for division by zero
    - Clean, well-documented code following PEP 8 standards
    """
    await system.submit_project_task(task)
    
    # Wait for completion
    result = await system.wait_for_completion(timeout_minutes=15)
    
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
├── claude_sdk_interface.py    # Claude SDK integration with fallback
├── base_agent.py             # Base agent functionality
├── specialized_agents.py     # Agent implementations
├── system_coordinator.py     # Multi-agent coordination
├── utils.py                  # Utilities and helpers
├── multiagent_system.py      # Main entry point
├── main.ipynb               # Interactive notebook for testing
├── test_modular_structure.py # System tests
└── __init__.py              # Package initialization
```

### Output Directory

All generated files and test results are saved to the `output/` directory:

```
output/
├── main.py                   # Generated programs
├── test_results.json         # Test execution results
└── debug_log.txt            # Debug information (when needed)
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

## 🔧 System Modes

### Full Mode (With Claude Code SDK)

When Claude Code SDK is available, the system operates with full capabilities:
- Advanced task analysis and code generation
- Real-time Claude Code integration
- Full tool access for agents
- Complex project handling

### Fallback Mode (Without Claude Code SDK)

When Claude Code SDK is not available, the system provides:
- Basic task execution simulation
- File generation for common tasks (Hello World programs, etc.)
- System monitoring and coordination
- Limited but functional development assistance

## 📝 Usage Examples

### Basic Task Execution Test

The system includes a built-in test for creating a simple Hello World program:

```python
# Run the test notebook
# This will create:
# - output/main.py: Generated Hello World program
# - output/test_results.json: Test execution results
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
# Test modular structure
cd src/agent
python test_modular_structure.py

# Test individual components
python -c "from multiagent_system import init_autonomous_system; print('✅ Import test passed')"
```

### Validation

```python
from src.agent import validate_system_requirements, print_system_requirements

# Check system requirements
print_system_requirements()

# Validate all dependencies
requirements = validate_system_requirements()
print(f"System ready: {all(requirements.values())}")
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
   pip install nest-asyncio
   # Claude Code SDK is optional
   npm install -g @anthropic-ai/claude-code
   ```

3. **Jupyter Environment Issues**
   ```python
   # The system automatically applies nested asyncio support
   # If issues persist, restart the Jupyter kernel
   ```

4. **No Output Files Generated**
   - Check the `output/` directory in the project root
   - Ensure the system is running in the correct directory
   - For fallback mode, only basic tasks like Hello World are supported

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

### Fallback Mode Limitations

When running without Claude Code SDK:
- Limited to basic code generation (Hello World, simple programs)
- Advanced project analysis may not work
- Complex multi-file projects are not supported
- System provides warnings about limited functionality

## 🎯 Current Status

### ✅ Implemented Features
- Modular multi-agent architecture
- Project manager with task delegation
- Specialized coding agents (Frontend, Backend, DevOps)
- System coordination and monitoring
- Interactive Jupyter notebook interface
- Fallback mode for environments without Claude Code SDK
- Basic file generation capabilities
- Test execution and results tracking

### 🔄 In Progress
- Enhanced code generation for complex projects
- Full Claude Code SDK integration testing
- Advanced project templates and examples

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

- Built with [Claude Code SDK](https://claude.ai/code) (optional dependency)
- Inspired by multi-agent system research
- Thanks to the open-source community for tools and libraries

## 🔗 Related Projects

- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- [Multi-Agent Systems Research](https://github.com/topics/multi-agent-systems)
- [Autonomous Software Development](https://github.com/topics/autonomous-development)

---

**⚡ Ready to revolutionize your development workflow with autonomous agents? Get started today!**

**Note**: This system is designed to work both with and without Claude Code SDK. In fallback mode, it provides limited but functional development assistance for learning and experimentation purposes.
