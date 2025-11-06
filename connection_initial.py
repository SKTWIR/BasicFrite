# Fichier : registration_screen.py

import tkinter as tk
from tkinter import messagebox
import sys

# Définitions de style (pour la cohérence)
BG_COLOR = "#f4f4f4"
BTN_PRIMARY = "#1E90FF"
BTN_PRIMARY_ACTIVE = "#187bcd"

def run_registration_screen(parent_window):
    """Ouvre une nouvelle fenêtre Toplevel pour l'inscription."""
    
    # ------------------ JANELA D'INSCRIPTION ------------------
    reg = tk.Toplevel(parent_window)
    reg.title("Inscription")
    reg.geometry("600x480") 
    reg.resizable(False, False)
    reg.configure(bg=BG_COLOR)

    # ---- Container avec Canvas + Scrollbar pour permettre rolagem ----
    container = tk.Frame(reg, bg=BG_COLOR)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg=BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Frame interne rolável
    frame_reg = tk.Frame(canvas, bg=BG_COLOR)
    canvas.create_window((0, 0), window=frame_reg, anchor="nw")

    # Atualiza a região de scroll
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_reg.bind("<Configure>", on_frame_configure)

    # (Opcional) roler avec la rodinha du mouse
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # NOTE: bind_all peut être trop invasif, nous le laissons sur frame_reg
    frame_reg.bind("<MouseWheel>", _on_mousewheel) 
    
    # --- Rendre la pop-up modale et bloquer la fenêtre parente ---
    reg.grab_set()
    parent_window.wait_window(reg) 

    # ------------------ CAMPOS DE CRÉATION DE COMPTE ------------------

    lbl_reg_title = tk.Label(frame_reg, text="Créer un compte", font=("Segoe UI", 16, "bold"), bg=BG_COLOR)
    lbl_reg_title.pack(pady=(20, 20))

    # Champs (Nom, Prénom, Username, Age, Poids, Taille, MDP)
    fields = [
        ("Nom :", "entry_nom"), ("Prénom :", "entry_prenom"), ("Nom d'utilisateur :", "entry_username"),
        ("Âge :", "entry_age"), ("Poids (kg) :", "entry_poids"), ("Taille (m) :", "entry_taille"),
        ("Mot de passe :", "entry_reg_mdp", True) # True pour show="*"
    ]
    
    # Dictionnaire pour stocker les références d'Entry
    entries = {}

    for i, (label_text, entry_name, *show_star) in enumerate(fields):
        lbl = tk.Label(frame_reg, text=label_text, bg=BG_COLOR, font=("Segoe UI", 12))
        lbl.pack(anchor="w", padx=40)
        
        entry = tk.Entry(frame_reg, font=("Segoe UI", 11), show="*" if show_star else "")
        entry.pack(fill="x", padx=40, pady=(0, 8))
        entries[entry_name] = entry

    # Função do botão "Créer le compte"
    def on_create_account():
        # Récupération des données
        nom = entries['entry_nom'].get()
        prenom = entries['entry_prenom'].get()
        # [ ... logique de validation à implémenter ici ... ]
        
        print(f"Création de compte initiée pour {prenom} {nom}. (logique à implémenter)")
        
        # Exemple de succès simulé:
        if nom and prenom and entries['entry_reg_mdp'].get():
             messagebox.showinfo("Succès", "Compte créé! Veuillez vous connecter.")
             reg.destroy() # Ferme l'inscription

    # Botão "Créer le compte" 
    btn_create = tk.Button(
        frame_reg, text="Créer le compte", command=on_create_account,
        font=("Segoe UI", 13, "bold"), bg=BTN_PRIMARY, fg="white", 
        activebackground=BTN_PRIMARY_ACTIVE, activeforeground="white", 
        relief="flat", height=2
    )
    btn_create.pack(fill="x", padx=40, pady=(10, 30))

    entries['entry_nom'].focus_set()