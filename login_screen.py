# Fichier : login_screen.py

import tkinter as tk
from tkinter import messagebox
# ANCIEN IMPORT: import registration_screen 
import connection_initial # <-- NOUVEL IMPORT

def on_forgot():
    print("Mot de passe oublié ? (fonctionnalité à implémenter)")

def run_login_screen(root, switch_to_menu_callback):
    """
    Lance l'interface de l'écran de connexion.
    """
    
    # Nettoyer l'écran précédent
    for widget in root.winfo_children():
        widget.destroy()
        
    # Définitions de style (pour la cohérence)
    BG_COLOR = "#f4f4f4"
    BTN_PRIMARY = "#1E90FF"
    
    # S'assurer que la fenêtre a les bonnes dimensions pour cet écran
    root.title("Connexion")
    root.geometry("400x320") 
    root.resizable(False, False)
    root.configure(bg=BG_COLOR)

    # Frame principal
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(expand=True, fill="both", padx=30, pady=20) 

    # Título
    lbl_title = tk.Label(frame, text="🏋️ Connexion à votre espace", font=("Segoe UI", 14, "bold"), bg=BG_COLOR)
    lbl_title.pack(pady=(0, 15))

    # Identifiant
    lbl_identifiant = tk.Label(frame, text="Identifiant :", bg=BG_COLOR)
    lbl_identifiant.pack(anchor="w")
    entry_identifiant = tk.Entry(frame)
    entry_identifiant.pack(fill="x", pady=(0, 10))

    # Mot de passe
    lbl_mdp = tk.Label(frame, text="Mot de passe :", bg=BG_COLOR)
    lbl_mdp.pack(anchor="w")
    entry_mdp = tk.Entry(frame, show="*")
    entry_mdp.pack(fill="x", pady=(0, 10))

    # Botão / link "Mot de passe oublié ?"
    btn_forgot = tk.Button(frame, text="Mot de passe oublié ?", bd=0, fg=BTN_PRIMARY, bg=BG_COLOR, 
                           cursor="hand2", font=("Segoe UI", 9, "underline"), activebackground=BG_COLOR,
                           activeforeground=BTN_PRIMARY, command=on_forgot)
    btn_forgot.pack(anchor="e", pady=(0, 15))

    # Fonction du bouton "Se connecter"
    def on_connect():
        identifiant = entry_identifiant.get()
        mdp = entry_mdp.get()
        print(f"Tentative de connexion : {identifiant} / {mdp} (logique à implémenter)")
        
        if identifiant and mdp:
            messagebox.showinfo("Succès", f"Bienvenue, {identifiant}!")
            switch_to_menu_callback()
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

    # Botão "Se connecter"
    btn_connect = tk.Button(frame, text="Se connecter", command=on_connect,
                            font=("Segoe UI", 12, "bold"), bg=BTN_PRIMARY, fg="white", 
                            activebackground="#1877bd", activeforeground="white", 
                            relief="flat", height=2)
    btn_connect.pack(fill="x")
    
    # ------------------ BOUTON D'INSCRIPTION ------------------
    inscription_frame = tk.Frame(frame, bg="#E6E6E6", bd=2, relief="groove")
    inscription_frame.pack(fill="x", pady=(15, 0))

    tk.Label(inscription_frame, text="Pas encore de compte ?", bg="#E6E6E6", font=("Segoe UI", 9)).pack(pady=(5, 0))
    
    btn_inscrire = tk.Button(
        inscription_frame,
        text="M'INSCRIRE MAINTENANT",
        command=lambda: connection_initial.run_registration_screen(root), # <-- APPEL CORRIGÉ
        font=("Segoe UI", 10, "bold"),
        bd=0,
        fg=BTN_PRIMARY,
        bg="#E6E6E6",
        cursor="hand2",
        activebackground="#E6E6E6",
        activeforeground=BTN_PRIMARY,
    )
    btn_inscrire.pack(pady=(0, 5))
    # ----------------------------------------------------------

    entry_identifiant.focus_set()

# Si le fichier est exécuté seul (pour test)
if __name__ == "__main__":
    def dummy_menu_callback():
        print("Switch to Menu!")

    root = tk.Tk()
    run_login_screen(root, dummy_menu_callback)
    root.mainloop()