# login.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Exemplo: credenciais válidas para validação (apenas demo).
# Em aplicação real, verifique contra base de dados / API / hash seguro.
VALID_CREDENTIALS = {
    "carol": "senha123",
    "user1": "motdepasse"
}


def validate_credentials(user_id: str, password: str) -> bool:
    """
    Valida credenciais com a tabela de exemplo.
    Retorna True se válidas, False caso contrário.
    """
    if user_id in VALID_CREDENTIALS and VALID_CREDENTIALS[user_id] == password:
        return True
    return False


def show_login(title: str = "Connexion", require_validation: bool = False) -> dict:
    """
    Mostra uma janela de login em francês.
    :param title: Título da janela
    :param require_validation: se True, valida contra VALID_CREDENTIALS e só fecha se válido.
    :return: dict { "id": str, "password": str, "success": bool }
    """
    result = {"id": "", "password": "", "success": False}

    root = tk.Tk()
    root.title(title)
    root.resizable(False, False)
    root.geometry("360x200")

    # --- Frame principal ---
    frm = ttk.Frame(root, padding=16)
    frm.pack(fill=tk.BOTH, expand=True)

    # Título (opcional)
    lbl_title = ttk.Label(frm, text="Bienvenue — Veuillez vous connecter", font=("Segoe UI", 11, "bold"))
    lbl_title.pack(pady=(0, 10))

    # Identifiant
    lbl_id = ttk.Label(frm, text="Identifiant :")
    lbl_id.pack(anchor="w")
    entry_id = ttk.Entry(frm)
    entry_id.pack(fill="x", pady=(0, 8))

    # Mot de passe
    lbl_pwd = ttk.Label(frm, text="Mot de passe :")
    lbl_pwd.pack(anchor="w")
    entry_pwd = ttk.Entry(frm, show="*")
    entry_pwd.pack(fill="x", pady=(0, 6))

    # Mostrar/ocultar senha
    def toggle_password():
        if entry_pwd.cget("show") == "":
            entry_pwd.config(show="*")
            btn_toggle.config(text="Afficher")
        else:
            entry_pwd.config(show="")
            btn_toggle.config(text="Masquer")

    btn_toggle = ttk.Button(frm, text="Afficher", width=8, command=toggle_password)
    btn_toggle.pack(anchor="e", pady=(0, 6))

    # Função acionada ao clicar em "Se connecter"
    def on_submit():
        user = entry_id.get().strip()
        pwd = entry_pwd.get()

        if not user or not pwd:
            messagebox.showwarning("Attention", "Veuillez entrer l'identifiant et le mot de passe.")
            return

        if require_validation:
            if validate_credentials(user, pwd):
                messagebox.showinfo("Succès", "Connexion réussie.")
                result.update({"id": user, "password": pwd, "success": True})
                root.destroy()
            else:
                messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect.")
                # manter a janela aberta para tentar novamente
        else:
            # sem validação externa -> retornamos os valores
            result.update({"id": user, "password": pwd, "success": True})
            root.destroy()

    def on_cancel():
        result.update({"id": "", "password": "", "success": False})
        root.destroy()

    # Botões
    btn_frame = ttk.Frame(frm)
    btn_frame.pack(fill="x", pady=(8, 0))

    btn_conn = ttk.Button(btn_frame, text="Se connecter", command=on_submit)
    btn_conn.pack(side="left", expand=True, fill="x", padx=(0, 6))

    btn_ann = ttk.Button(btn_frame, text="Annuler", command=on_cancel)
    btn_ann.pack(side="left", expand=True, fill="x", padx=(6, 0))

    # Atalho Enter para submeter
    root.bind("<Return>", lambda event: on_submit())

    # Colocar cursor inicial no campo identifiant
    entry_id.focus_set()

    # Centralizar a janela na tela (opcional)
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    root.geometry(f'+{x}+{y}')

    root.mainloop()
    return result


# Exemplo de uso
if __name__ == "__main__":
    # Se quiser forçar validação contra a tabela de exemplo, passe require_validation=True
    cred = show_login(require_validation=False)
    if cred["success"]:
        print("Conecté : ", cred["id"])
        # Aqui você pode continuar para a tela principal do app,
        # carregar o perfil do usuário, etc.
    else:
        print("Connexion annulée ou échouée.")
