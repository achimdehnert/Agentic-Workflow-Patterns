class Message:
    """
    A class representing a message exchanged between agents.

    Attributes:
        content (Any): The content of the message.
        sender (str): The sender's name.
        recipient (str): The recipient's name.
        metadata (dict): Additional metadata for the message.
    """

    def __init__(self, content, sender: str, recipient: str, metadata: dict = None) -> None:
        """
        Initializes the Message.

        Args:
            content (Any): The content of the message.
            sender (str): The sender's name.
            recipient (str): The recipient's name.
            metadata (dict, optional): Additional metadata. Defaults to None.
        """
        self.content = content
        self.sender = sender
        self.recipient = recipient
        self.metadata = metadata or {}
