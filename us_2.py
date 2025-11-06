import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont

# --- CONSTANTES ---
HARDCODED_CODE = "frite" # Le code secret

# --- Définition du style (THÈME BLEU) ---
BG_COLOR = "#D6EAF8"       # Bleu clair
FRAME_BG = "#EBF5FB"       # Bleu très clair pour le cadre central
TEXT_COLOR = "#17202A"     # Noir/Bleu foncé
BUTTON_BG = "#3498DB"      # Bleu vif
BUTTON_FG = "#FFFFFF"      # Blanc
LINK_FG = "#2980B9"        # Bleu lien hypertexte
FONT_TITLE = ("Helvetica", 16, "bold")
FONT_LABEL = ("Helvetica", 11)
FONT_BUTTON = ("Helvetica", 11, "bold")
FONT_LINK = ("Helvetica", 10, "underline")

# --- FONCTIONS LOGIQUES ---

def show_frame(frame_to_show):
    """
    Fait passer le frame demandé au premier plan.
    C'est notre "changeur de page".
    """
    frame_to_show.tkraise()

def handle_send_code():
    """
    PAGE 1 : Valide l'email et passe à la page de VÉRIFICATION DU CODE.
    """
    email = entry_email.get()
    
    # Validation très simple
    if not email or "@" not in email or "." not in email:
        messagebox.showerror("Email invalide", "Veuillez entrer une adresse email valide.")
        return
        
    # Simulation de l'envoi de l'email
    messagebox.showinfo(
        "Code 'envoyé'",
        f"Un email de réinitialisation a été 'envoyé' à {email}."
    )
    
    # Vider le champ de code pour la prochaine étape
    entry_code.delete(0, 'end')
    
    # Changer de page -> vers la page du CODE
    show_frame(frame_code_verify)

def handle_verify_code():
    """
    PAGE 2 : Valide le code et passe à la page de RÉINITIALISATION DU MDP.
    """
    code = entry_code.get()
    
    if code != HARDCODED_CODE:
        messagebox.showerror("Code incorrect", "Le code de vérification est incorrect.")
        return
    
    # Code correct ! On passe à la suite.
    # Vider les champs de mot de passe pour la prochaine étape
    entry_new_pass.delete(0, 'end')
    entry_confirm_pass.delete(0, 'end')
    
    # Changer de page -> vers la page du NOUVEAU MDP
    show_frame(frame_new_password)

def handle_reset_password():
    """
    PAGE 3 : Valide les nouveaux mots de passe et termine le processus.
    """
    new_pass = entry_new_pass.get()
    confirm_pass = entry_confirm_pass.get()
    
    if not new_pass or len(new_pass) < 6:
        messagebox.showerror("Mot de passe faible", "Le mot de passe doit contenir au moins 6 caractères.")
        return
        
    if new_pass != confirm_pass:
        messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
        return
        
    # Tout est bon !
    messagebox.showinfo(
        "Succès",
        "Votre mot de passe a été réinitialisé avec succès !"
    )
    
    # Vider l'email de départ et retourner à la première page (connexion)
    entry_email.delete(0, 'end')
    show_frame(frame_email)


# --- CONFIGURATION DE LA FENÊTRE PRINCIPALE ---
root = tk.Tk()
root.title("Récupération de mot de passe")
root.geometry("450x400") # Taille de fenêtre fixe
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# --- CONTENEUR PRINCIPAL (pour empiler les "pages") ---
main_container = tk.Frame(root, bg=BG_COLOR)
main_container.pack(fill="both", expand=True, padx=20, pady=20)

main_container.grid_rowconfigure(0, weight=1)
main_container.grid_columnconfigure(0, weight=1)

# --- PAGE 1 : DEMANDE D'EMAIL ---
frame_email = tk.Frame(main_container, bg=FRAME_BG)
frame_email.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

title_email = tk.Label(frame_email, text="Mot de passe oublié ?", font=FONT_TITLE, bg=FRAME_BG, fg=TEXT_COLOR)
title_email.pack(pady=(20, 10))

desc_email = tk.Label(frame_email, text="Entrez votre email pour recevoir un code.", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
desc_email.pack(pady=10, padx=20)

label_email = tk.Label(frame_email, text="Adresse Email :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
label_email.pack(pady=(10, 5))

entry_email = tk.Entry(frame_email, width=40, font=FONT_LABEL, relief="flat")
entry_email.pack(pady=5, padx=30)

btn_send_code = tk.Button(
    frame_email,
    text="Envoyer le code",
    command=handle_send_code,
    font=FONT_BUTTON,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    relief="flat",
    borderwidth=0
)
btn_send_code.pack(pady=20, ipadx=10, ipady=5)


# --- PAGE 2 : VÉRIFICATION DU CODE ---
frame_code_verify = tk.Frame(main_container, bg=FRAME_BG)
frame_code_verify.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

title_code = tk.Label(frame_code_verify, text="Vérifiez vos emails", font=FONT_TITLE, bg=FRAME_BG, fg=TEXT_COLOR)
title_code.pack(pady=(20, 10))

desc_code = tk.Label(frame_code_verify, text="Entrez le code reçu par email.", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
desc_code.pack(pady=10, padx=20)

label_code = tk.Label(frame_code_verify, text="Code de vérification :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
label_code.pack(pady=(10, 5))
entry_code = tk.Entry(frame_code_verify, width=40, font=FONT_LABEL, relief="flat")
entry_code.pack(pady=5, padx=30)

btn_verify_code = tk.Button(
    frame_code_verify,
    text="Valider le code",
    command=handle_verify_code,
    font=FONT_BUTTON,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    relief="flat",
    borderwidth=0
)
btn_verify_code.pack(pady=20, ipadx=10, ipady=5)

# Bouton "Retour" vers la page email
btn_back_to_email = tk.Button(
    frame_code_verify,
    text="< Retour",
    command=lambda: show_frame(frame_email), # Retourne à la page 1
    font=FONT_LINK,
    fg=LINK_FG,
    bg=FRAME_BG,
    relief="flat",
    borderwidth=0,
    activeforeground=TEXT_COLOR,
    activebackground=FRAME_BG
)
btn_back_to_email.pack(pady=10)


# --- PAGE 3 : NOUVEAU MOT DE PASSE ---
frame_new_password = tk.Frame(main_container, bg=FRAME_BG)
frame_new_password.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

title_new_pass = tk.Label(frame_new_password, text="Nouveau mot de passe", font=FONT_TITLE, bg=FRAME_BG, fg=TEXT_COLOR)
title_new_pass.pack(pady=(20, 10))

# Widgets pour le nouveau mot de passe
label_new_pass = tk.Label(frame_new_password, text="Nouveau mot de passe :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
label_new_pass.pack(pady=(10, 5))
entry_new_pass = tk.Entry(frame_new_password, width=40, font=FONT_LABEL, relief="flat", show="*")
entry_new_pass.pack(pady=5, padx=30)

# Widgets pour la confirmation
label_confirm_pass = tk.Label(frame_new_password, text="Confirmer le mot de passe :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
label_confirm_pass.pack(pady=(10, 5))
entry_confirm_pass = tk.Entry(frame_new_password, width=40, font=FONT_LABEL, relief="flat", show="*")
entry_confirm_pass.pack(pady=5, padx=30)

# Bouton de réinitialisation
btn_reset = tk.Button(
    frame_new_password,
    text="Réinitialiser le mot de passe",
    command=handle_reset_password,
    font=FONT_BUTTON,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    relief="flat",
    borderwidth=0
)
btn_reset.pack(pady=20, ipadx=10, ipady=5)

# Bouton "Retour" vers la page code
btn_back_to_code = tk.Button(
    frame_new_password,
    text="< Retour",
    command=lambda: show_frame(frame_code_verify), # Retourne à la page 2
    font=FONT_LINK,
    fg=LINK_FG,
    bg=FRAME_BG,
    relief="flat",
    borderwidth=0,
    activeforeground=TEXT_COLOR,
    activebackground=FRAME_BG
)
btn_back_to_code.pack(pady=10)


# --- LANCEMENT DE L'APP ---
show_frame(frame_email) # Affiche la première page au démarrage
root.mainloop()