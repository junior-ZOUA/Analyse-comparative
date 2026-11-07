import pandas as pd
import json
from config import *

def charger_catalogue():
    # encoding='utf-8' corrige le problème des accents (ClÃ© -> Clé)
    return pd.read_csv(CHEMIN_CATALOGUE, encoding='utf-8')

def charger_lagune():
    return pd.read_csv(CHEMIN_LAGUNE, sep=';', encoding='utf-8')

def charger_baobab():
    with open(CHEMIN_BAOBAB, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['items'] # On retourne juste la liste des articles

def charger_comptoir():
    # skiprows=2 permet d'ignorer le titre (ligne 1) et la ligne vide (ligne 2)
    # L'en-tête sera donc lu à partir de la ligne 3 (index 2)
    return pd.read_excel(CHEMIN_COMPTOIR, skiprows=2)

def charger_historique():
    return pd.read_csv(CHEMIN_HISTORIQUE, encoding='utf-8')