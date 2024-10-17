from src.patterns.dynamic_sharding.message import Message
from src.patterns.dynamic_sharding.agent import Agent
from src.patterns.web_search.pipeline import run  
from src.config.logging import logger
from typing import List
import asyncio


class ShardProcessingAgent(Agent):
    """
    An agent that processes a shard of celebrity names by fetching their biographies
    using web search.

    Attributes:
        name (str): The name of the shard processing agent.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes the ShardProcessingAgent.

        Args:
            name (str): The name of the agent.
        """
        super().__init__(name)
        logger.info(f"{self.name} initialized.")

    async def process(self, message: Message) -> Message:
        """
        Processes the shard by fetching biographies for each celebrity in the shard.

        Args:
            message (Message): The message containing the shard (list of celebrity names).

        Returns:
            Message: A message containing the concatenated biographies.
        """
        logger.info(f"{self.name} processing shard.")
        try:
            celebrity_names: List[str] = message.content
            tasks = []

            # Create tasks to fetch biographies for each celebrity
            for name in celebrity_names:
                task = asyncio.create_task(self.fetch_biography(name))
                tasks.append(task)

            # Gather biographies
            biographies = await asyncio.gather(*tasks)
            shard_biography = "\n\n".join(biographies)

            return Message(content=shard_biography, sender=self.name, recipient=message.sender)
        except Exception as e:
            logger.error(f"Error in {self.name}: {e}")
            return Message(
                content="An error occurred while processing the shard.",
                sender=self.name,
                recipient=message.sender
            )

    async def fetch_biography(self, celebrity_name: str) -> str:
        """
        Fetches the biography of a celebrity using web search.

        Args:
            celebrity_name (str): The name of the celebrity.

        Returns:
            str: The biography of the celebrity.
        """
        logger.info(f"{self.name} fetching biography for {celebrity_name}.")
        try:
            # Use the run function to perform web search asynchronously
            biography = await asyncio.to_thread(run, f"{celebrity_name} biography")
            return f"Biography of {celebrity_name}:\n{biography}"
        except Exception as e:
            logger.error(f"Error fetching biography for {celebrity_name}: {e}")
            return f"Could not fetch biography for {celebrity_name}."
