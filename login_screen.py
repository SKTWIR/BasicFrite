# Fichier : login_screen.py

import tkinter as tk
from tkinter import messagebox

def on_forgot():
    print("Mot de passe oublié ? (fonctionnalité à implémenter)")
    # messagebox.showinfo("Fonctionnalité", "Mot de passe oublié ?")

def run_login_screen(root, switch_to_menu_callback):
    """
    Lance l'interface de l'écran de connexion.
    Prend la fenêtre Tkinter root et la fonction de basculement vers le menu.
    """
    
    # Nettoyer l'écran précédent
    for widget in root.winfo_children():
        widget.destroy()
        
    # S'assurer que la fenêtre a les bonnes dimensions pour cet écran
    root.title("Connexion")
    root.geometry("400x260")
    root.resizable(False, False)
    root.configure(bg="#f4f4f4")

    # Frame principal
    frame = tk.Frame(root, bg="#f4f4f4")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Título
    lbl_title = tk.Label(frame, text="🏋️ Connexion à votre espace", font=("Segoe UI", 13, "bold"), bg="#f4f4f4")
    lbl_title.pack(pady=(0, 15))

    # Identifiant
    lbl_identifiant = tk.Label(frame, text="Identifiant :", bg="#f4f4f4")
    lbl_identifiant.pack(anchor="w")
    entry_identifiant = tk.Entry(frame)
    entry_identifiant.pack(fill="x", pady=(0, 10))

    # Mot de passe
    lbl_mdp = tk.Label(frame, text="Mot de passe :", bg="#f4f4f4")
    lbl_mdp.pack(anchor="w")
    entry_mdp = tk.Entry(frame, show="*")
    entry_mdp.pack(fill="x", pady=(0, 10))

    # Botão / link "Mot de passe oublié ?"
    btn_forgot = tk.Button(frame, text="Mot de passe oublié ?", bd=0, fg="#1E90FF", bg="#f4f4f4", 
                           cursor="hand2", font=("Segoe UI", 9, "underline"), activebackground="#f4f4f4",
                           activeforeground="#1E90FF", command=on_forgot)
    btn_forgot.pack(anchor="e", pady=(0, 15))

    # Fonction du bouton "Se connecter"
    def on_connect():
        identifiant = entry_identifiant.get()
        mdp = entry_mdp.get()
        print(f"Tentative de connexion : {identifiant} / {mdp} (logique à implémenter)")
        
        # Logique de succès simplifiée
        if identifiant and mdp:
            messagebox.showinfo("Succès", f"Bienvenue, {identifiant}!")
            # Appel du Menu Principal via le callback
            switch_to_menu_callback()
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

    # Botão "Se connecter"
    btn_connect = tk.Button(frame, text="Se connecter", command=on_connect,
                            font=("Segoe UI", 12, "bold"), bg="#1E90FF", fg="white", 
                            activebackground="#1877bd", activeforeground="white", 
                            relief="flat", height=2)
    btn_connect.pack(fill="x")

    entry_identifiant.focus_set()

# Si le fichier est exécuté seul (pour test)
if __name__ == "__main__":
    def dummy_menu_callback():
        print("Switch to Menu!")

    root = tk.Tk()
    run_login_screen(root, dummy_menu_callback)
    root.mainloop()