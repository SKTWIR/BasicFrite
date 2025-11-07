# Fichier : main_menu.py

import tkinter as tk
from tkinter import messagebox
import sys
import os # Ajouté pour le chemin du CSV
import csv # Ajouté pour la gestion du CSV

# Import des autres écrans
import connection_initial 
import us_15        
import us_31    
import us_28
import app_gui      

# --- CONSTANTE CSV ---
USER_CSV_FILE = os.path.join(os.path.dirname(__file__), 'User.csv')

# --- Variable Globale pour stocker l'utilisateur connecté ---
current_user_data = None

# --- Fonctions d'Action/Simulations ---

def show_user_info():
    # Remplacé par switch_to_profile
    messagebox.showinfo("Info", "Utilisez 'Mon Profil' pour voir vos informations.")

def view_sessions():
    messagebox.showinfo("📅 Mes Séances", "Séances de la semaine :\nLundi: Upper\nMercredi: Lower\nVendredi: Full Body")

# --- FONCTION DE SUPPRESSION (MISE À JOUR) ---

def delete_account():
    """
    Supprime le compte de l'utilisateur connecté (current_user_data) 
    du fichier User.csv.
    """
    global current_user_data
    if not current_user_data:
        messagebox.showerror("Erreur", "Aucun utilisateur connecté, suppression impossible.")
        return

    user_id_to_delete = current_user_data.get('id_user')
    user_pseudo = current_user_data.get('pseudo', 'Utilisateur')

    confirm = messagebox.askyesno(
        "Suppression du compte",
        f"ATTENTION: Êtes-vous sûr de vouloir supprimer définitivement le compte '{user_pseudo}' ?\n\nCette action est irréversible."
    )
    
    if confirm:
        rows = []
        fieldnames = []
        found = False

        try:
            # 1. Lire le fichier et exclure l'utilisateur
            with open(USER_CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                fieldnames = reader.fieldnames # Sauvegarde des en-têtes
                for row in reader:
                    if row['id_user'] == user_id_to_delete:
                        found = True
                        continue # Ne pas ajouter cet utilisateur à la nouvelle liste
                    rows.append(row)
        
        except Exception as e:
            messagebox.showerror("Erreur Lecture CSV", f"Erreur lors de la lecture des utilisateurs: {e}")
            return

        if not found:
            messagebox.showerror("Erreur", "Utilisateur non trouvé dans le CSV. Suppression annulée.")
            return

        # 2. Réécrire le fichier sans l'utilisateur
        try:
            with open(USER_CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(rows)
        
        except Exception as e:
            messagebox.showerror("Erreur Écriture CSV", f"Erreur lors de la suppression: {e}")
            return

        messagebox.showinfo("Compte supprimé", "Votre compte a été supprimé avec succès.")
        
        # 3. Renvoyer à l'écran de connexion
        switch_to_login()

# --- Fonctions de Navigation ---

def switch_to_login():
    """Déconnexion : Ferme le menu et affiche l'écran de connexion/initial."""
    global current_user_data
    current_user_data = None # Réinitialiser l'utilisateur
    
    # On vérifie si la fenêtre root existe avant de demander la confirmation
    if 'root' in globals() and root.winfo_exists():
        if messagebox.askyesno("Déconnexion", "Êtes-vous sûr de vouloir vous déconnecter ?"):
            connection_initial.run_connection_initial(root, switch_to_menu, switch_to_admin_menu)
    else:
        # Si la fenêtre est détruite (ex: après suppression), juste lancer la connexion
        run_app_start()


def switch_to_planning():
    """Lance l'écran de planification (us_15)."""
    us_15.run_planning_screen(root, switch_to_menu, current_user_data)

def switch_to_profile():
    """Lance l'écran du profil utilisateur (app_gui)."""
    if current_user_data:
        app_gui.run_profile_screen(root, switch_to_menu, current_user_data)
    else:
        messagebox.showerror("Erreur", "Impossible de charger le profil. Données utilisateur non trouvées.")

def switch_to_admin_menu(user_data):
    """Lance l'interface Administrateur."""
    global current_user_data
    current_user_data = user_data
    run_admin_menu()

def switch_to_menu(user_data):
    """Affiche l'écran du Menu Principal Utilisateur."""
    global root, current_user_data
    current_user_data = user_data 
    user_first_name = current_user_data.get('prénom', 'sportif')


    
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
        ("ℹ️ Mon Profil", switch_to_profile), 
        ("📅 Voir Mes Séances", view_sessions),
        ("🗓️ Modifier Jours/Semaine", switch_to_planning),
    ]
    
    for text, command in boutons:
        btn = tk.Button(button_frame, text=text, command=command, font=FONT_BUTTON,
                        bg=BUTTON_BG, fg=BUTTON_FG, width=25, height=1, relief="flat", bd=0, 
                        activebackground="#1F618D")
        btn.pack(pady=8)

    # --- US 28 : Message de motivation du jour ---
    btn_motivation = tk.Button(
        button_frame,  # 👈 agora segue o padrão: dentro do frame dos botões
        text="🔥 Message de motivation",
        command=lambda: us_28.show_daily_motivation(root, user_first_name),
        font=FONT_BUTTON,
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        width=25,
        height=1,
        relief="flat",
        bd=0,
        activebackground="#1F618D"
    )
    btn_motivation.pack(pady=8)
        
    # Bouton Supprimer le compte (maintenant fonctionnel)
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
        
    tk.Button(root, text="< Retour Menu Utilisateur", command=lambda: switch_to_menu(current_user_data), font=("Arial", 10),
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