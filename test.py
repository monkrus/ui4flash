import streamlit as st
import os

import google.generativeai as genai

# Streamlit Title and Description
st.title("Generative AI Chat with Streamlit")
st.write("Talk to a powerful AI model and have creative conversations!")

# Environment Variable Check
if "GEMINI_API_KEY" not in os.environ:
    st.error(
        "Please set the GEMINI_API_KEY environment variable before running the app."
    )
    st.stop()

# Configure Generative AI Model
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Model and Chat Session Setup (moved outside the loop for efficiency)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

# User Input Field
user_input = st.text_input("Enter your message:")

# Send Message and Display Response (happens on button click)
if st.button("Send"):
    if user_input:
        response = chat_session.send_message(user_input)
        st.write(f"AI: {response.text}")
    else:
        st.warning("Please enter a message to send.")
