# Fichier : us_28.py
# USER STORY 28
# En tant que sportif,
# je veux recevoir un message de motivation personnalisé chaque jour
# afin de rester inspiré.

import tkinter as tk
from datetime import date

BG_COLOR = "#ECF0F1"
TEXT_COLOR = "#17202A"
CARD_BG = "#FFFFFF"

# Liste de messages de motivation avec placeholder {name}
MESSAGES = [
    "Continue, {name} ! Chaque répétition te rapproche de ton objectif. 💪",
    "{name}, même les petites avancées comptent. Aujourd'hui, donne juste 1% de plus. 🔥",
    "Tu n’as pas besoin d’être parfait, seulement constant. On croit en toi, {name}. 🙌",
    "Chaque séance que tu fais, {name}, est une victoire sur la version de toi qui abandonne. 🏋️",
    "Respire, concentre-toi, et fais le premier pas. Le reste suivra, {name}. ✨",
    "{name}, rappelle-toi pourquoi tu as commencé. Ton futur toi te remercie déjà. 🚀",
    "La discipline bat la motivation. Mais aujourd’hui, tu as les deux, {name}. 😉",
    "Un jour ou dès le premier jour ? Tu as choisi de commencer, {name}. Continue. 🌟",
]

def get_daily_message(user_name: str = "sportif") -> str:
    """
    Retourne un message de motivation déterministe pour le jour courant.
    On utilise la date pour choisir un message dans la liste.
    """
    today = date.today()
    idx = today.toordinal() % len(MESSAGES)
    base = MESSAGES[idx]
    # Personnalisation avec le prénom / nom d'utilisateur
    return base.format(name=user_name)


def show_daily_motivation(root_window, user_name: str = "sportif"):
    """
    Ouvre une petite fenêtre avec le message de motivation du jour.
    :param root_window: fenêtre principale (root) venant de main_menu
    :param user_name: nom ou pseudo de l'utilisateur (optionnel)
    """
    win = tk.Toplevel(root_window)
    win.title("🔥 Message de motivation du jour")
    win.geometry("450x250")
    win.resizable(False, False)
    win.configure(bg=BG_COLOR)

    # Titre
    title_label = tk.Label(
        win,
        text="🔥 Message de motivation du jour",
        font=("Arial", 14, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    title_label.pack(pady=(15, 10))

    # Carte mensagem
    card = tk.Frame(win, bg=CARD_BG, bd=1, relief="solid")
    card.pack(padx=20, pady=10, fill="both", expand=True)

    msg = get_daily_message(user_name)

    msg_label = tk.Label(
        card,
        text=msg,
        font=("Arial", 11),
        bg=CARD_BG,
        fg=TEXT_COLOR,
        wraplength=380,
        justify="left"
    )
    msg_label.pack(padx=10, pady=10, fill="both", expand=True)

    # Botão fechar
    btn_close = tk.Button(
        win,
        text="Fermer",
        command=win.destroy,
        font=("Arial", 10, "bold"),
        bg="#BDC3C7",
        fg="#2C3E50",
        relief="flat",
        padx=10,
        pady=5
    )
    btn_close.pack(pady=(0, 15))


# Test isolado (se rodar esse arquivo direto)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test US 28")
    from functools import partial
    tk.Button(root, text="Voir le message du jour",
              command=partial(show_daily_motivation, root, "Caroline")).pack(padx=20, pady=20)
    root.mainloop()
