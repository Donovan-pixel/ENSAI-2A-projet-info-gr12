
---create table
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users(
    id_user SERIAL PRIMARY KEY,
    pseudo VARCHAR(30) UNIQUE,
    mot_de_passe TEXT,
   
);
DROP TABLE IF EXISTS recettes CASCADE;
CREATE TABLE recettes(
    id_meal SERIAL PRIMARY KEY,
    title TEXT,
    category TEXT,
    area TEXT,
    instructions TEXT,

);
DROP TABLE IF EXISTS ingredients CASCADE;
CREATE TABLE ingredients(
    id_ingredient SERIAL PRIMARY KEY,
    nom VARCHAR(255),
);
DROP TABLE IF EXISTS avis CASCADE;
CREATE TABLE avis(
    id_avis SERIAL PRIMARY KEY,
    FOREIGN KEY id_user REFERENCES users(id_user),
    FOREIGN KEY id_meal REFERENCES recettes(id_meal),
    note float,
    commentaire TEXT,
);

DROP TABLE IF EXISTS ingredients_favoris CASCADE;
CREATE TABLE ingredients_favoris (
    PRIMARY KEY (id_ingredient, id_user),
    FOREIGN KEY (id_ingredient) REFERENCES ingredients(id_ingredient),
    FOREIGN KEY (id_user) REFERENCES users(id_user),
);

DROP TABLE IF EXISTS recettes_favorites CASCADE;
CREATE TABLE recettes_favorites(
    PRIMARY KEY (id_meal,id_user),
    FOREIGN KEY (id_meal) REFERENCES recettes(id_meal),
    FOREIGN KEY (id_user) REFERENCES users(id_user)
);

DROP TABLE IF EXISTS meals_ingredients CASCADE;
CREATE TABLE meals_ingredients(
    PRIMARY KEY (id_meal,id_ingredient),
    FOREIGN KEY (id_meal) REFERENCES recettes(id_meal),
    FOREIGN KEY (id_ingredient) REFERENCES ingredients(id_ingredient),
);
DROP TABLE IF EXISTS ingredients_non_desires CASCADE;
CREATE TABLE ingredients_non_desires(
    PRIMARY KEY (id_ingredient,id_user),
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_ingredient) REFERENCES ingredients(id_ingredient),
);
