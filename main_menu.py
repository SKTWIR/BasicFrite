import tkinter as tk
from tkinter import messagebox
import sys
import os

# ⚠️ La fonction run_us_15_screen va exécuter le script us_15.py
# Pour des raisons de simplicité de l'exemple, nous utilisons os.system. 
# Dans un gros projet, il est préférable d'utiliser une structure de classes.

def run_us_15_screen(root_window):
    """
    Ferme la fenêtre du menu principal et lance l'écran de planification (us_15.py).
    """
    root_window.destroy()
    try:
        # ⚠️ NOTE: Ceci exécute le fichier us_15.py comme un processus séparé.
        # Assurez-vous que us_15.py existe et est exécutable.
        os.system(f"python {os.path.join(os.path.dirname(__file__), 'us_15.py')}")
    except Exception as e:
        print(f"Erreur lors du lancement de us_15.py: {e}")
        # En cas d'échec, relancer le menu
        run_main_menu() 

# --- Fonctions d'Action ---

def show_user_info():
    """Affiche les informations du profil utilisateur (Simulé)."""
    info_user = (
        "Nom: DUPONT\n"
        "Email: dupont@example.com\n"
        "Âge: 30 ans\n"
        "Poids: 75 kg\n"
        "Objectif: Hypertrophie"
    )
    messagebox.showinfo("ℹ️ Mon Profil", info_user)


def view_sessions():
    """Affiche un résumé des séances actuelles (Simulé)."""
    messagebox.showinfo("📅 Mes Séances", "Séances de la semaine :\nLundi: Upper\nMercredi: Lower\nVendredi: Full Body")

def logout(root_window):
    """Déconnecte l'utilisateur et ferme l'application."""
    if messagebox.askyesno("Déconnexion", "Êtes-vous sûr de vouloir vous déconnecter ?"):
        root_window.destroy()
        sys.exit() # Ferme le processus Python

def delete_account(root_window):
    """Supprime le compte utilisateur (Simulé) après confirmation."""
    confirm = messagebox.askyesno(
        "Suppression du compte",
        "Êtes-vous sûr de vouloir supprimer votre compte ? Cette action est définitive."
    )
    if confirm:
        messagebox.showinfo("Compte supprimé", "Votre compte a été supprimé (simulation).")
        root_window.destroy()
        sys.exit()


def run_main_menu():
    """Crée et affiche la fenêtre du Menu Principal."""
    
    menu_root = tk.Tk()
    menu_root.title("🏠 Menu Principal - Application Muscu")
    menu_root.geometry("450x350")
    menu_root.resizable(False, False)
    
    BG_COLOR = "#ECF0F1" # Gris clair
    BUTTON_BG = "#2980B9" # Bleu
    BUTTON_FG = "#FFFFFF" # Blanc
    FONT_BUTTON = ("Arial", 12, "bold")
    
    menu_root.configure(bg=BG_COLOR)
    
    # --- Titre ---
    label_titre = tk.Label(menu_root, text="💪 Menu Principal", 
                           font=("Arial", 20, "bold"), 
                           bg=BG_COLOR, fg="#2C3E50")
    label_titre.pack(pady=20)
    
    # --- Cadre pour les boutons (alignement vertical) ---
    button_frame = tk.Frame(menu_root, bg=BG_COLOR)
    button_frame.pack(pady=10)
    
    # --- Boutons de Fonctionnalités ---
    boutons = [
        ("ℹ️ Mon Profil", show_user_info),
        ("📅 Voir Mes Séances", view_sessions),
        ("🗓️ Modifier Jours/Semaine", lambda: run_us_15_screen(menu_root)), 
        ("🗑️ Supprimer mon compte", lambda: delete_account(menu_root)),  # 👈 NOVO
    ]

    
    for text, command in boutons:
        btn = tk.Button(button_frame, 
                        text=text, 
                        command=command,
                        font=FONT_BUTTON,
                        bg=BUTTON_BG,
                        fg=BUTTON_FG,
                        width=25, 
                        height=1,
                        relief="flat",
                        bd=0, 
                        activebackground="#1F618D")
        btn.pack(pady=8)
        
    # --- Bouton Déconnexion (Séparé) ---
    btn_logout = tk.Button(menu_root, 
                           text="🚪 Déconnexion", 
                           command=lambda: logout(menu_root),
                           font=("Arial", 10),
                           bg="#E74C3C", 
                           fg="#FFFFFF",
                           relief="flat")
    btn_logout.pack(pady=20)
    
    menu_root.mainloop()

if __name__ == '__main__':
    run_main_menu()