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
    global client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set it in the .env file.")
    client = OpenAI(api_key=api_key)

# Function to get AI suggestions

# Function to get user input with a prompt
def get_user_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        print("\nEOFError: Input stream ended unexpectedly.")
        return ""

# Function to chat with AI for detailed responses
def chat_with_ai(prompt, chat_history=[]):
    try:
        chat_history.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(model="gpt-4",
                                                  messages=chat_history)
        ai_response = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": ai_response})
        return ai_response, chat_history
    except Exception as e:
        print(f"Error during chat with AI: {e}")
        return "", chat_history

def define_mission():
    global area_of_focus, operational_objective, constraints, restraints
    if not area_of_focus:
        area_of_focus = get_user_input("Enter the area of focus: ")
        if not area_of_focus:
            print("Area of focus cannot be empty.")
    if not operational_objective:
        operational_objective = get_user_input("Enter the operational objective: ")
        if not operational_objective:
            print("Operational objective cannot be empty.")
    if constraints == "None":
        constraints = get_user_input("Enter the constraints (optional): ")
        if not constraints:
            constraints = "None"
    if restraints == "None":
        restraints = get_user_input("Enter the restraints (optional): ")
        if not restraints:
            restraints = "None"

    # Gather questions to define the mission
    chat_history = []
    for i in range(3):
        question_prompt = f"What are three questions that can help define the mission? Consider '{area_of_focus}', '{operational_objective}', '{constraints}', '{restraints}'"
        question, chat_history = chat_with_ai(question_prompt, chat_history)
        if question:
            print(f"Question {i + 1}: {question}")
            answer = get_user_input(f"Answer to question {i + 1}: ")
            chat_history.append({"role": "user", "content": question})
            chat_history.append({"role": "user", "content": answer})
        else:
            print("Error getting AI suggestions for questions.")
            break

    # Create a mission statement based on the answers
    mission_statement = ""
    if chat_history:
        mission_statement, chat_history = chat_with_ai("Create a mission statement based on the answers.", chat_history)
    else:
        print("Error creating mission statement.")

    # Print the mission details
    print("Mission Details:")
    print(f"Mission Statement: {mission_statement}")
    print(f"Area of focus: {area_of_focus}")
    print(f"Operational objective: {operational_objective}")
    print("Limitations:")
    print(f"Constraints: {constraints}")
    print(f"Restraints: {restraints}")

    return area_of_focus, operational_objective, constraints, restraints, mission_statement

def main():
    initialize_openai()
    print("Welcome to the Mission Definition Chatbot!")
    details = define_mission()
    print("Mission defined successfully.")
    print("Thank you for using the Mission Definition Chatbot!")

if __name__ == "__main__":
    main()
