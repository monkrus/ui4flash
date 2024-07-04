import streamlit as st
import os
import google.generativeai as genai

# Check for API Key (with user-friendly message)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Please set the `GEMINI_API_KEY` environment variable.")
    st.stop()

# Gemini Model Configuration
model_name = "gemini-1.5-flash"
generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024
}

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name, generation_config=generation_config)

except Exception as e:
    st.error(f"Error configuring the Gemini model: {e}")
    st.stop()

# --- Streamlit Chat App ---

st.title("Gemini Chatbot (1.5 Flash) with Streamlit")

# Chat History Management (with scrollable container)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat()

# Display chat history in a scrollable container
with st.container():
    for msg in st.session_state.chat_history:
        st.markdown(f"**{msg['sender']}:** {msg['text']}")

# User input and send button
user_input = st.text_input("Your message:", key="user_input")

if st.button("Send", key="send_button") and user_input:
    # Send message and get response
    response = st.session_state.chat_session.send_message(user_input)

    # Update chat history
    st.session_state.chat_history.append({"sender": "User", "text": user_input})
    st.session_state.chat_history.append({"sender": "Gemini", "text": response.text})

    # Clear the input field 
    st.empty()  # Remove the existing widget
    user_input = st.text_input("Your message:", key="user_input")  # Create a new widget

    # Scroll to the bottom of the container after each message
    st.markdown(
        """
        <script>
            const container = document.querySelector('.stChatMessage');
            container.scrollTop = container.scrollHeight;
        </script>
        """,
        unsafe_allow_html=True,
    )
