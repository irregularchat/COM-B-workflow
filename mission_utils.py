from openai_utils import chat_with_ai
from utils import get_user_input  # Correct import
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()  # Ensure this is called early in your script

def generate_mission_statement(data):
    """
    Generates a mission statement based on the provided input data.
    
    Args:
        data (dict): The input data containing key elements for the mission statement.
        
    Returns:
        str: The generated mission statement.
    """
    # Extract relevant information from the data
    area_of_focus = data.get("area_of_focus", "the operational area")
    operational_objective = data.get("operational_objective", "achieving the desired end state")
    constraints = data.get("constraints", "no constraints specified")
    restraints = data.get("restraints", "no restraints specified")
    key_tasks = data.get("key_tasks", "execute the mission tasks effectively")

    # Create a basic mission statement template
    mission_statement = (
        f"In {area_of_focus}, with the objective of {operational_objective}, "
        f"considering constraints such as {constraints} and restraints such as {restraints}, "
        f"the mission is to {key_tasks}."
    )    
    return mission_statement

def refine_mission_statement(mission_statement):
    """
    Optionally refines the mission statement using OpenAI.
    
    Args:
        mission_statement (str): The initial mission statement.
        
    Returns:
        str: The refined mission statement.
    """
    # Generate a refined version of the mission statement using OpenAI
    prompt = f"Improve the following mission statement to make it more clear and impactful, write it in military style for Joint Operation:\n\n{mission_statement}"
    refined_statement = chat_with_ai(prompt)  # Updated function call
    return refined_statement

def define_mission():
    # Load the variables needed for the script
    area_of_focus = os.getenv("AREA_OF_FOCUS", "")
    operational_objective = os.getenv("OPERATIONAL_OBJECTIVE", "")
    constraints = os.getenv("CONSTRAINTS", "None")
    restraints = os.getenv("RESTRAINTS", "None")
    psychological_objective = os.getenv("PSYCHOLOGICAL_OBJECTIVE", "")
    spo = os.getenv("SPO", "")

    while area_of_focus == "":
        area_of_focus = get_user_input("Enter the area of focus: ")
        if area_of_focus == "":
            print("Area of focus cannot be empty.")

    while operational_objective == "":
        operational_objective = get_user_input("Enter the operational objective: ")
        if operational_objective == "":
            print("Operational objective cannot be empty.")

    constraints = get_user_input("Enter the constraints [Specific restrictions limiting military commanders' actions](optional) (e.g., time, resources, etc.): ")
    if constraints == "":
        constraints = "None"

    restraints = get_user_input("Enter the restraints [Limitations on the use of force in operations.](optional) (e.g., rules, regulations, etc.): ")
    if restraints == "":
        restraints = "None"
    
    operational_context = get_user_input("Enter the operational context (optional) (e.g., background, situation, etc.): ")
    if operational_context == "":
        operational_context = "None"

    print(f"Area of focus: {area_of_focus}")
    print(f"Operational objective: {operational_objective}")
    print(f"Constraints: {constraints}")
    print(f"Restraints: {restraints}")
    print(f"Operational context: {operational_context}")

    return area_of_focus, operational_objective, psychological_objective, constraints, restraints, operational_context

def influence_mission(area_of_focus, operational_objective, psychological_objective, constraints, restraints):
    spo = ""
    while psychological_objective == "":
        psychological_objective = get_user_input("Enter the psychological objective: ")
        if psychological_objective == "":
            print("Psychological objective cannot be empty.")
    while spo == "":
        spo = create_spo(area_of_focus, operational_objective, psychological_objective, constraints, restraints)
        if spo == "":
            print("SPO cannot be empty.")
    print(f"\n\nPsychological objective: {psychological_objective}")
    print(f"Supporting psychological objective: {spo}")
    return psychological_objective, spo

def parse_spo(spo):
    try:
        spo_list = spo.split('\n')
        return [s.strip() for s in spo_list if s.strip()]
    except Exception as e:
        print(f"Error parsing SPO: {e}")
        return []

def create_spo(area_of_focus, operational_objective, psychological_objective, constraints, restraints):
    chat_history = []
    prompt = (
        f"You are a Military PSYOP Planner. The Supporting Psychological Objective (SPO) for each series is the culmination point of achieved intermediate objectives. "
        f"The plan of execution becomes linear with intermediate objectives preceding SPO accomplishment, and SPOs preceding the achievement of the PO, ultimately supporting the commander's objectives. "
        f"Given the area of focus: '{area_of_focus}', operational objective: '{operational_objective}', and psychological objective: '{psychological_objective}', "
        f"create a list without numbers of specific, measurable, and observable supporting psychological objectives (SPOs) that can be achieved. "
        f"Consider the constraints: {constraints} and restraints: {restraints}. Each SPO should be one sentence per line, starting with TA and an appropriate action verb. No markdown. No commentary."
    )
    spo, chat_history = chat_with_ai(prompt, chat_history)
    parsed_spo = parse_spo(spo)
    
    print("\nSupporting Psychological Objectives (SPOs):")
    for idx, spo in enumerate(parsed_spo, start=1):
        print(f"{idx}. {spo}")

    selected_spo = select_spo(parsed_spo)
    return selected_spo

def select_spo(parsed_spo):
    while True:
        user_input = get_user_input("Select 1 SPO that is the best: ")
        if user_input.strip().isdigit():
            selected_spo_index = int(user_input) - 1
            if 0 <= selected_spo_index < len(parsed_spo):
                selected_spo = parsed_spo[selected_spo_index]
                break
            else:
                print("Invalid selection. Please enter a valid index.")
        else:
            print("Invalid input. Please enter a number.")
    print("\n####################")
    print(f"\n\nSelected SPO:\n1. {selected_spo}")

    while True:
        user_input = get_user_input("Would you like to modify the selected SPO? (yes/no): ")
        if user_input.lower() == 'yes':
            modification_prompt = get_user_input("Enter your modifications for the selected SPO: ")
            chat_history = []
            prompt = f"Modify the selected SPO: {modification_prompt}"
            spo, chat_history = chat_with_ai(prompt, chat_history)
            parsed_spo = parse_spo(spo)
            for idx, spo in enumerate(parsed_spo, start=1):
                print(f"{idx}. {spo}")
            return select_spo(parsed_spo)
        elif user_input.lower() == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    return selected_spo
def create_initial_behavior(spo, area_of_focus, operational_objective, psychological_objective, constraints, restraints):
    chat_history = []
    prompt = (
        f"Given the area of focus '{area_of_focus}', operational objective '{operational_objective}', psychological objective '{psychological_objective}', "
        f"and the supporting psychological objective (SPO) '{spo}', generate initial behaviors that would align with these objectives. "
        f"Consider constraints such as {constraints} and restraints such as {restraints}. List the initial behaviors as a single sentence per line."
    )
    
    initial_behavior, chat_history = chat_with_ai(prompt, chat_history)
    initial_behavior_list = initial_behavior.split('\n')
    print("\n####################")
    print("\n\nInitial Behaviors:")
    for idx, behavior in enumerate(initial_behavior_list, start=1):
        print(f"{idx}. {behavior.strip()}")

    selected_behavior = select_initial_behavior(initial_behavior_list)
    return selected_behavior

def select_initial_behavior(initial_behavior_list):
    while True:
        user_input = get_user_input("Select 1 initial behavior that is the best: ")
        if user_input.strip().isdigit():
            selected_behavior_index = int(user_input) - 1
            if 0 <= selected_behavior_index < len(initial_behavior_list):
                selected_behavior = initial_behavior_list[selected_behavior_index].strip()
                break
            else:
                print("Invalid selection. Please enter a valid index.")
        else:
            print("Invalid input. Please enter a number.")

    print(f"\n\nSelected Initial Behavior:\n1. {selected_behavior}")

    while True:
        user_input = get_user_input("Would you like to modify the selected behavior? (yes/no): ")
        if user_input.lower() == 'yes':
            modification_prompt = get_user_input("Enter your modifications for the selected behavior: ")
            chat_history = []
            prompt = f"Modify the selected behavior: {modification_prompt}"
            modified_behavior, chat_history = chat_with_ai(prompt, chat_history)
            initial_behavior_list = modified_behavior.split('\n')
            for idx, behavior in enumerate(initial_behavior_list, start=1):
                print(f"{idx}. {behavior.strip()}")
            return select_initial_behavior(initial_behavior_list)
        elif user_input.lower() == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    return selected_behavior

def refine_desired_behavior(initial_behavior):
    chat_history = []  # Initialize chat history for the conversation
    prompt = (
        f"The initial desired behavior is: '{initial_behavior}'. Create a list, not numbered, of potential refined behaviors. "
        f"Unknown who the target audience (TA) would be yet but phrase the desired behavior as 'TA verb_here xxx', but don't use markdown. "
        f"This must be behaviors that are measurable and that would have an impact towards the objective."
    )
    refined_behavior, chat_history = chat_with_ai(prompt, chat_history)
    refined_behavior_list = refined_behavior.split('\n')
    
    # Display the refined behaviors
    print("\n####################")
    for i, item in enumerate(refined_behavior_list):
        print(f"{i + 1}. {item.strip()}")
    
    # User input to select the refined behavior
    while True:
        try:
            user_input = int(get_user_input("Select a refined behavior from the list above: "))
            if 0 < user_input <= len(refined_behavior_list):
                refined_behavior_selected = refined_behavior_list[user_input - 1].strip()
                break
            else:
                print("Please select a valid number from the list above.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return refined_behavior_selected
def break_down_behavior(refined_behavior, area_of_focus):
    chat_history = []  # Initialize history for the conversation
    prompt = (
        f"The desired behavior is: '{refined_behavior}' in '{area_of_focus}'. Consider in backwards order starting from the desired behavior "
        f"and backwards from each previous required behavior but then list it in sequential order ending with the desired behavior. "
        f"Create a list of intermediate behaviors that lead to achieving this behavior. Each behavior must be a sentence and not numbered. "
        f"Don't use markdown, and only return sentences of the behavior without any commentary. Mark when an intermediate behavior is REQUIRED "
        f"and mark when it has MULTIPLE OPTIONS to complete such as can be done online or automatically. If multiple options, provide the multiple "
        f"options as in the steps Option A or Option B, etc."
    )
    intermediate_behaviors, chat_history = chat_with_ai(prompt, chat_history)
    intermediate_behaviors_list = intermediate_behaviors.split('\n')

    # Display the intermediate behaviors
    print("\n####################")
    for i, item in enumerate(intermediate_behaviors_list):
        print(f"{i + 1}. {item.strip()}")
    
    return intermediate_behaviors_list
