import tkinter as tk

BG_COLOR = "#f4f4f4"
BTN_PRIMARY = "#1E90FF"
BTN_PRIMARY_ACTIVE = "#187bcd"


def main():
    # ------------------ JANELA PRINCIPAL (CONNEXION) ------------------
    root = tk.Tk()
    root.title("Connexion")
    root.geometry("600x480")  # você pode ajustar aqui
    root.resizable(False, False)
    root.configure(bg=BG_COLOR)

    # Frame principal
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(expand=True, fill="both", padx=40, pady=40)

    # Título
    lbl_title = tk.Label(
        frame,
        text="🏋️ Connexion à votre espace",
        font=("Segoe UI", 16, "bold"),
        bg=BG_COLOR
    )
    lbl_title.pack(pady=(0, 25))

    # Identifiant
    lbl_identifiant = tk.Label(frame, text="Identifiant :", bg=BG_COLOR, font=("Segoe UI", 12))
    lbl_identifiant.pack(anchor="w")
    entry_identifiant = tk.Entry(frame, font=("Segoe UI", 11))
    entry_identifiant.pack(fill="x", pady=(0, 15))

    # Mot de passe
    lbl_mdp = tk.Label(frame, text="Mot de passe :", bg=BG_COLOR, font=("Segoe UI", 12))
    lbl_mdp.pack(anchor="w")
    entry_mdp = tk.Entry(frame, show="*", font=("Segoe UI", 11))
    entry_mdp.pack(fill="x", pady=(0, 15))

    # Função "Mot de passe oublié ?"
    def on_forgot():
        print("Mot de passe oublié ? (fonctionnalité à implémenter)")

    btn_forgot = tk.Button(
        frame,
        text="Mot de passe oublié ?",
        bd=0,
        fg=BTN_PRIMARY,
        bg=BG_COLOR,
        cursor="hand2",
        font=("Segoe UI", 10, "underline"),
        activebackground=BG_COLOR,
        activeforeground=BTN_PRIMARY,
        command=on_forgot
    )
    btn_forgot.pack(anchor="e", pady=(0, 20))

    # Função do botão "Se connecter"
    def on_connect():
        identifiant = entry_identifiant.get()
        mdp = entry_mdp.get()
        print(f"Tentative de connexion : {identifiant} / {mdp} (logique à implémenter)")

    # Botão grande "Se connecter"
    btn_connect = tk.Button(
        frame,
        text="Se connecter",
        command=on_connect,
        font=("Segoe UI", 13, "bold"),
        bg=BTN_PRIMARY,
        fg="white",
        activebackground=BTN_PRIMARY_ACTIVE,
        activeforeground="white",
        relief="flat",
        height=2
    )
    btn_connect.pack(fill="x", pady=(0, 12))

    # ------------------ INSCRIPTION (M'INSCRIRE) ------------------

    def open_inscription_window():
        """Ouvre une nouvelle fenêtre pour créer un compte (USER STORY 1)."""
        reg = tk.Toplevel(root)
        reg.title("Inscription")
        reg.geometry("600x480")  # tamanho da janela de cadastro
        reg.resizable(False, False)
        reg.configure(bg=BG_COLOR)

        # ---- Container com Canvas + Scrollbar para permitir rolagem ----
        container = tk.Frame(reg, bg=BG_COLOR)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame interno rolável
        frame_reg = tk.Frame(canvas, bg=BG_COLOR)
        canvas.create_window((0, 0), window=frame_reg, anchor="nw")

        # Atualiza a região de scroll quando o conteúdo muda
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_reg.bind("<Configure>", on_frame_configure)

        # (Opcional) rolar com a rodinha do mouse
        def _on_mousewheel(event):
            # Em Mac, o delta costuma ser pequeno, mas isso já funciona
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        frame_reg.bind_all("<MouseWheel>", _on_mousewheel)

        # ------------------ CAMPOS DA CRIAÇÃO DE CONTA ------------------

        lbl_reg_title = tk.Label(
            frame_reg,
            text="Créer un compte",
            font=("Segoe UI", 16, "bold"),
            bg=BG_COLOR
        )
        lbl_reg_title.pack(pady=(20, 20))

        # 1 - Nom
        lbl_nom = tk.Label(frame_reg, text="Nom :", bg=BG_COLOR, font=("Segoe UI", 12))
        lbl_nom.pack(anchor="w", padx=40)
        entry_nom = tk.Entry(frame_reg, font=("Segoe UI", 11))
        entry_nom.pack(fill="x", padx=40, pady=(0, 8))

        # 2 - Prénom
        lbl_prenom = tk.Label(frame_reg, text="Prénom :", bg=BG_COLOR, font=("Segoe UI", 12))
        lbl_prenom.pack(anchor="w", padx=40)
        entry_prenom = tk.Entry(frame_reg, font=("Segoe UI", 11))
        entry_prenom.pack(fill="x", padx=40, pady=(0, 8))

        # 3 - Nom d'utilisateur
        lbl_username = tk.Label(frame_reg, text="Nom d'utilisateur :", bg=BG_COLOR, font=("Segoe UI", 12))
        lbl_username.pack(anchor="w", padx=40)
        entry_username = tk.Entry(frame_reg, font=("Segoe UI", 11))
        entry_username.pack(fill="x", padx=40, pady=(0, 8))

        # 4 - Âge
        lbl_age = tk.Label(frame_reg, text="Âge :", bg=BG_COLOR, font=("Segoe UI", 12))
        lbl_age.pack(anchor="w", padx=40)
        entry_age = tk.Entry(frame_reg, font=("Segoe UI", 11))
        entry_age.pack(fill="x", padx=40, pady=(0, 8))

        # 5 - Poids (kg)
        lbl_poids = tk.Label(frame_reg, text="Poids (kg) :", bg=BG_COLOR, font=("Segoe UI", 12))
        lbl_poids.pack(anchor="w", padx=40)
        entry_poids = tk.Entry(frame_reg, font=("Segoe UI", 11))
        entry_poids.pack(fill="x", padx=40, pady=(0, 8))

        # 6 - Taille (m)
        lbl_taille = tk.Label(frame_reg, text="Taille (m) :", bg=BG_COLOR, font=("Segoe UI", 12))
        lbl_taille.pack(anchor="w", padx=40)
        entry_taille = tk.Entry(frame_reg, font=("Segoe UI", 11))
        entry_taille.pack(fill="x", padx=40, pady=(0, 8))

        # 7 - Mot de passe
        lbl_reg_mdp = tk.Label(frame_reg, text="Mot de passe :", bg=BG_COLOR, font=("Segoe UI", 12))
        lbl_reg_mdp.pack(anchor="w", padx=40)
        entry_reg_mdp = tk.Entry(frame_reg, show="*", font=("Segoe UI", 11))
        entry_reg_mdp.pack(fill="x", padx=40, pady=(0, 15))

        # Função do botão "Créer le compte"
        def on_create_account():
            nom = entry_nom.get()
            prenom = entry_prenom.get()
            username = entry_username.get()
            age = entry_age.get()
            poids = entry_poids.get()
            taille = entry_taille.get()
            mdp = entry_reg_mdp.get()

            print(
                "Création de compte -> "
                f"Nom: {nom}, Prénom: {prenom}, Nom d'utilisateur: {username}, "
                f"Âge: {age}, Poids: {poids} kg, Taille: {taille} m, "
                f"Mot de passe: {mdp} (logique à implémenter)"
            )

        # Botão "Créer le compte" (mesmo estilo do Se connecter)
        btn_create = tk.Button(
            frame_reg,
            text="Créer le compte",
            command=on_create_account,
            font=("Segoe UI", 13, "bold"),
            bg=BTN_PRIMARY,
            fg="white",
            activebackground=BTN_PRIMARY_ACTIVE,
            activeforeground="white",
            relief="flat",
            height=2
        )
        btn_create.pack(fill="x", padx=40, pady=(10, 30))

        entry_nom.focus_set()

    # Botão "M'inscrire"
    btn_inscrire = tk.Button(
        frame,
        text="M'inscrire",
        command=open_inscription_window,
        font=("Segoe UI", 11, "bold"),
        bg="#ffffff",
        fg=BTN_PRIMARY,
        activebackground="#e6e6e6",
        activeforeground=BTN_PRIMARY,
        relief="groove",
        height=1
    )
    btn_inscrire.pack(pady=(0, 5))

    entry_identifiant.focus_set()
    root.mainloop()


if __name__ == "__main__":
    main()
