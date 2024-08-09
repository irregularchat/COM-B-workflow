from openai_utils import initialize_openai, get_ai_suggestions, chat_with_ai
from mission_utils import define_mission, influence_mission, create_initial_behavior, refine_desired_behavior, break_down_behavior
from target_audience_utils import select_potential_target_audience, assess_capability, assess_opportunity, assess_motivation, determine_hpem_stage
from mission_utils import define_mission, influence_mission, create_initial_behavior, refine_desired_behavior, break_down_behavior
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()  # Ensure this is called early in your script

# Load the variables needed for the script
area_of_focus = os.getenv("AREA_OF_FOCUS", "")
operational_objective = os.getenv("OPERATIONAL_OBJECTIVE", "")
constraints = os.getenv("CONSTRAINTS", "None")
restraints = os.getenv("RESTRAINTS", "None")
psychological_objective = os.getenv("PSYCHOLOGICAL_OBJECTIVE", "")
spo = os.getenv("SPO", "")

def main():
    print("Welcome to the Target Audience Refinement Tool using COM-B and HPEM Models.")
    initialize_openai()

    # Step 0: Define the Area Mission and Objectives
    area_of_focus, operational_objective, psychological_objective, constraints, restraints, operational_context = define_mission()

    # Step 1: Define and refine the desired behavior
    psychological_objective, spo = influence_mission(
        area_of_focus,
        operational_objective,
        psychological_objective,
        constraints,
        restraints
    )
    
    initial_behavior = create_initial_behavior(spo, area_of_focus, operational_objective, psychological_objective, constraints, restraints)
    refined_behavior = refine_desired_behavior(initial_behavior)
    print(f"Refined desired behavior: {refined_behavior}")

    # Step 2: Break down the desired behavior into intermediate behaviors
    intermediate_behaviors = break_down_behavior(refined_behavior, area_of_focus)
    print("\n####################\n")
    # Fixing the formatting
    formatted_intermediate_behaviors = "\n".join([f"{idx+1}. {behavior.strip()}" for idx, behavior in enumerate(intermediate_behaviors) if behavior.strip()])
    print("####################")
    print("Intermediate behaviors:\n" + formatted_intermediate_behaviors)
    print("\n####################\n")
    # Step 3: Describe the Potential Target Audience (PTA)
    pta_description = select_potential_target_audience(refined_behavior, intermediate_behaviors, constraints, restraints, operational_context)
    print(f"Potential Target Audience (PTA): {pta_description}")
    print("\n####################\n")

    # Step 4: Assess Capability
    capable_pta = assess_capability(intermediate_behaviors, refined_behavior, pta_description, area_of_focus, constraints, restraints, operational_context)
    print("\n####################\n")

    # Step 5: Assess Opportunity
    capable_opportune_pta = assess_opportunity(intermediate_behaviors, capable_pta, area_of_focus, constraints, restraints, operational_context)
    print("\n####################\n")

    # Step 6: Assess Motivation
    refined_target_audience = assess_motivation(intermediate_behaviors, capable_opportune_pta, area_of_focus, constraints, restraints, operational_context)
    print("\n####################\n")

    # Step 7: Determine HPEM Stage
    hpem_stage = determine_hpem_stage(refined_target_audience, refined_behavior, area_of_focus, constraints, restraints)
    print(f"The current HPEM stage of the TA is: {hpem_stage}")
    print("\n####################\n")

    # Step 8: Get AI suggestions for intermediate objectives and strategies
    intermediate_objectives_prompt = f"Given the TA is at the {hpem_stage} stage, what are the intermediate objectives and strategies to move them to the next stage?"
    intermediate_objectives = get_ai_suggestions(intermediate_objectives_prompt)  # Ensure model is correctly used inside this function

    print("Intermediate Objectives and Strategies:")
    print(intermediate_objectives)
    print("\n####################\n")


if __name__ == "__main__":
    main()
