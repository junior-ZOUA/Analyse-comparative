import unicodedata
import re

def normaliser_texte(texte):
    """Transforme 'Écouteurs  Sans-Fil ' en 'ecouteurs sans fil'"""
    if not isinstance(texte, str):
        return ""
    # Enlever les accents
    texte = ''.join(c for c in unicodedata.normalize('NFD', texte) if unicodedata.category(c) != 'Mn')
    # Minuscules et suppression des espaces en trop
    return " ".join(texte.lower().strip().split())

def extraire_nombre(texte):
    """Transforme '102 900 FCFA' ou '109 400' ou '3,4' en nombre propre (float ou int)"""
    if isinstance(texte, (int, float)):
        return float(texte)
    if not isinstance(texte, str):
        return None
    
    # Remplacer la virgule par un point (pour les notes)
    texte = texte.replace(',', '.')
    
    # Ne garder que les chiffres et le point
    texte_propre = re.sub(r'[^\d.]', '', texte)
    
    try:
        # Si c'est un entier (ex: 102900.0), on le convertit en int
        valeur = float(texte_propre)
        return int(valeur) if valeur.is_integer() else valeur
    except ValueError:
        return None