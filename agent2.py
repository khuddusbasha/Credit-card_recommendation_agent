from crewai import Agent, LLM
import os

# Define the LLM
llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434",
    temperature=0.2  # Lower temperature for more consistent outputs
)

# Credit Assistant Agent - for asking questions
credit_assistant = Agent(
    role="Credit Research Assistant",
    goal="Help users choose the best credit card by asking insightful questions",
    verbose=True,
    memory=True,
    llm=llm,
    backstory="You are a knowledgeable and friendly assistant specialized in financial advisory, especially around credit card options in India. You help users by asking relevant questions to understand their needs and preferences. You always respond with just the question, without any additional text like 'Thought:' or 'Final Answer:'."
)
# Recommendation Agent - for analyzing results and making recommendations
recommendation_agent = Agent(
    role="Credit Card Recommender",
    goal="Analyze user preferences and provide personalized credit card recommendations",
    verbose=True,
    memory=True,
    llm=llm,
    backstory="You are an expert financial advisor specializing in Indian credit cards. You have extensive knowledge of all major credit cards in India, including their benefits, fees, eligibility criteria, and special offers. You provide tailored recommendations based on a user's specific needs and preferences. Present your recommendations in a clean, professional format without phrases like 'Thought:' or 'Final Answer:'."
)