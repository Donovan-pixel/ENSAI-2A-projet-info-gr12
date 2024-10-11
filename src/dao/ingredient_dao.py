import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.ingredient import Ingredient


class IngredientDao(metaclasse=Singleton):
    """Classe contenant les méthodes pour accéder aux Ingrédients de la base de données"""

    @log
    def ajouterIngredient(self, ingredient) -> bool:
        """
        Ajouter un ingrédient dans la base de données

        Parameters
        ----------
        ingredient : Ingredient

        Returns
        -------
        created : bool
            True si la création est un succès,
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO ingredients(nom) VALUES    "
                        "(%(nom)s)                             "
                        "RETURNING id_ingredient;               ",
                        {
                            "nom": ingredient.nom,
                        },
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.info(e)

        created = False
        if res:
            ingredient.id_ingredient = res["id_ingredient"]
            created = True

        return created

    @log
    def obtenirIngredientParId(self, idIngredient) -> Ingredient:
        """
        Trouver un ingrédient grâce à son identifiant

        Parameters
        ----------
        idIngredient : int
            identifiant de l'ingrédient

        Returns
        -------
        ingredient : Ingredient
            renvoie l'ingrédient que l'on cherche par id
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                   "
                        "FROM ingredients                           "
                        "WHERE id_ingredient = %(idIngredient)s;    ",
                        {"idIngredient": idIngredient},
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.info(e)
            raise

        ingredient = None
        if res:
            ingredient = Ingredient(
                idIngredient=res["id-ingredient"],
                nom=res["nom"],
            )

        return ingredient

    @log
    def obtenirTousLesIngredients(self) -> list[Ingredient]:
        """
        Lister tous les ingrédients

        Parameters
        ----------
        None

        Returns
        -------
        liste_ingredients : list[Ingredient]
            renvoie la liste de tous les ingrédients dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "FROM ingredients;                     "
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.info(e)
            raise

        liste_ingredients = []

        if res:
            for row in res:
                ingredient = Ingredient(
                    idIngredient=res["id-ingredient"],
                    nom=res["nom"],
                )

                liste_ingredients.append(ingredient)

        return liste_ingredients

    @log
    def supprimer(self, ingredient: Ingredient) -> bool:
        """Suppression d'un ingredient dans la base de données

        Parameters
        ----------
        ingredient : Ingredient
            ingredient à supprimer de la base de données

        Returns
        -------
        bool :  True si le joueur a bien été supprimé,
                False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM ingredients                     "
                        " WHERE id_ingredient=%(idIngredient)s;      ",
                        {"idIngredient": ingredient.idIngredient},
                    )
                    res = cursor.rowcount

        except Exception as e:
            logging.info(e)
            raise

        return res > 0
