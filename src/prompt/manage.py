from src.config.logging import logger


class TemplateManager:
    @staticmethod
    def load_template(template_path: str) -> str:
        try:
            with open(template_path, 'r') as file:
                return file.read()
        except FileNotFoundError as e:
            logger.error(f"Template file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading template: {e}")
            raise

    @staticmethod
    def fill_template(template_content: str, **kwargs) -> str:
        try:
            filled_template = template_content
            for key, value in kwargs.items():
                placeholder = f"{{{key}}}"
                filled_template = filled_template.replace(placeholder, value)
            return filled_template
        except Exception as e:
            logger.error(f"Error filling template: {e}")
            raise

    def load_and_fill_template(self, template_path: str, **kwargs) -> str:
        try:
            template_content = self.load_template(template_path)
            return self.fill_template(template_content, **kwargs)
        except Exception as e:
            logger.error(f"Error loading and filling template: {e}")
            raise