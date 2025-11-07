# Fichier : us_journal.py (Journal d'Entraînement et Log de séries)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkFont
from datetime import date, datetime 
import csv 
import os.path 
import sys
from tkcalendar import Calendar

# --- VÉRIFICATION ET CHEMINS DES CSV ---
CSV_ENTRAINEMENT = os.path.join(os.path.dirname(__file__), "Entrainement.csv")
CSV_EXERCICE_LINKS = os.path.join(os.path.dirname(__file__), "Entrainement_Exercice.csv")
CSV_EXERCICE_MASTER = os.path.join(os.path.dirname(__file__), "Exercice_musculation.csv")
CSV_PERSONNE_EXO = os.path.join(os.path.dirname(__file__), "Personne_Exo.csv")
CSV_PERSONNE_ENTRAINEMENT = os.path.join(os.path.dirname(__file__), "Personne_Entrainement.csv")

# --- VARIABLES GLOBALES DU JOURNAL ---
root = None 
session_var = None
exercise_var = None 
weight_var = None
reps_var = None
training_date_var = None 
notes_text = None
notes_frame = None
log_frame = None
save_notes_btn = None
save_log_btn = None
weight_label = None
reps_label = None
exercise_combobox = None
weight_entry = None
reps_entry = None
training_date_entry = None
date_picker_btn = None
EXERCISE_NAMES_MAP = {}
SESSION_EXERCISE_LINKS = {}
SESSION_DATA = {}
MASTER_EXERCISE_LIST = []


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


# --- FONCTIONS UTILITAIRES DE CHARGEMENT CSV ---
# (Ces fonctions chargent les données au démarrage du module)

def load_exercise_master_list(filepath):
    exercise_names = {}
    try:
        with open(filepath, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            try: next(reader) 
            except StopIteration: return {}
            for row in reader:
                if not row: continue
                try:
                    exercise_id = row[0].strip()
                    exercise_titre = row[1].strip()
                    if exercise_id: exercise_names[exercise_id] = exercise_titre
                except IndexError: continue
    except Exception: return {}
    return exercise_names

def load_session_exercise_links(filepath):
    session_links = {}
    try:
        with open(filepath, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            try: next(reader) 
            except StopIteration: return {}
            for row in reader:
                if not row: continue
                try:
                    id_exercice = row[0].strip()
                    id_entrainement = row[1].strip()
                    series = row[2].strip()
                    repetitions = row[3].strip()
                    if not id_exercice or not id_entrainement: continue
                    if id_entrainement not in session_links:
                        session_links[id_entrainement] = []
                    session_links[id_entrainement].append({"id": id_exercice, "series": series, "reps": repetitions})
                except IndexError: continue
    except Exception: return {}
    return session_links

def load_sessions_from_csv(filepath, exercise_links, exercise_names_map):
    sessions = {}
    try:
        with open(filepath, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            try: next(reader)
            except StopIteration: return {}
            for row in reader:
                if not row: continue
                try:
                    id_entrainement = row[0].strip()
                    nom = row[1].strip()
                    type_ent = row[2].strip()
                    programme = row[3].strip()
                    temps = row[4].strip() if len(row) > 4 else ""
                    
                    session_key = f"{nom} : {type_ent} ({programme})"
                    exercise_data_list = []
                    seen_ids = set() 
                    exercise_details_for_this_session = exercise_links.get(id_entrainement, [])
                    
                    for ex_data in exercise_details_for_this_session: 
                        ex_id = ex_data["id"]
                        if ex_id in seen_ids: continue
                        seen_ids.add(ex_id)
                        exercise_name = exercise_names_map.get(ex_id, f"Exercice inconnu (ID: {ex_id})")
                        
                        full_exercise_info = {
                            "id": ex_id, "name": exercise_name, "series": ex_data["series"], "reps": ex_data["reps"]
                        }
                        exercise_data_list.append(full_exercise_info)
                        
                    sessions[session_key] = {
                        "exercises": exercise_data_list,
                        "csv_id": id_entrainement, 
                        "csv_programme": programme,
                        "csv_temps_moyen": temps
                    }
                except IndexError: continue
    except Exception: return {}
    return sessions

# --- CHARGEMENT DES DONNÉES AU DÉMARRAGE DU MODULE ---
EXERCISE_NAMES_MAP = load_exercise_master_list(CSV_EXERCICE_MASTER)
SESSION_EXERCISE_LINKS = load_session_exercise_links(CSV_EXERCICE_LINKS)
SESSION_DATA = load_sessions_from_csv(CSV_ENTRAINEMENT, SESSION_EXERCISE_LINKS, EXERCISE_NAMES_MAP)
MASTER_EXERCISE_LIST = sorted(list(set(EXERCISE_NAMES_MAP.values())))


# --- FONCTIONS HELPER POUR LES ID CSV (Ajoutées) ---

def get_next_personne_exo_id():
    """Vérifie Personne_Exo.csv, lit l'ID le plus haut et retourne max_id + 1."""
    HEADER = ['id_personne_exo', 'date', 'id_exercice', 'poids', 'id_user']
    file_exists = os.path.exists(CSV_PERSONNE_EXO)
    
    if not file_exists:
        try:
            with open(CSV_PERSONNE_EXO, mode='w', newline='', encoding='utf-8') as file:
                csv.writer(file, delimiter=';').writerow(HEADER)
            return 1
        except IOError as e:
            messagebox.showerror("Erreur Fichier", f"Impossible de créer {CSV_PERSONNE_EXO}.\n{e}")
            return -1

    max_id = 0
    try:
        with open(CSV_PERSONNE_EXO, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            try: next(reader) 
            except StopIteration: return 1
            for row in reader:
                if row and row[0].isdigit():
                    max_id = max(max_id, int(row[0]))
        return max_id + 1
    except IOError as e:
        messagebox.showerror("Erreur Fichier", f"Impossible de lire {CSV_PERSONNE_EXO}.\n{e}")
        return -1
    except Exception:
        return -1 # Erreur générique

def get_next_personne_entrainement_id():
    """Vérifie Personne_Entrainement.csv, lit l'ID le plus haut et retourne max_id + 1."""
    HEADER = ['cle_id', 'id_user', 'date_entrainement', 'id_entrainement', 'note']
    file_exists = os.path.exists(CSV_PERSONNE_ENTRAINEMENT)
    
    if not file_exists:
        try:
            with open(CSV_PERSONNE_ENTRAINEMENT, mode='w', newline='', encoding='utf-8') as file:
                csv.writer(file, delimiter=';').writerow(HEADER)
            return 1
        except IOError as e:
            messagebox.showerror("Erreur Fichier", f"Impossible de créer {CSV_PERSONNE_ENTRAINEMENT}.\n{e}")
            return -1

    max_id = 0
    try:
        with open(CSV_PERSONNE_ENTRAINEMENT, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            try: next(reader)
            except StopIteration: return 1
            for row in reader:
                if row and row[0].isdigit():
                    max_id = max(max_id, int(row[0]))
        return max_id + 1
    except IOError as e:
        messagebox.showerror("Erreur Fichier", f"Impossible de lire {CSV_PERSONNE_ENTRAINEMENT}.\n{e}")
        return -1
    except Exception:
        return -1 # Erreur générique

# --- FONCTION DE NOTIFICATION DE PROGRESSION (Ajoutée) ---
def notify_if_progress(user_id, id_exercice, exercise_name, new_poids, root_window):
    """
    Trouve le POIDS MAX précédent pour un user/exercice et affiche une alerte 
    si le new_poids est un record personnel.
    """
    max_previous_poids = 0.0
    
    if not os.path.exists(CSV_PERSONNE_EXO):
        return 

    try:
        new_poids_float = float(new_poids)
    except ValueError:
        print("Erreur: Le nouveau poids n'est pas un nombre valide.")
        return 

    try:
        with open(CSV_PERSONNE_EXO, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                if row.get('id_user') == str(user_id) and row.get('id_exercice') == str(id_exercice):
                    try:
                        current_poids = float(row.get('poids', 0))
                        if current_poids > max_previous_poids:
                            max_previous_poids = current_poids
                    except (ValueError, TypeError):
                        continue 

        if new_poids_float > max_previous_poids and max_previous_poids > 0:
            messagebox.showinfo(
                "Nouveau Record Personnel !",
                f"Bravo ! Vous avez battu votre record sur : {exercise_name}\n\n"
                f"Ancien record : {max_previous_poids} kg\n"
                f"Nouveau record : {new_poids_float} kg",
                parent=root_window
            )
        elif max_previous_poids == 0 and new_poids_float > 0:
             print(f"Première fois pour {exercise_name}. Pas de record à battre.")
        
    except Exception as e:
        print(f"Erreur lors de la vérification de progression : {e}")

# --- FONCTIONS LOGIQUES ET UI (Définies avant run_training_journal) ---

def open_date_picker_for_note():
    """Ouvre un petit calendrier popup pour choisir la date de la note."""
    popup = tk.Toplevel(root)
    popup.title("Choisir une date")
    popup.geometry("300x300")
    popup.configure(bg=FRAME_BG)
    popup.resizable(False, False)
    popup.transient(root); popup.grab_set()

    try:
        default_date = datetime.strptime(training_date_var.get(), '%Y-%m-%d').date()
    except ValueError:
        default_date = date.today()

    cal = Calendar(
        popup, selectmode='day',
        year=default_date.year, month=default_date.month, day=default_date.day,
        date_pattern='yyyy-mm-dd'
    )
    cal.pack(fill="both", expand=True, padx=10, pady=10)

    def on_click(event):
        training_date_var.set(cal.get_date())
        popup.destroy()

    cal.bind("<<CalendarSelected>>", on_click)
    root.wait_window(popup)

def get_all_logged_dates(user_id):
    logged_dates = set()
    if not os.path.exists(CSV_PERSONNE_EXO): return logged_dates 
    try:
        with open(CSV_PERSONNE_EXO, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                if row.get('id_user') == str(user_id):
                    date_str = row.get('date')
                    if date_str:
                        try:
                            datetime.strptime(date_str, '%Y-%m-%d')
                            logged_dates.add(date_str)
                        except ValueError: continue 
    except Exception as e:
        print(f"Erreur en lisant les dates de log : {e}")
    return logged_dates

def show_sessions_for_date(selected_date_iso, user_id):
    logs_on_this_day = []
    if os.path.exists(CSV_PERSONNE_EXO):
        try:
            with open(CSV_PERSONNE_EXO, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    if row.get('date') == selected_date_iso and row.get('id_user') == str(user_id):
                        exo_id = row.get('id_exercice')
                        exo_name = EXERCISE_NAMES_MAP.get(exo_id, f"ID Exercice: {exo_id}")
                        
                        log_info = {"name": exo_name, "poids": row.get('poids', 'N/A')}
                        logs_on_this_day.append(log_info)
        except Exception as e:
            messagebox.showerror("Erreur Lecture", f"Impossible de lire {CSV_PERSONNE_EXO}.\n{e}", parent=root)
            return
    
    popup = tk.Toplevel(root)
    popup.title(f"Logs du {selected_date_iso}")
    popup.geometry("400x300")
    popup.configure(bg=FRAME_BG)
    popup.resizable(False, False)
    popup.transient(root); popup.grab_set()

    text_frame = tk.Frame(popup, bg=FRAME_BG, padx=10, pady=10)
    text_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")
    info_text = tk.Text(text_frame, font=FONT_LABEL, bg=BG_COLOR, relief="flat", wrap="word", yscrollcommand=scrollbar.set)
    info_text.pack(fill="both", expand=True)
    scrollbar.config(command=info_text.yview)

    info_text.tag_configure("title", font=("Helvetica", 12, "bold"), spacing3=5)
    info_text.tag_configure("info", font=FONT_LABEL, lmargin1=10)

    if not logs_on_this_day:
        info_text.insert(tk.END, "Aucune série enregistrée pour ce jour.", "info")
    else:
        info_text.insert(tk.END, f"Séries enregistrées le {selected_date_iso}:\n", "title")
        for log in logs_on_this_day:
            info_text.insert(tk.END, f"• {log['name']} : {log['poids']} kg\n", "info")
            
    info_text.config(state="disabled")
    root.wait_window(popup)

def open_calendar_popup(user_id):
    """
    Ouvre un calendrier et marque les jours loggés (CORRECTION: Prend user_id).
    """
    popup = tk.Toplevel(root)
    popup.title("Calendrier des Logs") 
    popup.geometry("400x400")
    popup.configure(bg=FRAME_BG)
    popup.resizable(False, False)
    popup.transient(root); popup.grab_set()

    all_dates_logged = get_all_logged_dates(user_id) 
    
    display_date = date.today()
    if all_dates_logged:
         try:
             latest_date_str = max(all_dates_logged)
             display_date = datetime.strptime(latest_date_str, '%Y-%m-%d').date()
         except Exception:
             pass 

    cal = Calendar(
        popup, selectmode='day',
        year=display_date.year, month=display_date.month, day=display_date.day,
        date_pattern='yyyy-mm-dd',
        background=BUTTON_BG, foreground="white", headersbackground=BUTTON_BG, headersforeground="white", 
        selectbackground=BUTTON_BG, selectforeground="white", normalbackground=FRAME_BG, 
        normalforeground=TEXT_COLOR, othermonthbackground=BG_COLOR, othermonthforeground=TEXT_COLOR, 
        othermonthwebackground=BG_COLOR, othermonthweforeground=TEXT_COLOR, weekendbackground=FRAME_BG, 
        weekendforeground=TEXT_COLOR
    )
    cal.pack(fill="both", expand=True, padx=10, pady=10)

    cal.tag_config('log', background=BUTTON_BG, foreground='white') 
    
    for date_str in all_dates_logged:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            cal.calevent_create(date_obj, 'Log', 'log') 
        except ValueError:
            continue 

    def on_date_clicked(event):
        selected_date_iso = cal.get_date() 
        show_sessions_for_date(selected_date_iso, user_id) 

    cal.bind("<<CalendarSelected>>", on_date_clicked)
    root.wait_window(popup)


# --- FONCTIONS LOGIQUES D'ÉVÉNEMENT ---

def on_exercise_selected(event): 
    """
    Appelée quand l'utilisateur choisit un EXERCICE.
    """
    session_name = session_var.get()
    if not session_name: return

    selected_exercise_name = exercise_var.get()
    if not selected_exercise_name: return

    try:
        session_data = SESSION_DATA[session_name]
        exercise_data_list = session_data.get('exercises', [])
        found_reps = ""
        for exo_info in exercise_data_list:
            if exo_info["name"] == selected_exercise_name:
                found_reps = exo_info.get("reps", "") 
                break
        
        reps_var.set(found_reps)
        reps_entry.config(state="normal") 
        reps_entry.config(readonlybackground=BG_COLOR) # Assure que le fond reste gris

    except KeyError as e:
        print(f"Erreur: Séance '{session_name}' non trouvée dans on_exercise_selected: {e}")

def on_session_selected(event): 
    """
    Appelée quand l'utilisateur choisit une SÉANCE.
    """
    session_name = session_var.get()
    if not session_name: return
    try: data = SESSION_DATA[session_name]
    except KeyError: return
    
    # Activation des sections
    notes_frame.config(text="Détails de la Séance")
    notes_text.config(state="normal")
    save_notes_btn.config(state="normal")
    log_frame.config(text="Log d'Exercice")
    exercise_combobox.config(state="readonly")
    weight_label.config(state="normal")
    reps_label.config(state="normal")
    weight_entry.config(state="normal")
    reps_entry.config(state="disabled") # Reste désactivé jusqu'à sélection d'exo
    save_log_btn.config(state="normal")
    training_date_entry.config(state="normal")
    date_picker_btn.config(state="normal")

    notes_text.delete("1.0", "end")
    notes_text.insert("1.0", "") # Ne pré-remplit plus les notes
    
    exercise_data_list = data.get('exercises', [])
    exercise_names_list = [exo_info["name"] for exo_info in exercise_data_list]
    exercise_combobox['values'] = exercise_names_list
    
    exercise_var.set("")
    weight_var.set("")
    reps_var.set("")
    weight_entry.focus()


def save_notes(user_id):
    """Sauvegarde les notes de la séance pour l'utilisateur."""
    session_name = session_var.get()
    if not session_name: 
        messagebox.showwarning("Aucune séance", "Veuillez d'abord sélectionner une séance.")
        return
    training_date = training_date_var.get()
    new_notes = notes_text.get("1.0", "end-1c").strip()
    if not training_date:
        messagebox.showwarning("Date manquante", "Veuillez choisir une date pour cet entraînement.")
        return
    try: datetime.strptime(training_date, '%Y-%m-%d')
    except ValueError:
        messagebox.showwarning("Format de date invalide", "Veuillez entrer une date au format AAAA-MM-JJ.")
        return
    if not new_notes:
        messagebox.showwarning("Note vide", "Veuillez écrire une note avant de sauvegarder.")
        return
    try:
        id_entrainement = SESSION_DATA[session_name]['csv_id']
    except KeyError:
        messagebox.showerror("Erreur de Séance", "Impossible de trouver l'ID de la séance sélectionnée.")
        return
    
    cle_id = get_next_personne_entrainement_id()
    if cle_id == -1: return 
    new_row = [cle_id, user_id, training_date, id_entrainement, new_notes]
    try:
        with open(CSV_PERSONNE_ENTRAINEMENT, mode='a', newline='', encoding='utf-8') as file:
            csv.writer(file, delimiter=';').writerow(new_row)
        messagebox.showinfo("Sauvegardé", "Votre note d'entraînement a été enregistrée avec succès.")
    except IOError as e:
        messagebox.showerror("Erreur Sauvegarde", f"Impossible d'écrire dans {CSV_PERSONNE_ENTRAINEMENT}.\n{e}")

def save_exercise_log(user_id):
    """Sauvegarde le log de l'exercice pour l'utilisateur."""
    session_name = session_var.get()
    exercise_name = exercise_var.get()
    weight = weight_var.get()
    reps = reps_var.get()
    if not session_name or not exercise_name or not weight or not reps:
        messagebox.showwarning("Champs manquants", "Veuillez sélectionner un exercice et remplir le Poids/Répétitions.")
        return
    current_date = date.today().isoformat()
    exo_id_to_save = None
    try:
        exercise_data_list = SESSION_DATA[session_name]['exercises']
        for exo_info in exercise_data_list:
            if exo_info["name"] == exercise_name:
                exo_id_to_save = exo_info["id"]
                break
    except KeyError:
        messagebox.showerror("Erreur", "Séance non trouvée. Impossible de sauvegarder.")
        return
    if exo_id_to_save is None:
        messagebox.showerror("Erreur", f"Impossible de trouver l'ID pour l'exercice '{exercise_name}'.")
        return
    
    notify_if_progress(user_id, exo_id_to_save, exercise_name, weight, root)
    next_id = get_next_personne_exo_id()
    if next_id == -1: return
        
    new_row_data = [next_id, current_date, exo_id_to_save, weight, user_id]
    
    try:
        with open(CSV_PERSONNE_EXO, mode='a', newline='', encoding='utf-8') as file:
            csv.writer(file, delimiter=';').writerow(new_row_data)
        messagebox.showinfo("Série enregistrée", f"{exercise_name}: {weight}kg x {reps} reps\nSérie enregistrée avec succès !")
        weight_var.set("")
        weight_entry.focus()
    except IOError as e:
        messagebox.showerror("Erreur Sauvegarde", f"Impossible d'écrire dans {CSV_PERSONNE_EXO}.\n{e}")
        

def run_training_journal(root_window, switch_back_callback, user_data):
    """
    Fonction principale pour l'affichage du Journal d'Entraînement.
    """
    global root, session_var, exercise_var, weight_var, reps_var, training_date_var
    global exercise_combobox, weight_entry, reps_entry
    global notes_text, notes_frame, log_frame, save_notes_btn, save_log_btn, weight_label, reps_label
    global training_date_entry, date_picker_btn

    root = root_window 
    user_id = user_data['id_user'] 
    
    # Nettoyage
    for w in root.winfo_children():
        w.destroy()

    root.title("Journal d'Entraînement")
    root.geometry("600x740") 
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)

    # Variables de contrôle
    session_var = tk.StringVar()
    exercise_var = tk.StringVar()
    weight_var = tk.StringVar()
    reps_var = tk.StringVar()
    training_date_var = tk.StringVar(value=date.today().isoformat())

    main_frame = tk.Frame(root_window, bg=BG_COLOR, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    # --- Cadre d'en-tête ---
    header_frame = tk.Frame(main_frame, bg=BG_COLOR)
    header_frame.pack(fill="x", anchor="n")
    calendar_btn = tk.Button(
        header_frame, text="Recherche une séance", command=lambda: open_calendar_popup(user_id), 
        font=FONT_LINK, fg=TEXT_COLOR, bg=BG_COLOR, relief="flat", borderwidth=0,
        activeforeground=BUTTON_BG, activebackground=BG_COLOR
    )
    calendar_btn.pack(side="right", pady=5, padx=5)

    # --- 1. SÉLECTION DE LA SÉANCE ---
    tk.Label(main_frame, text="Choisir une séance :", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(10, 10))
    session_combobox = ttk.Combobox(
        main_frame, textvariable=session_var, font=FONT_LABEL,
        state="readonly", values=list(SESSION_DATA.keys()) 
    )
    session_combobox.pack(fill="x", ipady=5)
    session_combobox.bind("<<ComboboxSelected>>", on_session_selected) 

    # --- 2. DÉTAILS DE LA SÉANCE (DÉSACTIVÉ PAR DÉFAUT) ---
    notes_frame = ttk.LabelFrame(main_frame, text="Détails de la Séance (sélectionnez une séance)", padding=15)
    notes_frame.pack(fill="x", pady=20)

    date_picker_frame = tk.Frame(notes_frame, bg=FRAME_BG)
    date_picker_frame.pack(fill="x", anchor="w")

    tk.Label(date_picker_frame, text="Date de l'entraînement :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR).pack(side="left", padx=(0, 5))
    training_date_entry = tk.Entry(date_picker_frame, textvariable=training_date_var, font=FONT_LABEL, relief="flat", state="disabled", width=12)
    training_date_entry.pack(side="left", padx=5)
    date_picker_btn = tk.Button(
        date_picker_frame, text="📅", command=open_date_picker_for_note, font=FONT_LABEL,
        relief="flat", bg=FRAME_BG, fg=TEXT_COLOR, activebackground=FRAME_BG, 
        activeforeground=BUTTON_BG, borderwidth=0, state="disabled"
    )
    date_picker_btn.pack(side="left")

    tk.Label(notes_frame, text="Notes personnelles :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR).pack(anchor="w", pady=(10, 5))
    notes_text = tk.Text(notes_frame, height=6, font=FONT_LABEL, relief="flat", bg=BG_COLOR, state="disabled")
    notes_text.pack(fill="x")
    save_notes_btn = tk.Button(
        notes_frame, text="Sauvegarder les notes", command=lambda: save_notes(user_id), font=FONT_BUTTON,
        bg=BUTTON_BG, fg=BUTTON_FG, relief="flat", state="disabled"
    )
    save_notes_btn.pack(anchor="e", pady=(10, 0))

    # --- 3. LOG D'EXERCICE (DÉSACTIVÉ PAR DÉFAUT) ---
    log_frame = ttk.LabelFrame(main_frame, text="Log d'Exercice (sélectionnez une séance)", padding=15)
    log_frame.pack(fill="x", pady=(20, 0)) 
    tk.Label(log_frame, text="Choisir un exercice :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR).pack(anchor="w")
    exercise_combobox = ttk.Combobox(log_frame, textvariable=exercise_var, font=FONT_LABEL, state="disabled")
    exercise_combobox.pack(fill="x", ipady=5, pady=(5, 15))
    exercise_combobox.bind("<<ComboboxSelected>>", on_exercise_selected) 

    log_grid_frame = tk.Frame(log_frame, bg=FRAME_BG)
    log_grid_frame.pack(fill="x")
    log_grid_frame.columnconfigure((0, 1), weight=1)
    weight_label = tk.Label(log_grid_frame, text="Poids (kg) :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR, state="disabled")
    weight_label.grid(row=0, column=0, sticky="w")
    weight_entry = tk.Entry(log_grid_frame, textvariable=weight_var, font=FONT_LABEL, relief="flat", state="disabled")
    weight_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))
    reps_label = tk.Label(log_grid_frame, text="Répétitions :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR, state="disabled")
    reps_label.grid(row=0, column=1, sticky="w")
    reps_entry = tk.Entry(log_grid_frame, textvariable=reps_var, font=FONT_LABEL, relief="flat", state="disabled", readonlybackground=BG_COLOR )
    reps_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0))

    save_log_btn = tk.Button(
        log_frame, text="Enregistrer la série", command=lambda: save_exercise_log(user_id), font=FONT_BUTTON,
        bg=BUTTON_BG, fg=BUTTON_FG, relief="flat", state="disabled"
    )
    save_log_btn.pack(anchor="e", pady=(20, 0))

    # --- 4. Bouton de retour ---
    tk.Button(root_window, text="⬅️ Retour Menu Principal", command=lambda: switch_back_callback(user_data)).pack(pady=15)


# --- Test isolés ---
if __name__ == '__main__':
    def dummy_menu_callback(data_recue):
        print(f"Retour Menu! Données: {data_recue}")
        sys.exit()

    root = tk.Tk()
    dummy_user_data = {'id_user': '1', 'pseudo': 'TestUser'}
    run_training_journal(root, dummy_menu_callback, dummy_user_data)
    root.mainloop()