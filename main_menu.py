# Fichier : main_menu.py

import tkinter as tk
from tkinter import messagebox
import sys

# Import des autres écrans
import connection_initial 
import us_15        
import us_31        
import app_gui
import us_39_RechercheUserAndStatutAdmin   

# --- Variable Globale pour stocker l'utilisateur connecté ---
current_user_data = None

# --- Fonctions d'Action/Simulations ---

def show_user_info():
    # Remplacé par switch_to_profile, mais gardé au cas où
    if current_user_data:
        messagebox.showinfo("ℹ️ Mon Profil", f"Nom: {current_user_data.get('nom')}\nEmail: {current_user_data.get('email')}")
    else:
        messagebox.showerror("Erreur", "Aucun utilisateur connecté.")

def view_sessions():
    messagebox.showinfo("📅 Mes Séances", "Séances de la semaine :\nLundi: Upper\nMercredi: Lower\nVendredi: Full Body")

# --- Fonction Suppression de Compte ---

def delete_account():
    # ... (Logique de suppression inchangée) ...
    confirm = messagebox.askyesno("Suppression du compte", "Êtes-vous sûr de vouloir supprimer votre compte ? ...")
    if confirm:
        messagebox.showinfo("Compte supprimé", "Votre compte a été supprimé (simulation).")
        root.destroy()
        sys.exit()

# --- Fonctions de Navigation ---

def switch_to_login():
    """Déconnexion : Ferme le menu et affiche l'écran de connexion/initial."""
    global current_user_data
    current_user_data = None # Réinitialiser l'utilisateur lors de la déconnexion
    
    if messagebox.askyesno("Déconnexion", "Êtes-vous sûr de vouloir vous déconnecter ?"):
        connection_initial.run_connection_initial(root, switch_to_menu, switch_to_admin_menu)

# Dans main_menu.py

def switch_to_planning():
    """Lance l'écran de planification (us_15)."""
    # --- CORRECTION ---
    # Nous devons passer les current_user_data à l'écran de planification
    us_15.run_planning_screen(root, switch_to_menu, current_user_data)

def switch_to_profile():
    """Lance l'écran du profil utilisateur (app_gui) AVEC les données."""
    if current_user_data:
        # ⚠️ APPEL VERS APP_GUI AVEC LES DONNÉES
        app_gui.run_profile_screen(root, switch_to_menu, current_user_data)
    else:
        messagebox.showerror("Erreur", "Impossible de charger le profil. Données utilisateur non trouvées.")

def switch_to_admin_menu(user_data): # <-- Accepte les données
    """Lance l'interface Administrateur."""
    global current_user_data
    current_user_data = user_data # Stocke les données
    run_admin_menu()

def switch_to_menu(user_data): # <-- Accepte les données
    """Affiche l'écran du Menu Principal Utilisateur."""
    global root, current_user_data
    current_user_data = user_data # Stocke les données
    
    root.geometry("450x450") 
    root.resizable(False, False)
    
    for widget in root.winfo_children():
        widget.destroy()

    BG_COLOR = "#ECF0F1"
    BUTTON_BG = "#2980B9"
    BUTTON_FG = "#FFFFFF"
    FONT_BUTTON = ("Arial", 12, "bold")
    TEXT_COLOR = "#17202A" 

    root.configure(bg=BG_COLOR)
    
    tk.Label(root, text="💪 Menu Principal", font=("Arial", 20, "bold"), 
             bg=BG_COLOR, fg="#2C3E50").pack(pady=20)
    
    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)
    
    # Boutons de Fonctionnalités Utilisateur
    boutons = [
        ("ℹ️ Mon Profil", switch_to_profile), # <-- Appelle la fonction qui passe les données
        ("📅 Voir Mes Séances", view_sessions),
        ("🗓️ Modifier Jours/Semaine", switch_to_planning),
    ]
    
    for text, command in boutons:
        btn = tk.Button(button_frame, text=text, command=command, font=FONT_BUTTON,
                        bg=BUTTON_BG, fg=BUTTON_FG, width=25, height=1, relief="flat", bd=0, 
                        activebackground="#1F618D")
        btn.pack(pady=8)
        
    tk.Button(button_frame, 
              text="🗑️ Supprimer mon compte", 
              command=delete_account, 
              font=FONT_BUTTON,
              bg="#D35400", 
              fg=BUTTON_FG, 
              width=25, 
              height=1,
              relief="flat").pack(pady=8)
    
    challenge_button = tk.Button(root, text="⚡ Défi Finisher ⚡", font=("Arial", 12, "bold"),
        command=lambda: us_31.show_random_challenge(root), bg="#2ECC71", fg="#FFFFFF", relief="flat", padx=10, pady=5)
    challenge_button.pack(pady=10)
    
    # Bouton "Test Admin" est supprimé
               
    tk.Button(root, text="🚪 Déconnexion", command=switch_to_login, font=("Arial", 10),
               bg="#E74C3C", fg="#FFFFFF", relief="flat").pack(pady=20)


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
        ("👥 Gérer Utilisateurs", lambda: us_39_RechercheUserAndStatutAdmin.run_user_management(root, run_admin_menu)), 
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
        
    # --- MODIFICATION ICI ---
    # Le bouton appelle maintenant un lambda qui passe les données utilisateur
    tk.Button(root, text="< Retour Menu Utilisateur", 
               command=lambda: switch_to_menu(current_user_data), # <-- CORRECTION
               font=("Arial", 10),
               bg="#AAAAAA", fg="#17202A", relief="flat").pack(pady=20)

def run_app_start():
    """Fonction de démarrage : crée la fenêtre root et lance l'écran de connexion initial."""
    global root
    root = tk.Tk()
    
    # Démarrage sur l'écran de connexion/inscription
    connection_initial.run_connection_initial(root, switch_to_menu, switch_to_admin_menu)
    root.mainloop()

if __name__ == '__main__':
    run_app_start()