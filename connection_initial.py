# Fichier : connection_initial.py (Contient Connexion, Inscription, et lien vers Récupération/Support)

import tkinter as tk
from tkinter import messagebox
import sys
import us_2 # Module de récupération de mot de passe
import support_contact # Module de support

# Définitions de style (TEXT_COLOR corrigé)
BG_COLOR = "#f4f4f4"
BTN_PRIMARY = "#1E90FF"
BTN_PRIMARY_ACTIVE = "#187bcd"
TEXT_COLOR = "#17202A" # <-- Correction de la variable manquante
LINK_FG = "#2980B9"

def run_connection_initial(root_window, switch_to_menu_callback):
    """
    Lance l'interface de connexion et d'inscription dans la fenêtre root_window.
    """
    
    # ------------------ PRÉPARATION DE LA FENÊTRE ------------------
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

    # Fonction "Mot de passe oublié ?" (MODIFIÉE pour lancer us_2)
    def on_forgot():
        """Lance l'écran de récupération de mot de passe (us_2.py)."""
        us_2.run_password_recovery(root_window, lambda: run_connection_initial(root_window, switch_to_menu_callback))

    btn_forgot = tk.Button(frame, text="Mot de passe oublié ?", bd=0, fg=BTN_PRIMARY, bg=BG_COLOR, 
                           cursor="hand2", font=("Segoe UI", 10, "underline"), activebackground=BG_COLOR,
                           activeforeground=BTN_PRIMARY, command=on_forgot)
    btn_forgot.pack(anchor="e", pady=(0, 20))

    # Fonction du bouton "Se connecter"
    def on_connect():
        identifiant = entry_identifiant.get()
        mdp = entry_mdp.get()
        print(f"Tentative de connexion : {identifiant} / {mdp} (logique à implémenter)")
        
        # Logique de succès simplifiée
        if identifiant and mdp:
             messagebox.showinfo("Connexion Réussie", f"Bienvenue, {identifiant}!")
             switch_to_menu_callback()
        else:
             messagebox.showerror("Erreur", "Veuillez entrer vos identifiants.")

    # Botão grande "Se connecter"
    btn_connect = tk.Button(frame, text="Se connecter", command=on_connect,
                            font=("Segoe UI", 13, "bold"), bg=BTN_PRIMARY, fg="white", 
                            activebackground=BTN_PRIMARY_ACTIVE, activeforeground="white", 
                            relief="flat", height=2)
    btn_connect.pack(fill="x", pady=(0, 12))
    
    # ------------------ LIEN CONTACER LE SUPPORT ------------------
    support_button = tk.Button(
        frame,
        text="Contacter le support",
        command=lambda: support_contact.open_support_popup(root_window),
        font=("Segoe UI", 10, "underline"),
        fg=LINK_FG,
        bg=BG_COLOR,
        relief="flat",
        borderwidth=0,
        cursor="hand2",
        activeforeground=TEXT_COLOR, # <-- Utilisation de TEXT_COLOR (maintenant défini)
        activebackground=BG_COLOR
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
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        frame_reg.bind("<Configure>", on_frame_configure)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        frame_reg.bind("<MouseWheel>", _on_mousewheel) 
        canvas.bind_all("<MouseWheel>", _on_mousewheel) 
        
        # ------------------ CAMPOS DE CRÉATION DE COMPTE ------------------
        lbl_reg_title = tk.Label(frame_reg, text="Créer un compte", font=("Segoe UI", 16, "bold"), bg=BG_COLOR)
        lbl_reg_title.pack(pady=(20, 20))

        # Définition des champs et des variables d'entrée
        fields_data = [
            ("Nom :", False), ("Prénom :", False), ("Nom d'utilisateur :", False), 
            ("Adresse Email :", False), # <-- Email inclus ici
            ("Âge :", False), ("Poids (kg) :", False), ("Taille (m) :", False), 
            ("Mot de passe :", True)
        ]
        entries = {}
        for text, is_password in fields_data:
            lbl = tk.Label(frame_reg, text=text, bg=BG_COLOR, font=("Segoe UI", 12))
            lbl.pack(anchor="w", padx=40)
            entry = tk.Entry(frame_reg, font=("Segoe UI", 11), show="*" if is_password else "")
            entry.pack(fill="x", padx=40, pady=(0, 8 if not is_password else 15))
            entries[text] = entry 


        # Fonction du bouton "Créer le compte"
        def on_create_account():
            # Récupération simplifiée
            nom = entries["Nom :"].get()
            email = entries["Adresse Email :"].get()
            mdp = entries["Mot de passe :"].get()
            
            if nom and mdp and email:
                 messagebox.showinfo("Succès", "Compte créé! Veuillez vous connecter.")
                 reg.destroy()

        btn_create = tk.Button(frame_reg, text="Créer le compte", command=on_create_account,
                                font=("Segoe UI", 13, "bold"), bg=BTN_PRIMARY, fg="white", 
                                activebackground=BTN_PRIMARY_ACTIVE, activeforeground="white", 
                                relief="flat", height=2)
        btn_create.pack(fill="x", padx=40, pady=(10, 30))

        entries["Nom :"].focus_set()
        
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
    def dummy_menu_callback():
        print("Switch to Menu!")
        sys.exit()

    root = tk.Tk()
    run_connection_initial(root, dummy_menu_callback)
    root.mainloop()