# admin_notifications.py
import tkinter as tk
from tkinter import messagebox

BG_COLOR = "#f4f4f4"
BTN_PRIMARY = "#1E90FF"
BTN_PRIMARY_ACTIVE = "#187bcd"


def run_admin_notifications():
    """Interface Administrateur pour envoyer des notifications générales (USER STORY 40)."""

    root = tk.Tk()
    root.title("Interface administrateur - Notifications")
    root.geometry("600x480")
    root.resizable(False, False)
    root.configure(bg=BG_COLOR)

    # Frame principal
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    # Titre principal
    lbl_title = tk.Label(
        frame,
        text="📢 Notifications générales",
        font=("Segoe UI", 16, "bold"),
        bg=BG_COLOR
    )
    lbl_title.pack(pady=(0, 20))

    # Sous-texte explicatif
    lbl_info = tk.Label(
        frame,
        text="En tant qu'administrateur, vous pouvez envoyer un message à tous les utilisateurs.",
        font=("Segoe UI", 10),
        bg=BG_COLOR
    )
    lbl_info.pack(pady=(0, 15))

    # Champ : Titre de la notification (optionnel)
    lbl_titre = tk.Label(frame, text="Titre de la notification (optionnel) :", bg=BG_COLOR, font=("Segoe UI", 11))
    lbl_titre.pack(anchor="w")
    entry_titre = tk.Entry(frame, font=("Segoe UI", 11))
    entry_titre.pack(fill="x", pady=(0, 12))

    # Champ : Message
    lbl_message = tk.Label(frame, text="Message :", bg=BG_COLOR, font=("Segoe UI", 11))
    lbl_message.pack(anchor="w")

    text_message = tk.Text(frame, height=10, font=("Segoe UI", 11))
    text_message.pack(fill="both", expand=True, pady=(0, 15))

    # Função de envio
    def envoyer_notification():
        titre = entry_titre.get().strip()
        contenu = text_message.get("1.0", tk.END).strip()

        if not contenu:
            messagebox.showwarning(
                "Message vide",
                "Veuillez écrire un message avant d'envoyer la notification."
            )
            return

        # Aqui seria o lugar para enviar de verdade (BD, API, etc.)
        print("=== Notification générale envoyée ===")
        print(f"Titre : {titre if titre else '(sans titre)'}")
        print(f"Message :\n{contenu}")
        print("=====================================")

        messagebox.showinfo(
            "Notification envoyée",
            "La notification a été envoyée à tous les utilisateurs. (simulation)"
        )

        # Limpar os campos depois de enviar
        entry_titre.delete(0, tk.END)
        text_message.delete("1.0", tk.END)

    # Botão "Envoyer"
    btn_envoyer = tk.Button(
        frame,
        text="Envoyer la notification à tous les utilisateurs",
        command=envoyer_notification,
        font=("Segoe UI", 12, "bold"),
        bg=BTN_PRIMARY,
        fg="white",
        activebackground=BTN_PRIMARY_ACTIVE,
        activeforeground="white",
        relief="flat",
        height=2
    )
    btn_envoyer.pack(fill="x", pady=(10, 0))

    root.mainloop()


if __name__ == "__main__":
    run_admin_notifications()
