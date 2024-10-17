from typing import Any

class Message:
    """
    Represents a message exchanged between agents.

    Attributes:
        content (Any): The content of the message.
        sender (str): The name of the sender.
        recipient (str): The name of the recipient.
    """

    def __init__(self, content: Any, sender: str, recipient: str) -> None:
        """
        Initializes a new instance of the Message class.

        Args:
            content (Any): The content of the message.
            sender (str): The name of the sender.
            recipient (str): The name of the recipient.
        """
        self.content = content
        self.sender = sender
        self.recipient = recipient
