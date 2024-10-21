# DAG Orchestration Pattern

## Overview

The DAG (Directed Acyclic Graph) Orchestration Pattern is an advanced design pattern for managing complex workflows in a flexible and efficient manner. This pattern allows for the execution of multiple tasks in a specified order, with support for both parallel and serial task execution. The pattern uses a YAML-defined DAG to structure the workflow and a CoordinatorAgent to manage the execution.

## Key Components

1. **CoordinatorAgent**: Manages the execution of the entire DAG, creating and running sub-agents as needed.
2. **CollectAgent**: Gathers documents from a specified folder and prepares them for processing.
3. **PreprocessAgent**: Cleans and normalizes the collected document content using a Language Model (LLM).
4. **ExtractAgent**: Extracts key information (characters, themes, plot points) from the preprocessed documents using an LLM.
5. **SummarizeAgent**: Generates concise summaries of the preprocessed documents using an LLM.
6. **CompileAgent**: Compiles a final report based on the extracted key information and summaries.

## Process Flow

1. The CoordinatorAgent loads the DAG definition from a YAML file.
2. The CoordinatorAgent executes tasks in the DAG based on their dependencies:
   a. It identifies executable tasks (those with satisfied dependencies).
   b. It creates the appropriate sub-agents for each executable task.
   c. It runs the tasks in parallel when possible.
   d. It collects and stores the results of each task.
3. The CoordinatorAgent continues this process until all tasks in the DAG are completed.
4. The final output is returned based on the last task in the DAG.