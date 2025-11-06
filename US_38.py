import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox

# --- CONSTANTES ---
# L'ADRESSE A ÉTÉ MODIFIÉE ICI
SUPPORT_EMAIL = "support@basicfrite.com" 

# --- Définition du style ---
BG_COLOR = "#F4F6F7"
TEXT_COLOR = "#17202A"
LINK_FG = "#2980B9"
BUTTON_BG = "#3498DB"      # Bleu vif
BUTTON_FG = "#FFFFFF"      # Blanc
FONT_REGULAR = ("Helvetica", 11)
FONT_LINK = ("Helvetica", 10, "underline")
FONT_TITLE_POPUP = ("Helvetica", 16, "bold")
FONT_LABEL_POPUP = ("Helvetica", 11)

# --- FONCTIONS ---

def handle_send_support_request(popup_window, entry_name, entry_subject, text_message):
    """
    Simule l'envoi du formulaire de support.
    Vérifie juste que les champs ne sont pas vides.
    """
    name = entry_name.get()
    subject = entry_subject.get()
    message = text_message.get("1.0", "end-1c") 
    
    if not name or not subject or not message:
        messagebox.showwarning("Champs incomplets", "Veuillez remplir tous les champs du formulaire.", parent=popup_window)
        return
        
    print(f"--- NOUVELLE DEMANDE DE SUPPORT ---")
    print(f"Nom: {name}")
    print(f"Sujet: {subject}")
    print(f"Message: {message}")
    print(f"---------------------------------")
    
    messagebox.showinfo(
        "Demande envoyée",
        "Merci de nous avoir contactés !\nVotre demande a bien été envoyée à notre équipe.\nNous vous enverons une réponse dans les plus bref delais.",
        parent=popup_window
    )
    
    popup_window.destroy()


def open_support_popup():
    """
    Crée et affiche la fenêtre pop-up de support avec le formulaire.
    """
    
    popup = tk.Toplevel(root)
    popup.title("Contacter le Support")
    popup.geometry("450x600") # Taille de la fenêtre
    popup.configure(bg="#FFFFFF")
    popup.resizable(False, False)
    popup.transient(root)
    popup.grab_set()

    form_frame = tk.Frame(popup, bg="#FFFFFF")
    form_frame.pack(pady=20, padx=30, fill="both", expand=True)

    title_label = tk.Label(
        form_frame,
        text="Envoyer un message",
        font=FONT_TITLE_POPUP,
        bg="#FFFFFF",
        fg=TEXT_COLOR
    )
    title_label.pack(pady=(0, 20))

    label_name = tk.Label(form_frame, text="Votre email :", font=FONT_LABEL_POPUP, bg="#FFFFFF", fg=TEXT_COLOR)
    label_name.pack(anchor="w")
    entry_name = tk.Entry(form_frame, font=FONT_REGULAR, relief="flat", bg=BG_COLOR, width=40)
    entry_name.pack(fill="x", pady=(5, 15))

    label_subject = tk.Label(form_frame, text="Sujet :", font=FONT_LABEL_POPUP, bg="#FFFFFF", fg=TEXT_COLOR)
    label_subject.pack(anchor="w")
    entry_subject = tk.Entry(form_frame, font=FONT_REGULAR, relief="flat", bg=BG_COLOR, width=40)
    entry_subject.pack(fill="x", pady=(5, 15))

    label_message = tk.Label(form_frame, text="Votre message :", font=FONT_LABEL_POPUP, bg="#FFFFFF", fg=TEXT_COLOR)
    label_message.pack(anchor="w")
    text_message = tk.Text(
        form_frame,
        font=FONT_REGULAR,
        relief="flat",
        bg=BG_COLOR,
        height=8,
        borderwidth=0
    )
    text_message.pack(fill="x", pady=(5, 20))

    send_button = tk.Button(
        form_frame,
        text="Envoyer le message",
        font=("Helvetica", 11, "bold"),
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        relief="flat",
        borderwidth=0,
        command=lambda: handle_send_support_request(popup, entry_name, entry_subject, text_message)
    )
    send_button.pack(fill="x", ipady=8, pady=10)

    separator = tk.Frame(form_frame, height=1, bg="#EAECEE")
    separator.pack(fill="x", pady=20)

    alt_text_label = tk.Label(
        form_frame,
        text=f"Vous pouvez également nous contacter directement à l'adresse suivante :",
        font=("Helvetica", 10),
        bg="#FFFFFF",
        fg=TEXT_COLOR,
        wraplength=380, 
        justify="center"
    )
    alt_text_label.pack()
    
    # Ce label utilise maintenant la nouvelle constante
    email_label = tk.Label(
        form_frame,
        text=SUPPORT_EMAIL, 
        font=("Helvetica", 10, "bold"),
        bg="#FFFFFF",
        fg=TEXT_COLOR
    )
    email_label.pack(pady=5)


# --- CONFIGURATION DE LA FENÊTRE PRINCIPALE (Simulation) ---

root = tk.Tk()
root.title("Page Principale (Simulation)")
root.geometry("600x400")
root.configure(bg=BG_COLOR)



# --- LE BOUTON SUPPORT DISCRET ---
support_button = tk.Button(
    root,
    text="Contacter le support",
    command=open_support_popup,
    font=FONT_LINK,
    fg=LINK_FG,
    bg=BG_COLOR,
    relief="flat",
    borderwidth=0,
    activeforeground=TEXT_COLOR,
    activebackground=BG_COLOR
)
support_button.pack(side="bottom", anchor="se", padx=15, pady=15)

# --- Lancer l'application ---
root.mainloop()