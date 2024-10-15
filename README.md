# Agentic Workflow Patterns

**Agentic Workflow Patterns** is a repository showcasing best practices and design patterns for building agentic workflows in Python. This repository emphasizes modular, scalable, and reusable design techniques, aiming to facilitate intelligent automation and robust workflow management.

![Agentic Workflow](./img/agentic.png)

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview
This repository provides examples and templates for designing agentic workflows, which are workflows composed of self-contained agents, each responsible for distinct tasks. The focus is on creating reusable components that can be adapted for various automation tasks, enabling intelligent decision-making and streamlined processing.

## Getting Started
Clone this repository to get started. This project requires Python 3.8 or later.

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/)
- `pip` (comes with Python 3.8+)

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Agentic-Workflow-Patterns.git
   cd Agentic-Workflow-Patterns
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .agentic-workflow-patterns
   source .agentic-workflow-patterns/bin/activate
   ```

3. **Upgrade pip and install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Environment Setup
To maintain a clean environment and disable Python bytecode generation, configure the following environment variables:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=$PYTHONPATH:.
```

## Usage
After setting up the environment, you can start experimenting with the workflow patterns included in this repository. Each pattern is documented with examples and explanations to demonstrate its use in building agentic workflows.

## Contributing

We welcome and appreciate contributions! Here’s how to contribute to **Agentic Workflow Patterns**:

1. **Fork the Repository**: Create your own fork on GitHub to make changes independently.

2. **Create a Branch**: Work on a separate branch for each feature or fix to keep changes organized.
   ```bash
   git checkout -b feature-branch-name
   ```

3. **Make Changes**: Keep the code style consistent and ensure your changes are well-documented.

4. **Commit Your Changes**: Write a clear and concise commit message.
   ```bash
   git commit -m "Add feature or fix description"
   ```

5. **Submit a Pull Request**: Push your changes and open a pull request. Describe your changes, link related issues, and mention any specific areas to focus on in the review.

6. **Feedback & Reviews**: Be open to feedback; adjust and refine your PR as needed.

### Guidelines

- **Coding Style**: Follow existing code conventions.
- **Documentation**: Ensure your code and contributions are well-documented.
- **Testing**: Add tests if applicable to maintain repository stability.
- **Issue Reporting**: Report bugs or suggest features via issues, following the provided templates.

For additional questions or collaboration, check out our discussions page or reach out directly.

## License
This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
