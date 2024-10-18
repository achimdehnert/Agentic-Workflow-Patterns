from src.patterns.task_orchestration.coordinator import CoordinatorAgent
from src.patterns.task_orchestration.message import Message
from src.config.logging import logger
import asyncio

async def pipeline():
    coordinator = CoordinatorAgent(name="CoordinatorAgent", dag_file='dag.yaml')
    main_task = "Process books to generate summaries and extract key information."
    message = Message(content=main_task, sender="User", recipient="CoordinatorAgent")
    response = await coordinator.process(message)

    final_output = response.content
    with open('final_report.json', 'w') as output_file:
        json.dump(final_output, output_file, indent=2)
    print("Task completed. The final report has been saved to 'final_report.json'.")

if __name__ == "__main__":
    asyncio.run(pipeline())
