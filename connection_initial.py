# Fichier : connection_initial.py (Correction de l'encodage de lecture)

import tkinter as tk
from tkinter import messagebox
import sys
import os 
import csv 
import hashlib 

# Modules de l'application
import us_2 
import support_contact 

# --- CONSTANTES ---
BG_COLOR = "#f4f4f4"
BTN_PRIMARY = "#1E90FF"
BTN_PRIMARY_ACTIVE = "#187bcd"
TEXT_COLOR = "#17202A"
LINK_FG = "#2980B9"
USER_CSV_FILE = os.path.join(os.path.dirname(__file__), 'User.csv')
# --------------------

# --- FONCTIONS UTILITAIRES CSV ET SÉCURITÉ ---

def check_user(pseudo, password):
    """
    Vérifie le pseudo/mdp (en texte clair) et retourne la ligne.
    """
    if not os.path.exists(USER_CSV_FILE):
        messagebox.showerror("Erreur Fichier", "Fichier User.csv introuvable.")
        return None

    try:
        # --- CORRECTION ENCODAGE (Lecture) ---
        with open(USER_CSV_FILE, mode='r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                if row['pseudo'] == pseudo:
                    if row['motdepasse'] == password:
                        return row 
            return None
    except Exception as e:
        messagebox.showerror("Erreur de lecture", f"Erreur lors de la lecture du CSV (check_user): {e}")
        return None

def get_next_user_id():
    """Trouve le ID maximum dans le CSV et retourne ID+1."""
    max_id = 0
    if not os.path.exists(USER_CSV_FILE): return 1 
    try:
        # --- CORRECTION ENCODAGE (Lecture) ---
        with open(USER_CSV_FILE, mode='r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                try:
                    user_id = int(row['id_user'])
                    if user_id > max_id: max_id = user_id
                except (ValueError, TypeError): continue 
        return max_id + 1
    except Exception: return 1 

def does_user_exist(username, email):
    """Vérifie si le pseudo ou l'email existent déjà."""
    if not os.path.exists(USER_CSV_FILE): return False
    try:
        # --- CORRECTION ENCODAGE (Lecture) ---
        with open(USER_CSV_FILE, mode='r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                if row['pseudo'] == username or row['email'] == email:
                    return True
        return False
    except Exception: return False

# --- INTERFACE PRINCIPALE ---

def run_connection_initial(root_window, switch_to_menu_callback, switch_to_admin_callback):
    
    # ... (Le reste de la fonction est inchangé) ...
    
    # ------------------ PRÉPARATION DE LA FENÊTRE ------------------
    for widget in root_window.winfo_children():
        widget.destroy()

    root_window.title("Connexion")
    root_window.geometry("600x480") 
    root_window.resizable(False, False)
    root_window.configure(bg=BG_COLOR)

    frame = tk.Frame(root_window, bg=BG_COLOR)
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    lbl_title = tk.Label(frame, text="🏋️ Connexion à votre espace", font=("Segoe UI", 16, "bold"), bg=BG_COLOR)
    lbl_title.pack(pady=(0, 25))

    lbl_identifiant = tk.Label(frame, text="Identifiant (pseudo) :", bg=BG_COLOR, font=("Segoe UI", 12))
    lbl_identifiant.pack(anchor="w")
    entry_identifiant = tk.Entry(frame, font=("Segoe UI", 11))
    entry_identifiant.pack(fill="x", pady=(0, 15))

    lbl_mdp = tk.Label(frame, text="Mot de passe :", bg=BG_COLOR, font=("Segoe UI", 12))
    lbl_mdp.pack(anchor="w")
    entry_mdp = tk.Entry(frame, show="*", font=("Segoe UI", 11))
    entry_mdp.pack(fill="x", pady=(0, 15))

    def on_forgot():
        us_2.run_password_recovery(root_window, lambda: run_connection_initial(root_window, switch_to_menu_callback, switch_to_admin_callback))

    btn_forgot = tk.Button(frame, text="Mot de passe oublié ?", bd=0, fg=BTN_PRIMARY, bg=BG_COLOR, 
                           cursor="hand2", font=("Segoe UI", 10, "underline"), activebackground=BG_COLOR,
                           activeforeground=BTN_PRIMARY, command=on_forgot)
    btn_forgot.pack(anchor="e", pady=(0, 20))

    def on_connect():
        identifiant = entry_identifiant.get()
        mdp = entry_mdp.get()
        if not identifiant or not mdp:
            messagebox.showerror("Erreur", "Veuillez entrer un identifiant et un mot de passe.")
            return

        user_data = check_user(identifiant, mdp)
        
        if user_data: 
            statut = user_data.get('statut', '').strip().lower()
            
            if statut == 'bloqué':
                messagebox.showerror(
                    "Compte Bloqué", 
                    "Votre compte a été bloqué par un administrateur.\n\nVeuillez contacter le support pour plus d'informations."
                )
                return 
            
            messagebox.showinfo("Connexion Réussie", f"Bienvenue, {user_data['pseudo']}!")
            
            if user_data['is_admin'].lower() == 'true':
                 switch_to_admin_callback(user_data)
            else:
                 switch_to_menu_callback(user_data)
        else:
             messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect.")

    btn_connect = tk.Button(frame, text="Se connecter", command=on_connect,
                            font=("Segoe UI", 13, "bold"), bg=BTN_PRIMARY, fg="white", 
                            activebackground=BTN_PRIMARY_ACTIVE, activeforeground="white", 
                            relief="flat", height=2)
    btn_connect.pack(fill="x", pady=(0, 12))
    
    support_button = tk.Button(
        frame, text="Contacter le support",
        command=lambda: support_contact.open_support_popup(root_window),
        font=("Segoe UI", 10, "underline"), fg=LINK_FG, bg=BG_COLOR,
        relief="flat", borderwidth=0, cursor="hand2",
        activeforeground=TEXT_COLOR, activebackground=BG_COLOR
    )
    support_button.pack(anchor="center", pady=(5, 5))
    
    # ------------------ INSCRIPTION (open_inscription_window) ------------------
    
    def open_inscription_window():
        """Ouvre une nouvelle fenêtre pour créer un compte (Toplevel)."""
        reg = tk.Toplevel(root_window) 
        reg.title("Inscription")
        reg.geometry("600x480")
        reg.resizable(False, False)
        reg.configure(bg=BG_COLOR)

        # ---- Container avec Canvas + Scrollbar ----
        container = tk.Frame(reg, bg=BG_COLOR)
        container.pack(fill="both", expand=True)
        canvas = tk.Canvas(container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        frame_reg = tk.Frame(canvas, bg=BG_COLOR)
        canvas.create_window((0, 0), window=frame_reg, anchor="nw")
        
        def on_frame_configure(event): canvas.configure(scrollregion=canvas.bbox("all"))
        frame_reg.bind("<Configure>", on_frame_configure)
        def _on_mousewheel(event): canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        frame_reg.bind("<MouseWheel>", _on_mousewheel) 
        canvas.bind_all("<MouseWheel>", _on_mousewheel) 
        
        # ------------------ CAMPOS DE CRÉATION DE COMPTE ------------------
        lbl_reg_title = tk.Label(frame_reg, text="Créer un compte", font=("Segoe UI", 16, "bold"), bg=BG_COLOR)
        lbl_reg_title.pack(pady=(20, 20))

        fields_data = [
            ("Nom :", "nom", False), ("Prénom :", "prenom", False), ("Nom d'utilisateur :", "username", False), 
            ("Adresse Email :", "email", False), 
            ("Âge :", "age", False), ("Poids (kg) :", "poids", False), ("Taille (m) :", "taille", False), 
            ("Mot de passe :", "mdp", True)
        ]
        entries = {}
        for label_text, key, is_password in fields_data:
            lbl = tk.Label(frame_reg, text=label_text, bg=BG_COLOR, font=("Segoe UI", 12))
            lbl.pack(anchor="w", padx=40)
            entry = tk.Entry(frame_reg, font=("Segoe UI", 11), show="*" if is_password else "")
            entry.pack(fill="x", padx=40, pady=(0, 8 if not is_password else 15))
            entries[key] = entry 
            
        def on_create_account():
            data = {key: entry.get() for key, entry in entries.items()}
            
            required_fields = ['nom', 'prenom', 'username', 'email', 'mdp']
            if not all(data[f] for f in required_fields):
                messagebox.showerror("Champs requis", "Nom, Prénom, Pseudo, Email et Mot de passe sont requis.", parent=reg)
                return
                
            if '@' not in data['email'] or '.' not in data['email']:
                 messagebox.showerror("Email invalide", "Veuillez entrer une adresse email valide.", parent=reg)
                 return
                 
            if does_user_exist(data['username'], data['email']):
                messagebox.showerror("Erreur", "Ce nom d'utilisateur ou cet email est déjà utilisé.", parent=reg)
                return

            try:
                new_id = get_next_user_id()
                
                new_row = [
                    new_id,
                    data['username'], data['nom'], data['prenom'], 
                    data['age'] if data['age'] else '', 
                    data['poids'] if data['poids'] else '',
                    data['taille'] if data['taille'] else '',
                    data['mdp'], 
                    data['email'], 
                    'False', '','4', 'Force'
                ]

                # --- CORRECTION ENCODAGE (Écriture) ---
                with open(USER_CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
                    csv_writer = csv.writer(f, delimiter=';')
                    csv_writer.writerow(new_row)
                    
                messagebox.showinfo("Succès", "Compte créé! Veuillez vous connecter.", parent=reg)
                reg.destroy()

            except Exception as e:
                messagebox.showerror("Erreur d'écriture", f"Impossible d'enregistrer le compte: {e}", parent=reg)

        btn_create = tk.Button(frame_reg, text="Créer le compte", command=on_create_account,
                                font=("Segoe UI", 13, "bold"), bg=BTN_PRIMARY, fg="white", 
                                activebackground=BTN_PRIMARY_ACTIVE, activeforeground="white", 
                                relief="flat", height=2)
        btn_create.pack(fill="x", padx=40, pady=(10, 30))
        entries["nom"].focus_set()
        reg.grab_set()
        root_window.wait_window(reg)


    # Botão "M'inscrire" (sous le lien support)
    btn_inscrire = tk.Button(frame, text="M'inscrire", command=open_inscription_window,
                             font=("Segoe UI", 11, "bold"), bg="#ffffff", fg=BTN_PRIMARY, 
                             activebackground="#e6e6e6", activeforeground=BTN_PRIMARY, 
                             relief="groove", height=1)
    btn_inscrire.pack(pady=(5, 5))

    entry_identifiant.focus_set()


if __name__ == "__main__":
    def dummy_menu_callback(user_data):
        print(f"Switch to Menu! Data: {user_data}")
        sys.exit()
    def dummy_admin_callback(user_data):
        print(f"Switch to Admin Menu! Data: {user_data}")
        sys.exit()

    root = tk.Tk()
    run_connection_initial(root, dummy_menu_callback, dummy_admin_callback)
    root.mainloop()