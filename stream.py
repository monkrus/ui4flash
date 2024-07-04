import streamlit as st
import google.generativeai as genai
import os

# Configure the API key for Google Generative AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Define generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Initialize chat history in session state if not already present
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Start a chat session with the current history
chat_session = model.start_chat(history=st.session_state.chat_history)

st.title("Generative AI Chat")

# Input for the user's message
user_input = st.text_input("Enter your message:")

if st.button("Send"):
    # Send the user's message to the chat session and get the response
    response = chat_session.send_message(user_input)
    # Append user input and AI response to the chat history
    st.session_state.chat_history.append({"role": "user", "parts": [{"text": user_input}]})
    st.session_state.chat_history.append({"role": "model", "parts": [{"text": response.text}]})
    
    # Display the chat history
    for chat in st.session_state.chat_history:
        if "parts" in chat and chat["parts"]:
            st.write(f"{chat['role'].capitalize()}: {chat['parts'][0]['text']}")
