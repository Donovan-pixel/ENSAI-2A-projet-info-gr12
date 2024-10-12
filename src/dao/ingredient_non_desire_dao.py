import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.avis import Avis
from business_object.ingredient import Ingredient
from business_object.utilisateur import Utilisateur

class IngredientNonDesireDAO(metaclass=Singleton):
    "Classe contenant les méthodes pour gérer les ingrédients non désirés de la base de données"


    @log
    def ajouterIngredientNonDesire(self, ingredient:Ingredient, utilisateur:Utilisateur) -> bool:
        """Ajout d'un ingrédient non désiré dans la base de données

        Parameters
        ----------
        ingredient : Ingredient
            L'ingrédient à ajouter

        utilisateur : Utilisateur
            L'utilisateur pour qui c'est un ingrédient non désiré

        Returns
        -------
        added : bool
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
                            "id_ingredient": ingredient.id_ingredient,
                            "id_user": utilisateur.id_user,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception(e)
            return False

        added = False
        if res:
            added = True

        return added

        @log
        def supprimerIngredientNonDesire(self, ingredient:Ingredient, utilisateur:Utilisateur) -> bool:
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
                                "id_ingredient": ingredient.id_ingredient,
                                "id_user": utilisateur.id_user,
                            },
                        )   

                        return cursor.rowcount > 0
            except Exception as e:
                logging.exception(e)
                return False

    @log
    def obtenirIngredientsNonDesires(self, utilisateur:Utilisateur) -> list[Ingredient]:
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
                        "SELECT (id_ingredient, nom) FROM ingredient" 
                        "JOIN ingredients_non_desires" 
                        "ON ingredients_non_desires.id_ingredient = ingredient.id_ingredient"
                        "WHERE id_user = %(id_user)s;", 
                        {
                            "id_user": utilisateur.id_user,
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
                    id_ingredient = row[0],
                    nom = row[1]
                )

                liste.append(ingredient_non_desire)
        
        return liste
