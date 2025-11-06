# Fichier : us_15.py

import tkinter as tk
from tkinter import messagebox
# Nous ne pouvons plus importer app_gui car ce n'est pas le standard du menu.
# Nous allons utiliser un callback pour le retour au menu.

# --- 🧠 Logique d'adaptation de la répartition des groupes musculaires ---

def obtenir_repartition_musculaire(nb_seances: int) -> list:
    """
    Retourne la liste des groupes musculaires/types de séances par jour
    en fonction du nombre total de séances hebdomadaires (de 1 à 6).
    """
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

def run_planning_screen(root_window, switch_to_menu_callback):
    """
    Crée et affiche l'interface de planification en utilisant la fenêtre root_window.
    """
    # Nettoyer l'écran précédent
    for widget in root_window.winfo_children():
        widget.destroy()
        
    root_window.title("🏋️ Planificateur de Séances (us_15)")
    root_window.geometry("400x400") 
    root_window.resizable(False, False)

    # Variables d'accès local pour les fonctions internes
    global entry_seances, label_resultat 
    
    # --- Fonction Afficher Répartition (intégrée/adaptée) ---
    def afficher_repartition():
        """Récupère la saisie, calcule la répartition et met à jour l'affichage."""
        try:
            nb_seances_str = entry_seances.get()
            if not nb_seances_str:
                raise ValueError("Veuillez entrer un nombre.")
                
            nb_seances = int(nb_seances_str)
            
            if not 1 <= nb_seances <= 6:
                messagebox.showwarning("Avertissement", "Veuillez entrer un nombre de séances entre 1 et 6.")
                return

            planning_semaine = obtenir_repartition_musculaire(nb_seances)

            lignes_seances = ""
            for i, seance in enumerate(planning_semaine):
                lignes_seances += f"Séance {i+1}: {seance}\n"

            resultat_text = f"**{nb_seances}** séances par semaine :\n\n{lignes_seances.strip()}"
            label_resultat.config(text=resultat_text)
            
        except ValueError as e:
            messagebox.showerror("Erreur de Saisie", f"Saisie invalide : {e}")
            label_resultat.config(text="Veuillez entrer un nombre valide.")

    # --- Widgets ---

    # 1. Titre
    label_titre = tk.Label(root_window, text="Planification Hebdomadaire", font=("Arial", 16, "bold"))
    label_titre.pack(pady=15)

    # 2. Demande de saisie
    label_saisie = tk.Label(root_window, text="Nombre de séances par semaine (1-6) :", font=("Arial", 10))
    label_saisie.pack()

    # 3. Champ de saisie
    entry_seances = tk.Entry(root_window, width=5, font=("Arial", 12))
    entry_seances.pack(pady=5)
    entry_seances.insert(0, "4") # Valeur par défaut

    # 4. Bouton de calcul/affichage
    bouton_calculer = tk.Button(root_window, 
                               text="Afficher la Répartition", 
                               command=afficher_repartition, 
                               bg="#4CAF50", fg="white", 
                               font=("Arial", 11, "bold"))
    bouton_calculer.pack(pady=10)

    # 5. Zone d'affichage des résultats
    label_resultat = tk.Label(root_window, text="Cliquez sur 'Afficher la Répartition' pour commencer.", 
                              justify=tk.LEFT, 
                              font=("Arial", 10), 
                              padx=10, pady=10)
    label_resultat.pack(pady=15)

    # 6. Bouton de retour au menu
    bouton_menu = tk.Button(root_window, 
                           text="⬅️ Retour Menu Principal", 
                           command=switch_to_menu_callback, # Utilise le callback fourni par le menu
                           bg="#f0f0f0", 
                           font=("Arial", 10))
    bouton_menu.pack(pady=20)


# Si le fichier est exécuté seul (pour test)
if __name__ == '__main__':
    def dummy_menu_callback():
        print("Retour au Menu!")
        sys.exit()

    root = tk.Tk()
    run_planning_screen(root, dummy_menu_callback)
    root.mainloop()