import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.ingredient import Ingredient


class IngredientFavoriDao(metaclasse=Singleton):
    """Classe contenant les méthodes pour accéder aux Ingrédients Favoris de la base de données"""

    @log
    def ajouterIngredientFavori(self, ingredient, utilisateur) -> bool:
        """
        Ajouter un ingrédient favori, associé à un utilisateur, dans la base de données

        Parameters
        ----------
        ingredient : Ingredient
        utilisateur : Utilisateur

        Returns
        -------
        added : bool
            True si l'ajout est un succès,
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO ingredients_favoris(id_ingredient, id_user) VALUES    "
                        "(%(id_ingredient)s, %(id_user)s)                                  ",
                        {
                            "id_ingredient": ingredient.idIngredient,
                            "id_user": utilisateur.idUtilisateur,
                        },
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.info(e)
            raise

        added = False

        if res:
            ingredient.idIngredient = res["idIngredient"]
            added = True

        return added

    @log
    def obtenirTousLesIngredientsFavoris(self, utilisateur) -> list[Ingredient]:
        """
        Lister tous les ingrédients favoris d'un utilisateur

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        liste_ingredients_favoris : list[Ingredient]
            renvoie la liste de tous les ingrédients favoris de l'utilisateurs
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "FROM ingredients_favoris;                     "
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.info(e)
            raise

        liste_ingredients_favoris = []

        if res:
            for row in res:
                ingredient_favori = Ingredient(
                    idIngredient=res["id_ingredient"],
                    nom=res["nom"],
                )

                liste_ingredients_favoris.append(ingredient_favori)

        return liste_ingredients_favoris

    @log
    def supprimer(self, ingredient, utilisateur) -> bool:
        """Suppression d'un ingredient dans la base de données

        Parameters
        ----------
        ingredient : Ingredient
            ingrédient à supprimer

        utilisateur : Utilisateur

        Returns
        -------
        bool :  True si l'ingrédient a bien été supprimé,
                False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM ingredients_favoris                     "
                        " WHERE id_ingredient=%(idIngredient)s;      ",
                        {"idIngredient": ingredient.idIngredient},
                    )
                    res = cursor.rowcount

        except Exception as e:
            logging.info(e)
            raise

        return res > 0
