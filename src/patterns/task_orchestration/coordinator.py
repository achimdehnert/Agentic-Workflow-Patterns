from src.patterns.task_orchestration.agent import Agent
from src.patterns.task_orchestration.message import Message
from src.config.logging import logger
import asyncio
import yaml
import json
import os


class CoordinatorAgent(Agent):
    def __init__(self, name: str, dag_file: str) -> None:
        super().__init__(name)
        logger.info(f"{self.name} initialized.")
        self.dag_file = dag_file
        self.tasks = {}
        self.task_results = {}
        self.task_states = {}
        self.load_dag()

    async def process(self, message: Message) -> Message:
        logger.info(f"{self.name} processing message.")
        try:
            # Execute the DAG
            await self.execute_dag()

            # Get the final output
            final_task_id = self.find_final_task()
            final_output = self.task_results.get(final_task_id, "No final output generated.")

            # Return the final message
            return Message(content=final_output, sender=self.name, recipient=message.sender)

        except Exception as e:
            logger.error(f"Error during processing: {str(e)}")
            return Message(
                content="An error occurred while processing the task.",
                sender=self.name,
                recipient=message.sender
            )

    def load_dag(self):
        with open(self.dag_file, 'r') as file:
            dag_data = yaml.safe_load(file)
            for task_data in dag_data.get('tasks', []):
                task_id = task_data['id']
                self.tasks[task_id] = task_data
                self.task_states[task_id] = 'pending'
                logger.info(f"Task {task_id} loaded: {task_data['description']}")

    async def execute_dag(self):
        pending_tasks = set(self.tasks.keys())
        while pending_tasks:
            executable_tasks = [task_id for task_id in pending_tasks if self.can_execute(task_id)]
            if not executable_tasks:
                logger.error("No executable tasks found. Possible circular dependency.")
                break

            tasks = []
            for task_id in executable_tasks:
                task_data = self.tasks[task_id]
                agent_name = task_data['name']
                agent = self.create_agent(task_data['agent'], agent_name)
                input_data = self.collect_inputs(task_data['dependencies'])
                sub_message = Message(content=input_data, sender=self.name, recipient=agent.name)
                task = asyncio.create_task(self.run_task(task_id, agent, sub_message, task_data))
                tasks.append(task)
                pending_tasks.remove(task_id)
                self.task_states[task_id] = 'running'

            await asyncio.gather(*tasks)

    def can_execute(self, task_id):
        dependencies = self.tasks[task_id]['dependencies']
        return all(dep in self.task_results for dep in dependencies)

    def collect_inputs(self, dependencies):
        if not dependencies:
            return {}
        elif len(dependencies) == 1:
            dep = dependencies[0]
            return self.task_results[dep]
        else:
            inputs = {}
            for dep in dependencies:
                inputs[dep] = self.task_results[dep]
            return inputs

    async def run_task(self, task_id, agent, message, task_data):
        logger.info(f"Starting task {task_id}: {agent.name}")
        try:
            result_message = await agent.process(message)
            self.task_results[task_id] = result_message.content
            self.task_states[task_id] = 'completed'
            self.log_task_result(task_id, result_message.content)
            logger.info(f"Completed task {task_id}: {agent.name}")
        except Exception as e:
            self.task_states[task_id] = 'failed'
            logger.error(f"Task {task_id} failed: {e}")
            # Optionally, you can decide whether to halt the pipeline or continue

    def create_agent(self, agent_class_name, agent_name):
        module = __import__('agents', fromlist=[agent_class_name])
        agent_class = getattr(module, agent_class_name)
        return agent_class(name=agent_name)

    def find_final_task(self):
        all_tasks = set(self.tasks.keys())
        dependent_tasks = {dep for task in self.tasks.values() for dep in task['dependencies']}
        final_tasks = all_tasks - dependent_tasks
        return final_tasks.pop() if final_tasks else None

    def log_task_result(self, task_id, result):
        os.makedirs('task_logs', exist_ok=True)
        with open(f'task_logs/{task_id}.json', 'w') as f:
            json.dump(result, f, indent=2)
