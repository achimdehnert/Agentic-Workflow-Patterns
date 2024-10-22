# Agentic Workflow Patterns

**Agentic Workflow Patterns** is a repository showcasing best practices and design patterns for building agentic workflows in Python. This repository emphasizes modular, scalable, and reusable design techniques, aiming to facilitate intelligent automation and robust workflow management.

![Agentic Workflow](./img/agentic.png)

## Table of Contents
- [Overview](#overview)
- [Patterns Overview](#patterns-overview)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview
This repository provides examples and templates for designing agentic workflows, which are workflows composed of self-contained agents, each responsible for distinct tasks. The focus is on creating reusable components that can be adapted for various automation tasks, enabling intelligent decision-making and streamlined processing.

## Patterns Overview

### Pattern 1 - Reflection
The **Reflection** pattern implements an iterative content generation and refinement system using an Actor-Critic framework. This pattern enables self-improving content generation through continuous feedback loops between an Actor (content generator) and a Critic (content reviewer).

The pattern follows an iterative workflow where the Actor generates content, the Critic reviews it, and then both components revise their work based on the accumulated state history. This process continues for a specified number of cycles, leading to progressively refined content.

<p align="center">
    <img src="./img/framework/reflection.png" alt="Reflection" width="475"/>
</p>

### Pattern 2 - Web Access
The **Web Access** pattern implements an agentic workflow for retrieving, processing, and summarizing web content. This pattern orchestrates a pipeline of specialized agents that handle different aspects of web content acquisition and processing through search, scrape, and summarize operations. It leverages the SERP API for web searches and language models for generating queries and summaries.

<p align="center">
    <img src="./img/framework/web_access.png" alt="Web Access" width="350"/>
</p>

### Pattern 3 - Semantic Routing
The **Semantic Routing** pattern implements an agentic workflow for intelligently routing user queries to specialized agents based on semantic intent. This pattern uses a coordinator-delegate architecture where a main TravelPlannerAgent determines the user's intent and routes requests to specialized sub-agents for specific travel-related tasks like flight booking, hotel searches, and car rentals.

The pattern leverages language models for intent detection and query processing, ensuring that each request is handled by the most appropriate specialized agent.

<p align="center">
    <img src="./img/framework/semantic_router.png" alt="Semantic Router" width="1000"/>
</p>

### Pattern 4 - Parallel Delegation
The **Parallel Delegation** pattern implements an agentic workflow that processes complex queries by first identifying distinct entities through Named Entity Recognition (NER), then delegating these entities to specialized agents for parallel processing. This pattern is particularly effective for scenarios where multiple independent sub-tasks can be executed concurrently, such as travel planning where flight, hotel, and car rental searches can be performed simultaneously.

The pattern leverages asynchronous processing and parallel execution to optimize performance while maintaining a coordinated workflow through a central coordinator agent.

<p align="center">
    <img src="./img/framework/parallel_delegation.png" alt="Parallel Delegation" width="700"/>
</p>

### Pattern 5 - Dynamic Sharding
The **Dynamic Sharding Pattern** is an architectural approach designed to efficiently process large datasets by dynamically dividing the workload into smaller, manageable shards and processing them in parallel. This pattern enhances scalability, optimizes resource utilization, and improves the overall performance of systems handling extensive data or requests.

This project demonstrates the Dynamic Sharding Pattern by fetching biographies of a list of celebrities using web search. The coordinator agent dynamically shards the list of celebrity names and processes each shard concurrently through dynamically created sub-agents.

<p align="center">
    <img src="./img/framework/dynamic_sharding.png" alt="Dynamic Sharding" width="800"/>
</p>

### Pattern 6 - Task Decomposition
The **Task Decomposition** pattern is a design pattern where a *Coordinator Agent* manages the execution of a complex task by dividing it into multiple independent subtasks. In this pattern, the tasks are provided by the user rather than being automatically deduced by the coordinator. Each subtask is then processed by a separate *Sub-Task Agent* in parallel. After all subtasks are completed, the coordinator gathers and combines the results to produce the final output.

This pattern is beneficial for enhancing efficiency and scalability, especially for tasks that can be divided into smaller, independently executable units.

<p align="center">
    <img src="./img/framework/task_decomposition.png" alt="Task Decomposition" width="775"/>
</p>

### Pattern 7 - Dynamic Decomposition
The **Dynamic Decomposition** is an advanced design pattern where a *Coordinator Agent* autonomously decomposes a complex task into multiple subtasks without predefined structures. The coordinator uses a Language Model (LLM) to generate subtasks, which are then processed by separate *Sub-Task Agents* in parallel. After all subtasks are completed, the coordinator gathers and combines the results to produce a structured summary.

<p align="center">
    <img src="./img/framework/dynamic_decomposition.png" alt="Dynamic Decomposition" width="800"/>
</p>

### Pattern 8 - DAG Orchestration
The **DAG (Directed Acyclic Graph) Orchestration Pattern** is an advanced design pattern for managing complex workflows in a flexible and efficient manner. This pattern allows for the execution of multiple tasks in a specified order, with support for both parallel and serial task execution. The pattern uses a YAML-defined DAG to structure the workflow and a Coordinator Agent to manage the execution.

<p align="center">
    <img src="./img/framework/dag_orchestration.png" alt="DAG Orchestration" width="600"/>
</p>

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