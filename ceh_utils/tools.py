from typing import List, Dict, Any, Tuple, Callable
import operator
import re

from datetime import date

from rules_data.path_transcoding import path_transcoding


def parse_condition(condition: str) -> List[Tuple[Callable[[Any, Any], bool], Any]]:
    """
    Analyse la condition pour identifier les opérateurs et les valeurs de comparaison.
    Gère les expressions combinées avec 'or'.

    Args:
    condition (str): La condition sous forme de chaîne de caractères.

    Returns:
    List[Tuple[Callable, Any]]: Une liste de tuples contenant l'opérateur de comparaison et la valeur.
    """
    operators = {
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '=': operator.eq  # Gérer l'égalité explicite si nécessaire
    }
    # Séparer les conditions basées sur 'or'
    sub_conditions = [sub.strip() for sub in condition.split('or')]
    conditions = []

    # Regex pour extraire les opérateurs et les valeurs
    pattern = r'([><]=?|=)\s*([0-9]+(?:\.[0-9]+)?)'
    
    for sub in sub_conditions:
        match = re.search(pattern, sub)
        if match:
            op_symbol, value = match.groups()
            op = operators[op_symbol]
            value = float(value)
            conditions.append((op, value))
    
    return conditions
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
        # Gestion des opérateurs complexes
    if isinstance(condition_value, str) and any(op in condition_value for op in ['>', '<', '>=', '<=', 'or']):
        # Analyser la condition si elle est une chaîne contenant un opérateur spécial
        parsed_condition = parse_condition(condition_value)
        if isinstance(parsed_condition, list):
            # Gestion des conditions avec 'or'
            return any(op(current_data, val) for op, val in parsed_condition)
        else:
            op, val = parsed_condition
            return op(current_data, val)
    else:
        # Comparaison directe pour les égalités simples
        return current_data == condition_value


def apply_rules(json_data: Dict[str, Any], rules: List[Dict[str, Any]]) -> List[Tuple[str, str, int, date, date, str]]:
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
            created_at: date = rule.get('conditions').get('created_at')
            name: str = rule.get('conditions').get('name')
            code: str = rule.get('conditions').get('code')
            condition_members_len = len(condition_members)
            matched_messages.append((name, message, priority, created_at, rule_validity, code, condition_members_len))

    return matched_messages


def format_matched_message(matched_message: List[tuple]) -> List[Dict[str, str]]:
    """
    Format the matched messages into a list of dictionaries containing 'name', 'message', 'priority', 'created_at', 'validity', and 'code' fields.

    Parameters:
    matched_messages (list): A list of tuples containing the matched messages with elements (name, message, priority, rule_validity, code).
    
    Returns:
    list: A list of dictionaries containing formatted messages with fields 'name', 'message', 'priority', 'created_at', 'validity', and 'code'.
    """
    (name, message, priority, created_at, rule_validity, code, condition_members_len) = matched_message
    formatted_messages: List[Dict[str, str]] = [
        {
            "name": name,
            "message": message,
            "priority": priority,
            "created_at": created_at,
            "validity": rule_validity,
            "code": code, 
        }
    ]
    return formatted_messages

def apply_transcoding(condition, path_transcoding):
    if condition['path'] in path_transcoding:
        condition['path'] = path_transcoding[condition['path']]
    return condition

def select_highest_priority_rule(rules):
    """
    Cette fonction prend une liste de règles où chaque règle est un tuple contenant:
    (name, message, priority, created_at, rule_validity, code, condition_members_len)
    et retourne la règle avec la priorité la plus élevée et la plus récente en cas d'égalité.
    
    Args:
    rules (list of tuples): Liste des règles.
    
    Returns:
    tuple: La règle sélectionnée avec la priorité la plus élevée et la plus récente.
    """
    if not rules:
        return None
    
    # On utilise max avec une clé qui prend en compte la priorité et la date de création inverse
    # pour que la règle la plus récente soit choisie en cas d'égalité de priorité.
    return max(rules, key=lambda rule: (-rule[2], rule[3].toordinal(), rule[6]))


def get_meteo_for_location(ceh_data: Dict[str, Any]) -> str:
    """
    Get the weather for a given location for assistance vehicle
    """
    request_type = ceh_data.get('flow', {}).get('content', {}).get('collectedData', {}).get('request', {}).get('requestType', {})
    
    weather = ceh_data.get('flow', {}).get('content', {}).get('collectedData', {}).get('requestGeneralInformation', {}).get('weather', {})

    waiting = ceh_data.get('flow', {}).get('content', {}).get('collectedData', {}).get('requestGeneralInformation', {}).get('waiting', {})
    
