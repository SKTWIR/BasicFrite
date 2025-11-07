import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkFont
from datetime import date, datetime 
import csv 
import os.path 

# --- NOUVEL IMPORT REQUIS ---
try:
    from tkcalendar import Calendar
except ImportError:
    print("Erreur : La bibliothèque 'tkcalendar' est requise.")
    print("Veuillez l'installer avec : pip install tkcalendar")
    exit()

# --- VÉRIFICATION ET CHEMINS DES CSV ---
CSV_ENTRAINEMENT = "Entrainement.csv"
CSV_EXERCICE_LINKS = "Entrainement_Exercice.csv"
CSV_EXERCICE_MASTER = "Exercice_musculation.csv"
CSV_PERSONNE_EXO = "Personne_Exo.csv" # <-- AJOUTÉ : Fichier de log des séries

# Vérification que tous les fichiers nécessaires existent
fichiers_manquants = []
# On ne vérifie que les fichiers "source", pas le fichier de log qui sera créé
for f in [CSV_ENTRAINEMENT, CSV_EXERCICE_LINKS, CSV_EXERCICE_MASTER]:
    if not os.path.exists(f):
        fichiers_manquants.append(f)

if fichiers_manquants:
    message = f"Les fichiers CSV suivants sont introuvables :\n\n" + "\n".join(fichiers_manquants)
    message += "\n\nVeuillez vous assurer qu'ils sont dans le même dossier que le script."
    print(message)
    messagebox.showerror("Fichiers Manquants", message)
    exit()


# --- NOUVELLES FONCTIONS DE CHARGEMENT ---

def load_exercise_master_list(filepath):
    """
    Étape 1: Charge Exercice_musculation.csv dans un dictionnaire.
    Retourne un map: { 'id': 'Titre', ... }
    """
    exercise_names = {}
    try:
        with open(filepath, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            try:
                header = next(reader) 
            except StopIteration:
                return {}
            for row in reader:
                if not row: continue
                try:
                    exercise_id = row[0].strip()
                    exercise_titre = row[1].strip()
                    if exercise_id:
                        exercise_names[exercise_id] = exercise_titre
                except IndexError:
                    print(f"Erreur: Ligne mal formatée dans {filepath} : {row}")
    except Exception as e:
        messagebox.showerror("Erreur CSV", f"Impossible de lire {filepath}.\nErreur: {e}")
        return {}
    return exercise_names

def load_session_exercise_links(filepath):
    """
    Étape 2: MODIFIÉE
    Charge Entrainement_Exercice.csv pour lier les séances aux exercices.
    Retourne un map: { 'id_entrainement': [ {'id': 'id_ex', 'series': 's', 'reps': 'r'}, ... ] }
    """
    session_links = {}
    try:
        with open(filepath, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            try:
                header = next(reader) 
            except StopIteration:
                return {}
            for row in reader:
                if not row: continue
                try:
                    # --- NOUVEAU : Lecture des séries et répétitions ---
                    id_exercice = row[0].strip()
                    id_entrainement = row[1].strip()
                    series = row[2].strip()
                    repetitions = row[3].strip()
                    
                    if not id_exercice or not id_entrainement: continue
                    
                    if id_entrainement not in session_links:
                        session_links[id_entrainement] = []
                    
                    # Stocker un dictionnaire d'infos, pas juste l'ID
                    exercise_data = {
                        "id": id_exercice,
                        "series": series,
                        "reps": repetitions
                    }
                    session_links[id_entrainement].append(exercise_data)
                    
                except IndexError:
                    print(f"Erreur: Ligne mal formatée dans {filepath} : {row}")
    except Exception as e:
        messagebox.showerror("Erreur CSV", f"Impossible de lire {filepath}.\nErreur: {e}")
        return {}
    return session_links

def load_sessions_from_csv(filepath, exercise_links, exercise_names_map):
    """
    Étape 3: MODIFIÉE
    Charge Entrainement.csv et utilise les maps des étapes 1 & 2
    pour construire la structure de données finale.
    """
    sessions = {}
    try:
        with open(filepath, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            try:
                header = next(reader)
            except StopIteration:
                return {}
                
            for row in reader:
                if not row: continue
                try:
                    id_entrainement = row[0].strip()
                    nom = row[1].strip()
                    type_ent = row[2].strip()
                    programme = row[3].strip()
                    temps = row[4].strip() if len(row) > 4 else ""
                    
                    session_key = f"{nom} : {type_ent} ({programme})"
                    
                    # --- NOUVELLE LOGIQUE DE RECHERCHE D'EXERCICES ---
                    exercise_data_list = []
                    seen_ids = set() 
                    
                    # 1. Trouver les *détails* d'exercice pour cet entrainement
                    exercise_details_for_this_session = exercise_links.get(id_entrainement, [])
                    
                    # 2. Pour chaque dictionnaire de détails...
                    for ex_data in exercise_details_for_this_session: 
                        ex_id = ex_data["id"]
                        
                        if ex_id in seen_ids:
                            continue
                        seen_ids.add(ex_id)

                        # 3. Récupérer le nom de l'exercice
                        exercise_name = exercise_names_map.get(ex_id, f"Exercice inconnu (ID: {ex_id})")
                        
                        # 4. Créer un dictionnaire complet
                        full_exercise_info = {
                            "id": ex_id,
                            "name": exercise_name,
                            "series": ex_data["series"],
                            "reps": ex_data["reps"]
                        }
                        exercise_data_list.append(full_exercise_info)
                    # --- FIN DE LA NOUVELLE LOGIQUE ---
                    
                    sessions[session_key] = {
                        "date": "N/A",      
                        "notes": "",       
                        "exercises": exercise_data_list, # <-- Stocke la liste de dictionnaires
                        "csv_id": id_entrainement,
                        "csv_programme": programme,
                        "csv_temps_moyen": temps
                    }
                except IndexError:
                    print(f"Erreur: Ligne mal formatée dans {filepath} : {row}")
    except Exception as e:
        messagebox.showerror("Erreur CSV", f"Impossible de lire {filepath}.\nErreur: {e}")
        return {}
    return sessions

# --- CHARGEMENT DES DONNÉES AU DÉMARRAGE ---
print("Chargement de la base de données des exercices...")
EXERCISE_NAMES_MAP = load_exercise_master_list(CSV_EXERCICE_MASTER)
print(f"-> {len(EXERCISE_NAMES_MAP)} exercices chargés.")

print("Chargement des liaisons séances-exercices...")
SESSION_EXERCISE_LINKS = load_session_exercise_links(CSV_EXERCICE_LINKS)
print(f"-> {len(SESSION_EXERCISE_LINKS)} liaisons de séances chargées.")

print("Chargement des séances...")
SESSION_DATA = load_sessions_from_csv(CSV_ENTRAINEMENT, SESSION_EXERCISE_LINKS, EXERCISE_NAMES_MAP)
print(f"-> {len(SESSION_DATA)} séances chargées.")
print("--- Démarrage de l'application ---")

# --- LISTE MAÎTRESSE DES EXERCICES (DYNAMIQUE) ---
MASTER_EXERCISE_LIST = sorted(list(set(EXERCISE_NAMES_MAP.values())))


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


# --- NOUVELLE FONCTION HELPER POUR LE CSV DE LOG ---

def get_next_personne_exo_id():
    """
    Vérifie Personne_Exo.csv, lit l'ID le plus haut et retourne max_id + 1.
    Crée le fichier avec en-tête s'il n'existe pas.
    """
    # L'en-tête attendu
    HEADER = ['id_personne_exo', 'date', 'id_exercice', 'poids', 'id_user']
    file_exists = os.path.exists(CSV_PERSONNE_EXO)
    
    if not file_exists:
        # Cas 1: Le fichier n'existe pas. On le crée avec l'en-tête.
        try:
            with open(CSV_PERSONNE_EXO, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(HEADER)
            return 1 # C'est le premier enregistrement
        except IOError as e:
            messagebox.showerror("Erreur Fichier", f"Impossible de créer {CSV_PERSONNE_EXO}.\n{e}")
            return -1 # Signaler une erreur

    # Cas 2: Le fichier existe. On lit l'ID le plus élevé.
    max_id = 0
    try:
        with open(CSV_PERSONNE_EXO, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            try:
                next(reader) # Sauter l'en-tête
            except StopIteration:
                # Le fichier existe mais est vide (juste l'en-tête ou rien)
                return 1
                
            for row in reader:
                if row: # S'assurer que la ligne n'est pas vide
                    try:
                        # L'ID est dans la première colonne (index 0)
                        current_id = int(row[0])
                        if current_id > max_id:
                            max_id = current_id
                    except (IndexError, ValueError):
                        # Ignorer les lignes mal formées ou sans ID
                        continue
        return max_id + 1
        
    except IOError as e:
        messagebox.showerror("Erreur Fichier", f"Impossible de lire {CSV_PERSONNE_EXO}.\n{e}")
        return -1 # Signaler une erreur
    except Exception as e:
        print(f"Erreur inattendue get_next_personne_exo_id: {e}")
        return -1


# --- FONCTIONS LOGIQUES ---

def on_session_selected(event):
    """
    Appelée quand l'utilisateur choisit une SÉANCE.
    Met à jour la liste des exercices et active les champs.
    """
    session_name = session_var.get()
    if not session_name: return
    try: data = SESSION_DATA[session_name]
    except KeyError: return
    
    # Activer les sections
    notes_frame.config(text="Détails de la Séance")
    notes_text.config(state="normal")
    save_notes_btn.config(state="normal")
    log_frame.config(text="Log d'Exercice")
    exercise_combobox.config(state="readonly")
    weight_label.config(state="normal")
    reps_label.config(state="normal")
    weight_entry.config(state="normal")
    
    # --- MODIFIÉ : Mettre le champ reps en lecture seule ---
    reps_entry.config(state="readonly") 
    
    save_log_btn.config(state="normal")
    
    # Remplir les détails
    date_var.set(f"Date de la séance : {data.get('date', 'N/A')}")
    notes_text.delete("1.0", "end")
    notes_text.insert("1.0", data.get('notes', ''))
    
    # --- MODIFIÉ : Gérer la nouvelle structure de 'exercises' ---
    # 1. Récupérer la liste de dictionnaires d'exercices
    exercise_data_list = data.get('exercises', [])
    
    # 2. Extraire juste les noms pour l'affichage dans la combobox
    exercise_names_list = [exo_info["name"] for exo_info in exercise_data_list]
    
    # 3. Mettre à jour la combobox avec les noms
    exercise_combobox['values'] = exercise_names_list
    
    # Réinitialiser les champs de log
    exercise_var.set("")
    weight_var.set("")
    reps_var.set("")

def on_exercise_selected(event):
    """
    Appelée quand l'utilisateur choisit un EXERCICE.
    Trouve les répétitions associées et remplit le champ.
    """
    # 1. Obtenir la séance sélectionnée
    session_name = session_var.get()
    if not session_name:
        return

    # 2. Obtenir le *nom* de l'exercice sélectionné
    selected_exercise_name = exercise_var.get()
    if not selected_exercise_name:
        return

    try:
        # 3. Récupérer la liste de dictionnaires d'exercices pour cette séance
        session_data = SESSION_DATA[session_name]
        exercise_data_list = session_data.get('exercises', [])

        # 4. Trouver le bon dictionnaire d'exercice en se basant sur le nom
        found_reps = ""
        for exo_info in exercise_data_list:
            if exo_info["name"] == selected_exercise_name:
                found_reps = exo_info.get("reps", "") # Récupérer les reps
                break
        
        # 5. Mettre à jour le champ des répétitions
        reps_var.set(found_reps)

    except KeyError:
        print(f"Erreur: Séance '{session_name}' non trouvée dans on_exercise_selected.")
    except Exception as e:
        print(f"Erreur inattendue dans on_exercise_selected: {e}")

def save_notes():
    session_name = session_var.get()
    if not session_name: messagebox.showwarning("Aucune séance", "Veuillez d'abord sélectionner une séance."); return
    new_notes = notes_text.get("1.0", "end-1c")
    SESSION_DATA[session_name]['notes'] = new_notes
    print(f"Notes pour '{session_name}' sauvegardées (en mémoire) :\n{new_notes}")
    messagebox.showinfo("Sauvegardé", "Vos notes ont été enregistrées (pour cette session).")

def save_exercise_log():
    """
    FONCTION MODIFIÉE POUR SAUVEGARDER DANS Personne_Exo.csv
    """
    session_name = session_var.get()
    exercise_name = exercise_var.get()
    weight = weight_var.get()
    reps = reps_var.get()
    
    # --- 1. Validation de base ---
    if not session_name or not exercise_name or not weight or not reps:
        messagebox.showwarning("Champs manquants", "Veuillez sélectionner un exercice et remplir le champ 'Poids'.")
        return

    # --- 2. NOUVELLE LOGIQUE D'ENREGISTREMENT CSV ---
    
    # 2a. Obtenir la date du jour
    current_date = date.today().isoformat()
    
    # 2b. Obtenir l'ID de l'exercice (très important, on ne sauvegarde pas le nom)
    exo_id_to_save = None
    try:
        # On cherche dans la structure de données de la séance
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
    
    # 2c. Obtenir l'ID utilisateur (placeholder)
    # Comme demandé, on met une valeur statique "1"
    user_id = "1" 
    
    # 2d. Obtenir le prochain ID d'enregistrement
    next_id = get_next_personne_exo_id()
    if next_id == -1: 
        # Une erreur s'est produite dans la fonction helper (ex: fichier bloqué)
        print("Sauvegarde annulée à cause d'une erreur de lecture/écriture de l'ID.")
        return
        
    # 2e. Préparer la nouvelle ligne
    # id_personne_exo;date;id_exercice;poids;id_user
    new_row_data = [next_id, current_date, exo_id_to_save, weight, user_id]
    
    # 2f. Ajouter la ligne au CSV
    try:
        # On ouvre en mode 'a' (append) pour ajouter à la fin
        with open(CSV_PERSONNE_EXO, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(new_row_data)
            
        # --- 3. Feedback à l'utilisateur ---
        print(f"--- LOG SAUVEGARDÉ DANS CSV ---\n   Fichier: {CSV_PERSONNE_EXO}\n   Ligne: {new_row_data}\n------------------------")
        messagebox.showinfo("Série enregistrée", f"{exercise_name}: {weight}kg x {reps} reps\nSérie enregistrée avec succès !")
        
        # Réinitialiser
        weight_var.set("")
        weight_entry.focus()
        
    except IOError as e:
        messagebox.showerror("Erreur Sauvegarde", f"Impossible d'écrire dans {CSV_PERSONNE_EXO}.\n{e}")
    except Exception as e:
        messagebox.showerror("Erreur Inconnue", f"Une erreur est survenue lors de la sauvegarde : {e}")

def handle_save_new_session(popup_window, name_entry, date_entry, exo_listbox):
    session_name = name_entry.get()
    session_date = date_entry.get()
    selected_indices = exo_listbox.curselection()
    selected_exercises_names = [exo_listbox.get(i) for i in selected_indices]
    if not session_name: messagebox.showerror("Erreur", "Veuillez donner un nom à votre séance.", parent=popup_window); return
    if session_name in SESSION_DATA: messagebox.showerror("Erreur", "Une séance avec ce nom existe déjà.", parent=popup_window); return
    if not session_date: messagebox.showerror("Erreur", "Veuillez entrer une date.", parent=popup_window); return
    if not selected_exercises_names: messagebox.showerror("Erreur", "Veuillez sélectionner au moins un exercice.", parent=popup_window); return
    
    # --- MODIFIÉ : On doit créer la structure de données complète ---
    # C'est un peu un hack, car on n'a pas les reps/series
    # On va juste stocker les noms, comme l'ancienne méthode
    exercise_data_list = []
    for name in selected_exercises_names:
        exercise_data_list.append({
            "id": "custom",
            "name": name,
            "series": "",
            "reps": ""
        })

    SESSION_DATA[session_name] = {"date": session_date, "notes": "", "exercises": exercise_data_list}
    
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
    
    for exo in MASTER_EXERCISE_LIST: 
        exo_listbox.insert(tk.END, exo)
        
    btn_frame = tk.Frame(popup_frame, bg=FRAME_BG); btn_frame.pack(fill="x")
    cancel_btn = tk.Button(btn_frame, text="Annuler", command=popup.destroy, font=FONT_BUTTON, bg="#AAAAAA", fg=BUTTON_FG, relief="flat"); cancel_btn.pack(side="right", padx=(10, 0))
    save_btn = tk.Button(btn_frame, text="Enregistrer", command=lambda: handle_save_new_session(popup, name_entry, date_entry, exo_listbox), font=FONT_BUTTON, bg=BUTTON_BG, fg=BUTTON_FG, relief="flat"); save_btn.pack(side="right")


# --- FONCTIONS POUR LE CALENDRIER ---

def show_sessions_for_date(selected_date_iso):
    sessions_on_this_day = []
    for session_name, details in SESSION_DATA.items():
        if details['date'] == selected_date_iso:
            sessions_on_this_day.append({"name": session_name, "details": details})
            
    popup = tk.Toplevel(root)
    popup.title(f"Séances du {selected_date_iso}")
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
    info_text.tag_configure("notes", font=("Helvetica", 10, "italic"), lmargin1=10)

    if not sessions_on_this_day:
        info_text.insert(tk.END, "Aucune séance enregistrée pour ce jour.", "info")
    else:
        for session_info in sessions_on_this_day:
            session_name = session_info['name']
            details = session_info['details']
            
            info_text.insert(tk.END, f"• {session_name}\n", "title")
            info_text.insert(tk.END, "Exercices :\n", "info")
            # --- MODIFIÉ : Gérer la nouvelle structure ---
            for exo_info in details['exercises']:
                info_text.insert(tk.END, f"     - {exo_info['name']}\n", "info")
            notes = details.get('notes', 'Aucune note.')
            if not notes: notes = "Aucune note."
            info_text.insert(tk.END, f"Notes : {notes}\n\n", "notes")
            
    info_text.config(state="disabled")
    
def open_calendar_popup():
    popup = tk.Toplevel(root)
    popup.title("Calendrier des Séances")
    popup.geometry("400x400")
    popup.configure(bg=FRAME_BG)
    popup.resizable(False, False)
    popup.transient(root); popup.grab_set()

    display_date = date.today()
    if SESSION_DATA:
        valid_dates = [
            details['date'] for details in SESSION_DATA.values() 
            if details.get('date') and details.get('date') != 'N/A'
        ]
        if valid_dates:
            try:
                latest_date_str = max(valid_dates)
                display_date = datetime.strptime(latest_date_str, '%Y-%m-%d').date()
            except Exception as e:
                print(f"Erreur à l'analyse des dates pour le calendrier: {e}")

    cal = Calendar(
        popup,
        selectmode='day',
        year=display_date.year,
        month=display_date.month,
        day=display_date.day,
        date_pattern='yyyy-mm-dd',
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

    cal.tag_config('session', background=BUTTON_BG, foreground='white')
    
    for session_name, details in SESSION_DATA.items():
        try:
            date_str = details['date']
            if date_str == 'N/A': continue
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            cal.calevent_create(date_obj, 'Séance', 'session')
        except (ValueError, TypeError):
            pass

    def on_date_clicked(event):
        selected_date_iso = cal.get_date() 
        show_sessions_for_date(selected_date_iso)

    cal.bind("<<CalendarSelected>>", on_date_clicked)


# --- FENÊTRE PRINCIPALE ---
root = tk.Tk()
root.title("Journal d'Entraînement")
root.geometry("600x800")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# --- Cadre d'en-tête ---
header_frame = tk.Frame(main_frame, bg=BG_COLOR)
header_frame.pack(fill="x", anchor="n")
calendar_btn = tk.Button(
    header_frame, text="Calendrier 📅", command=open_calendar_popup,
    font=FONT_LINK, fg=TEXT_COLOR, bg=BG_COLOR, relief="flat", borderwidth=0,
    activeforeground=BUTTON_BG, activebackground=BG_COLOR
)
calendar_btn.pack(side="right", pady=5, padx=5)

# --- 1. SÉLECTION DE LA SÉANCE ---
select_label = tk.Label(main_frame, text="Choisir une séance :", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
select_label.pack(pady=(10, 10))
session_var = tk.StringVar()
session_combobox = ttk.Combobox(
    main_frame, textvariable=session_var, font=FONT_LABEL,
    state="readonly", values=list(SESSION_DATA.keys()) 
)
session_combobox.pack(fill="x", ipady=5)
session_combobox.bind("<<ComboboxSelected>>", on_session_selected)

# --- 2. DÉTAILS DE LA SÉANCE ---
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

# --- 3. LOG D'EXERCICE ---
log_frame = ttk.LabelFrame(main_frame, text="Log d'Exercice (sélectionnez une séance)", padding=15)
log_frame.pack(fill="x")
log_exo_label = tk.Label(log_frame, text="Choisir un exercice :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
log_exo_label.pack(anchor="w")
exercise_var = tk.StringVar()
exercise_combobox = ttk.Combobox(log_frame, textvariable=exercise_var, font=FONT_LABEL, state="disabled")
exercise_combobox.pack(fill="x", ipady=5, pady=(5, 15))

# --- Lier la sélection de l'exercice à la fonction ---
exercise_combobox.bind("<<ComboboxSelected>>", on_exercise_selected)

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

# --- Le champ des reps est grisé (readonly) quand il est activé ---
reps_entry = tk.Entry(
    log_grid_frame, 
    textvariable=reps_var, 
    font=FONT_LABEL, 
    relief="flat", 
    state="disabled", 
    readonlybackground=BG_COLOR # Couleur de fond quand 'readonly'
)
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
    main_frame, text="Créer une nouvelle séance", command=open_create_session_popup,
    font=FONT_BUTTON, bg="#2ECC71", fg=BUTTON_FG, relief="flat"
)
create_session_btn.pack(fill="x", ipady=8)

# --- LANCEMENT DE L'APP ---
root.mainloop()