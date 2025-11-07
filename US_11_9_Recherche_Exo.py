import tkinter as tk
from tkinter import ttk
import csv
import os

CSV_FILE = os.path.join(os.path.dirname(__file__), "Exercice_musculation.csv")


def load_exercices():
    exercices = []
    try:
        with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                exercices.append(row)
    except UnicodeDecodeError:
        with open(CSV_FILE, newline='', encoding='latin-1') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                exercices.append(row)
    return exercices


def run_exercise_search_screen(root_window, switch_back_callback):
    for w in root_window.winfo_children():
        w.destroy()
    root_window.title("🔍 Recherche Exercice")
    root_window.geometry("900x500")
    root_window.resizable(False, False)

    exercices = load_exercices()

    # Top: barre de recherche
    top_frame = tk.Frame(root_window)
    top_frame.pack(fill="x", padx=12, pady=(12, 6))
    tk.Label(top_frame, text="Recherche (Titre, Description, Partie du Corps) :").pack(side="left")
    entry_search = tk.Entry(top_frame, width=40)
    entry_search.pack(side="left", padx=(8, 6))

    # Tableau d'exercices avec scrollbar
    columns = ("Titre", "Description", "PartieDuCorps")
    frame_table = tk.Frame(root_window)
    frame_table.pack(fill="both", expand=True, padx=12, pady=6)
    
    tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=18)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=220 if col!="Description" else 420, anchor="w")
    
    vsb = tk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    frame_table.grid_rowconfigure(0, weight=1)
    frame_table.grid_columnconfigure(0, weight=1)

    def refresh_table(filtered=None):
        tree.delete(*tree.get_children())
        for exo in (filtered if filtered is not None else exercices):
            tree.insert("", "end", values=(exo["Titre"], exo["Description"], exo["PartieDuCorps"]))

    def do_search(*_):
        q = entry_search.get().strip().lower()
        if not q:
            refresh_table()
            return
        filtered = [e for e in exercices if q in (e["Titre"] or '').lower() or q in (e["PartieDuCorps"] or '').lower()]
        refresh_table(filtered)

    entry_search.bind('<Return>', do_search)
    tk.Button(top_frame, text="🔎 Chercher", command=do_search).pack(side="left", padx=(0, 6))
    tk.Button(top_frame, text="↺ Réinitialiser", command=lambda: (entry_search.delete(0, 'end'), refresh_table())).pack(side="left")

    # Bas: bouton retour (toujours visible en bas)
    bottom_frame = tk.Frame(root_window)
    bottom_frame.pack(side="bottom", fill="x", pady=10)
    tk.Button(bottom_frame, text="⬅️ Retour Menu", command=switch_back_callback).pack()

    refresh_table()
