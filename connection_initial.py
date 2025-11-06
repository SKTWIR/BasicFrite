import tkinter as tk

def main():
    # Janela principal de connexion
    root = tk.Tk()
    root.title("Connexion")
    root.geometry("400x320")
    root.resizable(False, False)
    root.configure(bg="#f4f4f4")

    # Frame principal
    frame = tk.Frame(root, bg="#f4f4f4")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Título
    lbl_title = tk.Label(
        frame,
        text="🏋️ Connexion à votre espace",
        font=("Segoe UI", 13, "bold"),
        bg="#f4f4f4"
    )
    lbl_title.pack(pady=(0, 15))

    # Identifiant
    lbl_identifiant = tk.Label(frame, text="Identifiant :", bg="#f4f4f4")
    lbl_identifiant.pack(anchor="w")
    entry_identifiant = tk.Entry(frame)
    entry_identifiant.pack(fill="x", pady=(0, 10))

    # Mot de passe
    lbl_mdp = tk.Label(frame, text="Mot de passe :", bg="#f4f4f4")
    lbl_mdp.pack(anchor="w")
    entry_mdp = tk.Entry(frame, show="*")
    entry_mdp.pack(fill="x", pady=(0, 10))

    # Função "Mot de passe oublié ?"
    def on_forgot():
        print("Mot de passe oublié ? (fonctionnalité à implémenter)")

    btn_forgot = tk.Button(
        frame,
        text="Mot de passe oublié ?",
        bd=0,
        fg="#1E90FF",
        bg="#f4f4f4",
        cursor="hand2",
        font=("Segoe UI", 9, "underline"),
        activebackground="#f4f4f4",
        activeforeground="#1E90FF",
        command=on_forgot
    )
    btn_forgot.pack(anchor="e", pady=(0, 15))

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
        font=("Segoe UI", 12, "bold"),
        bg="#1E90FF",
        fg="white",
        activebackground="#187bcd",
        activeforeground="white",
        relief="flat",
        height=2
    )
    btn_connect.pack(fill="x", pady=(0, 10))

    # ---------- INSCRIPTION (M'inscrire) ----------

    def open_inscription_window():
        """Ouvre une nouvelle fenêtre pour créer un compte (USER STORY 1)."""
        reg = tk.Toplevel(root)
        reg.title("Inscription")
        reg.geometry("420x380")
        reg.resizable(False, False)
        reg.configure(bg="#f4f4f4")

        frame_reg = tk.Frame(reg, bg="#f4f4f4")
        frame_reg.pack(expand=True, fill="both", padx=20, pady=20)

        # Titre
        lbl_reg_title = tk.Label(
            frame_reg,
            text="Créer un compte",
            font=("Segoe UI", 13, "bold"),
            bg="#f4f4f4"
        )
        lbl_reg_title.pack(pady=(0, 15))

        # 1 - Nom
        lbl_nom = tk.Label(frame_reg, text="Nom :", bg="#f4f4f4")
        lbl_nom.pack(anchor="w")
        entry_nom = tk.Entry(frame_reg)
        entry_nom.pack(fill="x", pady=(0, 6))

        # 2 - Prénom
        lbl_prenom = tk.Label(frame_reg, text="Prénom :", bg="#f4f4f4")
        lbl_prenom.pack(anchor="w")
        entry_prenom = tk.Entry(frame_reg)
        entry_prenom.pack(fill="x", pady=(0, 6))

        # 3 - Nom d'utilisateur
        lbl_username = tk.Label(frame_reg, text="Nom d'utilisateur :", bg="#f4f4f4")
        lbl_username.pack(anchor="w")
        entry_username = tk.Entry(frame_reg)
        entry_username.pack(fill="x", pady=(0, 6))

        # 4 - Âge
        lbl_age = tk.Label(frame_reg, text="Âge :", bg="#f4f4f4")
        lbl_age.pack(anchor="w")
        entry_age = tk.Entry(frame_reg)
        entry_age.pack(fill="x", pady=(0, 6))

        # 5 - Poids (kg)
        lbl_poids = tk.Label(frame_reg, text="Poids (kg) :", bg="#f4f4f4")
        lbl_poids.pack(anchor="w")
        entry_poids = tk.Entry(frame_reg)
        entry_poids.pack(fill="x", pady=(0, 6))

        # 6 - Taille (m)
        lbl_taille = tk.Label(frame_reg, text="Taille (m) :", bg="#f4f4f4")
        lbl_taille.pack(anchor="w")
        entry_taille = tk.Entry(frame_reg)
        entry_taille.pack(fill="x", pady=(0, 6))

        # 7 - Mot de passe
        lbl_reg_mdp = tk.Label(frame_reg, text="Mot de passe :", bg="#f4f4f4")
        lbl_reg_mdp.pack(anchor="w")
        entry_reg_mdp = tk.Entry(frame_reg, show="*")
        entry_reg_mdp.pack(fill="x", pady=(0, 10))

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
            font=("Segoe UI", 12, "bold"),
            bg="#1E90FF",
            fg="white",
            activebackground="#187bcd",
            activeforeground="white",
            relief="flat",
            height=2
        )
        btn_create.pack(fill="x", pady=(10, 0))

        # foco inicial
        entry_nom.focus_set()

    # Botão "M'inscrire" (abre tela de criação de conta)
    btn_inscrire = tk.Button(
        frame,
        text="M'inscrire",
        command=open_inscription_window,
        font=("Segoe UI", 10, "bold"),
        bg="#ffffff",
        fg="#1E90FF",
        activebackground="#e6e6e6",
        activeforeground="#1E90FF",
        relief="groove",
        height=1
    )
    btn_inscrire.pack(pady=(0, 5))

    # Foco inicial
    entry_identifiant.focus_set()

    root.mainloop()


if __name__ == "__main__":
    main()
