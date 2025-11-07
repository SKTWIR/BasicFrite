# Fichier : main_menu.py

import tkinter as tk
from tkinter import messagebox
import sys

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


# --- Fonctions d'Action/Simulations ---

def show_user_info():
    # (Actuellement inutilisée dans ce fichier, le profil passe par app_gui)
    messagebox.showinfo(
        "ℹ️ Mon Profil",
        "Nom: DUPONT\nÂge: 30 ans\nPoids: 75 kg\nObjectif: Hypertrophie"
    )


def view_sessions():
    messagebox.showinfo(
        "📅 Mes Séances",
        "Séances de la semaine :\nLundi: Upper\nMercredi: Lower\nVendredi: Full Body"
    )


# --- Suppression de Compte ---

def delete_account():
    """Supprime le compte utilisateur (Simulé) après confirmation."""
    confirm = messagebox.askyesno(
        "Suppression du compte",
        "Êtes-vous sûr de vouloir supprimer votre compte ? "
        "Cette action est définitive et non réversible."
    )
    if confirm:
        messagebox.showinfo(
            "Compte supprimé",
            "Votre compte a été supprimé (simulation)."
        )
        root.destroy()
        sys.exit()  # Arrête l'application après la suppression


# --- Chat utilisateur : voir notifications de l'administrateur ---

def open_chat_window():
    """Affiche les notifications envoyées par l'administrateur (Chat simple)."""
    chat = tk.Toplevel(root)
    chat.title("💬 Chat - Notifications")
    chat.geometry("450x400")

    BG_COLOR = "#ECF0F1"
    TEXT_COLOR = "#17202A"
    chat.configure(bg=BG_COLOR)

    tk.Label(
        chat,
        text="💬 Messages de l'administrateur",
        font=("Arial", 14, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=10)

    if not NOTIFICATIONS:
        tk.Label(
            chat,
            text="Aucune notification pour le moment.",
            font=("Arial", 11),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=20)
        return

    # Container avec scroll pour la liste de notifications
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

    # Carte pour chaque notification
    for notif in NOTIFICATIONS:
        card = tk.Frame(scroll_frame, bg="white", bd=1, relief="solid")
        card.pack(fill="x", pady=5)

        titre = notif.get("title") or "Notification"
        tk.Label(
            card,
            text=titre,
            font=("Arial", 11, "bold"),
            bg="white",
            anchor="w"
        ).pack(fill="x", padx=8, pady=(4, 0))

        tk.Label(
            card,
            text=notif.get("message", ""),
            font=("Arial", 10),
            justify="left",
            bg="white",
            anchor="w",
            wraplength=380
        ).pack(fill="x", padx=8, pady=(0, 6))


# --- Fenêtre Admin pour envoyer une notification générale ---

def open_admin_notification_window():
    """Fenêtre pour que l'administrateur envoie une notification générale (USER STORY 40)."""
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
        frame,
        text="📢 Envoyer une notification générale",
        font=("Arial", 14, "bold"),
        bg=BG_COLOR
    ).pack(pady=(0, 10))

    tk.Label(
        frame,
        text="Titre (optionnel) :",
        bg=BG_COLOR,
        font=("Arial", 11)
    ).pack(anchor="w")
    entry_titre = tk.Entry(frame, font=("Arial", 11))
    entry_titre.pack(fill="x", pady=(0, 8))

    tk.Label(
        frame,
        text="Message :",
        bg=BG_COLOR,
        font=("Arial", 11)
    ).pack(anchor="w")
    text_msg = tk.Text(frame, height=8, font=("Arial", 10))
    text_msg.pack(fill="both", expand=True, pady=(0, 10))

    def envoyer():
        titre = entry_titre.get().strip()
        contenu = text_msg.get("1.0", tk.END).strip()

        if not contenu:
            messagebox.showwarning(
                "Message vide",
                "Veuillez écrire un message avant d'envoyer."
            )
            return

        # Ajoute la notification à la liste globale (vue dans le Chat utilisateur)
        add_notification(titre or "Notification", contenu)

        messagebox.showinfo(
            "Notification envoyée",
            "La notification a été ajoutée au chat des utilisateurs."
        )
        win.destroy()

    tk.Button(
        frame,
        text="Envoyer à tous les utilisateurs",
        command=envoyer,
        font=("Arial", 11, "bold"),
        bg=BTN_PRIMARY,
        fg="white",
        activebackground=BTN_PRIMARY_ACTIVE,
        activeforeground="white",
        relief="flat",
        height=2
    ).pack(fill="x", pady=(5, 0))


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
    """Lance l'écran du profil utilisateur (app_gui)."""
    app_gui.run_profile_screen(root, switch_to_menu)


def switch_to_admin_menu():
    """Lance l'interface Administrateur."""
    global current_user_data
    current_user_data = user_data # Stocke les données
    run_admin_menu()


def switch_to_menu():
    """Affiche l'écran du Menu Principal Utilisateur."""
    global root

    root.geometry("450x450")  # Taille du menu utilisateur
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
        root,
        text="💪 Menu Principal",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR,
        fg="#2C3E50"
    ).pack(pady=20)

    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)

    # Boutons de Fonctionnalités Utilisateur
    boutons = [
        ("ℹ️ Mon Profil", switch_to_profile),
        ("📅 Voir Mes Séances", view_sessions),
        ("🗓️ Modifier Jours/Semaine", switch_to_planning),
    ]

    for text, command in boutons:
        btn = tk.Button(
            button_frame,
            text=text,
            command=command,
            font=FONT_BUTTON,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            width=25,
            height=1,
            relief="flat",
            bd=0,
            activebackground="#1F618D"
        )
        btn.pack(pady=8)

    # Bouton "Supprimer le compte"
    tk.Button(
        button_frame,
        text="🗑️ Supprimer mon compte",
        command=delete_account,
        font=FONT_BUTTON,
        bg="#D35400",  # Couleur danger
        fg=BUTTON_FG,
        width=25,
        height=1,
        relief="flat"
    ).pack(pady=8)

    # Bouton Défi Finisher
    challenge_button = tk.Button(
        root,
        text="⚡ Défi Finisher ⚡",
        font=("Arial", 12, "bold"),
        command=lambda: us_31.show_random_challenge(root),
        bg="#2ECC71",
        fg="#FFFFFF",
        relief="flat",
        padx=10,
        pady=5
    )
    challenge_button.pack(pady=10)

    # Bouton Chat (notifications de l'admin)
    tk.Button(
        root,
        text="💬 Chat",
        command=open_chat_window,
        font=("Arial", 10, "bold"),
        bg="#3498DB",
        fg="#FFFFFF",
        relief="flat"
    ).pack(pady=5)

    # Bouton Test Admin
    tk.Button(
        root,
        text="⚙️ Test Admin",
        command=switch_to_admin_menu,
        font=("Arial", 10),
        bg="#CCCCCC",
        fg=TEXT_COLOR,
        relief="flat"
    ).pack(pady=(5, 15))

    # Bouton Déconnexion
    tk.Button(
        root,
        text="🚪 Déconnexion",
        command=switch_to_login,
        font=("Arial", 10),
        bg="#E74C3C",
        fg="#FFFFFF",
        relief="flat"
    ).pack(pady=5)


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
        root,
        text="🔑 Menu Administrateur",
        font=("Arial", 20, "bold"),
        bg=BG_COLOR,
        fg="#17202A"
    ).pack(pady=20)

    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)

    # Boutons de Fonctionnalités Administrateur
    boutons_admin = [
        ("👥 Gérer Utilisateurs",
         lambda: messagebox.showinfo("Admin", "Fonctionnalité Gérer Utilisateurs (vide)")),
        ("📝 Gérer Contenu",
         lambda: messagebox.showinfo("Admin", "Fonctionnalité Gérer Contenu (vide)")),
        ("📊 Statistiques",
         lambda: messagebox.showinfo("Admin", "Fonctionnalité Statistiques (vide)")),
        ("📢 Envoyer une notification", open_admin_notification_window),
        ("🔗 Outil #5 (vide)",
         lambda: messagebox.showinfo("Admin", "Fonctionnalité Outil #5 (vide)")),
    ]

    for text, command in boutons_admin:
        btn = tk.Button(
            button_frame,
            text=text,
            command=command,
            font=FONT_BUTTON,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            width=25,
            height=1,
            relief="flat",
            bd=0,
            activebackground="#4A5867"
        )
        btn.pack(pady=8)

    # Bouton de retour vers le Menu Principal Utilisateur
    tk.Button(
        root,
        text="< Retour Menu Utilisateur",
        command=switch_to_menu,
        font=("Arial", 10),
        bg="#AAAAAA",
        fg="#17202A",
        relief="flat"
    ).pack(pady=20)

def run_app_start():
    """Fonction de démarrage : crée la fenêtre root et lance l'écran de connexion initial."""
    global root
    root = tk.Tk()

    # Démarrage sur l'écran de connexion/inscription
    connection_initial.run_connection_initial(root, switch_to_menu, switch_to_admin_menu)
    root.mainloop()


if __name__ == '__main__':
    run_app_start()
