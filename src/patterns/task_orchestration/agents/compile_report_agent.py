from src.patterns.task_orchestration.message import Message
from src.patterns.task_orchestration.agent import Agent
from src.config.logging import logger 
import asyncio


class CompileReportAgent(Agent):
    async def process(self, message: Message) -> Message:
        logger.info(f"{self.name} compiling final report.")
        input_data = message.content
        self.validate_input(input_data['task3'], 'key_info_schema.json')
        self.validate_input(input_data['task4'], 'summaries_schema.json')
        await asyncio.sleep(1)
        # Simulate report compilation
        report_sections = []
        for key_info_entry in input_data['task3']["key_info"]:
            summary_entry = next(
                (s for s in input_data['task4']["summaries"] if s["book_id"] == key_info_entry["book_id"]), None)
            if summary_entry:
                report_sections.append(
                    f"Book ID: {key_info_entry['book_id']}\n"
                    f"Title: {summary_entry['book_id']}\n"
                    f"Summary: {summary_entry['summary']}\n"
                    f"Characters: {', '.join(key_info_entry['characters'])}\n"
                    f"Themes: {', '.join(key_info_entry['themes'])}\n"
                    f"Plot Points: {', '.join(key_info_entry['plot_points'])}\n"
                )
        report = {
            "report": "\n".join(report_sections)
        }
        self.validate_output(report, 'final_report_schema.json')
        return Message(content=report, sender=self.name, recipient=message.sender)