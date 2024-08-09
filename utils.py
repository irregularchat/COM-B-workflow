import json

def get_user_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        print("EOFError: Input stream ended unexpectedly.")
        return ""

def parse_pta(pta):
    try:
        pta_list = pta.split('\n')
        return [p.strip() for p in pta_list if p.strip()]
    except Exception as e:
        print(f"Error parsing potential target audience: {e}")
        return []

