import openai
import os
import argparse
from dotenv import load_dotenv

# Import the OpenAI API key from a separate .env file
load_dotenv()
def initialize_openai(api_key):
    openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to get user input with a prompt
def get_user_input(prompt):
    return input(prompt)

# Function to get AI suggestions
def get_ai_suggestions(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003", # Use the davinci-003 model for text completion instead of a higher capacity model because of the token limit
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to chat with AI for detailed responses
def chat_with_ai(prompt, chat_history=[]):
    chat_history.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-4o", # Use the GPT-4 0 model for chat completion
        messages=chat_history
    )
    ai_response = response.choices[0].message['content']
    chat_history.append({"role": "assistant", "content": ai_response})
    return ai_response, chat_history
def define_mission():
    while area_of_focus == "":
        area_of_focus = get_user_input("Enter the area of focus: ")
        if area_of_focus == "":
            print("Area of focus cannot be empty.")
    print(f"Area of focus: {area_of_focus}")
    while operational_objective == "":
        operational_objective = get_user_input("Enter the operational objective: ")
        if operational_objective == "":
            print("Operational objective cannot be empty.")
    print(f"Operational objective: {operational_objective}")
    while psychological_objective == "":
        psychological_objective = get_user_input("Enter the psychological objective: ")
        if psychological_objective == "":
            print("Psychological objective cannot be empty.")
    print(f"Psychological objective: {psychological_objective}")
    constraints = get_user_input("Enter the constraints (optional) (e.g., time, resources, etc.): ")
    #if constraints is left blank than the constraints will be set to none
    if constraints == "":
        constraints = "None"
    print(f"Constraints: {constraints}")
    restaints = get_user_input("Enter the restraints (optional) (e.g., rules, regulations, etc.): ")
    #if restraints is left blank than the restraints will be set to none
    if restraints == "":
        restraints = "None"

def create_spo(area_of_focus, operational_objective, psychological_objective, constraints, restraints):
    chat_history = [] # Initialize chat history for the conversation
    # prompt gpt to create a specific, measurable, and observable supporting psychological objective (SPO)
    # prompt to gpt should return a numbered list of SPOs which python will parse and return as a list of strings for user to select from and modify as needed
    prompt = f"You are a Military PSYOP Planner. Given the area of focus: '{area_of_focus}', operational objective: '{operational_objective}', and psychological objective: '{psychological_objective}', create list of specific, measurable, and observable supporting psychological objectives (SPOs) that can be achieved. Consider the constraints: {constraints} and restraints: {restraints}."
    chat_with_ai(prompt, chat_history)
    return spo

def parse_spo(spo):
    #parse the spo list and return a list of strings
    spo_list = []
    for i in range(len(spo)):
        spo_list.append(spo
    return spo_list

def create_initial_behavior(spo, area_of_focus, operational_objective, psychological_objective, constraints, restraints):
    chat_history = [] # Initialize chat history for the conversation
    # prompt gpt to create a specific, measurable, and observable initial behavior
    # prompt to gpt should return a numbered list of initial behaviors which python will parse and return as a list of strings for user to select from and modify as needed
    prompt = f"What behavior in {area_of_focus} can occurate that would help to partially or fully achieve {spo} and get closer to '{operational_objective}' by '{psychological_objective}' considering constraints: {constraints}, and restraints: {restraints}, create a numbered list of 3 different behaviors and that could achive this that could be measured in some way."
    chat_with_ai(prompt, chat_history)
    return initial_behavior
    
# Function to refine the desired behavior
def refine_desired_behavior(initial_behavior):
    chat_history = [] # Initialize chat history for the conversation
    prompt = f"The initial desired behavior is: '{initial_behavior}'. How can we make this behavior more specific and measurable?"
    refined_behavior, chat_history = chat_with_ai(prompt, chat_history)
    while True:
        print(f"Refined behavior suggestion: {refined_behavior}")
        user_input = get_user_input("Is this refined behavior specific and measurable? (yes/no): ")
        if user_input.lower() == 'yes':
            break
        else:
            #get user input to refine the behavior then send it to gpt to refine further
            gpt_instructions = get_user_input("How should this behavior be refined?: ")
            prompt = "rifine the behavior further using: {gpt_instructions}"
            refined_behavior, chat_history = chat_with_ai(prompt, chat_history)
            # loop back to the top to prompt the user again
    return refined_behavior

def parse_intermediate_behaviors(intermediate_behaviors):
    #parse the intermediate behaviors list and return a list of strings
    intermediate_behaviors_list = []
    for i in range(len(intermediate_behaviors)):
        intermediate_behaviors_list.append(intermediate_behaviors)
    return intermediate_behaviors_list
# Function to break down the desired behavior into intermediate behaviors
def break_down_behavior(refined_behavior):
    chat_history = [] # Initialize history for the conversation
    prompt = f"The desired behavior is: '{refined_behavior}'. Consider in backwards order starting from the desired behavior and backwards from each previous required behavior but then list it in sequental order ending with the desired behavior. What are some intermediate behaviors that lead to achieving this behavior?"
    intermediate_behaviors, chat_history = chat_with_ai(prompt, chat_history)
    while True:
        parse_intermediate_behaviors(intermediate_behaviors)
        print(f"/nIntermediate behaviors suggestion: {intermediate_behaviors_list}")
        user_input = get_user_input("Are these intermediate behaviors acceptable? (yes/no): ")
        if user_input.lower() == 'yes':
            break 
        else:
            print("You may identify intermediate behaviors by number (e.g replace '1' with 'TA greets the customer' OR e.g replace expand after 4) ")
            prompt = "How can we refine these intermediate behaviors?"
            intermediate_behaviors, chat_history = chat_with_ai(prompt, chat_history)
    return intermediate_behaviors
def parse_pta(pta):
    #parse the pta list and return a list of strings
    pta_list = []
    for i in range(len(pta)):
        pta_list.append(pta)
    return pta_list

def select_potential_target_audience(desired_behavior, intermediate_behaviors, constraints, restraints):
    chat_history = [] # Initialize chat history for the conversation
    # prompt gpt to create a potential target audience
    # prompt to gpt should return a numbered list of potential target audiences which python will parse and return as a list of strings for user to select from and modify as needed
    prompt = f"Given the desired behavior: '{desired_behavior}' which will require intermediate behaviors: '{intermediate_behaviors_list}', but have constraints: {constraints}, and restraints: {restraints}, create a numbered list of recommended groups, demographics, people of specific psychographics, or individuals that can achieve this behavior."
    # store the response from gpt as pta and parse it then prompt the user to select a pta from the list and modify as needed
    pta, chat_history = chat_with_ai(prompt, chat_history)
    pta_list = parse_pta(pta)
    for i in range(len(pta_list)):
        print(f"{i+1}. {pta_list[i]}")
    while True:
        user_input = get_user_input("Select a potential target audience from the list above: ")
        if user_input in range(len(pta_list)):
            break
        else:
            print("Please select a valid number from the list above.")
    return pta

def refine_pta(pta, desired_behavior, intermediate_behaviors, constraints, restraints):
    chat_history = [] # Initialize chat history for the conversation
    # prompt gpt to refine the potential target audience
    # prompt to gpt should return a numbered list of potential target audiences which python will parse and return as a list of strings for user to select from and modify as needed
    prompt = f"Given the potential target audience: '{pta}', desired behavior: '{desired_behavior}', intermediate behaviors: '{intermediate_behaviors_list}', constraints: {constraints}, and restraints: {restraints}, refine the potential target audience to be focused on target audiences with the capability to do the desired behaviors, who live or go near or are in the area where the behaviors must take place, and who have or might feasibly be influenced to have the motivation to want to perform the desired behavior, including the intermediate behaviors, ."
    # store the response from gpt as pta and parse it then prompt the user to select a pta from the list and modify as needed
    pta, chat_history = chat_with_ai(prompt, chat_history)
    pta_list = parse_pta(pta)
    for i in range(len(pta_list)):
        print(f"{i+1}. {pta_list[i]}")
    while True:
        user_input = get_user_input("Select a potential target audience from the list above: ")
        if user_input in range(len(pta_list)):
            # as user if they accept the pta, want to modify it, want to write one in, or want to select a different pta
            user_input = get_user_input("Do you want to modify the selected potential target audience? (yes/no): ")
            if user_input.lower() == 'yes':
                user_input = get_user_input("Do you want to manually write in a potential target audience? (yes/no): ")
                if user_input.lower() == 'yes':
                    pta = get_user_input("Enter the potential target audience: ")
                else:
                    #prompt gpt with user inptu modifications and current pta to create a refined_pta
                    print("The current potential target audience is:" + pta)
                    user_input = get_user_input("How should the potential target audience be refined or modified?: ")
                    prompt = "refine the potential target audience using: {user_input}"
                    pta, chat_history = chat_with_ai(prompt, chat_history)
            else if user_input.lower() == 'no':
                pta = pta
            break
        else:
            print("Please select a valid number from the list above.")
    return pta
    
# Function to assess capability through a chat
def assess_capability(intermediate_behaviors):
    chat_history = [] # Initialize history for the conversation
    prompt = f"We are assessing the capability of the TA to perform the desired behavior and its intermediate behaviors. Intermediate behaviors: {intermediate_behaviors}. What are the physical limitations the TA might have?"
    response, chat_history = chat_with_ai(prompt, chat_history)
    print(response)
    physical_capability = get_user_input("Enter the details of physical limitations: ")
    
    prompt = "What are the psychological, cognitive, or interpersonal limitations the TA might have?"
    response, chat_history = chat_with_ai(prompt, chat_history)
    print(response)
    psychological_capability = get_user_input("Enter the details of psychological, cognitive, or interpersonal limitations: ")
    
    prompt = f"Based on the physical limitations: {physical_capability} and psychological limitations: {psychological_capability}, how can we enable the TA to overcome these limitations?"
    response, chat_history = chat_with_ai(prompt, chat_history)
    print(response)
    
    capability_enablers = get_user_input("Enter the enablers to overcome limitations: ")
    return capability_enablers

# Function to assess opportunity through a chat
def assess_opportunity(intermediate_behaviors):
    chat_history = [] # Initialize history for the conversation
    prompt = f"We are assessing the opportunity for the TA to perform the desired behavior and its intermediate behaviors. Intermediate behaviors: {intermediate_behaviors}. What are the social and physical opportunities and limitations in the environment?"
    response, chat_history = chat_with_ai(prompt, chat_history)
    print(response)
    opportunity_details = get_user_input("Enter the details of social and physical opportunities and limitations: ")
    
    prompt = f"Based on these details: {opportunity_details}, how can we create or enhance opportunities for the TA to perform the action?"
    response, chat_history = chat_with_ai(prompt, chat_history)
    print(response)
    
    opportunity_enablers = get_user_input("Enter the enablers to create or enhance opportunities: ")
    return opportunity_enablers

# Function to assess motivation through a chat
def assess_motivation(intermediate_behaviors):
    chat_history = [] # Initialize history for the conversation
    prompt = f"We are assessing the motivation of the TA to perform the desired behavior and its intermediate behaviors. Intermediate behaviors: {intermediate_behaviors}. What are the automatic (habits, emotions, values) and reflective (identity, beliefs, goals) motivations and limitations?"
    response, chat_history = chat_with_ai(prompt, chat_history)
    print(response)
    motivation_details = get_user_input("Enter the details of automatic and reflective motivations and limitations: ")
    
    prompt = f"Based on these details: {motivation_details}, how can we enhance the motivation of the TA to perform the action?"
    response, chat_history = chat_with_ai(prompt, chat_history)
    print(response)
    
    motivation_enablers = get_user_input("Enter the enablers to enhance motivation: ")
    return motivation_enablers

# Function to determine current HPEM stage through a chat
def determine_hpem_stage():
    chat_history = [] # Initialize history for the conversation
    stages = ["Awareness", "Understanding", "Attitude", "Preference", "Intention", "Behavior"]
    current_stage = stages[0]
    
    for stage in stages:
        prompt = f"Is the TA at the '{stage}' stage? What indicators or behaviors should we look for?"
        response, chat_history = chat_with_ai(prompt, chat_history)
        print(response)
        user_input = get_user_input(f"Is the TA at the '{stage}' stage? (yes/no): ")
        if user_input.lower() == 'yes':
            current_stage = stage
            break
    return current_stage

# Main function to guide the user through the process
def main():
    print("Welcome to the Target Audience Refinement Tool using COM-B and HPEM Models.")
    api_key = get_user_input("Please enter your OpenAI API key: ")
    initialize_openai(api_key)
    # Step 0 : Define the Area Mission and Objectives
    define_mission()
    create_spo(area_of_focus, operational_objective, psychological_objective, constraints, restraints)
                          
    # Step 1: Define and refine the desired behavior
    while initial_behavior == "":
        initial_behavior = get_user_input("Enter the initial desired behavior: ")
        if initial_behavior == "":
            print("Desired behavior cannot be empty.")
    refined_behavior = refine_desired_behavior(initial_behavior)
    print(f"Refined desired behavior: {refined_behavior}")

    # Step 2: Break down the desired behavior into intermediate behaviors
    intermediate_behaviors = break_down_behavior(refined_behavior)
    print(f"Intermediate behaviors: {intermediate_behaviors}")

    # Step 3: Describe the Potential Target Audience (PTA)
    pta_description = get_user_input("Describe the Potential Target Audience (PTA): ")
    
    # Step 4: Assess Capability
    capability_enablers = assess_capability(intermediate_behaviors)
    print(f"Capability enablers: {capability_enablers}")
    
    # Step 5: Assess Opportunity
    opportunity_enablers = assess_opportunity(intermediate_behaviors)
    print(f"Opportunity enablers: {opportunity_enablers}")
    
    # Step 6: Assess Motivation
    motivation_enablers = assess_motivation(intermediate_behaviors)
    print(f"Motivation enablers: {motivation_enablers}")
    
    # Step 7: Determine HPEM Stage
    hpem_stage = determine_hpem_stage()
    print(f"The current HPEM stage of the TA is: {hpem_stage}")
    
    # Step 8: Get AI suggestions for intermediate objectives and strategies
    intermediate_objectives_prompt = f"Given the TA is at the {hpem_stage} stage, what are the intermediate objectives and strategies to move them to the next stage?"
    intermediate_objectives = get_ai_suggestions(intermediate_objectives_prompt)
    print("Intermediate Objectives and Strategies:")
    print(intermediate_objectives)

if __name__ == "__main__":
    main()
