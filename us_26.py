# --- 🎯 USER STORY 26 : Choix de l'objectif et programme adapté ---

# Variable où l'on stocke l'objectif principal de l'utilisateur.
# Dans l'application réelle, cette valeur viendrait d'un formulaire (ex : menu déroulant).
# Objectifs possibles : "prise de masse", "perte de poids", "maintien".
objectif_principal = "prise de masse"


# Dictionnaire contenant un exemple de programme adapté à chaque objectif.
PROGRAMMES_PAR_OBJECTIF = {
    "prise de masse": {
        "description": "Programme orienté hypertrophie (gain de masse musculaire).",
        "type_seances": [
            "Séance 1 : Haut du corps (Pecs / Dos / Épaules)",
            "Séance 2 : Bas du corps (Quadriceps / Ischios / Fessiers)",
            "Séance 3 : Full Body axé charges moyennes à lourdes"
        ],
        "recommandations": [
            "Plage de 6 à 10 répétitions par série.",
            "3 à 5 séries par exercice.",
            "Temps de repos : 90 à 120 secondes.",
            "Légère surcharge progressive semaine après semaine."
        ],
    },
    "perte de poids": {
        "description": (
            "Programme orienté dépense calorique et maintien de la masse musculaire."
        ),
        "type_seances": [
            "Séance 1 : Full Body + cardio léger",
            "Séance 2 : Haut du corps + HIIT court",
            "Séance 3 : Bas du corps + marche rapide / vélo"
        ],
        "recommandations": [
            "Plage de 10 à 15 répétitions par série.",
            "2 à 4 séries par exercice.",
            "Temps de repos : 45 à 75 secondes.",
            "Ajouter du cardio (marche, vélo, HIIT) 2 à 3 fois par semaine."
        ],
    },
    "maintien": {
        "description": "Programme pour garder son niveau actuel et rester en forme.",
        "type_seances": [
            "Séance 1 : Full Body classique",
            "Séance 2 : Haut du corps",
            "Séance 3 : Bas du corps + gainage"
        ],
        "recommandations": [
            "Plage de 8 à 12 répétitions par série.",
            "3 à 4 séries par exercice.",
            "Temps de repos : 60 à 90 secondes.",
            "Conserver un volume stable sans forcer la progression."
        ],
    },
}


def obtenir_programme_adapte(objectif: str) -> dict:
    """
    Retourne un programme d'entraînement adapté en fonction de l'objectif saisi.

    :param objectif: Objectif de l'utilisateur
                     (ex: 'prise de masse', 'perte de poids', 'maintien').
    :return: Un dictionnaire contenant une description, un type de séances
             et des recommandations générales.
    """

    # Normalisation de l'objectif (minuscules / espaces)
    objectif_normalise = objectif.strip().lower()

    # Petites correspondances pour accepter plusieurs formulations
    correspondances = {
        "prise de masse": "prise de masse",
        "masse": "prise de masse",
        "perte de poids": "perte de poids",
        "minceur": "perte de poids",
        "maintien": "maintien",
        "maintenance": "maintien",
    }

    # On essaye de récupérer une clé propre à partir de ce que l'utilisateur a écrit
    cle_programme = correspondances.get(objectif_normalise)

    # Si l'objectif n'est pas reconnu, on peut par exemple retourner un programme "maintien"
    if cle_programme is None:
        cle_programme = "maintien"

    return PROGRAMMES_PAR_OBJECTIF[cle_programme]


# --- 💡 Exemple d'utilisation dans votre application ---

programme_choisi = obtenir_programme_adapte(objectif_principal)

print(f"Objectif choisi : {objectif_principal}")
print("---")
print("Description générale :")
print(programme_choisi["description"])
print()

print("Exemple de répartition des séances :")
for i, seance in enumerate(programme_choisi["type_seances"], start=1):
    print(f"  - {seance}")

print()
print("Recommandations générales :")
for reco in programme_choisi["recommandations"]:
    print(f"  - {reco}")
