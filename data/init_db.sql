"""-----------------------------------------------------
-- Joueur
-----------------------------------------------------
DROP TABLE IF EXISTS joueur CASCADE ;
CREATE TABLE joueur(
    id_joueur    SERIAL PRIMARY KEY,
    pseudo       VARCHAR(30) UNIQUE,
    mdp          VARCHAR(256),
    age          INTEGER,
    mail         VARCHAR(50),
    fan_pokemon  BOOLEAN
);
"""
---create table
DROP TABLE IF EXISTS Utilisateur;
CREATE TABLE Utilisateur(
    idUtilisateur SERIAL PRIMARY KEY,
    pseudo VARCHAR(30) UNIQUE,
    motDePasse VARCHAR(200),
    role VARCHAR(200)
);
DROP TABLE IF EXISTS Recette;
CREATE TABLE Recette(
    idRecette SERIAL PRIMARY KEY,
    titre VARCHAR(200),
    consignes TEXT,
    categorie VARCHAR(200),
    origine VARCHAR(100)
    noteMoyenne float,

);
DROP TABLE IF EXISTS Ingredient;
CREATE TABLE Ingredient(
    idIngredient SERIAL PRIMARY KEY,
    nom VARCHAR(200),
    quantite float,
    Description TEXT,

);
DROP TABLE IF EXISTS Avis;
CREATE TABLE Avis(
    idAvis SERIAL PRIMARY KEY,
    FOREIGN KEY idUtilisateur REFERENCES Utilisateur(idUtilisateur),
    FOREIGN KEY idRecette REFERENCES Recette(idRecette),
    note float,
    commentaire TEXT,
);

DROP TABLE IF EXISTS IngredientFavovis;
CREATE TABLE IngredientFavovis (
    PRIMARY KEY (idIngredient, idUtilisateur),
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur),
    FOREIGN KEY (idIngredient) REFERENCES Ingredient(idIngredient),
);

DROP TABLE IF EXISTS RecetteFavorite;
CREATE TABLE RecetteFavorite(
    PRIMARY KEY (idRecette,idUtilisateur)
    FOREIGN KEY (idRecette) REFERENCES Recette(idRecette),
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur)
)
