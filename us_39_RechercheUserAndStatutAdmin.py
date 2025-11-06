# filepath: c:\Users\irahmani\Documents\GitHub\BasicFrite\us_39_RechercheUserAndStatutAdmin.py
# User story 39 :
# en tant qu'admin je veux pouvoir gérer les user (chercher, bloquer, supprimé)
# afin de montrer la qualité de la plateforme

import os
import json
import tkinter as tk
from tkinter import messagebox
import csv

# Simple JSON-backed storage (file in the project folder)
DATA_FILE = os.path.join(os.path.dirname(__file__), "users_data.json")

# Sample users to initialize the file if it does not exist
SAMPLE_USERS = [
    {"username": "alice", "email": "alice@example.com", "status": "active"},
    {"username": "bob", "email": "bob@example.com", "status": "blocked"},
    {"username": "charlie", "email": "charlie@example.com", "status": "active"},
]

CSV_FILE = os.path.join(os.path.dirname(__file__), "User.csv")
CSV_FIELDS = [
    "id_user", "pseudo", "nom", "prénom", "age", "poids", "taille", "motdepasse", "email", "is_admin", "statut"
]

def load_users_csv():
    users = []
    try:
        with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                users.append(row)
        return users
    except UnicodeDecodeError:
        # Fallback for Windows/Excel CSV with accents
        with open(CSV_FILE, newline='', encoding='latin-1') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                users.append(row)
        return users

def save_users_csv(users):
    try:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, delimiter=';')
            writer.writeheader()
            for u in users:
                writer.writerow(u)
    except Exception:
        # Fallback
        with open(CSV_FILE, 'w', newline='', encoding='latin-1') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, delimiter=';')
            writer.writeheader()
            for u in users:
                writer.writerow(u)

def load_users():
    if not os.path.exists(DATA_FILE):
        save_users(SAMPLE_USERS)
        return list(SAMPLE_USERS)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # If file corrupted, reinit
        save_users(SAMPLE_USERS)
        return list(SAMPLE_USERS)


def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


# --- UI ---

def run_user_management(root_window, switch_back_callback):
    """Affiche l'écran d'administration des utilisateurs.
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

    tk.Label(top_frame, text="Recherche utilisateur (username ou email) :").pack(side="left")
    entry_search = tk.Entry(top_frame, width=30)
    entry_search.pack(side="left", padx=(8, 6))

    def refresh_list(filtered=None):
        listbox_users.delete(0, 'end')
        for u in (filtered if filtered is not None else users):
            listbox_users.insert('end', f"{u['pseudo']}  —  {u['email']}  [statut: {u['statut'] or 'actif'}]")

    def do_search():
        q = entry_search.get().strip().lower()
        if not q:
            refresh_list()
            return
        filtered = [u for u in users if q in (u['pseudo'] or '').lower() or q in (u['email'] or '').lower()]
        refresh_list(filtered)

    tk.Button(top_frame, text="🔎 Chercher", command=do_search).pack(side="left", padx=(0, 6))
    tk.Button(top_frame, text="↺ Réinitialiser", command=lambda: (entry_search.delete(0, 'end'), refresh_list())).pack(side="left")

    # centre: listbox and details
    center = tk.Frame(root_window)
    center.pack(fill="both", expand=True, padx=12, pady=6)

    listbox_users = tk.Listbox(center, width=60, height=15)
    listbox_users.pack(side="left", fill="y")

    details_frame = tk.Frame(center)
    details_frame.pack(side="left", fill="both", expand=True, padx=(12,0))

    lbl_details = tk.Label(details_frame, text="Sélectionnez un utilisateur pour voir les détails.", justify="left")
    lbl_details.pack(anchor="nw")

    # action buttons
    def get_selected_index():
        sel = listbox_users.curselection()
        if not sel:
            return None
        return sel[0]

    def get_user_by_list_index(idx):
        # listbox may be filtered, reconstruct username from listbox text
        text = listbox_users.get(idx)
        pseudo = text.split()[0]
        for u in users:
            if u['pseudo'] == pseudo:
                return u
        return None

    def on_select(event=None):
        idx = get_selected_index()
        if idx is None:
            lbl_details.config(text="Sélectionnez un utilisateur pour voir les détails.")
            return
        u = get_user_by_list_index(idx)
        if not u:
            lbl_details.config(text="Utilisateur introuvable.")
            return
        lbl_details.config(text=f"Pseudo: {u['pseudo']}\nNom: {u['nom']}\nPrénom: {u['prénom']}\nEmail: {u['email']}\nStatut: {u['statut'] or 'actif'}\nAdmin: {u['is_admin']}")

    listbox_users.bind('<<ListboxSelect>>', on_select)

    # actions
    def toggle_block():
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
                u['statut'] = ''
        else:
            if messagebox.askyesno("Bloquer", f"Bloquer {u['pseudo']} ?"):
                u['statut'] = 'bloqué'
        save_users_csv(users)
        refresh_list()
        on_select()

    def delete_user():
        idx = get_selected_index()
        if idx is None:
            messagebox.showwarning("Aucun utilisateur", "Veuillez sélectionner un utilisateur.")
            return
        u = get_user_by_list_index(idx)
        if not u:
            messagebox.showerror("Erreur", "Utilisateur introuvable.")
            return
        if messagebox.askyesno("Supprimer", f"Supprimer définitivement {u['pseudo']} ?"):
            users.remove(u)
            save_users_csv(users)
            refresh_list()
            lbl_details.config(text="Utilisateur supprimé.")

    btn_frame = tk.Frame(root_window)
    btn_frame.pack(fill="x", padx=12, pady=(6,12))

    tk.Button(btn_frame, text="🔓/🔒 Bloquer / Débloquer", command=toggle_block, width=20).pack(side="left", padx=6)
    tk.Button(btn_frame, text="🗑️ Supprimer", command=delete_user, width=12, bg="#D35400", fg="white").pack(side="left", padx=6)
    tk.Button(btn_frame, text="⬅️ Retour Admin", command=switch_back_callback).pack(side="right")

    # initial fill
    refresh_list()


if __name__ == '__main__':
    # test rapide
    root = tk.Tk()
    run_user_management(root, lambda: root.destroy())
    root.mainloop()

