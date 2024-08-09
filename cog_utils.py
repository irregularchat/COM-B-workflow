import os
from dotenv import load_dotenv
from openai_utils import get_ai_suggestions
from utils import get_user_input

# Define text formatting constants
HEADER = '\033[95m'
BOLD = '\033[1m'
ENDC = '\033[0m'

# Load environment variables
load_dotenv()

def parse_cog_response(response):
    """
    Parses the AI-generated response to extract COG definitions.
    
    Args:
        response (str): The response text from AI containing COG suggestions.
        
    Returns:
        list: A list of COGs extracted from the response.
    """
    cogs = response.split(";")[:5]  # Assuming AI provides semicolon-separated recommendations
    for i, cog in enumerate(cogs, 1):
        print(f"{i}. {cog.strip()}")
    return [cog.strip() for cog in cogs]

def define_cog(entity_type, area_of_focus, operational_objective, constraints, restraints, mission_statement):
    """
    Defines the Center of Gravity (COG) for a given entity (e.g., friendly, partner, competitor).
    
    Args:
        entity_type (str): The type of entity (e.g., friendly, partner, competitor).
        area_of_focus (str): The area of focus for the mission.
        operational_objective (str): The operational objective.
        constraints (str): Any constraints on the mission.
        restraints (str): Any restraints on the mission.
        mission_statement (str): The mission statement.
        
    Returns:
        str: The selected or defined COG.
    """
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

    # Generate COG suggestions using OpenAI
    cog_definitions = get_ai_suggestions(context_prompt)

    # Display suggested COGs
    cogs = parse_cog_response(cog_definitions)

    # Allow user interaction to select or modify the recommendations
    choice = get_user_input(f"Select a COG to modify/accept (1-{len(cogs)}), or type 'new' to enter a new one: ")
    if choice.isdigit() and 1 <= int(choice) <= len(cogs):
        selected_cog = cogs[int(choice) - 1].strip()
        modify = get_user_input(f"Would you like to modify this COG? {BOLD}(yes/no){ENDC}")
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
