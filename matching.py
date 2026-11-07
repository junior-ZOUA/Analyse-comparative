from rapidfuzz import process, fuzz
from cleaning import normaliser_texte

def creer_index_catalogue(df_catalogue):
    """
    Crée un dictionnaire qui associe le nom normalisé du catalogue à son ID.
    Exemple : {'samsung galaxy a15 128 go': 'P01', ...}
    """
    index = {}
    for _, row in df_catalogue.iterrows():
        nom_norm = normaliser_texte(row['nom'])
        index[nom_norm] = row['produit_id']
    return index

def trouver_produit_id(nom_brut, index_catalogue):
    """
    Cherche le produit_id correspondant au nom d'une boutique.
    Retourne un tuple : (produit_id, score_de_similarite)
    """
    if not isinstance(nom_brut, str):
        return None, 0

    nom_norm = normaliser_texte(nom_brut)
    
    # 1. Essai exact (le nom est identique après normalisation)
    if nom_norm in index_catalogue:
        return index_catalogue[nom_norm], 100
    
    # 2. Essai approximatif (matching flou) si l'exact ne marche pas
    # process.extractOne cherche la meilleure correspondance
    choix = process.extractOne(nom_norm, index_catalogue.keys(), scorer=fuzz.token_sort_ratio)
    
    # Si on trouve une correspondance avec un score de similarité >= 75%
    if choix and choix[1] >= 75:
        return index_catalogue[choix[0]], choix[1]
        
    # Si le score est trop bas, on considère qu'on ne connaît pas ce produit
    return None, 0