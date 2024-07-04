import os
import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai

# Configure the Google AI SDK
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
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

def send_message():
    input_text = entry.get()
    response = chat_session.send_message(input_text)
    output_text.insert(tk.END, f"You: {input_text}\n")
    output_text.insert(tk.END, f"AI: {response.text}\n\n")
    entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Google AI Chat")

# Create a text entry widget
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Create a button to send the message
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# Create a scrolled text widget to display the conversation
output_text = scrolledtext.ScrolledText(root, width=60, height=20)
output_text.pack(pady=10)

# Run the application
root.mainloop()