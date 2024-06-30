from openai import OpenAI
import os
from dotenv import load_dotenv

# Import the OpenAI API key from a separate .env file
load_dotenv()

# Initialize area of focus, operational objective, constraints, restraints from the .env file
area_of_focus = os.getenv("AREA_OF_FOCUS", "")
operational_objective = os.getenv("OPERATIONAL_OBJECTIVE", "")
constraints = os.getenv("CONSTRAINTS", "None")
restraints = os.getenv("RESTRAINTS", "None")

def initialize_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OpenAI API key not found. Please set it in the .env file.")
    return OpenAI(api_key=api_key)

# Function to get AI suggestions
def get_ai_suggestions(client, prompt):
    try:
        response = client.completions.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=300
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error getting AI suggestions: {e}")
        return ""

# Function to get user input with a prompt
def get_user_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        print("\nEOFError: Input stream ended unexpectedly.")
        return ""

# Function to chat with AI for detailed responses
def chat_with_ai(client, prompt, chat_history=[]):
    try:
        chat_history.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=chat_history
        )
        ai_response = response.choices[0].message["content"]
        chat_history.append({"role": "assistant", "content": ai_response})
        return ai_response, chat_history
    except Exception as e:
        print(f"Error during chat with AI: {e}")
        return "", chat_history
    
def define_mission(client):
    global area_of_focus, operational_objective, constraints, restraints

    if not area_of_focus:
        while area_of_focus == "":
            area_of_focus = get_user_input("Enter the area of focus: ")
            if area_of_focus == "":
                print("Area of focus cannot be empty.")

    if not operational_objective:
        while operational_objective == "":
            operational_objective = get_user_input("Enter the operational objective: ")
            if operational_objective == "":
                print("Operational objective cannot be empty.")

    if constraints == "None":
        constraints = get_user_input("Enter the constraints (optional) (e.g., time, resources, etc.): ")
        if constraints == "":
            constraints = "None"

    if restraints == "None":
        restraints = get_user_input("Enter the restraints (optional) (e.g., rules, regulations, etc.): ")
        if restraints == "":
            restraints = "None"
    
    # send gpt the mission details and have it ask 3 questions to help define the mission and store the answers 
    # iterate 3 times to get the questions asked by gpt and answers from user then answer goes into chat history to create more questions
    chat_history = []
    for i in range(3):
        question_prompt = f"What are three questions that can help define the mission? Consider '{area_of_focus}', '{operational_objective}', '{constraints}', '{restraints}'"
        question = get_ai_suggestions(client, question_prompt)
        if question:
            print(f"Question {i + 1}: {question}")
            answer = get_user_input(f"Answer to question {i + 1}: ")
            if answer:
                chat_history.append({"role": "user", "content": answer})
                chat_history.append({"role": "assistant", "content": question})
            else:
                print("Answer cannot be empty.")
                break
        else:
            print("Error getting AI suggestions for questions.")
            break
    
    # create a mission statement with the answers to the questions and the other mission variables use the questions and answers previously stored in chat history use chat_with_ai function
    mission_statement = ""
    if chat_history:
        mission_statement, chat_history = chat_with_ai(client, "Create a mission statement based on the answers to the questions.", chat_history)
    else:
        print("Error creating mission statement.")
    
    # print the mission details
    print("Mission Details:")
    print(f"Mission Statement: {mission_statement}")
    print(f"Area of focus: {area_of_focus}")
    print(f"Operational objective: {operational_objective}")
    print("Limitations:")
    print(f"Constraints: {constraints}")
    print(f"Restraints: {restraints}")
    
    return area_of_focus, operational_objective, constraints, restraints, mission_statement

def main():
    client = initialize_openai()
    print("Welcome to the Mission Definition Chatbot!")
    area_of_focus, operational_objective, constraints, restraints, mission_statement = define_mission(client)
    print("Mission defined successfully.")
    print("Thank you for using the Mission Definition Chatbot!")

if __name__ == "__main__":
    main()
