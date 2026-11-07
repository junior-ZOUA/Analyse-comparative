import datetime
from config import CHEMIN_JOURNAL

def ecrire_log(message, niveau="INFO"):
    """Écrit une ligne dans le journal des erreurs et l'affiche dans la console."""
    date_heure = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ligne = f"[{date_heure}] [{niveau}] {message}"
    
    # Affichage console
    print(ligne)
    
    # Écriture dans le fichier
    with open(CHEMIN_JOURNAL, "a", encoding="utf-8") as f:
        f.write(ligne + "\n")