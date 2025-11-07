# Fichier : admin_notifications.py

import tkinter as tk
from tkinter import messagebox
import json
import os

BG_COLOR = "#ECF0F1"
BTN_PRIMARY = "#2980B9"
BTN_PRIMARY_ACTIVE = "#1F618D"

# Caminho do arquivo onde as notificações serão salvas
NOTIFICATIONS_FILE = os.path.join(os.path.dirname(__file__), "notifications.json")


def save_notification(title: str, message: str):
    """Salva uma nova notificação no arquivo JSON."""
    # Carrega o que já existe
    if os.path.exists(NOTIFICATIONS_FILE):
        try:
            with open(NOTIFICATIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
        except Exception:
            data = []
    else:
        data = []

    # Adiciona nova notificação
    data.append({"title": title, "message": message})

    # Escreve de volta no arquivo
    with open(NOTIFICATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run_admin_notifications():
    """
    Interface Administrateur pour envoyer des notifications générales (USER STORY 40).
    Pode ser chamada a partir do menu Admin.
    """
    root = tk.Tk()
    root.title("📢 Envoyer une notification")
    root.geometry("500x380")
    root.resizable(False, False)
    root.configure(bg=BG_COLOR)

    frame = tk.Frame(root, bg=BG_COLOR)
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

        # Salva no arquivo JSON
        save_notification(titre or "Notification", contenu)

        messagebox.showinfo(
            "Notification envoyée",
            "La notification a été ajoutée pour tous les utilisateurs."
        )
        root.destroy()

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

    root.mainloop()


if __name__ == "__main__":
    run_admin_notifications()
