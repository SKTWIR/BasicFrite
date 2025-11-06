# Fichier : main_menu.py

import tkinter as tk
from tkinter import messagebox
import sys

# Import des autres écrans
import connection_initial 
import us_15        
import us_31        
import app_gui      

# --- Fonctions d'Action/Simulations (inchangées) ---

def show_user_info():
    messagebox.showinfo("ℹ️ Mon Profil", "Nom: DUPONT\nÂge: 30 ans\nPoids: 75 kg\nObjectif: Hypertrophie")

def view_sessions():
    messagebox.showinfo("📅 Mes Séances", "Séances de la semaine :\nLundi: Upper\nMercredi: Lower\nVendredi: Full Body")

# --- Fonctions de Navigation ---

def switch_to_login():
    """Déconnexion : Ferme le menu et affiche l'écran de connexion/initial."""
    if messagebox.askyesno("Déconnexion", "Êtes-vous sûr de vouloir vous déconnecter ?"):
        connection_initial.run_connection_initial(root, switch_to_menu)

def switch_to_planning():
    """Lance l'écran de planification (us_15)."""
    us_15.run_planning_screen(root, switch_to_menu)

def switch_to_profile():
    """Lance l'écran du profil utilisateur (app_gui)."""
    app_gui.run_profile_screen(root, switch_to_menu)

def switch_to_admin_menu():
    """
    Lance l'interface Administrateur.
    Cette fonction est le point d'entrée pour le bouton "Test Admin".
    """
    run_admin_menu()

def switch_to_menu():
    """Affiche l'écran du Menu Principal Utilisateur."""
    global root
    
    root.geometry("450x420") # TAILLE AUGMENTÉE pour faire de la place au bouton Admin
    root.resizable(False, False)
    
    for widget in root.winfo_children():
        widget.destroy()

    BG_COLOR = "#ECF0F1"
    BUTTON_BG = "#2980B9"
    BUTTON_FG = "#FFFFFF"
    FONT_BUTTON = ("Arial", 12, "bold")
    TEXT_COLOR = "#17202A" # Définition de TEXT_COLOR

    root.configure(bg=BG_COLOR)
    
    tk.Label(root, text="💪 Menu Principal", font=("Arial", 20, "bold"), 
             bg=BG_COLOR, fg="#2C3E50").pack(pady=20)
    
    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)
    
    # Boutons de Fonctionnalités Utilisateur
    boutons = [
        ("ℹ️ Mon Profil", switch_to_profile), 
        ("📅 Voir Mes Séances", view_sessions),
        ("🗓️ Modifier Jours/Semaine", switch_to_planning),
    ]
    
    for text, command in boutons:
        btn = tk.Button(button_frame, text=text, command=command, font=FONT_BUTTON,
                        bg=BUTTON_BG, fg=BUTTON_FG, width=25, height=1, relief="flat", bd=0, 
                        activebackground="#1F618D")
        btn.pack(pady=8)
        
    challenge_button = tk.Button(root, text="⚡ Défi Finisher ⚡", font=("Arial", 12, "bold"),
        command=lambda: us_31.show_random_challenge(root), bg="#2ECC71", fg="#FFFFFF", relief="flat", padx=10, pady=5)
    challenge_button.pack(pady=10)
    
    # --- NOUVEAU BOUTON : Test Admin (Placé ici, distinctement) ---
    tk.Button(root, text="⚙️ Test Admin", command=switch_to_admin_menu, font=("Arial", 10),
               bg="#CCCCCC", fg=TEXT_COLOR, relief="flat").pack(pady=(5, 15)) # Espacement ajusté
               
    tk.Button(root, text="🚪 Déconnexion", command=switch_to_login, font=("Arial", 10),
               bg="#E74C3C", fg="#FFFFFF", relief="flat").pack(pady=5)


def run_admin_menu():
    """Crée et affiche l'interface Administrateur."""
    
    for widget in root.winfo_children():
        widget.destroy()

    BG_COLOR = "#ECF0F1"
    BUTTON_BG = "#5D6D7E" 
    BUTTON_FG = "#FFFFFF"
    FONT_BUTTON = ("Arial", 12, "bold")
    TEXT_COLOR = "#17202A"
    
    root.geometry("450x450") 
    root.title("⚙️ Menu Administrateur")
    root.configure(bg=BG_COLOR)
    
    tk.Label(root, text="🔑 Menu Administrateur", font=("Arial", 20, "bold"), 
             bg=BG_COLOR, fg="#17202A").pack(pady=20)
    
    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)
    
    # Boutons de Fonctionnalités Administrateur (5 boutons vides)
    boutons_admin = [
        ("👥 Gérer Utilisateurs", lambda: messagebox.showinfo("Admin", "Fonctionnalité Gérer Utilisateurs (vide)")), 
        ("📝 Gérer Contenu", lambda: messagebox.showinfo("Admin", "Fonctionnalité Gérer Contenu (vide)")),
        ("📊 Statistiques", lambda: messagebox.showinfo("Admin", "Fonctionnalité Statistiques (vide)")),
        ("🛠️ Outil #4 (vide)", lambda: messagebox.showinfo("Admin", "Fonctionnalité Outil #4 (vide)")),
        ("🔗 Outil #5 (vide)", lambda: messagebox.showinfo("Admin", "Fonctionnalité Outil #5 (vide)")),
    ]
    
    for text, command in boutons_admin:
        btn = tk.Button(button_frame, text=text, command=command, font=FONT_BUTTON,
                        bg=BUTTON_BG, fg=BUTTON_FG, width=25, height=1, relief="flat", bd=0, 
                        activebackground="#4A5867")
        btn.pack(pady=8)
        
    # Bouton de retour vers le Menu Principal Utilisateur
    tk.Button(root, text="< Retour Menu Utilisateur", command=switch_to_menu, font=("Arial", 10),
               bg="#AAAAAA", fg="#17202A", relief="flat").pack(pady=20)


def run_app_start():
    """Fonction de démarrage : crée la fenêtre root et lance l'écran de connexion initial."""
    global root
    root = tk.Tk()
    
    # Démarrage sur l'écran de connexion/inscription
    connection_initial.run_connection_initial(root, switch_to_menu)
    root.mainloop()

if __name__ == '__main__':
    run_app_start()