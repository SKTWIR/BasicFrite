import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os

CSV_FILE = os.path.join(os.path.dirname(__file__), "Personne_Exo.csv")


def load_user_entrainements(user_id):
    data = []
    try:
        with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                if row.get('id_user') == str(user_id):
                    data.append(row)
    except Exception:
        with open(CSV_FILE, newline='', encoding='latin-1') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                if row.get('id_user') == str(user_id):
                    data.append(row)
    return data


def run_export_entrainement_screen(root_window, switch_back_callback, user_id):
    for w in root_window.winfo_children():
        w.destroy()
    root_window.title("⬇️ Export Entrainement")
    root_window.geometry("900x500")
    root_window.resizable(False, False)

    entrainements = load_user_entrainements(user_id)

    # Affichage tableau
    if entrainements:
        columns = list(entrainements[0].keys())
    else:
        columns = ["Aucune donnée"]

    frame_table = tk.Frame(root_window)
    frame_table.pack(fill="both", expand=True, padx=12, pady=6)
    tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=18)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="w")
    vsb = tk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    frame_table.grid_rowconfigure(0, weight=1)
    frame_table.grid_columnconfigure(0, weight=1)

    for row in entrainements:
        tree.insert("", "end", values=[row[c] for c in columns])

    def export_csv():
        if not entrainements:
            messagebox.showwarning("Aucune donnée", "Aucune donnée à exporter.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Exporter mes entrainements"
        )
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=columns, delimiter=';')
                    writer.writeheader()
                    for row in entrainements:
                        writer.writerow(row)
                messagebox.showinfo("Export réussi", f"Export effectué : {file_path}")
            except Exception as e:
                messagebox.showerror("Erreur export", str(e))

    # Bas: boutons export et retour (toujours visibles en bas)
    bottom_frame = tk.Frame(root_window)
    bottom_frame.pack(side="bottom", fill="x", pady=10)
    tk.Button(bottom_frame, text="⬇️ Générer mon récap (CSV)", command=export_csv, bg="#2980B9", fg="white", font=("Arial", 12, "bold")).pack(side="left", padx=20)
    tk.Button(bottom_frame, text="⬅️ Retour Menu", command=switch_back_callback).pack(side="right", padx=20)
