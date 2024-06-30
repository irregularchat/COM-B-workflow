from openai import OpenAI
import os
import argparse
from dotenv import load_dotenv

# Import the OpenAI API key from a separate .env file
load_dotenv()
area_of_focus = os.getenv("AREA_OF_FOCUS", "")
operational_objective = os.getenv("OPERATIONAL_OBJECTIVE", "")
constraints = os.getenv("CONSTRAINTS", "None")
restraints = os.getenv("RESTRAINTS", "None")
psychological_objective = os.getenv("PSYCHOLOGICAL_OBJECTIVE", "")
spo = os.getenv("SPO", "")

def initialize_openai():
    global client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if client.api_key is None:
        raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Function to get AI suggestions
def get_ai_suggestions(prompt):
    try:
        response = client.completions.create(engine="gpt-3.5-turbo",
                                             prompt=prompt,
                                             max_tokens=300)
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
    psychological_objective = ""
    while area_of_focus == "":
        area_of_focus = get_user_input("Enter the area of focus: ")
        if area_of_focus == "":
            print("Area of focus cannot be empty.")

    while operational_objective == "":
        operational_objective = get_user_input("Enter the operational objective: ")
        if operational_objective == "":
            print("Operational objective cannot be empty.")
    constraints = get_user_input("Enter the constraints (optional) (e.g., time, resources, etc.): ")
    if constraints == "":
        constraints = "None"

    restraints = get_user_input("Enter the restraints (optional) (e.g., rules, regulations, etc.): ")
    if restraints == "":
        restraints = "None"

    print(f"Area of focus: {area_of_focus}")
    print(f"Operational objective: {operational_objective}")
    print("Limitations:")
    print(f"Constraints: {constraints}")
    print(f"Restraints: {restraints}")
    return area_of_focus, operational_objective, psychological_objective, constraints, restraints

def influence_mission():
    global psychological_objective, spo
    while psychological_objective == "":
        psychological_objective = get_user_input("Enter the psychological objective: ")
        if psychological_objective == "":
            print("Psychological objective cannot be empty.")
    while spo == "":
        spo = create_spo(area_of_focus, operational_objective, psychological_objective, constraints, restraints)
        if spo == "":
            print("SPO cannot be empty.")
    print(f"Psychological objective: {psychological_objective}")
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
    chat_history = []  # Initialize chat history for the conversation
    prompt = (f"You are a Military PSYOP Planner. The Supporting Psychological Objective (SPO) for each series is the culmination point of achieved intermediate objectives. "
              f"The plan of execution becomes linear with intermediate objectives preceding SPO accomplishment, and SPOs preceding the achievement of the PO, ultimately supporting the commander's objectives. "
              f"Given the area of focus: '{area_of_focus}', operational objective: '{operational_objective}', and psychological objective: '{psychological_objective}', "
              f"create a list without numbers of specific, measurable, and observable supporting psychological objectives (SPOs) that can be achieved. "
              f"Consider the constraints: {constraints} and restraints: {restraints}. Each SPO should be one sentence per line, starting with TA and an appropriate action verb. No markdown. No commentary. "
              f"Use the following categories of verbs to guide your objectives:\n\n"
              f"#### Action Verbs\n"
              f"Increases/Decreases, Votes, Participates (in something specific), Surrenders, Turns in, Organizes/Holds, Attends, Registers, Surrenders.\n\n"
              f"#### Communication Verbs\n"
              f"Reports, Publicly condemns/states, Purchases, Donates, Signs, Joins, Refers, Comments, Reviews, Rates.\n\n"
              f"#### Support Verbs\n"
              f"Volunteers, Completes.\n\n"
              f"#### Miscellaneous Verbs\n"
              f"Renews, Subscribes.\n\n"
              f"Ensure that the SPOs are specific, measurable, and observable, avoiding weaker verbs such as believes, feels, hopes, thinks, understands, realizes, considers, appreciates, recognizes, assumes, dreams, wishes, imagines, envisions, refrains, stops, halts, ceases, restrains, maintains, continues, notes, observes, views, opposes, includes, questions, favors.")
    spo, chat_history = chat_with_ai(prompt, chat_history)
    parsed_spo = parse_spo(spo)
    
    # Display the SPOs to the user
    print("\nSupporting Psychological Objectives (SPOs):")
    for idx, spo in enumerate(parsed_spo, start=1):
        print(f"{idx}. {spo}")

    # User input for selecting one SPO
    while True:
        user_input = get_user_input("\nSelect 1 SPO that is the best: ")
        if user_input.strip().isdigit():
            selected_spo_index = int(user_input) - 1
            if 0 <= selected_spo_index < len(parsed_spo):
                selected_spo = parsed_spo[selected_spo_index]
                break
            else:
                print("Invalid selection. Please enter a valid index.")
        else:
            print("Invalid input. Please enter a number.")

    print(f"\nSelected SPO:\n1. {selected_spo}")

    # Option to modify the selected SPO
    while True:
        user_input = get_user_input("\nWould you like to modify the selected SPO? (yes/no): ")
        if user_input.lower() == 'yes':
            modification_prompt = get_user_input("Enter your modifications for the selected SPO: ")
            prompt = f"Modify the selected SPO: {modification_prompt}"
            spo, chat_history = chat_with_ai(prompt, chat_history)
            parsed_spo = parse_spo(spo)
            print("\nModified Supporting Psychological Objectives (SPOs):")
            for idx, spo in enumerate(parsed_spo, start=1):
                print(f"{idx}. {spo}")

            while True:
                user_input = get_user_input("\nSelect 1 SPO that is the best: ")
                if user_input.strip().isdigit():
                    selected_spo_index = int(user_input) - 1
                    if 0 <= selected_spo_index < len(parsed_spo):
                        selected_spo = parsed_spo[selected_spo_index]
                        break
                    else:
                        print("Invalid selection. Please enter a valid index.")
                else:
                    print("Invalid input. Please enter a number.")
            break
        elif user_input.lower() == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    if not selected_spo:
        print("SPO cannot be empty.")
        return ""
    spo = selected_spo
    return spo

def parse_initial_behavior(initial_behavior):
    try:
        initial_behavior_list = initial_behavior.split('\n')
        return [b.strip() for b in initial_behavior_list if b.strip()]
    except Exception as e:
        print(f"Error parsing initial behavior: {e}")
        return []

def create_initial_behavior(spo, area_of_focus, operational_objective, psychological_objective, constraints, restraints):
    chat_history = []  # Initialize chat history for the conversation
    prompt = (f"What behavior in {area_of_focus} can help achieve {spo} and get closer to '{operational_objective}' "
              f"by '{psychological_objective}' considering constraints: {constraints}, and restraints: {restraints}? "
              f"Create a list of 5 different behaviors that could be measured in some way. Do not number. Only return a sentence of the behavior.")
    initial_behavior, chat_history = chat_with_ai(prompt, chat_history)

    # User input to select the initial behavior
    initial_behavior_list = parse_initial_behavior(initial_behavior)
    # Add printed space and section divider
    print(" ")
    print("####################")
    for i, item in enumerate(initial_behavior_list):
        print(f"{i + 1}. {item}")
    while True:
        try:
            user_input = int(get_user_input("Select an initial behavior from the list above: "))
            if 0 < user_input <= len(initial_behavior_list):
                initial_behavior_selected = initial_behavior_list[user_input - 1]
                break
            else:
                print("Please select a valid number from the list above.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return initial_behavior_selected

def parse_refined_behavior(refined_behavior):
    try:
        refined_behavior_list = refined_behavior.split('\n')
        return [b.strip() for b in refined_behavior_list if b.strip()]
    except Exception as e:
        print(f"Error parsing refined behavior: {e}")
        return []

def refine_desired_behavior(initial_behavior):
    chat_history = []  # Initialize chat history for the conversation
    prompt = (f"The initial desired behavior is: '{initial_behavior}'. Create a list, not numbered, of potential refined behaviors. "
              f"Unknown who the target audience (TA) would be yet but phrase the desired behavior as 'TA verb_here xxx', but don't use markdown. "
              f"This must be behaviors that are measurable and that would have an impact towards the objective.")
    refined_behavior, chat_history = chat_with_ai(prompt, chat_history)
    refined_behavior_list = parse_refined_behavior(refined_behavior)
    # Add printed space and section divider
    print(" ")
    print("####################")
    for i, item in enumerate(refined_behavior_list):
        print(f"{i + 1}. {item}")
    while True:
        try:
            user_input = int(get_user_input("Select a refined behavior from the list above: "))
            if 0 < user_input <= len(refined_behavior_list):
                refined_behavior_selected = refined_behavior_list[user_input - 1]
                break
            else:
                print("Please select a valid number from the list above.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    return refined_behavior_selected

def parse_intermediate_behaviors(intermediate_behaviors):
    try:
        intermediate_behaviors_list = intermediate_behaviors.split('\n')
        return [b.strip() for b in intermediate_behaviors_list if b.strip()]
    except Exception as e:
        print(f"Error parsing intermediate behaviors: {e}")
        return []

def break_down_behavior(refined_behavior):
    chat_history = []  # Initialize history for the conversation
    prompt = (f"The desired behavior is: '{refined_behavior}' in '{area_of_focus}'. Consider in backwards order starting from the desired behavior "
              f"and backwards from each previous required behavior but then list it in sequential order ending with the desired behavior. "
              f"Create a list of intermediate behaviors that lead to achieving this behavior. Each behavior must be a sentence and not numbered. Don't use markdown, and only return sentences of the behavior without any commentary. "
              f"Mark when an intermediate behavior is REQUIRED and mark when it has MULTIPLE OPTIONS to complete such as can be done online or automatically. If multiple options, provide the multiple options as in the steps Option A or Option B, etc.")
    intermediate_behaviors, chat_history = chat_with_ai(prompt, chat_history)
    intermediate_behaviors_list = parse_intermediate_behaviors(intermediate_behaviors)
    # Add printed space and section divider
    print(" ")
    print("####################")

    for i, item in enumerate(intermediate_behaviors_list):
        print(f"{i + 1}. {item}")
    # Ask GPT to modify the intermediate behaviors with the user input or continue
    while True:
        user_input = get_user_input("Would you like to modify the intermediate behaviors? (yes/no): ")
        if user_input.lower() == 'yes':
            modification_prompt = get_user_input("Enter your modifications for the intermediate behaviors: ")
            prompt = f"Modify the intermediate behaviors: {modification_prompt}"
            intermediate_behaviors, chat_history = chat_with_ai(prompt, chat_history)
            intermediate_behaviors_list = parse_intermediate_behaviors(intermediate_behaviors)
            for i, item in enumerate(intermediate_behaviors_list):
                print(f"{i + 1}. {item}")
        elif user_input.lower() == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    return intermediate_behaviors_list

def parse_pta(pta):
    try:
        pta_list = pta.split('\n')
        return [p.strip() for p in pta_list if p.strip()]
    except Exception as e:
        print(f"Error parsing potential target audience: {e}")
        return []

def select_potential_target_audience(desired_behavior, intermediate_behaviors, constraints, restraints):
    chat_history = []  # Initialize chat history for the conversation
    prompt = (f"Given the desired behavior: '{desired_behavior}' which will require intermediate behaviors: '{intermediate_behaviors}', "
              f"but have constraints: {constraints}, and restraints: {restraints}, create a list of recommended target audiences (TA): groups, demographics, "
              f"people of specific psychographics, or individuals that can achieve this behavior. Each TA must be a single line and not numbered. Don't use markdown, without any commentary.")
    pta, chat_history = chat_with_ai(prompt, chat_history)
    # Add printed space and section divider
    print(" ")
    print("####################")
    pta_list = parse_pta(pta)
    for i, item in enumerate(pta_list):
        print(f"{i + 1}. {item}")
    while True:
        try:
            user_input = int(get_user_input("Select a potential target audience from the list above: "))
            if 0 < user_input <= len(pta_list):
                pta_selected = pta_list[user_input - 1]
                break
            else:
                print("Please select a valid number from the list above.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    return pta_selected

def refine_pta(pta, desired_behavior, intermediate_behaviors, constraints, restraints):
    chat_history = []  # Initialize chat history for the conversation
    prompt = (f"Given the potential target audience: '{pta}', desired behavior: '{desired_behavior}', intermediate behaviors: '{intermediate_behaviors}', "
              f"constraints: {constraints}, and restraints: {restraints}, refine the potential target audience to be focused on those with the capability to perform "
              f"the desired behaviors, who are in the area where the behaviors must take place, and who might be influenced to perform the desired behavior. Each refined TA must be a single line and not numbered. Don't use markdown, without any commentary.")
    refined_pta, chat_history = chat_with_ai(prompt, chat_history)
    pta_list = parse_pta(refined_pta)
    for i, item in enumerate(pta_list):
        print(f"{i + 1}. {item}")
    while True:
        try:
            user_input = int(get_user_input("Select a refined potential target audience from the list above: "))
            if 0 < user_input <= len(pta_list):
                refined_pta_selected = pta_list[user_input - 1]
                break
            else:
                print("Please select a valid number from the list above.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    return refined_pta_selected

def assess_capability(intermediate_behaviors, desired_behavior, pta, area_of_focus, constraints, restraints):
    chat_history = []  # Initialize history for the conversation
    psychological_prompt = (f"We are refining the current Target Audience by the capability to perform {desired_behavior} which consists of {intermediate_behaviors}. "
                            f"The current Target Audience is {pta}. Based on the psychological (psychological, cognitive and interpersonal) capabilities required, "
                            f"refine the current target audience to the broadest group of the current target audience who has the capability to do this behavior.")
    physical_prompt = (f"We are refining the current Target Audience by the capability to perform {desired_behavior} which consists of {intermediate_behaviors}. "
                       f"The current Target Audience is {pta}. Based on the physical capabilities required, refine the current target audience to the broadest group "
                       f"of the current target audience who has the capability to do this behavior.")

    psychological_capable_pta, chat_history = chat_with_ai(psychological_prompt, chat_history)
    physical_capable_pta, chat_history = chat_with_ai(physical_prompt, chat_history)
    print(f"Psychological Capable PTA: {psychological_capable_pta}")
    print(f"Physical Capable PTA: {physical_capable_pta}")

    capable_pta, chat_history = chat_with_ai("Merge the psychological capable PTA and physical capable PTA to find the intersection of the two potential target audiences. Attributes must be distinct enough that they can be measured or searched against when searching for this target audience.", chat_history)

    while True:
        print("The current target audience capable of performing the desired behavior is: " + capable_pta)
        user_input = get_user_input("Is this current target audience acceptable? (yes/no): ")
        if user_input.lower() == 'yes':
            break
        else:
            user_input = get_user_input("How should the current target audience be refined or broadened?: ")
            prompt = f"Refine the current target audience using: {user_input}"
            capable_pta, chat_history = chat_with_ai(prompt, chat_history)

    while True:
        print("The original potential target audience was: " + pta)
        print("The refined potential target audience based on capability is: " + capable_pta)
        user_input = get_user_input("Do you accept the refined potential target audience? (yes/no): ")
        if user_input.lower() == 'yes':
            break
        else:
            capable_pta = pta
            psychological_help_prompt = (f"We are refining the current Target Audience by the capability to perform {desired_behavior} which consists of {intermediate_behaviors}. "
                                         f"The current Target Audience is {pta}. Based on the psychological (psychological, cognitive and interpersonal) capabilities required, "
                                         f"refine the current target audience to the current target audience who does not have the capability to do this behavior.")
            physical_help_prompt = (f"We are refining the current Target Audience by the capability to perform {desired_behavior} which consists of {intermediate_behaviors}. "
                                    f"The current Target Audience is {pta}. Based on the physical capabilities required, refine the current target audience to the current target audience "
                                    f"who does not have the capability to do this behavior.")
            psychological_help_pta, chat_history = chat_with_ai(psychological_help_prompt, chat_history)
            physical_help_pta, chat_history = chat_with_ai(physical_help_prompt, chat_history)
            psychological_interventions_prompt = f"Given {psychological_help_pta} does not have full capability to perform the desired behavior, what interventions from the Behavior Change Wheel can help them to be able to perform the behavior?"
            physical_interventions_prompt = f"Given {physical_help_pta} does not have full capability to perform the desired behavior, what interventions from the Behavior Change Wheel can help them to be able to perform the behavior?"
            psychological_interventions, chat_history = chat_with_ai(psychological_interventions_prompt, chat_history)
            physical_interventions, chat_history = chat_with_ai(physical_interventions_prompt, chat_history)
            print("Interventions to help the target audience to be able to perform the desired behavior:")
            print("Psychological interventions: " + psychological_interventions)
            print("Physical interventions: " + physical_interventions)
    return capable_pta

def assess_opportunity(intermediate_behaviors, capable_pta, area_of_focus, constraints, restraints):
    chat_history = []  # Initialize history for the conversation
    social_prompt = (f"We are assessing the environmental opportunity in or around {area_of_focus} of the TA to perform the desired behavior and its intermediate behaviors. "
                     f"Intermediate behaviors: {intermediate_behaviors}. What are the opportunities and limitations in the environment - social context?")
    physical_prompt = (f"We are assessing the environmental opportunity in or around {area_of_focus} of the TA to perform the desired behavior and its intermediate behaviors. "
                       f"Intermediate behaviors: {intermediate_behaviors}. What are the opportunities and limitations in the environment - physical context?")
    social_opportune_pta, chat_history = chat_with_ai(social_prompt, chat_history)
    physical_opportune_pta, chat_history = chat_with_ai(physical_prompt, chat_history)
    print(f"Social Opportune PTA: {social_opportune_pta}")
    print(f"Physical Opportune PTA: {physical_opportune_pta}")

    capable_opportune_pta, chat_history = chat_with_ai("Merge the social opportune PTA and physical opportune PTA to find the intersection of the two potential target audiences. Attributes must be distinct enough that they can be measured or searched against when searching for this target audience.", chat_history)
    while True:
        print("The current target audience capable of performing the desired behavior is: " + capable_opportune_pta)
        user_input = get_user_input("Is this current target audience acceptable? (yes/no): ")
        if user_input.lower() == 'yes':
            break
        else:
            user_input = get_user_input("How should the current target audience be refined or broadened?: ")
            prompt = f"Modify the current target audience: {user_input}"
            capable_opportune_pta, chat_history = chat_with_ai(prompt, chat_history)

    while True:
        print("The original potential target audience was: " + capable_pta)
        print("The refined potential target audience based on opportunity is: " + capable_opportune_pta)
        user_input = get_user_input("Do you accept the refined potential target audience? (yes/no): ")
        if user_input.lower() == 'yes':
            break
        else:
            capable_opportune_pta = capable_pta
            social_interventions_prompt = f"Given {social_opportune_pta} does not have full opportunity to perform the desired behavior, what interventions from the Behavior Change Wheel can help them to be able to perform the behavior?"
            physical_interventions_prompt = f"Given {physical_opportune_pta} does not have full opportunity to perform the desired behavior, what interventions from the Behavior Change Wheel can help them to be able to perform the behavior?"
            social_interventions, chat_history = chat_with_ai(social_interventions_prompt, chat_history)
            physical_interventions, chat_history = chat_with_ai(physical_interventions_prompt, chat_history)
            print("Interventions to help the target audience to be able to perform the desired behavior:")
            print("Social interventions: " + social_interventions)
            print("Physical interventions: " + physical_interventions)
    return capable_opportune_pta

def assess_motivation(intermediate_behaviors, capable_opportune_pta, area_of_focus, constraints, restraints):
    chat_history = []  # Initialize history for the conversation
    automatic_prompt = (f"We are assessing the motivation of the TA to perform the desired behavior and its intermediate behaviors. "
                        f"Intermediate behaviors: {intermediate_behaviors}. What are the automatic motivations and habits that can help the TA to perform the behavior?")
    reflective_prompt = (f"We are assessing the motivation of the TA to perform the desired behavior and its intermediate behaviors. "
                         f"Intermediate behaviors: {intermediate_behaviors}. What are the reflective motivations and beliefs that can help the TA to perform the behavior?")
    automatic_motivated_pta, chat_history = chat_with_ai(automatic_prompt, chat_history)
    reflective_motivated_pta, chat_history = chat_with_ai(reflective_prompt, chat_history)
    print(f"Automatic Motivated PTA: {automatic_motivated_pta}")
    print(f"Reflective Motivated PTA: {reflective_motivated_pta}")

    motivated_pta, chat_history = chat_with_ai("Merge the automatic motivated PTA and reflective motivated PTA to find the intersection of the two potential target audiences. Attributes must be distinct enough that they can be measured or searched against when searching for this target audience.", chat_history)
    print("Intermediate behaviors: " + intermediate_behaviors)
    print("In the area of focus: " + area_of_focus)
    print("With constraints: " + constraints)
    print("With restraints: " + restraints)

    while True:
        print("The current target audience capable of performing the desired behavior is: " + motivated_pta)
        user_input = get_user_input("Is this current target audience acceptable? (yes/no): ")
        if user_input.lower() == 'yes':
            break
        else:
            user_input = get_user_input("How should the current target audience be refined or broadened?: ")
            prompt = f"Modify the current target audience: {user_input}"
            motivated_pta, chat_history = chat_with_ai(prompt, chat_history)

    while True:
        print("The original potential target audience was: " + capable_opportune_pta)
        print("The refined potential target audience based on motivation is: " + motivated_pta)
        user_input = get_user_input("Do you accept the refined potential target audience? (yes/no): ")
        if user_input.lower() == 'yes':
            break
        else:
            motivated_pta = capable_opportune_pta
            automatic_interventions_prompt = f"Given {automatic_motivated_pta} does not have full motivation to perform the desired behavior, what interventions from the Behavior Change Wheel can help them to be able to perform the behavior?"
            reflective_interventions_prompt = f"Given {reflective_motivated_pta} does not have full motivation to perform the desired behavior, what interventions from the Behavior Change Wheel can help them to be able to perform the behavior?"
            automatic_interventions, chat_history = chat_with_ai(automatic_interventions_prompt, chat_history)
            reflective_interventions, chat_history = chat_with_ai(reflective_interventions_prompt, chat_history)
            print("Interventions to help the target audience to be able to perform the desired behavior:")
            print("Automatic interventions: " + automatic_interventions)
            print("Reflective interventions: " + reflective_interventions)
    return motivated_pta

def determine_hpem_stage(refined_target_audience, desired_behavior, area_of_focus, constraints, restraints):
    chat_history = []  # Initialize history for the conversation
    stages = ["Awareness", "Understanding", "Attitude", "Preference", "Intention", "Behavior"]
    current_stage = stages[0]

    for stage in stages:
        prompt = f"Is {refined_target_audience} in {area_of_focus} likely at the '{stage}' stage to perform {desired_behavior}? What indicators or behaviors should we look for?"
        response, chat_history = chat_with_ai(prompt, chat_history)
        print(response)
        user_input = get_user_input(f"Is the TA at the '{stage}' stage? (yes/no): ")
        if user_input.lower() == 'yes':
            current_stage = stage
            break
    return current_stage

def main():
    print("Welcome to the Target Audience Refinement Tool using COM-B and HPEM Models.")
    initialize_openai()

    # Step 0: Define the Area Mission and Objectives
    area_of_focus, operational_objective, psychological_objective, constraints, restraints = define_mission()

    # Step 1: Define and refine the desired behavior
    psychological_objective, spo = influence_mission()
    
    initial_behavior = create_initial_behavior(spo, area_of_focus, operational_objective, psychological_objective, constraints, restraints)
    refined_behavior = refine_desired_behavior(initial_behavior)
    print(f"Refined desired behavior: {refined_behavior}")

    # Step 2: Break down the desired behavior into intermediate behaviors
    intermediate_behaviors = break_down_behavior(refined_behavior)
    print(f"Intermediate behaviors: {intermediate_behaviors}")

    # Step 3: Describe the Potential Target Audience (PTA)
    pta_description = select_potential_target_audience(refined_behavior, intermediate_behaviors, constraints, restraints)
    print(f"Potential Target Audience (PTA): {pta_description}")

    # Step 4: Assess Capability
    capable_pta = assess_capability(intermediate_behaviors, refined_behavior, pta_description, area_of_focus, constraints, restraints)

    # Step 5: Assess Opportunity
    capable_opportune_pta = assess_opportunity(intermediate_behaviors, capable_pta, area_of_focus, constraints, restraints)

    # Step 6: Assess Motivation
    refined_target_audience = assess_motivation(intermediate_behaviors, capable_opportune_pta, area_of_focus, constraints, restraints)

    # Step 7: Determine HPEM Stage
    hpem_stage = determine_hpem_stage(refined_target_audience, refined_behavior, area_of_focus, constraints, restraints)
    print(f"The current HPEM stage of the TA is: {hpem_stage}")

    # Step 8: Get AI suggestions for intermediate objectives and strategies
    intermediate_objectives_prompt = f"Given the TA is at the {hpem_stage} stage, what are the intermediate objectives and strategies to move them to the next stage?"
    intermediate_objectives = get_ai_suggestions(intermediate_objectives_prompt)
    print("Intermediate Objectives and Strategies:")
    print(intermediate_objectives)

if __name__ == "__main__":
    main()
