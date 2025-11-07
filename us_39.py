# Fichier : us_39.py
# Gestion des utilisateurs (Recherche, Bloquer, Supprimer)

import os
import tkinter as tk
from tkinter import messagebox
import csv
import sys

# --- CONSTANTES ---
CSV_FILE = os.path.join(os.path.dirname(__file__), "User.csv")
CSV_FIELDS = [
    "id_user", "pseudo", "nom", "prénom", "age", "poids", "taille", "motdepasse", "email", "is_admin", "statut"
]

# --- FONCTIONS CSV ---

def load_users_csv():
    """Charge tous les utilisateurs depuis le User.csv."""
    users = []
    if not os.path.exists(CSV_FILE):
        messagebox.showerror("Erreur Fichier", "Fichier User.csv introuvable.")
        return []
        
    try:
        # Essai en UTF-8 (standard)
        with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                users.append(row)
        return users
    except UnicodeDecodeError:
        # Fallback pour encodage Windows (avec accents)
        try:
            with open(CSV_FILE, newline='', encoding='latin-1') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    users.append(row)
            return users
        except Exception as e:
            messagebox.showerror("Erreur Encodage", f"Impossible de lire le CSV (latin-1): {e}")
            return []
    except Exception as e:
        messagebox.showerror("Erreur Lecture CSV", f"Erreur: {e}")
        return []


def save_users_csv(users):
    """Réécrit l'intégralité du fichier User.csv avec la liste (potentiellement modifiée)."""
    try:
        # Tente d'écrire en UTF-8
        with open(CSV_FILE, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, delimiter=';')
            writer.writeheader()
            for u in users:
                writer.writerow(u)
    except Exception:
        try:
            # Fallback en latin-1
            with open(CSV_FILE, 'w', newline='', encoding='latin-1') as f:
                writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, delimiter=';')
                writer.writeheader()
                for u in users:
                    writer.writerow(u)
        except Exception as e:
            messagebox.showerror("Erreur Écriture", f"Impossible de sauvegarder le CSV: {e}")


# --- INTERFACE ---

def run_user_management(root_window, switch_back_callback):
    """
    Affiche l'écran d'administration des utilisateurs.
    switch_back_callback doit ramener vers le menu administrateur.
    """
    # Nettoyage
    for w in root_window.winfo_children():
        w.destroy()

    root_window.title("🔒 Gestion des utilisateurs")
    root_window.geometry("650x450")
    root_window.resizable(False, False)

    users = load_users_csv()

    # --- Layout ---
    top_frame = tk.Frame(root_window)
    top_frame.pack(fill="x", padx=12, pady=(12, 6))

    tk.Label(top_frame, text="Recherche (pseudo ou email) :").pack(side="left")
    entry_search = tk.Entry(top_frame, width=30)
    entry_search.pack(side="left", padx=(8, 6))

    def refresh_list(filtered=None):
        """Met à jour la Listbox avec la liste fournie (ou la liste complète)."""
        listbox_users.delete(0, 'end')
        
        # S'assurer que la liste n'est pas vide
        current_list = filtered if filtered is not None else users
        
        for u in current_list:
            # Assurer que le statut 'actif' est affiché s'il est vide
            statut_display = u.get('statut') if u.get('statut') else 'actif'
            listbox_users.insert('end', f"{u['pseudo']}  —  {u['email']}  [statut: {statut_display}]")

    def do_search():
        """Filtre la liste basée sur la recherche."""
        q = entry_search.get().strip().lower()
        if not q:
            refresh_list()
            return
        # Recherche dans le pseudo OU l'email
        filtered = [u for u in users if q in (u['pseudo'] or '').lower() or q in (u['email'] or '').lower()]
        refresh_list(filtered)

    tk.Button(top_frame, text="🔎 Chercher", command=do_search).pack(side="left", padx=(0, 6))
    tk.Button(top_frame, text="↺ Réinitialiser", command=lambda: (entry_search.delete(0, 'end'), refresh_list())).pack(side="left")

    # Centre: listbox et détails
    center = tk.Frame(root_window)
    center.pack(fill="both", expand=True, padx=12, pady=6)

    listbox_users = tk.Listbox(center, width=60, height=15)
    listbox_users.pack(side="left", fill="y")

    details_frame = tk.Frame(center)
    details_frame.pack(side="left", fill="both", expand=True, padx=(12,0))

    lbl_details = tk.Label(details_frame, text="Sélectionnez un utilisateur pour voir les détails.", justify="left")
    lbl_details.pack(anchor="nw")

    # Fonctions d'action
    def get_selected_index():
        sel = listbox_users.curselection()
        if not sel:
            return None
        return sel[0]

    def get_user_by_list_index(idx):
        """Retrouve l'utilisateur dans la liste 'users' basé sur le pseudo de la listbox."""
        try:
            text = listbox_users.get(idx)
            pseudo = text.split()[0]
            for u in users:
                if u['pseudo'] == pseudo:
                    return u
            return None
        except IndexError:
            return None

    def on_select(event=None):
        """Affiche les détails de l'utilisateur sélectionné."""
        idx = get_selected_index()
        if idx is None:
            lbl_details.config(text="Sélectionnez un utilisateur pour voir les détails.")
            return
        u = get_user_by_list_index(idx)
        if not u:
            lbl_details.config(text="Utilisateur introuvable.")
            return
        
        # Affichage propre des détails
        details_text = (
            f"Pseudo: {u['pseudo']}\n"
            f"Nom: {u.get('nom', 'N/A')}\n"
            f"Prénom: {u.get('prénom', 'N/A')}\n"
            f"Email: {u.get('email', 'N/A')}\n"
            f"Statut: {u.get('statut') or 'actif'}\n"
            f"Admin: {u.get('is_admin', 'False')}"
        )
        lbl_details.config(text=details_text)

    listbox_users.bind('<<ListboxSelect>>', on_select)

    # Actions (Bloquer/Supprimer)
    def toggle_block():
        """Bascule le statut d'un utilisateur entre 'bloqué' et '' (actif)."""
        idx = get_selected_index()
        if idx is None:
            messagebox.showwarning("Aucun utilisateur", "Veuillez sélectionner un utilisateur.")
            return
        u = get_user_by_list_index(idx)
        if not u:
            messagebox.showerror("Erreur", "Utilisateur introuvable.")
            return

        if (u['statut'] or '').lower() == 'bloqué':
            if messagebox.askyesno("Débloquer", f"Débloquer {u['pseudo']} ?"):
                u['statut'] = '' # Statut actif (vide)
        else:
            if messagebox.askyesno("Bloquer", f"Bloquer {u['pseudo']} ?"):
                u['statut'] = 'bloqué'
        
        save_users_csv(users)
        refresh_list()
        on_select() # Met à jour les détails affichés

    def delete_user():
        """Supprime l'utilisateur sélectionné du CSV."""
        idx = get_selected_index()
        if idx is None:
            messagebox.showwarning("Aucun utilisateur", "Veuillez sélectionner un utilisateur.")
            return
        u = get_user_by_list_index(idx)
        if not u:
            messagebox.showerror("Erreur", "Utilisateur introuvable.")
            return
        
        if u['is_admin'].lower() == 'true':
            messagebox.showerror("Action impossible", "Vous ne pouvez pas supprimer un administrateur.")
            return
            
        if messagebox.askyesno("Supprimer", f"Supprimer définitivement {u['pseudo']} ?"):
            users.remove(u)
            save_users_csv(users)
            refresh_list()
            lbl_details.config(text="Utilisateur supprimé.")

    # Cadre des boutons d'action
    btn_frame = tk.Frame(root_window)
    btn_frame.pack(fill="x", padx=12, pady=(6,12))

    tk.Button(btn_frame, text="🔓/🔒 Bloquer / Débloquer", command=toggle_block, width=20).pack(side="left", padx=6)
    tk.Button(btn_frame, text="🗑️ Supprimer", command=delete_user, width=12, bg="#D35400", fg="white").pack(side="left", padx=6)
    
    # Bouton de retour (utilise le callback fourni par main_menu.py)
    tk.Button(btn_frame, text="⬅️ Retour Admin", command=switch_back_callback).pack(side="right")

    # Remplissage initial de la liste
    refresh_list()


if __name__ == '__main__':
    # Test rapide
    root = tk.Tk()
    run_user_management(root, lambda: root.destroy())
    root.mainloop()