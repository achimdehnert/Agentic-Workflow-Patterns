from src.patterns.dynamic_sharding.sub_agent import ShardProcessingAgent
from src.patterns.dynamic_sharding.message import Message
from src.patterns.dynamic_sharding.agent import Agent
from src.config.logging import logger
from typing import List
import asyncio


class CoordinatorAgent(Agent):
    """
    An agent that coordinates the processing of a list of celebrity names by sharding
    the list and dynamically creating sub-agents to process each shard in parallel.

    Attributes:
        name (str): The name of the coordinator agent.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes the CoordinatorAgent.

        Args:
            name (str): The name of the agent.
        """
        super().__init__(name)
        logger.info(f"{self.name} initialized.")

    async def process(self, message: Message) -> Message:
        """
        Processes the incoming message containing celebrity names and shard size,
        shards the list, creates sub-agents dynamically, and collects the results.

        Args:
            message (Message): The incoming message containing the list and shard size.

        Returns:
            Message: A message containing the consolidated biographies.
        """
        logger.info(f"{self.name} processing message.")
        try:
            # Extract the list of celebrity names and shard size from the message
            data = message.content
            celebrity_names: List[str] = data.get('celebrity_names', [])
            shard_size: int = data.get('shard_size', 1)

            if not celebrity_names:
                raise ValueError("No celebrity names provided.")

            # Shard the list
            shards = [celebrity_names[i:i + shard_size] for i in range(0, len(celebrity_names), shard_size)]
            logger.info(f"Sharded list into {len(shards)} shards.")

            # Create sub-agents dynamically and process shards in parallel
            tasks = []
            for idx, shard in enumerate(shards):
                agent_name = f"ShardProcessingAgent_{idx}"
                agent = ShardProcessingAgent(name=agent_name)
                task = asyncio.create_task(agent.process(Message(content=shard, sender=self.name, recipient=agent_name)))
                tasks.append(task)

            # Gather results from all sub-agents
            sub_responses = await asyncio.gather(*tasks)

            # Consolidate the results
            biographies = [response.content for response in sub_responses if response.content]
            final_response = "\n\n".join(biographies)

            return Message(content=final_response, sender=self.name, recipient=message.sender)
        except Exception as e:
            logger.error(f"Error in {self.name}: {e}")
            return Message(
                content="An error occurred while processing the request.",
                sender=self.name,
                recipient=message.sender
            )
