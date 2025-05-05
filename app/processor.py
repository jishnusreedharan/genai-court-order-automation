from app.utils import get_action_description

def process_action(customer_id, action):
    desc = get_action_description(action)
    return f"Action '{action}' ({desc}) executed for customer {customer_id}" if desc else f"Action '{action}' executed for customer {customer_id}"
