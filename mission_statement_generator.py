import os
from mission_utils import generate_mission_statement  # Assuming this utility exists
from openai_utils import chat_with_ai  # Assuming OpenAI API is used for generation
from utils import get_user_input  # General utility functions
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def main():
    # Load variables from .env and prompt the user for any missing information
    area_of_focus = os.getenv("AREA_OF_FOCUS", "") or get_user_input("Enter the area of focus: ")
    operational_objective = os.getenv("OPERATIONAL_OBJECTIVE", "") or get_user_input("Enter the operational objective: ")
    constraints = os.getenv("CONSTRAINTS", "None") or get_user_input("Enter the constraints [Specific restrictions limiting military commanders' actions](if any): ")
    restraints = os.getenv("RESTRAINTS", "None") or get_user_input("Enter the restraints [Imposed Limitations on the use of force in operations](if any): ")
    psychological_objective = os.getenv("PSYCHOLOGICAL_OBJECTIVE", "") or get_user_input("Enter the psychological objective: ")
    spo = os.getenv("SPO", "") or get_user_input("Enter the supporting psychological objective (SPO): ")

    # Store the data in a dictionary
    data = {
        "area_of_focus": area_of_focus,
        "operational_objective": operational_objective,
        "constraints": constraints,
        "restraints": restraints,
        "psychological_objective": psychological_objective,
        "spo": spo
    }

    # Generate the mission statement
    mission_statement = generate_mission_statement(data)
    
    # Optionally, use OpenAI to refine or generate the statement
    refined_statement = chat_with_ai(mission_statement)[0]
    
    # Output the result
    print("\nGenerated Mission Statement:")
    print(refined_statement)

if __name__ == "__main__":
    main()
