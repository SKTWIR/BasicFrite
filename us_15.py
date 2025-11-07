# Fichier : us_15.py (Planification et Gestion Objectif/Séances avec Sauvegarde CSV)

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Nécessaire pour la Combobox
import sys
import os
import csv

# --- CONSTANTES ---
USER_CSV_FILE = os.path.join(os.path.dirname(__file__), 'User.csv')
OBJECTIFS = ["Force", "Hypertrophie", "Endurance"]

# Définition complète des en-têtes (13 CHAMPS)
CSV_FIELDS = [
    "id_user", "pseudo", "nom", "prénom", "age", "poids", "taille", 
    "motdepasse", "email", "is_admin", "statut", "nbentrainementsemaine", "objectif"
]

# --- 🧠 Logique d'adaptation de la répartition des groupes musculaires ---

def obtenir_repartition_musculaire(nb_seances: int) -> list:
    """Retourne la répartition suggérée en fonction du nombre de séances."""
    repartitions = {
        1: ["Full Body"],
        2: ["Haut du Corps", "Bas du Corps"], 
        3: ["Full Body", "Upper", "Lower"], 
        4: ["Haut du Corps (Force)", "Bas du Corps", "Haut du Corps (Volume)", "Bas du Corps"], 
        5: ["Poussée", "Tirage", "Jambes", "Haut du Corps Léger", "Bas du Corps Léger"], 
        6: ["Poussée", "Tirage", "Jambes", "Poussée", "Tirage", "Jambes"], 
    }
    return repartitions.get(nb_seances, ["⚠️ Nombre de séances non géré (Max 6)"])

# --- FONCTIONS CSV (Pour la sauvegarde) ---

def save_planning_and_objective(user_id, nb_seances_str, objectif_str, switch_to_menu_callback, current_data):
    """Met à jour les champs 'nbentrainementsemaine' et 'objectif' dans le CSV."""
    
    try:
        # 1. Validation de base
        nb_seances = int(nb_seances_str)
        if not 0 <= nb_seances <= 7:
            messagebox.showerror("Erreur", "Le nombre de séances doit être entre 0 et 7.")
            return

        rows = []
        updated_row = current_data.copy()
        found = False
        
        # 2. Lecture du CSV
        try:
            # --- CORRECTION ENCODAGE ICI ---
            # Utilisation de 'utf-8-sig' pour gérer le BOM
            with open(USER_CSV_FILE, mode='r', newline='', encoding='utf-8-sig') as f:
            # --- FIN CORRECTION ---
                reader = csv.DictReader(f, delimiter=';')
                fieldnames = reader.fieldnames
                
                # Vérification de sécurité (si les en-têtes CSV ne correspondent pas au code)
                if 'nbentrainementsemaine' not in fieldnames or 'objectif' not in fieldnames:
                    messagebox.showerror(
                        "Erreur CSV (En-têtes)", 
                        "Votre fichier User.csv est obsolète.\n\n"
                        "Il manque les colonnes ';nbentrainementsemaine;objectif' à la fin de la première ligne de User.csv."
                    )
                    return 

                for row in reader:
                    if row['id_user'] == user_id:
                        found = True
                        row['nbentrainementsemaine'] = nb_seances_str
                        row['objectif'] = objectif_str
                        updated_row = row.copy() 
                    rows.append(row)
                        
        except Exception as e:
            messagebox.showerror("Erreur Lecture CSV", f"Erreur (lecture): {e}")
            return
    
        if not found:
            messagebox.showerror("Erreur", "ID utilisateur non trouvé lors de la lecture.")
            return
    
        # 3. Écriture du CSV complet
        try:
            # Utilisation de la liste d'en-têtes complète (CSV_FIELDS)
            with open(USER_CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, delimiter=';')
                writer.writeheader()
                writer.writerows(rows)
                
            messagebox.showinfo("Succès", "Planification et Objectif mis à jour !")
            
            # 4. Retour au menu en passant les données mises à jour
            switch_to_menu_callback(updated_row) 
    
        except ValueError as ve:
             messagebox.showerror(
                "Erreur d'écriture (ValueError)", 
                f"Erreur: {ve}\nAssurez-vous que User.csv a les bons en-têtes."
             )
        except Exception as e:
            messagebox.showerror("Erreur Écriture CSV", f"Erreur (écriture): {e}")
            return
    
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre valide pour les séances.")
    except Exception as e:
        messagebox.showerror("Erreur CSV", f"Erreur de traitement du fichier: {e}")


# --- ⚙️ Fonctions de l'Interface Utilisateur (Tkinter) ---

def run_planning_screen(root_window, switch_to_menu_callback, user_data):
    """
    Crée et affiche l'interface de planification en utilisant la fenêtre root_window.
    """
    # ... (Le reste de l'interface reste inchangé) ...
    
    for widget in root_window.winfo_children():
        widget.destroy()
    
    current_nb_seances = user_data.get('nbentrainementsemaine', '4')
    current_objectif = user_data.get('objectif', 'Force')
        
    root_window.title("🏋️ Planificateur de Séances")
    root_window.geometry("500x550") 
    root_window.resizable(False, False)

    global entry_seances, label_resultat, combo_objectif 
    
    main_frame = tk.Frame(root_window, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    tk.Label(main_frame, text="Planification Hebdomadaire & Objectifs", font=("Arial", 16, "bold")).pack(pady=(0, 20))

    tk.Label(main_frame, text="1. Nombre de séances par semaine (0-6) :", anchor="w").pack(fill="x", pady=(10, 5))
    entry_seances = tk.Entry(main_frame, width=5, font=("Arial", 12))
    entry_seances.insert(0, current_nb_seances) 
    entry_seances.pack(pady=5)
    
    tk.Label(main_frame, text="2. Objectif Principal :", anchor="w").pack(fill="x", pady=(15, 5))
    objectif_var = tk.StringVar(main_frame)
    objectif_var.set(current_objectif if current_objectif in OBJECTIFS else OBJECTIFS[0]) 
    
    combo_objectif = ttk.Combobox(
        main_frame,
        textvariable=objectif_var,
        values=OBJECTIFS,
        state="readonly",
        width=30,
        font=("Arial", 12)
    )
    combo_objectif.pack(pady=5)

    tk.Button(
        main_frame, 
        text="💾 Enregistrer la Planification", 
        command=lambda: (
            save_planning_and_objective(
                user_data.get('id_user'), 
                entry_seances.get(), 
                objectif_var.get(),
                switch_to_menu_callback,
                user_data
            ),
            afficher_repartition() 
        ),
        bg="#2ECC71", fg="white", font=("Arial", 11, "bold")
    ).pack(pady=20)

    tk.Label(main_frame, text="3. Répartition Suggérée :", anchor="w", font=("Arial", 11, "underline")).pack(fill="x", pady=(10, 5))
    
    label_resultat = tk.Label(main_frame, text="[Cliquez sur Enregistrer pour voir la suggestion]", 
                              justify=tk.LEFT, padx=10, pady=10)
    label_resultat.pack(fill="x")
    
    def afficher_repartition():
        """Récupère la saisie et met à jour l'affichage de la répartition."""
        try:
            nb_seances = int(entry_seances.get())
            if not 0 <= nb_seances <= 6: 
                 label_resultat.config(text="Veuillez choisir entre 1 et 6 séances pour une répartition standard.")
                 return

            planning_semaine = obtenir_repartition_musculaire(nb_seances)

            lignes_seances = ""
            for i, seance in enumerate(planning_semaine):
                lignes_seances += f"Séance {i+1}: {seance}\n"

            resultat_text = f"Objectif: {objectif_var.get()}\nPlanning: {nb_seances} séances\n\n{lignes_seances.strip()}"
            label_resultat.config(text=resultat_text)
            
        except ValueError:
            label_resultat.config(text="Erreur: Entrez un nombre valide pour les séances.")

    tk.Button(root_window, 
              text="⬅️ Retour Menu Principal", 
              command=lambda: switch_to_menu_callback(user_data), 
              bg="#f0f0f0", 
              font=("Arial", 10)).pack(pady=10)
    
    if current_nb_seances and current_nb_seances.isdigit() and int(current_nb_seances) > 0:
        afficher_repartition()


if __name__ == '__main__':
    def dummy_menu_callback(data_recue):
        print(f"Retour au Menu! Données: {data_recue}")
        sys.exit()

    root = tk.Tk()
    dummy_data = {'id_user': '1', 'prénom': 'Test', 'nom': 'User', 'email': 'test@test.com', 'age': '25', 'poids': '70', 'taille': '1.80', 'nbentrainementsemaine': '4', 'objectif': 'Force'}
    run_planning_screen(root, dummy_menu_callback, dummy_data)
    root.mainloop()