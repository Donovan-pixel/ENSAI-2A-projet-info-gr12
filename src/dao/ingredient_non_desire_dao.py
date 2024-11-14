import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.ingredient import Ingredient
from business_object.utilisateur import Utilisateur


class IngredientNonDesireDao(metaclass=Singleton):
    "Classe contenant les méthodes pour gérer les ingrédients non désirés de la base de données"

    @log
    def ajouterIngredientNonDesire(self, ingredient: Ingredient, utilisateur: Utilisateur) -> bool:
        """Ajout d'un ingrédient non désiré dans la base de données

        Parameters
        ----------
        ingredient : Ingredient
            L'ingrédient à ajouter

        utilisateur : Utilisateur
            L'utilisateur pour qui c'est un ingrédient non désiré

        Returns
        -------
        bool :
            True si l'ajout est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO ingredients_non_desires (id_ingredient, id_user)
                        VALUES (%(id_ingredient)s, %(id_user)s)
                        RETURNING id_ingredient;
                        """,
                        {
                            "id_ingredient": ingredient.idIngredient,
                            "id_user": utilisateur.idUtilisateur,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception(e)
            return False

        return bool(res)

    @log
    def supprimerIngredientNonDesire(
        self, ingredient: Ingredient, utilisateur: Utilisateur
    ) -> bool:
        """Suppression d'un ingrédient non désiré dans la base de données

        Parameters
        ----------
        ingredient : Ingredient
            L'ingrédient à supprimer

            utilisateur : Utilisateur
                L'utilisateur qui en a fait la demande

        Returns
        -------
        bool:
            True si la suppression est un succès
            False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM ingredients_non_desires
                        WHERE id_ingredient = %(id_ingredient)s AND id_user = %(id_user)s;
                        """,
                        {
                            "id_ingredient": ingredient.idIngredient,
                            "id_user": utilisateur.idUtilisateur,
                        },
                    )

                    res = cursor.rowcount

        except Exception as e:
            logging.exception(e)
            return False

        return res > 0

    @log
    def obtenirIngredientsNonDesires(self, utilisateur: Utilisateur) -> list[Ingredient]:
        """Obtention des ingrédients non désirés d'un utilisateur

        Parameters
        ----------
        utilisateur : Utilisateur
            L'utilisateur duquel on souhaite obtenir les ingrédients non désirée

        Returns
        -------
        list[Ingredient]:
            Liste contenant tous les ingrédients non désirés associés à l'utilisateur
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT i.id_ingredient, i.nom FROM ingredients i
                        JOIN ingredients_non_desires ind
                        ON ind.id_ingredient = i.id_ingredient
                        WHERE ind.id_user = %(id_user)s;
                        """,
                        {
                            "id_user": utilisateur.idUtilisateur,
                        },
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception(e)
            raise

        liste = []

        if res:
            for row in res:
                ingredient_non_desire = Ingredient(
                    idIngredient=row["id_ingredient"], nom=row["nom"]
                )

                liste.append(ingredient_non_desire)

        return liste
