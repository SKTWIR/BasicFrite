# Fichier : connection_initial.py (Contient Connexion et Inscription)

import tkinter as tk
from tkinter import messagebox
import sys

# Définitions de style
BG_COLOR = "#f4f4f4"
BTN_PRIMARY = "#1E90FF"
BTN_PRIMARY_ACTIVE = "#187bcd"

def run_connection_initial(root_window, switch_to_menu_callback):
    """
    Lance l'interface de connexion et d'inscription dans la fenêtre root_window.
    """
    
    # ------------------ PRÉPARATION DE LA FENÊTRE ------------------
    # Nettoyer l'écran précédent
    for widget in root_window.winfo_children():
        widget.destroy()

    root_window.title("Connexion")
    root_window.geometry("600x480") 
    root_window.resizable(False, False)
    root_window.configure(bg=BG_COLOR)

    # Frame principal
    frame = tk.Frame(root_window, bg=BG_COLOR)
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    # Título
    lbl_title = tk.Label(frame, text="🏋️ Connexion à votre espace", font=("Segoe UI", 16, "bold"), bg=BG_COLOR)
    lbl_title.pack(pady=(0, 25))

    # Identifiant
    lbl_identifiant = tk.Label(frame, text="Identifiant :", bg=BG_COLOR, font=("Segoe UI", 12))
    lbl_identifiant.pack(anchor="w")
    entry_identifiant = tk.Entry(frame, font=("Segoe UI", 11))
    entry_identifiant.pack(fill="x", pady=(0, 15))

    # Mot de passe
    lbl_mdp = tk.Label(frame, text="Mot de passe :", bg=BG_COLOR, font=("Segoe UI", 12))
    lbl_mdp.pack(anchor="w")
    entry_mdp = tk.Entry(frame, show="*", font=("Segoe UI", 11))
    entry_mdp.pack(fill="x", pady=(0, 15))

    # Fonction "Mot de passe oublié ?"
    def on_forgot():
        print("Mot de passe oublié ? (fonctionnalité à implémenter)")

    btn_forgot = tk.Button(frame, text="Mot de passe oublié ?", bd=0, fg=BTN_PRIMARY, bg=BG_COLOR, 
                           cursor="hand2", font=("Segoe UI", 10, "underline"), activebackground=BG_COLOR,
                           activeforeground=BTN_PRIMARY, command=on_forgot)
    btn_forgot.pack(anchor="e", pady=(0, 20))

    # Fonction du bouton "Se connecter" (MODIFIÉ pour appeler le callback du menu)
    def on_connect():
        identifiant = entry_identifiant.get()
        mdp = entry_mdp.get()
        print(f"Tentative de connexion : {identifiant} / {mdp} (logique à implémenter)")
        
        # Logique de succès simplifiée
        if identifiant and mdp:
             messagebox.showinfo("Connexion Réussie", f"Bienvenue, {identifiant}!")
             switch_to_menu_callback() # <-- BASCULE VERS LE MENU
        else:
             messagebox.showerror("Erreur", "Veuillez entrer vos identifiants.")

    # Botão grande "Se connecter"
    btn_connect = tk.Button(frame, text="Se connecter", command=on_connect,
                            font=("Segoe UI", 13, "bold"), bg=BTN_PRIMARY, fg="white", 
                            activebackground=BTN_PRIMARY_ACTIVE, activeforeground="white", 
                            relief="flat", height=2)
    btn_connect.pack(fill="x", pady=(0, 12))

    # ------------------ INSCRIPTION (M'INSCRIRE) ------------------

    def open_inscription_window():
        """Ouvre une nouvelle fenêtre pour créer un compte (Toplevel)."""
        reg = tk.Toplevel(root_window)
        reg.title("Inscription")
        reg.geometry("600x480") 
        reg.resizable(False, False)
        reg.configure(bg=BG_COLOR)
        
        # NOTE: Le reste de la logique d'inscription (Canvas, Frame, Champs...)
        # est un peu long, mais fonctionne comme un écran secondaire modal.
        # J'omets les détails des champs pour ne pas surcharger, 
        # mais la structure est conservée.

        # ---- Conteneur de défilement (Canvas + Scrollbar) ----
        container = tk.Frame(reg, bg=BG_COLOR)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        frame_reg = tk.Frame(canvas, bg=BG_COLOR)
        canvas.create_window((0, 0), window=frame_reg, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_reg.bind("<Configure>", on_frame_configure)

        def on_create_account():
            # Logique simplifiée
            messagebox.showinfo("Inscription", "Compte créé! Veuillez vous connecter.")
            reg.destroy()

        # Placeholders pour les champs (pour éviter les erreurs de variables)
        tk.Label(frame_reg, text="Créer un compte", font=("Segoe UI", 16, "bold"), bg=BG_COLOR).pack(pady=(20, 20))
        
        # NOTE: Les champs d'Entry et de Label seraient ajoutés ici dans frame_reg
        tk.Label(frame_reg, text="[Champs d'Inscription...]", bg=BG_COLOR).pack(pady=10)
        tk.Entry(frame_reg, font=("Segoe UI", 11)).pack(fill="x", padx=40, pady=5) # Exemple d'Entry
        
        # Botão "Créer le compte"
        btn_create = tk.Button(frame_reg, text="Créer le compte", command=on_create_account,
                                font=("Segoe UI", 13, "bold"), bg=BTN_PRIMARY, fg="white", 
                                activebackground=BTN_PRIMARY_ACTIVE, activeforeground="white", 
                                relief="flat", height=2)
        btn_create.pack(fill="x", padx=40, pady=(10, 30))
        
        # Rendre modale
        reg.grab_set()
        root_window.wait_window(reg)


    # Botão "M'inscrire"
    btn_inscrire = tk.Button(frame, text="M'inscrire", command=open_inscription_window,
                             font=("Segoe UI", 11, "bold"), bg="#ffffff", fg=BTN_PRIMARY, 
                             activebackground="#e6e6e6", activeforeground=BTN_PRIMARY, 
                             relief="groove", height=1)
    btn_inscrire.pack(pady=(0, 5))

    entry_identifiant.focus_set()


# Si le fichier est exécuté seul (pour test)
if __name__ == "__main__":
    def dummy_menu_callback():
        print("Switch to Menu!")
        sys.exit()

    root = tk.Tk()
    run_connection_initial(root, dummy_menu_callback)
    root.mainloop()