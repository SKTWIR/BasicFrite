import tkinter as tk
from tkinter import messagebox
# Importe la fonction qui lance l'interface du menu principal
import app_gui 
# NOTE: Assurez-vous que app_gui.py est dans le même répertoire que us_15.py

# --- 🧠 Logique d'adaptation de la répartition des groupes musculaires ---

def obtenir_repartition_musculaire(nb_seances: int) -> list:
    # ... (Reste inchangé) ...
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
    
    return repartitions.get(nb_seances, ["⚠️ Nombre de séances non géré (Max 6)"])

# --- ⚙️ Fonctions de l'Interface Utilisateur (Tkinter) ---

# Déclarer fenetre en tant que variable globale pour que retour_menu puisse y accéder
global fenetre 

def afficher_repartition():
    # ... (Reste inchangé, sauf que 'fenetre' doit être accessible si vous la passez en paramètre, 
    # mais en global comme ici, ça fonctionne aussi) ...
    """
    Récupère la saisie de l'utilisateur, calcule la répartition 
    et met à jour l'affichage dans l'interface.
    """
    try:
        nb_seances_str = entry_seances.get()
        if not nb_seances_str:
            raise ValueError("Veuillez entrer un nombre.")
            
        nb_seances = int(nb_seances_str)
        
        if not 1 <= nb_seances <= 6:
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
        messagebox.showerror("Erreur de Saisie", f"Saisie invalide : {e}")
        label_resultat.config(text="Veuillez entrer un nombre valide.")

def retour_menu():
    """
    Ferme la fenêtre actuelle (us_15.py) et lance la fonction run_main_menu
    dans le module app_gui.py.
    """
    # 1. Fermer la fenêtre de planification actuelle
    fenetre.destroy()
    
    # 2. Lancer le menu principal/profil utilisateur
    app_gui.run_main_menu()
    print("Action : Retour au Menu Principal exécuté.")


# --- 🖼️ Configuration de la Fenêtre Principale (us_15.py) ---

# Crée la fenêtre principale
fenetre = tk.Tk()
fenetre.title("🏋️ Planificateur de Séances (us_15)")
fenetre.geometry("400x400") 

# --- Widgets ---
# ... (Création des labels, entry et boutons reste identique) ...

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

# 6. Bouton de retour au menu (MODIFIÉ)
bouton_menu = tk.Button(fenetre, 
                        text="⬅️ Retour Menu Principal", 
                        command=retour_menu, # Appel de la nouvelle fonction
                        bg="#f0f0f0", 
                        font=("Arial", 10))
bouton_menu.pack(pady=20)


# 7. Lancement de la boucle principale de l'interface
fenetre.mainloop()