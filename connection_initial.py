import tkinter as tk

def main():
    # Janela principal
    root = tk.Tk()
    root.title("Connexion")
    root.geometry("400x260")
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

    # Botão / link "Mot de passe oublié ?"
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
    btn_connect.pack(fill="x")

    # Foco inicial
    entry_identifiant.focus_set()

    root.mainloop()


if __name__ == "__main__":
    main()
