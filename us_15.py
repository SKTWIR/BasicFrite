# --- Définition du nombre de séances par semaine ---

# Variable pour stocker le nombre de séances d'entraînement
# La valeur par défaut est mise à 3 comme exemple.
# Dans une vraie application, cette valeur serait saisie par l'utilisateur.
nombre_seances_par_semaine = 3

# ---  Logique d'adaptation de la répartition des groupes musculaires ---

def obtenir_repartition_musculaire(nb_seances: int) -> dict:
    """
    Retourne la répartition des groupes musculaires par séance
    en fonction du nombre total de séances hebdomadaires.
    """
    
    # Dictionnaire de répartition prédéfinies
    # Clé : Nombre de séances
    # Valeur : Liste des groupes/types de séances par jour
    repartitions = {
        1: ["Full Body"],
        2: ["Haut du Corps", "Bas du Corps"], # Upper/Lower
        3: ["Full Body", "Upper", "Lower"], # OU Push/Pull/Legs (PPL) simplifé
        4: ["Haut du Corps (Force)", "Bas du Corps", "Haut du Corps (Volume)", "Bas du Corps"], # Upper/Lower x2
        5: ["Poussée (Pecs/Epaules/Triceps)", "Tirage (Dos/Biceps)", "Jambes", "Haut du Corps Léger", "Bas du Corps Léger"], # Split 5 jours
        6: ["Poussée", "Tirage", "Jambes", "Poussée", "Tirage", "Jambes"], # Push/Pull/Legs (PPL) x2
    }
    
    # Récupération de la répartition, ou utilisation d'une valeur par défaut
    # si le nombre de séances n'est pas géré (ou si l'utilisateur entre 0, >6, etc.)
    return repartitions.get(nb_seances, ["Répartition Personnalisée / Non Gérée"])

# --- Utilisation dans le code ---

# Appel de la fonction pour obtenir le planning
planning_semaine = obtenir_repartition_musculaire(nombre_seances_par_semaine)

print(f"👉 Nombre de séances par semaine entré : **{nombre_seances_par_semaine}**")
print("---")
print("🗓️ Répartition musculaire suggérée pour la semaine :")

# Affichage du planning
for i, seance in enumerate(planning_semaine):
    print(f"Séance {i+1}: **{seance}**")

# ---
# Exemple de ce que vous feriez dans l'application :
# Le 'planning_semaine' (par exemple ['Full Body', 'Upper', 'Lower'])
# sera ensuite utilisé pour charger les exercices correspondants
# pour chaque jour d'entraînement.
# ---