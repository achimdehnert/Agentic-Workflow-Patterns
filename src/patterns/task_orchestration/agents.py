from src.patterns.task_orchestration.message import Message
from src.patterns.task_orchestration.agent import Agent
from src.llm.generate import ResponseGenerator
from src.config.logging import logger 
from glob import glob
import asyncio
import json 
import os 

import re 

def extract_json_from_response(response_text):
    try:
        # Use regular expression to extract JSON content within <JSON>...</JSON>
        json_match = re.search(r'<JSON>(.*?)</JSON>', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()
            return json.loads(json_str)
        else:
            logger.error("No JSON content found in LLM response.")
            return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        return None
    




class CollectBooksAgent(Agent):
    async def process(self, message: Message) -> Message:
        logger.info(f"{self.name} collecting books.")
        folder_path = './data/patterns/task_orchestration/docs'  # Folder containing book text files
        book_files = glob(os.path.join(folder_path, '*.txt'))
        books = {
            "books": []
        }
        for idx, filepath in enumerate(book_files):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            title = os.path.splitext(os.path.basename(filepath))[0]
            
            books["books"].append({
                "id": f"doc{idx+1}",
                "title": title,
                "content": content,
                "filename": filepath
            })
        # Validate output against schema
    
        self.validate_output(books, './data/patterns/task_orchestration/schemas/book_collection_schema.json')
        return Message(content=books, sender=self.name, recipient=message.sender)








class PreprocessBooksAgent(Agent):
    async def process(self, message: Message) -> Message:
        logger.info(f"{self.name} preprocessing books.")
        input_data = message.content

        # Validate input against schema
        self.validate_input(input_data, './data/patterns/task_orchestration/schemas/book_collection_schema.json')

        # Initialize the response generator
        response_generator = ResponseGenerator()

        preprocessed_books = {"preprocessed_books": []}

        for book in input_data["books"]:
            book_id = book["id"]
            book_title = book["title"]
            book_content = book["content"]

            # Prepare the LLM input
            llm_input = (
                f"You are an expert in text processing. Given the raw text of a book, clean the text by removing any "
                f"markup, correcting OCR errors, and normalizing the formatting while preserving the original content. "
                f"Return the cleaned text only.\n\n"
                f"Book Title: {book_title}\n"
                f"Raw Book Text:\n{book_content}"
            )

            logger.info(f"Processing book '{book_title}' with ID '{book_id}' using LLM.")

            try:
                # Blocking function to run in a separate thread
                def blocking_call():
                    return response_generator.generate_response(
                        model_name='gemini-1.5-flash-001',
                        system_instruction='',
                        contents=[llm_input]
                    ).text.strip()

                # Execute the blocking LLM call in a separate thread
                cleaned_content = await asyncio.to_thread(blocking_call)

                # Add the cleaned book to the preprocessed_books list
                preprocessed_books["preprocessed_books"].append({
                    "id": book_id,
                    "title": book_title,
                    "content": cleaned_content
                })

            except Exception as e:
                logger.error(f"Failed to preprocess book '{book_title}' with ID '{book_id}': {e}")
                # Handle the failure as needed; here we skip the book
                continue

        # Validate the output against the schema
        self.validate_output(preprocessed_books, './data/patterns/task_orchestration/schemas/preprocessed_books_schema.json')

        return Message(content=preprocessed_books, sender=self.name, recipient=message.sender)




class ExtractKeyInfoAgent(Agent):
    async def process(self, message: Message) -> Message:
        logger.info(f"{self.name} extracting key information.")
        input_data = message.content

        # Validate input against schema
        self.validate_input(input_data, './data/patterns/task_orchestration/schemas/preprocessed_books_schema.json')

        # Initialize the response generator
        response_generator = ResponseGenerator()

        key_info = {"key_info": []}

        for book in input_data["preprocessed_books"]:
            book_id = book["id"]
            book_title = book["title"]
            book_content = book["content"]

            # Prepare the LLM input
            llm_input = (
    f"You are a literary analyst. Given the text of a book, extract the following key information:\n"
    f"- List of main characters (only names).\n"
    f"- Major themes explored in the book.\n"
    f"- Important plot points.\n\n"
    f"Provide the output in valid JSON format with keys 'characters', 'themes', and 'plot_points'. "
    f"Each 'characters' field must be an array of strings (character names only), and not include descriptions. "
    f"Do not include any explanations or additional text.\n"
    f"Wrap the JSON output within <JSON>{{...}}</JSON> tags.\n\n"
    f"Book Title: {book_title}\n"
    f"Book Text:\n{book_content}"
)

            logger.info(f"Extracting key information from book '{book_title}' with ID '{book_id}' using LLM.")

            try:
                # Blocking function to run in a separate thread
                def blocking_call():
                    return response_generator.generate_response(
                        model_name='gemini-1.5-flash-001',
                        system_instruction='',
                        contents=[llm_input]
                    ).text.strip()

                # Execute the blocking LLM call in a separate thread
                extraction_result = await asyncio.to_thread(blocking_call)

                # Log the raw LLM response
                logger.debug(f"LLM Response for book '{book_title}': {extraction_result}")

                # Extract JSON from LLM response
                extracted_data = extract_json_from_response(extraction_result)
                if not extracted_data:
                    logger.error(f"Failed to extract JSON for book '{book_title}'. Skipping.")
                    continue
                print(extracted_data, '---' * 38)
                # Ensure extracted data conforms to the expected schema structure
                characters = extracted_data.get("characters", [])
                themes = extracted_data.get("themes", [])
                plot_points = extracted_data.get("plot_points", [])

                if not isinstance(characters, list) or not all(isinstance(c, str) for c in characters):
                    logger.error(f"Invalid characters format for book '{book_title}'. Skipping.")
                    continue

                if not isinstance(themes, list) or not all(isinstance(t, str) for t in themes):
                    logger.error(f"Invalid themes format for book '{book_title}'. Skipping.")
                    continue

                if not isinstance(plot_points, list) or not all(isinstance(p, str) for p in plot_points):
                    logger.error(f"Invalid plot points format for book '{book_title}'. Skipping.")
                    continue

                # Add the extracted key information to the key_info list
                key_info["key_info"].append({
                    "book_id": book_id,
                    "characters": characters,
                    "themes": themes,
                    "plot_points": plot_points
                })

            except Exception as e:
                logger.error(f"Failed to extract key information from book '{book_title}' with ID '{book_id}': {e}")
                # Handle the failure as needed; here we skip the book
                continue

        # Validate the output against the schema
        self.validate_output(key_info, './data/patterns/task_orchestration/schemas/key_info_schema.json')

        return Message(content=key_info, sender=self.name, recipient=message.sender)






class GenerateSummariesAgent(Agent):
    async def process(self, message: Message) -> Message:
        logger.info(f"{self.name} generating summaries.")
        input_data = message.content

        # Validate input against schema
        self.validate_input(input_data, './data/patterns/task_orchestration/schemas/preprocessed_books_schema.json')

        # Initialize the response generator
        response_generator = ResponseGenerator()

        summaries = {"summaries": []}

        for book in input_data["preprocessed_books"]:
            book_id = book["id"]
            book_title = book["title"]
            book_content = book["content"]

            # Prepare the LLM input
            llm_input = (
                f"You are a professional book summarizer. Given the text of a book, provide a concise summary "
                f"that captures the main plot, characters, and themes. The summary should be around 200 words.\n\n"
                f"Provide the summary in valid JSON format with the key 'summary'. "
                f"Do not include any explanations or additional text.\n"
                f"Wrap the JSON output within <JSON>{{...}}</JSON> tags.\n\n"
                f"Book Title: {book_title}\n"
                f"Book Text:\n{book_content}"
            )

            logger.info(f"Generating summary for book '{book_title}' with ID '{book_id}' using LLM.")

            try:
                # Blocking function to run in a separate thread
                def blocking_call():
                    return response_generator.generate_response(
                        model_name='gemini-1.5-flash-001',
                        system_instruction='',
                        contents=[llm_input]
                    ).text.strip()

                # Execute the blocking LLM call in a separate thread
                summary_result = await asyncio.to_thread(blocking_call)

                # Log the raw LLM response
                logger.debug(f"LLM Response for book '{book_title}': {summary_result}")

                # Extract JSON from LLM response
                extracted_data = extract_json_from_response(summary_result)
                if not extracted_data or 'summary' not in extracted_data:
                    logger.error(f"Failed to extract summary for book '{book_title}'. Skipping.")
                    continue

                # Add the summary to the summaries list
                summaries["summaries"].append({
                    "book_id": book_id,
                    "summary": extracted_data['summary']
                })

            except Exception as e:
                logger.error(f"Failed to generate summary for book '{book_title}' with ID '{book_id}': {e}")
                # Handle the failure as needed; here we skip the book
                continue

        # Validate the output against the schema
        self.validate_output(summaries, './data/patterns/task_orchestration/schemas/summaries_schema.json')

        return Message(content=summaries, sender=self.name, recipient=message.sender)



class CompileReportAgent(Agent):
    async def process(self, message: Message) -> Message:
        logger.info(f"{self.name} compiling final report.")
        input_data = message.content

        # Validate inputs
        self.validate_input(input_data['task3'], './data/patterns/task_orchestration/schemas/key_info_schema.json')
        self.validate_input(input_data['task4'], './data/patterns/task_orchestration/schemas/summaries_schema.json')

        key_info_data = input_data['task3']
        summaries_data = input_data['task4']

        # Initialize the response generator
        response_generator = ResponseGenerator()

        report_sections = []

        for key_info_entry in key_info_data["key_info"]:
            book_id = key_info_entry["book_id"]

            # Find the corresponding summary
            summary_entry = next(
                (s for s in summaries_data["summaries"] if s["book_id"] == book_id), None)

            if not summary_entry:
                logger.warning(f"No summary found for book ID '{book_id}'. Skipping.")
                continue

            # Prepare the LLM input to format the report section
            llm_input = (
                f"You are a report compiler. Given the summary and key information of a book, "
                f"compile a well-formatted report section for this book. The report should include:\n"
                f"- Title of the book.\n"
                f"- Summary.\n"
                f"- List of main characters with descriptions.\n"
                f"- Major themes.\n"
                f"- Important plot points.\n\n"
                f"Provide the report section in a clear and structured format.\n\n"
                f"Book Title: {summary_entry['book_id']}\n"
                f"Summary:\n{summary_entry['summary']}\n\n"
                f"Characters:\n{key_info_entry['characters']}\n\n"
                f"Themes:\n{key_info_entry['themes']}\n\n"
                f"Plot Points:\n{key_info_entry['plot_points']}"
            )

            logger.info(f"Compiling report section for book ID '{book_id}' using LLM.")

            try:
                # Blocking function to run in a separate thread
                def blocking_call():
                    return response_generator.generate_response(
                        model_name='gemini-1.5-flash-001',
                        system_instruction='',
                        contents=[llm_input]
                    ).text.strip()

                # Execute the blocking LLM call in a separate thread
                report_section = await asyncio.to_thread(blocking_call)

                # Add the report section to the report_sections list
                report_sections.append(report_section)

            except Exception as e:
                logger.error(f"Failed to compile report section for book ID '{book_id}': {e}")
                # Handle the failure as needed; here we skip the book
                continue

        # Combine all report sections into the final report
        report = {
            "report": "\n\n".join(report_sections)
        }

        # Validate the output against the schema
        self.validate_output(report, './data/patterns/task_orchestration/schemas/final_report_schema.json')

        return Message(content=report, sender=self.name, recipient=message.sender)
