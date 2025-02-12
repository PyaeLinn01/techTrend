import streamlit as st
import google.generativeai as genai
import re
#import os

# Load API key securely
api_key = st.secrets["GEMINI_API_KEY"]
if not api_key:
    st.error("API key not found. Set GEMINI_API_KEY as an environment variable.")
    st.stop()

# Configure Gemini AI
genai.configure(api_key=api_key)

# Load the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Define Tech Categories
tech_categories = {
    "laptops": ["laptop", "notebook", "ultrabook", "MacBook", "ThinkPad", "gaming laptop", "business laptop"],
    "computers": ["desktop", "PC", "workstation", "server", "all-in-one", "custom PC"],
    "keyboards": ["keyboard", "mechanical keyboard", "wireless keyboard", "gaming keyboard", "key switches"],
    "market_insights": ["customer demand", "trends", "market analysis", "consumer behavior", "pricing", "sales data"],
}

def get_tech_related_answer(user_input):
    """Generates a concise, tech-related response using Gemini AI."""

    # Detect category
    matched_category = next(
        (category for category, keywords in tech_categories.items() if any(keyword in user_input.lower() for keyword in keywords)),
        None
    )

    if matched_category:
        prompt = f"Focus on trending tech devices and market insights. The user is asking about {matched_category}. Answer concisely: {user_input}"
        
        try:
            response = model.generate_content(prompt)
            full_response = response.text.strip()
            
            # Ensure relevance
            if re.search(r"\b(laptop|computer|PC|keyboard|market|trend|consumer|sales|demand|technology|hardware|pricing)\b", full_response.lower()):
                max_length = 1000
                return full_response[:max_length] + ("..." if len(full_response) > max_length else "")
            else:
                return "I can only answer questions about trending tech devices and market insights."
        
        except Exception as e:
            return f"Error: {e}"

    return "I can only answer questions about tech trends, laptops, computers, keyboards, and market insights."

# Streamlit UI
st.title("Tech Trends Chatbot 🤖")
st.write("Ask about trending laptops, computers, keyboards, and market insights!")

user_input = st.text_input("Enter your tech-related question:")
if st.button("Get Answer") and user_input:
    response = get_tech_related_answer(user_input)
    st.write("### 🤖 Response:")
    st.success(response)
