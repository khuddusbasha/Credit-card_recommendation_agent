from crewai import Task, LLM, Crew
from agent2 import credit_assistant, recommendation_agent, llm
import re
import traceback

# Function to clean LLM output and remove thought processes
def clean_llm_output(output):
    """
    Clean the LLM output to remove thought processes and formatting
    """
    # Remove any "Thought:" statements
    output = re.sub(r'Thought:.*?\n', '', output, flags=re.DOTALL)
    
    # Remove any other typical LLM output markers
    output = re.sub(r'Final Answer:', '', output)
    output = re.sub(r'Answer:', '', output)
    
    # Trim whitespace
    output = output.strip()
    
    # Replace Indian Rupee symbol with "Rs." to avoid encoding issues
    output = output.replace("₹", "Rs.")
    
    # Ensure it ends with a question mark if it's a question
    if not output.endswith('?') and len(output) > 0 and not ":" in output[-10:]:
        output += '?'
        
    return output

# Function to generate the next question
def generate_question(qa_pairs):
    """
    Generate the next question based on previous Q&A pairs
    
    Args:
        qa_pairs: List of (question, answer) tuples from previous questions
        
    Returns:
        String containing the next question to ask
    """
    try:
        # Format conversation history - filter out any lines containing "Thought:"
        filtered_qa_pairs = []
        for q, a in qa_pairs:
            # Clean question and answer of any thought processes
            clean_q = clean_llm_output(q)
            clean_a = a
            filtered_qa_pairs.append((clean_q, clean_a))
            
        history = "\n".join([f"Q: {q}\nA: {a}" for q, a in filtered_qa_pairs])

        # Default question in case of any issues
        default_question = "What is your approximate monthly spending on credit cards?"
        
        if len(qa_pairs) == 0:
            # First question is fixed
            return "What is your primary goal for getting a new credit card? (e.g., cashback, travel rewards, building credit)"

        prompt = f"""
        You are a Credit Research Assistant helping users find the right credit card in India.

        Based on the previous conversation:
        {history}

        Ask the next insightful question about their credit habits, financial goals, or card preferences.
        Focus on information that would help recommend Indian credit cards.
        Keep it relevant, concise, and do not repeat earlier questions.
        Remember to focus on aspects relevant to the Indian credit card market.
        Use "Rs." instead of the Rupee symbol (₹) when referring to Indian currency.
        
        Important: Only respond with the question itself, nothing else. No explanations or thoughts.
        """

        task = Task(
            description=prompt,
            agent=credit_assistant,
            llm=llm,
            expected_output="A relevant follow-up question about credit needs for Indian users.",
            verbose=True
        )

        crew = Crew(
            agents=[credit_assistant],
            tasks=[task],
            verbose=True
        )

        # Use a try-except block for the LLM call
        try:
            result = crew.kickoff()
            result_str = str(result)
            
            # Clean the result
            cleaned_result = clean_llm_output(result_str)
            
            # Ensure we got an actual question (not empty or too long)
            if cleaned_result and len(cleaned_result) > 0 and len(cleaned_result) < 300:
                return cleaned_result
            else:
                return default_question
        except Exception as e:
            print(f"Error generating question: {str(e)}")
            print(traceback.format_exc())
            return default_question
    
    except Exception as e:
        print(f"Outer error in generate_question: {str(e)}")
        print(traceback.format_exc())
        return "What other factors are important to you when choosing a credit card?"

# Function to generate recommendations
def generate_recommendations(user_profile):
    """
    Generate credit card recommendations based on user profile
    
    Args:
        user_profile: String containing user responses
        
    Returns:
        String containing personalized credit card recommendations
    """
    try:
        recommendation_task = Task(
            description=f"""
            OBJECTIVE: Recommend the best Indian credit cards for this user.
            
            USER PROFILE:
            {user_profile}
            
            TASK:
            1. Analyze the user profile to understand their needs, preferences, and financial situation.
            2. Using your knowledge of Indian credit cards, identify the most suitable options.
            3. Provide 3-5 personalized credit card recommendations with the following details:
               - Card name and issuing bank
               - Key benefits and features
               - Annual fees and charges
               - Why this card matches the user's specific needs
               - Any special offers or promotions currently available
            4. Include eligibility considerations when relevant.
            5. Provide a brief conclusion summarizing your recommendations.
            
            Your recommendations should be specific to the Indian market, 
            and directly tied to the user's stated preferences.
            
            Some popular Indian credit cards to consider:
            - HDFC Bank Regalia/Diners Club Black
            - SBI Card PRIME/ELITE
            - ICICI Bank Amazon Pay Card
            - Axis Bank Flipkart Card
            - Axis Bank Atlas Credit Card
            - HDFC Bank Infinia Credit Card
            - SBI Card Elite
            - ICICI Emerald Credit Card  
            - American Express Platinum Travel Credit Card
            - Standard Chartered Ultimate Credit Card
            - Indusind Iconia Amex Credit Card
            - Yes First Credit Card
            
            IMPORTANT: Present your recommendations in a clean, direct format. Do not include phrases like "Thought:" or "I can give a great answer" or "Final Answer:" in your response.
            """,
            agent=recommendation_agent,
            llm=llm,
            expected_output="A detailed list of personalized Indian credit card recommendations.",
            verbose=True
        )
        
        crew = Crew(
            agents=[recommendation_agent],
            tasks=[recommendation_task],
            verbose=True
        )
        
        result = crew.kickoff()
        result_str = str(result)
        
        # Clean the result
        recommendations = clean_llm_output(result_str)

        # Clean up the recommendations to remove thought processes
        recommendations = recommendations.replace("Thought: I now can give a great answer", "")
        recommendations = recommendations.replace("Final Answer:", "")
        recommendations = recommendations.replace("Answer:", "")
        recommendations = recommendations.strip()
        
        # Replace Indian Rupee symbol with "Rs." to avoid encoding issues
        recommendations = recommendations.replace("₹", "Rs.")
        
        # Write recommendations to a file with UTF-8 encoding
        try:
            with open("card_recommendations.md", "w", encoding="utf-8") as f:
                f.write(recommendations)
        except Exception as e:
            # If UTF-8 fails, try with ASCII and replace problematic characters
            with open("card_recommendations.md", "w", encoding="ascii", errors="replace") as f:
                f.write(recommendations)
        
        return recommendations
    except Exception as e:
        # Return a helpful error message
        error_message = f"Error generating recommendations: {str(e)}"
        try:
            with open("card_recommendations.md", "w", encoding="utf-8") as f:
                f.write(error_message)
        except:
            with open("card_recommendations.md", "w", encoding="ascii", errors="replace") as f:
                f.write(error_message)
        return error_message
        '''
        # Further cleanup specific to recommendations
        result_str = result_str.replace("Thought: I now can give a great answer", "")
        result_str = result_str.replace("Final Answer:", "")
        result_str = result_str.replace("Answer:", "")
        result_str = result_str.strip()
        
        return result_str
    except Exception as e:
        error_message = f"Error generating recommendations: {str(e)}"
        print(error_message)
        print(traceback.format_exc())
        return error_message'''