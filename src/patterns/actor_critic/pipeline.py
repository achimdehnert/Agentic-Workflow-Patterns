from src.patterns.actor_critic.manage import StateManager
from src.patterns.actor_critic.critic import Critic
from src.patterns.actor_critic.actor import Actor
from src.config.logging import logger


class Pipeline:
    def __init__(self, topic: str, num_cycles: int):
        self.topic = topic
        self.num_cycles = num_cycles
        self.history_manager = StateManager()
        self.actor = Actor(topic, './data/patterns/actor_critic/output', './config/patterns/actor_critic.yml')
        self.critic = Critic(topic, './data/patterns/actor_critic/output', './config/patterns/actor_critic.yml')

    def run(self) -> str:
        try:
            for cycle in range(self.num_cycles):
                self._run_cycle(cycle)
            return self.history_manager.to_markdown()
        except Exception as e:
            logger.error(f"Error in ActorCriticPipeline: {e}")
            raise

    def _run_cycle(self, cycle: int) -> None:
        if cycle == 0:
            print('here')
            self._run_initial_cycle()
        else:
            self._run_revised_cycle(cycle)

    def _run_initial_cycle(self) -> None:
        print('bar')
        initial_draft = self.actor.generate_initial_draft()
        print('bar3')
        self.history_manager.add_entry("Initial Draft v0", initial_draft)

        initial_review = self.critic.review_draft(initial_draft)
        self.history_manager.add_entry("Initial Review", initial_review)

    def _run_revised_cycle(self, cycle: int) -> None:
        revised_draft = self.actor.revise_draft(self.history_manager.history_md, cycle)
        self.history_manager.add_entry(f"Revised Draft v{cycle}", revised_draft)

        revised_review = self.critic.revise_review(self.history_manager.history_md, cycle)
        self.history_manager.add_entry(f"Revised Review v{cycle}", revised_review)


if __name__ == "__main__":
    try:
        topic = 'perplexity'
        num_cycles = 2
        pipeline = Pipeline(topic=topic, num_cycles=num_cycles)
        final_history = pipeline.run()
        logger.info("Actor-Critic pipeline completed successfully.")
        print(final_history)
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")