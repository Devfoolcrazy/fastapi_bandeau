from typing import List, Dict, Any, Tuple

from datetime import date

from rules_data.path_transcoding import path_transcoding

def check_condition(json_data: Dict[str, Any], key: str, value: Dict[str, Any]) -> bool:
    """
    Check if a given condition is met in the JSON data.

    Parameters:
    - json_data: dictionary, the JSON data to be checked
    - key: string, the key to be checked in the JSON data
    - value: dictionary, contains 'path' and 'value' to compare against in the JSON data

    Returns:
    - bool: True if the condition is met, False otherwise
    """
    data_path = value.get('path')
    condition_value = value.get('value')
    current_data = json_data
    path_parts = data_path.split('.')
    
    for part in path_parts:
        if part in current_data:
            current_data = current_data[part]
        else:
            return False

    return current_data == condition_value



def apply_rules(json_data: Dict[str, Any], rules: List[Dict[str, Any]]) -> List[Tuple[str, str, int, date, str]]:
    """
    Generate the matched messages based on the given JSON data and rules.

    :param json_data: The JSON data to apply the rules to.
    :param rules: The rules to be applied to the JSON data.
    :return: A list of matched messages containing name, message, priority, rule validity, and code.
    """
    matched_messages: List[Tuple[str, str, int, date, str]] = []
    current_date: date = date.today()

    for rule in rules:
        condition_members: Dict[str, Any] = rule.get('conditions', {}).get('condition_members', {})
        for key, value in condition_members.items():
            condition_members[key] = apply_transcoding(value, path_transcoding)

        rule_validity: date = rule.get('conditions', {}).get('validity')

        if rule_validity and rule_validity < current_date:
            continue  # Ignorer les règles expirées

        condition_met: bool = all(check_condition(json_data, key, value) for key, value in condition_members.items())

        if condition_met:
            message: str = rule.get('conditions').get('message')
            priority: int = rule.get('conditions').get('priority')
            name: str = rule.get('conditions').get('name')
            code: str = rule.get('conditions').get('code')

            matched_messages.append((name, message, priority, rule_validity, code))

    return matched_messages


def format_matched_messages(matched_messages: List[tuple]) -> List[Dict[str, str]]:
    """
    Format the matched messages into a list of dictionaries containing 'name', 'message', 'priority', 'validity', and 'code' fields.
    
    Parameters:
    matched_messages (list): A list of tuples containing the matched messages with elements (name, message, priority, rule_validity, code).
    
    Returns:
    list: A list of dictionaries containing formatted messages with fields 'name', 'message', 'priority', 'validity', and 'code'.
    """
    formatted_messages = [
        {
            "name": name,
            "message": message,
            "priority": priority,
            "validity": rule_validity,
            "code": code
        }
        for name, message, priority, rule_validity, code in matched_messages
    ]
    return formatted_messages

def apply_transcoding(condition, path_transcoding):
    if condition['path'] in path_transcoding:
        condition['path'] = path_transcoding[condition['path']]
    return condition