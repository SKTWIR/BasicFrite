import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont # Import pour gérer les polices

# --- DÉFINITION DE LA CLASSE (SANS L'IMC) ---

class UserProfile:
    """
    Une classe pour stocker et valider les informations d'un profil utilisateur.
    (Version simplifiée sans calcul d'IMC)
    """
    
    def __init__(self, first_name, last_name, age=None, weight=None, height=None):
        """
        Le constructeur valide les données dès la création.
        Lève une ValueError si les données sont invalides.
        """
        
        # 1. Valider les noms (requis)
        if not first_name or not last_name:
            raise ValueError("Le prénom et le nom ne peuvent pas être vides.")
        self.first_name = first_name
        self.last_name = last_name

        # 2. Valider l'âge (optionnel, mais doit être positif si fourni)
        if age is not None:
            if not isinstance(age, int) or age <= 0:
                raise ValueError("L'âge doit être un nombre entier positif.")
        self.age = age

        # 3. Valider le poids (optionnel, mais doit être positif si fourni)
        if weight is not None:
            if not isinstance(weight, (float, int)) or weight <= 0:
                raise ValueError("Le poids (kg) doit être un nombre positif.")
        self.weight = weight

        # 4. Valider la taille (optionnelle, mais doit être positive si fournie)
        if height is not None:
            if not isinstance(height, (float, int)) or height <= 0 or height > 3:
                raise ValueError("La taille (m) doit être un nombre positif (ex: 1.75).")
        self.height = height

# --- Fin de la définition de la classe ---


def submit_data():
    """
    Récupère les données des champs, tente de créer un UserProfile.
    Affiche un succès ou une erreur.
    """
    try:
        # 1. Récupérer les données des champs
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        
        # 2. Gérer les conversions de nombres (peut lever une ValueError)
        age = int(entry_age.get()) if entry_age.get() else None
        weight = float(entry_weight.get()) if entry_weight.get() else None
        height = float(entry_height.get()) if entry_height.get() else None

        # 3. Tenter de créer l'utilisateur
        user = UserProfile(
            first_name=first_name,
            last_name=last_name,
            age=age,
            weight=weight,
            height=height
        )

        # 4. Afficher un succès (message simplifié)
        messagebox.showinfo(
            "Succès",
            f"Utilisateur {user.first_name} créé avec succès!"
        )
        
    except ValueError as e:
        # 5. Afficher une erreur
        messagebox.showerror("Erreur de validation", str(e))

# --- Configuration de la fenêtre principale ---
root = tk.Tk()
root.title("Profil Utilisateur")

# --- Définition du style (THÈME BLEU) ---
BG_COLOR = "#D6EAF8"       # Bleu clair pour le fond
TEXT_COLOR = "#17202A"     # Noir/Bleu foncé pour le texte
BUTTON_BG = "#3498DB"      # Bleu vif pour le bouton
BUTTON_FG = "#FFFFFF"      # Blanc pour le texte du bouton
FONT_LABEL = ("Helvetica", 11)
FONT_ENTRY = ("Helvetica", 11)
FONT_BUTTON = ("Helvetica", 11, "bold")

# Appliquer la couleur de fond à la fenêtre principale
root.configure(bg=BG_COLOR)
# Empêcher la fenêtre d'être redimensionnée (optionnel, mais propre)
root.resizable(False, False)

# --- Cadre principal (pour l'espacement) ---
# On met tous les widgets dans ce cadre pour avoir une marge
main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
main_frame.pack(expand=True, fill="both")


# --- Création des widgets (Labels et Champs de saisie) ---
fields = {
    "Prénom": tk.StringVar(),
    "Nom": tk.StringVar(),
    "Âge": tk.StringVar(),
    "Poids (kg)": tk.StringVar(),
    "Taille (m)": tk.StringVar(),
}

row_index = 0
entries = {} 

for label_text, var in fields.items():
    # Label
    label = tk.Label(
        main_frame, 
        text=f"{label_text} :", 
        font=FONT_LABEL, 
        bg=BG_COLOR, 
        fg=TEXT_COLOR
    )
    label.grid(row=row_index, column=0, padx=10, pady=8, sticky="e")
    
    # Champ de saisie (Entry)
    entry = tk.Entry(
        main_frame, 
        textvariable=var, 
        width=40, 
        font=FONT_ENTRY,
        relief="flat",  # Style plus moderne
        bg="#FEFEFE"    # Fond blanc pour le champ
    )
    entry.grid(row=row_index, column=1, padx=10, pady=8)
    
    # Stocker les champs par leur nom
    if label_text == "Prénom": entries["first_name"] = entry
    if label_text == "Nom": entries["last_name"] = entry
    if label_text == "Âge": entries["age"] = entry
    if label_text == "Poids (kg)": entries["weight"] = entry
    if label_text == "Taille (m)": entries["height"] = entry
    
    row_index += 1

# Renommer les variables pour la fonction submit_data
entry_first_name = entries["first_name"]
entry_last_name = entries["last_name"]
entry_age = entries["age"]
entry_weight = entries["weight"]
entry_height = entries["height"]

# --- Bouton de soumission ---
submit_button = tk.Button(
    main_frame, 
    text="Enregistrer", 
    command=submit_data,
    font=FONT_BUTTON,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    relief="flat",       # Style moderne
    borderwidth=0,
    activebackground="#2874A6", # Couleur au clic
    activeforeground="#FFFFFF"
)
# Placer le bouton avec plus d'espace en dessous
submit_button.grid(row=row_index, column=1, pady=(20, 10), padx=10, sticky="e")

# --- Lancer l'application ---
root.mainloop()