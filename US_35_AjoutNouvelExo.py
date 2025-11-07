import tkinter as tk
from tkinter import messagebox
import csv
import os

CSV_FILE = os.path.join(os.path.dirname(__file__), "Exercice_musculation.csv")
CSV_FIELDS = [
    "id", "Titre", "Description", "Type", "PartieDuCorps", "Equipment", "NiveauXP", "Score"
]

def get_next_id():
    try:
        with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            ids = [int(row["id"]) for row in reader if row["id"].isdigit()]
            return str(max(ids) + 1) if ids else "0"
    except Exception:
        return "0"

def append_exercise(data):
    try:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, delimiter=';')
            writer.writerow(data)
        return True
    except Exception as e:
        print(e)
        return False

def run_add_exercise_screen(root_window, switch_back_callback):
    for w in root_window.winfo_children():
        w.destroy()
    root_window.title("➕ Ajout Nouvel Exercice")
    root_window.geometry("700x600")
    root_window.resizable(False, False)

    frame = tk.Frame(root_window)
    frame.pack(padx=30, pady=30, fill="both", expand=True)

    fields = [
        ("Titre", ""),
        ("Description", ""),
        ("Type", "Strength"),
        ("PartieDuCorps", ""),
        ("Equipment", ""),
        ("NiveauXP", ""),
        ("Score", "")
    ]
    entries = {}
    for i, (label, default) in enumerate(fields):
        tk.Label(frame, text=label+" :", anchor="w").grid(row=i, column=0, sticky="w", pady=6)
        entry = tk.Entry(frame, width=60)
        entry.insert(0, default)
        entry.grid(row=i, column=1, pady=6)
        entries[label] = entry

    def submit():
        data = {k: v.get().strip() for k, v in entries.items()}
        if not data["Titre"] or not data["Description"] or not data["PartieDuCorps"]:
            messagebox.showerror("Erreur", "Titre, Description et PartieDuCorps sont obligatoires.")
            return
        data["id"] = get_next_id()
        if append_exercise(data):
            messagebox.showinfo("Succès", f"Exercice '{data['Titre']}' ajouté !")
            for v in entries.values():
                v.delete(0, tk.END)
            entries["Titre"].focus_set()
        else:
            messagebox.showerror("Erreur", "Impossible d'ajouter l'exercice.")

    tk.Button(frame, text="Ajouter l'exercice", command=submit, bg="#2ECC71", fg="white", font=("Arial", 12, "bold")).grid(row=len(fields), column=1, pady=20, sticky="e")
    tk.Button(root_window, text="⬅️ Retour Menu Admin", command=switch_back_callback).pack(pady=10, side="bottom")
