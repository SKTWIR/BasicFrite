# Fichier : us_2.py (Récupération de mot de passe)

import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
import sys # Pour l'exécution seule, mais nécessaire si on le met dans un bloc

# --- CONSTANTES ---
HARDCODED_CODE = "frite" # Le code secret

# --- Définition du style (THÈME BLEU) ---
BG_COLOR = "#D6EAF8" 
FRAME_BG = "#EBF5FB" 
TEXT_COLOR = "#17202A" 
BUTTON_BG = "#3498DB" 
BUTTON_FG = "#FFFFFF" 
LINK_FG = "#2980B9" 
FONT_TITLE = ("Helvetica", 16, "bold")
FONT_LABEL = ("Helvetica", 11)
FONT_BUTTON = ("Helvetica", 11, "bold")
FONT_LINK = ("Helvetica", 10, "underline")

# Variables pour stocker les widgets entre les fonctions
global entry_email, entry_code, entry_new_pass, entry_confirm_pass 
global frame_email, frame_code_verify, frame_new_password

def run_password_recovery(root_window, switch_to_login_callback):
    """
    Lance l'interface multi-page de récupération de mot de passe dans root_window.
    Prend une fonction de rappel pour revenir à l'écran de connexion.
    """
    global entry_email, entry_code, entry_new_pass, entry_confirm_pass
    global frame_email, frame_code_verify, frame_new_password
    
    # Nettoyer l'écran précédent
    for widget in root_window.winfo_children():
        widget.destroy()

    # --- CONFIGURATION DE LA FENÊTRE ---
    root_window.title("Récupération de mot de passe")
    root_window.geometry("450x400")
    root_window.configure(bg=BG_COLOR)
    root_window.resizable(False, False)

    # --- FONCTIONS LOGIQUES (Définies localement ou adaptées pour le contexte) ---
    def show_frame(frame_to_show):
        frame_to_show.tkraise()

    def handle_send_code():
        email = entry_email.get()
        if not email or "@" not in email or "." not in email:
            messagebox.showerror("Email invalide", "Veuillez entrer une adresse email valide.")
            return
        
        messagebox.showinfo("Code 'envoyé'", f"Un email de réinitialisation a été 'envoyé' à {email}.")
        entry_code.delete(0, 'end')
        show_frame(frame_code_verify)

    def handle_verify_code():
        code = entry_code.get()
        if code != HARDCODED_CODE:
            messagebox.showerror("Code incorrect", "Le code de vérification est incorrect.")
            return
        
        entry_new_pass.delete(0, 'end')
        entry_confirm_pass.delete(0, 'end')
        show_frame(frame_new_password)

    def handle_reset_password():
        new_pass = entry_new_pass.get()
        confirm_pass = entry_confirm_pass.get()
        
        if not new_pass or len(new_pass) < 6:
            messagebox.showerror("Mot de passe faible", "Le mot de passe doit contenir au moins 6 caractères.")
            return
            
        if new_pass != confirm_pass:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return
            
        messagebox.showinfo("Succès", "Votre mot de passe a été réinitialisé avec succès ! Vous pouvez vous connecter.")
        
        # Retourne à l'écran de connexion
        entry_email.delete(0, 'end')
        switch_to_login_callback()


    # --- CONTENEUR PRINCIPAL (pour empiler les "pages") ---
    main_container = tk.Frame(root_window, bg=BG_COLOR)
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

    tk.Label(frame_email, text="Adresse Email :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR).pack(pady=(10, 5))
    entry_email = tk.Entry(frame_email, width=40, font=FONT_LABEL, relief="flat")
    entry_email.pack(pady=5, padx=30)

    tk.Button(frame_email, text="Envoyer le code", command=handle_send_code, font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG, relief="flat", borderwidth=0).pack(pady=20, ipadx=10, ipady=5)
    
    # Bouton Retour (vers l'écran de connexion initial)
    tk.Button(frame_email, text="< Retour à la Connexion", command=switch_to_login_callback, 
              font=FONT_LINK, fg=LINK_FG, bg=FRAME_BG, relief="flat", borderwidth=0, activeforeground=TEXT_COLOR, activebackground=FRAME_BG).pack(pady=10)


    # --- PAGE 2 : VÉRIFICATION DU CODE ---
    frame_code_verify = tk.Frame(main_container, bg=FRAME_BG)
    frame_code_verify.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(frame_code_verify, text="Vérifiez vos emails", font=FONT_TITLE, bg=FRAME_BG, fg=TEXT_COLOR).pack(pady=(20, 10))
    tk.Label(frame_code_verify, text="Entrez le code reçu par email.", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR).pack(pady=10, padx=20)
    tk.Label(frame_code_verify, text="Code de vérification :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR).pack(pady=(10, 5))
    entry_code = tk.Entry(frame_code_verify, width=40, font=FONT_LABEL, relief="flat")
    entry_code.pack(pady=5, padx=30)

    tk.Button(frame_code_verify, text="Valider le code", command=handle_verify_code, font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG, relief="flat", borderwidth=0).pack(pady=20, ipadx=10, ipady=5)

    # Bouton "Retour" vers la page email
    tk.Button(frame_code_verify, text="< Retour", command=lambda: show_frame(frame_email), font=FONT_LINK, fg=LINK_FG, bg=FRAME_BG, relief="flat", borderwidth=0, activeforeground=TEXT_COLOR, activebackground=FRAME_BG).pack(pady=10)


    # --- PAGE 3 : NOUVEAU MOT DE PASSE ---
    frame_new_password = tk.Frame(main_container, bg=FRAME_BG)
    frame_new_password.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(frame_new_password, text="Nouveau mot de passe", font=FONT_TITLE, bg=FRAME_BG, fg=TEXT_COLOR).pack(pady=(20, 10))
    tk.Label(frame_new_password, text="Nouveau mot de passe :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR).pack(pady=(10, 5))
    entry_new_pass = tk.Entry(frame_new_password, width=40, font=FONT_LABEL, relief="flat", show="*")
    entry_new_pass.pack(pady=5, padx=30)

    tk.Label(frame_new_password, text="Confirmer le mot de passe :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR).pack(pady=(10, 5))
    entry_confirm_pass = tk.Entry(frame_new_password, width=40, font=FONT_LABEL, relief="flat", show="*")
    entry_confirm_pass.pack(pady=5, padx=30)

    tk.Button(frame_new_password, text="Réinitialiser le mot de passe", command=handle_reset_password, font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG, relief="flat", borderwidth=0).pack(pady=20, ipadx=10, ipady=5)

    # Bouton "Retour" vers la page code
    tk.Button(frame_new_password, text="< Retour", command=lambda: show_frame(frame_code_verify), font=FONT_LINK, fg=LINK_FG, bg=FRAME_BG, relief="flat", borderwidth=0, activeforeground=TEXT_COLOR, activebackground=FRAME_BG).pack(pady=10)


    # --- LANCEMENT DE L'APP ---
    show_frame(frame_email)
    
# Si exécuté seul pour test
if __name__ == '__main__':
    def dummy_login_callback():
        print("Retour Connexion.")
        sys.exit()

    root = tk.Tk()
    run_password_recovery(root, dummy_login_callback)
    root.mainloop()