-- #######################################################################
-- # SCRIPT DE CRÉATION DES TABLES POUR LA BASE DE DONNÉES "ENTRAINEMENT"
-- # Basé sur le MLD fourni
-- #######################################################################

-- IMPORTANT: Toujours commencer par créer les tables de base (sans FK)
-- puis les tables de jonction (qui utilisent les FK).

-- Création de la table User (renommée Utilisateur pour éviter les mots-clés)
CREATE TABLE Utilisateur (
    id_user         INT PRIMARY KEY AUTO_INCREMENT, -- PK, utilise AUTO_INCREMENT pour un SGBD comme MySQL
    pseudo          VARCHAR(50) NOT NULL UNIQUE,    -- Doit être unique
    nom             VARCHAR(50),
    prenom          VARCHAR(50),
    age             INT,
    poids           INT,
    taille          INT,
    motdepasse      VARCHAR(255) NOT NULL,          -- Augmenté à 255 pour le hachage sécurisé
    email           VARCHAR(50) NOT NULL UNIQUE,    -- Doit être unique
    is_admin        BOOLEAN DEFAULT FALSE           -- LOGICAL traduit en BOOLEAN
);

---

-- Création de la table Entrainement
CREATE TABLE Entrainement (
    id_entrainement     INT PRIMARY KEY AUTO_INCREMENT, -- PK
    nom_d_Entrainement  VARCHAR(50) NOT NULL
);

---

-- Création de la table Exercice_musculation
CREATE TABLE Exercice_musculation (
    id_exercice     INT PRIMARY KEY AUTO_INCREMENT,     -- PK
    Titre           VARCHAR(100) NOT NULL,
    Description     TEXT,
    Type            VARCHAR(50),
    PartieDuCorps   VARCHAR(50),
    Equipement      VARCHAR(50),
    NiveauXP        VARCHAR(50),
    Score           INT
);

---

-- #######################################################################
-- # CRÉATION DES TABLES DE JONCTION (RELATIONS N:M)
-- #######################################################################

-- 1. Table de jonction Utilisateur <-> Entrainement (RelationUserTraining)
-- Un Utilisateur peut avoir plusieurs Entrainements, et un Entrainement peut être associé à plusieurs Utilisateurs.
CREATE TABLE RelationUserTraining (
    id_user         INT NOT NULL,
    id_entrainement INT NOT NULL,

    -- Définition de la Clé Primaire composée
    PRIMARY KEY (id_user, id_entrainement),

    -- Définition des Clés Étrangères
    FOREIGN KEY (id_user) REFERENCES Utilisateur(id_user)
        ON DELETE CASCADE, -- Si l'utilisateur est supprimé, la relation est supprimée
    FOREIGN KEY (id_entrainement) REFERENCES Entrainement(id_entrainement)
        ON DELETE CASCADE  -- Si l'entraînement est supprimé, la relation est supprimée
);

---

-- 2. Table de jonction Entrainement <-> Exercice_musculation (Entrainement_Exercice)
-- Un Entrainement contient plusieurs Exercices, et un Exercice est dans plusieurs Entrainements.
CREATE TABLE Entrainement_Exercice (
    id_exercice     INT NOT NULL,
    id_entrainement INT NOT NULL,
    series          INT,
    repetitions     INT,

    -- Définition de la Clé Primaire composée
    PRIMARY KEY (id_exercice, id_entrainement),

    -- Définition des Clés Étrangères
    FOREIGN KEY (id_exercice) REFERENCES Exercice_musculation(id_exercice)
        ON DELETE CASCADE,
    FOREIGN KEY (id_entrainement) REFERENCES Entrainement(id_entrainement)
        ON DELETE CASCADE
);