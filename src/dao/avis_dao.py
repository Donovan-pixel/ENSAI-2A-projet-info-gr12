import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.avis import Avis


class AvisDao(metaclass=Singleton):
    "Classe contenant les méthodes pour accéder aux avis de la base de données"

    @log
    def ajouter_avis(self):
        """Ajout d'un avis dans la base de données

        Parameters
        ----------
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
                            "id_user": self.id_user,
                            "id_meal": self.id_meal,
                            "note": self.note,
                            "commentaire": self.commentaire,
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


        def obtenirAvisParRecette(self, recette) -> List:
            """Ajout d'un avis dans la base de données

            Parameters
            ----------
            L'avis à ajouter

            Returns
            -------
            added : bool
                True si l'ajout est un succès
                False sinon
            """

            res = None

            

