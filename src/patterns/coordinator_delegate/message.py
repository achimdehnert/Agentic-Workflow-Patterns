
from typing import Optional 
from typing import Dict 


class Message:
    def __init__(self, content: str, sender: str, recipient: str, metadata: Optional[Dict] = None):
        self.content = content
        self.sender = sender
        self.recipient = recipient
        self.metadata = metadata or {}