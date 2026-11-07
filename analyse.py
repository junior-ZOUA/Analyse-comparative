import pandas as pd
from journal import ecrire_log
from cleaning import extraire_nombre, normaliser_texte
from matching import creer_index_catalogue, trouver_produit_id

def preparer_toutes_les_donnees(df_catalogue, lagune, baobab, comptoir):
    """
    Transforme les 3 sources différentes en UN SEUL tableau propre.
    """
    index_cat = creer_index_catalogue(df_catalogue)
    tous_les_prix = []

    # --- 1. TRAITEMENT DE MARCHÉ LAGUNE ---
    for _, row in lagune.iterrows():
        pid, score = trouver_produit_id(row['designation'], index_cat)
        
        if pid:
            prix = extraire_nombre(row['prix'])
            dispo = (row['disponibilite'] == 'En stock' or row['disponibilite'] == 'Stock limité')
            if prix and dispo:
                tous_les_prix.append({'produit_id': pid, 'enseigne': 'Marché Lagune', 'prix_paye': prix})
        else:
            ecrire_log(f"Lagune : Produit non reconnu -> {row['designation']}", "WARNING")

    # --- 2. TRAITEMENT DE BAOBAB SHOP ---
    for item in baobab:
        pid, score = trouver_produit_id(item['title'], index_cat)
        
        if pid:
            # PIÈGE : Le prix payé = amount + delivery_fee
            prix = item['pricing']['amount'] + item['pricing']['delivery_fee']
            stock = item['stock']
            if stock > 0:
                tous_les_prix.append({'produit_id': pid, 'enseigne': 'Baobab Shop', 'prix_paye': prix})
        else:
            ecrire_log(f"Baobab : Produit non reconnu -> {item['title']}", "WARNING")

    # --- 3. TRAITEMENT DE COMPTOIR IVOIRE ---
    for _, row in comptoir.iterrows():
        pid, score = trouver_produit_id(row['Article'], index_cat)
        
        if pid:
            # PIÈGE : Prix payé = Prix catalogue - (Prix catalogue * Remise / 100)
            prix_cat = extraire_nombre(row['Prix catalogue (FCFA)'])
            remise = extraire_nombre(row['Remise (%)'])
            quantite = extraire_nombre(row['Quantité en rayon'])
            
            if prix_cat is not None and remise is not None and quantite is not None:
                prix_final = prix_cat * (1 - remise / 100)
                if quantite > 0:
                    tous_les_prix.append({'produit_id': pid, 'enseigne': 'Comptoir Ivoire', 'prix_paye': int(prix_final)})
        else:
            ecrire_log(f"Comptoir : Produit non reconnu -> {row['Article']}", "WARNING")

    # On transforme notre liste en tableau Pandas
    df_prix = pd.DataFrame(tous_les_prix)
    return df_prix

def generer_comparatif(df_prix):
    """
    Prend le tableau de tous les prix et calcule le minimum, l'écart, etc.
    """
    grouped = df_prix.groupby('produit_id')
    resultats = []
    
    for pid, group in grouped:
        if len(group) >= 2: # Le prof exige au moins 2 enseignes
            prix_min = group['prix_paye'].min()
            enseigne_min = group.loc[group['prix_paye'].idxmin(), 'enseigne']
            
            for _, row in group.iterrows():
                ecart_fcfa = row['prix_paye'] - prix_min
                ecart_pct = (ecart_fcfa / prix_min) * 100
                
                resultats.append({
                    'produit_id': pid,
                    'enseigne': row['enseigne'],
                    'prix_paye': row['prix_paye'],
                    'enseigne_moins_chere': enseigne_min,
                    'prix_min': prix_min,
                    'ecart_fcfa': ecart_fcfa,
                    'ecart_pct': round(ecart_pct, 2)
                })
                
    df_final = pd.DataFrame(resultats)
    return df_final

def generer_synthese(df_rapport):
    """Calcule les statistiques globales demandées par le prof."""
    print("\n=== 1. NOMBRE DE VICTOIRES (Enseigne la moins chère) ===")
    victoires = df_rapport[df_rapport['prix_paye'] == df_rapport['prix_min']]
    compte_victoires = victoires['enseigne'].value_counts()
    print(compte_victoires)

    print("\n=== 2. ÉCART MOYEN PAR ENSEIGNE (en %) ===")
    ecart_moyen = df_rapport.groupby('enseigne')['ecart_pct'].mean().round(2)
    print(ecart_moyen)

    print("\n=== 3. TOP 3 DES PRODUITS AVEC LE PLUS GROS ÉCART (en FCFA) ===")
    top_ecarts = df_rapport.drop_duplicates('produit_id').nlargest(3, 'ecart_fcfa')
    print(top_ecarts[['produit_id', 'ecart_fcfa', 'enseigne_moins_chere']])

def calculer_panier(df_prix):
    """Calcule le coût du panier selon les quantités demandées."""
    print("\n=== 4. CALCUL DU PANIER DE RENTRÉE ===")
    
    panier = {'P04': 1, 'P12': 1, 'P14': 2, 'P15': 1, 'P28': 1}
    resultats = {}
    
    for enseigne in df_prix['enseigne'].unique():
        total = 0
        manquants = []
        
        for pid, qte in panier.items():
            ligne = df_prix[(df_prix['produit_id'] == pid) & (df_prix['enseigne'] == enseigne)]
            
            if not ligne.empty:
                total += ligne.iloc[0]['prix_paye'] * qte
            else:
                manquants.append(pid)
                
        resultats[enseigne] = {'total': total, 'manquants': manquants}

    for enseigne, data in resultats.items():
        if data['manquants']:
            print(f"- {enseigne} : {data['total']} FCFA (Produits indisponibles : {', '.join(data['manquants'])})")
        else:
            print(f"- {enseigne} : {data['total']} FCFA (Panier complet !)")

    print("\n=== 5. LE PANIER IDÉAL (Acheter chaque article au moins cher) ===")
    total_ideal = 0
    for pid, qte in panier.items():
        lignes_produit = df_prix[df_prix['produit_id'] == pid]
        if not lignes_produit.empty:
            prix_min = lignes_produit['prix_paye'].min()
            total_ideal += prix_min * qte
            
    print(f"En achetant chaque article là où il est le moins cher, le panier coûte : {total_ideal} FCFA")

def analyser_historique(df_historique):
    """Compare les prix du Black Friday à la moyenne annuelle."""
    print("\n=== 7. ANALYSE DU BLACK FRIDAY (24 au 30 nov 2025) ===")
    
    df_historique['date'] = pd.to_datetime(df_historique['date'])
    
    moyennes_annuelles = df_historique.groupby('source')['prix_fcfa'].mean()
    
    debut_bf = pd.to_datetime('2025-11-24')
    fin_bf = pd.to_datetime('2025-11-30')
    masque_bf = (df_historique['date'] >= debut_bf) & (df_historique['date'] <= fin_bf)
    df_bf = df_historique[masque_bf]
    
    moyennes_bf = df_bf.groupby('source')['prix_fcfa'].mean()
    
    for source in moyennes_annuelles.index:
        if source in moyennes_bf.index:
            prix_annee = moyennes_annuelles[source]
            prix_bf = moyennes_bf[source]
            baisse = ((prix_annee - prix_bf) / prix_annee) * 100
            print(f"- {source} :")
            print(f"  * Moyenne annuelle : {prix_annee:.2f} FCFA")
            print(f"  * Black Friday     : {prix_bf:.2f} FCFA")
            print(f"  * Variation        : {baisse:.2f} %")