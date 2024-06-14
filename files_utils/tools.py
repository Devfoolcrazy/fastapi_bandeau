import yaml
import json
import logging
import os

import pandas as pd

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

def load_csv(file_path):
    return pd.read_csv(file_path, delimiter=';')

def get_file_list(folder_path):
    """Liste les fichiers dans le dossier spécifié.
    
    Args:
        forlder_path (str): Le chemin vers le dossier dont on veut lister les fichiers.

    Returns:
        list: Une liste des noms des fichiers dans le dossier.
    """
    # Liste tous les éléments dans le dossier
    elements = os.listdir(folder_path)
    # Filtre pour ne garder que les fichiers (ignore les dossiers)
    files = [f for f in elements if os.path.isfile(os.path.join(folder_path, f))]
    return files