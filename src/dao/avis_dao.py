import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.avis import Avis
from business_object.recette import Recette


class AvisDao(metaclass=Singleton):
    "Classe contenant les méthodes pour accéder aux avis de la base de données"

    @log
    def ajouter_avis(self, avis:Avis) -> bool:
        """Ajout d'un avis dans la base de données

        Parameters
        ----------
        avis : Avis
            L'avis à ajouter

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
                        "INSERT INTO Avis(id_user, id_meal, note, commentaire) VALUES        "
                        "(%(id_user)s, %(id_meal)s, %(note)s, %(commentaire)s)             "
                        "  RETURNING id_avis;                                                ",
                        {
                            "id_user": avis.id_user,
                            "id_meal": avis.id_meal,
                            "note": avis.note,
                            "commentaire": avis.commentaire,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            self.id_meal = res["id_meal"]
            created = True

        return created

        @log
        def obtenirAvisParRecette(self, recette:Recette) -> List:
            """Obtention des avis par recette

            Parameters
            ----------
            recette : Recette 
                La recette à partir de laquelle faire la recherche

            Returns
            -------
            res : List
                Liste contenant les avis correspondant à la recette indiquée
            """

            res = None

            try:
                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT * FROM avis JOIN recettes ON recettes.id_meal = avis.id_meal"
                            "WHERE id_meals = %(id_recette)s", 
                            {
                                "id_recette": recettes.id_meal,
                            },
                        )
                        res = cursor.fetchall()
            except Exception as e:
                logging.info(e)

            return res
            

