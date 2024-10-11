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
            logging.error(f"Erreur lors de l'ajout de l'ingrédient non désiré : {e}")
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

                        if cursor.rowcount > 0:
                            return True
                        else:
                            return False
            except Exception as e:
                logging.exception(e)
                return False

    @log
    def obtenirIngredientsNonDesires(self, utilisateur:Utilisateur) -> List[Ingredient]:
        """Obtention des ingrédients non désirés d'un utilisateur

        Parameters
        ----------
        utilisateur : Utilisateur
            L'utilisateur duquel on souhaite obtenir ses ingrédients non désirée

        Returns
        -------
        List[Ingredient]:
            Liste contenant tous les ingrédients non désirés associés à l'utilisateur
        """

        ingredients_non_desires = []

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM ingredients_non_desires JOIN recettes ON recettes.id_meal = avis.id_meal"
                        "WHERE id_meals = %(id_recette)s", 
                        {
                            "id_recette": recettes.id_meal,
                        },
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)