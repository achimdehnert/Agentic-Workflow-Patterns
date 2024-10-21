# Pattern 7 - Dynamic Decomposition

## Overview
The **Dynamic Decomposition** is an advanced design pattern where a *Coordinator Agent* autonomously decomposes a complex task into multiple subtasks without predefined structures. The coordinator uses a Language Model (LLM) to generate subtasks, which are then processed by separate *Sub-Task Agents* in parallel. After all subtasks are completed, the coordinator gathers and combines the results to produce a structured summary.

<p align="center">
    <img src="../../../img/framework/dynamic_decomposition.png" alt="Dynamic Decomposition" width="500"/>
</p>

## Key Components

### **CoordinatorAgent**
- **Receives the complex task input**.
- **Analyzes the task** using an LLM to dynamically determine necessary subtasks.
- **Decomposes the task** into independent subtasks.
- **Spawns sub-agents** for each identified subtask.
- **Waits** until all sub-agents complete their assigned tasks.
- **Combines results** from all sub-agents into a structured summary.

### **SubTaskAgent**
- **Receives** a specific subtask from the coordinator.
- **Processes** the subtask by interacting with an LLM.
- **Extracts information** or performs analysis based on the assigned task.
- **Returns the result** to the coordinator.

### **ResponseGenerator**
- Interfaces with the LLM to generate subtasks and process individual subtasks.

### **Message**
- Represents messages exchanged between agents, containing content, sender, and recipient information.

## Process Flow

1. The coordinator receives the complex task input.
2. It uses an LLM to generate subtasks for analyzing or processing the input.
3. The LLM output is parsed from JSON format into a dictionary of subtasks.
4. Sub-agents are created for each subtask:
   a. Each sub-agent receives a message with the task details.
   b. The sub-agent prepares an input for the LLM based on its specific task.
   c. The LLM is called to process the task or extract information.
   d. The result is returned to the coordinator.
5. All sub-agents execute their tasks in parallel.
6. The coordinator collects results from all sub-agents.
7. A final structured summary is created, combining all subtask results.