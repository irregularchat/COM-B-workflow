from openai import OpenAI
import os
from dotenv import load_dotenv
from colorama import init

# Define formatting
HEADER = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

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

def get_user_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        print("\nEOFError: Input stream ended unexpectedly.")
        return ""

def chat_with_ai(prompt, chat_history=[]):
    try:
        chat_history.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="gpt-4",
            messages=chat_history
        )
        ai_response = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": ai_response})
        return ai_response, chat_history
    except Exception as e:
        print(f"Error during chat with AI: {e}")
        return "", chat_history

def generate_question(area_of_focus, operational_objective, constraints, restraints, chat_history):
    # Generate a question based on the context using the AI
    question = ""
    prompt = (
        f"Think like a planner, In {area_of_focus}, trying to achieve: {operational_objective}, "
        f"Constraints: {constraints}, Restraints: {restraints}. Please provide a question that helps define the mission."
    )
    question, chat_history = chat_with_ai(prompt, chat_history)
    return question, chat_history

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
        question, chat_history = generate_question(area_of_focus, operational_objective, constraints, restraints, chat_history)
        if question:
            answer = get_user_input(question)
            if answer:
                chat_history.append({"role": "user", "content": answer})
        else:
            print("Error generating question.")

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

def parse_cog_response(response):
    # Parse the AI response to extract the Center of Gravity definitions
    cogs = response.split(";")[:3]  # Assuming AI provides semicolon-separated recommendations
    for i, cog in enumerate(cogs, 1):
        print(f"{i}. {cog.strip()}")
    return cogs

def define_cog(entity_type, area_of_focus, operational_objective, constraints, restraints, mission_statement):
    print(f"\nDefining Center of Gravity for {entity_type}...")

    # Initialize chat history and DIME questions tailored to the entity type
    chat_history = []
    dime_questions = {
        f"{BOLD}Diplomatic{ENDC}": f"What international alliances and diplomatic relations fortify {entity_type}'s position?",
        f"{BOLD}Information{ENDC}": f"Which communication and propaganda efforts are most influential for {entity_type}?",
        f"{BOLD}Military{ENDC}": f"What units or systems are crucial for {entity_type}'s success?",
        f"{BOLD}Economic{ENDC}": f"What economic policies and resources ensure {entity_type}'s sustained operations?"
    }

    # Asking DIME-related questions
    responses = {}
    for category, question in dime_questions.items():
        print(f"{HEADER}DIME Analysis{ENDC}")
        print(question)  # Show the question to the user
        response = get_user_input(f"{category} response for {entity_type} (leave blank if not applicable): ")
        if response:
            responses[category] = response
            chat_history.append({"role": "user", "content": response})

    # Build context from mission details and DIME responses
    mission_context = (
        f"Mission focus: {area_of_focus}, Objective: {operational_objective}, "
        f"Constraints: {constraints}, Restraints: {restraints}, Mission Statement: {mission_statement}"
    )
    additional_context = ", ".join(f"{k}: {v}" for k, v in responses.items())
    context_prompt = (
        f"Based on the mission details and {entity_type} specifics -- {mission_context}, {additional_context}. "
        "Please provide 5 potential centers of gravity; semicolon-separated; no markdown; no bullet points; no numbering; no commentary"
    )

    # Generate a prompt for AI to provide three recommendations
    prompt = context_prompt + " Please provide three potential centers of gravity."
    cog_definitions, chat_history = chat_with_ai(prompt, chat_history)

    # Display suggested CoGs
    cogs = cog_definitions.split(";")[:5]  # Assuming AI provides semicolon-separated recommendations
    for i, cog in enumerate(cogs, 1):
        print(f"{i}. {cog.strip()}")

    # Allow user interaction to select or modify the recommendations
    choice = get_user_input(f"Select a CoG to modify/accept (1-{len(cogs)}), or type 'new' to enter a new one: ")
    if choice.isdigit() and 1 <= int(choice) <= len(cogs):
        selected_cog = cogs[int(choice) - 1].strip()
        modify = get_user_input(f"Would you like to modify this CoG? {BOLD}(yes/no){ENDC}")
        if modify.lower() == "yes":
            new_cog = get_user_input("Enter your modified Center of Gravity: ")
            return new_cog
        else:
            return selected_cog
    elif choice.lower() == 'new':
        new_cog = get_user_input("Enter your new Center of Gravity: ")
        return new_cog
    else:
        print("Invalid choice. No changes made.")
        return None

def main():
    initialize_openai()
    print(f"{HEADER}Welcome to the Mission Definition Chatbot!{ENDC}")
    area_of_focus, operational_objective, constraints, restraints, mission_statement = define_mission()
    define_cog("friendly", area_of_focus, operational_objective, constraints, restraints, mission_statement)
    define_cog("enemy", area_of_focus, operational_objective, constraints, restraints, mission_statement)
    define_cog("host nation", area_of_focus, operational_objective, constraints, restraints, mission_statement)

if __name__ == "__main__":
    main()
