import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.ingredient import Ingredient
from business_object.utilisateur import Utilisateur


class IngredientFavoriDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Ingrédients Favoris de la base de données"""

    @log
    def ajouterIngredientFavori(self, ingredient: Ingredient, utilisateur: Utilisateur) -> bool:
        """
        Ajouter un ingrédient favori, associé à un utilisateur, dans la base de données

        Parameters
        ----------
        ingredient : Ingredient
            L'ingrédient à ajouter

        utilisateur : Utilisateur
            L'utilisateur pour qui c'est un ingrédient favori

        Returns
        -------
        bool :
            True si l'ajout est un succès,
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO ingredients_favoris(id_ingredient, id_user) VALUES"
                        "(%(id_ingredient)s, %(id_user)s)                              "
                        "RETURNING id_ingredient;                                      ",
                        {
                            "id_ingredient": ingredient.idIngredient,
                            "id_user": utilisateur.idUtilisateur,
                        },
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.exception(e)
            raise

        return bool(res)

    @log
    def obtenirIngredientsFavoris(self, utilisateur: Utilisateur) -> list[Ingredient]:
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
                        """
                        SELECT ingredients.id_ingredient, ingredients.nom
                        FROM ingredients_favoris
                        JOIN ingredients
                        ON ingredients.id_ingredient = ingredients_favoris.id_ingredient
                        WHERE id_user = %(id_user)s;
                        """,
                        {
                            "id_user": utilisateur.idUtilisateur,
                        },
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.exception(e)
            raise

        liste_ingredients_favoris = []

        if res:
            for row in res:
                ingredient_favori = Ingredient(
                    id_ingredient=res["id_ingredient"],
                    nom=res["nom"],
                )

                liste_ingredients_favoris.append(ingredient_favori)

        return liste_ingredients_favoris

    @log
    def supprimerIngredientFavori(self, ingredient: Ingredient, utilisateur: Utilisateur) -> bool:
        """Supprimer un ingrédient favori, associé à un utilisateur, de la base de données

        Parameters
        ----------
        ingredient : Ingredient
            ingrédient à supprimer

        utilisateur : Utilisateur
            L'utilisateur qui en fait la demande

        Returns
        -------
        bool :
            True si l'ingrédient a bien été supprimé,
            False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM ingredients_favoris
                        WHERE id_ingredient=%(id_ingredient)s
                        AND id_user = %(id_user)s;
                        """,
                        {
                            "id_ingredient": ingredient.idIngredient,
                            "id_user": utilisateur.idUtilisateur,
                        },
                    )
                    res = cursor.rowcount

        except Exception as e:
            logging.exception(e)
            raise

        return res > 0
