# Fichier : us_32.py
# USER STORY 32
# En tant que sportif,
# je souhaite que le coach virtuel me recommande des exercices alternatifs
# afin de changer d’exercice s'il me fait mal.

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
import random

BASE_DIR = os.path.dirname(__file__)
EXERCICE_CSV = os.path.join(BASE_DIR, "Exercice_musculation.csv")
ENTRAINEMENT_EXO_CSV = os.path.join(BASE_DIR, "Entrainement_Exercice.csv")

# --- STYLE (même esprit que le reste de l'appli) ---
BG_COLOR = "#D6EAF8"
FRAME_BG = "#EBF5FB"
TEXT_COLOR = "#17202A"
BUTTON_BG = "#3498DB"
BUTTON_FG = "#FFFFFF"
FONT_TITLE = ("Helvetica", 16, "bold")
FONT_LABEL = ("Helvetica", 11)
FONT_BUTTON = ("Helvetica", 11, "bold")


def load_exercices():
    """Charge tous les exercices depuis Exercice_musculation.csv."""
    exercices = []
    if not os.path.exists(EXERCICE_CSV):
        messagebox.showerror("Erreur", "Fichier Exercice_musculation.csv introuvable.")
        return exercices

    try:
        with open(EXERCICE_CSV, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                exercices.append(row)
    except UnicodeDecodeError:
        # fallback au cas où l'encodage serait différent
        with open(EXERCICE_CSV, newline="", encoding="latin-1") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                exercices.append(row)

    return exercices


def find_alternative(exercices, exercice_source):
    """Trouve un exercice alternatif de même Type et PartieDuCorps, mais avec un id différent."""
    if not exercice_source:
        return None

    type_src = (exercice_source.get("Type") or "").strip()
    part_src = (exercice_source.get("PartieDuCorps") or "").strip()
    id_src = exercice_source.get("id")

    candidates = [
        e for e in exercices
        if e.get("id") != id_src
        and (e.get("Type") or "").strip() == type_src
        and (e.get("PartieDuCorps") or "").strip() == part_src
    ]

    if not candidates:
        return None

    # On peut choisir au hasard pour varier
    return random.choice(candidates)


def update_exercise_in_training(old_id, new_id):
    """
    Remplace toutes les occurrences de old_id par new_id dans Entrainement_Exercice.csv.
    => C'est ici que l'on "change" l'exercice dans la planification.
    """
    if not os.path.exists(ENTRAINEMENT_EXO_CSV):
        messagebox.showerror("Erreur", "Fichier Entrainement_Exercice.csv introuvable.")
        return

    rows = []
    fieldnames = None

    try:
        with open(ENTRAINEMENT_EXO_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            fieldnames = reader.fieldnames
            for row in reader:
                if row.get("id_exercice") == str(old_id):
                    row["id_exercice"] = str(new_id)
                rows.append(row)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la lecture des entraînements : {e}")
        return

    try:
        with open(ENTRAINEMENT_EXO_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(rows)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'écriture des entraînements : {e}")
        return


def run_alternative_exercise_screen(root_window, switch_back_callback=None):
    """
    Interface pour choisir un exercice et voir une alternative,
    avec bouton 'Changer' qui met à jour Entrainement_Exercice.csv.
    """
    exercices = load_exercices()
    if not exercices:
        return

    # Nettoyer la fenêtre principale
    for w in root_window.winfo_children():
        w.destroy()

    root_window.title("US 32 - Exercice alternatif")
    root_window.geometry("900x500")
    root_window.resizable(False, False)
    root_window.configure(bg=BG_COLOR)

    # Titre
    tk.Label(
        root_window,
        text="🧠 Coach virtuel - Exercice alternatif",
        font=FONT_TITLE,
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=10)

    # Cadre principal
    main_frame = tk.Frame(root_window, bg=BG_COLOR)
    main_frame.pack(expand=True, fill="both", padx=20, pady=10)

    # --- Sélecteur d'exercice en haut ---
    top_frame = tk.Frame(main_frame, bg=BG_COLOR)
    top_frame.pack(fill="x", pady=(0, 10))

    tk.Label(
        top_frame,
        text="Choisissez votre exercice actuel :",
        font=FONT_LABEL,
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(side="left")

    # Liste des titres + mapping
    titres = [e.get("Titre", f"Exercice {e.get('id')}") for e in exercices]
    selected_title = tk.StringVar(value=titres[0])

    dropdown = ttk.Combobox(
        top_frame,
        textvariable=selected_title,
        values=titres,
        width=50,
        state="readonly"
    )
    dropdown.pack(side="left", padx=10)

    # Cadres exercice actuel / alternatif
    left_frame = tk.LabelFrame(
        main_frame,
        text="Exercice actuel",
        bg=FRAME_BG,
        fg=TEXT_COLOR,
        font=FONT_LABEL
    )
    left_frame.pack(side="left", expand=True, fill="both", padx=(0, 10))

    right_frame = tk.LabelFrame(
        main_frame,
        text="Exercice alternatif proposé",
        bg=FRAME_BG,
        fg=TEXT_COLOR,
        font=FONT_LABEL
    )
    right_frame.pack(side="left", expand=True, fill="both", padx=(10, 0))

    # Labels de texte
    lbl_current = tk.Label(
        left_frame,
        text="",
        bg=FRAME_BG,
        justify="left",
        wraplength=380,
        font=FONT_LABEL
    )
    lbl_current.pack(padx=10, pady=10, anchor="nw")

    lbl_alt = tk.Label(
        right_frame,
        text="",
        bg=FRAME_BG,
        justify="left",
        wraplength=380,
        font=FONT_LABEL
    )
    lbl_alt.pack(padx=10, pady=10, anchor="nw")

    def on_changer():
        """Appelé quand on clique sur 'Changer' sous l'exercice alternatif."""
        titre = selected_title.get()
        exercice_source = next((e for e in exercices if e.get("Titre") == titre), None)
        if not exercice_source:
            messagebox.showerror("Erreur", "Exercice source introuvable.")
            return

        alternative = find_alternative(exercices, exercice_source)
        if not alternative:
            messagebox.showinfo("Info", "Aucune alternative disponible à enregistrer.")
            return

        old_id = exercice_source.get("id")
        new_id = alternative.get("id")
        update_exercise_in_training(old_id, new_id)

        messagebox.showinfo(
            "Succès",
            f"L'exercice '{exercice_source.get('Titre')}' a été remplacé par\n"
            f"'{alternative.get('Titre')}' dans la planification (Entrainement_Exercice.csv)."
        )

    # Bouton "Changer" sous l'alternative
    btn_changer = tk.Button(
        right_frame,
        text="Changer",
        command=on_changer,
        font=FONT_BUTTON,
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        relief="flat",
        padx=10,
        pady=5
    )
    btn_changer.pack(pady=(0, 10), anchor="se", padx=10)

    def refresh_display(*args):
        """Met à jour les infos affichées quand on change d'exercice."""
        titre = selected_title.get()
        exercice_source = next((e for e in exercices if e.get("Titre") == titre), None)

        if not exercice_source:
            lbl_current.config(text="Exercice introuvable.")
            lbl_alt.config(text="")
            return

        # Texte exercice actuel
        txt_cur = (
            f"Titre : {exercice_source.get('Titre')}\n"
            f"Type : {exercice_source.get('Type')}\n"
            f"Partie du corps : {exercice_source.get('PartieDuCorps')}\n\n"
            f"Description :\n{exercice_source.get('Description')}"
        )
        lbl_current.config(text=txt_cur)

        # Trouver alternative
        alternative = find_alternative(exercices, exercice_source)
        if not alternative:
            lbl_alt.config(
                text="Aucune alternative trouvée pour cet exercice\n"
                     "(même Type et même Partie du corps)."
            )
            return

        txt_alt = (
            f"Titre : {alternative.get('Titre')}\n"
            f"Type : {alternative.get('Type')}\n"
            f"Partie du corps : {alternative.get('PartieDuCorps')}\n\n"
            f"Description :\n{alternative.get('Description')}"
        )
        lbl_alt.config(text=txt_alt)

    # Met à jour quand on change dans la combobox
    selected_title.trace_add("write", refresh_display)

    # Premier affichage
    refresh_display()

    # Bas : bouton retour / fermer
    bottom_frame = tk.Frame(root_window, bg=BG_COLOR)
    bottom_frame.pack(side="bottom", fill="x", pady=10)

    if switch_back_callback:
        tk.Button(
            bottom_frame,
            text="⬅️ Retour Menu",
            command=switch_back_callback
        ).pack()
    else:
        tk.Button(
            bottom_frame,
            text="Fermer",
            command=root_window.destroy
        ).pack()


if __name__ == "__main__":
    # Test autonome
    root = tk.Tk()
    run_alternative_exercise_screen(root)
    root.mainloop()
