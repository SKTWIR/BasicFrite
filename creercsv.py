import pandas as pd
import random
import numpy as np
import hashlib # Pour hacher les mots de passe (sécurité!)

# --- 1. DÉFINITION DES DONNÉES ET STRUCTURES ---

# 1.1 Logique de répétitions et séries par objectif
OBJECTIFS = {
    "Force": {"reps": [1, 5], "series": [3, 5], "type": "Force"},
    "Hypertrophie": {"reps": [8, 12], "series": [3, 4], "type": "Hypertrophie"},
    "Endurance": {"reps": [15, 25], "series": [2, 3], "type": "Endurance"},
}

# 1.2 Structure des programmes et parties du corps ciblées
PROGRAMMES = {
    "PPL": {
        "Poussée": ["Pectoraux", "Épaules", "Triceps"],
        "Tirage": ["Dos", "Biceps", "Trapèzes"],
        "Jambes": ["Jambes", "Fessiers", "Mollets", "Abdominaux"],
    },
    "Full Body": {
        "FB A": ["Pectoraux", "Dos", "Jambes"],
        "FB B": ["Épaules", "Biceps", "Triceps", "Jambes", "Abdominaux"],
    }
}

# Paramètres de génération
NB_UTILISATEURS = 10
NB_EXERCICES_PAR_GROUPE_MUSCULAIRE = 2 # Ex: 2 exercices de Pectoraux dans une séance Push
START_ID = 1

# --- 2. FONCTIONS D'AIDE ---

def generate_hashed_password(password):
    """Génère un hachage SHA-256 pour le mot de passe."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# --- 3. GÉNÉRATION DES DONNÉES SIMULÉES (TABLES 'User' et 'Exercice_musculation') ---

# 3.1 Génération des Utilisateurs (User)
data_user = []
for i in range(START_ID, START_ID + NB_UTILISATEURS):
    is_admin = (i == START_ID) # Le premier utilisateur est admin
    
    # Données aléatoires
    nom = f"Nom_{i}"
    prenom = f"Prenom_{i}"
    pseudo = f"user_{i}_train"
    email = f"user{i}@trainingapp.com"
    
    # Attributs physiques
    age = random.randint(20, 50)
    poids = random.randint(60, 100)
    taille = random.randint(160, 195)
    
    # Hachage sécurisé du mot de passe
    motdepasse_hache = generate_hashed_password("password123") 
    
    data_user.append({
        'id_user': i,
        'pseudo': pseudo,
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'poids': poids,
        'taille': taille,
        'motdepasse': motdepasse_hache,
        'email': email,
        'is_admin': is_admin
    })
df_user = pd.DataFrame(data_user)

# 3.2 Lecture des Exercices existants (Exercice_musculation)
try:
    df_exercices = pd.read_csv('Exercice_musculation.csv', sep=';')
    
    # Renommage et vérification pour la cohérence
    if 'id' in df_exercices.columns and 'id_exercice' not in df_exercices.columns:
        df_exercices.rename(columns={'id': 'id_exercice'}, inplace=True)
    
    if 'id_exercice' not in df_exercices.columns or 'PartieDuCorps' not in df_exercices.columns:
        print("Erreur: Colonnes 'id_exercice' et/ou 'PartieDuCorps' manquantes. Vérifiez votre Exercice_musculation.csv.")
        exit()
except FileNotFoundError:
    print("Erreur: Le fichier Exercice_musculation.csv est introuvable. Assurez-vous qu'il est dans le répertoire.")
    exit()

# --- 4. GÉNÉRATION DES ENTRAÎNEMENTS ET DES RELATIONS ---

data_entrainement = []
data_entrainement_exercice = []
data_user_training = []
current_entrainement_id = 1
utilisateur_ids = df_user['id_user'].tolist()

# 4.1 Génération des Entraînements types (PPL & Full Body)
for objectif, params in OBJECTIFS.items():
    min_reps, max_reps = params['reps']
    min_series, max_series = params['series']
    
    for programme_type, seances in PROGRAMMES.items():
        
        for seance_name, parties_ciblees in seances.items():
            
            # --- Création de l'Entraînement ---
            nom_entrainement = f"{programme_type} - {seance_name} ({objectif})"
            
            data_entrainement.append({
                'id_entrainement': current_entrainement_id,
                'nom_d_Entrainement': nom_entrainement
            })
            
            # --- 4.2 Lier l'Entraînement aux Exercices (Entrainement_Exercice) ---
            
            exercices_selectionnes = []
            
            for partie in parties_ciblees:
                # Filtrer les exercices disponibles (recherche flexible)
                exercices_disponibles = df_exercices[
                    df_exercices['PartieDuCorps'].astype(str).str.contains(partie, case=False, na=False)
                ]['id_exercice'].tolist()
                
                if exercices_disponibles:
                    # Choisir N exercices au hasard par partie
                    num_to_select = min(NB_EXERCICES_PAR_GROUPE_MUSCULAIRE, len(exercices_disponibles))
                    selection = random.sample(exercices_disponibles, num_to_select)
                    exercices_selectionnes.extend(selection)
            
            # Générer les lignes Entrainement_Exercice
            for exo_id in exercices_selectionnes:
                series = random.randint(min_series, max_series)
                repetitions = random.randint(min_reps, max_reps)
                
                data_entrainement_exercice.append({
                    'id_exercice': exo_id,
                    'id_entrainement': current_entrainement_id,
                    'series': series,
                    'repetitions': repetitions
                })
                
            # --- 4.3 Lier l'Entraînement aux Utilisateurs (RelationUserTraining) ---
            
            # Lier tous les programmes types à l'utilisateur Administrateur (ID 1)
            data_user_training.append({
                'id_user': utilisateur_ids[0], # Utilisateur Admin
                'id_entrainement': current_entrainement_id
            })

            # Lier quelques programmes au hasard à d'autres utilisateurs
            if programme_type == "PPL":
                user_list = random.sample(utilisateur_ids[1:], random.randint(2, 5))
                for user_id in user_list:
                     data_user_training.append({
                        'id_user': user_id,
                        'id_entrainement': current_entrainement_id
                    })
            
            current_entrainement_id += 1

df_entrainement = pd.DataFrame(data_entrainement)
df_entrainement_exercice = pd.DataFrame(data_entrainement_exercice)
df_user_training = pd.DataFrame(data_user_training)


# --- 5. ÉCRITURE DES FICHIERS CSV FINAUX ---

print("\n--- Écriture des fichiers CSV ---")

# 5.1 USER
df_user.to_csv('User_Generes.csv', index=False, sep='|')
print(f"✅ User_Generes.csv créé. ({len(df_user)} utilisateurs)")

# 5.2 ENTRAINEMENT
df_entrainement.to_csv('Entrainement_Generes.csv', index=False, sep=',') 
print(f"✅ Entrainement_Generes.csv créé. ({len(df_entrainement)} entraînements types)")

# 5.3 RELATION USER <-> ENTRAINEMENT
df_user_training.to_csv('RelationUserTraining_Generes.csv', index=False, sep=',')
print(f"✅ RelationUserTraining_Generes.csv créé. ({len(df_user_training)} relations)")

# 5.4 ENTRAINEMENT <-> EXERCICE
df_entrainement_exercice.to_csv('Entrainement_Exercice_Generes.csv', index=False, sep=',')
print(f"✅ Entrainement_Exercice_Generes.csv créé. ({len(df_entrainement_exercice)} lignes d'exercices)")

# 5.5 Le fichier Exercice_musculation est conservé, mais renommé pour la cohérence
df_exercices.to_csv('Exercice_musculation_Utilise.csv', index=False, sep=';')
print(f"✅ Exercice_musculation_Utilise.csv conservé. ({len(df_exercices)} exercices)")

print("\nOpération de génération de données terminée.")