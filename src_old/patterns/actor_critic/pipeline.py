
from src.patterns.actor_critic.history_manager import HistoryManager
from src.patterns.actor_critic.critic import Critic
from src.patterns.actor_critic.actor import Actor
from src.config.logging import logger


class ActorCriticPipeline:
    """
    Orchestrates the Actor-Critic workflow for generating, reviewing, and revising drafts.
    """

    def __init__(self, topic: str, num_cycles: int):
        self.topic = topic
        self.num_cycles = num_cycles
        self.history_manager = HistoryManager()
        self.actor = Actor(topic)
        self.critic = Critic(topic)

    def run(self) -> str:
        """
        Execute the Actor-Critic pipeline for the specified number of cycles.
        
        Returns:
            str: The final history in Markdown format.
        """
        for cycle in range(self.num_cycles):
            if cycle == 0:
                self.run_initial_cycle(cycle)
            else:
                self.run_revised_cycle(cycle)

        return self.history_manager.to_markdown()

    def run_initial_cycle(self, cycle: int) -> None:
        """
        Run the initial cycle of draft generation and review.
        
        Args:
            cycle (int): The current cycle number.
        """
        initial_draft = self.actor.generate_initial_draft()
        self.history_manager.add_entry(f"Initial Draft v{cycle}", initial_draft)
        
        initial_review = self.critic.review_draft(initial_draft)
        self.history_manager.add_entry("Initial Review", initial_review)

    def run_revised_cycle(self, cycle: int) -> None:
        """
        Run a revised cycle of draft revision and review.
        
        Args:
            cycle (int): The current cycle number.
        """
        revised_draft = self.actor.revise_draft(self.history_manager.history_md, cycle)
        self.history_manager.add_entry(f"Revised Draft v{cycle}", revised_draft)
        
        revised_review = self.critic.revise_review(self.history_manager.history_md, cycle)
        self.history_manager.add_entry(f"Revised Review v{cycle}", revised_review)


if __name__ == "__main__":
    topic = 'perplexity'
    num_cycles = 3

    try:
        pipeline = ActorCriticPipeline(topic=topic, num_cycles=num_cycles)
        final_history = pipeline.run()
        logger.info("Actor-Critic pipeline completed successfully.")
        print(final_history)
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
