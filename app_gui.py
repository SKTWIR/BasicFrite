# Fichier : app_gui.py (Adapté pour être appelé par main_menu)

import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
import sys # Ajout de sys pour être complet

# --- DÉFINITION DE LA CLASSE ---

class UserProfile:
    """Une classe pour stocker et valider les informations d'un profil utilisateur."""
    
    # AJOUT DE L'ARGUMENT email
    def __init__(self, first_name, last_name, email=None, age=None, weight=None, height=None):
        if not first_name or not last_name:
            raise ValueError("Le prénom et le nom ne peuvent pas être vides.")
        self.first_name = first_name
        self.last_name = last_name

        # NOUVELLE VALIDATION : Email
        if email is not None and ('@' not in str(email) or '.' not in str(email)):
             raise ValueError("L'email doit être une adresse valide.")
        self.email = email
        
        if age is not None:
            if not isinstance(age, int) or age <= 0:
                raise ValueError("L'âge doit être un nombre entier positif.")
            # ... (Le reste des validations age, weight, height) ...
        self.age = age

        if weight is not None:
            if not isinstance(weight, (float, int)) or weight <= 0:
                raise ValueError("Le poids (kg) doit être un nombre positif.")
        self.weight = weight

        if height is not None:
            if not isinstance(height, (float, int)) or height <= 0 or height > 3:
                raise ValueError("La taille (m) doit être un nombre positif (ex: 1.75).")
        self.height = height


# --- VARIABLES GLOBALES ---
entry_first_name = None
entry_last_name = None
entry_email = None # NOUVELLE VARIABLE GLOBALE POUR L'EMAIL
entry_age = None
entry_weight = None
entry_height = None
current_root = None 


def submit_data(return_callback):
    """Récupère les données des champs, y compris l'email, et met à jour le profil."""
    global entry_email # S'assurer que l'email est accessible
    
    try:
        # 1. Récupérer les données des champs
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        email = entry_email.get() # RÉCUPÉRATION DE L'EMAIL
        
        # 2. Gérer les conversions de nombres
        age = int(entry_age.get()) if entry_age.get() else None
        weight = float(entry_weight.get()) if entry_weight.get() else None
        height = float(entry_height.get()) if entry_height.get() else None

        # 3. Tenter de créer l'utilisateur (déclenche la validation de l'email)
        user = UserProfile(
            first_name=first_name, last_name=last_name, email=email, # PASSAGE DE L'EMAIL
            age=age, weight=weight, height=height
        )

        # 4. Afficher un succès et revenir au menu
        messagebox.showinfo("Succès", f"Profil de {user.first_name} mis à jour! Email: {user.email}. Retour au menu.")
        return_callback()
        
    except ValueError as e:
        # 5. Afficher une erreur
        messagebox.showerror("Erreur de validation", str(e))


def return_to_menu(callback):
    """Ferme cet écran et exécute la fonction de rappel (switch_to_menu)."""
    callback()


def run_profile_screen(root_window, switch_to_menu_callback):
    """Lance l'interface du profil utilisateur dans la fenêtre fournie."""
    global entry_first_name, entry_last_name, entry_email, entry_age, entry_weight, entry_height, current_root

    # 1. Nettoyer l'écran précédent
    for widget in root_window.winfo_children():
        widget.destroy()

    # 2. Configuration de la fenêtre
    root_window.title("Profil Utilisateur")
    root_window.geometry("550x480") # TAILLE AJUSTÉE pour le nouvel champ
    root_window.resizable(False, False)
    current_root = root_window 

    # --- Définition du style (THÈME BLEU) ---
    BG_COLOR = "#D6EAF8"
    TEXT_COLOR = "#17202A"
    BUTTON_BG = "#3498DB"
    BUTTON_FG = "#FFFFFF"
    FONT_LABEL = ("Helvetica", 11)
    FONT_ENTRY = ("Helvetica", 11)
    FONT_BUTTON = ("Helvetica", 11, "bold")

    root_window.configure(bg=BG_COLOR)

    # --- Cadre principal (pour l'espacement) ---
    main_frame = tk.Frame(root_window, bg=BG_COLOR, padx=20, pady=20)
    main_frame.pack(expand=True, fill="both")

    # --- Label Titre
    tk.Label(main_frame, text="ℹ️ Mon Profil", font=("Helvetica", 16, "bold"), bg=BG_COLOR).grid(row=0, column=0, columnspan=2, pady=10)

    # --- Création des widgets (Labels et Champs de saisie) ---
    fields = {
        "Prénom": tk.StringVar(value="Jean"),
        "Nom": tk.StringVar(value="DUPONT"),
        "Email": tk.StringVar(value="jean.dupont@fit.fr"), # AJOUT DU CHAMP EMAIL ICI
        "Âge": tk.StringVar(value="30"),
        "Poids (kg)": tk.StringVar(value="75.5"),
        "Taille (m)": tk.StringVar(value="1.78"),
    }

    row_index = 1
    entries = {} 

    for label_text, var in fields.items():
        label = tk.Label(main_frame, text=f"{label_text} :", font=FONT_LABEL, bg=BG_COLOR, fg=TEXT_COLOR)
        label.grid(row=row_index, column=0, padx=10, pady=8, sticky="e")
        
        entry = tk.Entry(main_frame, textvariable=var, width=40, font=FONT_ENTRY, relief="flat", bg="#FEFEFE")
        entry.grid(row=row_index, column=1, padx=10, pady=8)
        
        # Stocker les champs
        if label_text == "Prénom": entry_first_name = entry
        elif label_text == "Nom": entry_last_name = entry
        elif label_text == "Email": entry_email = entry # NOUVELLE LIAISON
        elif label_text == "Âge": entry_age = entry
        elif label_text == "Poids (kg)": entry_weight = entry
        elif label_text == "Taille (m)": entry_height = entry
        
        row_index += 1

    # --- Bouton de soumission ---
    submit_button = tk.Button(main_frame, text="Enregistrer", command=lambda: submit_data(switch_to_menu_callback),
        font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG, relief="flat", borderwidth=0, activebackground="#2874A6", activeforeground="#FFFFFF"
    )
    submit_button.grid(row=row_index, column=1, pady=(20, 10), padx=10, sticky="e")
    row_index += 1

    # --- Bouton Retour Menu ---
    return_button = tk.Button(main_frame, text="⬅️ Retour Menu", command=lambda: return_to_menu(switch_to_menu_callback),
        font=("Helvetica", 10), bg="#AAAAAA", relief="flat"
    )
    return_button.grid(row=row_index, column=0, columnspan=2, pady=(10, 0), sticky="s")


# --- Ceci est nécessaire si le fichier est exécuté seul ---
if __name__ == '__main__':
    def dummy_callback():
        print("Retour Menu Principal demandé.")
        sys.exit()

    root = tk.Tk()
    run_profile_screen(root, dummy_callback)
    root.mainloop()