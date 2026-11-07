#  Analyse Comparative de Marché

Ce projet Python a été réalisé dans le cadre de ma formation (L2 Computer Science - DA Python). Il s'agit d'un outil d'analyse comparative de prix pour un client cherchant à acheter de l'électronique et de l'électroménager à Abidjan.

##  Objectif
Comparer les prix d'un même catalogue de produits vendus par trois enseignes fictives :
- **Marché Lagune** (CSV, export Excel français)
- **Baobab Shop** (JSON, API mobile)
- **Comptoir Ivoire** (Excel, classeur avec en-têtes décalés)

##  Fonctionnalités
- **Collecte multi-formats** : Lecture de CSV, JSON et Excel.
- **Nettoyage** : Parsing des prix textuels (ex: "102 900 FCFA"), gestion de l'encodage, normalisation des noms.
- **Rapprochement (Matching)** : Utilisation de `rapidfuzz` pour faire le lien entre les noms "sales" des boutiques et les noms officiels du catalogue (ex: "Fridge" -> "Réfrigérateur").
- **Comparatif** : Calcul du prix payé (avec livraison et remises), recherche du prix minimum et calcul des écarts (en FCFA et en %).
- **Décision** : Génération d'une synthèse (nombre de victoires par enseigne, top 3 des écarts) et calcul du coût du panier de rentrée.
- **Historique** : Analyse des prix sur l'année pour comparer la période du Black Friday à la moyenne annuelle.
- **Traçabilité** : Journalisation des anomalies dans un fichier `journal_erreurs.log`.

##  Technologies utilisées
- Python 3
- Pandas (Manipulation de données)
- Openpyxl (Lecture de fichiers Excel)
- Rapidfuzz (Correspondance floue / Fuzzy matching)

## Comment lancer le projet ?
1. Cloner le dépôt :
   `git clone https://github.com/junior-ZOUA/Analyse-comparative.git`
2. Créer un environnement virtuel : `python -m venv venv`
3. L'activer (Windows) : `venv\Scripts\activate`
4. Installer les dépendances : `pip install -r requirements.txt`
5. Lancer l'application console : `python main.py`
