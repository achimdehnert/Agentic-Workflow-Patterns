from src.patterns.dynamic_sharding.message import Message

class Agent:
    """
    Represents a base class for agents in the system.

    Attributes:
        name (str): The name of the agent.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes a new instance of the Agent class.

        Args:
            name (str): The name of the agent.
        """
        self.name = name

    async def process(self, message: Message) -> Message:
        """
        Processes a message and returns a response message.

        Args:
            message (Message): The message to be processed.

        Returns:
            Message: The response message.
        """
        raise NotImplementedError("Subclasses must implement the process method.")
