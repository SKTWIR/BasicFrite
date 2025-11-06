# Fichier : main_menu.py

import tkinter as tk
from tkinter import messagebox
import sys

# Import des autres écrans
import login_screen # <-- Votre écran de connexion (doit exister)
import us_15        # <-- Votre écran de planification

# --- Fonctions d'Action (simulées) ---

def show_user_info():
    messagebox.showinfo("ℹ️ Mon Profil", "Nom: DUPONT\nÂge: 30 ans\nPoids: 75 kg\nObjectif: Hypertrophie")

def view_sessions():
    messagebox.showinfo("📅 Mes Séances", "Séances de la semaine :\nLundi: Upper\nMercredi: Lower\nVendredi: Full Body")

# --- Fonctions de Navigation ---

def switch_to_login():
    """Déconnexion : Ferme le menu et affiche l'écran de connexion."""
    if messagebox.askyesno("Déconnexion", "Êtes-vous sûr de vouloir vous déconnecter ?"):
        # ⚠️ APPEL VERS LOGIN_SCREEN
        login_screen.run_login_screen(root, switch_to_menu)

def switch_to_planning():
    """Lance l'écran de planification (us_15)."""
    # ⚠️ APPEL VERS US_15, en lui passant la fenêtre root et la fonction de retour
    us_15.run_planning_screen(root, switch_to_menu)

def switch_to_menu():
    """Affiche l'écran du Menu Principal."""
    global root
    
    root.geometry("450x350")
    root.resizable(False, False)
    
    # Nettoyer l'écran précédent
    for widget in root.winfo_children():
        widget.destroy()

    BG_COLOR = "#ECF0F1"
    BUTTON_BG = "#2980B9"
    BUTTON_FG = "#FFFFFF"
    FONT_BUTTON = ("Arial", 12, "bold")
    
    root.configure(bg=BG_COLOR)
    
    # Titre
    tk.Label(root, text="💪 Menu Principal", font=("Arial", 20, "bold"), 
             bg=BG_COLOR, fg="#2C3E50").pack(pady=20)
    
    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)
    
    # Boutons de Fonctionnalités
    boutons = [
        ("ℹ️ Mon Profil", show_user_info),
        ("📅 Voir Mes Séances", view_sessions),
        ("🗓️ Modifier Jours/Semaine", switch_to_planning), # <-- Bouton modifié
    ]
    
    for text, command in boutons:
        btn = tk.Button(button_frame, text=text, command=command, font=FONT_BUTTON,
                        bg=BUTTON_BG, fg=BUTTON_FG, width=25, height=1, relief="flat", bd=0, 
                        activebackground="#1F618D")
        btn.pack(pady=8)
        
    # Bouton Déconnexion (Appelle switch_to_login)
    tk.Button(root, text="🚪 Déconnexion", command=switch_to_login, font=("Arial", 10),
               bg="#E74C3C", fg="#FFFFFF", relief="flat").pack(pady=20)


def run_app_start():
    """Fonction de démarrage : crée la fenêtre root et lance l'écran de connexion."""
    global root
    root = tk.Tk()
    
    # Démarrage sur l'écran de connexion
    login_screen.run_login_screen(root, switch_to_menu)
    root.mainloop()

if __name__ == '__main__':
    run_app_start()