import openai
import os
from dotenv import load_dotenv

# Initialize global variables
model_name = "gpt-4"

def initialize_openai():
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY", "")

    if not api_key:
        raise ValueError("OpenAI API key not found. Please set it in the .env file.")
    
    # Set the API key for the OpenAI client
    openai.api_key = api_key

def get_ai_suggestions(prompt):
    try:
        response = openai.Completion.create(
            model=model_name,
            prompt=prompt,
            max_tokens=3000
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error getting AI suggestions: {e}")
        return ""

def chat_with_ai(prompt, chat_history=[]):
    try:
        # The latest API uses a 'messages' list for chat history, each message must be in a specific format
        if not chat_history:
            chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
        
        # Append the user's prompt to the chat history
        chat_history.append({"role": "user", "content": prompt})
        
        # Create the chat completion
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=chat_history
        )
        
        # Extract the assistant's reply
        ai_response = response.choices[0].message['content']
        
        # Append the assistant's reply to the chat history
        chat_history.append({"role": "assistant", "content": ai_response})
        
        return ai_response, chat_history
    except Exception as e:
        print(f"Error during chat with AI: {e}")
        return "", chat_history
