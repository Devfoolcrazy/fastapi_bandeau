import yaml
import json
import logging

def load_rules_from_yaml(filename: str) -> dict:
    """
    Load rules from a YAML file.
    
    Args:
        filename (str): The name of the YAML file to load.
        
    Returns:
        dict: The loaded rules.
    """
    try:
        with open(filename, 'r') as f:
            rules = yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        raise

    return rules
