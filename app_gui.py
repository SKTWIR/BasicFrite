# Fichier : app_gui.py (Ajout de nbentrainementsemaine)

import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
import sys
import os 
import csv 
# Pour le graphique de progression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime


# --- CONSTANTES ---
USER_CSV_FILE = os.path.join(os.path.dirname(__file__), 'User.csv')
PROGRESS_CSV_FILE = os.path.join(os.path.dirname(__file__), 'Progression.csv')

# --- DÉFINITION DE LA CLASSE (Validation) ---

class UserProfile:
    """Valide les informations du profil utilisateur."""
    
    def __init__(self, first_name, last_name, email=None, age=None, weight=None, height=None, nb_seances=None):
        if not first_name or not last_name:
            raise ValueError("Le prénom et le nom ne peuvent pas être vides.")
        self.first_name = first_name
        self.last_name = last_name

        if email is not None and ('@' not in str(email) or '.' not in str(email)):
             raise ValueError("L'email doit être une adresse valide.")
        self.email = email
        
        if age is not None:
            if not isinstance(age, int) or age <= 0:
                raise ValueError("L'âge doit être un nombre entier positif.")
        self.age = age

        if weight is not None:
             if not isinstance(weight, (float, int)) or weight <= 0:
                raise ValueError("Le poids (kg) doit être un nombre positif.")
        self.weight = weight

        if height is not None:
            if not isinstance(height, (float, int)) or height <= 0 or height > 3:
                raise ValueError("La taille (m) doit être un nombre positif (ex: 1.75).")
        self.height = height
        
        # NOUVELLE VALIDATION
        if nb_seances is not None:
            if not isinstance(nb_seances, int) or not 0 <= nb_seances <= 7:
                 raise ValueError("Le nombre de séances doit être un entier entre 0 et 7.")
        self.nb_seances = nb_seances

def load_user_progress(user_id):
    """
    Charge les données de progression d'un utilisateur spécifique
    depuis PROGRESS_CSV_FILE.
    """
    progress = {}

    if user_id is None:
        return progress

    # Garantir comparação por string (CSV sempre lê como texto)
    user_id_str = str(user_id)

    if not os.path.exists(PROGRESS_CSV_FILE):
        return progress  # pas de fichier = pas de données

    try:
        with open(PROGRESS_CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                if row.get('id_user') != user_id_str:
                    continue

                exercice = row.get('exercice', 'Inconnu')
                date_str = row.get('date', '')
                poids_str = row.get('poids', '')

                if not date_str or not poids_str:
                    continue

                # Conversion de la date (on tente deux formats courants)
                date_obj = None
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
                    try:
                        date_obj = datetime.strptime(date_str, fmt).date()
                        break
                    except ValueError:
                        continue
                if date_obj is None:
                    # Si la date est illisible, on ignore la ligne
                    continue

                try:
                    poids_val = float(poids_str.replace(',', '.'))
                except ValueError:
                    continue

                if exercice not in progress:
                    progress[exercice] = []
                progress[exercice].append((date_obj, poids_val))

        # Tri des listes par date
        for exo, points in progress.items():
            points.sort(key=lambda x: x[0])

    except Exception as e:
        messagebox.showerror("Erreur Progression", f"Erreur lors du chargement des données de progression : {e}")

    return progress

def show_progress_window(root_window, user_data):
    """
    Affiche une fenêtre avec un graphique de progression pour un exercice choisi.
    USER STORY 17.
    """
    global current_editing_user_id

    user_id = None

    # 1) Tenta pegar a partir de user_data (vindo du main_menu)
    if isinstance(user_data, dict):
        for key in ("id_user", "id", "user_id"):
            val = user_data.get(key)
            if val not in (None, ""):
                user_id = val
                break

    # 2) Se ainda não tiver, cai pro global usado no profil
    if not user_id and current_editing_user_id:
        user_id = current_editing_user_id

    if not user_id:
        messagebox.showerror(
            "Erreur",
            "ID utilisateur introuvable pour afficher la progression."
        )
        return

    # Carrega os dados de progressão desse usuário
    progress = load_user_progress(user_id)
    if not progress:
        messagebox.showinfo(
            "Progression",
            "Aucune donnée de progression trouvée pour cet utilisateur."
        )
        return

    # --- A partir daqui, a parte visual fica igual ao que eu já tinha te mandado ---

    win = tk.Toplevel(root_window)
    win.title("📈 Progression de l'utilisateur")
    win.geometry("700x500")
    win.resizable(False, False)
    BG_COLOR = "#D6EAF8"
    win.configure(bg=BG_COLOR)

    full_name = f"{user_data.get('prénom', '')} {user_data.get('nom', '')}".strip()
    tk.Label(
        win,
        text=f"📈 Progression de {full_name}",
        font=("Helvetica", 14, "bold"),
        bg=BG_COLOR
    ).pack(pady=10)

    exercices = list(progress.keys())
    selected_exo = tk.StringVar(value=exercices[0])

    top_frame = tk.Frame(win, bg=BG_COLOR)
    top_frame.pack(pady=5)

    tk.Label(
        top_frame,
        text="Choisissez un exercice :",
        font=("Helvetica", 11),
        bg=BG_COLOR
    ).pack(side="left", padx=5)

    exo_menu = tk.OptionMenu(top_frame, selected_exo, *exercices)
    exo_menu.config(font=("Helvetica", 10))
    exo_menu.pack(side="left", padx=5)

    graph_frame = tk.Frame(win, bg=BG_COLOR)
    graph_frame.pack(expand=True, fill="both", padx=10, pady=10)

    def plot_exercise(exercice_name):
        for widget in graph_frame.winfo_children():
            widget.destroy()

        data_points = progress.get(exercice_name, [])
        if not data_points:
            tk.Label(
                graph_frame,
                text="Aucune donnée pour cet exercice.",
                font=("Helvetica", 11),
                bg=BG_COLOR
            ).pack(pady=20)
            return

        dates = [p[0] for p in data_points]
        poids = [p[1] for p in data_points]

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(dates, poids, marker='o')
        ax.set_title(f"Évolution du poids - {exercice_name}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Poids (kg)")
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def on_exercice_change(*args):
        plot_exercise(selected_exo.get())

    selected_exo.trace_add("write", on_exercice_change)
    plot_exercise(selected_exo.get())


# --- VARIABLES GLOBALES ---
entry_first_name = None
entry_last_name = None
entry_email = None 
entry_age = None
entry_weight = None
entry_height = None
entry_nb_seances = None # NOUVELLE VARIABLE GLOBALE
current_editing_user_id = None 


def submit_data(return_callback, current_data):
    """
    Récupère les données des champs, valide, et sauvegarde les modifications
    dans le fichier User.csv.
    """
    global current_editing_user_id
    if not current_editing_user_id:
        messagebox.showerror("Erreur", "Aucun ID utilisateur. Impossible de sauvegarder.")
        return
        
    try:
        # 1. Récupérer les données des champs
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        email = entry_email.get()
        age_str = entry_age.get() if entry_age.get() else ''
        weight_str = entry_weight.get() if entry_weight.get() else ''
        height_str = entry_height.get() if entry_height.get() else ''
        nb_seances_str = entry_nb_seances.get() if entry_nb_seances.get() else '' # NOUVELLE VALEUR
        
        # 2. Validation
        age_val = int(age_str) if age_str else None
        weight_val = float(weight_str) if weight_str else None
        height_val = float(height_str) if height_str else None
        nb_seances_val = int(nb_seances_str) if nb_seances_str else None
        
        UserProfile(first_name, last_name, email, age_val, weight_val, height_val, nb_seances_val) # Validation
        
        # 3. Lecture du CSV et mise à jour
        rows = []
        fieldnames = []
        found = False
        updated_row_data = current_data 
        
        try:
            with open(USER_CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                fieldnames = reader.fieldnames
                for row in reader:
                    if row['id_user'] == current_editing_user_id:
                        found = True
                        row['nom'] = last_name
                        row['prénom'] = first_name 
                        row['email'] = email
                        row['age'] = age_str
                        row['poids'] = weight_str
                        row['taille'] = height_str
                        row['nbentrainementsemaine'] = nb_seances_str # <-- NOUVELLE SAUVEGARDE
                        updated_row_data = row 
                    rows.append(row)
        except Exception as e:
            messagebox.showerror("Erreur Lecture CSV", f"Erreur (lecture): {e}")
            return
            
        if not found:
            messagebox.showerror("Erreur", "Utilisateur non trouvé dans le CSV lors de la sauvegarde.")
            return

        # 5. Écriture du CSV complet
        try:
            with open(USER_CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(rows)
        except Exception as e:
            messagebox.showerror("Erreur Écriture CSV", f"Erreur (écriture): {e}")
            return

        messagebox.showinfo("Succès", f"Profil de {first_name} mis à jour!")
        return_callback(updated_row_data) 

    except (ValueError, TypeError) as e:
        messagebox.showerror("Erreur de validation", str(e))


def return_to_menu(callback, data_to_return):
    """Ferme cet écran et exécute la fonction de rappel (switch_to_menu)."""
    callback(data_to_return)


def run_profile_screen(root_window, switch_to_menu_callback, user_data): 
    """
    Lance l'interface du profil utilisateur dans la fenêtre fournie.
    """
    global entry_first_name, entry_last_name, entry_email, entry_age, entry_weight, entry_height, entry_nb_seances, current_editing_user_id

    current_editing_user_id = user_data.get('id_user')
    
    # 1. Nettoyer l'écran précédent
    for widget in root_window.winfo_children():
        widget.destroy()

    # 2. Configuration de la fenêtre
    root_window.title("Profil Utilisateur")
    root_window.geometry("550x520") # TAILLE AJUSTÉE
    root_window.resizable(False, False)

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

    # Remplissage des champs (utilisant 'prénom' avec accent)
    fields = {
        "Prénom": tk.StringVar(value=user_data.get('prénom', '')),
        "Nom": tk.StringVar(value=user_data.get('nom', '')),
        "Email": tk.StringVar(value=user_data.get('email', '')),
        "Âge": tk.StringVar(value=user_data.get('age', '')),
        "Poids (kg)": tk.StringVar(value=user_data.get('poids', '')),
        "Taille (m)": tk.StringVar(value=user_data.get('taille', '')),
        "Séances/semaine": tk.StringVar(value=user_data.get('nbentrainementsemaine', '0')), # NOUVEL AFFICHAGE
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
        elif label_text == "Email": entry_email = entry
        elif label_text == "Âge": entry_age = entry
        elif label_text == "Poids (kg)": entry_weight = entry
        elif label_text == "Taille (m)": entry_height = entry
        elif label_text == "Séances/semaine": entry_nb_seances = entry # NOUVELLE LIAISON
        
        row_index += 1

        # --- Bouton Voir progression (US 17) ---
    progress_button = tk.Button(
        main_frame,
        text="📈 Voir progression",
        command=lambda: show_progress_window(root_window, user_data),
        font=FONT_BUTTON,
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        relief="flat",
        borderwidth=0,
        activebackground="#2874A6",
        activeforeground="#FFFFFF"
    )
    progress_button.grid(row=row_index, column=0, pady=(20, 10), padx=10, sticky="w")

    # --- Bouton Enregistrer ---
    submit_button = tk.Button(
        main_frame,
        text="Enregistrer",
        command=lambda: submit_data(switch_to_menu_callback, user_data),
        font=FONT_BUTTON,
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        relief="flat",
        borderwidth=0,
        activebackground="#2874A6",
        activeforeground="#FFFFFF"
    )
    submit_button.grid(row=row_index, column=1, pady=(20, 10), padx=10, sticky="e")
    row_index += 1


    # Bouton Retour Menu (Passe les données)
    return_button = tk.Button(main_frame, text="⬅️ Retour Menu", 
                              command=lambda: return_to_menu(switch_to_menu_callback, user_data),
                              font=("Helvetica", 10), bg="#AAAAAA", relief="flat")
    
    return_button.grid(row=row_index, column=0, columnspan=2, pady=(10, 0), sticky="s")


# --- Exécution seule pour test ---
if __name__ == '__main__':
    def dummy_callback(data_recue):
        print(f"Retour Menu Principal demandé. Données reçues: {data_recue}")
        sys.exit()
    
    dummy_data = {'id_user': '1', 'prénom': 'Test', 'nom': 'User', 'email': 'test@test.com', 'age': '25', 'poids': '70', 'taille': '1.80', 'nbentrainementsemaine': '3'}

    root = tk.Tk()
    run_profile_screen(root, dummy_callback, dummy_data)
    root.mainloop()