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
CSV_PERSONNE_EXO = "Personne_Exo.csv" # Fichier de log des séries
CSV_PERSONNE_ENTRAINEMENT = "Personne_Entrainement.csv" # <-- NOUVEAU FICHIER

# Vérification que tous les fichiers nécessaires existent
fichiers_manquants = []
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
    Étape 2: Charge Entrainement_Exercice.csv pour lier les séances aux exercices.
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
                    id_exercice = row[0].strip()
                    id_entrainement = row[1].strip()
                    series = row[2].strip()
                    repetitions = row[3].strip()
                    
                    if not id_exercice or not id_entrainement: continue
                    
                    if id_entrainement not in session_links:
                        session_links[id_entrainement] = []
                    
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
    Étape 3: Charge Entrainement.csv et utilise les maps des étapes 1 & 2
    pour construire la structure de données finale (SESSION_DATA).
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
                    
                    exercise_data_list = []
                    seen_ids = set() 
                    
                    exercise_details_for_this_session = exercise_links.get(id_entrainement, [])
                    
                    for ex_data in exercise_details_for_this_session: 
                        ex_id = ex_data["id"]
                        
                        if ex_id in seen_ids:
                            continue
                        seen_ids.add(ex_id)

                        exercise_name = exercise_names_map.get(ex_id, f"Exercice inconnu (ID: {ex_id})")
                        
                        full_exercise_info = {
                            "id": ex_id,
                            "name": exercise_name,
                            "series": ex_data["series"],
                            "reps": ex_data["reps"]
                        }
                        exercise_data_list.append(full_exercise_info)
                    
                    sessions[session_key] = {
                        "date": "N/A", # Cette date n'est plus utilisée pour les notes
                        "notes": "", # Ceci n'est plus qu'une valeur par défaut      
                        "exercises": exercise_data_list,
                        "csv_id": id_entrainement, # <-- TRES IMPORTANT
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


# --- FONCTIONS HELPER POUR LES ID CSV ---

def get_next_personne_exo_id():
    """
    Vérifie Personne_Exo.csv, lit l'ID le plus haut et retourne max_id + 1.
    Crée le fichier avec en-tête s'il n'existe pas.
    """
    HEADER = ['id_personne_exo', 'date', 'id_exercice', 'poids', 'id_user']
    file_exists = os.path.exists(CSV_PERSONNE_EXO)
    
    if not file_exists:
        try:
            with open(CSV_PERSONNE_EXO, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(HEADER)
            return 1
        except IOError as e:
            messagebox.showerror("Erreur Fichier", f"Impossible de créer {CSV_PERSONNE_EXO}.\n{e}")
            return -1

    max_id = 0
    try:
        with open(CSV_PERSONNE_EXO, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            try:
                next(reader) 
            except StopIteration:
                return 1
                
            for row in reader:
                if row:
                    try:
                        current_id = int(row[0])
                        if current_id > max_id:
                            max_id = current_id
                    except (IndexError, ValueError):
                        continue
        return max_id + 1
        
    except IOError as e:
        messagebox.showerror("Erreur Fichier", f"Impossible de lire {CSV_PERSONNE_EXO}.\n{e}")
        return -1
    except Exception as e:
        print(f"Erreur inattendue get_next_personne_exo_id: {e}")
        return -1

# --- NOUVELLE FONCTION HELPER ---
def get_next_personne_entrainement_id():
    """
    Vérifie Personne_Entrainement.csv, lit l'ID le plus haut et retourne max_id + 1.
    Crée le fichier avec en-tête s'il n'existe pas.
    """
    HEADER = ['cle_id', 'id_user', 'date_entrainement', 'id_entrainement', 'note']
    file_exists = os.path.exists(CSV_PERSONNE_ENTRAINEMENT)
    
    if not file_exists:
        try:
            with open(CSV_PERSONNE_ENTRAINEMENT, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(HEADER)
            return 1
        except IOError as e:
            messagebox.showerror("Erreur Fichier", f"Impossible de créer {CSV_PERSONNE_ENTRAINEMENT}.\n{e}")
            return -1

    max_id = 0
    try:
        with open(CSV_PERSONNE_ENTRAINEMENT, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            try:
                next(reader) 
            except StopIteration:
                return 1
                
            for row in reader:
                if row:
                    try:
                        current_id = int(row[0])
                        if current_id > max_id:
                            max_id = current_id
                    except (IndexError, ValueError):
                        continue
        return max_id + 1
        
    except IOError as e:
        messagebox.showerror("Erreur Fichier", f"Impossible de lire {CSV_PERSONNE_ENTRAINEMENT}.\n{e}")
        return -1
    except Exception as e:
        print(f"Erreur inattendue get_next_personne_entrainement_id: {e}")
        return -1


# --- FONCTION DE NOTIFICATION DE PROGRESSION ---

def notify_if_progress(user_id, id_exercice, exercise_name, new_poids):
    """
    MODIFIÉE: Trouve le POIDS MAX précédent pour un user/exercice
    et affiche une alerte si le new_poids est un record personnel.
    Lit depuis CSV_PERSONNE_EXO.
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
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo(
                "Nouveau Record Personnel !",
                f"Bravo ! Vous avez battu votre record sur : {exercise_name}\n\n"
                f"Ancien record : {max_previous_poids} kg\n"
                f"Nouveau record : {new_poids_float} kg"
            )
            root.destroy()
        elif max_previous_poids == 0 and new_poids_float > 0:
             print(f"Première fois pour {exercise_name}. Pas de record à battre.")
        
    except Exception as e:
        print(f"Erreur lors de la vérification de progression : {e}")
        
# --- NOUVELLE FONCTION ---
def open_date_picker_for_note():
    """
    Ouvre un petit calendrier popup pour choisir la date de la note.
    Met à jour la variable training_date_var.
    """
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
        popup,
        selectmode='day',
        year=default_date.year,
        month=default_date.month,
        day=default_date.day,
        date_pattern='yyyy-mm-dd'
    )
    cal.pack(fill="both", expand=True, padx=10, pady=10)

    def on_click(event):
        """Met à jour la date et ferme le popup."""
        training_date_var.set(cal.get_date())
        popup.destroy()

    cal.bind("<<CalendarSelected>>", on_click)


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
    reps_entry.config(state="readonly") 
    save_log_btn.config(state="normal")
    
    # --- NOUVEAU : Activer la section date ---
    training_date_var.set(date.today().isoformat())
    training_date_entry.config(state="normal")
    date_picker_btn.config(state="normal")
    # --- FIN NOUVEAU ---

    # Remplir les détails
    notes_text.delete("1.0", "end")
    # On ne pré-remplit plus les notes, l'utilisateur en crée une nouvelle
    notes_text.insert("1.0", data.get('notes', '')) 
    
    exercise_data_list = data.get('exercises', [])
    exercise_names_list = [exo_info["name"] for exo_info in exercise_data_list]
    exercise_combobox['values'] = exercise_names_list
    
    exercise_var.set("")
    weight_var.set("")
    reps_var.set("")

def on_exercise_selected(event):
    """
    Appelée quand l'utilisateur choisit un EXERCICE.
    Trouve les répétitions associées et remplit le champ.
    """
    session_name = session_var.get()
    if not session_name:
        return

    selected_exercise_name = exercise_var.get()
    if not selected_exercise_name:
        return

    try:
        session_data = SESSION_DATA[session_name]
        exercise_data_list = session_data.get('exercises', [])

        found_reps = ""
        for exo_info in exercise_data_list:
            if exo_info["name"] == selected_exercise_name:
                found_reps = exo_info.get("reps", "") 
                break
        
        reps_var.set(found_reps)

    except KeyError:
        print(f"Erreur: Séance '{session_name}' non trouvée dans on_exercise_selected.")
    except Exception as e:
        print(f"Erreur inattendue dans on_exercise_selected: {e}")

# --- FONCTION DE SAUVEGARDE DES NOTES (MODIFIÉE) ---
def save_notes():
    """
    Sauvegarde la note de séance dans Personne_Entrainement.csv.
    """
    session_name = session_var.get()
    if not session_name: 
        messagebox.showwarning("Aucune séance", "Veuillez d'abord sélectionner une séance.")
        return

    # 1. Récupérer les données de l'interface
    training_date = training_date_var.get()
    new_notes = notes_text.get("1.0", "end-1c").strip()
    
    # 2. Valider les entrées
    if not training_date:
        messagebox.showwarning("Date manquante", "Veuillez choisir une date pour cet entraînement.")
        return
    try:
        # Valider le format de la date
        datetime.strptime(training_date, '%Y-%m-%d')
    except ValueError:
        messagebox.showwarning("Format de date invalide", "Veuillez entrer une date au format AAAA-MM-JJ.")
        return
        
    if not new_notes:
        messagebox.showwarning("Note vide", "Veuillez écrire une note avant de sauvegarder.")
        return

    # 3. Récupérer les données "cachées"
    try:
        id_entrainement = SESSION_DATA[session_name]['csv_id']
    except KeyError:
        messagebox.showerror("Erreur de Séance", "Impossible de trouver l'ID de la séance sélectionnée.")
        return
    
    id_user = "1" # Placeholder
    
    # 4. Obtenir le nouvel ID pour le CSV
    cle_id = get_next_personne_entrainement_id()
    if cle_id == -1:
        return # Erreur déjà affichée par la fonction helper

    # 5. Préparer la ligne
    # cle_id; id_user; date_entrainement; id_entrainement; note
    new_row = [cle_id, id_user, training_date, id_entrainement, new_notes]
    
    # 6. Écrire dans le CSV
    try:
        with open(CSV_PERSONNE_ENTRAINEMENT, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(new_row)
        
        messagebox.showinfo("Sauvegardé", "Votre note d'entraînement a été enregistrée avec succès.")
        print(f"Note enregistrée: {new_row}")
        
    except IOError as e:
        messagebox.showerror("Erreur Sauvegarde", f"Impossible d'écrire dans {CSV_PERSONNE_ENTRAINEMENT}.\n{e}")
    except Exception as e:
        messagebox.showerror("Erreur Inconnue", f"Une erreur est survenue lors de la sauvegarde : {e}")

def save_exercise_log():
    """
    Sauvegarde une série dans Personne_Exo.csv et notifie si progression.
    """
    session_name = session_var.get()
    exercise_name = exercise_var.get()
    weight = weight_var.get()
    reps = reps_var.get()
    
    if not session_name or not exercise_name or not weight or not reps:
        messagebox.showwarning("Champs manquants", "Veuillez sélectionner un exercice et remplir le champ 'Poids'.")
        return

    # Utilise la date du jour pour le log de la SÉRIE
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
    
    user_id = "1" 
    
    # Vérifier la progression AVANT de sauvegarder la nouvelle valeur
    notify_if_progress(user_id, exo_id_to_save, exercise_name, weight)

    next_id = get_next_personne_exo_id()
    if next_id == -1: 
        print("Sauvegarde annulée à cause d'une erreur de lecture/écriture de l'ID.")
        return
        
    new_row_data = [next_id, current_date, exo_id_to_save, weight, user_id]
    
    try:
        with open(CSV_PERSONNE_EXO, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(new_row_data)
            
        print(f"--- LOG SAUVEGARDÉ DANS CSV ---\n   Fichier: {CSV_PERSONNE_EXO}\n   Ligne: {new_row_data}\n------------------------")
        messagebox.showinfo("Série enregistrée", f"{exercise_name}: {weight}kg x {reps} reps\nSérie enregistrée avec succès !")
        
        weight_var.set("")
        weight_entry.focus()
        
    except IOError as e:
        messagebox.showerror("Erreur Sauvegarde", f"Impossible d'écrire dans {CSV_PERSONNE_EXO}.\n{e}")
    except Exception as e:
        messagebox.showerror("Erreur Inconnue", f"Une erreur est survenue lors de la sauvegarde : {e}")


# --- FONCTION HELPER POUR LE CALENDRIER ---

def get_all_logged_dates():
    """
    Lit Personne_Exo.csv et retourne un set de toutes les dates uniques (AAAA-MM-JJ)
    où un exercice a été enregistré.
    """
    logged_dates = set()
    if not os.path.exists(CSV_PERSONNE_EXO):
        return logged_dates 

    try:
        with open(CSV_PERSONNE_EXO, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                date_str = row.get('date')
                if date_str:
                    try:
                        datetime.strptime(date_str, '%Y-%m-%d')
                        logged_dates.add(date_str)
                    except ValueError:
                        continue 
    except Exception as e:
        print(f"Erreur en lisant les dates de log : {e}")
    
    return logged_dates

# --- FONCTIONS POUR LE CALENDRIER (AFFICHAGE) ---

def show_sessions_for_date(selected_date_iso):
    """
    Affiche les exercices et poids loggés pour une date
    spécifique en lisant Personne_Exo.csv.
    """
    
    logs_on_this_day = []
    if os.path.exists(CSV_PERSONNE_EXO):
        try:
            with open(CSV_PERSONNE_EXO, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    if row.get('date') == selected_date_iso:
                        exo_id = row.get('id_exercice')
                        exo_name = EXERCISE_NAMES_MAP.get(exo_id, f"ID Exercice: {exo_id}")
                        
                        log_info = {
                            "name": exo_name,
                            "poids": row.get('poids', 'N/A')
                        }
                        logs_on_this_day.append(log_info)
        except Exception as e:
            messagebox.showerror("Erreur Lecture", f"Impossible de lire {CSV_PERSONNE_EXO}.\n{e}")
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
    
def open_calendar_popup():
    """
    Ouvre un calendrier et marque les jours
    en lisant Personne_Exo.csv (via get_all_logged_dates).
    """
    popup = tk.Toplevel(root)
    popup.title("Calendrier des Logs") 
    popup.geometry("400x400")
    popup.configure(bg=FRAME_BG)
    popup.resizable(False, False)
    popup.transient(root); popup.grab_set()

    all_dates_logged = get_all_logged_dates()
    
    display_date = date.today()
    if all_dates_logged:
        try:
            latest_date_str = max(all_dates_logged)
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

    cal.tag_config('log', background=BUTTON_BG, foreground='white') 
    
    for date_str in all_dates_logged:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            cal.calevent_create(date_obj, 'Log', 'log') 
        except ValueError:
            continue 

    def on_date_clicked(event):
        selected_date_iso = cal.get_date() 
        show_sessions_for_date(selected_date_iso) 

    cal.bind("<<CalendarSelected>>", on_date_clicked)


# --- FENÊTRE PRINCIPALE ---
root = tk.Tk()
root.title("Journal d'Entraînement")
root.geometry("600x740") 
root.configure(bg=BG_COLOR)
root.resizable(False, False)

main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# --- Cadre d'en-tête ---
header_frame = tk.Frame(main_frame, bg=BG_COLOR)
header_frame.pack(fill="x", anchor="n")
calendar_btn = tk.Button(
    header_frame, text="Recherche une séance", command=open_calendar_popup,
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

# --- 2. DÉTAILS DE LA SÉANCE (MODIFIÉ) ---
notes_frame = ttk.LabelFrame(main_frame, text="Détails de la Séance (sélectionnez une séance)", padding=15)
notes_frame.pack(fill="x", pady=20)

# --- NOUVEAU CADRE POUR LA DATE ---
date_picker_frame = tk.Frame(notes_frame, bg=FRAME_BG)
date_picker_frame.pack(fill="x", anchor="w")

date_label = tk.Label(date_picker_frame, text="Date de l'entraînement :", font=FONT_LABEL, bg=FRAME_BG, fg=TEXT_COLOR)
date_label.pack(side="left", padx=(0, 5))

training_date_var = tk.StringVar()
training_date_entry = tk.Entry(date_picker_frame, textvariable=training_date_var, font=FONT_LABEL, relief="flat", state="disabled", width=12)
training_date_entry.pack(side="left", padx=5)

date_picker_btn = tk.Button(
    date_picker_frame, text="📅", command=open_date_picker_for_note, font=FONT_LABEL,
    relief="flat", bg=FRAME_BG, fg=TEXT_COLOR, activebackground=FRAME_BG, 
    activeforeground=BUTTON_BG, borderwidth=0, state="disabled"
)
date_picker_btn.pack(side="left")
# --- FIN DU NOUVEAU CADRE ---

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
log_frame.pack(fill="x", pady=(20, 0)) 
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
    readonlybackground=BG_COLOR 
)
reps_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0))

save_log_btn = tk.Button(
    log_frame, text="Enregistrer la série", command=save_exercise_log, font=FONT_BUTTON,
    bg=BUTTON_BG, fg=BUTTON_FG, relief="flat", state="disabled"
)
save_log_btn.pack(anchor="e", pady=(20, 0))

# --- 4. BOUTON DE CRÉATION DE SÉANCE (SUPPRIMÉ) ---

# --- LANCEMENT DE l'APP ---
root.mainloop()