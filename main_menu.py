# Fichier : main_menu.py (Fusionné)

import tkinter as tk
from tkinter import messagebox
import sys
import os 
import csv 

# Notifications générales stockées en mémoire (simulation de base de données)
NOTIFICATIONS = []

def add_notification(title: str, message: str):
    """Ajoute une notification dans la liste globale (simulé)."""
    NOTIFICATIONS.append({"title": title, "message": message})

# Import des autres écrans
import connection_initial
import us_15
import us_31
import app_gui
import us_39 # <-- NOUVEL IMPORT

# --- CONSTANTE CSV ---
USER_CSV_FILE = os.path.join(os.path.dirname(__file__), 'User.csv')

# --- Variable Globale pour stocker l'utilisateur connecté ---
current_user_data = None

# --- Fonctions d'Action/Simulations ---

def show_user_info():
    messagebox.showinfo("Info", "Utilisez 'Mon Profil' pour voir vos informations.")

def view_sessions():
    messagebox.showinfo(
        "📅 Mes Séances",
        "Séances de la semaine :\nLundi: Upper\nMercredi: Lower\nVendredi: Full Body"
    )

# --- FONCTION DE SUPPRESSION (Version CSV fonctionnelle) ---

def delete_account():
    # ... (La fonction delete_account reste inchangée) ...
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
            with open(USER_CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                fieldnames = reader.fieldnames 
                for row in reader:
                    if row['id_user'] == user_id_to_delete:
                        found = True
                        continue 
                    rows.append(row)
        except Exception as e:
            messagebox.showerror("Erreur Lecture CSV", f"Erreur lors de la lecture des utilisateurs: {e}")
            return
        if not found:
            messagebox.showerror("Erreur", "Utilisateur non trouvé dans le CSV. Suppression annulée.")
            return
        try:
            with open(USER_CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(rows)
        except Exception as e:
            messagebox.showerror("Erreur Écriture CSV", f"Erreur lors de la suppression: {e}")
            return
        messagebox.showinfo("Compte supprimé", "Votre compte a été supprimé avec succès.")
        switch_to_login(force_logout=True)


# --- NOUVELLE FONCTIONNALITÉ : Chat utilisateur (Notifications) ---

def open_chat_window():
    # ... (La fonction open_chat_window reste inchangée) ...
    chat = tk.Toplevel(root)
    chat.title("💬 Chat - Notifications")
    chat.geometry("450x400")
    BG_COLOR = "#ECF0F1"
    TEXT_COLOR = "#17202A"
    chat.configure(bg=BG_COLOR)
    tk.Label(
        chat, text="💬 Messages de l'administrateur", font=("Arial", 14, "bold"),
        bg=BG_COLOR, fg=TEXT_COLOR
    ).pack(pady=10)
    if not NOTIFICATIONS:
        tk.Label(
            chat, text="Aucune notification pour le moment.", font=("Arial", 11),
            bg=BG_COLOR, fg=TEXT_COLOR
        ).pack(pady=20)
        return
    container = tk.Frame(chat, bg=BG_COLOR)
    container.pack(fill="both", expand=True, padx=10, pady=10)
    canvas = tk.Canvas(container, bg=BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=BG_COLOR)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    def on_config(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scroll_frame.bind("<Configure>", on_config)
    for notif in NOTIFICATIONS:
        card = tk.Frame(scroll_frame, bg="white", bd=1, relief="solid")
        card.pack(fill="x", pady=5)
        titre = notif.get("title") or "Notification"
        tk.Label(
            card, text=titre, font=("Arial", 11, "bold"), bg="white", anchor="w"
        ).pack(fill="x", padx=8, pady=(4, 0))
        tk.Label(
            card, text=notif.get("message", ""), font=("Arial", 10),
            justify="left", bg="white", anchor="w", wraplength=380
        ).pack(fill="x", padx=8, pady=(0, 6))


# --- NOUVELLE FONCTIONNALITÉ : Fenêtre Admin pour envoyer une notification ---

def open_admin_notification_window():
    # ... (La fonction open_admin_notification_window reste inchangée) ...
    BG_COLOR = "#ECF0F1"
    BTN_PRIMARY = "#2980B9"
    BTN_PRIMARY_ACTIVE = "#1F618D"
    win = tk.Toplevel(root)
    win.title("📢 Envoyer une notification")
    win.geometry("500x380")
    win.resizable(False, False)
    win.configure(bg=BG_COLOR)
    frame = tk.Frame(win, bg=BG_COLOR)
    frame.pack(expand=True, fill="both", padx=20, pady=20)
    tk.Label(
        frame, text="📢 Envoyer une notification générale",
        font=("Arial", 14, "bold"), bg=BG_COLOR
    ).pack(pady=(0, 10))
    tk.Label(
        frame, text="Titre (optionnel) :", bg=BG_COLOR, font=("Arial", 11)
    ).pack(anchor="w")
    entry_titre = tk.Entry(frame, font=("Arial", 11))
    entry_titre.pack(fill="x", pady=(0, 8))
    tk.Label(
        frame, text="Message :", bg=BG_COLOR, font=("Arial", 11)
    ).pack(anchor="w")
    text_msg = tk.Text(frame, height=8, font=("Arial", 10))
    text_msg.pack(fill="both", expand=True, pady=(0, 10))
    def envoyer():
        titre = entry_titre.get().strip()
        contenu = text_msg.get("1.0", tk.END).strip()
        if not contenu:
            messagebox.showwarning("Message vide", "Veuillez écrire un message avant d'envoyer.")
            return
        add_notification(titre or "Notification", contenu)
        messagebox.showinfo("Notification envoyée", "La notification a été ajoutée au chat des utilisateurs.")
        win.destroy()
    tk.Button(
        frame, text="Envoyer à tous les utilisateurs", command=envoyer,
        font=("Arial", 11, "bold"), bg=BTN_PRIMARY, fg="white",
        activebackground=BTN_PRIMARY_ACTIVE, activeforeground="white",
        relief="flat", height=2
    ).pack(fill="x", pady=(5, 0))


# --- Fonctions de Navigation ---

def switch_to_login(force_logout=False):
    # ... (La fonction switch_to_login reste inchangée) ...
    global current_user_data
    current_user_data = None 
    if not ('root' in globals() and root.winfo_exists()):
        run_app_start()
        return
    if force_logout:
        connection_initial.run_connection_initial(root, switch_to_menu, switch_to_admin_menu)
    elif messagebox.askyesno("Déconnexion", "Êtes-vous sûr de vouloir vous déconnecter ?"):
        connection_initial.run_connection_initial(root, switch_to_menu, switch_to_admin_menu)


def switch_to_planning():
    us_15.run_planning_screen(root, switch_to_menu, current_user_data)

def switch_to_profile():
    if current_user_data:
        app_gui.run_profile_screen(root, switch_to_menu, current_user_data)
    else:
        messagebox.showerror("Erreur", "Impossible de charger le profil. Données utilisateur non trouvées.")

def switch_to_admin_menu(user_data):
    global current_user_data
    current_user_data = user_data
    run_admin_menu()

def switch_to_menu(user_data):
    # ... (La fonction switch_to_menu reste inchangée) ...
    global root, current_user_data
    current_user_data = user_data 
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
    tk.Label(
        root, text="💪 Menu Principal", font=("Arial", 20, "bold"),
        bg=BG_COLOR, fg="#2C3E50"
    ).pack(pady=20)
    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)
    boutons = [
        ("ℹ️ Mon Profil", switch_to_profile), 
        ("📅 Voir Mes Séances", view_sessions),
        ("🗓️ Modifier Jours/Semaine", switch_to_planning),
    ]
    for text, command in boutons:
        btn = tk.Button(
            button_frame, text=text, command=command, font=FONT_BUTTON,
            bg=BUTTON_BG, fg=BUTTON_FG, width=25, height=1,
            relief="flat", bd=0, activebackground="#1F618D"
        )
        btn.pack(pady=8)
    tk.Button(button_frame, 
              text="🗑️ Supprimer mon compte", command=delete_account, font=FONT_BUTTON,
              bg="#D35400", fg=BUTTON_FG, width=25, height=1,
              relief="flat").pack(pady=8)
    challenge_button = tk.Button(
        root, text="⚡ Défi Finisher ⚡", font=("Arial", 12, "bold"),
        command=lambda: us_31.show_random_challenge(root),
        bg="#2ECC71", fg="#FFFFFF", relief="flat", padx=10, pady=5
    )
    challenge_button.pack(pady=10)
    tk.Button(
        root, text="💬 Chat", command=open_chat_window,
        font=("Arial", 10, "bold"), bg="#3498DB", fg="#FFFFFF", relief="flat"
    ).pack(pady=5)
    tk.Button(
        root, text="🚪 Déconnexion", command=switch_to_login,
        font=("Arial", 10), bg="#E74C3C", fg="#FFFFFF", relief="flat"
    ).pack(pady=20)


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

    tk.Label(
        root, text="🔑 Menu Administrateur", font=("Arial", 20, "bold"),
        bg=BG_COLOR, fg="#17202A"
    ).pack(pady=20)

    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)

    # --- CORRECTION DU BOUTON ADMIN ---
    boutons_admin = [
        ("👥 Gérer Utilisateurs",
         lambda: us_39.run_user_management(root, run_admin_menu)), # <-- MODIFIÉ
        ("📝 Gérer Contenu",
         lambda: messagebox.showinfo("Admin", "Fonctionnalité Gérer Contenu (vide)")),
        ("📊 Statistiques",
         lambda: messagebox.showinfo("Admin", "Fonctionnalité Statistiques (vide)")),
        ("📢 Envoyer une notification", open_admin_notification_window),
        ("🔗 Outil #5 (vide)",
         lambda: messagebox.showinfo("Admin", "Fonctionnalité Outil #5 (vide)")),
    ]
    # --- FIN CORRECTION ---

    for text, command in boutons_admin:
        btn = tk.Button(
            button_frame, text=text, command=command, font=FONT_BUTTON,
            bg=BUTTON_BG, fg=BUTTON_FG, width=25, height=1,
            relief="flat", bd=0, activebackground="#4A5867"
        )
        btn.pack(pady=8)
        
    tk.Button(root, text="< Retour Menu Utilisateur", 
               command=lambda: switch_to_menu(current_user_data), 
               font=("Arial", 10),
               bg="#AAAAAA", fg="#17202A", relief="flat").pack(pady=20)


def run_app_start():
    """Fonction de démarrage : crée la fenêtre root et lance l'écran de connexion initial."""
    global root
    root = tk.Tk()

    connection_initial.run_connection_initial(root, switch_to_menu, switch_to_admin_menu)
    root.mainloop()


if __name__ == '__main__':
    run_app_start()