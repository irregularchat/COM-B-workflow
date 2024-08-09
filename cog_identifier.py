import argparse
from cog_utils import define_cog  # Assuming this utility exists
from utils import load_data, save_output, get_user_input  # General utility functions

def main():
    parser = argparse.ArgumentParser(description="Identify the Center of Gravity (COG).")
    parser.add_argument("--input", type=str, required=True, help="Path to the input file")
    parser.add_argument("--output", type=str, required=True, help="Path to save the COG analysis")
    
    args = parser.parse_args()
    
    # Load input data
    data = load_data(args.input)
    
    # Prompt user to select entities
    print("Select the entities for which you want to identify the COG:")
    print("1. Friendly")
    print("2. Partner")
    print("3. Competitor")
    print("4. All")
    
    selection = get_user_input("Enter your choice (e.g., 1,2 or 4 for all): ")
    selected_entities = []

    if selection:
        if '1' in selection:
            selected_entities.append("friendly")
        if '2' in selection:
            selected_entities.append("partner")
        if '3' in selection or not selected_entities:
            selected_entities.append("competitor")
        if '4' in selection:
            selected_entities = ["friendly", "partner", "competitor"]
    else:
        selected_entities = ["competitor"]  # Default to competitor if left blank

    cog_results = {}
    
    for entity in selected_entities:
        cog = define_cog(
            entity_type=entity,
            area_of_focus=data.get("area_of_focus", ""),
            operational_objective=data.get("operational_objective", ""),
            constraints=data.get("constraints", ""),
            restraints=data.get("restraints", ""),
            mission_statement=data.get("mission_statement", "")
        )
        cog_results[entity] = cog
    
    # Save the output
    save_output(args.output, cog_results)
    print(f"Center of Gravity (COG) analysis saved to {args.output}")

if __name__ == "__main__":
    main()
