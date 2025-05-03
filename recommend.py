from task2 import generate_recommendations

def get_card_recommendations(qa_pairs):
    """
    Generate credit card recommendations based on user profile
    
    Args:
        qa_pairs: List of (question, answer) tuples from the user
        
    Returns:
        String containing personalized credit card recommendations
    """
    try:
        # Format the user profile based on Q&A pairs
        user_profile = "\n".join([f"Question: {q}\nAnswer: {a}" for q, a in qa_pairs])
        
        # Call the function from task2.py
        recommendations = generate_recommendations(user_profile)
        
        # Clean up the recommendations to remove thought processes
        recommendations = recommendations.replace("Thought: I now can give a great answer", "")
        recommendations = recommendations.replace("Final Answer:", "")
        recommendations = recommendations.replace("Answer:", "")
        recommendations = recommendations.replace("₹", "Rs.")
        recommendations = recommendations.strip()
        
        # Write recommendations to a file with error handling for encoding issues
        try:
            with open("card_recommendations.md", "w", encoding="utf-8") as f:
                f.write(recommendations)
        except UnicodeEncodeError:
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