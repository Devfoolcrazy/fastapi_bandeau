import yaml
import json

def load_questions_from_yaml(file_path):
    """
    Load questions from a YAML file and return the data.
    
    :param file_path: The path to the YAML file to load questions from.
    :return: The loaded data from the YAML file.
    """
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def convert_problems_to_dict(data):
    """
    Convert a list of problems into a dictionary using the problem name as the key.

    Parameters:
    data (list): A list of dictionaries representing problems.

    Returns:
    dict: A dictionary where the key is the problem name and the value is the problem dictionary.
    """
    return {problem['name']: problem for problem in data['problems']}


def load_prompts(file_path):
    """
    A function that loads prompts from a file.

    Parameters:
    file_path (str): The path to the file containing prompts.

    Returns:
    dict: The prompts loaded from the file.
    """
    with open(file_path, 'r') as file:
        prompts = json.load(file)
    return prompts