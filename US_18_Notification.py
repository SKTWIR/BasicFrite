import tkinter as tk
from tkinter import messagebox
import csv
import os

CSV_FILE = os.path.join(os.path.dirname(__file__), "Entrainement_Exercice.csv")


def notify_if_progress(user_id, id_exercice, new_poids):
    """
    Affiche une alertbox si le user_id a déjà fait cet exercice avec un poids inférieur.
    """
    try:
        with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                if row.get('user_id') == str(user_id) and row.get('id_exercice') == str(id_exercice):
                    try:
                        ancien_poids = float(row.get('poids', 0))
                        if float(new_poids) > ancien_poids:
                            root = tk.Tk()
                            root.withdraw()
                            messagebox.showinfo(
                                "Progression !",
                                f"Bravo ! Vous avez augmenté votre charge sur l'exercice {id_exercice} (ancien poids : {ancien_poids} kg, nouveau : {new_poids} kg)."
                            )
                            root.destroy()
                            break
                    except Exception:
                        continue
    except Exception as e:
        print("Erreur notification progression:", e)
