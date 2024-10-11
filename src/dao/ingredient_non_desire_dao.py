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
    def ajouterIngredientNonDesire(self, ingredient:Ingredient, utilisateur:Utilisateur):
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
                        "INSERT INTO ingredients_non_desires(id_avis, id_user, id_meal, note, commentaire) VALUES"
                        "(%(id_ingredient)s, %(id_user)s);             ",
                        {
                            "id_ingredient": ingredient.id_ingredient,
                            "id_user": utilisateur.id_user,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        






