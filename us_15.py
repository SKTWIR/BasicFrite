import tkinter as tk
from tkinter import messagebox

# --- 🧠 Logique d'adaptation de la répartition des groupes musculaires ---

def obtenir_repartition_musculaire(nb_seances: int) -> list:
    """
    Retourne la liste des groupes musculaires/types de séances par jour
    en fonction du nombre total de séances hebdomadaires (de 1 à 6).
    """
    
    # Dictionnaire de répartition prédéfinies
    repartitions = {
        1: ["Full Body"],
        2: ["Haut du Corps", "Bas du Corps"], 
        3: ["Full Body", "Upper", "Lower"], 
        4: ["Haut du Corps (Force)", "Bas du Corps", "Haut du Corps (Volume)", "Bas du Corps"], 
        5: ["Poussée", "Tirage", "Jambes", "Haut du Corps Léger", "Bas du Corps Léger"], 
        6: ["Poussée", "Tirage", "Jambes", "Poussée", "Tirage", "Jambes"], 
    }
    
    # Retourne la répartition gérée, ou un message si le nombre n'est pas pris en charge
    return repartitions.get(nb_seances, ["⚠️ Nombre de séances non géré (Max 6)"])

# --- ⚙️ Fonctions de l'Interface Utilisateur (Tkinter) ---

def afficher_repartition():
    """
    Récupère la saisie de l'utilisateur, calcule la répartition 
    et met à jour l'affichage dans l'interface.
    """
    try:
        # Récupère la valeur entrée et la convertit en entier
        nb_seances_str = entry_seances.get()
        if not nb_seances_str:
            # Si le champ est vide
            raise ValueError("Veuillez entrer un nombre.")
            
        nb_seances = int(nb_seances_str)
        
        if not 1 <= nb_seances <= 6:
            # Gère les cas hors de la plage 1-6
            messagebox.showwarning("Avertissement", "Veuillez entrer un nombre de séances entre 1 et 6.")
            return

        # 1. Obtenir la liste des séances
        planning_semaine = obtenir_repartition_musculaire(nb_seances)

        # 2. Construire la chaîne de caractères pour l'affichage
        lignes_seances = ""
        for i, seance in enumerate(planning_semaine):
            lignes_seances += f"Séance {i+1}: {seance}\n"

        # 3. Mettre à jour le Label de résultat
        resultat_text = f"**{nb_seances}** séances par semaine :\n\n{lignes_seances.strip()}"
        label_resultat.config(text=resultat_text)
        
    except ValueError as e:
        # Gère les erreurs de conversion (si l'utilisateur entre du texte, etc.)
        messagebox.showerror("Erreur de Saisie", f"Saisie invalide : {e}")
        label_resultat.config(text="Veuillez entrer un nombre valide.")

def retour_menu():
    """
    Fonction appelée par le bouton 'Retour Menu'.
    Dans une vraie application, elle chargerait l'écran principal.
    """
    # ⚠️ TODO: Insérer ici le code pour charger l'écran du menu principal
    print("Action : Retour au Menu Principal (Fonctionnalité en attente de développement)")
    messagebox.showinfo("Menu", "Retour au Menu Principal...\n(Cette fonction n'est pas encore développée dans ce module)")


# --- 🖼️ Configuration de la Fenêtre Principale ---

# Crée la fenêtre principale
fenetre = tk.Tk()
fenetre.title("🏋️ Planificateur de Séances")
fenetre.geometry("400x400") # Taille de la fenêtre

# --- Widgets ---

# 1. Titre
label_titre = tk.Label(fenetre, text="Planification Hebdomadaire", font=("Arial", 16, "bold"))
label_titre.pack(pady=15)

# 2. Demande de saisie
label_saisie = tk.Label(fenetre, text="Nombre de séances par semaine (1-6) :", font=("Arial", 10))
label_saisie.pack()

# 3. Champ de saisie
entry_seances = tk.Entry(fenetre, width=5, font=("Arial", 12))
entry_seances.pack(pady=5)
entry_seances.insert(0, "4") # Valeur par défaut

# 4. Bouton de calcul/affichage
bouton_calculer = tk.Button(fenetre, 
                           text="Afficher la Répartition", 
                           command=afficher_repartition, 
                           bg="#4CAF50", fg="white", 
                           font=("Arial", 11, "bold"))
bouton_calculer.pack(pady=10)

# 5. Zone d'affichage des résultats
label_resultat = tk.Label(fenetre, text="Cliquez sur 'Afficher la Répartition' pour commencer.", 
                           justify=tk.LEFT, 
                           font=("Arial", 10), 
                           padx=10, pady=10)
label_resultat.pack(pady=15)

# 6. Bouton de retour au menu
bouton_menu = tk.Button(fenetre, 
                        text="⬅️ Mes informations personnelles", 
                        command=retour_menu, 
                        bg="#f0f0f0", 
                        font=("Arial", 10))
bouton_menu.pack(pady=20)


# 7. Lancement de la boucle principale de l'interface (nécessaire pour afficher la fenêtre)
fenetre.mainloop()