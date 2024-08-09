from openai_utils import chat_with_ai
from utils import get_user_input

def select_potential_target_audience(refined_behavior, intermediate_behaviors, constraints, restraints, operational_context):
    chat_history = []
    prompt = (
        f"Given the desired behavior: '{refined_behavior}' which will require intermediate behaviors: '{intermediate_behaviors}', "
        f"but have constraints: {constraints}, and restraints: {restraints}, and our {operational_context} create a list of recommended target audiences (TA): groups, demographics, "
        f"people of specific psychographics, or individuals that can achieve this behavior. Each TA must be a single line and not numbered. Don't use markdown, without any commentary."
    )
    pta, chat_history = chat_with_ai(prompt, chat_history)
    pta_list = parse_pta(pta)
    
    for idx, item in enumerate(pta_list, start=1):
        print(f"{idx}. {item}")
    
    while True:
        user_input = get_user_input("Select a potential target audience from the list above: ")
        if user_input.strip().isdigit():
            selected_pta_index = int(user_input) - 1
            if 0 <= selected_pta_index < len(pta_list):
                selected_pta = pta_list[selected_pta_index]
                break
            else:
                print("Invalid selection. Please enter a valid index.")
        else:
            print("Invalid input. Please enter a number.")
    return selected_pta

def assess_capability(intermediate_behaviors, refined_behavior, pta, area_of_focus, constraints, restraints, operational_context):
    chat_history = []

    psychological_prompt = (
        f"We are refining the current Target Audience by the capability to perform {refined_behavior} which consists of {intermediate_behaviors}. "
        f"The current Target Audience is {pta}. Based on the psychological (psychological, cognitive and interpersonal) capabilities required, "
        f"refine the current target audience to the broadest group of the current target audience who has the capability to do this behavior."
        f"consider {operational_context}."
    )
    physical_prompt = (
        f"We are refining the current Target Audience by the capability to perform {refined_behavior} which consists of {intermediate_behaviors}. "
        f"The current Target Audience is {pta}. Based on the physical capabilities required, refine the current target audience to the broadest group "
        f"of the current target audience who has the capability to do this behavior."
    )

    psychological_capable_pta, chat_history = chat_with_ai(psychological_prompt, chat_history)
    physical_capable_pta, chat_history = chat_with_ai(physical_prompt, chat_history)
    
    capable_pta, chat_history = chat_with_ai(
        "Merge the psychological capable PTA and physical capable PTA to find the intersection of the two potential target audiences. "
        "Attributes must be distinct enough that they can be measured or searched against when searching for this target audience.", 
        chat_history
    )

    while True:
        user_input = get_user_input("Is this current target audience acceptable? (yes/no): ")
        if user_input.lower() == 'yes':
            break
        else:
            user_input = get_user_input("How should the current target audience be refined or broadened?: ")
            prompt = f"Refine the current target audience using: {user_input}"
            capable_pta, chat_history = chat_with_ai(prompt, chat_history)

    return capable_pta

def assess_opportunity(intermediate_behaviors, capable_pta, area_of_focus, constraints, restraints, operational_context):
    chat_history = []

    social_prompt = (
        f"We are assessing the environmental opportunity in or around {area_of_focus} of the TA to perform the desired behavior and its intermediate behaviors. "
        f"Intermediate behaviors: {intermediate_behaviors}. What are the opportunities and limitations in the environment - social context?"
    )
    physical_prompt = (
        f"We are assessing the environmental opportunity in or around {area_of_focus} of the TA to perform the desired behavior and its intermediate behaviors. "
        f"Intermediate behaviors: {intermediate_behaviors}. What are the opportunities and limitations in the environment - physical context?"
    )
    social_opportune_pta, chat_history = chat_with_ai(social_prompt, chat_history)
    physical_opportune_pta, chat_history = chat_with_ai(physical_prompt, chat_history)
    
    capable_opportune_pta, chat_history = chat_with_ai(
        "Merge the social opportune PTA and physical opportune PTA to find the intersection of the two potential target audiences. "
        "Attributes must be distinct enough that they can be measured or searched against when searching for this target audience.", 
        chat_history
    )

    return capable_opportune_pta

def assess_motivation(intermediate_behaviors, capable_opportune_pta, area_of_focus, constraints, restraints, operational_context):
    chat_history = []

    automatic_prompt = (
        f"We are assessing the motivation of the TA to perform the desired behavior and its intermediate behaviors. "
        f"Intermediate behaviors: {intermediate_behaviors}. What are the automatic motivations and habits that can help the TA to perform the behavior?"
    )
    reflective_prompt = (
        f"We are assessing the motivation of the TA to perform the desired behavior and its intermediate behaviors. "
        f"Intermediate behaviors: {intermediate_behaviors}. What are the reflective motivations and beliefs that can help the TA to perform the behavior?"
    )
    automatic_motivated_pta, chat_history = chat_with_ai(automatic_prompt, chat_history)
    reflective_motivated_pta, chat_history = chat_with_ai(reflective_prompt, chat_history)
    
    motivated_pta, chat_history = chat_with_ai(
        "Merge the automatic motivated PTA and reflective motivated PTA to find the intersection of the two potential target audiences. "
        "Attributes must be distinct enough that they can be measured or searched against when searching for this target audience.", 
        chat_history
    )

    return motivated_pta

def determine_hpem_stage(refined_target_audience, refined_behavior, area_of_focus, constraints, restraints):
    chat_history = []
    stages = ["Awareness", "Understanding", "Attitude", "Preference", "Intention", "Behavior"]
    current_stage = stages[0]

    for stage in stages:
        prompt = f"Is {refined_target_audience} in {area_of_focus} likely at the '{stage}' stage to perform {refined_behavior}? What indicators or behaviors should we look for?"
        response, chat_history = chat_with_ai(prompt, chat_history)
        print(response)
        user_input = get_user_input(f"Is the TA at the '{stage}' stage? (yes/no): ")
        if user_input.lower() == 'yes':
            current_stage = stage
            break
    return current_stage
