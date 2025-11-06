import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkFont
from datetime import date, datetime # Imports de date/datetime

# --- NOUVEL IMPORT REQUIS ---
try:
    from tkcalendar import Calendar
except ImportError:
    print("Erreur : La bibliothèque 'tkcalendar' est requise.")
    print("Veuillez l'installer avec : pip install tkcalendar")
    exit()

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
    },
    "Séance D: Mobilité / Abdos": {
        "date": "2025-11-07",
        "notes": "Session rapide post-travail.",
        "exercises": [
            "Planche (Gainage)",
            "Hanging Leg Raises",
            "Etirements (Chat-Vache)"
        ]
    }
}

# --- LISTE MAÎTRESSE DES EXERCICES ---
MASTER_EXERCISE_LIST = sorted([
    "Développé Couché", "Dips (lestés)", "Écartés à la poulie",
    "Extensions Triceps (corde)", "Squat (Barre haute)", "Presse à cuisse",
    "Leg Extensions", "Soulevé de Terre Roumain (Haltères)", "Extensions Mollets (debout)",
    "Tractions (pronation)", "Rowing Buste Penché (Barre)", "Tirage Vertical (prise large)",
    "Curl Biceps (Haltères)", "Soulevé de Terre (classique)", "Fentes (Haltères)",
    "Rowing (Haltère unilatéral)", "Développé Militaire (Barre)", "Élévations latérales",
    "Curl Incliné (Haltères)", "Oiseau (Haltères)", "Planche (Gainage)", 
    "Hanging Leg Raises", "Etirements (Chat-Vache)"
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
FONT_LINK = ("Helvetica", 10, "underline")


# --- FONCTIONS LOGIQUES EXISTANTES ---
# (Ces fonctions sont inchangées)
def on_session_selected(event):
    session_name = session_var.get()
    if not session_name: return
    try: data = SESSION_DATA[session_name]
    except KeyError: return
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
    session_name = session_var.get()
    if not session_name: messagebox.showwarning("Aucune séance", "Veuillez d'abord sélectionner une séance."); return
    new_notes = notes_text.get("1.0", "end-1c")
    SESSION_DATA[session_name]['notes'] = new_notes
    print(f"Notes pour '{session_name}' sauvegardées :\n{new_notes}")
    messagebox.showinfo("Sauvegardé", "Vos notes ont été enregistrées avec succès.")
def save_exercise_log():
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
def handle_save_new_session(popup_window, name_entry, date_entry, exo_listbox):
    session_name = name_entry.get()
    session_date = date_entry.get()
    selected_indices = exo_listbox.curselection()
    selected_exercises = [exo_listbox.get(i) for i in selected_indices]
    if not session_name: messagebox.showerror("Erreur", "Veuillez donner un nom à votre séance.", parent=popup_window); return
    if session_name in SESSION_DATA: messagebox.showerror("Erreur", "Une séance avec ce nom existe déjà.", parent=popup_window); return
    if not session_date: messagebox.showerror("Erreur", "Veuillez entrer une date.", parent=popup_window); return
    if not selected_exercises: messagebox.showerror("Erreur", "Veuillez sélectionner au moins un exercice.", parent=popup_window); return
    SESSION_DATA[session_name] = {"date": session_date, "notes": "", "exercises": selected_exercises}
    session_combobox['values'] = list(SESSION_DATA.keys())
    messagebox.showinfo("Succès", f"La séance '{session_name}' a été créée.", parent=popup_window)
    print(f"Nouvelle séance créée : {session_name}")
    popup_window.destroy()
def open_create_session_popup():
    popup = tk.Toplevel(root)
    popup.title("Créer une nouvelle séance")
    popup.geometry("450x600")
    popup.configure(bg=FRAME_BG)
    popup.resizable(False, False)
    popup.transient(root); popup.grab_set()
    popup_frame = tk.Frame(popup, bg=FRAME_BG, padx=20, pady=20)
    popup_frame.pack(fill="both", expand=True)
    name_label = tk.Label(popup_frame, text="Nom de la séance :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR); name_label.pack(anchor="w")
    name_entry = tk.Entry(popup_frame, font=FONT_LABEL, relief="flat"); name_entry.pack(fill="x", pady=(5, 15))
    date_label = tk.Label(popup_frame, text="Date (AAAA-MM-JJ) :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR); date_label.pack(anchor="w")
    date_var = tk.StringVar(value=date.today().isoformat()); date_entry = tk.Entry(popup_frame, textvariable=date_var, font=FONT_LABEL, relief="flat"); date_entry.pack(fill="x", pady=(5, 15))
    exo_label = tk.Label(popup_frame, text="Choisir les exercices :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR); exo_label.pack(anchor="w")
    listbox_frame = tk.Frame(popup_frame); listbox_frame.pack(fill="both", expand=True, pady=(5, 15))
    exo_scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
    exo_listbox = tk.Listbox(listbox_frame, font=FONT_LABEL, selectmode=tk.MULTIPLE, yscrollcommand=exo_scrollbar.set, relief="flat", bg=BG_COLOR)
    exo_scrollbar.config(command=exo_listbox.yview); exo_scrollbar.pack(side="right", fill="y"); exo_listbox.pack(side="left", fill="both", expand=True)
    for exo in MASTER_EXERCISE_LIST: exo_listbox.insert(tk.END, exo)
    btn_frame = tk.Frame(popup_frame, bg=FRAME_BG); btn_frame.pack(fill="x")
    cancel_btn = tk.Button(btn_frame, text="Annuler", command=popup.destroy, font=FONT_BUTTON, bg="#AAAAAA", fg=BUTTON_FG, relief="flat"); cancel_btn.pack(side="right", padx=(10, 0))
    save_btn = tk.Button(btn_frame, text="Enregistrer", command=lambda: handle_save_new_session(popup, name_entry, date_entry, exo_listbox), font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG, relief="flat"); save_btn.pack(side="right")


# --- FONCTIONS POUR LE CALENDRIER (MODIFIÉES/VÉRIFIÉES) ---

def show_sessions_for_date(selected_date_iso):
    """
    Affiche les séances pour une date spécifique (format AAAA-MM-JJ)
    """
    # 1. Trouver les séances pour cette date
    sessions_on_this_day = []
    for session_name, details in SESSION_DATA.items():
        if details['date'] == selected_date_iso:
            sessions_on_this_day.append({"name": session_name, "details": details})
            
    # 2. Ouvrir un pop-up pour afficher les résultats
    popup = tk.Toplevel(root)
    popup.title(f"Séances du {selected_date_iso}")
    popup.geometry("400x300")
    popup.configure(bg=FRAME_BG)
    popup.resizable(False, False)
    popup.transient(root); popup.grab_set()

    # Cadre avec scrollbar
    text_frame = tk.Frame(popup, bg=FRAME_BG, padx=10, pady=10)
    text_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")
    info_text = tk.Text(text_frame, font=FONT_LABEL, bg=BG_COLOR, relief="flat", wrap="word", yscrollcommand=scrollbar.set)
    info_text.pack(fill="both", expand=True)
    scrollbar.config(command=info_text.yview)

    # Définir les styles
    info_text.tag_configure("title", font=("Helvetica", 12, "bold"), spacing3=5)
    info_text.tag_configure("info", font=FONT_LABEL, lmargin1=10)
    info_text.tag_configure("notes", font=("Helvetica", 10, "italic"), lmargin1=10)

    if not sessions_on_this_day:
        info_text.insert(tk.END, "Aucune séance enregistrée pour ce jour.", "info")
    else:
        for session_info in sessions_on_this_day:
            session_name = session_info['name']
            details = session_info['details']
            
            info_text.insert(tk.END, f"• {session_name}\n", "title")
            info_text.insert(tk.END, "Exercices :\n", "info")
            for exo in details['exercises']:
                info_text.insert(tk.END, f"    - {exo}\n", "info")
            notes = details.get('notes', 'Aucune note.')
            if not notes: notes = "Aucune note."
            info_text.insert(tk.END, f"Notes : {notes}\n\n", "notes")
            
    info_text.config(state="disabled")
    
def open_calendar_popup():
    """
    Ouvre un pop-up avec un calendrier cliquable.
    """
    popup = tk.Toplevel(root)
    popup.title("Calendrier des Séances")
    popup.geometry("400x400")
    popup.configure(bg=FRAME_BG)
    popup.resizable(False, False)
    popup.transient(root); popup.grab_set()

    # --- Logique pour définir le mois d'affichage ---
    if SESSION_DATA:
        latest_date_str = max(details['date'] for details in SESSION_DATA.values())
        display_date = datetime.strptime(latest_date_str, '%Y-%m-%d').date()
    else:
        display_date = date.today()

    cal = Calendar(
        popup,
        selectmode='day',
        year=display_date.year,
        month=display_date.month,
        day=display_date.day,
        date_pattern='yyyy-mm-dd', # Important pour la compatibilité
        background=BUTTON_BG,
        foreground="white",
        headersbackground=BUTTON_BG,
        headersforeground="white",
        selectbackground=BUTTON_BG,
        selectforeground="white",
        normalbackground=FRAME_BG,
        normalforeground=TEXT_COLOR,
        othermonthbackground=BG_COLOR,
        othermonthforeground=TEXT_COLOR,
        othermonthwebackground=BG_COLOR,
        othermonthweforeground=TEXT_COLOR,
        weekendbackground=FRAME_BG,
        weekendforeground=TEXT_COLOR
    )
    cal.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Marquer les jours avec des séances ---
    cal.tag_config('session', background=BUTTON_BG, foreground='white')
    
    for session_name, details in SESSION_DATA.items():
        try:
            date_str = details['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # --- CORRECTION APPLIQUÉE ICI ---
            # cal.calendar_event_create est incorrect
            # Le nom correct de la méthode est cal.calevent_create
            cal.calevent_create(date_obj, 'Séance', 'session')
            
        except ValueError:
            print(f"Format de date invalide pour '{session_name}': {details['date']}")

    def on_date_clicked(event):
        """Fonction interne appelée par le clic sur le calendrier"""
        selected_date_iso = cal.get_date() 
        show_sessions_for_date(selected_date_iso)

    # Lier l'événement de sélection d'un jour
    cal.bind("<<CalendarSelected>>", on_date_clicked)


# --- FENÊTRE PRINCIPALE ---
root = tk.Tk()
root.title("Journal d'Entraînement")
root.geometry("600x800")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# --- Cadre d'en-tête (Nettoyé) ---
header_frame = tk.Frame(main_frame, bg=BG_COLOR)
header_frame.pack(fill="x", anchor="n")

# Bouton Calendrier (MAINTENANT LE SEUL BOUTON D'HISTORIQUE)
calendar_btn = tk.Button(
    header_frame,
    text="Calendrier 📅",
    command=open_calendar_popup,
    font=FONT_LINK,
    fg=TEXT_COLOR,
    bg=BG_COLOR,
    relief="flat",
    borderwidth=0,
    activeforeground=BUTTON_BG,
    activebackground=BG_COLOR
)
calendar_btn.pack(side="right", pady=5, padx=5)

# LE BOUTON "HISTORIQUE 📜" A ÉTÉ SUPPRIMÉ


# --- 1. SÉLECTION DE LA SÉANCE (Haut) ---
select_label = tk.Label(main_frame, text="Choisir une séance :", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
select_label.pack(pady=(10, 10))
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
    notes_frame, text="Sauvegarder les notes", command=save_notes, font=FONT_BUTTON,
    bg=BUTTON_BG, fg=BUTTON_FG, relief="flat", state="disabled"
)
save_notes_btn.pack(anchor="e", pady=(10, 0))


# --- 3. LOG D'EXERCICE (Bas) ---
log_frame = ttk.LabelFrame(main_frame, text="Log d'Exercice (sélectionnez une séance)", padding=15)
log_frame.pack(fill="x")
log_exo_label = tk.Label(log_frame, text="Choisir un exercice :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
log_exo_label.pack(anchor="w")
exercise_var = tk.StringVar()
exercise_combobox = ttk.Combobox(log_frame, textvariable=exercise_var, font=FONT_LABEL, state="disabled")
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
    log_frame, text="Enregistrer la série", command=save_exercise_log, font=FONT_BUTTON,
    bg=BUTTON_BG, fg=BUTTON_FG, relief="flat", state="disabled"
)
save_log_btn.pack(anchor="e", pady=(20, 0))


# --- 4. BOUTON DE CRÉATION DE SÉANCE ---
separator = ttk.Separator(main_frame, orient="horizontal")
separator.pack(fill="x", pady=(30, 20)) 
create_session_btn = tk.Button(
    main_frame,
    text="Créer une nouvelle séance",
    command=open_create_session_popup,
    font=FONT_BUTTON,
    bg="#2ECC71",
    fg=BUTTON_FG,
    relief="flat"
)
create_session_btn.pack(fill="x", ipady=8)


# --- LANCEMENT DE L'APP ---
root.mainloop()