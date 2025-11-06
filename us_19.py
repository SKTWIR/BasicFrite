import tkinter as tk
from tkinter import ttk  # On utilise ttk pour des widgets plus modernes
from tkinter import messagebox
from tkinter import font as tkFont
from datetime import date # Pour pré-remplir la date du jour

# --- BASE DE DONNÉES FICTIVE ---
SESSION_DATA = {
    "Séance A: Pectoraux / Triceps": {
        "date": "2025-11-05",
        "notes": "Bonne séance, un peu fatigué sur les dips.",
        "exercises": [
            "Développé Couché",
            "Dips (lestés)",
            "Écartés à la poulie",
            "Extensions Triceps (corde)"
        ]
    },
    "Séance B: Jambes / Mollets": {
        "date": "2025-11-06",
        "notes": "Ne pas oublier de s'échauffer les genoux la prochaine fois !",
        "exercises": [
            "Squat (Barre haute)",
            "Presse à cuisse",
            "Leg Extensions",
            "Soulevé de Terre Roumain (Haltères)",
            "Extensions Mollets (debout)"
        ]
    },
    "Séance C: Dos / Biceps": {
        "date": "2025-11-07",
        "notes": "", # Notes vides à remplir
        "exercises": [
            "Tractions (pronation)",
            "Rowing Buste Penché (Barre)",
            "Tirage Vertical (prise large)",
            "Curl Biceps (Haltères)"
        ]
    }
}

# --- NOUVEAU : LISTE MAÎTRESSE DES EXERCICES ---
# C'est la liste de TOUS les exercices que vous pouvez choisir
MASTER_EXERCISE_LIST = sorted([
    "Développé Couché", "Dips (lestés)", "Écartés à la poulie",
    "Extensions Triceps (corde)", "Squat (Barre haute)", "Presse à cuisse",
    "Leg Extensions", "Soulevé de Terre Roumain (Haltères)", "Extensions Mollets (debout)",
    "Tractions (pronation)", "Rowing Buste Penché (Barre)", "Tirage Vertical (prise large)",
    "Curl Biceps (Haltères)", "Soulevé de Terre (classique)", "Fentes (Haltères)",
    "Rowing (Haltère unilatéral)", "Développé Militaire (Barre)", "Élévations latérales",
    "Curl Incliné (Haltères)", "Oiseau (Haltères)"
])
# --- Fin de la liste maîtresse ---


# --- Définition du style ---
BG_COLOR = "#D6EAF8"
FRAME_BG = "#EBF5FB"
TEXT_COLOR = "#17202A"
BUTTON_BG = "#3498DB"
BUTTON_FG = "#FFFFFF"
FONT_TITLE = ("Helvetica", 14, "bold")
FONT_LABEL = ("Helvetica", 11)
FONT_BUTTON = ("Helvetica", 11, "bold")


# --- FONCTIONS LOGIQUES EXISTANTES ---

def on_session_selected(event):
    # (Code inchangé)
    session_name = session_var.get()
    if not session_name:
        return
    try:
        data = SESSION_DATA[session_name]
    except KeyError:
        return

    notes_frame.config(text="Détails de la Séance")
    notes_text.config(state="normal")
    save_notes_btn.config(state="normal")
    log_frame.config(text="Log d'Exercice")
    exercise_combobox.config(state="readonly")
    weight_label.config(state="normal")
    reps_label.config(state="normal")
    weight_entry.config(state="normal")
    reps_entry.config(state="normal")
    save_log_btn.config(state="normal")
    date_var.set(f"Date de la séance : {data['date']}")
    notes_text.delete("1.0", "end")
    notes_text.insert("1.0", data['notes'])
    exercise_combobox['values'] = data['exercises']
    exercise_var.set("")
    weight_var.set("")
    reps_var.set("")

def save_notes():
    # (Code inchangé)
    session_name = session_var.get()
    if not session_name:
        messagebox.showwarning("Aucune séance", "Veuillez d'abord sélectionner une séance.")
        return
    new_notes = notes_text.get("1.0", "end-1c")
    SESSION_DATA[session_name]['notes'] = new_notes
    print(f"Notes pour '{session_name}' sauvegardées :\n{new_notes}")
    messagebox.showinfo("Sauvegardé", "Vos notes ont été enregistrées avec succès.")

def save_exercise_log():
    # (Code inchangé)
    session = session_var.get()
    exercise = exercise_var.get()
    weight = weight_var.get()
    reps = reps_var.get()
    if not session or not exercise or not weight or not reps:
        messagebox.showwarning("Champs manquants", "Veuillez sélectionner un exercice et remplir les champs 'Poids' et 'Répétitions'.")
        return
    print(f"--- LOG SAUVEGARDÉ ---\n  Séance  : {session}\n  Exercice: {exercise}\n  Poids   : {weight} kg\n  Reps    : {reps}\n------------------------")
    messagebox.showinfo("Série enregistrée", f"{exercise}: {weight}kg x {reps} reps\nSérie enregistrée !")
    weight_var.set("")
    reps_var.set("")
    weight_entry.focus()

# --- NOUVELLES FONCTIONS POUR LA CRÉATION DE SÉANCE ---

def handle_save_new_session(popup_window, name_entry, date_entry, exo_listbox):
    """
    Valide et enregistre la nouvelle séance depuis le pop-up.
    """
    # 1. Récupérer les données
    session_name = name_entry.get()
    session_date = date_entry.get()
    
    # Récupérer les indices des items sélectionnés dans la Listbox
    selected_indices = exo_listbox.curselection()
    # Créer la liste des noms d'exercices
    selected_exercises = [exo_listbox.get(i) for i in selected_indices]
    
    # 2. Validation
    if not session_name:
        messagebox.showerror("Erreur", "Veuillez donner un nom à votre séance.", parent=popup_window)
        return
    if session_name in SESSION_DATA:
        messagebox.showerror("Erreur", "Une séance avec ce nom existe déjà.", parent=popup_window)
        return
    if not session_date:
        messagebox.showerror("Erreur", "Veuillez entrer une date.", parent=popup_window)
        return
    if not selected_exercises:
        messagebox.showerror("Erreur", "Veuillez sélectionner au moins un exercice.", parent=popup_window)
        return
        
    # 3. Sauvegarder dans notre "BDD"
    SESSION_DATA[session_name] = {
        "date": session_date,
        "notes": "", # Notes vides par défaut
        "exercises": selected_exercises
    }
    
    # 4. Mettre à jour le Combobox principal
    session_combobox['values'] = list(SESSION_DATA.keys())
    
    # 5. Confirmer et fermer
    messagebox.showinfo("Succès", f"La séance '{session_name}' a été créée.", parent=popup_window)
    print(f"Nouvelle séance créée : {session_name}")
    popup_window.destroy()


def open_create_session_popup():
    """
    Ouvre la fenêtre pop-up pour créer une nouvelle séance.
    """
    # 1. Créer la fenêtre pop-up
    popup = tk.Toplevel(root)
    popup.title("Créer une nouvelle séance")
    popup.geometry("450x600")
    popup.configure(bg=FRAME_BG)
    popup.resizable(False, False)
    
    # Rendre la pop-up "modale"
    popup.transient(root)
    popup.grab_set()

    # Cadre principal du pop-up
    popup_frame = tk.Frame(popup, bg=FRAME_BG, padx=20, pady=20)
    popup_frame.pack(fill="both", expand=True)

    # --- Widgets du formulaire ---
    
    # Nom de la séance
    name_label = tk.Label(popup_frame, text="Nom de la séance :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
    name_label.pack(anchor="w")
    name_entry = tk.Entry(popup_frame, font=FONT_LABEL, relief="flat")
    name_entry.pack(fill="x", pady=(5, 15))

    # Date de la séance
    date_label = tk.Label(popup_frame, text="Date (AAAA-MM-JJ) :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
    date_label.pack(anchor="w")
    date_var = tk.StringVar(value=date.today().isoformat()) # Pré-remplir avec aujourd'hui
    date_entry = tk.Entry(popup_frame, textvariable=date_var, font=FONT_LABEL, relief="flat")
    date_entry.pack(fill="x", pady=(5, 15))

    # Sélection des exercices (Listbox)
    exo_label = tk.Label(popup_frame, text="Choisir les exercices :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
    exo_label.pack(anchor="w")
    
    # Cadre pour la Listbox et sa Scrollbar
    listbox_frame = tk.Frame(popup_frame)
    listbox_frame.pack(fill="both", expand=True, pady=(5, 15))
    
    exo_scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
    exo_listbox = tk.Listbox(
        listbox_frame,
        font=FONT_LABEL,
        selectmode=tk.MULTIPLE, # Permet la sélection multiple
        yscrollcommand=exo_scrollbar.set,
        relief="flat",
        bg=BG_COLOR
    )
    exo_scrollbar.config(command=exo_listbox.yview)
    
    exo_scrollbar.pack(side="right", fill="y")
    exo_listbox.pack(side="left", fill="both", expand=True)
    
    # Remplir la Listbox avec la liste maîtresse
    for exo in MASTER_EXERCISE_LIST:
        exo_listbox.insert(tk.END, exo)

    # --- Boutons (Enregistrer / Annuler) ---
    btn_frame = tk.Frame(popup_frame, bg=FRAME_BG)
    btn_frame.pack(fill="x")
    
    cancel_btn = tk.Button(
        btn_frame,
        text="Annuler",
        command=popup.destroy,
        font=FONT_BUTTON,
        bg="#AAAAAA", # Gris
        fg=BUTTON_FG,
        relief="flat"
    )
    cancel_btn.pack(side="right", padx=(10, 0))
    
    save_btn = tk.Button(
        btn_frame,
        text="Enregistrer",
        command=lambda: handle_save_new_session(popup, name_entry, date_entry, exo_listbox),
        font=FONT_BUTTON,
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        relief="flat"
    )
    save_btn.pack(side="right")


# --- FENÊTRE PRINCIPALE ---
root = tk.Tk()
root.title("Journal d'Entraînement")
root.geometry("600x800") # Augmenté la hauteur pour le nouveau bouton
root.configure(bg=BG_COLOR)
root.resizable(False, False)

main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# --- 1. SÉLECTION DE LA SÉANCE (Haut) ---
select_label = tk.Label(main_frame, text="Choisir une séance :", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
select_label.pack(pady=(0, 10))

session_var = tk.StringVar()
session_combobox = ttk.Combobox(
    main_frame,
    textvariable=session_var,
    font=FONT_LABEL,
    state="readonly",
    values=list(SESSION_DATA.keys())
)
session_combobox.pack(fill="x", ipady=5)
session_combobox.bind("<<ComboboxSelected>>", on_session_selected)


# --- 2. DÉTAILS DE LA SÉANCE (Milieu) ---
notes_frame = ttk.LabelFrame(main_frame, text="Détails de la Séance (sélectionnez une séance)", padding=15)
notes_frame.pack(fill="x", pady=20)

date_var = tk.StringVar(value="Date de la séance : N/A")
date_label = tk.Label(notes_frame, textvariable=date_var, font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
date_label.pack(anchor="w")

notes_label = tk.Label(notes_frame, text="Notes personnelles :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
notes_label.pack(anchor="w", pady=(10, 5))
notes_text = tk.Text(notes_frame, height=6, font=FONT_LABEL, relief="flat", bg=BG_COLOR, state="disabled")
notes_text.pack(fill="x")

save_notes_btn = tk.Button(
    notes_frame,
    text="Sauvegarder les notes",
    command=save_notes,
    font=FONT_BUTTON,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    relief="flat",
    state="disabled"
)
save_notes_btn.pack(anchor="e", pady=(10, 0))


# --- 3. LOG D'EXERCICE (Bas) ---
log_frame = ttk.LabelFrame(main_frame, text="Log d'Exercice (sélectionnez une séance)", padding=15)
log_frame.pack(fill="x")

log_exo_label = tk.Label(log_frame, text="Choisir un exercice :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
log_exo_label.pack(anchor="w")

exercise_var = tk.StringVar()
exercise_combobox = ttk.Combobox(
    log_frame,
    textvariable=exercise_var,
    font=FONT_LABEL,
    state="disabled"
)
exercise_combobox.pack(fill="x", ipady=5, pady=(5, 15))

log_grid_frame = tk.Frame(log_frame, bg=FRAME_BG)
log_grid_frame.pack(fill="x")
log_grid_frame.columnconfigure((0, 1), weight=1)

weight_label = tk.Label(log_grid_frame, text="Poids (kg) :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR, state="disabled")
weight_label.grid(row=0, column=0, sticky="w")
weight_var = tk.StringVar()
weight_entry = tk.Entry(log_grid_frame, textvariable=weight_var, font=FONT_LABEL, relief="flat", state="disabled")
weight_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))

reps_label = tk.Label(log_grid_frame, text="Répétitions :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR, state="disabled")
reps_label.grid(row=0, column=1, sticky="w")
reps_var = tk.StringVar()
reps_entry = tk.Entry(log_grid_frame, textvariable=reps_var, font=FONT_LABEL, relief="flat", state="disabled")
reps_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0))

save_log_btn = tk.Button(
    log_frame,
    text="Enregistrer la série",
    command=save_exercise_log,
    font=FONT_BUTTON,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    relief="flat",
    state="disabled"
)
save_log_btn.pack(anchor="e", pady=(20, 0))


# --- 4. AJOUT : BOUTON DE CRÉATION DE SÉANCE ---
separator = ttk.Separator(main_frame, orient="horizontal")
separator.pack(fill="x", pady=(30, 20)) # Séparateur visuel

create_session_btn = tk.Button(
    main_frame,
    text="Créer une nouvelle séance",
    command=open_create_session_popup,
    font=FONT_BUTTON,
    bg="#2ECC71", # Un bouton vert pour "Créer"
    fg=BUTTON_FG,
    relief="flat"
)
create_session_btn.pack(fill="x", ipady=8) # ipady = padding interne pour un bouton plus gros


# --- LANCEMENT DE L'APP ---
root.mainloop()