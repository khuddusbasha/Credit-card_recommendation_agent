import os
import streamlit as st
from task2 import generate_question
from recommend import get_card_recommendations
import time
st.set_page_config(page_title="Credit Assistant", layout="centered")
st.title("💳 Credit Research Assistant")
# Initialize session state
if "started" not in st.session_state:
    st.session_state.started = False
if "qa_pairs" not in st.session_state:
    st.session_state.qa_pairs = []
if "current_question" not in st.session_state:
    st.session_state.current_question = ""
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "next_question" not in st.session_state:
    st.session_state.next_question = ""
if "generating_question" not in st.session_state:
    st.session_state.generating_question = False
if "recommendations" not in st.session_state:
    st.session_state.recommendations = ""
if "recommendations_generated" not in st.session_state:
    st.session_state.recommendations_generated = False
# Function to safely generate a question
def safe_generate_question():
    try:
        return generate_question(st.session_state.qa_pairs)
    except Exception as e:
        st.error(f"Error generating question: {str(e)}")
        return "What other factors are important to you when choosing a credit card?"
# Step 1: Start the assistant
if not st.session_state.started:
    st.write("Welcome to the Credit Assistant.")
    st.write("This assistant will help you find the best credit card based on your needs.")
    st.write("You'll be asked 3 questions about your preferences and financial situation.")
    
    if st.button("Start Conversation"):
        st.session_state.started = True
        # Start with a fixed first question
        st.session_state.current_question = "What is your primary goal for getting a new credit card? (e.g., cashback, travel rewards, building credit)"
        st.rerun()
# Step 2: Conduct Q&A
if st.session_state.started:
    if st.session_state.question_count >= 3:  # Stop after 3 questions
        st.success("🎉 You've completed the questionnaire.")
        st.write("### Your Responses:")
        for q, a in st.session_state.qa_pairs:
            st.markdown(f"**Q:** {q}\n**A:** {a}")
            
        # Save responses to file
        with open("queries.md", "w", encoding="utf-8") as f:
            for q, a in st.session_state.qa_pairs:
                f.write(f"**Q:** {q}\n**A:** {a}\n\n")
                
        # Use the path for download
        st.download_button("📥 Download Responses", data=open("queries.md", encoding="utf-8").read(), file_name="queries.md")
        
        # Generate recommendations if not already done
        if not st.session_state.recommendations_generated:
            st.write("### Generating Credit Card Recommendations")
            with st.spinner("Analyzing your profile to find the best credit cards for you..."):
                try:
                    recommendations = get_card_recommendations(st.session_state.qa_pairs)
                    
                    # Clean up the recommendations to remove thought processes
                    recommendations = recommendations.replace("Thought: I now can give a great answer", "")
                    recommendations = recommendations.replace("Final Answer:", "")
                    recommendations = recommendations.replace("Answer:", "")
                    # Replace Rupee symbol to avoid encoding issues
                    recommendations = recommendations.replace("₹", "Rs.")
                    recommendations = recommendations.strip()
                    
                    st.session_state.recommendations = recommendations
                    st.session_state.recommendations_generated = True
                    st.success("✅ Recommendations generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error generating recommendations: {str(e)}")
                    if st.button("Try recommendations again"):
                        st.rerun()
        
        # Display recommendations
        if st.session_state.recommendations_generated:
            st.markdown("## 🎯 Your Personalized Credit Card Recommendations")
            
            # Clean up the recommendations one more time before displaying
            recommendations_clean = st.session_state.recommendations.replace("Thought: I now can give a great answer", "")
            recommendations_clean = recommendations_clean.replace("Final Answer:", "")
            recommendations_clean = recommendations_clean.replace("₹", "Rs.")
            recommendations_clean = recommendations_clean.strip()
            
            st.markdown(recommendations_clean)
            
            # Use file for download if available
            # In the section where recommendations are displayed and file is read for download:
            if os.path.exists("card_recommendations.md"):
                try:
                    with open("card_recommendations.md", "r", encoding="utf-8") as f:
                         recommendation_text = f.read()
                except:
        # Fallback to a more forgiving encoding if UTF-8 fails
                    with open("card_recommendations.md", "r", encoding="ascii", errors="replace") as f:
                        recommendation_text = f.read()
    
    # Clean the file content
                    recommendation_text = recommendation_text.replace("Thought: I now can give a great answer", "")
                    recommendation_text = recommendation_text.replace("Final Answer:", "")
                    recommendation_text = recommendation_text.strip()
    
                    st.download_button(
                        "📥 Download Recommendations", 
                        data=recommendation_text, 
                        file_name="credit_card_recommendations.md"
                        )

            
            st.write("### Thank you for using the Credit Research Assistant!")
            st.write("We hope these recommendations help you find the perfect credit card for your needs.")
            
        st.stop()
    st.subheader("Please answer the following question:")
    
    # Display progress
    progress_value = st.session_state.question_count / 3
    st.progress(progress_value)
    st.write(f"Question {st.session_state.question_count + 1} of 3")
    
    # Display current question
    user_response = st.text_input(st.session_state.current_question, key=f"q{st.session_state.question_count}")
    
    # Save response and generate next question
    if st.button("Submit Answer"):
        if user_response:
            # Save the current Q&A pair
            st.session_state.qa_pairs.append((st.session_state.current_question, user_response))
            st.session_state.question_count += 1
            
            # Get next question if we haven't reached the limit
            if st.session_state.question_count < 3:  # Changed from 5 to 3
                st.session_state.generating_question = True
                
                # Use a spinner but don't wrap the actual LLM call
                with st.spinner("Generating next question..."):
                    # Process indicator to show work is happening
                    st.session_state.next_question = safe_generate_question()
                
                st.session_state.current_question = st.session_state.next_question
                st.session_state.generating_question = False
            
            st.rerun()