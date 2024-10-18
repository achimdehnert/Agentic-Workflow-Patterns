# agent.py
import json
from jsonschema import validate
from src.config.logging import logger
from src.patterns.task_orchestration.message import Message

class Agent:
    def __init__(self, name: str) -> None:
        self.name = name

    async def process(self, message: 'Message') -> 'Message':
        raise NotImplementedError("This method should be implemented by subclasses.")

    def validate_input(self, data, schema_file):
        with open(schema_file, 'r') as f:
            schema = json.load(f)
        try:
            validate(instance=data, schema=schema)
            logger.info(f"{self.name} input validated against {schema_file}.")
        except Exception as e:
            logger.error(f"{self.name} input validation error: {e}")
            raise

    def validate_output(self, data, schema_file):
        with open(schema_file, 'r') as f:
            schema = json.load(f)
        try:
            validate(instance=data, schema=schema)
            logger.info(f"{self.name} output validated against {schema_file}.")
        except Exception as e:
            logger.error(f"{self.name} output validation error: {e}")
            raise
