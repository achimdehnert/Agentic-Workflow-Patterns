# Pattern 3 - Semantic Router

## Overview

The **Semantic Routing** pattern implements an agentic workflow for intelligently routing user queries to specialized agents based on semantic intent. This pattern uses a coordinator-delegate architecture where a main TravelPlannerAgent determines the user's intent and routes requests to specialized sub-agents for specific travel-related tasks like flight booking, hotel searches, and car rentals.

The pattern leverages language models for intent detection and query processing, ensuring that each request is handled by the most appropriate specialized agent.

<p align="center">
    <img src="../../../img/framework/semantic_router.png" alt="Semantic Router" width="500"/>
</p>

## Key Components

### TravelPlannerAgent (Coordinator)
- Determines user intent through semantic analysis
- Routes queries to appropriate specialized agents
- Manages communication between sub-agents
- Consolidates and formats final responses
- Handles intent classification into categories:
  - FLIGHT
  - HOTEL
  - CAR_RENTAL
  - UNKNOWN

### Specialized Sub-Agents
- **FlightSearchAgent**
  - Processes flight-related queries
  - Generates optimized flight search parameters
  - Returns summarized flight information

- **HotelSearchAgent**
  - Handles hotel booking queries
  - Processes accommodation requests
  - Returns relevant hotel information

- **CarRentalSearchAgent**
  - Manages car rental inquiries
  - Processes vehicle rental requests
  - Returns car rental options and details

### Pipeline
- Orchestrates the entire workflow
- Initializes all agents
- Manages message flow
- Handles both single and batch query processing

## Process Flow

1. **Query Reception**
   - User submits a travel-related query
   - Pipeline creates a message object
   - Query is forwarded to TravelPlannerAgent

2. **Intent Detection**
   - TravelPlannerAgent analyzes query semantics
   - Determines specific travel intent
   - Routes to appropriate specialized agent

3. **Specialized Processing**
   - Sub-agent receives routed query
   - Generates optimized web search query
   - Processes and summarizes results
   - Returns formatted response

4. **Response Consolidation**
   - TravelPlannerAgent receives sub-agent response
   - Consolidates information
   - Formats final user-friendly response
   - Returns completed result
