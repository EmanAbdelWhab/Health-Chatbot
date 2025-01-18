import os
import streamlit as st
import google.generativeai as genai

# Load API Key securely
API_KEY = 'your_api_key_here'
if not API_KEY:
    raise ValueError("API key not found. Please set the 'GEMINI_API_KEY' environment variable.")

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Function to create the health expert chatbot model
def create_health_expert_chatbot():
    generation_config = {
        "temperature": 0.8,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction="Act as a highly knowledgeable health expert and doctor. classfiy what the patient has based on the input, patient symptoms, diagnoses, and relevant health topics. Refuse to engage in any non-medical conversations.and If the disease not dangerous make the response less words"
    )
    return model

# Function to get diagnosis based on user input
def get_diagnosis(user_input):
    """Send user input to the chatbot and retrieve the response."""
    if not user_input.strip():
        return "Please describe your symptoms clearly so I can provide accurate advice."

    model = create_health_expert_chatbot()
    chat_session = model.start_chat(history=[ 
        {"role": "user", "parts": ["Hi, doctor."]},
        {"role": "model", "parts": ["Hello! I am here to help with any health concerns. Please describe your symptoms or medical issue, and I will assist you."]}
    ])
    
    try:
        response = chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit interface
def main():
    st.title("Health Expert Chatbot")
    st.write("Welcome to the Health Expert Chatbot! Please describe your symptoms or medical concerns.")
    
    # Chat history container
    chat_history = []
    st.markdown(
        """
        <style>
        body {
            background-color: #f4f7fc;
            font-family: 'Arial', sans-serif;
        }

        .stTextInput {
            position: fixed;
            bottom: 50px;
            left: 20px;
            width: 75%;
            height: 40px;
            padding: 8px 15px;
            font-size: 16px;
            border-radius: 25px;
            border: 1px solid #ccc;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .stButton>button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 120px;
            height: 40px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border-radius: 25px;
            border: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            cursor: pointer;
        }

        .stButton>button:hover {
            background-color: #45a049;
        }

        .stButton>button:active {
            transform: scale(0.98);
        }

        </style>
        """, 
        unsafe_allow_html=True
    )

    # User input for symptoms
    user_input = st.text_input("Describe your symptoms...")

    if st.button("Send"):
        if user_input:
            # Get diagnosis response
            response = get_diagnosis(user_input)
            
            # Display chat history
            chat_history.append(f"User: {user_input}")
            chat_history.append(f"Doctor: {response}")
            
            # Display chat
            for message in chat_history:
                st.write(message)
        else:
            st.warning("Please enter a symptom description.")

if __name__ == "__main__":
    main()
