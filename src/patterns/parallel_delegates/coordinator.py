from src.patterns.parallel_delegates.message import Message
from src.patterns.parallel_delegates.agent import Agent
from src.config.logging import logger
from typing import List
from typing import Dict
from enum import Enum
import asyncio

class EntityType(Enum):
    FLIGHT = 1
    HOTEL = 2
    CAR_RENTAL = 3
    UNKNOWN = 4


class TravelPlannerAgent(Agent):
    def __init__(self, name: str, sub_agents: List[Agent]) -> None:
        super().__init__(name)
        self.sub_agents: Dict[str, Agent] = {agent.name: agent for agent in sub_agents}
        logger.info(f"{self.name} initialized with {len(self.sub_agents)} sub-agents.")

    async def perform_ner(self, query: str) -> Dict[EntityType, List[str]]:
        try:
            template = self.template_manager.create_template('coordinator', 'ner')
            system_instructions = template['system']
            user_instructions = self.template_manager.fill_template(template['user'], query=query)
            response_schema = template['schema']
            contents = [user_instructions]

            logger.info(f"Performing NER for query: {query}")
            response = self.response_generator.generate_response('gemini-1.5-pro-001', system_instructions, contents, response_schema)

            
            entities = eval(response.text.strip())  # Caution: Ensure safe eval usage
            entities = entities['entities']
            print(entities)
            
            return {EntityType[k.upper()]: v for k, v in entities.items() if v}
        except Exception as e:
            logger.error(f"Error during NER: {e}")
            return {}

    async def route_to_agents(self, entities: Dict[EntityType, List[str]]) -> List[Message]:
        tasks = []
        for entity_type, entity_values in entities.items():
            print(entity_type, '====>', entity_values)
            if entity_type == EntityType.FLIGHT:
                agent = self.sub_agents.get("FlightSearchAgent")
            elif entity_type == EntityType.HOTEL:
                agent = self.sub_agents.get("HotelSearchAgent")
            elif entity_type == EntityType.CAR_RENTAL:
                agent = self.sub_agents.get("CarRentalSearchAgent")
            else:
                continue

            if agent:
                task = asyncio.create_task(self.process_entity(agent, entity_type, entity_values))
                tasks.append(task)

        return await asyncio.gather(*tasks)

    async def process_entity(self, agent: Agent, entity_type: EntityType, entity_values: List[str]) -> Message:
        query = f"{entity_type.name}: {', '.join(entity_values)}"
        message = Message(content=query, sender=self.name, recipient=agent.name, metadata={"entity_type": entity_type.name})
        return await agent.process(message)

    async def consolidate_responses(self, query: str, sub_responses: List[Message]) -> str:
        template = self.template_manager.create_template('coordinator', 'consolidate')
        system_instructions = template['system']
        user_instructions = self.template_manager.fill_template(
            template['user'],
            query=query,
            flight_summary=next((r.content for r in sub_responses if r.metadata["entity_type"] == "FLIGHT"), ""),
            hotel_summary=next((r.content for r in sub_responses if r.metadata["entity_type"] == "HOTEL"), ""),
            car_rental_summary=next((r.content for r in sub_responses if r.metadata["entity_type"] == "CAR_RENTAL"), "")
        )
        contents = [user_instructions]

        logger.info("Generating final consolidated response for the user.")
        final_response = self.response_generator.generate_response('gemini-1.5-pro-001', system_instructions, contents)
        return final_response.text.strip()

    async def process(self, message: Message) -> Message:
        logger.info(f"{self.name} processing message: {message.content}")
        
        try:
            query = message.content

            # Perform Named Entity Recognition
            entities = await self.perform_ner(query)
            
            # Route to appropriate sub-agents and process in parallel
            sub_responses = await self.route_to_agents(entities)

            # Consolidate the final response
            final_response_text = await self.consolidate_responses(query, sub_responses)
            
            return Message(content=final_response_text, sender=self.name, recipient="User")
        except Exception as e:
            logger.error(f"Unexpected error during processing: {e}")
            return Message(content="I encountered an error while processing your request. Please try again later.", sender=self.name, recipient="User")
