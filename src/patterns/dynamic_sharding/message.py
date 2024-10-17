class Message:
    """
    A class representing a message exchanged between agents.

    Attributes:
        content (Any): The content of the message.
        sender (str): The sender's name.
        recipient (str): The recipient's name.
    """

    def __init__(self, content, sender: str, recipient: str) -> None:
        """
        Initializes the Message.

        Args:
            content (Any): The content of the message.
            sender (str): The sender's name.
            recipient (str): The recipient's name.
        """
        self.content = content
        self.sender = sender
        self.recipient = recipient
