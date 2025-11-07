# Fichier : us_seances_editor.py (Corrigé pour l'encodage)

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
import csv

# --- CONSTANTES ---
USER_CSV_FILE = os.path.join(os.path.dirname(__file__), 'User.csv')
ENTRAINEMENT_CSV_FILE = os.path.join(os.path.dirname(__file__), 'Entrainement.csv')
SEANCES_USER_CSV_FILE = os.path.join(os.path.dirname(__file__), 'Seances_Utilisateur.csv')

# --- Fonctions de lecture/écriture CSV ---

def load_all_workouts():
    """Charge tous les entraînements depuis Entrainement.csv dans un dict pour accès facile."""
    workouts = {}
    if not os.path.exists(ENTRAINEMENT_CSV_FILE):
        return {}
    try:
        # CORRECTION : Utilisation de utf-8-sig pour la lecture
        with open(ENTRAINEMENT_CSV_FILE, mode='r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                workouts[row['id_entrainement']] = row # Clé = ID, Valeur = Ligne
        return workouts
    except Exception as e:
        messagebox.showerror("Erreur Fichier", f"Erreur lecture Entrainement.csv: {e}")
        return {}

def load_user_seances(user_id):
    """Charge les séances spécifiques (juste les IDs) de l'utilisateur."""
    seances = []
    if not os.path.exists(SEANCES_USER_CSV_FILE):
        return []
    try:
        # CORRECTION : Utilisation de utf-8-sig pour la lecture
        with open(SEANCES_USER_CSV_FILE, mode='r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                # La clé 'user_id' est désormais correctement lue
                if row['user_id'] == user_id: 
                    seances.append(row)
        return seances
    except Exception as e:
        messagebox.showerror("Erreur Fichier", f"Erreur lecture Seances_Utilisateur.csv: {e}")
        return []

def get_next_seance_user_id():
    """Calcule le prochain ID unique pour Seances_Utilisateur.csv"""
    max_id = 0
    if not os.path.exists(SEANCES_USER_CSV_FILE): return 1
    try:
        # CORRECTION : Utilisation de utf-8-sig pour la lecture
        with open(SEANCES_USER_CSV_FILE, mode='r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                try:
                    user_id = int(row['id_seance_user'])
                    if user_id > max_id: max_id = user_id
                except (ValueError, TypeError): continue 
        return max_id + 1
    except Exception: return 1 

def update_user_seance_count(user_id, new_count):
    """Met à jour 'nbentrainementsemaine' dans User.csv."""
    rows = []
    fieldnames = []
    
    try:
        # CORRECTION : Utilisation de utf-8-sig pour la lecture
        with open(USER_CSV_FILE, mode='r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            fieldnames = reader.fieldnames
            for row in reader:
                # La clé 'id_user' est désormais correctement lue
                if row['id_user'] == user_id:
                    row['nbentrainementsemaine'] = str(new_count)
                rows.append(row)
                
        # L'écriture reste en utf-8 standard
        with open(USER_CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(rows)
        return True
    except Exception as e:
        messagebox.showerror("Erreur Sauvegarde", f"Erreur mise à jour User.csv: {e}")
        return False

def save_user_seances(user_id, seances_list):
    """Réécrit toutes les séances pour un utilisateur dans Seances_Utilisateur.csv."""
    all_rows = []
    fieldnames = ['id_seance_user', 'user_id', 'id_entrainement']
    
    # 1. Lire toutes les séances SAUF celles de l'utilisateur actuel
    try:
        if os.path.exists(SEANCES_USER_CSV_FILE):
            # CORRECTION : Utilisation de utf-8-sig pour la lecture
            with open(SEANCES_USER_CSV_FILE, mode='r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                if reader.fieldnames:
                    fieldnames = reader.fieldnames
                for row in reader:
                    # La clé 'user_id' est désormais correctement lue
                    if row['user_id'] != user_id:
                        all_rows.append(row)
                        
        # 2. Ajouter les nouvelles séances de l'utilisateur actuel
        all_rows.extend(seances_list)
        
        # 3. Réécrire le fichier complet
        with open(SEANCES_USER_CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(all_rows)
        
        # 4. Mettre à jour le compteur dans User.csv
        update_user_seance_count(user_id, len(seances_list))
        
    except Exception as e:
        messagebox.showerror("Erreur Sauvegarde", f"Erreur sauvegarde Seances_Utilisateur.csv: {e}")

# --- INTERFACE ---

def run_seances_editor_screen(root_window, switch_back_callback, user_data):
    
    for w in root_window.winfo_children():
        w.destroy()
        
    root_window.title(f"📅 Mes Séances ({user_data.get('pseudo')})")
    root_window.geometry("700x500")
    
    # --- Chargement des données ---
    ALL_WORKOUTS = load_all_workouts()
    user_seances = load_user_seances(user_data['id_user'])
    
    # --- Fonctions de l'interface ---
    
    def refresh_listbox():
        """Met à jour la Listbox avec les séances actuelles."""
        listbox_seances.delete(0, 'end')
        for seance in user_seances:
            workout_id = seance['id_entrainement']
            # Retrouve les détails de l'entraînement
            workout_details = ALL_WORKOUTS.get(workout_id)
            if workout_details:
                display_text = (
                    f"ID: {workout_id} | {workout_details['nom_d_Entrainement']} "
                    f"({workout_details['programme_entrainement']}) - {workout_details['type_entrainement']}"
                )
                # Stocke l'ID unique de la SÉANCE (pas l'ID de l'entraînement)
                listbox_seances.insert('end', (display_text, seance['id_seance_user']))
            else:
                listbox_seances.insert('end', (f"ID Entraînement {workout_id} introuvable", seance['id_seance_user']))

    def delete_seance():
        """Supprime la séance sélectionnée."""
        selected_idx = listbox_seances.curselection()
        if not selected_idx:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une séance à supprimer.")
            return
            
        selected_tuple = listbox_seances.get(selected_idx[0])
        id_seance_to_delete = selected_tuple[1] # Récupère le id_seance_user

        if not messagebox.askyesno("Confirmer", "Êtes-vous sûr de vouloir supprimer cette séance ?"):
            return
            
        # Retirer de la liste
        user_seances[:] = [s for s in user_seances if s['id_seance_user'] != id_seance_to_delete]
        
        # Sauvegarder (met aussi à jour User.csv)
        # ⚠️ NOTE: On utilise user_data pour renvoyer la ligne mise à jour au menu
        save_user_seances(user_data['id_user'], user_seances)
        
        # Mettre à jour l'affichage
        refresh_listbox()
        # Mettre à jour les données utilisateur globales (pour que 'nbentrainementsemaine' soit correct)
        user_data['nbentrainementsemaine'] = str(len(user_seances))


    def add_seance():
        """Ouvre une pop-up pour ajouter un entraînement."""
        
        popup = tk.Toplevel(root_window)
        popup.title("Ajouter une séance")
        popup.geometry("400x200")
        popup.transient(root_window)
        popup.grab_set()

        tk.Label(popup, text="Choisir un entraînement à ajouter :").pack(pady=10)
        
        # 2. Créer la Combobox avec tous les entraînements
        combo_var = tk.StringVar()
        
        # Formatter les options pour la Combobox
        # (Texte affiché, ID de l'entraînement)
        workout_options = []
        for w_id, w_details in ALL_WORKOUTS.items():
            display = f"{w_details['nom_d_Entrainement']} ({w_details['programme_entrainement']})"
            workout_options.append((display, w_id))
            
        combo = ttk.Combobox(
            popup, 
            textvariable=combo_var, 
            values=[opt[0] for opt in workout_options], # Affiche seulement le texte
            state="readonly", width=50
        )
        combo.pack(pady=10, padx=10)
        
        def confirm_add():
            selected_text = combo.get()
            if not selected_text:
                messagebox.showwarning("Erreur", "Veuillez choisir un entraînement.", parent=popup)
                return
            
            # Retrouver l'ID basé sur le texte sélectionné
            selected_id = None
            for opt in workout_options:
                if opt[0] == selected_text:
                    selected_id = opt[1]
                    break
            
            if not selected_id:
                messagebox.showerror("Erreur", "Sélection invalide.", parent=popup)
                return

            # 3. Ajout de la nouvelle séance
            new_seance = {
                'id_seance_user': str(get_next_seance_user_id()),
                'user_id': user_data['id_user'],
                'id_entrainement': selected_id
            }
            user_seances.append(new_seance)
            
            # 4. Sauvegarde
            save_user_seances(user_data['id_user'], user_seances)
            
            # 5. Mises à jour
            refresh_listbox()
            user_data['nbentrainementsemaine'] = str(len(user_seances))
            popup.destroy()

        tk.Button(popup, text="Ajouter", command=confirm_add).pack(pady=20)


    # --- Layout de l'interface ---
    
    tk.Label(root_window, text="Gestionnaire de Séances", font=("Arial", 16, "bold")).pack(pady=10)
    
    # Affichage du statut
    tk.Label(root_window, 
             text=f"Objectif : {user_data.get('objectif', 'Non défini')} | Séances actuelles : {len(user_seances)}", 
             font=("Arial", 11)).pack()

    # Frame pour la liste et le scroll
    frame_list = tk.Frame(root_window)
    frame_list.pack(fill="both", expand=True, padx=20, pady=10)
    
    scrollbar = tk.Scrollbar(frame_list, orient="vertical")
    listbox_seances = tk.Listbox(frame_list, yscrollcommand=scrollbar.set, height=15, font=("Arial", 11))
    scrollbar.config(command=listbox_seances.yview)
    
    scrollbar.pack(side="right", fill="y")
    listbox_seances.pack(side="left", fill="both", expand=True)
    
    refresh_listbox()

    # Frame pour les boutons d'action
    frame_actions = tk.Frame(root_window)
    frame_actions.pack(fill="x", padx=20, pady=5)

    tk.Button(
        frame_actions, text="➕ Ajouter Séance", 
        command=add_seance, 
        bg="#2ECC71", fg="white", font=("Arial", 10, "bold")
    ).pack(side="left", fill="x", expand=True, padx=5)
    
    tk.Button(
        frame_actions, text="➖ Supprimer Séance", 
        command=delete_seance, 
        bg="#E74C3C", fg="white", font=("Arial", 10, "bold")
    ).pack(side="left", fill="x", expand=True, padx=5)

    # Bouton Retour
    tk.Button(
        root_window, text="⬅️ Retour Menu Principal", 
        command=lambda: switch_back_callback(user_data) # Renvoie les données (potentiellement mises à jour)
    ).pack(pady=15)


# --- Test local ---
if __name__ == '__main__':
    def dummy_menu_callback(data_recue):
        print(f"Retour au Menu! Données: {data_recue}")
        sys.exit()

    root = tk.Tk()
    dummy_data = {'id_user': '1', 'pseudo': 'TestUser', 'nbentrainementsemaine': '3', 'objectif': 'Force'}
    run_seances_editor_screen(root, dummy_menu_callback, dummy_data)
    root.mainloop()