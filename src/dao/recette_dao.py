import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from src.business_object.recette import Recette


class RecetteDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux recettes de la base de données"""

    @log
    def ajouterRecette(self, recette:Recette) -> bool:
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

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO recettes(title, category, area, instructions) VALUES        "
                        "(%(title)s, %(category)s, %(area)s, %(instructions)s)             "
                        "  RETURNING id_meal;                                                ",
                        {
                            "title": recette.title,
                            "category": recette.category,
                            "area": recette.area,
                            "instructions": recette.instructions,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            recette.id_meal = res["id_meal"]
            created = True

        return created

    @log
    def obtenirRecetteParId(self, id_recette) -> Recette:
        """Trouver une recette grâce à son id
        Parameters
        ----------
        id_recette : int
        l'id de la recette qu'on souhaite trouver
        Return
        ------
        recette : Recette
        renvoie la recette que l'on cherche par id
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM recettes                      "
                        " WHERE id_meal = %(id_meal)s;  ",
                        {"id_meal": id_recette},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        recette = None
        if res:
            recette = Recette(
                idRecette=res["id_meal"],
                titre=res["title"],
                origine=res["area"],
                categorie=res["category"],
                consignes=res["instructions"],
            )

        return recette
