# Parallel Task Decomposition Pattern

## Overview
The **Parallel Task Decomposition Pattern** is a design pattern where a *Coordinator Agent* decomposes a complex task into multiple independent subtasks. Each subtask is then processed by a separate *Sub-Task Agent* in parallel. After all subtasks are completed, the coordinator gathers and combines the results to produce the final output. This pattern is beneficial for enhancing efficiency and scalability, especially for tasks that can be divided into smaller, independently executable units.

## Key Components

### **CoordinatorAgent**
- **Receives the complex task input.**
- **Decomposes the task** into independent subtasks.
- **Spawns sub-agents** for each subtask.
- **Waits** until all sub-agents complete their assigned tasks.
- **Combines results** from all sub-agents into the final output.

### **SubTaskAgent**
- **Receives** a specific subtask from the coordinator.
- **Processes** the subtask independently.
- **Returns the result** to the coordinator.

### **Agent Base Class**
- Provides a **common interface** for all agents.

### **Message Class**
- Represents **messages exchanged between agents**.
