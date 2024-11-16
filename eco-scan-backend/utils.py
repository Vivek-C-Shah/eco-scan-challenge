# utils.py

import json

def calculate_reward_points(total_carbon_score):
    # Simple logic: 1 point per kg CO₂ saved
    eco_reward_points = total_carbon_score // 1000
    return eco_reward_points

def parse_gpt_response(response_content):
    """
    Parses the GPT response to extract the list of clothing items.
    Assumes the GPT model returns a JSON array of item names.
    """
    try:
        # Find the JSON array in the response
        start_index = response_content.find('[')
        end_index = response_content.find(']', start_index) + 1
        items_json = response_content[start_index:end_index]
        identified_items = json.loads(items_json)
        return identified_items
    except Exception as e:
        print(f"Error parsing GPT response: {e}")
        # If parsing fails, return an empty list
        return []
