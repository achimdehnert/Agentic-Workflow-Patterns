# Pattern 1: Reflection

## Overview

The **Reflection** pattern implements an iterative content generation and refinement system using an Actor-Critic framework. This pattern enables self-improving content generation through continuous feedback loops between an Actor (content generator) and a Critic (content reviewer).

The pattern follows an iterative workflow where the Actor generates content, the Critic reviews it, and then both components revise their work based on the accumulated state history. This process continues for a specified number of cycles, leading to progressively refined content.

<p align="center">
    <img src="../../../img/framework/reflection.png" alt="Reflection" width="500"/>
</p>

## Key Components

### Actor

The Actor is responsible for content generation and revision:
- Generates initial content drafts based on a given topic
- Revises drafts based on the Critic's feedback and previous versions
- Maintains version history of drafts

Key classes:
- `Actor`: Main agent class for content generation
- `DraftGenerator`: Generates initial drafts
- `RevisionGenerator`: Produces revised versions of drafts

### Critic

The Critic provides feedback and analysis:
- Reviews content produced by the Actor
- Generates detailed feedback and suggestions
- Revises its reviews based on the evolution of content
- Maintains version history of reviews

### Runner (Pipeline)

The Runner orchestrates the entire workflow:
- Manages the interaction between Actor and Critic
- Maintains state across multiple revision cycles
- Coordinates the generation-review-revision loop
- Produces final output in markdown format

## Process Flow

1. **Initialization**
   - Runner is created with model configurations, topic, and number of cycles
   - Actor and Critic agents are initialized
   - State manager is prepared to track workflow history

2. **Initial Cycle**
   - Actor generates the first draft based on the topic
   - Critic reviews the initial draft
   - Both outputs are saved to state history

3. **Revision Cycles**
   - Actor generates a revised draft based on complete history
   - Critic provides updated review based on new draft and previous history
   - Both new versions are added to state history
   - Process repeats for specified number of cycles

4. **Final Output**
   - Complete history is formatted as markdown
   - Contains all drafts and reviews from all cycles