import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.recette import Recette
from business_object.ingredient import Ingredient


class RecetteDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux recettes de la base de données"""

    @log
    def ajouterRecette(self, recette: Recette) -> bool:
        """Ajout d'une recette de la base de données

        Parameters
        ---------
        recette : Recette
            Recette qu'il faut ajouter

        Returns
        ------
        bool :
            True si la recette a bien été ajoutée
            False sinon
        """

        res = None
        created = False

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO recettes(title, category, area, instructions) VALUES        "
                        "(%(title)s, %(category)s, %(area)s, %(instructions)s)                   "
                        "  RETURNING id_meal;                                                    ",
                        {
                            "title": recette.titre,
                            "category": recette.categorie,
                            "area": recette.origine,
                            "instructions": recette.consignes,
                        },
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.info(e)
            raise

        if res:
            recette.idRecette = res["id_meal"]
            created = True

        return created

    @log
    def obtenirToutesLesRecettes(self) -> list[Recette]:
        """Obtention de toutes les recettes de la base de données

        Returns:
        -------
        list[Recette]:
            Liste des recettes
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT * FROM recettes;
                        """
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.exception(e)
            raise

        recettes = []

        if res:
            for row in res:
                recette = Recette(
                    idRecette=row["id_recette"],
                    titre=row["title"],
                    categorie=row["category"],
                    origine=row["area"],
                    consignes=row["instructions"],
                )
                recettes.append(recette)

        return recettes

    @log
    def obtenirRecettesparLettre(self, lettre) -> list[Recette]:
        """Rechercher des recettes commençant par une lettre donnée

        Parameters:
        ---------
        lettre : str
            Première lettre des recettes recherchées

        Returns:
        ------
        list[Recette] :
            Liste des recettes commençant par la lettre
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT * FROM recettes
                        WHERE nom ILIKE '%(lettre)s%'
                        """,
                        {
                            "lettre": lettre,
                        },
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.exception(e)
            raise

        recettes = []

        if res:
            for row in res:
                recette = Recette(
                    idRecette=row["id_recette"],
                    titre=row["title"],
                    categorie=row["category"],
                    origine=row["area"],
                    consignes=row["instructions"],
                )
                recettes.append(recette)

        return recettes

    @log
    def obtenirRecettesParIngredient(self, ingredient: Ingredient) -> list[Recette]:
        """Obtention des recettes contenant un ingrédient spécifique

        Parameters
        ----------
        ingredient : Ingredient
            L'ingrédient contenu dans les recettes recherchées

        Returns
        -------
        List[Recette]
            Liste des recettes contenant l'ingrédient spécifié
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT * FROM recettes
                        JOIN recettes_ingredients ri ON r.id_recette = ri.id_recette
                        WHERE ri.id_ingredient = %(id_ingredient)s;
                        """,
                        {"id_ingredient": ingredient.id_ingredient},
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.exception(e)
            raise

        recettes = []

        if res:
            for row in res:
                recette = Recette(
                    idRecette=row["id_recette"],
                    titre=row["nom"],
                    categorie=row["categorie"],
                    origine=row["origine"],
                    consignes=row["instructions"],
                )
                recettes.append(recette)

        return recettes

    @log
    def obtenirRecettesParIngredients(self, ingredients: list[Ingredient]) -> list[Recette]:
        """Obtention de recettes contenant certains ingrédients

        Parameters:
        ---------
        ingredients : list[Ingredient]
            Liste des ingrédients contenus dans les recettes recherchées

        Returns:
        ------
        list[Recette] :
            Liste des recettes contenant les ingrédients voulus
        """

        ingredients_id = tuple([ing.idIngredient for ing in ingredients])

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:

                    cursor.execute(
                        """
                        SELECT * FROM recettes
                        JOIN meals_ingredients
                        ON meals_ingredients.id_meal = recettes.id_meal
                        WHERE meals_ingredients.id_ingredient IN %(ingredients_id)s
                        GROUP BY recettes.id_meal
                        """,
                        {
                            "ingredients_id": ingredients_id,
                        },
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.exception(e)
            raise

        recettes = []

        if res:
            for row in res:
                recette = Recette(
                    idRecette=row["id_recette"],
                    titre=row["title"],
                    categorie=row["category"],
                    origine=row["area"],
                    consignes=row["instructions"],
                )
                recettes.append(recette)

        return recettes

    @log
    def obtenirRecettesParCategorie(self, categorie: str) -> list[Recette]:
        """Obtention de recettes par catégorie

        Parameters:
        ---------
        categorie : str
            Catégorie de recettes recherchées

        Returns:
        ------
        list[Recette] :
            Liste des recettes de la catégorie recherchée
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                            SELECT * FROM recettes
                            WHERE categorie = %(categorie)s;
                            """,
                        {"categorie": categorie},
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.exception(e)
            raise

        recettes = []

        if res:
            for row in res:
                recette = Recette(
                    idRecette=row["id_recette"],
                    titre=row["nom"],
                    categorie=row["categorie"],
                    origine=row["origine"],
                    consignes=row["instructions"],
                )
                recettes.append(recette)

        return recettes
