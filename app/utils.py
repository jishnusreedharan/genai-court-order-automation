import csv

def load_csv_dict(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))

CUSTOMERS = load_csv_dict("customers.csv")
ACTIONS = load_csv_dict("actions.csv")

def validate_customer(nid):
    return next((r['customer_id'] for r in CUSTOMERS if r['national_id'] == nid), None)

def validate_action(action):
    return any(r['action_name'].lower() == action.lower() for r in ACTIONS)

def get_action_description(action):
    match = next((r['description'] for r in ACTIONS if r['action_name'].lower() == action.lower()), None)
    return match or ""
