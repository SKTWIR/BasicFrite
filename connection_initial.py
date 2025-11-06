import tkinter as tk

def main():
    # Janela principal
    root = tk.Tk()
    root.title("Connexion")
    root.geometry("400x300")
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

    # Botão "Se connecter"
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
        """Ouvre une nouvelle fenêtre pour créer un compte."""
        reg = tk.Toplevel(root)
        reg.title("Inscription")
        reg.geometry("400x260")
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

        # Nom
        lbl_nom = tk.Label(frame_reg, text="Nom :", bg="#f4f4f4")
        lbl_nom.pack(anchor="w")
        entry_nom = tk.Entry(frame_reg)
        entry_nom.pack(fill="x", pady=(0, 8))

        # Prénom
        lbl_prenom = tk.Label(frame_reg, text="Prénom :", bg="#f4f4f4")
        lbl_prenom.pack(anchor="w")
        entry_prenom = tk.Entry(frame_reg)
        entry_prenom.pack(fill="x", pady=(0, 8))

        # Mot de passe
        lbl_reg_mdp = tk.Label(frame_reg, text="Mot de passe :", bg="#f4f4f4")
        lbl_reg_mdp.pack(anchor="w")
        entry_reg_mdp = tk.Entry(frame_reg, show="*")
        entry_reg_mdp.pack(fill="x", pady=(0, 12))

        # Função do botão "Créer le compte"
        def on_create_account():
            nom = entry_nom.get()
            prenom = entry_prenom.get()
            mdp = entry_reg_mdp.get()
            print(f"Création de compte -> Nom: {nom}, Prénom: {prenom}, Mot de passe: {mdp} (logique à implémenter)")
            # aqui depois vocês podem salvar no arquivo / base de données

        btn_create = tk.Button(
            frame_reg,
            text="Créer le compte",
            command=on_create_account,
            font=("Segoe UI", 11, "bold"),
            bg="#28a745",
            fg="white",
            activebackground="#218838",
            activeforeground="white",
            relief="flat",
            height=2
        )
        btn_create.pack(fill="x", pady=(10, 0))

    # Botão "M'inscrire"
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
