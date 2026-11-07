import time
import pandas as pd
from loaders import *
from cleaning import *
from journal import ecrire_log
from analyse import (
    preparer_toutes_les_donnees, 
    generer_comparatif, 
    generer_synthese, 
    calculer_panier, 
    analyser_historique
)

def afficher_menu():
    print("\n--------------------------------------------------------")
    print("                    MENU PRINCIPAL")
    print("--------------------------------------------------------")
    print("[1] Charger les données des enseignes")
    print("[2] Nettoyer et préparer les données")
    print("[3] Consulter le catalogue des produits")
    print("[4] Rechercher un produit")
    print("[5] Comparer les prix des trois enseignes")
    print("[6] Consulter la synthèse comparative")
    print("[7] Calculer le coût du panier de rentrée")
    print("[8] Analyser l'historique des prix")
    print("[9] Consulter le journal des anomalies")
    print("[10] Exporter les résultats en CSV")
    print("[11] Mesurer la complexité et le temps d'exécution")
    print("[0] Quitter l'application")
    print("========================================================")
    return input("Votre choix : ")

def main():
    print("\n       Bienvenue dans votre comparateur de prix !\n")
    print("        Sources :")
    print("        [1] Marché Lagune")
    print("        [2] Baobab Shop")
    print("        [3] Comptoir Ivoire")

    # Variables pour stocker les données en mémoire (l'état de l'application)
    df_cat = None
    df_lag = None
    baobab = None
    df_comp = None
    df_hist = None
    df_prix = None
    df_rapport = None

    ecrire_log("Démarrage de l'application", "INFO")
    
    while True:
        choix = afficher_menu()
        
        if choix == "1":
            ecrire_log("Chargement des fichiers sources...", "INFO")
            print("\n Chargement en cours...")
            df_cat = charger_catalogue()
            df_lag = charger_lagune()
            baobab = charger_baobab()
            df_comp = charger_comptoir()
            df_hist = charger_historique()
            print(" Toutes les données ont été chargées en mémoire !")
            
        elif choix == "2":
            if df_lag is None:
                print(" Veuillez d'abord charger les données (Choix 1).")
                continue
            print("\n Nettoyage des prix de Marché Lagune...")
            # On ajoute la colonne propre
            df_lag['prix_clean'] = df_lag['prix'].apply(extraire_nombre)
            print(" Nettoyage terminé. Les prix sont prêts pour l'analyse.")

        elif choix == "3":
            if df_cat is None:
                print(" Veuillez d'abord charger les données (Choix 1).")
                continue
            print("\n--- CATALOGUE DES PRODUITS ---")
            print(df_cat[['produit_id', 'nom', 'marque']].to_string(index=False))

        elif choix == "4":
            if df_cat is None:
                print(" Veuillez d'abord charger les données (Choix 1).")
                continue
            recherche = input("\nEntrez le nom d'un produit à rechercher : ")
            # On utilise notre fonction de matching
            from matching import creer_index_catalogue, trouver_produit_id
            index_cat = creer_index_catalogue(df_cat)
            pid, score = trouver_produit_id(recherche, index_cat)
            
            if pid:
                produit = df_cat[df_cat['produit_id'] == pid].iloc[0]
                print(f"\n Produit trouvé (Similarité {score:.1f}%) : {produit['produit_id']} - {produit['nom']}")
            else:
                print("\n Produit introuvable dans le catalogue.")

        elif choix == "5":
            if df_lag is None or 'prix_clean' not in df_lag.columns:
                print(" Veuillez d'abord charger (1) et nettoyer (2) les données.")
                continue
            print("\n Comparaison des prix en cours...")
            df_prix = preparer_toutes_les_donnees(df_cat, df_lag, baobab, df_comp)
            df_rapport = generer_comparatif(df_prix)
            print(" Comparatif généré avec succès !")

        elif choix == "6":
            if df_rapport is None:
                print(" Veuillez d'abord faire la comparaison (Choix 5).")
                continue
            generer_synthese(df_rapport)

        elif choix == "7":
            if df_prix is None:
                print(" Veuillez d'abord faire la comparaison (Choix 5).")
                continue
            calculer_panier(df_prix)

        elif choix == "8":
            if df_hist is None:
                print(" Veuillez d'abord charger les données (Choix 1).")
                continue
            analyser_historique(df_hist)

        elif choix == "9":
            print("\n--- JOURNAL DES ANOMALIES (Dernières lignes) ---")
            try:
                with open("sorties/journal_erreurs.log", "r", encoding="utf-8") as f:
                    lignes = f.readlines()
                    # Afficher les 15 dernières lignes du journal
                    for ligne in lignes[-15:]:
                        print(ligne.strip())
                print(f"\n(Total : {len(lignes)} lignes dans le journal. Fichier complet dans sorties/)")
            except FileNotFoundError:
                print("Aucun journal trouvé pour le moment.")

        elif choix == "10":
            if df_rapport is None:
                print(" Veuillez d'abord faire la comparaison (Choix 5).")
                continue
            df_rapport.to_csv("sorties/rapport_comparatif.csv", index=False, encoding='utf-8')
            print("\n Le fichier 'sorties/rapport_comparatif.csv' a bien été exporté !")

        elif choix == "11":
            if df_hist is None:
                print(" Veuillez d'abord charger les données (Choix 1).")
                continue
            print("\n Mesure de la complexité (Analyse de l'historique de 20 876 lignes)...")
            debut_chrono = time.perf_counter()
            
            analyser_historique(df_hist)
            
            fin_chrono = time.perf_counter()
            temps_execution = fin_chrono - debut_chrono
            print(f"\n Résultat : Le traitement a pris {temps_execution:.4f} secondes.")

        elif choix == "0":
            ecrire_log("Fermeture de l'application.", "INFO")
            print("\nAu revoir ! ")
            break
            
        else:
            print("\n Choix invalide. Veuillez taper un nombre entre 0 et 11.")

if __name__ == "__main__":
    main()