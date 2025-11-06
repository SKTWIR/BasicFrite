# Fichier : us_31.py

import tkinter as tk
import random

# --- LA LISTE DES DÉFIS (Version "Finisher" / Bonus) ---
CHALLENGE_LIST = [
    # --- GAINAGE & ABDOS (Core) ---
    "Tenir 1 minute de planche (gainage).",
    "Tenir 30 secondes en 'Hollow Hold' (position bateau).",
    "Faire 50 'Bicycle Crunches' (abdos vélo).",
    "Faire 20 'Hanging Knee Raises' (relevés de genoux suspendu).",
    "30 'Deadbugs' (mouvement lent et contrôlé).",
    "Faire 1 minute de 'Mountain Climbers'.",
    "Faire 20 'Leg Raises' (relevés de jambes) au sol.",
    "Aller aux toilettes et faire caca pendant au moins 2h", # ⚠️ Ce défi est inhabituel pour une app fitness

    # --- MOBILITÉ & ÉTIREMENT (Mobility) ---
    "Tenir la position 'Deep Squat' (squat profond) pendant 90 secondes.",
    "Faire 60 secondes de 'Pigeon Pose' (étirement fessier) de chaque côté.",
    "Tenir 60 secondes en 'Cobra Pose' (étirement abdos/dos).",
    "Rester 60 secondes en étirement 'ischio-jambiers' (debout, toucher les pieds).",
    "Faire 10 'Wall Slides' (mobilité d'épaules) contre un mur.",
    "Faire 1 minute de 'Cat-Cow' (chat-vache) pour la colonne.",
    "Faire 30 secondes de 'Downward Dog' (chien tête en bas).",

    # --- BURNOUT RAPIDE (Finisher) ---
    "Tenir 60 secondes en position de Chaise (Wall Sit).",
    "Faire un maximum de pompes en 1 minute (genoux OK).",
    "Faire un maximum de 'Air Squats' en 1 minute.",
    "Faire 30 'Calf Raises' (extensions de mollets) lentes.",
    "Faire 20 Dips sur une chaise ou un banc.",
    "Tenir 30 secondes en 'Dead Hang' (suspendu à la barre, pour le grip).",
    "Faire 5 'Negative Pull-ups' (descentes lentes) si tu as une barre.",

    # --- ÉQUILIBRE & STABILITÉ ---
    "Tenir 60 secondes sur la jambe gauche (yeux ouverts).",
    "Tenir 60 secondes sur la jambe droite (yeux ouverts).",
    "Essayer de tenir 30 secondes sur chaque jambe (yeux FERMÉS).",
    "Marcher 10 mètres sur la pointe des pieds, 10 mètres sur les talons.",
]


def show_random_challenge(parent_root):
    """
    Crée la fenêtre pop-up et y affiche un défi au hasard, liée à la fenêtre principale.
    """
    
    # 1. Piocher un défi au hasard dans la liste
    challenge = random.choice(CHALLENGE_LIST)
    
    # 2. Créer la fenêtre pop-up (Toplevel)
    popup = tk.Toplevel(parent_root)
    popup.title("✅ Ton Défi !")
    popup.configure(bg="#2C3E50") # Fond bleu nuit
    
    # 3. Créer le Label qui contient le texte du défi
    challenge_label = tk.Label(
        popup,
        text=challenge,
        font=("Arial", 14, "bold"),
        wraplength=380, # Permet au texte de revenir à la ligne
        pady=30,
        padx=20,
        fg="#ECF0F1", # Texte blanc-gris
        bg="#2C3E50" # Fond bleu nuit
    )
    challenge_label.pack()

    # 4. Créer un bouton pour fermer la pop-up
    ok_button = tk.Button(
        popup,
        text="C'est parti !",
        font=("Arial", 12, "bold"),
        command=popup.destroy, # La commande détruit la pop-up
        bg="#2ECC71", # Vert "succès"
        fg="#FFFFFF", # Texte blanc
        relief="flat",
        padx=10,
        pady=5
    )
    ok_button.pack(pady=(0, 20))

    # 5. Rendre la pop-up "modale"
    popup.transient(parent_root) 
    popup.grab_set() 
    parent_root.wait_window(popup)

# Retirez le if __name__ == '__main__': et le root.mainloop() d'origine
# pour que le fichier puisse être importé comme module.